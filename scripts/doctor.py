from __future__ import annotations

import argparse
import compileall
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the OmniDistill runtime and bundled scripts.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    checks = {
        "python>=3.10": sys.version_info >= (3, 10),
        "skill": (root / "SKILL.md").is_file(),
        "agents": (root / "agents" / "openai.yaml").is_file(),
        "references": (root / "references").is_dir(),
        "scripts_compile": compileall.compile_dir(root / "scripts", quiet=1),
    }
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    return 0 if all(checks.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
