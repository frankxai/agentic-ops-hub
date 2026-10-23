import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from fleet import route_executor as router

from fleet import opencode_launch
from fleet.token_planner import PlannerError

KEY_FILE_VALUE = "TEST-ONLY-NOT-A-KEY"
GATEWAY = "vercel/deepseek/deepseek-v4.1-flash"


def global_config(tmp: Path, *, key=KEY_FILE_VALUE, hostile=True) -> Path:
    cfg = {"model": "opencode/beam-free", "small_model": "opencode/beam-free",
           "enabled_providers": ["opencode", "vercel"] if hostile else ["vercel"],
           "provider": {"vercel": {"options": {"apiKey": key}}}}
    path = tmp / "opencode.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    return path


class IsolatedLedger(unittest.TestCase):
    def setUp(self):
        self.ledger_tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.ledger_tmp.cleanup)
        env = patch.dict(os.environ, {"STARLIGHT_RECEIPTS_DIR": self.ledger_tmp.name})
        env.start()
        self.addCleanup(env.stop)


class LaunchConfigTests(unittest.TestCase):
    def block(self):
        return opencode_launch.gateway_provider_block()

    def test_strict_config_pins_model_and_small_model_and_whitelists_only_the_gateway(self):
        cfg = opencode_launch.build_launch_config("vercel/zai/glm-5.3#medium", allow_free=False, provider_block=self.block())
        self.assertEqual(cfg["model"], "vercel/zai/glm-5.3")  # a config file takes no variant suffix
        self.assertEqual(cfg["small_model"], "vercel/zai/glm-5.3")
        self.assertEqual(cfg["enabled_providers"], ["vercel"])
        self.assertIn("opencode", cfg["disabled_providers"])
        self.assertNotIn("opencode/", json.dumps(cfg))

    def test_strict_config_refuses_a_non_gateway_model(self):
        with self.assertRaises(opencode_launch.LaunchError):
            opencode_launch.build_launch_config("opencode/beam-free", allow_free=False, provider_block=self.block())

    def test_free_primary_config_cannot_make_paid_gateway_side_calls(self):
        cfg = opencode_launch.build_launch_config("opencode/beam-free", allow_free=True, provider_block=self.block())
        self.assertEqual(cfg["enabled_providers"], ["opencode"])
        self.assertIn("vercel", cfg["disabled_providers"])
        self.assertEqual(cfg["provider"], {})

    def test_paid_primary_stays_gateway_only_even_with_free_opt_in(self):
        cfg = opencode_launch.build_launch_config("vercel/zai/glm-5.3#medium", allow_free=True,
                                                  provider_block=self.block())
        self.assertEqual(cfg["enabled_providers"], ["vercel"])
        self.assertIn("opencode", cfg["disabled_providers"])
        self.assertIn("omniroute", cfg["disabled_providers"])

    def test_argv_is_standalone_and_keeps_the_variant_inside_dash_m(self):
        argv = opencode_launch.opencode_argv("vercel/zai/glm-5.3#medium", "do it", "oc")
        self.assertEqual(argv, ["oc", "run", "--standalone", "-m", "vercel/zai/glm-5.3#medium", "--", "do it"])
        self.assertNotIn("--variant", argv)


class GatewayCredentialTests(unittest.TestCase):
    def test_provider_block_is_fixed_and_carries_no_override_or_secret(self):
        block = opencode_launch.gateway_provider_block()
        self.assertEqual(block, {"options": {"apiKey": "{env:AI_GATEWAY_API_KEY}"}})

    def test_env_key_needs_no_file_and_nothing_is_injected(self):
        self.assertIsNone(opencode_launch.gateway_key({"AI_GATEWAY_API_KEY": "x"}, Path("missing.json")))

    def test_only_the_api_key_is_taken_from_the_global_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = global_config(Path(tmp))
            data = json.loads(path.read_text(encoding="utf-8"))
            data["provider"]["vercel"].update({"npm": "evil", "api": "https://evil.example", "models": {"a": {}}})
            data["provider"]["vercel"]["options"]["baseURL"] = "https://nongateway.example/v1"
            path.write_text(json.dumps(data), encoding="utf-8")
            key = opencode_launch.gateway_key({}, path)
            self.assertEqual(key, KEY_FILE_VALUE)
            cfg = opencode_launch.build_launch_config(GATEWAY, allow_free=False,
                                                      provider_block=opencode_launch.gateway_provider_block())
        text = json.dumps(cfg)
        for hostile in ("nongateway", "evil", "baseURL", KEY_FILE_VALUE):
            self.assertNotIn(hostile, text)

    def test_no_credentials_anywhere_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            for path in (Path(tmp) / "absent.json", global_config(Path(tmp), key=""),
                         global_config(Path(tmp), key="{env:SOMETHING}")):
                with self.assertRaises(opencode_launch.LaunchError):
                    opencode_launch.gateway_key({}, path)


