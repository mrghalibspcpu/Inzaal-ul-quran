# Inzaal-ul-Quran — Urdu Translation + Tafsir Database — Progress

Deliverable: `quran.db` (ShiaVerse Android app) — modified copy of the original ShiaVerse Quran database.
Only `tr` (Urdu translation) and `talighe` (Urdu tafsir notes) are changed. All Arabic text, IDs,
chapter/verse numbers, juz/hizb/page, indexes and ChapterProperty metadata are byte-identical to the original.

## Completed surahs (verified)
- **Surah 1 — Al-Fatiha (7/7 ayat)** ✔ complete, checked
- **Surah 2 — Al-Baqarah (286/286 ayat)** ✔ complete, checked
- **Surah 3 — Al-i-Imran (200/200 ayat)** ✔ complete, checked
- **Surah 4 — An-Nisa (176/176 ayat)** ✔ complete, checked
- **Surah 5 — Al-Ma'ida (120/120 ayat)** ✔ complete, checked
- **Surah 6 — Al-An'am (133/165 ayat)** ⏳ in progress (through 6:133)

Progress: **922 / 6236 ayat** rewritten so far (verify.py ALL CHECKS PASSED). See `work/progress.json`.

## Repo layout (content arranged surah by surah)
Completed work is tracked under **`content/surah-NNN/`** — one folder per surah,
part files of ~10 ayat each. See `content/README.md` for the exact layout and
the full rebuild instructions. Proven on 2026-11-09: rebuilding from
`work/quran.original.db` + `content/**` reproduces `quran.db` **byte-identically
for all 6,236 rows (every column)**.

## How the work is stored (safe from loss)
The translated content (our original Urdu wording, numbered-points tafsir) is committed
under `content/surah-NNN/*.py` — sorted order is apply order. To rebuild the deliverable:
see `content/README.md`. The large binary DBs (`quran.db` deliverable, `work/quran.original.db`
pristine copy, `work/backups/`) are gitignored and intentionally NOT committed mid-work;
the final cumulative `quran.db` will be committed at the repo root once all 6,236 ayat are done and verified.

## Verification tooling
- `work/verify.py` — integrity, schema/index equality vs original, per-row non-tr/talighe diff, counts.
- `work/lint.py` — suspicious-token scan of completed `tr`/`talighe` cells.
- Backups: `work/backups/quran.after-surah-001..005.db` (recreated 2026-11-09 from pristine + content;
  verified reproducible) and `quran.snapshot-2026-11-09-s6-133.db` (current full state).

## Honest status
Surahs 1–5 are fully complete and verified (789 ayat). Surah 6 is complete through 6:133 (133/165).
Everything from the rest of Surah 6 onwards (through Surah 114) remains.
`quran.db` at the repo root currently contains the completed work (surahs 1–6, through 6:133).
It is NOT final yet; surah-by-surah work continues in order.
