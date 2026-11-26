# 차시 덱 작성 안내 (에이전트·개발자용 — 과학 공통: 물리·화학·생명과학·지구과학)

이 폴더는 **수업용 16:9 HTML 슬라이드**를 만드는 원본이다.
최상위 규칙은 `../../docs/슬라이드_제작_가이드라인_과학공통.md`(이하 "가이드라인")이고, 이 문서는 그 규칙을 이 엔진에서 **어떻게 구현하는지**를 적는다.
엔진 사용 본보기는 `content/과학공통_본보기/0-0-1_과학_공통_본보기/`(빌드 결과 `../과학공통_본보기/0-0-1_과학_공통_본보기.html`, 13장) — 네 영역의 그림·실험실·문항 장 꼴을 한두 장씩 담았다. 같은 과목에서 먼저 완성·검토한 덱이 생기면 그것이 본보기다.

## 1. 폴더와 작업 흐름

```
차시자료/
  <과목 키>/<덱 폴더>.html        ← 빌드 결과(사이트용, 손으로 고치지 않음)
  완성본/<과목 키>/<덱 폴더>.html  ← (선택) 오프라인 파일, build.py --offline
  _소스/
    AUTHORING.md          이 문서
    묶음설정.json          꼬리말(credit) — 모든 덱 표지 왼쪽 아래
    engine/harness.css    공용 스타일   (고치지 않는다 — 덱 전용 스타일은 extra.css)
    engine/harness.js     공용 엔진     (고치지 않는다 — 실험실은 labs.js)
    engine/harness-ui.html  색 이름(HARNESS_COL)·조작 UI
    vendor/katex/         KaTeX 0.16.11 사본(오프라인 파일용)
    content/<과목 키>/<덱 폴더>/       과목 키 = 통합과학1_<출판사>, 과학2_<출판사> …
      plan.md             구성안(화면 문장 전문, 계산·반응식 검산, 필수 탐구 이행 절)
      meta.json           {"title":"…","file":"<덱 폴더>","header":"Ⅰ-1-1 … (고등 통합과학1 12–17쪽)"}
      slides.html         <section class="slide"> … 들만 (엔진 껍데기 없이)
      labs.js             (선택) window.DECK_LABS = { 이름(root, API){…} };
      extra.css           (선택) 이 덱 전용 스타일. 클래스 이름은 덱 접두어로 (예: .is1111-…)
      img/                (선택) 직접 만든 그림 — src="img/…"는 빌드할 때 파일 안에 들어감
    작업지시/              공통.md, 과학공통_약속.md, <과목>_약속.md, 에이전트_안내.md, 덱목록.json, 진행상황.md
    _자료/                (각자 준비) 교과서·지도서·교육과정 PDF — 덱목록.json의 파일 이름으로
    _추출/                (각자 준비) 쪽별 텍스트 — tools/extract_pages.py로 만듦
    tools/build.py        python build.py <과목 키>/<덱 id>   → 차시자료/<과목 키>/<file>.html  (--offline: + 완성본)
    tools/render.mjs      node render.mjs <html> <출력폴더> [--slides=3,5-8] [--steps]
    tools/sheet.py        캡처 4장을 한 장에 모음
    tools/관리/            진행상황 기록·완료 덱 배포 도구(prog.py, deploy_done.sh, gdone.sh)
```

작업 순서: `slides.html`·`labs.js` 작성 → `python build.py <과목 키>/<덱 id>` → `node render.mjs <결과 html> ../_render/<과목 키>/<덱 폴더>` →
표준 출력의 **자동 점검 건수·콘솔 오류**를 0으로 → `_render/…/sNN.png`(또는 `sheet.py` 모음)를 **직접 보고** 겹침·잘림·빈 공간을 고친다 → 반복.
캡처는 "모든 단계를 펼친" 상태다. 단계가 서로를 덮는 장은 `--steps`(하위 폴더)로 확인한다. 명령은 `_소스/tools`에서 실행한다.

## 2. 슬라이드 기본 구조

