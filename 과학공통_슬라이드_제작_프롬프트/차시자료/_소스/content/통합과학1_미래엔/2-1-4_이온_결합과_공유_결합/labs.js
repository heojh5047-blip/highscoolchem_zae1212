/* 2-1-4 이온 결합과 공유 결합 — 실험실 (덱 접두어 is1214) */
window.DECK_LABS = {
  /* 전기 전도성 비교: 물질 4가지 × 상태(고체·액체 / 수용액)를 골라 측정기를 대면 전구와 입자 모습이 나오고 표에 ◯×가 기록된다 (교과서 72쪽 탐구) */
  is1214cond(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const SUB = ['증류수', '설탕', '황산 구리(Ⅱ)', '염화 나트륨'];
    const IONIC = [false, false, true, true];
    const LIQ = [true, false, false, false];          // 증류수는 처음부터 액체, 수용액 칸 없음
    let s = -1, t = -1, rec = {}, stopA = null;
    const scene = API.mk('g', {}, svg), table = API.mk('g', {}, svg);
    const flows = (si, ti) => IONIC[si] && ti === 1;
    function drawTable(){
      table.innerHTML = '';
      const X = [20, 230, 360, 470], Y0 = 290;
      API.mk('rect', {x: 10, y: Y0 - 26, width: 540, height: 168, rx: 10, fill: '#F6F9FC', stroke: '#C9D3DD', 'stroke-width': 2}, table);
      ['물질', '고체(액체)', '수용액'].forEach((h, i) => T(table, X[i], Y0, h, {size: 18, weight: 700}));
      SUB.forEach((n, i) => {
        const y = Y0 + 28 + i * 28;
        T(table, X[0], y, '가나다라'[i] + ' ' + n, {size: 18});
        [0, 1].forEach(k => {
          const key = i + ',' + k;
          if (k === 1 && LIQ[i]) { T(table, X[1 + k] + 30, y, '—', {size: 18, anchor: 'middle', fill: API.COL.muted}); return; }
          if (key in rec) T(table, X[1 + k] + 30, y, rec[key] ? '◯' : '×', {size: 20, anchor: 'middle', fill: rec[key] ? API.COL.plus : API.COL.muted, weight: 700});
        });
      });
    }
    const ions = [], mols = [];
    function build(){
      scene.innerHTML = ''; ions.length = 0; mols.length = 0;
      // 측정기와 홈
      API.mk('rect', {x: 200, y: 14, width: 160, height: 54, rx: 10, fill: '#16233D'}, scene);
      const bulb = API.mk('circle', {cx: 280, cy: 41, r: 16, fill: '#5B6B7F', stroke: '#F7C548', 'stroke-width': 0}, scene); bulb.dataset.k = 'bulb';
      API.mk('line', {x1: 230, y1: 68, x2: 230, y2: 200, stroke: '#8C99A6', 'stroke-width': 6}, scene);
      API.mk('line', {x1: 330, y1: 68, x2: 330, y2: 200, stroke: '#8C99A6', 'stroke-width': 6}, scene);
      T(scene, 222, 92, '(−)', {size: 17, anchor: 'end'}); T(scene, 338, 92, '(+)', {size: 17});
      const sol = s >= 0 && (t === 1 || LIQ[s]);
      API.mk('path', {d: 'M140 110 L140 225 Q140 245 160 245 L400 245 Q420 245 420 225 L420 110', fill: sol ? (s === 2 ? '#CFE6FA' : '#EEF4F8') : '#FFFFFF', stroke: API.COL.muted, 'stroke-width': 3}, scene);
      if (s < 0 || t < 0 && !LIQ[s]) { T(scene, 280, 190, s < 0 ? '물질을 고르자' : '상태를 고르자', {size: 19, anchor: 'middle', fill: API.COL.muted}); return; }
      if (s === 0) { T(scene, 280, 236, '물 분자만(이온 없음)', {size: 16, anchor: 'middle', fill: API.COL.muted}); for (let i = 0; i < 6; i++) mols.push(API.mk('circle', {cx: 170 + i * 40, cy: 150 + (i % 2) * 40, r: 8, fill: '#C9D3DD'}, scene)); return; }
      if (!sol) {   // 고체: 격자 또는 분자 결정 (가만히)
        for (let j = 0; j < 3; j++) for (let i = 0; i < 6; i++) {
          const x = 180 + i * 34, y = 160 + j * 26;
          if (IONIC[s]) API.mk('circle', {cx: x, cy: y, r: (i + j) % 2 ? 12 : 8, fill: (i + j) % 2 ? '#7FB3E6' : '#F08A97', stroke: (i + j) % 2 ? API.COL.minus : API.COL.plus}, scene);
          else API.mk('rect', {x: x - 12, y: y - 9, width: 24, height: 18, rx: 6, fill: '#E9E2D0', stroke: API.COL.grav}, scene);
        }
        T(scene, 280, 236, IONIC[s] ? '고체: 이온이 고정되어 움직이지 못함' : '고체: 분자로 이루어짐', {size: 16, anchor: 'middle', fill: API.COL.muted});
        return;
      }
      for (let i = 0; i < 6; i++) {
        const y = 122 + (i % 3) * 28 + (i > 2 ? 14 : 0), x = 165 + ((i * 97) % 230);
        if (IONIC[s]) {
          ions.push({el: API.mk('circle', {cx: x, cy: y, r: 8, fill: s === 2 ? '#5DA9E9' : '#F08A97', stroke: API.COL.plus}, scene), x, y, q: 1});
          ions.push({el: API.mk('circle', {cx: 400 - (x - 160), cy: y + 12, r: 12, fill: s === 2 ? '#E9D78A' : '#7FB3E6', stroke: API.COL.minus}, scene), x: 400 - (x - 160), y: y + 12, q: -1});
        } else mols.push(API.mk('rect', {x: x - 12, y: y - 9, width: 24, height: 18, rx: 6, fill: '#E9E2D0', stroke: API.COL.grav}, scene));
      }
      T(scene, 280, 236, IONIC[s] ? '수용액: 양이온 → (−)극, 음이온 → (+)극' : '수용액: 분자 그대로(이온 없음)', {size: 16, anchor: 'middle', fill: IONIC[s] ? API.COL.plus : API.COL.muted});
    }
    function run(){
      if (stopA) { stopA(); stopA = null; }
      build();
      const on = flows(s, LIQ[s] ? 0 : t);
      const bulb = scene.querySelector('[data-k="bulb"]');
      bulb.setAttribute('fill', on ? '#F7C548' : '#5B6B7F'); bulb.setAttribute('stroke-width', on ? 6 : 0);
      let k = 0;
      stopA = API.loop(root, dt => {
        k += dt;
        ions.forEach(p => { if (!on) return; p.x += (p.q > 0 ? -1 : 1) * dt * 40; if (p.x < 160) p.x = 400; if (p.x > 400) p.x = 160; p.el.setAttribute('cx', p.x.toFixed(1)); });
        mols.forEach((m, i) => m.setAttribute('transform', `translate(${(Math.sin(k * 2 + i) * 4).toFixed(1)},${(Math.cos(k * 2.3 + i) * 4).toFixed(1)})`));
        if (on) bulb.setAttribute('opacity', (0.75 + 0.25 * Math.sin(k * 10)).toFixed(2));
      });
      return on;
    }
    function sync(){
      O('sub').querySelectorAll('[data-s]').forEach(b => b.classList.toggle('on', +b.dataset.s === s));
      O('st').querySelectorAll('[data-t]').forEach(b => { b.classList.toggle('on', +b.dataset.t === t); b.disabled = s >= 0 && LIQ[s] && +b.dataset.t === 1; });
    }
    O('sub').querySelectorAll('[data-s]').forEach(b => b.addEventListener('click', () => { s = +b.dataset.s; if (LIQ[s]) t = 0; sync(); if (stopA) { stopA(); stopA = null; } build(); O('msg').textContent = ''; }));
    O('st').querySelectorAll('[data-t]').forEach(b => b.addEventListener('click', () => { t = +b.dataset.t; sync(); if (stopA) { stopA(); stopA = null; } build(); O('msg').textContent = ''; }));
    $('[data-act="run"]').addEventListener('click', () => {
      if (s < 0 || t < 0) { O('msg').textContent = '물질과 상태를 먼저 고르자.'; return; }
      const on = run(), tt = LIQ[s] ? 0 : t; rec[s + ',' + tt] = on; drawTable();
      O('msg').textContent = `${SUB[s]} ${LIQ[s] ? '(액체)' : tt ? '수용액' : '고체'}: ${on ? '불이 켜짐 → 전류가 흐른다 ◯' : '불이 켜지지 않음 → 전류가 흐르지 않는다 ×'}`;
    });
    $('[data-act="sum"]').addEventListener('click', () => {
      const need = 7, have = Object.keys(rec).length;
      if (have < need) { O('msg').textContent = `아직 ${need - have}칸이 비었다. 모든 물질의 고체와 수용액을 측정해 표를 채우자.`; return; }
      O('msg').textContent = '황산 구리(Ⅱ)·염화 나트륨(금속+비금속, 이온 결합 물질): 고체 ×, 수용액 ◯ / 증류수·설탕(비금속, 공유 결합 물질): 모두 × → 이온 결합 물질만 수용액에서 이온이 이동해 전류가 흐른다.';
    });
    $('[data-act="reset"]').addEventListener('click', () => { if (stopA) { stopA(); stopA = null; } s = -1; t = -1; rec = {}; O('msg').textContent = ''; sync(); build(); drawTable(); });
    sync(); build(); drawTable();
  }
};
