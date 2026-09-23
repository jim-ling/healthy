#!/usr/bin/env python3
"""Build a local, source-traceable SQLite FTS5 index for health materials."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from pathlib import Path

TEXT_EXT = {".csv", ".tsv", ".json", ".md", ".txt", ".log"}
SKIP_PARTS = {"_clean_tmp", "__pycache__"}


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def row_text(row: dict[str, object]) -> str:
    return " | ".join(f"{k}: {v}" for k, v in row.items() if v not in (None, ""))


def records(path: Path):
    try:
        if path.suffix.lower() in {".csv", ".tsv"}:
            delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
            with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                for line, row in enumerate(reader, start=2):
                    yield line, row_text(row)
        elif path.suffix.lower() == ".json":
            obj = json.loads(path.read_text(encoding="utf-8", errors="replace"))
            if isinstance(obj, list):
                for i, item in enumerate(obj, start=1):
                    yield i, json.dumps(item, ensure_ascii=False)
            elif isinstance(obj, dict) and isinstance(obj.get("results"), list):
                for i, item in enumerate(obj["results"], start=1):
                    yield i, json.dumps(item, ensure_ascii=False)
            else:
                yield 1, json.dumps(obj, ensure_ascii=False)
        else:
            for line, text in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
                if text.strip():
                    yield line, text
    except (OSError, UnicodeError, json.JSONDecodeError, csv.Error) as exc:
        print(f"skip {path}: {exc}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=Path("/Users/mac/Documents/phatxm/meddata"))
    ap.add_argument("--db", type=Path, default=Path(".local/health_rag.sqlite3"))
    args = ap.parse_args()
    args.db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(args.db)
    con.executescript("""
      PRAGMA journal_mode=WAL;
      DROP TABLE IF EXISTS documents;
      DROP TABLE IF EXISTS chunks;
      CREATE TABLE documents(
        id INTEGER PRIMARY KEY, path TEXT UNIQUE, sha256 TEXT, source_type TEXT
      );
      CREATE TABLE chunks(
        id INTEGER PRIMARY KEY, document_id INTEGER, line INTEGER, text TEXT,
        FOREIGN KEY(document_id) REFERENCES documents(id)
      );
      CREATE VIRTUAL TABLE chunks_fts USING fts5(
        text, content='chunks', content_rowid='id', tokenize='unicode61'
      );
    """)
    file_count = chunk_count = 0
    for path in sorted(args.source.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXT:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        rel = str(path.relative_to(args.source))
        cur = con.execute(
            "INSERT INTO documents(path, sha256, source_type) VALUES (?, ?, ?)",
            (rel, file_hash(path), path.suffix.lower().lstrip(".")),
        )
        doc_id = cur.lastrowid
        file_count += 1
        for line, text in records(path):
            cur = con.execute("INSERT INTO chunks(document_id, line, text) VALUES (?, ?, ?)", (doc_id, line, text))
            con.execute("INSERT INTO chunks_fts(rowid, text) VALUES (?, ?)", (cur.lastrowid, text))
            chunk_count += 1
    con.commit()
    con.close()
    print(f"indexed files={file_count} chunks={chunk_count} db={args.db}")


if __name__ == "__main__":
    main()
