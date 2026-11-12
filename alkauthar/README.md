# Al-Kauthar — Deliverable Quran Database (`alkauthar/quran.db`)

This folder carries the modified ShiaVerse Quran database for the Al-Kauthar app, committed separately so a sandbox reset never destroys the deliverable.

## What this file is

`alkauthar/quran.db` is a copy of the working deliverable `quran.db` (repo root, gitignored by design). It is byte-identical to the committed root deliverable `inzaal-ul-quran.db` (same sha256). It is a **modified copy** of the pristine upstream ShiaVerse database (`mrghalibspcpu/ShiaVerse` → `assets/quran.db`, blob `b7f13f14332dfbe90dc57c9a762db19cf885b236`, 6,236 Quran rows).

Only two columns are changed versus the pristine original:

- `Quran.tr` — Urdu translation
- `Quran.talighe` — Urdu tafsir notes (three sections per ayah: theme, verse transliteration + line-by-line reading, practical lesson)

Everything else — Arabic text, IDs, chapter/verse numbers, juz/hizb/page, indexes, schema, `ChapterProperty` metadata, `android_metadata` — is **byte-identical** to the pristine original. `work/verify.py` re-checks all of this and reports ALL CHECKS PASSED.

## Snapshot status

- Refreshed: 2026-11-12 (Urdu translation & tafsir QA commit `eb1f2ee`) — **the Quran rewrite and QA pass are COMPLETE**.
- Progress at snapshot: **6,236 / 6,236 ayat** rewritten (all 114 chapters fully translated & verified).
- sha256: `3277241b844bcc33d4e84544f9121839a3723209b411bc04613471d90441c112`
- Size: ~11 MiB (11,062,272 bytes).
- Integrity: `pragma integrity_check` = ok; 6,236 rows; IDs 1..6236 in order.

## Note on `inzaal-ul-quran-shia.db`

A separate, Shia-enriched database is committed at the repository root as **`inzaal-ul-quran-shia.db`** (2026-11-12, sha256 `1ca5dfa6bd17d5cb4ce905e56b8a59578dfd4ff06136bb4e494805ac1dbd41ee`). It is the same base as this file PLUS, appended to every `talighe`:

- `اہلِ بیتؑ کا نکتہ` for **1,330 ayat** where BOTH Tafsir-e-Mubeen (Dr Hassan Rizvi, pristine ShiaVerse DB) and Tafsir al-Mizan (Arabic; CC BY-ND 4.0, used for reference/attribution) mention Ahl al-Bayt material.
- `ربط` (previous-verse link) for **6,122 ayat** — every ayah except each surah's first.

This `alkauthar/quran.db` snapshot intentionally remains the QA-refreshed non-enriched deliverable; copy root `inzaal-ul-quran-shia.db` instead if you want the Shia-enriched edition.

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
