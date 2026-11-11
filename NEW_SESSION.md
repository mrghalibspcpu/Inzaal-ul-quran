# NEW_SESSION.md — Inzaal-ul-Quran: Agent Handoff Prompt

Copy the whole of this file (plus the latest `git log` and `work/progress.json` summary) into a new agent session when starting fresh. It is written so the agent knows exactly what to do and how.

---

## Role & goal

You are continuing work on **Inzaal-ul-Quran** — an Urdu translation + tafsir rewrite of the ShiaVerse Quran database (`mrghalibspcpu/ShiaVerse` Android app). The deliverable is `quran.db`, a modified copy of the pristine ShiaVerse DB. Only two columns may differ from the pristine original: `Quran.tr` (Urdu translation) and `Quran.talighe` (Urdu tafsir notes). Everything else — Arabic text, IDs, chapter/verse numbers, juz/hizb/page, indexes, schema, `ChapterProperty` — must remain **byte-identical**. `work/verify.py` proves this; run it.

Repo: `mrghalibspcpu/Inzaal-ul-quran` (already cloned at `/home/user/Inzaal-ul-quran` in this sandbox).

## Hard branch rules

- Work ONLY on branch `arena/d4219406-inzaal-ul-quran`. Never switch to, create, or push another branch. Never rename it.
- Push after every part: `git push origin arena/d4219406-inzaal-ul-quran`.
- Never delete, rename, or move the repo root or its `.git`.

## Current status (update this section at each surah completion)

- Surahs **1–83 complete** (Al-Fatiha … Al-Mutaffifin), verify.py = ALL CHECKS PASSED.
- **5,884 / 6,236 ayat** done. `work/progress.json` is the authoritative per-ayah tracker (IDs list). `PROGRESS.md` tracks completed surahs and is bumped only at surah completion.
- Branch tip at time of writing: the surah-32 completion commit. Always check `git log --oneline -3` and `work/progress.json` first — **the status above may be stale; the repo wins.**
- Next up: **Surah 84 — Al-Inshiqaq** (ayat 1–25). Then surahs 85–114.

## Environment realities (read this before touching anything)

1. **The sandbox resets without warning** (has happened 4 times, most recently 2026-11-10 — repo reverted to base commit; `quran.db`, `work/*.db`, `/tmp` lost; untracked `content/` survived). Therefore: (a) content modules in git are the source of truth, (b) `alkauthar/quran.db` is a tracked snapshot of the deliverable refreshed at surah completions, (c) rebuild steps below handle a full wipe.
2. **Blocked hosts**: `raw.githubusercontent.com` (returns empty) and `release-assets.githubusercontent.com` (connection EOF). Use `api.github.com` instead — it works.
3. **Pristine DB re-fetch** (only after a wipe): 
   `curl -sS -H "Accept: application/vnd.github+json" https://api.github.com/repos/mrghalibspcpu/ShiaVerse/git/blobs/b7f13f14332dfbe90dc57c9a762db19cf885b236` → base64-decode `.content` → save as BOTH `work/quran.original.db` and `./quran.db`. Integrity: 16,943,104 bytes, 6,236 rows, `pragma integrity_check` = ok. sha256 of deliverable at surah-28 snapshot: `dce31f6a…` (see `alkauthar/README.md`).
4. **Full rebuild after wipe**: `git fetch -q origin arena/d4219406-inzaal-ul-quran && git reset --hard origin/arena/d4219406-inzaal-ul-quran` → re-fetch pristine blob → `find content -name '*.py' | sort` → replay each through `python3 work/apply_surah.py` → `python3 work/lint.py && python3 work/verify.py` → make `work/backups/quran.current-<N>.db`. No other steps are valid recovery.

## Per-part workflow (repeat for every ~10 ayat)

