from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path


INCLUDE_DIRS = ("agents", "assets", "references", "scripts")
INCLUDE_FILES = ("SKILL.md", "LICENSE")
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an installable OmniDistill Skill archive.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path("dist") / "omni-distill.zip")
    args = parser.parse_args()
    root = args.root.resolve()
    validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    if validator.is_file():
        result = subprocess.run([sys.executable, str(validator), str(root)], check=False)
        if result.returncode:
            return result.returncode
    elif not (root / "SKILL.md").is_file():
        print("SKILL.md is missing.", file=sys.stderr)
        return 2

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    files = [root / name for name in INCLUDE_FILES]
    for directory in INCLUDE_DIRS:
        files.extend(path for path in (root / directory).rglob("*") if path.is_file())
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(files)):
            if any(part in EXCLUDED_PARTS for part in path.parts):
                continue
            archive.write(path, Path("omni-distill") / path.relative_to(root))
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        if "omni-distill/SKILL.md" not in names or "omni-distill/agents/openai.yaml" not in names:
            print("Archive validation failed.", file=sys.stderr)
            return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
