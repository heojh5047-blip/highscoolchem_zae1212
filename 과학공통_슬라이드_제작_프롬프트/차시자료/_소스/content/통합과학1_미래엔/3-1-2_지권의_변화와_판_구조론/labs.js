/* 3-1-2 지권의 변화와 판 구조론 — 실험실 (덱 접두어 is1312) */
window.DECK_LABS = {
  /* 판의 경계 살펴보기: 경계 종류를 고르면 단면(보존형은 위에서 본 그림)과 판의 이동, 지진·화산 여부, 지형, 실제 예가 나온다(교과서 113–115쪽) */
  is1312plate(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const OC = '#5B6B7F', CO = '#8C6A4F', MAG = '#D7263D';
    const K = [
      {n: '발산형 — 해양판끼리', q: 1, v: 1, land: '해령(해저 산맥)', ex: '동태평양 해령'},
      {n: '발산형 — 대륙 안', q: 1, v: 1, land: '열곡대', ex: '동아프리카 열곡대'},
      {n: '보존형', q: 1, v: 0, land: '변환 단층', ex: '산안드레아스 단층'},
      {n: '수렴형 — 해양판·대륙판', q: 1, v: 1, land: '해구, 습곡 산맥', ex: '안데스산맥'},
      {n: '수렴형 — 해양판·해양판', q: 1, v: 1, land: '해구, 호상열도', ex: '마리아나 해구'},
      {n: '수렴형 — 대륙판·대륙판', q: 1, v: 0, land: '습곡 산맥', ex: '히말라야산맥'}];
    let k = -1, seen = new Set(), t = 0;
    const base = API.mk('g', {}, svg), mov = API.mk('g', {}, svg), info = API.mk('g', {}, svg);
    const P = (d, fill) => API.mk('path', {d, fill}, base);
    const star = (x, y) => API.mk('path', {d: `M${x} ${y - 13} l5 9 l10 1 l-8 7 l3 10 l-10 -6 l-10 6 l3 -10 l-8 -7 l10 -1 Z`, fill: '#F7C548', stroke: '#C2410C', 'stroke-width': 1.5}, base);
    const volc = (x, y, s = 1) => { API.mk('path', {d: `M${x - 22 * s} ${y} L${x} ${y - 34 * s} L${x + 22 * s} ${y} Z`, fill: '#6B4F3A'}, base); API.mk('path', {d: `M${x - 4} ${y - 34 * s} Q${x} ${y - 60 * s} ${x + 6} ${y - 34 * s} Z`, fill: MAG}, base); };
    // 판 위에서 움직이는 화살 표시(띠): [x0, x1, y, 방향 ±1]
    let bands = [];
    function drawBase(){
      base.innerHTML = ''; bands = [];
      API.mk('rect', {x: 0, y: 0, width: 560, height: 280, rx: 12, fill: '#EEF4F8'}, base);
      if (k < 0) { T(base, 280, 140, '왼쪽에서 판의 경계를 고르자', {size: 19, anchor: 'middle', fill: API.COL.muted}); return; }
      if (k !== 2) API.mk('rect', {x: 0, y: 170, width: 560, height: 110, fill: '#F7C548', opacity: .45}, base);
      if (k === 0) { P('M20 110 H270 V150 H20 Z', OC); P('M290 110 H540 V150 H290 Z', OC); P('M262 110 L280 80 L298 110 Z', '#6B7B8F'); P('M272 280 Q276 180 280 90 Q284 180 288 280 Z', MAG); star(240, 100); volc(280, 90, .5); bands = [[30, 250, 128, -1], [310, 530, 128, 1]]; API.mk('rect', {x: 0, y: 0, width: 560, height: 105, fill: '#7FB3E6', opacity: .35}, base); }
      if (k === 1) { P('M20 90 H250 L262 150 H20 Z', CO); P('M310 90 H540 V150 H298 Z', CO); P('M250 90 L280 140 L310 90 Z', '#EEF4F8'); P('M272 280 Q276 200 280 145 Q284 200 288 280 Z', MAG); star(230, 80); volc(330, 90, .6); bands = [[30, 230, 120, -1], [330, 530, 120, 1]]; }
      if (k === 2) { P('M20 30 H540 V136 H20 Z', '#8C99A6'); P('M20 144 H540 V250 H20 Z', OC); API.mk('line', {x1: 20, y1: 140, x2: 540, y2: 140, stroke: '#16233D', 'stroke-width': 4, 'stroke-dasharray': '12 6'}, base); star(280, 140); T(base, 30, 24, '위에서 본 그림', {size: 16, fill: API.COL.muted}); bands = [[40, 520, 84, -1], [40, 520, 196, 1]]; }
      if (k === 3) { P('M20 120 H300 L380 270 L350 275 L280 150 H20 Z', OC); P('M300 80 H540 V160 H330 Z', CO); P('M330 80 L380 40 L430 80 Z', '#6B4F3A'); volc(380, 44, .6); P('M292 118 L300 135 L310 118 Z', '#EEF4F8'); star(310, 150); star(345, 210); API.mk('rect', {x: 0, y: 0, width: 300, height: 115, fill: '#7FB3E6', opacity: .35}, base); T(base, 280, 112, '해구', {size: 16, anchor: 'end'}); bands = [[30, 270, 138, 1]]; }
      if (k === 4) { P('M20 120 H260 L340 270 L310 275 L240 150 H20 Z', OC); P('M260 115 H540 V150 H285 Z', '#6B7B8F'); volc(360, 115, .6); volc(420, 115, .5); P('M252 118 L260 135 L270 118 Z', '#EEF4F8'); star(270, 150); star(305, 210); API.mk('rect', {x: 0, y: 0, width: 560, height: 112, fill: '#7FB3E6', opacity: .35}, base); T(base, 390, 60, '호상열도', {size: 16, anchor: 'middle'}); T(base, 250, 112, '해구', {size: 16, anchor: 'end'}); bands = [[30, 230, 138, 1]]; }
      if (k === 5) { P('M20 100 H270 V170 H20 Z', CO); P('M270 100 H540 V170 H270 Z', '#A27D5E'); P('M200 100 Q240 30 270 20 Q300 30 340 100 Z', '#6B4F3A'); P('M230 100 Q260 50 270 45 Q280 50 310 100 Z', '#8C6A4F'); star(270, 140); bands = [[30, 190, 135, 1], [350, 530, 135, -1]]; }
    }
    function drawMov(){
      mov.innerHTML = '';
      bands.forEach(([x0, x1, y, d]) => {
        for (let x = x0; x < x1; x += 60) {
          const xx = x0 + ((x - x0 + d * t * 30) % (x1 - x0) + (x1 - x0)) % (x1 - x0);
          API.mk('path', {d: d > 0 ? `M${xx} ${y - 8} l12 8 l-12 8` : `M${xx + 12} ${y - 8} l-12 8 l12 8`, fill: 'none', stroke: '#FFFFFF', 'stroke-width': 3}, mov);
        }
      });
    }
    function drawInfo(){
      info.innerHTML = '';
      API.mk('rect', {x: 0, y: 292, width: 560, height: 144, rx: 12, fill: '#F6F9FC', stroke: '#C9D3DD', 'stroke-width': 2}, info);
      if (k < 0) return;
      const c = K[k];
      T(info, 20, 324, c.n, {size: 20, weight: 700});
      T(info, 20, 356, `지진: ${c.q ? '자주 발생' : '드묾'}`, {size: 18, fill: c.q ? API.COL.plus : API.COL.muted});
      T(info, 200, 356, `화산 활동: ${c.v ? '활발' : (k === 2 ? '거의 없음' : '없음')}`, {size: 18, fill: c.v ? API.COL.plus : API.COL.muted});
      T(info, 20, 388, `지형: ${c.land}`, {size: 18});
      T(info, 20, 418, `예: ${c.ex}`, {size: 18});
      T(info, 540, 418, `살펴본 경계 ${seen.size} / 6`, {size: 16, anchor: 'end', fill: API.COL.muted});
    }
    function sync(){ O('kind').querySelectorAll('[data-k]').forEach(b => b.classList.toggle('on', +b.dataset.k === k)); }
    O('kind').querySelectorAll('[data-k]').forEach(b => b.addEventListener('click', () => { k = +b.dataset.k; seen.add(k); O('msg').textContent = ''; sync(); drawBase(); drawMov(); drawInfo(); }));
    $('[data-act="sum"]').addEventListener('click', () => {
      if (seen.size < 6) { O('msg').textContent = `아직 ${6 - seen.size}가지 경계를 살펴보지 않았다.`; return; }
      O('msg').textContent = '모든 경계에서 지진이 자주 일어난다. 화산 활동은 판이 갈라지는 발산형 경계와 판이 섭입하는 수렴형 경계에서 활발하고, 보존형 경계와 대륙판끼리 충돌하는 곳에서는 거의 없다.';
    });
    $('[data-act="reset"]').addEventListener('click', () => { k = -1; seen = new Set(); O('msg').textContent = ''; sync(); drawBase(); drawMov(); drawInfo(); });
    API.loop(root, dt => { if (k < 0) return; t += dt; drawMov(); });
    drawBase(); drawInfo();
  }
};
