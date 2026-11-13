# 덱 작성 안내 (에이전트·개발자용 — 범용)

이 폴더는 **16:9 HTML 슬라이드 덱**을 만드는 원본이다. 최상위 규칙은 `../../docs/슬라이드_제작_가이드라인_범용.md`(이하 "가이드라인")이고, 이 문서는 그 규칙을 이 엔진에서 **어떻게 쓰는지**를 적는다. 대상별 흐름·장수는 `작업지시/약속_예시/<대상>_약속.md`가 정한다.
본보기 덱은 들어 있지 않다. 이 묶음으로 처음 완성해 검토를 마친 덱이 다음 덱의 본보기다(같은 묶음 키 안에서 먼저 만든 덱의 `slides.html`을 읽고 꼴을 맞춘다).

## 1. 폴더와 작업 흐름

```
차시자료/
  <묶음 키>/<file>.html              ← 빌드본 (점검·캡처용, 손으로 고치지 않음)
  완성본/<묶음 키>/<file>.html       ← 완성본 = 선생님이 받는 파일 (오프라인 단일 HTML, build.py --offline)
  목록.html                          ← (선택) 덱 목록 한 장 (tools/site_index.py)
  _소스/
    AUTHORING.md          이 문서
    묶음설정.json         {"credit": "제작: ○○학교 ○○○", "title": "목록.html 제목"} — 꼬리말은 모든 덱 표지 왼쪽 아래에 들어감
    engine/               harness.css·harness.js·harness-ui.html (고치지 않는다)
    vendor/katex/         KaTeX 0.16.11 사본(MIT) — 완성본에 넣을 수식 글꼴
    content/<묶음 키>/<덱 폴더>/
      plan.md             구성안(화면 문장 전문, 목표 이행 대응표, 출처, 확인이 필요한 점)
      meta.json           {"title":"실험실 안전 교육","file":"1_실험실_안전_교육","header":"1차시 실험실 안전 교육 (교사 연수, 50분)"}
                          (선택) "credit": "…" — 이 덱만 꼬리말을 바꿈, "" 이면 넣지 않음
      slides.html         <section class="slide"> … 들만 (엔진 껍데기 없이)
      labs.js             (선택) window.DECK_LABS = { 이름(root, API){…} };
      extra.css           (선택) 이 덱 전용 스타일. 클래스 이름은 덱 접두어로 (.ts1-…)
      img/                (선택) 그림·화면 갈무리 — src="img/파일.png" 는 빌드 때 파일 안에 들어감
      자료/               (선택) 선생님이 준 PDF·문서와 그 추출 텍스트(_추출.txt). 완성본에는 들어가지 않음
    작업지시/             공통.md, 약속_예시/, 덱목록.json, 검토/
    tools/                build.py, offline.mjs, render.mjs, sheet.py, motion_check.mjs, ask_check.mjs, verify_offline.mjs …
    _render/              캡처 (만들어짐, 지워도 됨)
```

작업 순서: `slides.html`·`labs.js` 작성 → `python build.py <묶음 키>/<덱 폴더>` → `node render.mjs "../../<묶음 키>/<file>.html" "../_render/<묶음 키>/<덱 폴더>"` → 표준 출력의 **자동 점검·콘솔 오류**를 0으로 → `_render/…/sNN.png`(또는 `sheet.py` 모음)를 **Read로 직접 보고** 겹침·잘림·빈 공간을 고친다 → 반복 → 끝나면 `python build.py <덱> --offline` → `node verify_offline.mjs "../../완성본/<묶음 키>/<file>.html"`.
명령은 `_소스/tools` 폴더에서 실행한다. 캡처는 "모든 단계를 펼친" 상태다. 단계가 서로를 덮는 장은 `--steps`(하위 폴더로)로 단계별 캡처도 본다.

## 2. 슬라이드 기본 구조