```html
<section class="slide" data-sec="01 · 알짜힘" data-title="알짜힘">
  <h2><span class="no">1</span>알짜힘</h2>
  …
</section>
```
- 무대 1280×720, 안전 여백 위 78·좌우 84·아래 64(패딩으로 잡혀 있음). 위 띠는 엔진이 붙인다.
- `data-sec` = 머리띠 왼쪽 글(꼴은 `작업지시/과학공통_약속.md` 2절), `data-title` = 목차 제목. 표지는 `class="slide cover"`(`.cover-text` > `.kicker`, `h1`(`.acc`), `.sub`, `.meta` + 오른쪽 `svg.cover-fig`).
- 제목 표식: `<span class="no">1</span>`(개념 번호) · `<span class="tag">탐구</span>`(교과서 이름 그대로) · `.tag.alt`(연결·융합) · `.tag.q`(확인·문항) · `.tag.ex`(예제) · `.tag.ink`(정리).
- 레이아웃: `.row > .col`(`.row.stretch`, `.col.stack`, 열 너비 `style="flex:0 0 440px"`), `.card`(`.q`, `.tip`), `.note`(`.puzzle`, `.q`, `.big`), `.stages`(3열, `.c2`) > `.stage`, `.flow > .fnode(.hl) + .farr`, `.std` + `.code`(성취기준), `ol.goals`, `.chips > button.chk`, `table`(`.tight`, `td.l`), `.bogi` + `.choices`(객관식), `.blank`(빈칸, 안에 `.step` 정답).
- 공식 `.formula`(`.sm`) + `.unit`. 정답 `.answer`(여럿이면 `.answers`). 판서 공간 `.board`.
- 글자: 본문 24px, `.f22` `.f21`, 보조 `.small`(19px). **19px 아래로 내리지 않는다.** 넘치면 문장을 줄이거나 장을 나눈다.
- 형광펜 `<mark>`는 핵심 정의에만. 색 클래스 `.c-plus .c-minus .c-field .c-muted`.

## 3. 단계 공개 (S1)
- `.step`은 문서 순서대로 하나씩. **같은 `data-g`**는 함께(그림 `<g class="step" data-g="a2">` + 설명 `<p class="step" data-g="a2">`).
- SVG `<text class="tex">`에도 `class="step" data-g=…`.
- 공개 순서는 각 그룹이 문서에서 처음 나오는 위치. 순서를 고정하려면 빈 `<span class="step" data-g="…"></span>`을 먼저 둔다.
- SVG 라벨은 기준선 아래로 글자 크기의 약 0.35배 더 내려간다. viewBox 가장자리 라벨은 0.4×크기 이상 여유(D8).
- 예제 풀이·정답·결론·질문의 답은 `.step`. 처음부터 보여 줄 내용에는 붙이지 않는다.
- 질문 먼저(가이드라인 6.5): 답 단계 앞 질문 문장에는 '?' 또는 'Q'. 지시문이면 `data-q`.
- 낱말 묶기: 엔진이 인라인 수식·빈칸 앞뒤에 붙은 조사를 자동으로 묶는다(띄어 쓰면 묶이지 않음).

## 4. 수식·단위·화학식 (M, P, C, B, E)
- 본문 수식 `$…$`(블록 `$$…$$`). 변수 기울임, 숫자·단위는 `\text{}`: `$9.8\ \text{m/s}^2$`, `$25\ {}^\circ\text{C}$`, `$3\ \Omega$`, `$1013\ \text{hPa}$`.
- 단위 곱 `\cdot`(가운뎃점 금지), 유니코드 첨자 ₂ ² 금지(자동 점검 M1). 아래첨자 글자는 `v_\text{나중}`, `E_\mathrm{k}`.
- 수식 안 괄호 `\left( … \right)`, 여러 줄 계산 `\begin{aligned} … &= … \end{aligned}`.
- **화학식은 `\ce{}`**(mhchem): `$\ce{H2O}$`, `$\ce{2H2 + O2 -> 2H2O}$`, `$\ce{6CO2 + 6H2O -> C6H12O6 + 6O2}$`. 본문 글자 `H2O`, `CO2`는 자동 점검 **C1**에 걸린다(생명·지구 장의 $\ce{CO2}$, $\ce{O2}$도 마찬가지).
- **유전자 기호는 기울임**: `$A$`, `$Aa$`, `$AaBb$`(KaTeX 기본 기울임). 세대 `$\mathrm{F_1}$`.
- 위도·각: `$37^\circ\,\mathrm{N}$`, `$23.5^\circ$`. μm: `$10\ \mu\text{m}$`.
- HTML 속성 안의 `<`, `>`는 `&lt;` `&gt;`(mhchem 화살표 `->`도 속성 안에서는 `-&gt;`).

