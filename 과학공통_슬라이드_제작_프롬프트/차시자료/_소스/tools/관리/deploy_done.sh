#!/bin/bash
# 완료(✅) 덱만 Firebase Hosting에 배포한다.
#  차시자료를 스테이징 폴더에 복사(미완성 덱·_소스 제외) → decks.json 생성(완료 덱만, 탭 순서 정렬) → 스테이징에서 firebase deploy --only hosting.
#  원본 폴더의 파일은 옮기지 않으므로, 작업 중인 덱을 빌드해도 섞이지 않는다.
# 사용: bash deploy_done.sh [과목 키 순서…]
#   과목 키 순서(탭 순서)를 인자로 주면 그 순서, 없으면 관리설정.json의 「과목순서」, 그것도 비면 덱목록.json 순서.
#   STAGE=<폴더> 로 스테이징 위치를 바꿀 수 있다(기본: 임시 폴더). DRY=1 이면 배포하지 않고 스테이징까지만.
# Database 규칙(database.rules.json)은 바꾸지 않는다 — 규칙을 올릴 때는 묶음 폴더에서 firebase deploy --only database.
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$HERE/../../../.." && pwd)"          # 묶음 폴더(firebase.json이 있는 곳)
S="$R/차시자료"
PY="$(command -v python3 || command -v python)"
ST="${STAGE:-$(mktemp -d)}"
rm -rf "$ST"; mkdir -p "$ST/public"
"$PY" -I - "$S" "$ST/public" "$HERE/관리설정.json" <<'PY'
import sys,os,re,shutil,json
S,P,CF=sys.argv[1:4]
cfg=json.load(open(CF,encoding='utf-8-sig')) if os.path.exists(CF) else {}
keep=set(cfg.get('늘_넣을_폴더',['js','css']))
md=open(S+'/_소스/작업지시/진행상황.md',encoding='utf-8-sig').read().split('\n')
done=set();key=None
for l in md:
    if l.startswith('## '): key=l[3:].strip()
    m=re.match(r'\| (\S+) \| (\S+) \| ✅',l)
    if m and key: done.add((key,m.group(2)))
for n in os.listdir(S):
    src=os.path.join(S,n)
    if n.startswith(('_','.')) or n in ('완성본','목록.html'): continue
    if os.path.isfile(src): shutil.copy2(src,P); continue
    if n in keep: shutil.copytree(src,os.path.join(P,n)); continue
    os.makedirs(os.path.join(P,n),exist_ok=True)
    for f in os.listdir(src):
        if not f.endswith('.html'): continue
        fol=f[:-5]
        if (n,fol) in done or (n,fol.rstrip('ab')) in done: shutil.copy2(os.path.join(src,f),os.path.join(P,n,f))
        else: print('제외(미완성):',n,f)
PY
# decks.json: site_index.py 결과에서 완료 덱만 남기고 탭 순서 정렬
(cd "$S/_소스/tools" && "$PY" -I site_index.py >/dev/null)
"$PY" -I - "$S/decks.json" "$ST/public" "$HERE/관리설정.json" "$S/_소스/작업지시/덱목록.json" "$@" <<'PY'
import json,sys,os,re
src,P,CF,DLp=sys.argv[1:5]; args=sys.argv[5:]
d=json.load(open(src,encoding='utf-8'))
cfg=json.load(open(CF,encoding='utf-8-sig')) if os.path.exists(CF) else {}
DL=json.load(open(DLp,encoding='utf-8-sig')) if os.path.exists(DLp) else {}
order=args or cfg.get('과목순서') or [k for k in DL if not k.startswith('_')]
d['decks']=[x for x in d['decks'] if os.path.exists(os.path.join(P,x['key'],x['file']+'.html'))]
d['decks'].sort(key=lambda x: order.index(x['key']) if x['key'] in order else len(order))
for x in d['decks']: x['label']=re.sub(r'\s*\([^)]*\)\s*$','',x['label'])   # 탭에 출판사 이름을 쓰지 않는다
for p in (src, os.path.join(P,'decks.json')): json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('decks.json: 덱',len(d['decks']),'개 · 탭 순서:',' → '.join(dict.fromkeys(x['key'] for x in d['decks'])) or '없음')
PY
"$PY" -I - "$R/firebase.json" "$ST/firebase.json" <<'PY'
import json,sys
c=json.load(open(sys.argv[1],encoding='utf-8')); c['hosting']['public']='public'; c.pop('database',None)
json.dump(c,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
PY
cp "$R/.firebaserc" "$ST/"
if [ -n "$DRY" ]; then echo "DRY: 스테이징만 만듦 → $ST"; exit 0; fi
cd "$ST" && firebase deploy --only hosting --non-interactive 2>&1 | grep -E "Deploy complete|Error|found|Hosting URL" || true