```html
<section class="slide cover" data-sec="교사 연수 · 1차시" data-title="표지">
  <div class="cover-text">
    <div class="kicker">과학실 안전과 교구 관리 · 1차시</div>
    <h1>실험실<br><span class="acc">안전 교육</span></h1>
    <p class="sub">사고는 준비한 만큼 줄어든다</p>
    <p class="meta">교사 연수 · 50분</p>
  </div>
  <svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="보안경과 장갑을 그린 상징 그림">…</svg>
</section>

<section class="slide" data-sec="01 · 왜 안전 교육인가" data-title="여는 질문">
  <h2><span class="tag q">여는 질문</span>우리 과학실에서 가장 아찔했던 순간은?</h2>
  …
</section>
```
- 무대 1280×720, 안전 여백 위 78·좌우 84·아래 64(패딩으로 잡혀 있음). 위 띠는 엔진이 자동으로 붙인다.
- `data-sec` = 머리띠 왼쪽 글, `data-title` = 목차에 뜰 짧은 제목. 표지는 `class="slide cover"`(꼬리말이 여기 들어감).
- 제목 앞 표식: `<span class="no">1</span>`(번호) · `<span class="tag">실습</span>`(활동) · `.tag.alt`(연결·다시 보기) · `.tag.q`(질문·확인) · `.tag.ex`(사례·예) · `.tag.ink`(정리). 표식 글은 대상 약속 파일의 목록대로.
- 레이아웃: `.row > .col`(`.row.stretch`, `.col.stack`, 열 너비 `style="flex:0 0 440px"`), `.card`(`.q`, `.tip`), `.note`(`.puzzle`, `.q`, `.big`), `.stages`(3열, `.c2` 2열) > `.stage`, `.flow > .fnode(.hl) + .farr`, `.std` + `.code`(인용 문장·기준 문장), `ol.goals`, `.chips > button.chk`(체크 칩), `table`(`.tight`, `td.l`), `.bogi` + `.choices`(객관식), `.blank`(빈칸, 안에 `.step` 정답).
- 핵심 상자 `.formula`(`.sm`) + 안에 `.unit`(설명 줄). 정답 `.answer`(여러 개면 `.answers`). 판서 공간 `.board`(`.col.stack` 안에서 남는 높이를 채움).
- 글자 크기: 본문 24px, `.f22` `.f21`, 보조 `.small`(19px). **19px 아래로 내리지 않는다.** 넘치면 문장을 줄이거나 장을 나눈다. `.note.big`(21px).
- 형광펜 `<mark>`는 핵심 정의·꼭 기억할 한 문장에만.
- 색 클래스: `.c-plus`(위험·금지) `.c-minus`(정보) `.c-field`(권장·바른 예) `.c-muted`.

## 3. 단계 공개 (S1)
- `.step`은 문서 순서대로 하나씩. **같은 `data-g`**는 함께(`<g class="step" data-g="a2">` + `<p class="step" data-g="a2">`).
- **공개 순서는 각 data-g 그룹이 DOM에서 처음 나오는 위치**로 정해진다. 순서를 고정하려면 원하는 자리에 빈 `<span class="step" data-g="…"></span>`을 먼저 둔다.
- SVG 라벨은 기준선 아래로 글자 크기의 약 0.35배가 더 내려간다. viewBox 가장자리 라벨은 0.4×크기 이상 여유(D8).
- render.mjs는 시작할 때 출력 폴더의 s*.png를 지운다. `--steps` 캡처는 하위 폴더로.
- 답·결론·사례의 결말은 `.step`. 처음부터 보여 줄 것에는 붙이지 않는다.
- 낱말 묶기: 엔진이 낱말마다 `span.w`(nowrap)로 감싸고, 수식·빈칸 바로 앞뒤에 **붙여 쓴** 조사·괄호·문장 부호도 한 덩어리로 묶는다.
- 질문 먼저(가이드라인 6.5): 답 단계 앞 질문에는 '?' 또는 'Q'. 지시문에는 `data-q`.

## 4. 수식 (수식이 있을 때만)
- 본문 `$…$`, 블록 `$$…$$`. 숫자·단위는 `\text{}`: `$10\ \text{분}$`, `$25\ {}^\circ\text{C}$`.
- 단위 곱 `\cdot`(가운뎃점 금지), 유니코드 첨자 금지, 아래첨자 글자는 `V_\mathrm{A}`.
- 괄호 `\left( … \right)`, 여러 줄 `\begin{aligned} … &= … \end{aligned}`.
- 화학식은 `$\ce{H2O}$`(mhchem — 빌드가 불러온다). 화학이 아닌 낱말이 C1에 걸리면 `<span data-audit="skip">A4</span>` 또는 `$\text{A4}$`(가이드라인 2.3).
- HTML 속성 안의 `<`, `>`는 `&lt;` `&gt;`.

## 5. 그림
**직접 그린 SVG** 또는 선생님이 준 그림·화면 갈무리(`img/`)만 쓴다. 교과서·인터넷 그림을 베끼지 않는다.
`svg.fig` + `viewBox` + `style="width:…px"`로 크기를 정하고 `aria-label`을 단다. 장식용은 `aria-hidden="true"`.

