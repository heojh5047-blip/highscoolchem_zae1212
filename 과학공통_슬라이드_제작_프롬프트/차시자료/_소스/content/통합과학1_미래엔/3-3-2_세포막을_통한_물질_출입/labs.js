/* 3-3-2 세포막을 통한 물질 출입 — 실험실 (덱 접두어 is1332) */
window.DECK_LABS = {
  /* 삼투 관찰: 세포(양파 표피세포·적혈구·껍데기 없는 달걀) × 용액(증류수·같은 농도·10 % 소금물)을 고르고 담가 두면
     물 분자의 이동 방향과 세포 모양 변화가 애니메이션으로 나온다. 결과는 교과서 151–153쪽과 지도서 예시 답 */
  is1332osm(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const CN = {onion: '양파 표피세포', rbc: '적혈구', egg: '달걀'}, SN = ['증류수', '같은 농도', '10 % 소금물'];
    const RES = {
      onion: ['물이 들어와 부피가 커진다(세포벽 때문에 터지지 않음)', '변화 없음', '물이 빠져나가 세포막이 세포벽에서 분리된다'],
      rbc: ['물이 들어와 부풀다가 터진다(세포벽 없음)', '변화 없음', '물이 빠져나가 쭈그러든다'],
      egg: ['물이 들어와 질량이 증가한다', '거의 변화 없음', '물이 빠져나가 질량이 감소한다']};
    let c = null, s = -1, rec = {}, stopA = null;
    const g = API.mk('g', {}, svg), tab = API.mk('g', {}, svg);
    function cellShape(k){   // k: −1(수축) … 0 … +1(팽창), burst when rbc & k>=1
      g.innerHTML = '';
      const sol = s < 0 ? '#FFFFFF' : ['#EEF6FC', '#F3F7FA', '#E8E0F7'][s];
      API.mk('rect', {x: 10, y: 10, width: 540, height: 250, rx: 14, fill: sol, stroke: '#C9D3DD', 'stroke-width': 2}, g);
      if (s >= 0) for (let i = 0; i < [0, 8, 22][s]; i++) API.mk('circle', {cx: 30 + (i * 73) % 500, cy: 30 + (i * 41) % 210, r: 4, fill: '#7B4FC8', opacity: .6}, g);
      if (!c) { T(g, 280, 140, '세포를 고르자', {size: 19, anchor: 'middle', fill: API.COL.muted}); return; }
      const cx = 280, cy = 135;
      if (c === 'onion') {
        API.mk('rect', {x: cx - 120, y: cy - 80, width: 240, height: 160, rx: 6, fill: '#FFFFFF', stroke: API.COL.field, 'stroke-width': 7}, g);
        const sx = k < 0 ? 1 + 0.45 * k : 1, sy = k < 0 ? 1 + 0.45 * k : 1;
        API.mk('rect', {x: cx - 112 * sx, y: cy - 72 * sy, width: 224 * sx, height: 144 * sy, rx: k < 0 ? 40 : 4, fill: '#C04878', stroke: API.COL.plus, 'stroke-width': 2}, g);
        T(g, cx + 128, cy - 84, '세포벽', {size: 16}); 
      } else if (c === 'rbc') {
        if (k >= 1) { API.mk('circle', {cx, cy, r: 92, fill: '#F6C0C6', stroke: API.COL.plus, 'stroke-width': 3, 'stroke-dasharray': '14 10'}, g); T(g, cx, cy + 8, '터짐!', {size: 22, anchor: 'middle', fill: API.COL.plus, weight: 700}); }
        else { const r = 70 * (1 + 0.3 * k); API.mk('ellipse', {cx, cy, rx: r, ry: k < 0 ? r * 0.7 : r * 0.8, fill: '#F08A97', stroke: API.COL.plus, 'stroke-width': 3, 'stroke-dasharray': k < -0.5 ? '6 6' : null}, g); API.mk('ellipse', {cx, cy, rx: r * 0.4, ry: r * 0.3, fill: '#E05A6E'}, g); }
      } else {
        const r = 80 * (1 + 0.12 * k);
        API.mk('ellipse', {cx, cy, rx: r * 0.8, ry: r, fill: '#FDF6E3', stroke: '#C9B48A', 'stroke-width': 3}, g);
        API.mk('circle', {cx, cy: cy + 10, r: r * 0.35, fill: '#F7C548'}, g);
      }
    }
    function arrows(dir, t){   // dir +1 in, −1 out
      if (!dir) return;
      for (let i = 0; i < 6; i++) {
        const a = i / 6 * Math.PI * 2, R0 = 150, R1 = 105, f = (t * 0.8 + i / 6) % 1;
        const R = dir > 0 ? R0 - (R0 - R1) * f : R1 + (R0 - R1) * f;
        API.mk('circle', {cx: 280 + R * Math.cos(a) * 1.4, cy: 135 + R * Math.sin(a) * 0.8, r: 6, fill: API.COL.minus}, g);
      }
      T(g, 280, 252, dir > 0 ? '물: 세포 밖 → 안' : '물: 세포 안 → 밖', {size: 17, anchor: 'middle', fill: API.COL.minus, weight: 700});
    }
    function drawTab(){
      tab.innerHTML = '';
      API.mk('rect', {x: 10, y: 272, width: 540, height: 164, rx: 10, fill: '#F6F9FC', stroke: '#C9D3DD', 'stroke-width': 2}, tab);
      T(tab, 24, 298, '세포', {size: 16, weight: 700}); SN.forEach((n, i) => T(tab, 200 + i * 120, 298, n, {size: 16, anchor: 'middle', weight: 700}));
      ['onion', 'rbc', 'egg'].forEach((k, j) => {
        const y = 330 + j * 32; T(tab, 24, y, CN[k], {size: 16});
        [0, 1, 2].forEach(i => { const v = rec[k + i]; if (v) T(tab, 200 + i * 120, y, v, {size: 16, anchor: 'middle', fill: v === '그대로' ? API.COL.muted : API.COL.ink}); });
      });
    }
    const SHORT = {onion: ['커짐', '그대로', '원형질 분리'], rbc: ['터짐', '그대로', '쭈그러듦'], egg: ['질량↑', '그대로', '질량↓']};
    function sync(){ O('cell').querySelectorAll('[data-c]').forEach(b => b.classList.toggle('on', b.dataset.c === c)); O('sol').querySelectorAll('[data-s]').forEach(b => b.classList.toggle('on', +b.dataset.s === s)); }
    const stop = () => { if (stopA) { stopA(); stopA = null; } };
    O('cell').querySelectorAll('[data-c]').forEach(b => b.addEventListener('click', () => { c = b.dataset.c; stop(); sync(); cellShape(0); O('msg').textContent = ''; }));
    O('sol').querySelectorAll('[data-s]').forEach(b => b.addEventListener('click', () => { s = +b.dataset.s; stop(); sync(); cellShape(0); O('msg').textContent = ''; }));
    $('[data-act="go"]').addEventListener('click', () => {
      if (!c || s < 0) { O('msg').textContent = '세포와 용액을 모두 고르자.'; return; }
      stop(); const dir = s === 0 ? 1 : s === 2 ? -1 : 0; let t = 0;
      stopA = API.loop(root, dt => { t += dt; const k = Math.min(1, t / 2.5) * dir; cellShape(k); arrows(dir, t); if (t > 2.5 && !rec[c + s]) { rec[c + s] = SHORT[c][s]; drawTab(); O('msg').textContent = `${CN[c]} + ${SN[s]}: ${RES[c][s]}.`; } if (t > 6) { stop(); } });
    });
    $('[data-act="sum"]').addEventListener('click', () => {
      const n = Object.keys(rec).length;
      if (!(rec.onion0 && rec.onion2)) { O('msg').textContent = '먼저 양파 표피세포를 증류수와 10 % 소금물에 각각 담가 보자.'; return; }
      let m = '양파 표피세포: 증류수에서는 물이 들어오고(밖 → 안), 10 % 소금물에서는 물이 빠져나가 세포막이 세포벽에서 분리된다(안 → 밖).';
      if (rec.rbc0) m += ' 적혈구는 증류수에서 세포벽이 없어 터진다.'; else m += ' 적혈구도 증류수에 넣어 비교해 보자.';
      m += ' → 세포막은 물질의 출입을 조절해 생명활동을 유지한다(같은 농도 용액에서는 변화 없음).';
      O('msg').textContent = m;
    });
    $('[data-act="reset"]').addEventListener('click', () => { stop(); c = null; s = -1; rec = {}; O('msg').textContent = ''; sync(); cellShape(0); drawTab(); });
    cellShape(0); drawTab();
  }
};
