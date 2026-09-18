# -*- coding: utf-8 -*-
"""db_manifest.json 校验：逐文件重算 SHA-256 比对 + 检测未登记多余文件。

在仓根执行：python scripts/verify_manifest.py
任一不符 → 非零退出（发布流水线以退出码为门）。
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    mpath = ROOT / "db_manifest.json"
    m = json.loads(mpath.read_text(encoding="utf-8"))
    known = set()
    bad = []
    for f in m["files"]:
        p = ROOT / f["path"]
        known.add(f["path"])
        if not p.exists():
            bad.append((f["path"], "缺失"))
            continue
        b = p.read_bytes()
        if len(b) != f["bytes"] or hashlib.sha256(b).hexdigest() != f["sha256"]:
            bad.append((f["path"], "sha256/字节数不符"))
    extra = []
    dbdir = ROOT / "data" / "db"
    if dbdir.is_dir():
        for p in sorted(dbdir.iterdir()):
            rel = f"data/db/{p.name}"
            if rel not in known:
                extra.append(rel)
    if bad or extra:
        for path, why in bad:
            print(f"FAIL {path}: {why}")
        for path in extra:
            print(f"FAIL {path}: 未登记的多余文件")
        return 1
    print(f"OK {m['file_count']} 文件全部与清单一致"
          f"（upstream {m['upstream']['tag']}, {m['total_bytes']} 字节）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
