from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import biscuit_demo


class Args:
    def __init__(self, project: str, name: str = "Test Project", tagline: str = "Does a useful thing", brand: str = "subtle", force: bool = False):
        self.project = project
        self.name = name
        self.tagline = tagline
        self.brand = brand
        self.force = force


class BiscuitDemoTests(unittest.TestCase):
    def test_init_creates_complete_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            project.mkdir()

            result = biscuit_demo.command_init(Args(str(project)))

            self.assertEqual(result, 0)
            demo = project / "demo"
            for filename in biscuit_demo.REQUIRED_DEMO_FILES:
                self.assertTrue((demo / filename).is_file(), filename)
            for dirname in ("sample-input", "sample-output", "screenshots"):
                self.assertTrue((demo / dirname).is_dir(), dirname)

    def test_json_handles_quotes_and_unicode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            project.mkdir()
            args = Args(
                str(project),
                name='Biscuit "Logic"',
                tagline="Listens → responds; café test",
            )

            self.assertEqual(biscuit_demo.command_init(args), 0)
            config = json.loads((project / "demo" / "demo-config.json").read_text(encoding="utf-8"))
            self.assertEqual(config["project"]["name"], args.name)
            self.assertEqual(config["project"]["tagline"], args.tagline)

    def test_init_does_not_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            project.mkdir()
            self.assertEqual(biscuit_demo.command_init(Args(str(project))), 0)

            script = project / "demo" / "demo-script.md"
            script.write_text("my edited script\n", encoding="utf-8")

            self.assertEqual(biscuit_demo.command_init(Args(str(project), name="Changed")), 0)
            self.assertEqual(script.read_text(encoding="utf-8"), "my edited script\n")

    def test_check_accepts_valid_packet_without_capture_tools(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            project.mkdir()
            self.assertEqual(biscuit_demo.command_init(Args(str(project))), 0)

            with patch.object(biscuit_demo, "_find_obs", return_value=None), patch.object(biscuit_demo.shutil, "which", return_value=None):
                self.assertEqual(biscuit_demo.command_check(Args(str(project))), 0)


if __name__ == "__main__":
    unittest.main()
