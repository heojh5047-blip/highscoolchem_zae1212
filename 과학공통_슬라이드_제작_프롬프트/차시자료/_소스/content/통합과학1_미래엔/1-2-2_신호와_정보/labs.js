/* 1-2-2 신호와 정보 — 실험실 (덱 접두어 is1122) */
window.DECK_LABS = {
  /* 스마트 기기로 거리·시간을 재고 속력 분석: 측정마다 기록 표 + 거리–시간 그래프(원점에서 측정 점까지 선, 기울기 = 속력) */
  is1122run(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), I = k => $(`[data-i="${k}"]`);
    const svg = $('svg');
    const M = [['걷기', 1.4, API.COL.grav], ['뛰기', 5.4, API.COL.plus], ['자전거', 7.3, API.COL.bfield]];
    // 그래프: 원점 (70,340), 시간 0–45 s → 10 px/s, 거리 0–60 m → 5 px/m
    const X = t => 70 + 10 * t, Y = d => 340 - 5 * d;
    const grid = API.mk('g', {stroke: '#E2E7EC', 'stroke-width': 1.5}, svg);
    [10, 20, 30, 40].forEach(t => API.mk('line', {x1: X(t), y1: Y(0), x2: X(t), y2: Y(60)}, grid));
    [20, 40, 60].forEach(d => API.mk('line', {x1: X(0), y1: Y(d), x2: X(45), y2: Y(d)}, grid));
    API.arrow(svg, X(0), Y(0), X(45) + 22, Y(0), API.COL.muted, 2.5);
    API.arrow(svg, X(0), Y(0), X(0), Y(60) - 26, API.COL.muted, 2.5);
    [0, 10, 20, 30, 40].forEach(t => API.texText(svg, X(t), Y(0) + 26, String(t), {size: 18, anchor: 'middle'}));
    [20, 40, 60].forEach(d => API.texText(svg, X(0) - 10, Y(d) + 6, String(d), {size: 18, anchor: 'end'}));
    API.texText(svg, X(45) + 20, Y(0) - 12, '$t$ [s]', {size: 18, anchor: 'end', mix: true});
    API.texText(svg, X(0) + 12, Y(60) - 12, '거리 [m]', {size: 18, mix: true});
    M.forEach((m, i) => { API.mk('line', {x1: 330, y1: 30 + 26 * i, x2: 360, y2: 30 + 26 * i, stroke: m[2], 'stroke-width': 4}, svg); API.texText(svg, 368, 36 + 26 * i, m[0], {size: 18, mix: true}); });
    const plot = API.mk('g', {}, svg);
    let mode = 1, rec = [], seed = 11;
    const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    function draw(){
      root.querySelectorAll('[data-act^="w"]').forEach((b, i) => b.classList.toggle('on', i === mode));
      O('d').textContent = I('d').value + ' m';
      plot.textContent = '';
      rec.forEach(r => {
        const t = Math.min(r.t, 45), d = r.d * t / r.t;
        API.mk('line', {x1: X(0), y1: Y(0), x2: X(t), y2: Y(d), stroke: M[r.m][2], 'stroke-width': 3, 'stroke-linecap': 'round'}, plot);
        if (r.t <= 45) API.mk('circle', {cx: X(r.t), cy: Y(r.d), r: 6, fill: M[r.m][2]}, plot);
      });
      O('rows').innerHTML = rec.slice(-6).map((r, i) => `<tr><td>${rec.length - Math.min(6, rec.length) + i + 1}</td><td>${M[r.m][0]}</td><td>${r.d.toFixed(1)}</td><td>${r.t.toFixed(1)}</td><td>${(r.d / r.t).toFixed(1)}</td></tr>`).join('');
    }
    root.querySelectorAll('[data-act^="w"]').forEach((b, i) => b.addEventListener('click', () => { mode = i; draw(); }));
    I('d').addEventListener('input', draw);
    $('[data-act="measure"]').addEventListener('click', () => {
      const D = +I('d').value, d = D + 0.4 * (rnd() - 0.5), t = D / M[mode][1] + 0.3 * (rnd() - 0.5);
      rec.push({m: mode, d, t}); draw();
      const avg = M.map((m, i) => { const r = rec.filter(x => x.m === i); return r.length ? r.reduce((a, x) => a + x.d / x.t, 0) / r.length : null; });
      const have = avg.map((v, i) => [v, i]).filter(x => x[0] !== null).sort((a, b) => b[0] - a[0]);
      O('msg').textContent = have.length > 1
        ? `평균 속력: ${have.map(x => `${M[x[1]][0]} ${x[0].toFixed(1)} m/s`).join(', ')} → ${M[have[0][1]][0]}가 가장 빠르다(그래프 기울기가 가장 크다).`
        : `${M[mode][0]}: ${d.toFixed(1)} m ÷ ${t.toFixed(1)} s = ${(d / t).toFixed(1)} m/s. 다른 이동 방법도 측정해 비교해 보자.`;
    });
    $('[data-act="reset"]').addEventListener('click', () => { rec = []; seed = 11; mode = 1; I('d').value = 45; O('msg').textContent = ''; draw(); });
    draw();
  }
};