### 5.1 SVG 라벨 — 그림 속 글자는 전부 이것으로
```html
<text class="tex" x="200" y="40" data-mix="보안경||착용" data-size="22" data-anchor="middle"></text>
<text class="tex" x="120" y="80" data-mix="출구 쪽으로" data-size="20" data-weight="700" data-halo="1" fill="#2E9E6A"></text>
<text class="tex" x="60" y="120" data-tex="t_{1/2}" data-size="22"></text>
```
x, y는 **글자 기준선**. `data-anchor` start|middle|end, `||` 줄바꿈, `data-halo` 흰 바탕. `data-mix`는 한글과 `$수식$`을 섞을 때, `data-tex`는 수식만.
**라벨 크기**: `data-size`는 viewBox 단위라 SVG가 줄어 보이면 라벨도 줄어든다. **화면에서 18px 이상**이 되게 정하거나 viewBox를 표시 크기에 맞춘다(16px 미만이면 점검 `3.2`). 일부러 겹친 라벨은 `data-overlap="ok"`.

### 5.2 엔진 부품
- 화살표 `<g data-arw="x1,y1,x2,y2,색,굵기[,d]">` — 색: ink plus minus field equi bfield ox rd grav muted white 또는 #hex. 흐름·순서·이동에 쓰고 라벨을 단다(D2).
- 표시 원 `<g data-chg="x,y,r,+|-|P|M|N[,d]">`, ± 묶음 `<g data-pm="+|-,크기,x:y x:y …[,색]">`.
- 단계 카드·흐름·표는 HTML 레이아웃(2절)으로 만드는 편이 고치기 쉽다. 배치도·순서도처럼 위치가 중요한 그림만 SVG로.
- 체크리스트(가이드라인 S14):
  ```html
  <div class="chips"><button class="chk">보안경을 썼다</button><button class="chk">환기 장치를 켰다</button></div>
  ```
  `.chips.sm .chk`(18px)는 쓰지 않는다.

### 5.3 교과 전용 부품 (교과 수업 덱에서만)
`<g data-atom="x,y,r,원소[,라벨|-][,d]">`(원자 모형), `<svg data-circuit='{"parts":[…]}'>`(회로도), `data-field`·`data-vfield`·`data-bgrid`(장), `.cappanel` — 엔진 `harness.js` 머리 주석에 형식이 있다. 쓰기 전에 짧은 시험 장을 만들어 캡처로 모양을 확인한다.

### 5.4 색 뜻 (D7, 가이드라인 2.5)
위험·금지 `plus` · 정보·차례 `minus` · 권장·바른 예·완료 `field` · 주의·확인 `equi` · 셋째 범주 `bfield` · 보조선 `muted` · 지난 단계·다른 덱 몫 `grav` · 형광펜 `#FFE45C`. 실제 기준 색이 있는 것(안전 표지 등)은 출처의 색.

### 5.5 id (D5)
`<defs>`의 gradient·marker·clipPath 등 모든 id는 **덱 전체에서 고유**: 덱 접두어 + 슬라이드 번호(`grad-ts1-07`). 화살표는 marker 대신 `data-arw`.

## 6. 실험실 (인터랙티브)
```html
<div class="lab" data-lab="ts1store">            <!-- labs.js 의 DECK_LABS.ts1store 와 연결 -->
  <div class="lab-ctl">
    <div class="ctl"><div class="lbl"><span>보관 온도</span><output data-o="T"></output></div>
      <input type="range" min="0" max="40" step="1" value="20" data-i="T" aria-label="보관 온도"></div>
    <div class="res"><div class="small">판단</div><div class="big"><output data-o="ok"></output></div><output class="kind" data-o="msg"></output></div>
    <p><button class="btn" data-act="reset">처음으로</button></p>
  </div>
  <div class="lab-fig" style="width:563px;height:403px"><svg viewBox="0 0 560 400" width="560" height="400" aria-label="보관 조건 그림"></svg>
    <div class="ov" data-ov="l1">라벨</div>     <!-- 바뀌는 라벨은 HTML 겹침(.ov, .ov.mid, .ov.halo) + API.place -->
  </div>
</div>
```
```js
window.DECK_LABS = {
  ts1store(root, API){
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), I=k=>$(`[data-i="${k}"]`);
    const svg=$('svg'), g=API.mk('g',{},svg);
    function draw(){ const T=+I('T').value; O('T').textContent=T+' °C'; /* 판단 → O('ok'), O('msg') 글자, g 비우고 다시 그리기 */ }
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',draw));
    $('[data-act="reset"]').addEventListener('click',()=>{ I('T').value=20; draw(); });
    draw();
  }
};
```
API: `mk(tag,attrs,parent)`, `arrow(g,x1,y1,x2,y2,color,w,dash)`, `charge(g,x,y,r,sign)`, `texText(parent,x,y,tex,{size,anchor,fill,mix})`(처음 그릴 때 만든 것만 KaTeX로 바뀜 — 값이 바뀌는 라벨은 `.ov` + `API.tex()`), `place(el,x,y,visible)`, `clamp`, `fmtN`, `signed`, `COL`, `loop(root,fn)`(보일 때만 도는 애니메이션), `onShow(fn)`, `ready(fn)`, `tex(str)`, `isActive(root)`, (교과용) `atom`, `ATOM`, `vfield`, `fieldAt`, `trace`, `fieldLines`, `bgrid`.
- 조작 옆에 현재 값과 단위(`output`, 일반 글자 — `$…$` 넣지 않음), 결과는 크게, 해석은 문장으로. 극단값에서도 그림이 칸 안에.
- 실험실 동작은 scratchpad의 덱 이름 하위 폴더에 임시 스크립트(헤드리스 Chrome으로 단추 누르기 → output 읽기)로 확인한다. 틀: `tools/_labtest.mjs`, 공용 연결: `tools/평가/cdp.mjs`의 `launch()`.

