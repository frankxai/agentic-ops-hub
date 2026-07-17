import unittest
from pathlib import Path


class C940AutomationInstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = Path(__file__).parents[1] / "scripts" / "install_c940_automation.ps1"
        cls.text = cls.path.read_text(encoding="utf-8")

    def test_manages_required_tasks(self):
        for task in (
            "StarlightAgentWatchdog",
            "StarlightSecretScan",
            "StarlightSubstrateBackup",
            "StarlightMorningBrief",
            "StarlightCrossRepoIndexer",
            "ArcaneaAgentSurface",
        ):
            self.assertIn(task, self.text)

    def test_uses_absolute_pwsh_and_no_wscript_wrapper(self):
        self.assertIn("Get-Command pwsh", self.text)
        self.assertNotIn("wscript.exe", self.text.lower())
        self.assertNotIn("run-hidden.vbs", self.text.lower())

    def test_removes_indexer_storm_and_permanent_surface_watch(self):
        self.assertNotIn("PT5M", self.text)
        self.assertNotIn("-Watch", self.text)
        self.assertIn("New-HourlyTrigger", self.text)

    def test_enforces_bounded_non_overlapping_execution(self):
        self.assertIn("IgnoreNew", self.text)
        self.assertIn("ExecutionTimeLimit", self.text)
        self.assertIn("RunLevel Limited", self.text)


if __name__ == "__main__":
    unittest.main()
