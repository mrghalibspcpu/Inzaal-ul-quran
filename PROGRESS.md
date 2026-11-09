# Inzaal-ul-Quran — Urdu Translation + Tafsir Database — Progress

Deliverable: `quran.db` (ShiaVerse Android app) — modified copy of the original ShiaVerse Quran database.
Only `tr` (Urdu translation) and `talighe` (Urdu tafsir notes) are changed. All Arabic text, IDs,
chapter/verse numbers, juz/hizb/page, indexes and ChapterProperty metadata are byte-identical to the original.

## Completed surahs (verified)
- **Surah 1 — Al-Fatiha (7/7 ayat)** ✔ complete
- **Surah 2 — Al-Baqarah (286/286 ayat)** ✔ complete
- **Surah 3 — Al-i-Imran (200/200 ayat)** ✔ complete
- **Surah 4 — An-Nisa (176/176 ayat)** ✔ complete
- **Surah 5 — Al-Ma'ida (120/120 ayat)** ✔ complete
- **Surah 6 — Al-An'am (165/165 ayat)** ✔ complete
- **Surah 7 — Al-A'raf (206/206 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)

Progress: **1,160 / 6,236 ayat** rewritten so far. See `work/progress.json`.

## Repo layout (content arranged surah by surah)
Completed work is tracked under **`content/surah-NNN/`** — one folder per surah,
part files of ~10 ayat each (surah 7 also has a small `p22` catch-up file for ayat 81-84).
See `content/README.md` for the exact layout and the full rebuild instructions.

## How the work is stored (safe from loss)
The translated content is committed under `content/surah-NNN/*.py` — sorted order is apply order.
Rebuild recipe: `content/README.md`. The large binary DBs (`quran.db` deliverable,
`work/quran.original.db` pristine copy, `work/backups/`) are gitignored and intentionally NOT
committed mid-work; the final cumulative `quran.db` will be committed at the repo root once all
6,236 ayat are done and verified.

## Verification tooling
- `work/verify.py` — integrity, schema/index equality vs original, per-row non-tr/talighe diff, counts.
- `work/lint.py` — suspicious-token scan of completed `tr`/`talighe` cells.
- Backups: `work/backups/quran.after-surah-001..007.db` (surah 6/7 recreated from pristine + content)
  and `quran.current-964.db`.

## Honest status
Surahs 1–7 are fully complete and verified (1,160 ayat). Everything from Surah 8 — Al-Anfal
onwards (5,076 ayat, through Surah 114) remains. `quran.db` at the repo root currently contains the
completed work for surahs 1–7. It is NOT final yet; surah-by-surah work continues in order.
