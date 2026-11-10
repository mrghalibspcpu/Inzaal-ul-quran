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
- **Surah 7 — Al-A'raf (206/206 ayat)** ✔ complete
- **Surah 8 — Al-Anfal (75/75 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 9 — At-Tawbah (129/129 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 10 — Yunus (109/109 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 11 — Hud (123/123 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 12 — Yusuf (111/111 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 13 — Ar-Ra'd (43/43 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 14 — Ibrahim (52/52 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 15 — Al-Hijr (99/99 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 16 — An-Nahl (128/128 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 17 — Al-Isra (111/111 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 18 — Al-Kahf (110/110 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 19 — Maryam (98/98 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 20 — Ta-Ha (135/135 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 21 — Al-Anbiya (112/112 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 22 — Al-Hajj (78/78 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 23 — Al-Mu'minun (118/118 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 24 — An-Nur (64/64 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 25 — Al-Furqan (77/77 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 26 — Ash-Shu'ara (227/227 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 27 — An-Naml (93/93 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 28 — Al-Qasas (88/88 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)

Progress: **3,340 / 6,236 ayat** rewritten so far. See `work/progress.json`.

## Repo layout (content arranged surah by surah)
Completed work is tracked under **`content/surah-NNN/`** — one folder per surah, part files of ~10 ayat each
(surah 7 also has a small `p22` catch-up file for ayat 81-84). See `content/README.md`.

## How the work is stored (safe from loss)
The translated content is committed under `content/surah-NNN/*.py`. Rebuild recipe: `content/README.md`.
The large binary DBs (`quran.db`, `work/quran.original.db`, `work/backups/`) are gitignored; the final
cumulative `quran.db` will be committed at the repo root once all 6,236 ayat are done and verified.

## Verification tooling
- `work/verify.py` — integrity, schema/index equality vs original, per-row non-tr/talighe diff, counts.
- `work/lint.py` — suspicious-token scan of completed `tr`/`talighe` cells.
- Backups: `work/backups/quran.current-2310.db` … `quran.current-3159.db`, `quran.current-3209.db`, `quran.after-surah-019.db` … `quran.after-surah-027.db`, `quran.after-surah-028.db` (fresh checkpoints after recovery; earlier checkpoints were lost with the sandbox reset).

## Honest status
Surahs 1–26 are fully complete and verified (3,159 ayat). Everything from Surah 27 — An-Naml onwards
(3,077 ayat, through Surah 114) remains. `quran.db` at the repo root currently contains the completed
work for surahs 1–26. It is NOT final yet; surah-by-surah work continues in order.

## Recovery note (2026-11-10)
The local sandbox lost the binary databases (`quran.db`, `work/quran.original.db`, `work/backups/`).
All translated content lives in git under `content/`, so nothing committed was lost. The original
ShiaVerse database (`assets/quran.db`, 16,943,104 bytes) was re-fetched from the same upstream
source used originally; `quran.db` was rebuilt from it by replaying all 236 committed `content/`
part files; `work/verify.py` reports ALL CHECKS PASSED for the rebuilt database.
Fresh checkpoints exist again under `work/backups/` (e.g. `quran.after-surah-019.db`).

## Recovery note (2026-11-10, second occurrence)
The sandbox lost the binary DBs again (gitignored): `quran.db`, `work/quran.original.db`, `work/backups/` were 0-byte/missing and local git was reset to the base commit. The remote branch `origin/arena/d4219406-inzaal-ul-quran` (tip d616c73) had every commit, and the committed `content/` tree was byte-identical to the lost working tree. The pristine ShiaVerse DB was re-fetched from upstream (`mrghalibspcpu/ShiaVerse` → `assets/quran.db`, blob `b7f13f1...`, 16,943,104 bytes, integrity ok), `quran.db` was rebuilt by replaying all committed part files, and `work/verify.py` reports ALL CHECKS PASSED (2,972 ayat; surah 26 at v40).
