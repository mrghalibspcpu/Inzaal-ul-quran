#!/usr/bin/env python3
"""
Verify quran.db (deliverable) against work/quran.original.db (pristine).
Checks:
  1. integrity_check = ok on both
  2. schema objects (type,name,sql) identical
  3. row counts: Quran=6236, ChapterProperty=114, android_metadata=1
  4. every non-tr/talighe field of every row identical to original
  5. every completed ayah (from work/progress.json) has non-empty tr & talighe
  6. completion report per chapter
"""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / 'work' / 'quran.original.db'
DB = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'quran.db'
PROGRESS = ROOT / 'work' / 'progress.json'

failures = []

def check(cond, msg):
    tag = 'PASS' if cond else 'FAIL'
    print(f'[{tag}] {msg}')
    if not cond:
        failures.append(msg)

a = sqlite3.connect(ORIG)
b = sqlite3.connect(DB)

check(a.execute('PRAGMA integrity_check').fetchone()[0] == 'ok', 'original DB integrity_check ok')
check(b.execute('PRAGMA integrity_check').fetchone()[0] == 'ok', 'deliverable DB integrity_check ok')

schema_a = a.execute("SELECT type,name,sql FROM sqlite_master ORDER BY type,name").fetchall()
schema_b = b.execute("SELECT type,name,sql FROM sqlite_master ORDER BY type,name").fetchall()
check(schema_a == schema_b, 'schema objects (tables/indexes/views) identical')

check(a.execute('SELECT count(*) FROM Quran').fetchone()[0] == 6236, 'original has 6236 Quran rows')
check(b.execute('SELECT count(*) FROM Quran').fetchone()[0] == 6236, 'deliverable has 6236 Quran rows')
check(b.execute('SELECT count(*) FROM ChapterProperty').fetchone()[0] == 114, 'deliverable has 114 ChapterProperty records')
check(a.execute('SELECT sum(Verse) FROM ChapterProperty').fetchone()[0] == 6236, 'ChapterProperty verse total = 6236')

# row-level comparison of everything except tr/talighe
cols = ['ID', 'Arabic', 'chapter', 'verse', 'juz', 'hizb', 'page', 'search']
rows_a = a.execute(f'SELECT {",".join(cols)} FROM Quran ORDER BY ID').fetchall()
rows_b = b.execute(f'SELECT {",".join(cols)} FROM Quran ORDER BY ID').fetchall()
check(rows_a == rows_b, 'all fields other than tr/talighe are byte-identical to original')

rows_a_cp = a.execute('SELECT * FROM ChapterProperty ORDER BY Id').fetchall()
rows_b_cp = b.execute('SELECT * FROM ChapterProperty ORDER BY Id').fetchall()
check(rows_a_cp == rows_b_cp, 'ChapterProperty table unchanged')

rows_a_am = a.execute('SELECT * FROM android_metadata').fetchall()
rows_b_am = b.execute('SELECT * FROM android_metadata').fetchall()
check(rows_a_am == rows_b_am, 'android_metadata unchanged')

# chapter/verse order sanity
ids_b = [r[0] for r in b.execute('SELECT ID FROM Quran ORDER BY ID').fetchall()]
check(ids_b == list(range(1, 6237)), 'Quran IDs are 1..6236 in order')

if PROGRESS.exists():
    progress = json.loads(PROGRESS.read_text())
    completed = progress['completed_ayah_ids']
    if completed:
        placeholders = ','.join('?' * len(completed))
        bad = list(b.execute(f"SELECT ID FROM Quran WHERE ID IN ({placeholders}) AND (trim(tr)='' OR trim(talighe)='')", completed))
        check(not bad, f'all {len(completed)} completed ayat have non-empty tr and talighe')
    print('\nCompleted surahs:', progress['completed_surah_ids'])
    print('Completed ayat:', len(completed), '/ 6236')
    done = set(completed)
    print('\nPer-chapter completion (done/total):')
    for ch, total in b.execute('SELECT chapter, count(*) FROM Quran GROUP BY chapter ORDER BY chapter'):
        n = sum(1 for (i,) in b.execute('SELECT ID FROM Quran WHERE chapter=?', (ch,)) if i in done)
        if n:
            print(f'  surah {ch}: {n}/{total}')

print()
if failures:
    print(f'VERIFICATION FAILED: {len(failures)} problem(s)')
    sys.exit(1)
print('ALL CHECKS PASSED')
