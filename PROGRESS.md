# Inzaal-ul-Quran — Urdu Translation + Tafsir Database — Progress

Deliverable: `quran.db` (ShiaVerse Android app) — modified copy of the original ShiaVerse Quran database.
Only `tr` (Urdu translation) and `talighe` (Urdu tafsir notes) are changed. All Arabic text, IDs,
chapter/verse numbers, juz/hizb/page, indexes and ChapterProperty metadata are byte-identical to the original.

## Deliverables (2026-11-13)

- `inzaal-ul-quran.db` (root, tracked) — ShiaVerse-identical schema, rewritten Urdu `tr`/`talighe`, QA pass, PLUS the curated Ahl al-Bayt points below. sha256 `0d8f0fe6eb4eb2d2f66ffaa366eb5fa6bd888e92f2bb3c3cd6810a394f979968`.
- `alkauthar/quran.db` (root, tracked) — byte-identical snapshot of the above for the Al-Kauthar app (now also carrying the curated points; refreshed 2026-11-13).
- `inzaal-ul-quran-shia.db` — **removed 2026-11-13 at the user's request.** Its broad auto-detected enrichment (1,330 points + 6,122 `ربط` lines) is superseded by the curated build in `inzaal-ul-quran.db`.

The current deliverable contains:

- `اہلِ بیتؑ کا نکتہ` for **20 ayat only** — exclusively the ayat that are themselves about Ahl al-Bayt or traditionally attributed to them (2:124, 3:33, 3:61, 3:103, 4:59, 5:3, 5:55, 5:67, 8:41, 9:100, 24:55, 33:33, 33:56, 42:23, 56:10, 59:7, 76:1, 76:7, 76:8, 108:1). Each point is hand-written in easy, عام فہم Urdu and cites BOTH Tafsir-e-Mubeen (Dr Hassan Rizvi) and Tafsir al-Mizan (Arabic; `app-furqan/quran-app-data`, CC BY-ND 4.0 — reference/attribution only). Al-Kauthar (`تفسیر الکوثر`) could not be fetched (APK hosts blocked) — 2-of-2.
- **No `ربط` (previous-verse link) lines anywhere** — removed completely per the user's directive of 2026-11-12 (IDs 12 and 27 included).
- The five Urdu `tr` fixes (IDs 4079, 5147, 5757, 5988, 6014) are now actually present in the released DB (they were in `content/` but missing from the previously committed binary).
- Verify = ALL CHECKS PASSED (Arabic/schema/metadata byte-identical); lint = 0 suspicious; quote balance 7,983/7,983; 0 invisible chars; integrity ok; 6,236 rows.
- Rebuild recipe: rebuild `quran.db` (pristine + `content/**`) → `cp quran.db inzaal-ul-quran.db` → `python3 work/enrich_shia.py inzaal-ul-quran.db` → `cp inzaal-ul-quran.db alkauthar/quran.db`.

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
- **Surah 29 — Al-Ankabut (69/69 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 30 — Ar-Rum (60/60 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 31 — Luqman (34/34 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 32 — As-Sajdah (30/30 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 33 — Al-Ahzab (73/73 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 34 — Saba (54/54 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 35 — Fatir (45/45 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 36 — Yasin (83/83 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 37 — As-Saffat (182/182 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 38 — Sad (88/88 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 39 — Az-Zumar (75/75 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 40 — Ghafir (85/85 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 41 — Ha Mim As-Sajdah / Fussilat (54/54 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 42 — Ash-Shura (53/53 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 43 — Az-Zukhruf (89/89 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 44 — Ad-Dukhan (59/59 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 45 — Al-Jathiya (37/37 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 46 — Al-Ahqaf (35/35 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 47 — Muhammad (38/38 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 48 — Al-Fath (29/29 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 49 — Al-Hujurat (18/18 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 50 — Qaf (45/45 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 51 — Adh-Dhariyat (60/60 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 52 — At-Tur (49/49 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 53 — An-Najm (62/62 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 54 — Al-Qamar (55/55 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 55 — Ar-Rahman (78/78 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 56 — Al-Waqia (96/96 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 57 — Al-Hadid (29/29 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 58 — Al-Mujadala (22/22 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 59 — Al-Hashr (24/24 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 60 — Al-Mumtahina (13/13 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 61 — As-Saff (14/14 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 62 — Al-Jumu'a (11/11 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 63 — Al-Munafiqun (11/11 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 64 — At-Taghabun (18/18 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 65 — At-Talaq (12/12 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 66 — At-Tahrim (12/12 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 67 — Al-Mulk (30/30 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 68 — Al-Qalam (52/52 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 69 — Al-Haqqah (52/52 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 70 — Al-Ma'arij (44/44 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 71 — Nuh (28/28 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 72 — Al-Jinn (28/28 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 73 — Al-Muzzammil (20/20 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 74 — Al-Muddaththir (56/56 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 75 — Al-Qiyamah (40/40 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 76 — Al-Insan (31/31 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 77 — Al-Mursalat (50/50 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 78 — An-Naba (40/40 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 79 — An-Nazi'at (46/46 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 80 — Abasa (42/42 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 81 — At-Takwir (29/29 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 82 — Al-Infitar (19/19 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 83 — Al-Mutaffifin (36/36 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 84 — Al-Inshiqaq (25/25 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 85 — Al-Buruj (22/22 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 86 — At-Tariq (17/17 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 87 — Al-A'la (19/19 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 88 — Al-Ghashiyah (26/26 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 89 — Al-Fajr (30/30 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 90 — Al-Balad (20/20 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 91 — Ash-Shams (15/15 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 92 — Al-Layl (21/21 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 93 — Ad-Duha (11/11 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 94 — Ash-Sharh (8/8 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 95 — At-Tin (8/8 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 96 — Al-Alaq (19/19 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 97 — Al-Qadr (5/5 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 98 — Al-Bayyinah (8/8 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 99 — Az-Zalzalah (8/8 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 100 — Al-Adiyat (11/11 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 101 — Al-Qari'ah (11/11 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 102 — At-Takathur (8/8 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 103 — Al-Asr (3/3 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 104 — Al-Humazah (9/9 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 105 — Al-Fil (5/5 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 106 — Quraish (4/4 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 107 — Al-Ma'un (7/7 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 108 — Al-Kauthar (3/3 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 109 — Al-Kafirun (6/6 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 110 — An-Nasr (3/3 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 111 — Al-Masad (5/5 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 112 — Al-Ikhlas (4/4 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 113 — Al-Falaq (5/5 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)
- **Surah 114 — An-Nas (6/6 ayat)** ✔ complete (verify.py ALL CHECKS PASSED)

Progress: **6,236 / 6,236 ayat** rewritten — ALL 114 SURAHS COMPLETE. See `work/progress.json`.

## Repo layout (content arranged surah by surah)
Completed work is tracked under **`content/surah-NNN/`** — one folder per surah, part files of ~10 ayat each
(surah 7 also has a small `p22` catch-up file for ayat 81-84). See `content/README.md`.

## How the work is stored (safe from loss)
The translated content is committed under `content/surah-NNN/*.py`. Rebuild recipe: `content/README.md`.
The working binaries (`quran.db`, `work/quran.original.db`, `work/backups/`) are gitignored; the final
cumulative database **has been committed at the repo root as `inzaal-ul-quran.db`** (all 6,236 ayat verified;
schema byte-identical to the ShiaVerse `quran.db`; sha256 `0d8f0fe6eb4eb2d2f66ffaa366eb5fa6bd888e92f2bb3c3cd6810a394f979968`).
`alkauthar/quran.db` is a second tracked copy with identical bytes, kept for the Al-Kauthar app.

## Verification tooling
- `work/verify.py` — integrity, schema/index equality vs original, per-row non-tr/talighe diff, counts.
- `work/lint.py` — suspicious-token scan of completed `tr`/`talighe` cells.
- Backups: `work/backups/quran.current-2310.db` … `quran.current-3159.db`, `quran.current-3209.db`, `quran.after-surah-019.db` … `quran.after-surah-027.db`, `quran.after-surah-028.db`, `quran.after-surah-029.db`, `quran.after-surah-030.db`, `quran.after-surah-031.db`, `quran.after-surah-032.db`, `quran.after-surah-033.db`, `quran.after-surah-034.db`, `quran.after-surah-035.db`, `quran.after-surah-036.db`, `quran.after-surah-037.db`, `quran.after-surah-038.db`, `quran.after-surah-039.db`, `quran.after-surah-040.db`, `quran.after-surah-041.db`, `quran.after-surah-042.db`, `quran.after-surah-043.db`, `quran.after-surah-044.db`, `quran.after-surah-045.db`, `quran.after-surah-046.db`, `quran.after-surah-047.db`, `quran.after-surah-048.db`, `quran.after-surah-049.db`, `quran.after-surah-050.db`, `quran.after-surah-051.db`, `quran.after-surah-052.db`, `quran.after-surah-053.db`, `quran.after-surah-054.db`, `quran.after-surah-055.db`, `quran.after-surah-056.db`, `quran.after-surah-057.db`, `quran.after-surah-058.db`, `quran.after-surah-059.db`, `quran.after-surah-060.db`, `quran.after-surah-061.db`, `quran.after-surah-062.db`, `quran.after-surah-063.db`, `quran.after-surah-064.db`, `quran.after-surah-065.db`, `quran.after-surah-066.db`, `quran.after-surah-067.db`, `quran.after-surah-068.db`, `quran.after-surah-069.db`, `quran.after-surah-070.db`, `quran.after-surah-071.db`, `quran.after-surah-072.db`, `quran.after-surah-073.db`, `quran.after-surah-074.db`, `quran.after-surah-075.db`, `quran.after-surah-076.db`, `quran.after-surah-077.db`, `quran.after-surah-078.db`, `quran.after-surah-079.db`, `quran.after-surah-080.db`, `quran.after-surah-081.db`, `quran.after-surah-082.db`, `quran.after-surah-083.db`, `quran.after-surah-084.db`, `quran.after-surah-085.db`, `quran.after-surah-086.db`, `quran.after-surah-087.db`, `quran.after-surah-088.db`, `quran.after-surah-089.db`, `quran.after-surah-090.db`, `quran.after-surah-091.db`, `quran.after-surah-092.db`, `quran.after-surah-093.db`, `quran.after-surah-094.db`, `quran.after-surah-095.db`, `quran.after-surah-096.db`, `quran.after-surah-097.db`, `quran.after-surah-098.db`, `quran.after-surah-099.db`, `quran.after-surah-100.db`, `quran.after-surah-101.db`, `quran.after-surah-102.db`, `quran.after-surah-103.db`, `quran.after-surah-104.db`, `quran.after-surah-105.db`, `quran.after-surah-106.db`, `quran.after-surah-107.db`, `quran.after-surah-108.db`, `quran.after-surah-109.db`, `quran.after-surah-110.db`, `quran.after-surah-111.db`, `quran.after-surah-112.db`, `quran.after-surah-113.db`, `quran.after-surah-114.db` (fresh checkpoints after recovery; earlier checkpoints were lost with the sandbox reset).

## Honest status
All 114 surahs are fully complete and verified (6,236 ayat). The Quran rewrite is finished.
`inzaal-ul-quran.db` at the repo root (committed; sha256 `3062f540…`) contains the complete work for all 114 surahs — rewritten translation/tafsir plus the curated Ahl al-Bayt points in the 20 ayat that are about (or attributed to) Ahl al-Bayt — and `alkauthar/quran.db` holds identical bytes. The rewrite is complete and verified.

## Deliverable refresh note (2026-11-13)
The 2026-11-12 `inzaal-ul-quran-shia.db` (1,330 auto-detected Ahl al-Bayt points + 6,122 `ربط` previous-verse links) was removed from the repo at the user's request. The new deliverable `inzaal-ul-quran.db`/`alkauthar/quran.db` (sha256 `0d8f0fe6eb4eb2d2f66ffaa366eb5fa6bd888e92f2bb3c3cd6810a394f979968`) carries the same rewritten Urdu work PLUS the **20 curated** Ahl al-Bayt points (hand-written, easy عام فہم Urdu, Mubeen + al-Mizan citations), and **no `ربط` lines anywhere**. The five Urdu `tr` fixes (IDs 4079, 5147, 5757, 5988, 6014) that had landed in `content/` earlier are now also present in the released DB binary. Verify = ALL CHECKS PASSED; lint = 0 suspicious.

## Recovery note (2026-11-10)
The local sandbox lost the binary databases (`quran.db`, `work/quran.original.db`, `work/backups/`).
All translated content lives in git under `content/`, so nothing committed was lost. The original
ShiaVerse database (`assets/quran.db`, 16,943,104 bytes) was re-fetched from the same upstream
source used originally; `quran.db` was rebuilt from it by replaying all 236 committed `content/`
part files; `work/verify.py` reports ALL CHECKS PASSED for the rebuilt database.
Fresh checkpoints exist again under `work/backups/` (e.g. `quran.after-surah-019.db`).

## Recovery note (2026-11-10, second occurrence)
The sandbox lost the binary DBs again (gitignored): `quran.db`, `work/quran.original.db`, `work/backups/` were 0-byte/missing and local git was reset to the base commit. The remote branch `origin/arena/d4219406-inzaal-ul-quran` (tip d616c73) had every commit, and the committed `content/` tree was byte-identical to the lost working tree. The pristine ShiaVerse DB was re-fetched from upstream (`mrghalibspcpu/ShiaVerse` → `assets/quran.db`, blob `b7f13f1...`, 16,943,104 bytes, integrity ok), `quran.db` was rebuilt by replaying all committed part files, and `work/verify.py` reports ALL CHECKS PASSED (2,972 ayat; surah 26 at v40).
