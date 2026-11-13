# Al-Kauthar — Deliverable Quran Database (`alkauthar/quran.db`)

This folder carries the modified ShiaVerse Quran database for the Al-Kauthar app, committed separately so a sandbox reset never destroys the deliverable.

## What this file is

`alkauthar/quran.db` is a copy of the working deliverable `quran.db` (repo root, gitignored by design). It is byte-identical to the committed root deliverable `inzaal-ul-quran.db` (same sha256). It is a **modified copy** of the pristine upstream ShiaVerse database (`mrghalibspcpu/ShiaVerse` → `assets/quran.db`, blob `b7f13f14332dfbe90dc57c9a762db19cf885b236`, 6,236 Quran rows).

Only two columns are changed versus the pristine original:

- `Quran.tr` — Urdu translation
- `Quran.talighe` — Urdu tafsir notes (three sections per ayah: theme, verse transliteration + line-by-line reading, practical lesson)

Everything else — Arabic text, IDs, chapter/verse numbers, juz/hizb/page, indexes, schema, `ChapterProperty` metadata, `android_metadata` — is **byte-identical** to the pristine original. `work/verify.py` re-checks all of this and reports ALL CHECKS PASSED.

## Snapshot status

- Refreshed: 2026-11-13 — now carrying the rewritten Urdu work **plus the curated Ahl al-Bayt points** (this snapshot is no longer the non-enriched one).
- Progress at snapshot: **6,236 / 6,236 ayat** rewritten (all 114 chapters fully translated & verified).
- sha256: `0d8f0fe6eb4eb2d2f66ffaa366eb5fa6bd888e92f2bb3c3cd6810a394f979968`
- Size: ~11 MB (11,078,656 bytes).
- Integrity: `pragma integrity_check` = ok; 6,236 rows; IDs 1..6236 in order. Contains `اہلِ بیتؑ کا نکتہ` in **20 ayat only** (the ayat about/attributed to Ahl al-Bayt), and **no `ربط` lines anywhere**.

## Note on `inzaal-ul-quran-shia.db`

The separate, Shia-enriched `inzaal-ul-quran-shia.db` (2026-11-12) was **removed from the repository root at the user's request on 2026-11-13**. Its contents are superseded by the curated build: the root `inzaal-ul-quran.db` and this snapshot now carry hand-written, easy عام فہم Urdu Ahl al-Bayt points for the 20 ayat about (or attributed to) Ahl al-Bayt — sourced from BOTH Tafsir-e-Mubeen and Tafsir al-Mizan — and contain **no previous-verse `ربط` sections** anywhere.

This snapshot is refreshed at every surah completion (`cp quran.db alkauthar/quran.db` + commit). Check `git log -- alkauthar/` for the latest refresh, and `work/progress.json` for authoritative per-ayah state.

## How to install / use

Copy `alkauthar/quran.db` to the app's database location, replacing the stock file. No schema migration is needed.

## How to rebuild from source (if ever needed)

The canonical source of truth for the Urdu work is `content/**/content_s*.py` (tracked in git). To rebuild:

1. Fetch the pristine upstream blob (see `NEW_SESSION.md` for the exact recipe).
2. Place it as both `work/quran.original.db` and `quran.db`.
3. Replay all content modules: `find content -name '*.py' | sort | while read f; do python3 work/apply_surah.py "$f"; done`
4. `python3 work/lint.py && python3 work/verify.py`
5. `cp quran.db inzaal-ul-quran.db` (or a chosen deliverable path)
6. `python3 work/enrich_shia.py inzaal-ul-quran.db` — appends the 20 curated `اہلِ بیتؑ کا نکتہ` lines only (idempotent)
7. `cp inzaal-ul-quran.db alkauthar/quran.db` (this file, byte-identical)
8. Re-check: `python3 work/lint.py alkauthar/quran.db && python3 work/verify.py alkauthar/quran.db`
