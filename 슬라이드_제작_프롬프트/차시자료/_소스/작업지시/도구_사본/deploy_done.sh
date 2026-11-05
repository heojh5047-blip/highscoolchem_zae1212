#!/bin/bash
# 진행상황.md에서 ✅인 덱만 남기고 site_index.py → firebase deploy (hosting). 미완성 덱 HTML은 잠시 치웠다가 되돌린다.
set -e
R=/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트; S=$R/차시자료; H=$(mktemp -d /tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/hold.XXXX)
python3 -I - "$S" "$H" <<'PY'
import sys,os,re,shutil
S,H=sys.argv[1],sys.argv[2]
md=open(S+'/_소스/작업지시/진행상황.md',encoding='utf-8').read().split('\n')
done=set();key=None
for l in md:
    if l.startswith('## '): key=l[3:].strip()
    m=re.match(r'\| (\S+) \| (\S+) \| ✅',l)
    if m and key: done.add((key,m.group(2)))
for key in os.listdir(S):
    p=os.path.join(S,key)
    if not os.path.isdir(p) or key.startswith(('_','.')) or key in('js','css','물리학'): continue
    for f in os.listdir(p):
        if not f.endswith('.html'): continue
        fol=f[:-5]
        if (key,fol) in done or (key,fol.rstrip('ab')) in done: continue
        os.makedirs(os.path.join(H,key),exist_ok=True); shutil.move(os.path.join(p,f),os.path.join(H,key,f)); print('보류:',key,f)
PY
cd $S/_소스/tools && python3 -I site_index.py
# 상단 탭 순서: 화학 → 물질과 에너지 → 화학 반응의 세계 (과목 안 덱 순서는 그대로)
python3 -I - "$S/decks.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p,encoding='utf-8'))
order=['화학_미래엔','물질과에너지_미래엔','화학반응의세계_미래엔']
d['decks'].sort(key=lambda x: order.index(x['key']) if x['key'] in order else len(order))
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('탭 순서:', ' → '.join(dict.fromkeys(x['key'] for x in d['decks'])))
PY
cd $R && firebase deploy --only hosting --non-interactive 2>&1 | grep -E "Deploy complete|Error|found" || true
for d in $H/*/; do [ -d "$d" ] && mv "$d"*.html "$S/$(basename $d)/"; done; rmdir $H/* $H 2>/dev/null || true
