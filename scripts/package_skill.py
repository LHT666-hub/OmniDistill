from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

from validate_distillation_package import validate


EXCLUDES = {".git", "__pycache__", ".pytest_cache", "dist", "snapshots"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and package one generated Skill.")
    parser.add_argument("package", type=Path)
    parser.add_argument("--output", type=Path, default=Path("dist"))
    args = parser.parse_args()
    package = args.package.resolve()
    errors, warnings, achieved = validate(package)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    output_dir = args.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{package.name}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as handle:
        for path in sorted(p for p in package.rglob("*") if p.is_file()):
            if any(part in EXCLUDES for part in path.parts):
                continue
            handle.write(path, Path(package.name) / path.relative_to(package))
    print(f"{archive} ({achieved})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
