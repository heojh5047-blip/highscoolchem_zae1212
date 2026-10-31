# 차시 덱 작성 안내 (에이전트·개발자용 — 고등학교 화학 3과목)

이 폴더는 **수업용 16:9 HTML 슬라이드(가이드라인 A형)**를 만드는 원본이다.
최상위 규칙은 `../../docs/슬라이드_제작도구_가이드라인_화학.md` (이하 "가이드라인")이고, 이 문서는 그 규칙을 이 엔진에서 **어떻게 구현하는지**를 적는다.
엔진 사용 본보기는 `content/물리학/1-1-1_평형과_안정성/`(빌드 결과 `../물리학/1-1-1_평형과_안정성.html`) — 같은 엔진으로 만든 **물리** 덱이다. 슬라이드 구성·밀도·그림 수준·단계 공개·움직임·실험실 코드의 꼴은 이것을 보고, 내용·색 뜻은 화학 규칙(가이드라인 2장, `작업지시/화학3과목_공통_약속.md`)을 따른다. 같은 과목에서 먼저 완성된 화학 덱이 생기면 그것이 본보기다.

## 1. 폴더와 작업 흐름

```
차시자료/
  화학_미래엔/2-2-2_전자쌍_반발_이론과_분자_구조.html   ← 빌드 결과 (수업에서 여는 파일, 손으로 고치지 않음)
  _소스/
    AUTHORING.md          이 문서
    engine/harness.css    공용 스타일   (고치지 않는다 — 덱 전용 스타일은 extra.css)
    engine/harness.js     공용 엔진     (고치지 않는다 — 실험실은 labs.js)
    engine/harness-ui.html  색 이름(HARNESS_COL)·조작 UI
    content/<과목 키>/<덱 폴더>/       과목 키 = 화학_미래엔, 화학_비상, 물질과에너지_미래엔 …
      plan.md             구성안(화면 문장 전문, 반응식·계산 검산, 필수 탐구 이행 절)
      meta.json           {"title":"전자쌍 반발 이론과 분자 구조","file":"2-2-2_전자쌍_반발_이론과_분자_구조","header":"Ⅱ-2-2 전자쌍 반발 이론과 분자 구조 (고등 화학, 미래엔 72–77쪽)"}
      slides.html         <section class="slide"> … 들만 (deck·엔진 껍데기 없이)
      labs.js             (선택) window.DECK_LABS = { 이름(root, API){…} };
      extra.css           (선택) 이 덱 전용 스타일. 클래스 이름은 덱 접두어로 (예: .cm222-…)
    작업지시/              공통.md, 화학3과목_공통_약속.md, <과목>_약속.md, 덱목록.json
    _자료/                (각자 준비) 교과서·지도서 PDF — 덱목록.json의 파일 이름으로
    _추출/                (각자 준비) 쪽별 텍스트 — tools/extract_pages.py로 만듦
    tools/build.py        python build.py 화학_미래엔/2-2-2   → 차시자료/화학_미래엔/<file>.html
    tools/render.mjs      node render.mjs <html> <출력폴더> [--slides=3,5-8] [--steps]
    tools/sheet.py        캡처 4장을 한 장에 모음
    tools/extract_pages.py  PDF → 쪽별 텍스트
```

작업 순서: `slides.html`·`labs.js` 작성 → `python build.py <과목 키>/<덱 폴더>` → `node render.mjs <결과 html> ../_render/<과목 키>/<덱 폴더>` →
표준 출력의 **자동 점검 건수·콘솔 오류**를 0으로 만들고 → `_render/…/sNN.png` 를 **Read 로 직접 보고** 겹침·잘림·어색한 배치·빈 공간을 고친다 → 반복.
캡처는 "모든 단계를 펼친" 상태다. 단계가 서로를 덮는 슬라이드는 `--steps` 로 단계별 캡처도 확인한다.
명령은 `_소스/tools` 폴더에서 실행한다.

## 2. 슬라이드 기본 구조