1. **Check state first**: `ls quran.db work/quran.original.db` (missing ⇒ full rebuild, above). Fetch Arabic for the ayat: `python3 -c "import sqlite3; con=sqlite3.connect('work/quran.original.db'); [print(r) for r in con.execute('SELECT ID, verse, Arabic FROM Quran WHERE chapter=<N> AND verse BETWEEN a AND b')]"`. IDs are 1–6236 sequential in chapter order; do not invent them.
2. **Author** `content/surah-NNN/content_sNNN_pNN.py` with `SURAH = <n>` and `ENTRIES = { <ID>: (<tr>, <talighe>), … }`. Urdu only (plus Arabic transliteration inside the talighe quotes). Each talighe has exactly three sections: `۱۔` theme, `۲۔` verse transliteration + meaning, `۳۔ عملی سبق:` practical lesson — always the last marker string `۳۔ عملی سبق`.
3. **Sanitize mechanically**: replace ONLY `\u0640` (tatweel) with `'— '`, then collapse runs of 2+ spaces with `re.sub(r'[^\n\S]{2,}', ' ', s)`. Scan for Devanagari codepoints U+0900–097F (zero tolerance) and stray ZWNJ `\u200c` (zero tolerance).
4. **Apply & verify**: `PYTHONDONTWRITEBYTECODE=1 python3 work/apply_surah.py <file>` → remove `__pycache__` → `python3 work/lint.py` (0 suspicious spots required) → `grep -c '۳۔ عملی سبق' <file>` (must equal the entry count) → `git add` the content file + `work/progress.json` → commit (`"Surah NN ayat X-Y translated/tafsir added"`) → **push**.
5. After apply, spot-check the DB: `python3 -c "import sqlite3; [print(r) for r in sqlite3.connect('quran.db').execute('SELECT ID, substr(tr,1,60) FROM Quran WHERE ID BETWEEN a AND b ORDER BY ID')]"`.

## Per-surah completion checklist

1. `python3 work/verify.py` → must end with **ALL CHECKS PASSED**.
2. `cp quran.db work/backups/quran.after-surah-NNN.db`
3. Bump `PROGRESS.md` (add surah line; update total ayat; add backup names) — it is only updated at surah completion.
4. `cp quran.db alkauthar/quran.db` and commit both (alkauthar DB is tracked on purpose) — refresh the snapshot.
5. Commit + push. **Report to the user in Urdu** (their standing request) summarizing: ayat count, verify status, backup names, commit hash, and what's next.

## Hard-won pitfalls — do NOT repeat

- **NEVER do blanket Unicode/character replacements on content files.** On 2026-11-10 a "normalization" pass mapped Urdu letters to Arabic ones across a whole part (پ→ف, چ→ج, گ→ك, ک→ك, ی→ي, ہ→ه), corrupting the Urdu prose; it was caught and fully reverted, but only because the pre-corruption commit existed. Urdu letters **پ چ گ ک ی ہ ں ھ ے ۔ ۱۲۳** are legitimate and must stay. Only U+0640 tatweel may be transformed. If a stray non-Urdu character is suspected in an Arabic transliteration quote, fix exactly that character after locating it — or leave it alone; it is cosmetic and inside quotes.
- **Command-echo garbling**: heredoc/cat output in the tool log renders duplicated/corrupted, but bytes on disk are usually fine. Always confirm via `grep -n '^<ID>:' file` and sqlite read-back, never from the echoed output.
- **Tatweel fixer** is mandatory each part (observed 8–46 occurrences per file).
- **Empty or placeholder IDs are forbidden** — every ID in ENTRIES must come from the DB query for that surah.
- **`apply_surah.py` note line** (`N ayah(s) of surah NN not in this file`) is expected for partial parts; it is not an error.
- `work/progress.json` — do not hand-edit; `apply_surah.py` rewrites it.
- Lint must report **0 suspicious spots**; verify **ALL CHECKS PASSED**; if either fails, stop and repair before committing.
- This session hit **four sandbox wipes**. Assume everything untracked can vanish at any moment; trust only what is pushed to `origin arena/d4219406-inzaal-ul-quran`.

## Connected apps

- `google_drive`: ON (unused so far — ask the user before use).
- `gmail`: connected but OFF — the user must turn it on before any Gmail action. Never ask for credentials; use the connector only.

## User's standing directives

- Keep going surah by surah **without pausing for permission between parts**; report in Urdu at each surah completion.
- Push every part; branch `arena/d4219406-inzaal-ul-quran` only.
- The user reads Urdu reports; write progress reports in Urdu (technical terms in English are fine).
