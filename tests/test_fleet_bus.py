import contextlib
import io
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from scripts import fleet_bus


class FleetBusFreshnessTests(unittest.TestCase):
    def _write_beat(self, root: Path, machine: str, at: datetime):
        path = root / "heartbeats" / f"{machine}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"machine_id": machine, "status": "live", "at": at.isoformat()}),
            encoding="utf-8",
        )

    def test_stale_book_heartbeat_is_not_online(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "bus"
            self._write_beat(root, "yoga-book", datetime.now(timezone.utc) - timedelta(hours=12))
            with patch.object(fleet_bus, "BUS_ROOT", root):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    fleet_bus.cmd_status(None)
            data = json.loads(out.getvalue())
            self.assertFalse(data["book_online"])
            self.assertEqual(data["book_state"], "stale")
            self.assertFalse(data["heartbeats"][0]["fresh"])

    def test_fresh_book_heartbeat_is_online(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "bus"
            self._write_beat(root, "yoga-book", datetime.now(timezone.utc) - timedelta(minutes=5))
            with patch.object(fleet_bus, "BUS_ROOT", root):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    fleet_bus.cmd_status(None)
            data = json.loads(out.getvalue())
            self.assertTrue(data["book_online"])
            self.assertEqual(data["book_state"], "online")

    def test_swarm_line_labels_stale_book(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "bus"
            self._write_beat(root, "yoga-book", datetime.now(timezone.utc) - timedelta(hours=12))
            with patch.object(fleet_bus, "BUS_ROOT", root), patch.object(
                fleet_bus, "detect_machine", return_value="c940"
            ):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    fleet_bus.cmd_swarm_line(None)
            self.assertIn("book=STALE", out.getvalue())
            self.assertNotIn("book=ONLINE", out.getvalue())


if __name__ == "__main__":
    unittest.main()
