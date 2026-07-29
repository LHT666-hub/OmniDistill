from __future__ import annotations

import argparse
import mimetypes
import sys
from pathlib import Path

from common import read_csv, sha256_file, write_csv
from init_distillation_workspace import SOURCE_FIELDS


def source_kind(path: Path) -> str:
    name = path.name.lower()
    if any(word in name for word in ("interview", "transcript", "访谈", "对话")):
        return "interview"
    if any(word in name for word in ("chat", "slack", "email", "聊天", "邮件")):
        return "private-record"
    if path.suffix.lower() in {".pdf", ".doc", ".docx"}:
        return "document"
    if path.suffix.lower() in {".py", ".js", ".ts", ".java", ".r"}:
        return "code"
    return "artifact"


def main() -> int:
    parser = argparse.ArgumentParser(description="Register source files with provenance placeholders.")
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    raw_root = workspace / "sources" / "raw"
    index_path = workspace / "sources" / "source-index.csv"
    if not raw_root.is_dir() or not index_path.exists():
        print("Not an initialized OmniDistill workspace.", file=sys.stderr)
        return 2

    metadata: dict[str, dict[str, str]] = {}
    if args.metadata:
        for row in read_csv(args.metadata.resolve()):
            key = (row.get("path") or "").replace("\\", "/")
            if key:
                metadata[key] = row

    rows: list[dict[str, str]] = []
    seen_hashes: dict[str, str] = {}
    for number, path in enumerate(sorted(p for p in raw_root.rglob("*") if p.is_file()), 1):
        relative = path.relative_to(raw_root).as_posix()
        digest = sha256_file(path)
        meta = metadata.get(relative, {})
        kind = meta.get("source_kind") or source_kind(path)
        rights = meta.get("rights") or "unknown"
        consent = meta.get("consent") or ("required" if kind == "private-record" else "unknown")
        allowed = meta.get("allowed_use") or ("internal_only" if rights == "unknown" else "as_declared")
        duplicate_of = seen_hashes.get(digest, "")
        seen_hashes.setdefault(digest, f"S-{number:04d}")
        notes = meta.get("notes", "")
        if duplicate_of:
            notes = f"{notes}; duplicate_of={duplicate_of}".strip("; ")
        rows.append(
            {
                "source_id": f"S-{number:04d}",
                "path": relative,
                "sha256": digest,
                "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                "source_kind": kind,
                "author": meta.get("author", ""),
                "published_at": meta.get("published_at", ""),
                "access_level": meta.get("access_level", "full"),
                "rights": rights,
                "consent": consent,
                "independence_group": meta.get("independence_group", ""),
                "allowed_use": allowed,
                "notes": notes,
            }
        )
    write_csv(index_path, rows, SOURCE_FIELDS)
    print(f"Registered {len(rows)} source files in {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
