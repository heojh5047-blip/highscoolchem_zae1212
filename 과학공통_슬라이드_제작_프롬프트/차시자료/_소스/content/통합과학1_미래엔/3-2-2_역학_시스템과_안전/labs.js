/* 3-2-2 역학 시스템과 안전 — 실험실 (덱 접두어 is1322) */
window.DECK_LABS = {
  /* 달걀 낙하: 높이와 바닥을 고르면 충돌 직전 속력·운동량, 충돌 시간, 힘–시간 그래프(반사인, 넓이 = 충격량)와 최대 힘이 나오고 깨짐 한계(덱이 정한 25 N)와 비교한다.
     달걀 질량 0.06 kg, g = 9.8, 충돌 시간: 나무판 0.005 s · 방석 0.04 s · 스펀지 0.06 s · 에어 매트 0.12 s (덱이 정한 값) */
  is1322egg(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), I = k => $(`[data-i="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const M = 0.06, G = 9.8, LIM = 25;
    const SURF = [['나무판', 0.005, '#C8A27A'], ['방석', 0.04, '#7FB3E6'], ['스펀지', 0.06, '#F7C548'], ['에어 매트', 0.12, '#8BD3A7']];
    let s = -1, rec = [], stopA = null;
    const scene = API.mk('g', {}, svg), graph = API.mk('g', {}, svg), tab = API.mk('g', {}, svg);
    const calc = (h, k) => { const v = Math.sqrt(2 * G * h), p = M * v, t = SURF[k][1]; return {v, p, t, F: Math.PI / 2 * p / t}; };
    function drawScene(y, broken){
      scene.innerHTML = '';
      API.mk('rect', {x: 0, y: 0, width: 170, height: 250, rx: 10, fill: '#F6F9FC', stroke: '#C9D3DD'}, scene);
      if (s >= 0) API.mk('rect', {x: 20, y: 214, width: 130, height: 20, rx: 6, fill: SURF[s][2]}, scene);
      else T(scene, 85, 230, '바닥을 고르자', {size: 16, anchor: 'middle', fill: API.COL.muted});
      const ey = y == null ? 40 : y;
      if (broken) { API.mk('path', {d: `M60 214 Q85 196 110 214 Z`, fill: '#FDF1E4', stroke: '#C2410C', 'stroke-width': 2}, scene); API.mk('ellipse', {cx: 85, cy: 210, rx: 18, ry: 5, fill: '#F7C548'}, scene); }
      else API.mk('ellipse', {cx: 85, cy: ey, rx: 16, ry: 20, fill: '#FDF1E4', stroke: '#C2410C', 'stroke-width': 2}, scene);
      T(scene, 85, 20, `h = ${(+I('h').value).toFixed(1)} m`, {size: 16, anchor: 'middle'});
    }
    function axes(){
      graph.innerHTML = '';
      const x0 = 210, y0 = 230, w = 330, h = 200;
      API.mk('line', {x1: x0, y1: y0, x2: x0 + w, y2: y0, stroke: API.COL.muted, 'stroke-width': 2}, graph);
      API.mk('line', {x1: x0, y1: y0, x2: x0, y2: y0 - h, stroke: API.COL.muted, 'stroke-width': 2}, graph);
      T(graph, x0 - 6, y0 - h + 4, '힘', {size: 16, anchor: 'end'}); T(graph, x0 + w, y0 + 20, '시간 (0–0.13 s)', {size: 16, anchor: 'end'});
      const yl = y0 - LIM / 100 * h;
      API.mk('line', {x1: x0, y1: yl, x2: x0 + w, y2: yl, stroke: API.COL.plus, 'stroke-width': 2, 'stroke-dasharray': '8 6'}, graph);
      T(graph, x0 + w, yl - 6, `깨짐 한계 ${LIM} N`, {size: 16, anchor: 'end', fill: API.COL.plus});
      return {x0, y0, w, h};
    }
    function curve(c, k, col, op){
      const {x0, y0, w, h} = axes._g;
      const pts = []; const n = 40;
      for (let i = 0; i <= n; i++) { const tt = c.t * i / n, f = c.F * Math.sin(Math.PI * i / n); pts.push(`${(x0 + tt / 0.13 * w).toFixed(1)},${(y0 - Math.min(f, 100) / 100 * h).toFixed(1)}`); }
      API.mk('polygon', {points: `${x0},${y0} ` + pts.join(' ') + ` ${(x0 + c.t / 0.13 * w).toFixed(1)},${y0}`, fill: col, 'fill-opacity': op * .6, stroke: col, 'stroke-opacity': op, 'stroke-width': 3}, graph);
      if (c.F > 100) T(graph, x0 + 8, y0 - h + 18, `최대 ${c.F.toFixed(0)} N ↑`, {size: 16, fill: API.COL.plus, weight: 700});
    }
    function drawGraph(){
      axes._g = axes();
      rec.slice(-3).forEach((r, i, a) => curve(r.c, r.k, SURF[r.k][2], i === a.length - 1 ? 1 : .5));
    }
    function drawTab(){
      tab.innerHTML = '';
      API.mk('rect', {x: 0, y: 262, width: 560, height: 174, rx: 10, fill: '#F6F9FC', stroke: '#C9D3DD', 'stroke-width': 2}, tab);
      const X = [12, 104, 186, 312, 410, 500];
      ['바닥', '높이', '충격량[N·s]', '충돌 시간', '최대 힘', '결과'].forEach((h, i) => T(tab, X[i], 288, h, {size: 16, weight: 700}));
      rec.slice(-5).forEach((r, j) => {
        const y = 314 + j * 24;
        T(tab, X[0], y, SURF[r.k][0], {size: 16}); T(tab, X[1], y, `${r.h.toFixed(1)} m`, {size: 16}); T(tab, X[2], y, r.c.p.toFixed(3), {size: 16});
        T(tab, X[3], y, `${r.c.t} s`, {size: 16}); T(tab, X[4], y, `${r.c.F.toFixed(1)} N`, {size: 16});
        T(tab, X[5], y, r.c.F > LIM ? '깨짐' : '안전', {size: 16, fill: r.c.F > LIM ? API.COL.plus : API.COL.field, weight: 700});
      });
    }
    function sync(){ O('surf').querySelectorAll('[data-s]').forEach(b => b.classList.toggle('on', +b.dataset.s === s)); }
    I('h').addEventListener('input', () => { O('h').textContent = (+I('h').value).toFixed(1); drawScene(); });
    O('surf').querySelectorAll('[data-s]').forEach(b => b.addEventListener('click', () => { s = +b.dataset.s; sync(); drawScene(); O('msg').textContent = ''; }));
    $('[data-act="drop"]').addEventListener('click', () => {
      if (s < 0) { O('msg').textContent = '바닥을 먼저 고르자.'; return; }
      if (stopA) { stopA(); stopA = null; }
      const h = +I('h').value, c = calc(h, s), broken = c.F > LIM; let t = 0;
      stopA = API.loop(root, dt => { t += dt; const y = 40 + Math.min(1, (t / 0.7) ** 2) * 154; drawScene(y, false); if (t >= 0.7) { stopA(); stopA = null; drawScene(194, broken);
        rec.push({h, k: s, c}); drawGraph(); drawTab();
        O('msg').textContent = `${SURF[s][0]}, ${h.toFixed(1)} m: 충돌 직전 속력 ${c.v.toFixed(2)} m/s, 충격량 ${c.p.toFixed(3)} N·s, 충돌 시간 ${c.t} s → 최대 힘 ${c.F.toFixed(1)} N → ${broken ? '깨졌다!' : '깨지지 않았다.'}`; } });
    });
    $('[data-act="sum"]').addEventListener('click', () => {
      const hs = new Set(rec.map(r => r.h.toFixed(1))), ks = new Set(rec.map(r => r.k));
      if (ks.size < 2) { O('msg').textContent = '같은 높이에서 바닥을 2가지 이상 바꿔 떨어뜨려 보자.'; return; }
      let m = '같은 높이면 충격량(그래프 넓이)은 같다. 충돌 시간이 긴 바닥일수록 최대 힘이 작아 달걀이 깨지지 않는다.';
      m += hs.size >= 2 ? ' 높이를 낮추면(속력을 줄이면) 충격량 자체가 줄어든다.' : ' 높이도 바꿔 보자.';
      O('msg').textContent = m;
    });
    $('[data-act="reset"]').addEventListener('click', () => { if (stopA) { stopA(); stopA = null; } s = -1; rec = []; O('msg').textContent = ''; sync(); drawScene(); drawGraph(); drawTab(); });
    drawScene(); drawGraph(); drawTab();
  }
};
