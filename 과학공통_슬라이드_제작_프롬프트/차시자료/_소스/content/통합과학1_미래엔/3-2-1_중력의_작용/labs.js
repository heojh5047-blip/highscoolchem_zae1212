/* 3-2-1 중력의 작용 — 실험실 (덱 접두어 is1321) */
window.DECK_LABS = {
  /* 동시 낙하: 높이 1 m에서 공 A는 자유 낙하, 공 B는 수평 속력 v로 동시에 출발. 0.1 s마다 위치를 찍고(다중 섬광) 구간 거리를 표로. 중력 가속도 지구·2배·달 비교 (교과서 126–129쪽) */
  is1321proj(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), I = k => $(`[data-i="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const X0 = 70, Y0 = 30, S = 200, H = 1;        // 1 m = 200 px
    let g = 9.8, runs = {}, stopA = null;
    const bg = API.mk('g', {}, svg), dots = API.mk('g', {}, svg), tab = API.mk('g', {}, svg);
    function drawBg(){
      bg.innerHTML = '';
      for (let c = 0; c <= 2.5; c += 0.1) API.mk('line', {x1: X0 + c * S, y1: Y0, x2: X0 + c * S, y2: Y0 + H * S, stroke: '#EEF1F4', 'stroke-width': 1}, bg);
      for (let r = 0; r <= H + 0.001; r += 0.1) API.mk('line', {x1: X0, y1: Y0 + r * S, x2: 540, y2: Y0 + r * S, stroke: '#EEF1F4', 'stroke-width': 1}, bg);
      API.mk('line', {x1: X0 - 10, y1: Y0 + H * S, x2: 550, y2: Y0 + H * S, stroke: '#8C6A4F', 'stroke-width': 4}, bg);
      API.mk('rect', {x: X0 - 30, y: Y0 - 10, width: 30, height: 14, fill: API.COL.muted}, bg);
      T(bg, X0 - 34, Y0 + 6, '1 m', {size: 16, anchor: 'end'});
      T(bg, 540, Y0 + H * S + 22, '눈금 10 cm', {size: 16, anchor: 'end', fill: API.COL.muted});
    }
    function drawTab(rows){
      tab.innerHTML = '';
      API.mk('rect', {x: 0, y: 262, width: 560, height: 174, rx: 10, fill: '#F6F9FC', stroke: '#C9D3DD', 'stroke-width': 2}, tab);
      const cols = [20, 210, 300, 390, 480];
      T(tab, cols[0], 288, '구간 [s]', {size: 16, weight: 700});
      T(tab, cols[0], 316, 'A 연직 [cm]', {size: 16, fill: API.COL.plus});
      T(tab, cols[0], 344, 'B 수평 [cm]', {size: 16, fill: API.COL.minus});
      T(tab, cols[0], 372, 'B 연직 [cm]', {size: 16, fill: API.COL.minus});
      (rows || []).slice(0, 4).forEach((r, i) => {
        const x = 170 + i * 95;
        T(tab, x, 288, `${(i / 10).toFixed(1)}–${((i + 1) / 10).toFixed(1)}`, {size: 16, anchor: 'middle', weight: 700});
        T(tab, x, 316, r[0].toFixed(1), {size: 16, anchor: 'middle'}); T(tab, x, 344, r[1].toFixed(1), {size: 16, anchor: 'middle'}); T(tab, x, 372, r[0].toFixed(1), {size: 16, anchor: 'middle'});
      });
      if (rows) T(tab, 20, 410, `g = ${g} m/s² · 바닥까지 ${Math.sqrt(2 * H / g).toFixed(2)} s · B의 수평 이동 ${(+I('v').value * Math.sqrt(2 * H / g) * 100).toFixed(0)} cm`, {size: 16, fill: API.COL.muted});
    }
    function frame(t, v, all){
      dots.innerHTML = '';
      const tl = Math.sqrt(2 * H / g);
      const ts = []; for (let k = 0; k * 0.1 <= Math.min(t, tl) + 1e-9; k++) ts.push(k * 0.1);
      const tt = Math.min(t, tl);
      ts.forEach((s, i) => {
        const y = Y0 + 0.5 * g * s * s * S;
        API.mk('circle', {cx: X0, cy: y, r: 7, fill: API.COL.plus, opacity: .45}, dots);
        API.mk('circle', {cx: X0 + v * s * S, cy: y, r: 7, fill: API.COL.minus, opacity: .45}, dots);
        API.mk('line', {x1: X0, y1: y, x2: X0 + v * s * S, y2: y, stroke: '#8C99A6', 'stroke-dasharray': '4 4'}, dots);
      });
      const y = Y0 + 0.5 * g * tt * tt * S;
      API.mk('circle', {cx: X0, cy: y, r: 9, fill: API.COL.plus}, dots); API.mk('circle', {cx: X0 + v * tt * S, cy: y, r: 9, fill: API.COL.minus}, dots);
      T(dots, X0 + 14, Y0 - 12, 'A', {size: 16, fill: API.COL.plus}); T(dots, X0 + 30, Y0 - 12, 'B', {size: 16, fill: API.COL.minus});
    }
    function rowsFor(v){ const r = []; for (let k = 0; k < 4; k++) { const a = (t => 0.5 * g * t * t * 100); r.push([a((k + 1) / 10) - a(k / 10), v * 10]); } return r; }
    O('gsel').querySelectorAll('[data-g]').forEach(b => b.addEventListener('click', () => { g = +b.dataset.g; O('gsel').querySelectorAll('[data-g]').forEach(x => x.classList.toggle('on', x === b)); if (stopA) { stopA(); stopA = null; } dots.innerHTML = ''; drawTab(null); O('msg').textContent = ''; }));
    I('v').addEventListener('input', () => { O('v').textContent = (+I('v').value).toFixed(1); });
    $('[data-act="go"]').addEventListener('click', () => {
      if (stopA) { stopA(); stopA = null; }
      const v = +I('v').value, tl = Math.sqrt(2 * H / g); let t = 0;
      stopA = API.loop(root, dt => { t += dt / 3; frame(t, v); if (t >= tl) { stopA(); stopA = null; frame(tl, v); drawTab(rowsFor(v)); runs[g] = runs[g] || new Set(); runs[g].add(v.toFixed(1)); O('msg').textContent = `두 공이 ${tl.toFixed(2)} s에 동시에 바닥에 닿았다. 매 순간 A와 B의 높이가 같다.`; } });
    });
    $('[data-act="sum"]').addEventListener('click', () => {
      const e = runs[9.8];
      if (!e) { O('msg').textContent = '먼저 지구(9.8)에서 떨어뜨려 보자.'; return; }
      let m = 'B의 수평 구간 거리는 일정(수평 등속), A와 B의 연직 구간 거리는 같고 9.8 cm씩 늘어난다(연직 자유 낙하) → 둘 다 연직 방향으로 중력만 받아 같은 가속도로 운동한다.';
      if (e.size >= 2) m += ' 속력을 바꿔도 낙하 시간은 같고 수평 거리만 달라진다.';
      if (runs[19.6] || runs[1.6]) m += ' 중력 가속도가 클수록 더 빨리 떨어지고 수평으로 덜 간다.';
      else m += ' 「2배」와 「달」도 해 보자.';
      O('msg').textContent = m;
    });
    drawBg(); drawTab(null); frame(0, 1);
  }
};
