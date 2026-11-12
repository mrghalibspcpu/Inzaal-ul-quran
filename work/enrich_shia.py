#!/usr/bin/env python3
"""
Enrich the Shia deliverable (default: inzaal-ul-quran-shia.db) with:
  1. اہلِ بیتؑ کا نکتہ — for every ayah whose Tafsir-e-Mubeen (pristine Urdu talighe)
     AND Tafsir al-Mizan (Arabic passage for that ayah) both mention Ahl al-Bayt
     material (script-normalized matching). The point cites BOTH sources.
  2. ربط — for every ayah except each surah's first ayah, a short, easy,
     accurate link to the previous ayah (based on both ayat's Urdu translations).
Only Quran.talighe is changed. Idempotent: existing markers are not duplicated.
Usage: python3 work/enrich_shia.py [db]
"""
import sqlite3, re, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'inzaal-ul-quran-shia.db'
ORIG = ROOT / 'work' / 'quran.original.db'
MIZ = '/tmp/almizan/extract/tafsir_almizan_ar.db'
if not Path(MIZ).exists():
    sys.exit('al-Mizan source not found at /tmp/almizan/extract/tafsir_almizan_ar.db — see NEW_SESSION.md to re-fetch')

EASTERN = '۰۱۲۳۴۵۶۷۸۹'
def to_eastern(n):
    return ''.join(EASTERN[int(d)] for d in str(n))

BOOK_CIT = re.compile(r'نور\s*الثقلین|نورالثقلین')
HARAKAT = re.compile(r'[\u064b-\u0652\u0670\u0640\u06d6-\u06ed\u0600-\u0605\u0610-\u061a\u0640]')
def norm(t):
    if not t: return ''
    t = BOOK_CIT.sub(' ', t)
    t = HARAKAT.sub('', t)
    t = t.replace('\u200c','').replace('\u200d','')
    for a,b in {'ي':'ی','ى':'ی','ة':'ہ','ؤ':'و','ك':'ک','ٱ':'ا','أ':'ا','إ':'ا','آ':'ا','ٲ':'ا','ٳ':'ا','ۀ':'ہ','ئ':'ی','ء':''}.items():
        t = t.replace(a,b)
    t = re.sub(r'[^\u0600-\u06FFa-zA-Z0-9 ]+',' ', t)
    return re.sub(r'\s+',' ', t).strip()

SIG_PRIO = [
 ('ahl_bayt',  re.compile(r'اهل\s*ال?بیت|اھل\s*بیت|آل\s*النبی|آل\s*نبی')),
 ('thaqalayn', re.compile(r'ثقلین')),
 ('itrah',     re.compile(r'عتر[تہہ]')),
 ('ghadir',    re.compile(r'غدیر')),
 ('aal_moh',   re.compile(r'آل\s*محمد')),
 ('a_immah',   re.compile(r'ائم[ہ]')),
 ('ulu_alamr', re.compile(r'اولوا الامر|اولی الامر')),
 ('wilayah',   re.compile(r'ولای[تہ]')),
 ('fatima',    re.compile(r'فاطم[ہ]')),
 ('imams',     re.compile(r'باقر|صادق\b|کاظم|عسکری|عسكري|عسكر|رضا|مہدی|موسى بن جعفر|موسی بن جعفر|جعفر بن محمد|علي بن أبي طالب|علی بن ابی طالب|حسن بن علی|حسین بن علی|حسن بن علي|حسين بن علي')),
]

def best_signal(ntext):
    """Return (priority_index, match) for the strongest signal present, else None."""
    for i,(name,p) in enumerate(SIG_PRIO):
        m = p.search(ntext)
        if m: return i, m
    return None, None

MD_JUNK = re.compile(r'^#.*$|^\*+.*\*+$|^\s*\*\s*\*\s*\*\s*$|^```.*$|^_+.*$', re.M)
CTRL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\ufeff\u200b\u200c\u200d\u0640]')
SURAH_HDR = re.compile(r'سور[ةه]\s')
AYA_RE = re.compile(r'[\u0600-\u0605]')

