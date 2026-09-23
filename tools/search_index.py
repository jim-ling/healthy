#!/usr/bin/env python3
"""Search the local health index and print traceable source locations."""
import argparse
import sqlite3
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("query", nargs="+")
ap.add_argument("--db", type=Path, default=Path(".local/health_rag.sqlite3"))
ap.add_argument("-n", type=int, default=10)
args = ap.parse_args()
query = " ".join(args.query)
con = sqlite3.connect(args.db)
rows = con.execute("""
  SELECT documents.path, chunks.line, chunks.text, bm25(chunks_fts) AS score
  FROM chunks_fts JOIN chunks ON chunks.id=chunks_fts.rowid
  JOIN documents ON documents.id=chunks.document_id
  WHERE chunks_fts MATCH ? ORDER BY score LIMIT ?
""", (query, args.n)).fetchall()
for path, line, text, score in rows:
    print(f"[{path}:{line}] {text[:800]}")
if not rows:
    print("no results")
