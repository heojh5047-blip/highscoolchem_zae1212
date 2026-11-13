#!/bin/bash
# 완료(✅) 덱만 배포: 차시자료를 별도 스테이징 폴더에 복사(미완성 덱·_소스 제외) → decks.json 생성·탭 순서 정렬 → 스테이징에서 firebase deploy --only hosting.
# 원본 폴더의 파일은 옮기지 않으므로, 작업 중인 에이전트가 빌드해도 섞이지 않는다.
set -e
R=/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트; S=$R/차시자료
ST=/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/stage
rm -rf $ST; mkdir -p $ST/public
python3 -I - "$S" "$ST/public" <<'PY'
import sys,os,re,shutil,json
S,P=sys.argv[1],sys.argv[2]
md=open(S+'/_소스/작업지시/진행상황.md',encoding='utf-8').read().split('\n')
done=set();key=None
for l in md:
    if l.startswith('## '): key=l[3:].strip()
    m=re.match(r'\| (\S+) \| (\S+) \| ✅',l)
    if m and key: done.add((key,m.group(2)))
for n in os.listdir(S):
    src=os.path.join(S,n)
    if n.startswith(('_','.')): continue
    if os.path.isfile(src): shutil.copy2(src,P); continue
    if n in ('js','css','물리학'): shutil.copytree(src,os.path.join(P,n)); continue
    os.makedirs(os.path.join(P,n),exist_ok=True)
    for f in os.listdir(src):
        if not f.endswith('.html'): continue
        fol=f[:-5]
        if (n,fol) in done or (n,fol.rstrip('ab')) in done: shutil.copy2(os.path.join(src,f),os.path.join(P,n,f))
        else: print('제외(미완성):',n,f)
PY
# decks.json: site_index.py 결과를 받아 완료 덱만 남기고 탭 순서 정렬
cd $S/_소스/tools && python3 -I site_index.py >/dev/null
python3 -I - "$S/decks.json" "$ST/public" <<'PY'
import json,sys,os
src,P=sys.argv[1],sys.argv[2]; d=json.load(open(src,encoding='utf-8'))
d['decks']=[x for x in d['decks'] if os.path.exists(os.path.join(P,x['key'],x['file']+'.html'))]
order=['화학_미래엔','물질과에너지_미래엔','화학반응의세계_미래엔']
d['decks'].sort(key=lambda x: order.index(x['key']) if x['key'] in order else len(order))
import re
for x in d['decks']: x['label']=re.sub(r'\s*\([^)]*\)\s*$','',x['label'])   # 탭에 출판사 이름을 쓰지 않는다
for p in (src, os.path.join(P,'decks.json')): json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('decks.json: 덱',len(d['decks']),'개 · 탭 순서:',' → '.join(dict.fromkeys(x['key'] for x in d['decks'])))
PY
python3 -I - "$R/firebase.json" "$ST/firebase.json" <<'PY'
import json,sys
c=json.load(open(sys.argv[1],encoding='utf-8')); c['hosting']['public']='public'; c.pop('database',None)
json.dump(c,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
PY
cp $R/.firebaserc $ST/
cd $ST && firebase deploy --only hosting --non-interactive 2>&1 | grep -E "Deploy complete|Error|found" || true
