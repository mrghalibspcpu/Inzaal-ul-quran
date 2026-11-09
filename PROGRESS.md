# Inzaal-ul-Quran — Urdu Translation + Tafsir Database — Progress

Deliverable: `quran.db` (ShiaVerse Android app) — modified copy of the original ShiaVerse Quran database.
Only `tr` (Urdu translation) and `talighe` (Urdu tafsir notes) are changed. All Arabic text, IDs,
chapter/verse numbers, juz/hizb/page, indexes and ChapterProperty metadata are byte-identical to the original.

## Completed surahs (verified)
- **Surah 1 — Al-Fatiha (7/7 ayat)** ✔ complete, checked
- **Surah 2 — Al-Baqarah (286/286 ayat)** ✔ complete, checked (verify.py ALL CHECKS PASSED)
- **Surah 3 — Al-i-Imran (200/200 ayat)** ✔ complete, checked (verify.py ALL CHECKS PASSED)

Progress: **493 / 6236 ayat** rewritten so far. See `work/progress.json`.

## How the work is stored (safe from loss)
Content modules (original Urdu wording, numbered-points tafsir) are committed under `work/content_*.py`.
To rebuild the deliverable at any time: copy the pristine original ShiaVerse `assets/quran.db` as `quran.db`,
then run `python3 work/apply_surah.py work/content_*.py` in ID order. `work/verify.py` audits the result.
The large binary DBs (`quran.db`, backups, pristine copy) are intentionally not committed mid-work.

## Verification tooling
- `work/verify.py` — integrity, schema/index equality, per-row non-tr/talighe diff vs original, counts.
- `work/lint.py` — suspicious-token scan of completed `tr`/`talighe` cells.

## Honest status
Surahs 1–3 are fully complete (493 ayat). Everything from Surah 4 — An-Nisa onwards (5,743 ayat)
remains to be rewritten and checked. `quran.db` at the repo root currently contains the completed work
for surahs 1–3. The final cumulative database will be committed at the repo root only when all 6,236
ayat are complete and verified — never before.
