# -*- coding: utf-8 -*-
"""덱 목록 만들기 — 두 가지 방식
  python site_index.py            # ① Firebase 사이트: 차시자료/<과목 키>/*.html → 차시자료/decks.json (index.html이 읽음)
                                  #    덱목록.json에 있는 과목 키만. 탭 순서 = 덱목록.json의 과목 키 순서
  python site_index.py --all      #    본보기(과학공통_본보기) 등 모든 폴더까지
  python site_index.py --목록     # ② 오프라인 HTML(선택): 차시자료/완성본/<과목 키>/*.html → 차시자료/목록.html
                                  #    (서버 없이 두 번 눌러 여는 링크 모음. 완성본 폴더와 함께 옮긴다)
덱을 새로 빌드하거나 지운 뒤, firebase deploy 전에 ①을 실행한다.
(과학공통 묶음: 화학 묶음의 decks.json 만들기와 범용 묶음의 목록.html 만들기를 한 파일에 합친 판)
"""
import json, os, re, sys, io
from html import escape
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.dirname(SRC)

def make_decks_json():
    DL = {}
    try: DL = json.load(open(os.path.join(SRC, '작업지시', '덱목록.json'), encoding='utf-8-sig'))
    except (OSError, ValueError): pass
    ALL = '--all' in sys.argv
    out = []
    for key in sorted(os.listdir(SITE)):
        p = os.path.join(SITE, key)
        if not os.path.isdir(p) or key.startswith(('_', '.')) or key in ('js', 'css', 'vendor', 'app', '교실용', '완성본'): continue
        info = DL.get(key) if isinstance(DL.get(key), dict) else None
        if not info and not ALL: continue
        info = info or {}
        label = info.get('label') or info.get('course') or key     # 탭 이름 — 출판사 이름은 쓰지 않는다
        decks = {d['folder']: d for d in info.get('decks', [])}
        pos = {d['folder']: i for i, d in enumerate(info.get('decks', []))}
        units = info.get('units', {})
        files = sorted(f[:-5] for f in os.listdir(p) if f.endswith('.html'))
        def order(f):
            if f in pos: return [0, pos[f], f]
            if f.rstrip('ab') in pos: return [0, pos[f.rstrip('ab')], f]
            m = re.match(r'(\d+)-(\d+|M)(?:-(\d+))?', f)
            return [1] + [int(x) if x and x.isdigit() else 99 for x in (m.groups() if m else ('99', '99', '99'))] + [f]
        for f in sorted(files, key=order):
            html = open(os.path.join(p, f + '.html'), encoding='utf-8').read(8000)
            title = (re.search(r'<title>([^<]*)</title>', html) or [None, f])[1]
            head = re.search(r'SLIDE HARNESS · (.*)', html)
            dk = decks.get(f) or decks.get(f.rstrip('ab'))
            uid = dk['unit'] if dk else (re.match(r'(\d+)', f).group(1) if re.match(r'(\d+)', f) else '')
            uname = (uid + '. ' + units[uid]['name']) if uid in units and isinstance(units[uid], dict) and units[uid].get('name') else uid
            out.append({"key": key, "label": label, "file": f, "id": dk['id'] if dk else f.split('_')[0],
                        "title": title, "unit": uid, "unitName": uname,
                        "pages": (f"교과서 {dk['bookPages']}쪽" if dk and dk.get('bookPages') else (head.group(1).strip() if head else ''))})
    ORDER = [k for k in DL if not k.startswith('_')]               # 탭 순서 = 덱목록.json의 과목 키 순서
    out.sort(key=lambda d: ORDER.index(d['key']) if d['key'] in ORDER else len(ORDER))
    json.dump({"decks": out}, open(os.path.join(SITE, 'decks.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'decks.json: 덱 {len(out)}개 ({", ".join(dict.fromkeys(d["key"] for d in out)) or "없음"})')

def make_offline_list():
    try:
        DL = json.load(open(os.path.join(SRC, '작업지시', '덱목록.json'), encoding='utf-8-sig'))
    except (OSError, ValueError):
        DL = {}
    CFG = {}
    try: CFG = json.load(open(os.path.join(SRC, '묶음설정.json'), encoding='utf-8-sig'))
    except (OSError, ValueError): pass
    SKIP = ('js', 'css', 'vendor', 'app', '완성본', '교실용')

    def keys_in(base):
        if not os.path.isdir(base): return []
        return [k for k in sorted(os.listdir(base)) if os.path.isdir(os.path.join(base, k)) and not k.startswith(('_', '.')) and k not in SKIP]

    def order_key(f, pos):
        if f in pos: return (0, pos[f], f)
        nums = [int(x) for x in re.findall(r'\d+', f)[:3]]
        return (1, nums, f)

    groups = []
    done = set()
    for base, kind in ((os.path.join(SITE, '완성본'), '완성본'), (SITE, '빌드본')):
        for key in keys_in(base):
            if key in done: continue
            p = os.path.join(base, key)
            files = [f[:-5] for f in os.listdir(p) if f.endswith('.html')]
            if not files: continue
            done.add(key)
            info = DL.get(key) if isinstance(DL.get(key), dict) else {}
            label = info.get('label') or (f"{info['course']} ({info['publisher']})" if info.get('course') else key)
            decks = {d.get('folder'): d for d in info.get('decks', [])}
            pos = {d.get('folder'): i for i, d in enumerate(info.get('decks', []))}
            items = []
            for f in sorted(files, key=lambda f: order_key(f, pos)):
                head = open(os.path.join(p, f + '.html'), encoding='utf-8').read(6000)
                title = (re.search(r'<title>([^<]*)</title>', head) or [None, f])[1]
                sub = re.search(r'SLIDE HARNESS · (.*)', head)
                dk = decks.get(f) or {}
                rel = os.path.relpath(os.path.join(p, f + '.html'), SITE).replace(os.sep, '/')
                items.append((dk.get('title') or title, (sub.group(1).strip() if sub else ''), rel))
            groups.append((label, kind, items))

    title = CFG.get('title') or '슬라이드 목록'
    credit = CFG.get('credit', '')
    body = ''.join(
        f'<h2>{escape(label)} <small>{escape(kind)}</small></h2><ul>' +
        ''.join(f'<li><a href="{escape("/".join(map(lambda s: s, rel.split("/"))))}">{escape(t)}</a><span>{escape(s)}</span></li>' for t, s, rel in items) +
        '</ul>' for label, kind, items in groups) or '<p>아직 만든 덱이 없습니다. <code>python build.py --offline</code>로 덱을 만든 뒤 다시 실행하세요.</p>'
    page = f"""<!DOCTYPE html>
    <html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <style>
    body{{margin:0;background:#F5F7F9;color:#16233D;font-family:'Malgun Gothic','맑은 고딕','Apple SD Gothic Neo','Noto Sans KR',sans-serif}}
    .wrap{{max-width:900px;margin:0 auto;padding:32px 20px}} h1{{font-size:30px;margin:0 0 20px}}
    h2{{font-size:21px;margin:28px 0 10px}} h2 small{{font-size:14px;color:#5B6B7F;font-weight:400}}
    ul{{list-style:none;padding:0;margin:0}} li{{background:#fff;border:1px solid #DDE3E8;border-radius:10px;padding:14px 18px;margin:8px 0;display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}}
    a{{font-size:19px;font-weight:700;color:#1F6FD1;text-decoration:none}} a:hover{{text-decoration:underline}} li span{{color:#5B6B7F;font-size:15px}}
    footer{{margin-top:36px;padding-top:12px;border-top:1px solid #DDE3E8;color:#5B6B7F;font-size:14px;text-align:center}}
    </style></head><body><div class="wrap"><h1>{escape(title)}</h1>
    {body}
    {f'<footer>{escape(credit)}</footer>' if credit else ''}
    </div></body></html>
    """
    open(os.path.join(SITE, '목록.html'), 'w', encoding='utf-8', newline='\n').write(page)
    n = sum(len(g[2]) for g in groups)
    print(f'목록.html: 덱 {n}개 ({", ".join(g[0] + "/" + g[1] for g in groups) or "없음"})')

if __name__ == '__main__':
    make_offline_list() if '--목록' in sys.argv else make_decks_json()
