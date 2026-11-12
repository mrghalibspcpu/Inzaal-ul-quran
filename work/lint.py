#!/usr/bin/env python3
"""Lint the completed entries in quran.db for common artefacts."""
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'quran.db'
progress = json.loads((ROOT / 'work' / 'progress.json').read_text())
ids = progress['completed_ayah_ids']

con = sqlite3.connect(DB)
pattern = re.compile(r'[A-Za-z0-9]|[\[\]{}]|،،|۔،|۔۔|\?\?|  +')
issues = 0
for (qid, tr, talighe) in con.execute(
        f"SELECT ID, tr, talighe FROM Quran WHERE ID IN ({','.join('?'*len(ids))}) ORDER BY ID", ids):
    for label, text in (('tr', tr), ('talighe', talighe)):
        m = pattern.search(text)
        if m:
            print(f'ID {qid} [{label}]: suspicious token {m.group()!r}')
            print('   ...', text[max(0, m.start()-60):m.end()+60].replace('\n', ' '))
            issues += 1
print()
print(f'{issues} suspicious spot(s) in {len(ids)} completed ayat')
