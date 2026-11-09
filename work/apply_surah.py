#!/usr/bin/env python3
"""
Apply completed surah content to the deliverable quran.db.
Usage: python3 work/apply_surah.py work/content_s001.py [work/content_s002.py ...]
Each content module must define:
    SURAH = <chapter number>
    ENTRIES = { <Quran.ID: int>: (<tr>: str, <talighe>: str), ... }
Only tr and talighe are ever modified. All other columns, the schema,
indexes and row order are left exactly as they are.
"""
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'quran.db'
PROGRESS = ROOT / 'work' / 'progress.json'


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    if len(sys.argv) < 2:
        sys.exit('usage: apply_surah.py content_sNNN.py ...')
    progress = json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {'completed_ayah_ids': [], 'completed_surah_ids': []}
    completed = set(progress['completed_ayah_ids'])
    surah_ids = set(progress['completed_surah_ids'])
    con = sqlite3.connect(DB)
    try:
        for arg in sys.argv[1:]:
            path = Path(arg)
            mod = load_module(path)
            surah = int(mod.SURAH)
            entries = mod.ENTRIES
            # sanity: every entry id belongs to this surah and count matches
            rows = con.execute('SELECT ID, verse FROM Quran WHERE chapter=? ORDER BY verse', (surah,)).fetchall()
            expected_ids = [r[0] for r in rows]
            missing = [i for i in expected_ids if i not in entries]
            extra = [i for i in entries if i not in set(expected_ids)]
            if extra:
                sys.exit(f'{path}: IDs not in surah {surah}: {extra}')
            if missing:
                print(f'note: {len(missing)} ayah(s) of surah {surah} not in this file (partial apply OK)')
            for qid, (tr, talighe) in entries.items():
                if not tr.strip() or not talighe.strip():
                    sys.exit(f'{path}: empty tr/talighe at ID {qid}')
                con.execute('UPDATE Quran SET tr=?, talighe=? WHERE ID=?', (tr, talighe, qid))
                completed.add(qid)
            con.commit()
            print(f'applied surah {surah}: {len(entries)} ayat -> {path}')
    finally:
        con.close()
    con = sqlite3.connect(DB)
    full_surahs = []
    for ch in range(1, 115):
        ids = [r[0] for r in con.execute('SELECT ID FROM Quran WHERE chapter=?', (ch,))]
        if ids and all(i in completed for i in ids):
            full_surahs.append(ch)
    con.close()
    progress = {'completed_ayah_ids': sorted(completed), 'completed_surah_ids': full_surahs}
    PROGRESS.write_text(json.dumps(progress, indent=1), encoding='utf-8')
    print('progress saved:', progress['completed_surah_ids'], f'({len(completed)} ayat)')


if __name__ == '__main__':
    main()