```html
<section class="slide" data-sec="02 · 중심 원자에 공유 전자쌍만 있을 때" data-title="공유 전자쌍만 있을 때">
  <h2><span class="no">3</span>중심 원자에 공유 전자쌍만 있을 때</h2>
  …
</section>
```
- 무대 1280×720, 안전 여백 위 78·좌우 84·아래 64 (패딩으로 이미 잡혀 있음). 위 띠(단원·쪽 번호)는 엔진이 자동으로 붙인다.
- `data-sec` = 머리띠 왼쪽 글(꼴은 `화학3과목_공통_약속.md` 2절), `data-title` = 목차에 뜰 짧은 제목. 표지는 `class="slide cover"`.
- 제목 앞 표식: `<span class="no">1</span>`(개념 번호) · `<span class="tag">탐구|해 보기|과학 마당|…</span>`(글은 교과서 이름 그대로 — 과목 약속 3절) · `.tag.alt`(연결) · `.tag.q`(확인하기·문항) · `.tag.ex`(예제·연습 해 보기) · `.tag.ink`(스스로 정리).
- 레이아웃: `.row > .col` (`.row.stretch`, `.col.stack`, 열 너비는 `style="flex:0 0 440px"`), `.card`(`.q`, `.tip`), `.note`(`.puzzle`, `.q`, `.big`), `.stages`(3열, `.c2` 2열) > `.stage`, `.pane`(`.plus .minus .grav .elec`) + `.ph`, `.flow > .fnode(.hl) + .farr`, `.std` + `.code`(성취기준·필수 탐구 문장), `ol.goals`, `.chips > button.chk`(학생 체크), `table`(`.tight`, `td.l`), `.bogi` + `.choices`(객관식), `.blank`(빈칸, 안에 `.step` 정답).
- 공식 `.formula`(`.sm`) + 안에 `.unit`(단위·설명 줄). 반응식도 `.formula`에 `$\ce{…}$`로. 정답 `.answer`(여러 개면 `.answers`로 감쌈). 판서 공간 `.board` (`.col.stack` 안에 두면 남는 높이를 채움).
- 글자 크기: 본문 24px 기본, `.f22` `.f21`, 보조 `.small`(19px). **19px 아래로 내리지 않는다.** 넘치면 글자를 줄이지 말고 문장을 줄이거나 슬라이드를 나눈다. `.note`를 키울 때는 `.note.big`(21px).
- 형광펜 `<mark>` 는 핵심 정의(교과서 정의 문장)에만.
- 색 클래스: `.c-plus .c-minus .c-field .c-muted`.

## 3. 단계 공개 (S1)
- `.step` 요소는 문서 순서대로 한 번에 하나씩 나타난다. **같은 `data-g` 값**을 가진 `.step`들은 함께 나타난다 (그림 속 `<g class="step" data-g="a2">` 와 그 설명 `<p class="step" data-g="a2">` 를 묶을 때).
- SVG 안의 `<text class="tex">` 에도 `class="step" data-g=…` 를 줄 수 있다.
- **공개 순서는 각 data-g 그룹이 문서(DOM)에서 처음 나오는 위치로 정해진다.** 그룹 멤버가 문서 앞쪽에 있으면 의도보다 먼저 열린다. 순서를 고정하려면 원하는 자리에 빈 `<span class="step" data-g="…"></span>`을 먼저 둔다.
- SVG 라벨(texSVG)은 기준선 아래로 글자 크기의 약 0.35배가 더 내려간다. viewBox 가장자리 라벨은 기준선에서 0.4×크기 이상 여유를 둔다(D8 잘림 방지).
- 회로도 부품은 목록 순서대로 그려진다. 스위치(`sw`)는 도선 뒤에 두어야 흰 접점이 덮이지 않는다.
- render.mjs는 시작할 때 출력 폴더의 s*.png를 지운다. `--steps` 캡처는 하위 폴더로 받는다.
- 예제 풀이·정답·결론·질문의 답은 `.step`. 처음부터 다 보여 줄 내용에는 붙이지 않는다. 새 현상은 현상 → 입자 모형 → 화학식 순서로 단계를 나눈다(S10).
- 낱말 묶기(keepWords): 엔진이 낱말마다 `span.w`(nowrap)로 감싸고, **인라인 수식·화학식·빈칸(.blank) 바로 앞뒤에 붙은 글자(조사·괄호·문장 부호)도 자동으로 한 덩어리로 묶는다**(`$\ce{H2O}$는`, `<span class="blank">…</span>을`). 띄어 쓰면 묶이지 않는다.

