# -*- coding: utf-8 -*-
"""(선택) 덱 목록 한 장 만들기: 차시자료/완성본/<묶음 키>/*.html (없으면 차시자료/<묶음 키>/*.html) → 차시자료/목록.html
사용: python site_index.py
  - 만든 덱이 여러 개일 때 한 페이지에서 골라 열고 싶으면 쓴다. 덱 하나만 쓸 때는 필요 없다.
  - 목록.html은 인터넷·서버 없이 두 번 눌러 열린다(덱 파일로 가는 링크만 있음). 폴더 구조를 그대로 둔 채 함께 옮겨야 링크가 산다.
  - 묶음 이름·덱 제목·순서는 작업지시/덱목록.json에서 읽는다(없거나 목록에 없는 폴더도 파일 이름으로 넣는다).
(범용 묶음 사본: 원본의 decks.json(Firebase 사이트용) 대신 정적 목록.html을 만든다)
"""
import json, os, re, sys, io
from html import escape
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.dirname(SRC)
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
