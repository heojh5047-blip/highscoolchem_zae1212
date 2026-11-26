/* 과학 공통 본보기 — 실험실 (이름은 덱 접두어 sc001 + 낱말) */
window.DECK_LABS = {
  /* 힘·질량 → 가속도, v–t 그래프(계산값) + 측정 기록 표(고정 시드 오차) */
  sc001run(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), I = k => $(`[data-i="${k}"]`);
    const svg = $('svg');
    // 그래프 틀: 원점 (70,350), t 0–2 s → 가로 230 px/s, v 0–40 m/s → 세로 7.5 px/(m/s)
    const X = t => 70 + 230 * t, Y = v => 350 - 7.5 * v;
    const grid = API.mk('g', {stroke: '#E2E7EC', 'stroke-width': 1.5}, svg);
    [0.5, 1, 1.5, 2].forEach(t => API.mk('line', {x1: X(t), y1: Y(0), x2: X(t), y2: Y(40)}, grid));
    [10, 20, 30, 40].forEach(v => API.mk('line', {x1: X(0), y1: Y(v), x2: X(2), y2: Y(v)}, grid));
    API.arrow(svg, X(0), Y(0), X(2) + 26, Y(0), API.COL.muted, 2.5);
    API.arrow(svg, X(0), Y(0), X(0), Y(40) - 28, API.COL.muted, 2.5);
    [0, 0.5, 1, 1.5, 2].forEach(t => API.texText(svg, X(t), Y(0) + 26, String(t), {size: 18, anchor: 'middle'}));
    [10, 20, 30, 40].forEach(v => API.texText(svg, X(0) - 10, Y(v) + 6, String(v), {size: 18, anchor: 'end'}));
    API.texText(svg, X(2) + 24, Y(0) - 12, '$t$ [s]', {size: 18, anchor: 'end', mix: true});
    API.texText(svg, X(0) + 12, Y(40) - 14, '$v$ [m/s]', {size: 18, mix: true});
    const old = API.mk('g', {}, svg), now = API.mk('g', {}, svg);
    let seed = 7, rec = [];
    const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const line = (g, a, col, w, dash) => {               // v = a t, 그래프 위쪽(40 m/s)에서 자른다
      const tEnd = Math.min(2, 40 / a);
      const attr = {x1: X(0), y1: Y(0), x2: X(tEnd), y2: Y(a * tEnd), stroke: col, 'stroke-width': w, 'stroke-linecap': 'round'};
      if (dash) attr['stroke-dasharray'] = dash;
      API.mk('line', attr, g);
    };
    function draw(){
      const F = +I('F').value, m = +I('m').value, a = F / m;
      O('F').textContent = F + ' N'; O('m').textContent = m + ' kg';
      O('a').textContent = a.toFixed(2);
      O('msg').textContent = `a = F ÷ m = ${F} ÷ ${m}`;
      now.textContent = ''; line(now, a, API.COL.plus, 4);
      old.textContent = ''; rec.forEach(r => line(old, r.a, API.COL.grav, 2.5, '6 6'));
      O('rows').innerHTML = rec.slice(-5).map(r => `<tr><td>${r.n}</td><td>${r.F}</td><td>${r.m}</td><td>${r.a.toFixed(2)}</td></tr>`).join('');
    }
    root.querySelectorAll('input').forEach(i => i.addEventListener('input', draw));
    $('[data-act="measure"]').addEventListener('click', () => {
      const F = +I('F').value, m = +I('m').value, a = F / m * (1 + 0.06 * (rnd() - 0.5));
      rec.push({n: rec.length + 1, F, m, a}); draw();
    });
    $('[data-act="reset"]').addEventListener('click', () => { rec = []; seed = 7; I('F').value = 8; I('m').value = 2; draw(); });
    draw();
  }
};
