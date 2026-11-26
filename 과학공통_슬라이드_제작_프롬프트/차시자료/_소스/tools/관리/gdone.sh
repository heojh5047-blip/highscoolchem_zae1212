#!/bin/bash
# 덱 하나를 끝냈을 때(제작·지도서 대조·재검토): 보고 기록 → 완료 덱 배포 → 배포 기록 → (설정하면) git commit
# 사용: bash gdone.sh <과목 키> <덱 id> "<보고 한 줄>" [작업 종류(기본: 완료)]
#   예: bash gdone.sh 통합과학1_출판사 1-1-1 "장수 32 / 점검 0 / 콘솔 0 / motion 0 / ask 0" "지도서 대조"
#   WORK=<임시 작업 폴더> 를 주면 그 안의 생성 스크립트(*.py, *.html, *.js — 맨 위 단계만)를 작업지시/덱_생성스크립트/<과목 키>_<id>/에 남긴다.
#   관리설정.json의 git_commit이 true면 묶음 폴더에서 git commit, git_push_branch가 있으면 push도 한다.
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$HERE/../../../.." && pwd)"
PY="$(command -v python3 || command -v python)"
KEY="$1"; ID="$2"; MSG="$3"; KIND="${4:-완료}"
[ -z "$KEY" ] || [ -z "$ID" ] && { echo "사용: bash gdone.sh <과목 키> <덱 id> \"<보고 한 줄>\" [작업 종류]"; exit 1; }
"$PY" -I "$HERE/prog.py" report "[$KIND] $KEY $ID / $MSG"
if [ -n "$WORK" ] && [ -d "$WORK" ]; then
  D="$R/차시자료/_소스/작업지시/덱_생성스크립트/${KEY}_${ID}"; mkdir -p "$D"
  find "$WORK" -maxdepth 1 -type f \( -name '*.py' -o -name '*.html' -o -name '*.js' \) -exec cp {} "$D/" \;
fi
bash "$HERE/deploy_done.sh" | tail -1 && "$PY" -I "$HERE/prog.py" deploy "$KEY" "$ID $KIND 배포"
GC=$("$PY" -I -c "import json,sys;c=json.load(open(sys.argv[1],encoding='utf-8-sig'));print('1' if c.get('git_commit') else '');print(c.get('git_push_branch',''))" "$HERE/관리설정.json")
COMMIT=$(echo "$GC" | sed -n 1p); BR=$(echo "$GC" | sed -n 2p)
if [ -n "$COMMIT" ]; then
  cd "$R" && git add -A && git commit -qm "$KIND: $KEY $ID" && echo "git commit 완료"
  [ -n "$BR" ] && git push -q origin "$BR" 2>&1 | tail -1
fi
