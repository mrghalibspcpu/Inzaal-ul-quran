# Inzaal-ul-Quran — Urdu Translation + Tafsir Database — Progress

Deliverable: `quran.db` (ShiaVerse Android app) — modified copy of the original ShiaVerse Quran database.
Only `tr` (Urdu translation) and `talighe` (Urdu tafsir notes) are changed. All Arabic text, IDs,
chapter/verse numbers, juz/hizb/page, indexes and ChapterProperty metadata are byte-identical to the original.

## Completed surahs (verified)
- **Surah 1 — Al-Fatiha (7/7 ayat)** ✔ complete, checked
- **Surah 2 — Al-Baqarah (286/286 ayat)** ✔ complete, checked (verify.py ALL CHECKS PASSED, lint 0 hits)
- **Surah 3 — Al-i-Imran** — in progress (10/200 ayat done)

Progress: **293 / 6236 ayat** rewritten so far. See `work/progress.json`.

## How the work is stored (safe from loss)
Content modules (original Urdu wording, numbered-points tafsir) are committed under `work/content_*.py`.
To rebuild the deliverable at any time: copy the pristine original ShiaVerse `assets/quran.db` as `quran.db`,
then run `python3 work/apply_surah.py work/content_*.py` in ID order. `work/verify.py` audits the result.
The large binary DBs (`quran.db`, backups, pristine copy) are intentionally not committed mid-work.

## Verification tooling
- `work/verify.py` — integrity, schema/index equality, per-row non-tr/talighe diff vs original, counts.
- `work/lint.py` — suspicious-token scan of completed `tr`/`talighe` cells.

## Honest status
Only surahs 1–2 are fully complete (293 ayat). Surah 3 is underway. Everything from Surah 3 (ayat 11+)
through Surah 114 remains to be rewritten and checked. `quran.db` at the repo root currently contains
the completed work for surahs 1–2 (and the in-progress surah 3 ayat as they land). The final cumulative
database will be committed at the repo root only when all 6,236 ayat are complete and verified.
