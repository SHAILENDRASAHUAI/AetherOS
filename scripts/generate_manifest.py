#!/usr/bin/env python3
import hashlib
import json
import os
import sys
from datetime import datetime, timezone


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "dist"
    if not os.path.isdir(output_dir):
        raise SystemExit(f"Output directory does not exist: {output_dir}")

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifacts": [],
    }

    for name in sorted(os.listdir(output_dir)):
        path = os.path.join(output_dir, name)
        if not os.path.isfile(path):
            continue
        if name.endswith(".sha256") or name.endswith("manifest.json"):
            continue
        digest = sha256(path)
        size = os.path.getsize(path)
        manifest["artifacts"].append({"name": name, "sha256": digest, "size": size})
        with open(path + ".sha256", "w", encoding="utf-8") as out:
            out.write(f"{digest}  {name}\n")

    with open(os.path.join(output_dir, "manifest.json"), "w", encoding="utf-8") as out:
        json.dump(manifest, out, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
