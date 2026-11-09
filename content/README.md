# Urdu Translation + Tafsir — completed content, arranged surah by surah

Each folder holds the original Urdu translation (`tr`) and tafsir (`talighe`)
for one surah, split into small parts of ~10 ayat each. Nothing else from the
database was ever touched — Arabic text, IDs, chapter/verse numbers,
juz/hizb/page, indexes and chapter metadata are byte-identical to the
original upstream database.

```
content/
  surah-001/content_s001.py       (Surah 1  — Al-Fatiha, 7 ayat)
  surah-002/content_s002_pNN.py   (Surah 2  — Al-Baqarah, 286 ayat, parts 01–29)
  surah-003/content_s003_pNN.py   (Surah 3  — Al-i-Imran, 200 ayat, parts 01–20)
  surah-004/content_s004_pNN.py   (Surah 4  — An-Nisa, 176 ayat, parts 01–18)
  surah-005/content_s005_pNN.py   (Surah 5  — Al-Ma'ida, 120 ayat, parts 01–12)
  surah-006/content_s006_pNN.py   (Surah 6  — Al-An'am, 165 ayat, in progress)
  ...
```

Part numbering follows Ayat order (1..N). Each module defines:

```python
SURAH = <chapter number>
ENTRIES = { <Quran.ID: int>: (<tr>: str, <talighe>: str), ... }
```

## Rebuilding the deliverable from scratch

```sh
cp quran.db quran.db.keep            # back up current deliverable
cp work/quran.original.db quran.db   # pristine upstream copy (gitignored)
for f in $(find content -name '*.py' | sort); do python3 work/apply_surah.py "$f"; done
python3 work/verify.py               # must print ALL CHECKS PASSED
```

`work/verify.py` audits: SQLite integrity, schema/index equality with the
original, per-row equality of every non-`tr`/`talighe` column vs the original,
and completeness of all completed ayat. `work/lint.py` scans completed cells
for suspicious Latin tokens.

Status and counts: see `PROGRESS.md` at the repo root and `work/progress.json`.