## 4. 수식과 화학식 (M1–M13, C1–C12, T2)
- 본문 수식은 `$…$` (블록은 `$$…$$`). 변수는 기울임(기본), 숫자·단위는 `\text{}`: `$0.1\ \text{M}$`, `$22.4\ \text{L}$`, `$25\ {}^\circ\text{C}$`.
- **화학식·이온·반응식은 `\ce{}`**(KaTeX mhchem — 빌드가 불러온다): `$\ce{H2O}$`, `$\ce{CH3COOH}$`, `$\ce{SO4^2-}$`, `$\ce{Al^3+}$`, `$\ce{e-}$`, `$\ce{2H2(g) + O2(g) -> 2H2O(l)}$`, `$\ce{N2(g) + 3H2(g) <=> 2NH3(g)}$`, `$\ce{CuSO4*5H2O}$`(가운뎃점 수화물), `$\ce{->[\Delta]}$`, `$\ce{->[\text{촉매}]}$`. 본문 글자 `H2O`, `Na+`는 자동 점검 **C1**에 걸린다.
- 농도·평형: `$[\ce{H3O+}]$`, `$K=\dfrac{[\ce{NH3}]^2}{[\ce{N2}][\ce{H2}]^3}$`, `$K_\mathrm{w}$`, `$K_\mathrm{a}$`, `$\text{pH}=-\log[\ce{H+}]$`(교과서 꼴), `$\Delta H=-92\ \text{kJ}$`, `$E_\mathrm{a}$`, `$E^\circ$`.
- 산화수: `$\overset{+7}{\ce{Mn}}\ce{O4-}$`. 부분 전하: `$\delta^+$`, `$\delta^-$`. 핵종: `$\ce{^{14}_{6}C}$`.
- 단위 곱 `\cdot` (가운뎃점 · 금지 — `\ce{}` 안의 `*`는 mhchem이 수화물 점으로 바꿈), 유니코드 첨자 ₂ 금지. 아래첨자 글자는 `V_\mathrm{A}`.
- 단위는 그 양에만 (M3): 식 뒤에 `[mol]` 을 붙이지 말고 `.unit` 줄에 "$n$의 단위: mol".
- 수식 안 괄호는 `\left( … \right)` (M6). 여러 줄 계산은 `\begin{aligned} … &= … \end{aligned}` (T6).
- HTML 속성 안(`data-mix` 등)의 `<`, `>`는 `&lt;` `&gt;`, 본문에서도 `$Q&lt;K$`. mhchem 화살표 `->`, `<=>`의 `>`·`<`도 속성 안에서는 `-&gt;`, `&lt;=&gt;`로 쓴다(본문 `$…$`에서는 그대로 써도 브라우저가 고쳐 읽지만, 덱 안에서 한 가지로).
- 마이크로·그리스 문자 접두어는 `$30\ \mu\text{L}$`처럼 `\mu`로 쓴다.

## 5. 그림
모든 그림은 **직접 그린 SVG**다. 교과서 그림·사진을 복사하거나 다시 베끼지 않는다(저작권, 가이드라인 7.3-5). 같은 개념을 설명하는 새 도식으로 그린다.
`svg.fig` + `viewBox` + `style="width:…px"` 로 크기를 정하고, `aria-label`을 단다. 장식용은 `aria-hidden="true"`.

### 5.1 SVG 라벨 (M1) — 그림 속 글자는 전부 이것으로
```html
<text class="tex" x="200" y="40" data-tex="\ce{NH3}" data-size="24" data-anchor="middle"></text>
<text class="tex" x="120" y="80" data-mix="$\ce{H+}$를||내놓음" data-size="20" data-weight="700" data-halo="1" fill="#D7263D"></text>
```
x, y는 **글자 기준선**. `data-anchor` start|middle|end, `||` 는 줄바꿈, `data-halo` 는 흰 바탕(선과 겹칠 때). 그림 가장자리 라벨은 안쪽에 둔다(D8).

**라벨 크기(가이드라인 3.2)**: `data-size`는 viewBox 단위라서, SVG가 화면에 줄어 들어가면 라벨도 같은 비율로 작아진다. **화면에서 실제 18px 이상**(눈금 숫자·원자 기호 포함)이 되도록 `data-size`를 정하거나 viewBox를 표시 크기에 맞춰 잡는다. 실제 크기가 16px 미만이면 자동 점검 `3.2`가 알려 준다. 일부러 겹친 라벨(단계에서 덮어쓰는 라벨)은 `data-overlap="ok"`.

