set -e
R=/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스
SC=/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad
python3 -I $SC/화학반응의세계_미래엔_1-5/gen.py "$R/content/화학반응의세계_미래엔/1-5_완충_작용/slides.html"
cd $R/tools && python3 -I build.py 화학반응의세계_미래엔/1-5_완충_작용
export CHROME=$SC/cdn/chrome.sh
pgrep -f "node server.mjs" >/dev/null || (cd $SC/cdn && nohup node server.mjs > server.log 2>&1 &)
node render.mjs "../../화학반응의세계_미래엔/1-5_완충_작용.html" "../_render/화학반응의세계_미래엔/1-5_완충_작용" "$@" 2>&1 | tail -40
