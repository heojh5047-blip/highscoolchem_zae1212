# -*- coding: utf-8 -*-
"""웹사이트 덱 목록 만들기: 차시자료/<과목 키>/*.html → 차시자료/decks.json (첫 화면 index.html이 읽음)
사용: python site_index.py            # 화학 과목 폴더(덱목록.json의 과목 키)만
      python site_index.py --all      # 물리 본보기 등 모든 과목 폴더
덱을 새로 빌드하거나 지운 뒤, firebase deploy 전에 실행한다.
"""
import json, os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.dirname(SRC)
DL = json.load(open(os.path.join(SRC, '작업지시', '덱목록.json'), encoding='utf-8'))
ALL = '--all' in sys.argv
out = []
for key in sorted(os.listdir(SITE)):
    p = os.path.join(SITE, key)
    if not os.path.isdir(p) or key.startswith(('_', '.')) or key in ('js', 'css', 'vendor', 'app', '교실용'): continue
    info = DL.get(key)
    if not info and not ALL: continue
    label = f"{info['course']} ({info['publisher']})" if info else key
    decks = {d['folder']: d for d in (info or {}).get('decks', [])}
    units = (info or {}).get('units', {})
    files = sorted(f[:-5] for f in os.listdir(p) if f.endswith('.html'))
    def order(f):
        m = re.match(r'(\d+)-(\d+|M)(?:-(\d+))?', f)
        return [int(x) if x and x.isdigit() else 99 for x in (m.groups() if m else ('99', '99', '99'))] + [f]
    for f in sorted(files, key=order):
        html = open(os.path.join(p, f + '.html'), encoding='utf-8').read(8000)
        title = (re.search(r'<title>([^<]*)</title>', html) or [None, f])[1]
        head = re.search(r'SLIDE HARNESS · (.*)', html)
        dk = decks.get(f) or decks.get(f.rstrip('ab'))
        uid = dk['unit'] if dk else (re.match(r'(\d+)', f).group(1) if re.match(r'(\d+)', f) else '')
        uname = (uid + '. ' + units[uid]['name']) if uid in units else uid
        out.append({"key": key, "label": label, "file": f, "id": dk['id'] if dk else f.split('_')[0],
                    "title": title, "unit": uid, "unitName": uname,
                    "pages": (f"교과서 {dk['bookPages']}쪽" if dk else (head.group(1).strip() if head else ''))})
json.dump({"decks": out}, open(os.path.join(SITE, 'decks.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'decks.json: 덱 {len(out)}개 ({", ".join(sorted(set(d["key"] for d in out))) or "없음"})')