### 5.2 엔진 부품 (속성만 쓰면 엔진이 그린다)
- **원자 모형** `<g data-atom="x,y,r,원소[,라벨|-][,d]">` — 원소별 고정 색 공(가이드 2.5 원자 색 표, `HARNESS_ATOM`으로 바꿈) + 원소 기호 LaTeX 라벨(흰 글씨/검은 글씨 자동). 라벨: 생략 → 원소 기호, `-` → 없음, 그 밖 → LaTeX(예: `\mathrm{Na}^{+}`, `\mathrm{O}^{\delta-}`). `d` → 점선(빈자리·이전 위치: `data-atom="120,80,22,O,d"`). 반지름은 `작업지시/화학3과목_공통_약속.md` 5절. 실험실에서는 `API.atom(g,x,y,r,'O','',false)`.
  - 공-막대 모형: 결합 막대(`line`, 굵기 6–8, `#9AA5B1`, 둥근 끝)를 **먼저** 그리고 그 위에 `data-atom`을 둔다. 이중 결합은 막대 두 개(간격 8), 삼중 결합은 세 개.
  - 쐐기 결합(D23): 앞으로 나온 결합 = 채운 삼각형 `polygon`(ink), 뒤로 들어간 결합 = 가로 짧은 선을 촘촘히 쌓은 쐐기(점선 쐐기), 종이 면 = 실선.
  - 비공유 전자쌍 로브: 옅은 타원 `ellipse`(fill `#E08A2C`, 불투명도 .18, 테 equi 1.5) + 안에 점 두 개.
- **전자점(루이스 전자점식)**: `<circle r="4" fill="#16233D">`를 원소 기호 둘레 네 자리(위·아래·왼쪽·오른쪽)에 둔다. 원소 기호 라벨(`data-tex="\mathrm{F}"`, 크기 S)의 기준선을 기호 중심 y + 0.36S에 두면, 점의 중심은 기호 중심에서 가로 ±0.70S, 세로 ±0.75S, 쌍의 두 점 간격 0.36S(중심에서 ±0.18S)이다(S=40에서 시험해 맞춘 값 — 다른 크기에서는 캡처로 확인). 공유 전자쌍은 두 기호 사이 가운데. 강조는 옅은 상자(`field` 공유, `equi` 비공유, 불투명도 .18)를 `.step`으로.
- 화살표 `<g data-arw="x1,y1,x2,y2,색,굵기[,d]">` 색: ink plus minus field equi bfield **ox rd** grav muted white 또는 #hex. 전자 이동 `minus`, 산화·환원 `ox`·`rd`, 정반응·역반응 `field`·`bfield`.
  - **쌍극자 모멘트 화살표(D24)**: `data-arw`로 $\delta^+$ 쪽 → 전기 음성도 큰 쪽 화살표를 그리고, 꼬리에서 화살표 길이의 15% 지점에 화살표와 수직인 짧은 선(길이 14, 굵기 같게)을 덧그려 + 꼬리를 만든다.
  - **가역 화살표 ⇌**를 그림에 그릴 때는 반쪽 화살촉 두 줄(`path`)로 직접 그리거나, 라벨 `data-tex="\ce{<=>}"`를 쓴다.
- 전하 `<g data-chg="x,y,r,+|-|P|M|N[,d]">` (단원자 이온·전자를 단순한 원으로 보일 때. P/M/N은 안에 라벨을 넣을 때)
- ± 기호 묶음 `<g data-pm="+|-,크기,x:y x:y …[,색]">` (대전체·전극 표면)
- **회로도 (D1)** `<svg class="fig" viewBox="0 0 470 260" data-circuit='{"parts":[…],"stroke":3,"labelSize":22}'>` — 물의 전기 분해·화학 전지·전기 분해·도금 장치의 회로 부분. 비커·전극·염다리·용액은 직접 그린 SVG로 겹친다(D27·D28).
  - `["wire",[[x,y],[x,y],…]]` 꺾은선 도선 · `["node",[x,y]]` 분기점 ● · `["term",[x,y],"a",{"side":"left"}]` 단자 ○
  - `["bat",[x,y],{"dir":"h|v","pos":"right|left|up|down","label":"V","signs":true}]` 전원(긴 판(+)이 pos 쪽, 라벨 오른쪽 아래, `signs`면 극 옆 +·−). 도선은 가로면 x±8, 세로면 y±8 까지만
  - `["sw",[x1,y1],[x2,y2],true|false]` 스위치 · `["bulb",[x,y],{"r":14,"on":true}]` 전구 · `["meter",[x,y],"A|V|G",{"r":16}]` 전류계·전압계 · `["R",[x1,y1],[x2,y2],"R",{…}]` 저항 · `["arrow",[x1,y1],[x2,y2],{"label":"e^-","color":"minus"}]` 전자 이동 화살표 · `["label",[x,y],"\\ce{Zn}",{"size":20,"anchor":"middle"}]`
  - 부품은 SVG **맨 아래층**에 그려지므로, 비커·용액·강조 원 등은 SVG 안에 직접 덧그린다. 도선은 전극 끝까지 정확히 잇는다(캡처로 확인).
