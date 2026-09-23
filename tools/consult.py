#!/usr/bin/env python3
"""Small traceable local consultation helper; it retrieves evidence, not diagnoses."""
import argparse
import re
import sqlite3
from pathlib import Path

ALIASES = {
    "睡眠": "sleep insomnia", "失眠": "sleep insomnia", "褪黑素": "melatonin",
    "癌症": "cancer oncology", "肿瘤": "cancer oncology", "疼痛": "pain headache",
    "病痛": "pain", "长寿": "longevity lifespan", "衰老": "aging ageing",
    "年轻": "aging longevity", "草药": "herb herbal botanical", "中药": "herb herbal",
    "补充剂": "supplement", "跌打损伤": "injury trauma pain", "肥胖": "obesity",
    "皮肤": "skin dermatology", "头痛": "headache", "鼻炎": "rhinitis",
}

ap = argparse.ArgumentParser(description="本地健康资料咨询检索（不替代诊断）")
ap.add_argument("question", nargs="+")
ap.add_argument("--db", type=Path, default=Path(".local/health_rag.sqlite3"))
ap.add_argument("-n", type=int, default=5)
args = ap.parse_args()
raw = " ".join(args.question)
expanded = " ".join([raw] + [v for k, v in ALIASES.items() if k in raw])
tokens = re.findall(r"[A-Za-z0-9_]+", expanded.lower())
query = " OR ".join(sorted(set(tokens)))
print(f"问题：{raw}")
print(f"检索词：{query or '（未识别到可检索词）'}")
print("说明：以下是资料线索，不是诊断、处方或疗效保证。")
if not query or not args.db.exists():
    print("请先运行：python3 tools/build_index.py")
    raise SystemExit(0)
con = sqlite3.connect(args.db)
rows = con.execute("""
  SELECT documents.path, chunks.line, chunks.text
  FROM chunks_fts JOIN chunks ON chunks.id=chunks_fts.rowid
  JOIN documents ON documents.id=chunks.document_id
  WHERE chunks_fts MATCH ? ORDER BY bm25(chunks_fts) LIMIT ?
""", (query, args.n)).fetchall()
for i, (path, line, text) in enumerate(rows, 1):
    print(f"\n{i}. {path}:{line}\n{text[:900]}")
if not rows:
    print("\n没有找到匹配资料；需要增加同义词、英文术语或补充数据源。")
