set -e
R=/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스
python3 -I /tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/화학반응의세계_미래엔_1-3/gen.py "$R/content/화학반응의세계_미래엔/1-3_중화_적정/slides.html"
cd $R/tools && python3 -I build.py 화학반응의세계_미래엔/1-3_중화_적정
export CHROME=/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/cdn/chrome.sh
node render.mjs "../../화학반응의세계_미래엔/1-3_중화_적정.html" "../_render/화학반응의세계_미래엔/1-3_중화_적정" "$@" 2>&1 | tail -30
