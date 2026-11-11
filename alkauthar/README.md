# Al-Kauthar — Deliverable Quran Database (`alkauthar/quran.db`)

This folder carries the modified ShiaVerse Quran database for the Al-Kauthar app, committed separately so a sandbox reset never destroys the deliverable.

## What this file is

`alkauthar/quran.db` is a copy of the working deliverable `quran.db` (repo root, gitignored by design). It is a **modified copy** of the pristine upstream ShiaVerse database (`mrghalibspcpu/ShiaVerse` → `assets/quran.db`, blob `b7f13f14332dfbe90dc57c9a762db19cf885b236`, 6,236 Quran rows).

Only two columns are changed versus the pristine original:

- `Quran.tr` — Urdu translation
- `Quran.talighe` — Urdu tafsir notes (three sections per ayah: theme, verse transliteration + line-by-line reading, practical lesson)

Everything else — Arabic text, IDs, chapter/verse numbers, juz/hizb/page, indexes, schema, `ChapterProperty` metadata, `android_metadata` — is **byte-identical** to the pristine original. `work/verify.py` re-checks all of this and reports ALL CHECKS PASSED.

## Snapshot status

- Committed: 2026-11-11, after Surah 66 (At-Tahrim) completion.
- Progress at snapshot: **5,241 / 6,236 ayat** rewritten (surahs 1–66 complete, 66 chapters fully translated & verified).
- sha256: `e13d8875a26963c57a09f8c1a825c4cffb1ea2384e7d5dd42a5773cc7e57abb7`
- Size: 14 MiB (16,943,104 bytes).
- Integrity: `pragma integrity_check` = ok; 6,236 rows; IDs 1..6236 in order.

This snapshot is refreshed at every surah completion (`cp quran.db alkauthar/quran.db` + commit). Check `git log -- alkauthar/` for the latest refresh, and `work/progress.json` for authoritative per-ayah state.

## How to install / use

Copy `alkauthar/quran.db` to the app's database location, replacing the stock file. No schema migration is needed.

## How to rebuild from source (if ever needed)

The canonical source of truth for the Urdu work is `content/**/content_s*.py` (tracked in git). To rebuild:

1. Fetch the pristine upstream blob (see `NEW_SESSION.md` for the exact recipe).
2. Place it as both `work/quran.original.db` and `quran.db`.
3. Replay all content modules: `find content -name '*.py' | sort | while read f; do python3 work/apply_surah.py "$f"; done`
4. `python3 work/lint.py && python3 work/verify.py`
5. `cp quran.db alkauthar/quran.db`