- (물리용, 화학 덱에서는 거의 쓰지 않음) 전기력선 `data-field`, 방사형 장 `data-vfield`, 수직 자기장 `data-bgrid`, 축전기 패널 `.cappanel` — 쓰는 법은 본보기 덱과 엔진 머리 주석.

### 5.3 색 의미 (D7, 고정)
`작업지시/화학3과목_공통_약속.md` 4절의 주제별 표를 따른다. 요약: 양이온·$\delta^+$·(+)극 `plus` · 음이온·전자·$\delta^-$·(−)극 `minus` · 공유 전자쌍 `field` · 비공유 전자쌍·$E_\mathrm{a}$ `equi` · 정반응 `field` / 역반응 `bfield` · 산화 `ox` / 환원 `rd` · 보조선 `muted` · 형광펜 `#FFE45C` · 글자 `ink`. 원자 칠은 `data-atom` 원소 색. 화살표에는 무엇의 이동인지 라벨(D2). 그래프 축은 `$t$ [s]`, `$[\ce{A}]$ [M]`, `$V$ [mL]`, `pH` 형식(D4)이고 축 화살표·선과 겹치지 않게.

### 5.4 id (D5)
`<defs>` 의 gradient·marker·clipPath 등 모든 id는 **덱 전체에서 고유**하게: 덱 접두어와 슬라이드 번호를 붙인다(`grad-cm222-07`). 화살표는 marker 대신 `data-arw`를 쓴다.

## 6. 실험실 (가이드라인 5.11 — 성취기준 필수 탐구는 반드시, S12)
```html
<div class="lab" data-lab="cm412dilute">            <!-- labs.js 의 DECK_LABS.cm412dilute 와 연결 -->
  <div class="lab-ctl">
    <div class="ctl"><div class="lbl"><span>희석 횟수</span><output data-o="k"></output></div>
      <input type="range" min="0" max="6" step="1" value="0" data-i="k" aria-label="희석 횟수"></div>
    <div class="res"><div class="small">측정한 pH</div><div class="big"><output data-o="pH"></output></div><output class="kind" data-o="msg"></output></div>
  </div>
  <div class="lab-fig" style="width:563px;height:403px"><svg viewBox="0 0 560 400" width="560" height="400" aria-label="희석과 pH 그래프"></svg>
    <div class="ov" data-ov="l1">$[\ce{H+}]$</div>     <!-- 수식·화학식 라벨은 HTML 겹침(.ov, .ov.mid, .ov.halo)으로, API.place 로 위치 -->
  </div>
</div>
```
```js
window.DECK_LABS = {
  cm412dilute(root, API){
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), V=k=>$(`[data-ov="${k}"]`);
    const svg=$('svg'), g=API.mk('g',{},svg);
    function draw(){ /* 값 읽기 → output 글자 갱신 → g 비우고 다시 그리기(API.atom, API.arrow …) → API.place(V('l1'),x,y) */ }
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',draw)); draw();
    API.loop(root,(dt,t)=>{ /* 입자 운동 등 애니메이션: 슬라이드가 보일 때만 돈다 */ });
  }
};
```
API: `mk(tag,attrs,parent)`, `arrow(g,x1,y1,x2,y2,color,w,dash)`, **`atom(g,x,y,r,원소,라벨,점선)`**, `ATOM`(원자 색 표), `charge(g,x,y,r,sign)`, `texText(parent,x,y,tex,{size,anchor,fill,mix})`(SVG LaTeX 라벨 — **API.ready 안에서 만들면 안 되고**, 처음 그릴 때 만든 것만 KaTeX로 바뀐다. 값이 바뀌는 라벨은 HTML `.ov` 겹침에 `API.tex('\\ce{…}')` 결과를 넣는다), `place(el,x,y,visible)`, `clamp`, `fmtN`, `niceRatio`, `signed`, `COL`, `loop(root,fn)`, `onShow(fn)`, `ready(fn)`, `tex(str)`, `isActive(root)`, (물리용) `vfield`, `fieldAt`, `trace`, `fieldLines`, `bgrid`.
- 슬라이더 옆에 **현재 값과 단위**(`output`), 결과는 크게, 해석은 문장으로(`output.kind`). 극단값에서도 그림이 칸 밖으로 나가지 않게 상한·로그 척도(pH, 농도).
- output 글자는 수식이 아니라 일반 글자(예: `0.10 M`, `pH 3.00`). `$…$`는 output에 넣지 않는다 — 화학식이 바뀌어야 하면 `.ov`.
- **필수 탐구 실험실(S12)**: 탐구 활동 문장의 동사마다 조작·출력이 있어야 한다. "측정하기" → 측정 버튼과 측정값(고정 시드의 작은 오차), "데이터를 수집하여" → 측정할 때마다 결과 표(`table.tight`)에 행이 쌓임, "그래프로 표현하고 해석하기" → 표의 점이 그래프에 찍히고 해석 문장, "설계하고 수행하기" → 조작·종속·통제 변인 고르기 단계, "비교하기" → 두 조건을 한 그래프·표에. 초기화 버튼(`<button data-act="reset">`)을 둔다.
- **움직임**: 입자 운동·반응 진행·전자 흐름 같은 시뮬레이션은 `API.loop`로(보일 때만 돈다). 정적 그림의 움직임은 `data-anim`(가이드 6.4).
- 실험실 동작은 scratchpad의 덱 이름 하위 폴더에 임시 스크립트(헤드리스 Chrome으로 입력 → output 읽기)를 두어 확인한다. `tools/_labtest.mjs`가 그 틀이다.