## 5. 그림
모든 그림은 **직접 그린 SVG**다. 교과서 그림·사진을 복사하거나 베끼지 않는다. `svg.fig` + `viewBox` + `style="width:…px"`, `aria-label` 필수, 장식은 `aria-hidden="true"`.

### 5.1 SVG 라벨 (M1) — 그림 속 글자는 전부 이것으로
```html
<text class="tex" x="200" y="40" data-tex="F=12\ \text{N}" data-size="22" data-anchor="middle"></text>
<text class="tex" x="120" y="80" data-mix="무게 $W$||둘째 줄" data-size="20" data-weight="700" data-halo="1" fill="#1F6FD1"></text>
```
x, y는 글자 기준선. `data-anchor` start|middle|end, `||` 줄바꿈, `data-halo` 흰 바탕. **화면에서 실제 18px 이상**(viewBox가 줄어 보이면 그만큼 키움 — 16px 미만이면 자동 점검 `3.2`). 일부러 겹친 라벨은 `data-overlap="ok"`.

### 5.2 엔진 부품 🟢 (속성만 쓰면 엔진이 그린다)
- **화살표** `<g data-arw="x1,y1,x2,y2,색,굵기[,d]">` — 색: ink plus minus field equi bfield ox rd grav muted white 또는 #hex. 힘(길이 비례 D9·D12), 속도, 전류, 이동, 흐름.
- **회로도** `<svg class="fig" viewBox="0 0 480 270" data-circuit='{"parts":[…],"stroke":3,"labelSize":22}'>`
  - `["wire",[[x,y],…]]` · `["node",[x,y]]` ● · `["term",[x,y],"a",{"side":"left"}]` ○
  - `["bat",[x,y],{"dir":"h|v","pos":"right|left|up|down","label":"6\\ \\text{V}","signs":true}]` 긴 판(+)이 pos 쪽. 도선은 가로면 x±8, 세로면 y±8까지
  - `["R",[x1,y1],[x2,y2],"R=3\\ \\Omega",{…}]` · `["C",…]` · `["L",…]` · `["D",…,{"led":true}]` · `["sw",[x1,y1],[x2,y2],true|false]` · `["bulb",[x,y],{"r":14,"on":true}]` · `["meter",[x,y],"A|V|G",{"r":16}]`(도선은 원 둘레까지) · `["ac",[x,y],{"r":18}]` · `["npn",[x,y],{…}]` · `["arrow",[x1,y1],[x2,y2],{"label":"I","color":"plus"}]` · `["label",[x,y],"\\text{A}",{"size":20}]`
  - 부품은 SVG 맨 아래층. 전류·전자 화살표를 단계 공개하려면 `data-arw`를 SVG 안에 따로 둔다(본보기 5번 장). 스위치는 도선 뒤에.
- **원자 모형** `<g data-atom="x,y,r,원소[,라벨|-][,d]">` — 원소별 고정 색 공 + 기호 라벨. 반지름 H 18 · 2주기 24 · 3주기 29(라벨이 화면 18px 이상). 분자는 원자를 겹쳐(H₂ 중심 간 24, O₂ 32) 그리고, 공-막대는 막대(`line` 6–8px `#9AA5B1`)를 먼저. 실험실 `API.atom(g,x,y,r,'O','',false)`.
- **전하** `<g data-chg="x,y,r,+|-|P|M|N[,d]">` · **± 묶음** `<g data-pm="+|-,크기,x:y …[,색]">` (정전기, 대전체)
- **전기력선** `<svg data-field='…'>`, 방사형 장 `<g data-vfield='…'>`, **수직 자기장** `<g data-bgrid="x,y,w,h,간격,in|out[,색,크기]">`, 축전기 패널 `.cappanel[data-cfg]` — 쓰는 법은 `engine/harness.js` 머리 주석.