class BinaryResolutionTests(unittest.TestCase):
    def test_batch_shim_is_never_returned_and_the_native_exe_is_used(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "node_modules" / "@opencode" / "cli" / "bin" / "opencode.exe"
            exe.parent.mkdir(parents=True)
            exe.write_text("", encoding="utf-8")
            got = opencode_launch.resolve_opencode(str(Path(tmp) / "opencode.CMD"), windows=True)
            self.assertEqual(Path(got), exe)

    def test_only_a_shim_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(opencode_launch.LaunchError):
                opencode_launch.resolve_opencode(str(Path(tmp) / "opencode.cmd"), windows=True)

    def test_missing_opencode_is_refused_and_posix_path_is_kept(self):
        with self.assertRaises(opencode_launch.LaunchError):
            opencode_launch.resolve_opencode(found="", windows=False)
        self.assertEqual(opencode_launch.resolve_opencode("/usr/bin/opencode", windows=False), "/usr/bin/opencode")


class ShellInjectionTests(IsolatedLedger):
    TASK = 'x" & echo MARKER & rem "'

    def test_task_with_cmd_metacharacters_reaches_the_child_as_one_literal_argument(self):
        argv = opencode_launch.opencode_argv("vercel/zai/glm-5.3", self.TASK, sys.executable)
        # Real process boundary, no model call: the child is Python echoing its own argv back.
        probe = argv[:1] + ["-c", "import sys,json;print(json.dumps(sys.argv[1:]))"] + argv[argv.index("--"):]
        out = subprocess.run(probe, capture_output=True, text=True, shell=False)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(json.loads(out.stdout), ["--", self.TASK])

    def test_launch_uses_shell_false_and_the_resolved_binary(self):
        seen = {}

        def fake_runner(argv, env=None):
            seen["argv"] = argv
            return SimpleNamespace(returncode=0)

        opencode_launch.run("scout", self.TASK, env={"AI_GATEWAY_API_KEY": "x"}, binary="C:/bin/opencode.exe",
                            allowance_usd=0.01, runner=fake_runner)
        self.assertEqual(seen["argv"][0], "C:/bin/opencode.exe")
        self.assertEqual(seen["argv"][-2:], ["--", self.TASK])


class SupervisionTests(IsolatedLedger):
    def test_timeout_kills_the_child_and_its_descendant(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "alive.txt"
            grandchild = ("import time,pathlib\nwhile True:\n pathlib.Path(r'%s').write_text(str(time.time()))\n"
                          " time.sleep(0.1)" % marker)
            parent = ("import subprocess,sys,time\nsubprocess.Popen([sys.executable,'-c',%r])\ntime.sleep(60)" % grandchild)
            t0 = time.time()
            with self.assertRaises(subprocess.TimeoutExpired):
                opencode_launch.supervised_run([sys.executable, "-c", parent], env=dict(os.environ), timeout=2)
            self.assertLess(time.time() - t0, 20)
            time.sleep(0.5)
            stamp = marker.read_text() if marker.exists() else "0"
            time.sleep(0.8)
            self.assertEqual(stamp, marker.read_text() if marker.exists() else "0", "the grandchild kept running")

    @unittest.skipUnless(os.name == "nt", "Windows Job-object containment")
    def test_windows_descendant_spawned_immediately_is_contained(self):
        with tempfile.TemporaryDirectory() as tmp:
            pidfile = Path(tmp) / "pid.txt"
            sleeper = "import time;time.sleep(60)"
            parent = ("import subprocess,sys,time;"
                      "p=subprocess.Popen([sys.executable,'-c',%r]);"
                      "open(r'%s','w').write(str(p.pid));"
                      "time.sleep(60)" % (sleeper, pidfile))
            with self.assertRaises(subprocess.TimeoutExpired):
                opencode_launch.supervised_run([sys.executable, "-c", parent], env=dict(os.environ), timeout=1.5)
            time.sleep(0.5)
            self.assertTrue(pidfile.exists(), "the parent must have started and spawned its child")
            pid = int(pidfile.read_text())
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True, errors="replace").stdout or ""
            self.assertNotIn(str(pid), out, "the immediately spawned descendant survived containment")

    def test_windows_job_setup_failure_runs_nothing(self):
        if os.name != "nt":
            self.skipTest("Windows only")
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "ran.txt"
            code = "open(r'%s','w').write('x')" % marker
            with patch.object(opencode_launch, "_windows_job", side_effect=OSError("boom")):
                with self.assertRaises(opencode_launch.LaunchError):
                    opencode_launch.supervised_run([sys.executable, "-c", code], env=dict(os.environ), timeout=5)
            time.sleep(0.5)
            self.assertFalse(marker.exists(), "a child must not run when it cannot be contained")

    def test_return_code_propagates(self):
        res = opencode_launch.supervised_run([sys.executable, "-c", "raise SystemExit(7)"], env=dict(os.environ))
        self.assertEqual(res.returncode, 7)

    def test_launch_directory_is_removed_when_the_run_times_out(self):
        holder = {}

        def slow(argv, env=None, timeout=None):
            holder["dir"] = Path(env["OPENCODE_CONFIG_DIR"])
            raise subprocess.TimeoutExpired(argv, timeout)

        with self.assertRaises(subprocess.TimeoutExpired):
            opencode_launch.run("scout", "t", env={"AI_GATEWAY_API_KEY": "x"}, binary="oc", timeout=1, allowance_usd=0.01, runner=slow)
        self.assertFalse(holder["dir"].exists())

    def test_global_file_key_goes_to_the_child_environment_never_to_disk(self):
        seen = {}

        def fake_runner(argv, env=None):
            seen["env"] = env
            seen["text"] = (Path(env["OPENCODE_CONFIG_DIR"]) / "opencode.json").read_text(encoding="utf-8")
            return SimpleNamespace(returncode=0)

        with tempfile.TemporaryDirectory() as tmp:
            opencode_launch.run("scout", "t", env={}, config_path=global_config(Path(tmp)), binary="oc",
                                allowance_usd=0.01, runner=fake_runner)
        self.assertEqual(seen["env"]["AI_GATEWAY_API_KEY"], KEY_FILE_VALUE)
        self.assertNotIn(KEY_FILE_VALUE, seen["text"])


class RunTests(IsolatedLedger):
    def run_launch(self, route_class="scout", allow_free=False):
        seen = {}

        def fake_runner(argv, env=None):
            seen["argv"], seen["env"] = argv, env
            directory = Path(env["OPENCODE_CONFIG_DIR"])
            seen["dir"] = directory
            seen["config"] = json.loads((directory / "opencode.json").read_text(encoding="utf-8"))
            return SimpleNamespace(returncode=0)

        base = {"AI_GATEWAY_API_KEY": "x", "OPENCODE_CONFIG": "hostile.json", "OPENCODE_CONFIG_CONTENT": "{}"}
        code = opencode_launch.run(route_class, "task", allow_free=allow_free, env=base, binary="oc", allowance_usd=None if allow_free else 0.01, runner=fake_runner)
        return code, seen

    def test_launch_sets_the_config_dir_strips_overrides_and_cleans_up(self):
        code, seen = self.run_launch()
        self.assertEqual(code, 0)
        self.assertEqual(seen["argv"][1:5], ["run", "--standalone", "-m", GATEWAY])
        self.assertEqual(seen["argv"][-2:], ["--", "task"])
        self.assertEqual(seen["env"]["OPENCODE_CONFIG_DIR"], str(seen["dir"]))
        self.assertNotIn("OPENCODE_CONFIG", seen["env"])
        self.assertNotIn("OPENCODE_CONFIG_CONTENT", seen["env"])
        self.assertEqual(seen["config"]["small_model"], GATEWAY)
        self.assertEqual(seen["config"]["enabled_providers"], ["vercel"])
        self.assertFalse(seen["dir"].exists(), "the launch directory must be removed after the run")

    def test_cleanup_happens_when_the_run_raises(self):
        holder = {}

        def boom(argv, env=None):
            holder["dir"] = Path(env["OPENCODE_CONFIG_DIR"])
            raise RuntimeError("crash")

        with self.assertRaises(RuntimeError):
            opencode_launch.run("scout", "t", env={"AI_GATEWAY_API_KEY": "x"}, binary="oc", allowance_usd=0.01, runner=boom)
        self.assertFalse(holder["dir"].exists())

    def test_generated_file_holds_no_secret_when_the_key_comes_from_env(self):
        _, seen = self.run_launch()
        self.assertNotIn(KEY_FILE_VALUE, json.dumps(seen["config"]))
        self.assertEqual(seen["config"]["provider"]["vercel"]["options"]["apiKey"], "{env:AI_GATEWAY_API_KEY}")

    def test_unresolved_route_refuses_before_anything_is_written(self):
        called = []
        for bad in ("nonsense", "", None):
            with self.assertRaises(PlannerError):
                opencode_launch.run(bad, "t", env={"AI_GATEWAY_API_KEY": "x"}, binary="oc",
                                    runner=lambda *a, **k: called.append(1))
        self.assertEqual(called, [])

    def test_missing_credentials_refuse_before_launch(self):
        called = []
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(opencode_launch.LaunchError):
                opencode_launch.run("scout", "t", env={}, config_path=Path(tmp) / "none.json", binary="oc",
                                    runner=lambda *a, **k: called.append(1))
        self.assertEqual(called, [])

    def test_allow_free_launch_is_opt_in(self):
        _, seen = self.run_launch(allow_free=True)
        self.assertIn("opencode", seen["config"]["enabled_providers"])
        _, strict = self.run_launch()
        self.assertNotIn("opencode", strict["config"]["enabled_providers"])

    def test_main_refuses_with_exit_2_on_unknown_class_and_empty_task(self):
        self.assertEqual(opencode_launch.main(["--class", "nonsense", "--", "task"]), 2)
        self.assertEqual(opencode_launch.main(["--class", "scout", "--"]), 2)

    def test_launch_dir_file_is_created_exclusively(self):
        with opencode_launch.launch_dir({"model": "vercel/x/y"}) as directory:
            with self.assertRaises(FileExistsError):
                os.close(os.open(directory / "opencode.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL))


class PaidAdmissionTests(IsolatedLedger):
    def launch(self, **kw):
        options = dict(env={"AI_GATEWAY_API_KEY": "synthetic-key"}, binary="oc", allowance_usd=0.01,
                       runner=lambda *a, **k: SimpleNamespace(returncode=0))
        options.update(kw)
        return opencode_launch.run("scout", "test fixture", **options)

    def test_missing_or_invalid_allowance_refuses_before_runner(self):
        called = []
        for bad in (None, 0, -1, float("inf"), float("nan"), True):
            with self.assertRaises(ValueError):
                self.launch(allowance_usd=bad, runner=lambda *a, **k: called.append(True))
        self.assertEqual(called, [])
        self.assertEqual(router.reservations(), [])

    def test_allowance_over_class_ceiling_refuses_before_runner(self):
        called = []
        with self.assertRaises(router.BudgetError):
            self.launch(allowance_usd=1, runner=lambda *a, **k: called.append(True))
        self.assertEqual(called, [])

    def test_exhausted_monthly_ledger_cannot_launch(self):
        from datetime import datetime, timezone
        ledger = Path(self.ledger_tmp.name) / "routing.jsonl"
        ledger.write_text(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "cost_usd": 80,
                                      "used": GATEWAY, "pool": "token-pass"}) + "\n")
        called = []
        with self.assertRaises(router.BudgetError):
            self.launch(runner=lambda *a, **k: called.append(True))
        self.assertEqual(called, [])

    def test_two_concurrent_launches_cannot_reserve_the_same_headroom(self):
        import copy
        from concurrent.futures import ThreadPoolExecutor
        schema = copy.deepcopy(router.load_schema())
        schema["token_pass"]["hard_cap_usd"] = 0.01
        called = []
        def launch_one(_):
            try:
                self.launch(runner=lambda *a, **k: (called.append(True) or SimpleNamespace(returncode=0)))
                return "launched"
            except router.BudgetError:
                return "refused"
        with patch.object(router, "load_schema", return_value=schema):
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(launch_one, range(2)))
        self.assertCountEqual(results, ["launched", "refused"])
        self.assertEqual(len(called), 1)
        self.assertEqual(len(router.reservations()), 1)

    def test_success_surfaces_unresolved_hold_without_a_fake_zero_receipt(self):
        events = []
        self.assertEqual(self.launch(on_admission=events.append), 0)
        self.assertEqual(events[0]["usage_state"], "unresolved")
        self.assertEqual(events[0]["held_usd"], 0.01)
        self.assertEqual(router.reservations()[0]["id"], events[0]["reservation_id"])
        self.assertFalse((Path(self.ledger_tmp.name) / "routing.jsonl").exists())
        self.assertNotIn("synthetic-key", json.dumps(events))

    def test_callback_failure_releases_the_hold_before_runner_entry(self):
        called = []
        def callback(_):
            raise RuntimeError("cannot persist admission")
        with self.assertRaises(RuntimeError):
            self.launch(on_admission=callback, runner=lambda *a, **k: called.append(True))
        self.assertEqual(called, [])
        self.assertEqual(router.reservations(), [])

    def test_missing_executable_refuses_before_reservation(self):
        with patch.object(opencode_launch, "resolve_opencode", side_effect=opencode_launch.LaunchError("missing")):
            with self.assertRaises(opencode_launch.LaunchError):
                self.launch(binary=None)
        self.assertEqual(router.reservations(), [])

    def test_nonzero_timeout_and_runner_error_keep_unknown_usage_reserved(self):
        runners = [lambda *a, **k: SimpleNamespace(returncode=1),
                   lambda *a, **k: (_ for _ in ()).throw(subprocess.TimeoutExpired("oc", 1)),
                   lambda *a, **k: (_ for _ in ()).throw(OSError("unknown launch outcome"))]
        for runner in runners:
            before = len(router.reservations())
            try:
                self.launch(runner=runner)
            except (subprocess.TimeoutExpired, OSError):
                pass
            self.assertEqual(len(router.reservations()), before + 1)
        self.assertFalse((Path(self.ledger_tmp.name) / "routing.jsonl").exists())

    def test_explicit_free_route_does_not_require_paid_allowance(self):
        self.assertEqual(self.launch(allow_free=True, allowance_usd=None, env={}), 0)
        self.assertEqual(router.reservations(), [])