## 7. 덱 구성 (가이드라인 2.6, 3.3)
권장 순서: 표지(cover, 오른쪽 상징 그림 — 분자 모형·입자 상자 등) → (대단원·중단원 도입: 그 단원 첫 덱만) → 학습 목표(성취기준 `.std` + `ol.goals` + 오늘의 흐름 `.flow`) → 도입(교과서 도입 질문, 예측 질문 S6) → 개념 슬라이드들(**새 개념 앞에는 '왜 필요한가' 연결 슬라이드** S5, 현상 → 입자 → 화학식 S10) → 탐구·해 보기(S7, 안전 S9) + **필수 탐구 실험실(S12)** → 예제·연습 해 보기(판서 공간 + 단계 정답, S8) → 확인하기 → 읽기(과학 마당·이야기·화학과 나의 미래) → 소단원 마무리 활동 → 이 소단원 몫 문항(**한 장에 한 문항**, 그림 + `.board` + 가운데 정답, S2) → 스스로 정리(개념 지도 빈칸) → 스스로 점검하기.
- 교과서의 모든 개념·탐구·활동·예제·문항을 빠짐없이 다룬다. 지도서의 지도 내용(오개념, 발문, 예시 답안·평가 기준)을 반영한다.
- 교과서 문장을 그대로 길게 베끼지 않는다. 정의 문장은 정확히 하되 수업용 문장으로 다시 쓴다. 문항은 숫자·조건·화학식을 그대로 쓰되 문장은 다듬는다.
- 과정이 있는 현상은 단계별 그림 카드(S3), 서로 다른 과정은 슬라이드를 나눈다.
- 한 슬라이드에 정보를 몰아넣지 않는다. 25–40장 정도가 보통이다(과목 약속 분량 메모).

## 8. 점검 (가이드라인 8장)
render.mjs 표준 출력의 자동 점검(D8 넘침·라벨 겹침, T4 칸 넘침, T2 수식 줄바꿈, M1 KaTeX 오류·유니코드 첨자, **C1 본문 글자 화학식**, M2 가운뎃점, T5 flex 글자, D5 중복 id, S2 판서 공간, 3.2 그림 라벨이 화면에서 16px 미만)과 콘솔 오류가 **0건**이어야 한다.
그다음 캡처를 눈으로 본다: 글자·라벨이 선이나 다른 글자와 겹치지 않는가, 전자점이 네 자리에 대칭으로 있는가, 대칭 분자가 대칭인가, 결합각 표시가 맞는가, 반응 전후 원자 수가 같은가, 회로 도선이 끊기지 않았는가, 화살표 방향(전자 이동·쌍극자·$\Delta H$)이 맞는가, 빈 공간이 너무 크거나 한쪽에 몰리지 않았는가, 정답이 가운데 정렬인가.
반응식·계산·필수 탐구 이행은 plan.md 검산 절(공통 약속 11절)과 대조한다.