### 5.3 SVG로 직접 그리는 그림 ✏️ (영역 팩 약속 — 가이드라인 10장)
- **자유 물체도**: 물체 상황 그림과 점으로 줄인 힘 그림을 나란히. 힘마다 `data-arw`(가이드라인 2.4 힘 색) + 이름·크기 라벨, 힘마다 단계 공개(본보기 3번 장).
- **운동·자료 그래프**: 축 `data-arw`(muted), 격자 `#E2E7EC`, 눈금 숫자 `text.tex` 18px, 곡선은 **식으로 계산한 path**(Python 생성 스크립트 또는 `labs.js`). 본보기 11번 장의 반감기 곡선은 `x=80+100t, y=290-2.4·100·(1/2)^t`를 0.05 간격으로 계산했다.
- **세포·기관 모식도**: 윤곽 + 옅은 실제 색 + 이름표(`text.tex`) + 지시선(`line` muted 1.5). 이름표는 그림 위·아래 한 줄에 맞춘다(본보기 8번 장).
- **교배표**: HTML `table`(칸 안 `<span class="step">$Aa$</span>`). **가계도**: `rect`(남) · `circle`(여), 칠 = 형질 발현, 범례(본보기 9번 장).
- **지층 단면**: `<defs><pattern id="<접두어>-p<장>-ss">`로 암석 무늬, 층은 `rect`, 관입암은 `polygon`, 부정합 위 지층은 굽은 경계 `path`로 덮고, 부정합면 선은 `ox` 3.5px(본보기 10번 장).
- **천구·궤도·일기도·지도**: 가이드라인 D45–D47. 방위·축척·범례.
- 좌표가 복잡한 그림(대칭 분자, 궤도, 등압선, 단면)은 덱 작업 폴더의 **Python 생성 스크립트**로 계산해 넣고, 스크립트를 `작업지시/덱_생성스크립트/<과목 키>_<id>/`에 남긴다(관리 도구 `gdone.sh`가 `WORK=`로 복사).

### 5.4 색 의미 (D7, 고정)
가이드라인 2.4절 표와 `작업지시/과학공통_약속.md` 4절. 요약: 무게 `minus` · 외력·당기는 힘·전류 `plus` · 수직 항력·장력 `ink` · 마찰력 `equi` · 알짜힘 `field` · 전자 `minus` · 자기장 `bfield` · 보조선·축·지시선 `muted` · 이전 상태 `grav` 점선 · 형광펜 `#FFE45C`. 실제 색(세포 소기관, 암석, 물질)은 칠에만.

### 5.5 id (D5)
`<defs>`의 gradient·pattern·marker·clipPath id는 **덱 전체에서 고유**: 덱 접두어 + 장 번호(`sc001-p10-ss`). 화살표는 marker 대신 `data-arw`.