class ConsumerDeadlineTests(unittest.TestCase):
    def test_wrapper_argv_carries_the_timeout_before_the_task(self):
        argv = opencode_launch.wrapper_argv("scout", "t", timeout=100.9)
        self.assertEqual(argv[argv.index("--timeout") + 1], "100")
        self.assertLess(argv.index("--timeout"), argv.index("--"))
        self.assertNotIn("--timeout", opencode_launch.wrapper_argv("scout", "t"))

    def test_capacity_probe_wrapper_deadline_is_shorter_than_the_outer_one(self):
        from scripts import cli_capacity
        argv = cli_capacity.opencode_probe_command(allowance_usd=0.01)
        inner = int(argv[argv.index("--timeout") + 1])
        self.assertLess(inner, cli_capacity.LIVE_PROBE_TIMEOUT_S)


class WrapperCommandTests(unittest.TestCase):
    def test_wrapper_argv_is_self_contained(self):
        argv = opencode_launch.wrapper_argv("code", "fix it", allow_free=False)
        self.assertEqual(argv[:2], ["python", "-B"])
        self.assertTrue(argv[2].endswith("opencode_launch.py"))
        self.assertEqual(argv[3:5], ["--class", "code"])
        self.assertEqual(argv[-2:], ["--", "fix it"])
        self.assertIn("--allow-free", opencode_launch.wrapper_argv("code", "t", allow_free=True))


if __name__ == "__main__":
    unittest.main()
