#!/usr/bin/env python3
"""Biscuit Demo: tiny hackathon demo preparation helper.

Python stdlib only. Intentionally boring.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
BRAND_MODES = {"subtle", "intro", "none"}
REQUIRED_DEMO_FILES = (
    "demo-config.json",
    "demo-script.md",
    "demo-checklist.md",
)


def render_template(name: str, values: dict[str, str]) -> str:
    path = TEMPLATES / name
    if not path.exists():
        raise FileNotFoundError(f"Template missing: {path}")
    text = path.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_safely(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return "skipped"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return "written"


def command_init(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    if not project.exists() or not project.is_dir():
        print(f"ERROR: project directory does not exist: {project}", file=sys.stderr)
        return 2

    demo = project / "demo"
    demo.mkdir(exist_ok=True)
    for folder in ("sample-input", "sample-output", "screenshots"):
        (demo / folder).mkdir(exist_ok=True)

    values = {
        "PROJECT_NAME": args.name,
        "TAGLINE": args.tagline,
        "BRAND_MODE": args.brand,
        "PROJECT_NAME_JSON": json.dumps(args.name, ensure_ascii=False),
        "TAGLINE_JSON": json.dumps(args.tagline, ensure_ascii=False),
        "BRAND_MODE_JSON": json.dumps(args.brand),
    }

    files = {
        "demo-config.json": render_template("demo-config.json", values),
        "demo-script.md": render_template("demo-script.md", values),
        "demo-checklist.md": render_template("demo-checklist.md", values),
    }

    print(f"Biscuit Demo → {project}")
    for filename, content in files.items():
        result = write_safely(demo / filename, content, args.force)
        marker = "✓" if result == "written" else "·"
        print(f"  {marker} {filename}: {result}")

    print("\nNext:")
    print(f'  python "{Path(__file__).resolve()}" check "{project}"')
    print("  Fill in demo/demo-script.md, then rehearse the visible action once before recording.")
    return 0


def _find_obs() -> str | None:
    for executable in ("obs", "obs64.exe", "obs.exe"):
        found = shutil.which(executable)
        if found:
            return found

    candidates: list[Path] = []
    if sys.platform == "darwin":
        candidates.append(Path("/Applications/OBS.app"))
    elif os.name == "nt":
        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        candidates.append(Path(program_files) / "obs-studio" / "bin" / "64bit" / "obs64.exe")

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def command_check(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    demo = project / "demo"
    failures: list[str] = []

    print(f"Biscuit Demo check → {project}")
    if not demo.is_dir():
        print("  ✗ demo/: missing")
        return 1

    for filename in REQUIRED_DEMO_FILES:
        path = demo / filename
        if path.is_file():
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename}: missing")
            failures.append(filename)

    config_path = demo / "demo-config.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            brand = config.get("branding", {}).get("mode")
            target = config.get("demo", {}).get("target_seconds")
            if brand not in BRAND_MODES:
                failures.append("invalid branding.mode")
                print(f"  ✗ branding.mode: {brand!r}")
            else:
                print(f"  ✓ branding.mode: {brand}")
            if not isinstance(target, int) or not 30 <= target <= 180:
                failures.append("invalid demo.target_seconds")
                print(f"  ✗ demo.target_seconds: {target!r}")
            else:
                print(f"  ✓ target length: {target}s")
        except (json.JSONDecodeError, OSError) as exc:
            failures.append("invalid demo-config.json")
            print(f"  ✗ config: {exc}")

    obs = _find_obs()
    ffmpeg = shutil.which("ffmpeg")
    print(f"  {'✓' if obs else '·'} OBS Studio: {obs or 'not found on this machine'}")
    print(f"  {'✓' if ffmpeg else '·'} FFmpeg: {ffmpeg or 'not found on PATH (optional)'}")

    for folder in ("sample-input", "sample-output", "screenshots"):
        path = demo / folder
        print(f"  {'✓' if path.is_dir() else '·'} {folder}/")

    if failures:
        print("\nNOT READY: fix the required demo packet items above.")
        return 1

    print("\nREADY: demo packet is structurally valid.")
    if not obs:
        print("Capture note: install/locate OBS on the machine you will record from.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="biscuit-demo",
        description="Prepare small, repeatable hackathon show-and-tell demos.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a demo packet inside an existing project")
    init.add_argument("project", help="Path to the existing project repository")
    init.add_argument("--name", required=True, help="Human-readable project name")
    init.add_argument("--tagline", required=True, help="One-sentence description")
    init.add_argument("--brand", choices=sorted(BRAND_MODES), default="subtle")
    init.add_argument("--force", action="store_true", help="Overwrite existing demo template files")
    init.set_defaults(func=command_init)

    check = sub.add_parser("check", help="Validate a project's demo packet and capture tools")
    check.add_argument("project", help="Path to the project repository")
    check.set_defaults(func=command_check)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
