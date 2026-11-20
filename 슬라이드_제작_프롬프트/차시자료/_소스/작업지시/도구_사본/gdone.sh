#!/bin/bash
# gdone.sh <key> <id> "<report>"  — 지도서 대조 한 덱 끝: 기록·배포·커밋
SC=/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad
D=/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/작업지시/도구_사본/덱_생성스크립트
python3 -I $SC/prog.py report "[지도서 대조] $1 $2 / $3"
[ -d "$SC/$1_$2" ] && (cd $SC && find "$1_$2" -maxdepth 1 -type f \( -name '*.py' -o -name '*.html' -o -name '*.js' \) -exec sh -c 'mkdir -p "$0/$(dirname "$1")" && cp "$1" "$0/$1"' $D {} \;)
pgrep -f "node server.mjs" >/dev/null || (cd $SC/cdn && nohup node server.mjs > server.log 2>&1 &)
$SC/deploy_done.sh | tail -1 && python3 -I $SC/prog.py deploy $1 "$2 지도서 대조 배포"
cd /home/user/highscoolchem_zae1212 && git add -A && git commit -qm "지도서 review: $1 $2

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QqDrBaqCpbLyDP8Z3qB6es"; git push -q origin claude/chem-slides-firebase-deploy-boci5o 2>&1|tail -1
