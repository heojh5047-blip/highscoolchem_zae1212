# -*- coding: utf-8 -*-
"""진행상황.md 고치기 (묶음 상대 경로 — 어디서 실행해도 같은 파일을 고친다)
사용:
  python prog.py <과목 키> <덱 id> <상태> [장수 점검 콘솔 탐구 확인필요]   # 그 과목 절의 표에서 그 덱 행을 고침
  python prog.py report "<한 줄>"                                       # 「보고 모음」 끝에 한 줄
  python prog.py deploy <과목 키> "<글>"                                 # 그 과목 절의 「### 배포 기록」에 한 줄
상태 글: ⬜ 대기 · 🔄 작업 중 · ✅ 완료 (deploy_done.sh는 ✅인 덱만 배포한다)
진행상황.md 꼴은 작업지시/진행상황.md(틀)를 따른다: 「## <과목 키>」 아래 표 「| 덱 | 폴더 | 상태 | 장수 | 자동 점검 | 콘솔 | 필수 탐구 | 확인 필요 |」, 그 아래 「### 배포 기록」, 문서 끝 「## 보고 모음」.
"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, '..', '..', '작업지시', '진행상황.md')
L = open(P, encoding='utf-8-sig').read().split('\n')
a = sys.argv[1:]
if not a: raise SystemExit(__doc__)
if a[0] == 'report':
    try: sec = L.index('## 보고 모음')
    except ValueError: L += ['', '## 보고 모음', '']; sec = len(L) - 2
    end = next((k for k in range(sec + 1, len(L)) if L[k].startswith('## ')), len(L))
    last = max([k for k in range(sec, end) if L[k].startswith('- ')] or [sec])
    L.insert(last + 1, '- ' + a[1])
elif a[0] == 'deploy':
    sec = L.index('## ' + a[1]); i = next(k for k in range(sec, len(L)) if L[k] == '### 배포 기록')
    L.insert(i + 2 if i + 1 < len(L) and L[i + 1] == '' else i + 1, '- ' + a[2])
else:
    key, id_, st = a[0], a[1], a[2]; sec = L.index('## ' + key)
    for k in range(sec, len(L)):
        if k > sec and L[k].startswith('## '): raise SystemExit(f'행 없음: {key} {id_}')
        if L[k].startswith(f'| {id_} |'):
            c = [x.strip() for x in L[k].strip().strip('|').split('|')]
            c[2] = st
            for j, v in enumerate(a[3:]): c[3 + j] = v
            L[k] = '| ' + ' | '.join(c) + ' |'; break
    else: raise SystemExit(f'행 없음: {key} {id_}')
open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('진행상황.md 고침:', ' '.join(a[:3]))