## 6. 실험실 (가이드라인 5.4 — 성취기준 필수 탐구는 반드시, S12)
```html
<div class="lab" data-lab="sc001run">            <!-- labs.js 의 DECK_LABS.sc001run 과 연결 -->
  <div class="lab-ctl">
    <div class="ctl"><div class="lbl"><span>알짜힘 $F$</span><output data-o="F"></output></div>
      <input type="range" min="2" max="20" step="2" value="8" data-i="F" aria-label="알짜힘"></div>
    <div class="res"><div class="small">가속도 $a$ [$\text{m/s}^2$]</div><div class="big"><output data-o="a"></output></div><output class="kind" data-o="msg"></output></div>
    <div><button class="btn" data-act="measure">측정하기</button><button class="btn" data-act="reset">초기화</button></div>
    <table class="tight"><thead><tr><th>번</th><th>$F$ [N]</th><th>측정 $a$</th></tr></thead><tbody data-o="rows"></tbody></table>
  </div>
  <div class="lab-fig" style="width:563px;height:403px"><svg viewBox="0 0 560 400" width="560" height="400" aria-label="속도-시간 그래프"></svg>
    <div class="ov" data-ov="l1">$v$</div>     <!-- 값이 바뀌는 수식 라벨은 HTML 겹침(.ov)으로, API.place 로 위치 -->
  </div>
</div>
```
API: `mk(tag,attrs,parent)`, `arrow(g,x1,y1,x2,y2,color,w,dash)`, `atom(g,x,y,r,원소,라벨,점선)`, `charge(g,x,y,r,sign)`, `texText(parent,x,y,tex,{size,anchor,fill,mix})`(처음 그릴 때 만든 라벨만 KaTeX로 바뀜 — 축 이름·눈금처럼 고정된 라벨에 쓰고, 값이 바뀌는 라벨은 `.ov` + `API.tex()`), `place(el,x,y,visible)`, `clamp`, `fmtN`, `niceRatio`, `signed`, `COL`, `loop(root,fn)`, `onShow(fn)`, `ready(fn)`, `tex(str)`, `isActive(root)`, (물리) `vfield`, `fieldAt`, `trace`, `fieldLines`, `bgrid`.
- 슬라이더 옆에 **현재 값과 단위**(`output`, 일반 글자 — `$…$`·유니코드 첨자를 넣지 않는다. 단위에 위첨자가 필요하면 라벨 쪽에 `$\text{m/s}^2$`).
- **측정 → 기록 표 → 그래프 → 해석 문장**, 고정 시드 오차(LCG), 초기화 버튼. 본보기 4번 장 `labs.js`가 꼴이다.
- 움직이는 시뮬레이션은 `API.loop`(보일 때만). 정적 그림의 움직임은 `data-anim`.
- 실험실 동작은 `tools/_labtest.mjs`에 `PRE`(JS 식, 결과는 `console.warn('LAB …')`)를 주어 확인한다. 임시 스크립트는 작업 폴더(scratch) 안에.

## 7. 덱 구성 (가이드라인 3장, 과학공통 약속 9절)
표지(오른쪽 상징 그림) → (대단원·중단원 도입: 그 단원 첫 덱만) → 학습 목표(성취기준 `.std` + `ol.goals` + 오늘의 흐름) → 도입(예측 질문 S6) → 개념 장들(연결 S5, 현상 → 모형 → 기호 S10) → 탐구(S7, 안전 S9) + **필수 탐구 실험실(S12)** → 예제(판서 + 단계 정답, S8) → 확인하기 → 읽기 자료 → 이 소단원 몫 문항(한 장에 한 문항, S2) → 스스로 정리(개념 지도 빈칸) → 스스로 점검하기.
- 교과서의 모든 개념·탐구·활동·예제·문항을 빠짐없이. 지도서의 지도 내용(오개념, 발문, 예시 답안)을 반영한다.
- 교과서 문장을 길게 베끼지 않는다. 문항은 숫자·조건을 그대로 쓰되 문장은 다듬는다.
- 고등 25–40장, 중학 18–30장이 보통(과목 약속 분량).

## 8. 점검 (가이드라인 8장)
render.mjs 자동 점검(D8 넘침·라벨 겹침, T4, T2, M1 KaTeX 오류·유니코드 첨자, **C1 본문 글자 화학식**, M2, T5, D5, S2, 3.2 라벨 크기)과 콘솔 오류 **0건**.
그다음 캡처를 눈으로: 겹침·잘림, 힘 화살표 길이 비례·라벨, 회로 도선 끊김·극, 원자 수 보존, 이름표가 맞는 구조를 가리키는지, 교배표·가계도 기호, 지층 무늬·순서, 그래프가 계산값과 맞는지, 빈 공간·쏠림, 정답 가운데.
계산·반응식·필수 탐구 이행은 plan.md 검산 절(과학공통 약속 11절)과 대조한다.

## 9. 오프라인 파일 (선택)
`python build.py <과목 키>/<덱 id> --offline` → `차시자료/완성본/<과목 키>/<file>.html`(KaTeX·mhchem·woff2·본문 글꼴 포함). `node verify_offline.mjs "../../완성본/<과목 키>/<file>.html"` → OK(외부 요청 0, KaTeX 오류 0, 점검 0). 묶음 전체 링크 모음은 `python site_index.py --목록` → `차시자료/목록.html`.