### 6.1 실습 타이머 (연수·활동용 — 시험을 마친 코드)
```html
<div class="lab" data-lab="ts1timer" data-min="10">
  <div class="lab-ctl" style="flex:1 1 auto">
    <div class="res"><div class="small">남은 시간</div><div class="big"><output data-o="t">10:00</output></div><output class="kind" data-o="msg">시작을 누르세요</output></div>
    <p><button class="btn" data-act="go">시작</button> <button class="btn" data-act="plus">+1분</button> <button class="btn" data-act="reset">처음으로</button></p>
  </div>
</div>
```
```js
  // 실습 타이머: data-min(분)에서 거꾸로 센다. 슬라이드를 넘겨도 계속 돌고, 0이 되면 문구가 바뀐다.
  ts1timer(root, API){
    const O = k => root.querySelector(`[data-o="${k}"]`), B = k => root.querySelector(`[data-act="${k}"]`);
    const full = (+root.dataset.min || 10) * 60;
    let left = full, endAt = 0, id = 0;
    const fmt = s => String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0');
    function show(){
      O('t').textContent = fmt(Math.max(0, Math.ceil(left)));
      O('msg').textContent = left <= 0 ? '시간이 끝났습니다 — 정리해 주세요' : id ? (left <= 60 ? '1분 남았습니다' : '진행 중') : (left < full ? '멈춤' : '시작을 누르세요');
      B('go').textContent = id ? '멈춤' : '시작';
    }
    function tick(){ left = (endAt - Date.now()) / 1000; if (left <= 0){ left = 0; clearInterval(id); id = 0; } show(); }
    B('go').addEventListener('click', () => { if (id){ clearInterval(id); id = 0; } else if (left > 0){ endAt = Date.now() + left * 1000; id = setInterval(tick, 250); } show(); });
    B('plus').addEventListener('click', () => { left += 60; if (id) endAt += 60000; show(); });
    B('reset').addEventListener('click', () => { clearInterval(id); id = 0; left = full; show(); });
    show();
  }
```
한 덱에 타이머가 여럿이면 실험실 이름을 하나로 두고(`data-lab="ts1timer"`), 장마다 `data-min`만 바꾼다(같은 함수가 장마다 따로 돈다).

## 7. 덱 구성
대상 약속 파일(`작업지시/약속_예시/`)의 구성과 장수를 따른다. 공통 원칙:
- 표지 → 목표·흐름 → 여는 질문 → 내용(새 내용 앞 '왜 필요한가' S5, 사례 → 그림 → 정리 S10) → 활동·실습(S7, S13) → 정리(S14) → 마무리(질문·다음 안내).
- 한 장에 정보를 몰아넣지 않는다. 과정은 단계 카드(S3), 서로 다른 과정은 장을 나눈다.
- 선생님이 준 자료의 문장을 길게 베끼지 않는다. 사실은 출처대로(S15), 화면 아래 `.small`에 출처.

## 8. 점검
render.mjs 표준 출력의 자동 점검(D8 넘침·라벨 겹침, T4 칸 넘침, T2 수식 줄바꿈, M1 KaTeX 오류·유니코드 첨자, C1, M2, T5, D5, S2, 3.2 라벨 크기)과 콘솔 오류가 **0건**이어야 한다.
그다음 캡처를 눈으로 본다: 글자·라벨이 선이나 다른 글자와 겹치지 않는가, 같은 종류 카드의 크기·간격이 같은가, 화살표 방향·순서가 맞는가, 빈 공간이 너무 크거나 한쪽에 몰리지 않았는가, 정답이 가운데인가, 표지 꼬리말이 그림과 겹치지 않는가.
마지막으로 완성본을 만들고 `verify_offline.mjs`가 OK(외부 요청 0, 점검 0)인지 본다.
