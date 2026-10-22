import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

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


class LaunchConfigTests(unittest.TestCase):
    def block(self):
        return {"options": {"apiKey": "{env:AI_GATEWAY_API_KEY}"}}

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

    def test_allow_free_config_enables_opencode_and_disables_nothing(self):
        cfg = opencode_launch.build_launch_config("opencode/beam-free", allow_free=True, provider_block=self.block())
        self.assertEqual(cfg["enabled_providers"], ["vercel", "opencode"])
        self.assertNotIn("disabled_providers", cfg)

    def test_argv_is_standalone_and_keeps_the_variant_inside_dash_m(self):
        argv = opencode_launch.opencode_argv("vercel/zai/glm-5.3#medium", "do it", "oc")
        self.assertEqual(argv, ["oc", "run", "--standalone", "-m", "vercel/zai/glm-5.3#medium", "do it"])
        self.assertNotIn("--variant", argv)


class GatewayCredentialTests(unittest.TestCase):
    def test_env_key_becomes_a_reference_and_no_secret_is_written(self):
        block = opencode_launch.gateway_provider_block({"AI_GATEWAY_API_KEY": "x"}, Path("missing.json"))
        self.assertEqual(block["options"]["apiKey"], "{env:AI_GATEWAY_API_KEY}")

    def test_without_env_the_global_provider_block_is_copied(self):
        with tempfile.TemporaryDirectory() as tmp:
            block = opencode_launch.gateway_provider_block({}, global_config(Path(tmp)))
        self.assertEqual(block["options"]["apiKey"], KEY_FILE_VALUE)

    def test_no_credentials_anywhere_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            for path in (Path(tmp) / "absent.json", global_config(Path(tmp), key="")):
                with self.assertRaises(opencode_launch.LaunchError):
                    opencode_launch.gateway_provider_block({}, path)


class RunTests(unittest.TestCase):
    def run_launch(self, route_class="scout", allow_free=False):
        seen = {}

        def fake_runner(argv, env=None):
            seen["argv"], seen["env"] = argv, env
            directory = Path(env["OPENCODE_CONFIG_DIR"])
            seen["dir"] = directory
            seen["config"] = json.loads((directory / "opencode.json").read_text(encoding="utf-8"))
            return SimpleNamespace(returncode=0)

        base = {"AI_GATEWAY_API_KEY": "x", "OPENCODE_CONFIG": "hostile.json", "OPENCODE_CONFIG_CONTENT": "{}"}
        code = opencode_launch.run(route_class, "task", allow_free=allow_free, env=base, runner=fake_runner)
        return code, seen

    def test_launch_sets_the_config_dir_strips_overrides_and_cleans_up(self):
        code, seen = self.run_launch()
        self.assertEqual(code, 0)
        self.assertEqual(seen["argv"][1:5], ["run", "--standalone", "-m", GATEWAY])
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
            opencode_launch.run("scout", "t", env={"AI_GATEWAY_API_KEY": "x"}, runner=boom)
        self.assertFalse(holder["dir"].exists())

    def test_generated_file_holds_no_secret_when_the_key_comes_from_env(self):
        _, seen = self.run_launch()
        self.assertNotIn(KEY_FILE_VALUE, json.dumps(seen["config"]))
        self.assertEqual(seen["config"]["provider"]["vercel"]["options"]["apiKey"], "{env:AI_GATEWAY_API_KEY}")

    def test_unresolved_route_refuses_before_anything_is_written(self):
        called = []
        for bad in ("nonsense", "", None):
            with self.assertRaises(PlannerError):
                opencode_launch.run(bad, "t", env={"AI_GATEWAY_API_KEY": "x"}, runner=lambda *a, **k: called.append(1))
        self.assertEqual(called, [])

    def test_missing_credentials_refuse_before_launch(self):
        called = []
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(opencode_launch.LaunchError):
                opencode_launch.run("scout", "t", env={}, config_path=Path(tmp) / "none.json",
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