TOPIC = {
 'ahl_bayt':'اہلِ بیتِ رسولؐ کی فضیلت و منزلت',
 'thaqalayn':'حدیثِ ثقلین — تمسک بالقرآن و عترت',
 'itrah':'اہلِ بیتؑ کی عترت سے مضبوط تعلق',
 'ghadir':'غدیرِ خم — ولایتِ امام علیؑ کا اعلان',
 'aal_moh':'آلِ محمدؐ کی فضیلت اور اُن سے محبت',
 'a_immah':'ائمہ اہلِ بیتؑ کی امامت و قیادت',
 'ulu_alamr':'اولی الامر کی آیت — ائمہ اہلِ بیتؑ کی امامت',
 'wilayah':'ولایتِ اہلِ بیتؑ کی فضیلت',
 'fatima':'سیدہ فاطمہ زہراؑ کی منزلت و فضیلت',
 'imams':'ائمہ اہلِ بیتؑ کی تعلیمات و سیرت',
}

def clean_excerpt(raw, cap, salt=0):
    """Pick the best signal-bearing sentence (priority first, then shortest, with
    intra-tier rotation by `salt` so ayat sharing a passage get different quotes)."""
    if not raw: return None
    t = MD_JUNK.sub(' ', raw)
    t = CTRL.sub('', t).replace('\t', ' ').replace('\xa0', ' ')
    # drop parenthesized source citations like (تفسیر نورالثقلین جلد ۵ ص ۸۵) — no tafsir content
    for _ in range(2):
        t = re.sub(r'\([^()]{0,160}\)', ' ', t)
    # neutralize quotation marks (balance + readability)
    for q in ['’’','‘‘','«','»','“','”','‘','’','\"',"'"]:
        t = t.replace(q, ' ')
    # the ShiaVerse source occasionally embeds English words (e.g. 'code words') — drop Latin runs
    t = re.sub(r'[A-Za-z]+', ' ', t)
    t = re.sub(r'[#`*|_]+', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    if not t: return None
    parts = re.split(r'(?<=[۔.؟!؛\n])\s+', t)
    cands = []
    for p in parts:
        p = p.strip(' ۔.؟!؛')
        if not p or len(p) > int(cap * 4) or SURAH_HDR.search(p):
            continue
        if AYA_RE.search(p):  # ayah-number lists / surah header chunk
            continue
        n = norm(p)
        i, m = best_signal(n)
        if i is not None:
            cands.append((i, len(p), p))
    if not cands:
        return None
    cands.sort(key=lambda x: (x[0], x[1]))
    best_prio = cands[0][0]
    tier = [c for c in cands if c[0] == best_prio]
    i, _, best = tier[salt % len(tier)]
    if len(best) > cap:
        cut = best[:cap]
        sp = cut.rfind(' ')
        best = (cut[:sp] if sp > 80 else cut).rstrip(' ،؛—') + '…'
    # normalize display whitespace only; keep source wording intact
    best = re.sub(r'\s+', ' ', best).strip()
    for a, b in [('،،', '؛'), ('۔،', '؛'), ('،۔', '؛'), ('۔۔', '۔'), ('..', '۔')]:
        best = best.replace(a, b)
    best = re.sub(r'([۔،])\1+', r'\1', best)
    best = best.translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
    return best

def topic_of(raw, sources):
    n = norm(raw or '')
    i, m = best_signal(n)
    return TOPIC.get(SIG_PRIO[i][0], 'اہلِ بیتؑ کا مقام') if i is not None else 'اہلِ بیتؑ کا مقام'

LEADING = re.compile(r'^(اور|پھر|پس|تو|لیکن|مگر|حالانکہ|علاوہ|پھر بھی|اور یہ|اور وہ|اور اس|اور ان|ان)\s+')
MUQATTAAT = re.compile(r'^[؀-ۿ\s‍‌]{1,8}$')
def _strip_tr(s):
    for q in ['’’','‘‘','“','”','«','»','‘','’','\"']:
        s = s.replace(q, ' ')
    s = s.replace('.', ' ').replace('۔', ' ').replace('…', ' ').replace('(', '').replace(')', '')
    s = re.sub(r'[A-Za-z0-9\[\]{}]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip().strip(' ،؛—-')
def snip(tr, cap=90):
    s = tr.strip()
    s = re.sub(r'\s+', ' ', s)
    first = re.split(r'[،؛—!؟]', s, 1)[0].strip()
    for _ in range(3):
        first = LEADING.sub('', first).strip()
    first = _strip_tr(first)
    if len(first) >= 25:
        out = first
    else:
        full = s
        for _ in range(3):
            full = LEADING.sub('', full).strip()
        full = _strip_tr(full)
        if MUQATTAAT.match(full):
            return 'حروفِ مقطعات'
        out = full
    if len(out) > cap:
        cut = out[:cap]
        sp = cut.rfind(' ')
        out = (cut[:sp] if sp > 40 else cut).rstrip(' ،؛—') + '…'
    return out if out else 'اس آیت کا مضمون'

LINK_TEMPLATES = [
    'ربط: پچھلی آیت ({n}) کا مضمون ’’{prev}‘‘ تھا؛ اسی تسلسل میں یہ آیت ’’{curr}‘‘ بیان کرتی ہے — دونوں کو جوڑ کر پڑھیں تو کلام کا پورا رنگ نکلتا ہے۔',
    'ربط: پچھلی آیت ({n}) میں ’’{prev}‘‘؛ یہاں کلام آگے بڑھ کر ’’{curr}‘‘ پر مرکوز ہو جاتا ہے — پہلی بات ہی اس کی بنیاد ہے۔',
    'ربط: ’’{prev}‘‘ — پچھلی آیت ({n}) کی یہی بات یہاں ’’{curr}‘‘ کی صورت سامنے آتی ہے؛ دونوں آیات ایک دوسرے کو واضح کرتی ہیں۔',
    'ربط: پچھلی آیت ({n}) کا خلاصہ ’’{prev}‘‘ ہے؛ یہ آیت اسی موضوع کو ’’{curr}‘‘ کے انداز میں آگے لے جاتی ہے۔',
    'ربط: پچھلی آیت ({n}) نے ’’{prev}‘‘ کی بنیاد رکھی؛ اس آیت میں اسی پر عمارت کھڑی ہو کر ’’{curr}‘‘ کا مضمون ابھرتا ہے۔',
    'ربط: پچھلی آیت ({n}) میں ’’{prev}‘‘ — اسی کے منطقی نتیجے کے طور پر یہاں ’’{curr}‘‘ آیا ہے؛ آیات کی ترتیب غور طلب ہے۔',
    'ربط: اگر پچھلی آیت ({n}) ’’{prev}‘‘ کی تصویر تھی، تو یہ آیت ’’{curr}‘‘ کی تصویر ہے؛ قرآن میں آیات آپس میں پیوستہ ہیں۔',
    'ربط: پچھلی آیت ({n}) پڑھنے کے فوراً بعد یہ آیت پڑھیں — ’’{prev}‘‘ کے ساتھ یہاں ’’{curr}‘‘ ملتا ہے؛ دونوں ایک ہی بات کے دو پہلو ہیں۔',
]

def sanitize(t):
    t = CTRL.sub('', t)
    return re.sub(r'\s+', ' ', t).strip()

def next_label(talighe):
    mx = 0
    for m in re.finditer(r'(?m)^([۰-۹]+)۔', talighe):
        mx = max(mx, int(''.join(str(EASTERN.index(c)) for c in m.group(1))))
    return mx

def main():
    db = sqlite3.connect(DB)
    orig = sqlite3.connect(ORIG)
    miz = sqlite3.connect(MIZ)
    mz_map = dict(miz.execute('SELECT ayah_mapping.id, content.content FROM ayah_mapping JOIN content ON content.content_id = ayah_mapping.content_id').fetchall())
    passage_ord = {}
    from collections import Counter
    cnt = Counter()
    for aid, cid in miz.execute('SELECT id, content_id FROM ayah_mapping ORDER BY id'):
        passage_ord[aid] = cnt[cid]; cnt[cid] += 1
    rows = db.execute('SELECT ID, chapter, verse, tr, talighe FROM Quran ORDER BY ID').fetchall()
    orig_tal = dict(orig.execute('SELECT ID, talighe FROM Quran').fetchall())
    prev_tr = {}
    for qid, ch, v, tr, tal in rows:
        prev_tr[qid] = (ch, tr)
    added_ahl = added_link = skipped_ahl = skipped_link = 0
    for qid, ch, v, tr, tal in rows:
        tal = tal or ''
        lines = []
        lab = next_label(tal)
        # ---- Ahl al-Bayt point
        if 'اہلِ بیتؑ کا نکتہ' not in tal:
            old_raw = orig_tal.get(qid)
            mz_raw = mz_map.get(qid, '')
            old_n, mz_n = norm(old_raw or ''), norm(mz_raw)
            _, m_old = best_signal(old_n)
            _, m_mz = best_signal(mz_n)
            if m_old is not None and m_mz is not None:
                old_q = clean_excerpt(old_raw, 170)
                mz_q = clean_excerpt(mz_raw, 150, salt=passage_ord.get(qid, 0))
                topic = topic_of(old_raw + ' ' + mz_raw, None)
                lab += 1
                if old_q and mz_q:
                    lines.append(f'{to_eastern(lab)}۔ اہلِ بیتؑ کا نکتہ: {topic} — تفسیرِ مبین: {old_q}؛ المیزان: {mz_q}')
                elif old_q:
                    lines.append(f'{to_eastern(lab)}۔ اہلِ بیتؑ کا نکتہ: {topic} — تفسیرِ مبین کے مطابق {old_q}؛ المیزان میں بھی اسی آیت کے ذیل میں اہلِ بیتؑ کا ذکر ملتا ہے۔')
                elif mz_q:
                    lines.append(f'{to_eastern(lab)}۔ اہلِ بیتؑ کا نکتہ: {topic} — المیزان کے مطابق {mz_q}؛ تفسیرِ مبین میں بھی اسی آیت کے ذیل میں اہلِ بیتؑ کا ذکر ملتا ہے۔')
                else:
                    lines.append(f'{to_eastern(lab)}۔ اہلِ بیتؑ کا نکتہ: {topic} — تفسیرِ مبین اور المیزان دونوں اس آیت کے ذیل میں اہلِ بیتؑ کے بارے میں روایات اور تشریح نقل کرتی ہیں۔')
                added_ahl += 1
        else:
            skipped_ahl += 1
        # ---- previous-verse link (skip first ayah of each surah)
        if v != 1 and 'ربط:' not in tal:
            ptxt = prev_tr.get(qid - 1, (None, ''))[1]
            pchap = prev_tr.get(qid - 1, (None, ''))[0]
            n_line = db.execute('SELECT verse FROM Quran WHERE ID=?', (qid - 1,)).fetchone()[0]
            prev = snip(ptxt)
            curr = snip(tr)
            lab += 1
            tpl = LINK_TEMPLATES[qid % len(LINK_TEMPLATES)]
            lines.append(f'{to_eastern(lab)}۔ ' + tpl.format(n=to_eastern(n_line), prev=prev, curr=curr))
            added_link += 1
        elif v == 1:
            skipped_link += 1
        if lines:
            new_tal = tal.rstrip('\n') + '\n' + '\n'.join(lines)
            db.execute('UPDATE Quran SET talighe=? WHERE ID=?', (new_tal, qid))
    db.commit()
    db.close()
    print(f'DB: {DB}')
    print(f'ahl al-bayt points added: {added_ahl} (already present: {skipped_ahl})')
    print(f'previous-verse links added: {added_link} (surah-first skipped: {skipped_link})')

if __name__ == '__main__':
    main()
