/* 2-2-1 지각과 생명체를 구성하는 물질 — 실험실 (덱 접두어 is1221) */
window.DECK_LABS = {
  /* DNA 모형: 왼쪽·오른쪽 염기를 골라 염기쌍을 연결(A–T, G–C만 끼워짐)하고, 꼬아서 이중나선을 보고, 염기 수 규칙과 다른 모둠 배열을 비교한다 (교과서 86–87쪽 탐구) */
  is1221dna(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const COLB = {A: '#F7C548', T: '#E08A2C', G: '#8BD3A7', C: '#7FB3E6'}, PAIR = {A: 'T', T: 'A', G: 'C', C: 'G'};
    const NAME = {A: '아데닌', T: '타이민', G: '구아닌', C: '사이토신'};
    const MAX = 10;
    let L = '', R = '', pairs = [], twist = false, ph = 0, stopA = null;
    const g = API.mk('g', {}, svg), side = API.mk('g', {}, svg);
    function draw(){
      g.innerHTML = '';
      const cx = 170, hw0 = 105, top = 40, dy = 36;
      const X = (i, s) => { const a = twist ? Math.cos(i * 0.62 + ph) : 1; return cx + s * hw0 * a; };
      if (!pairs.length) { T(g, cx, 200, '염기쌍을 연결해 보자', {size: 19, anchor: 'middle', fill: API.COL.muted}); }
      // 뼈대(당–인산)
      [-1, 1].forEach(s => {
        const pts = pairs.map((p, i) => `${X(i, s).toFixed(1)},${top + i * dy}`).join(' ');
        if (pairs.length > 1) API.mk('polyline', {points: pts, fill: 'none', stroke: '#8C99A6', 'stroke-width': 3}, g);
      });
      // 앞뒤 구분: 꼬았을 때 cos가 음수이면 뒤쪽(흐리게)
      pairs.forEach((p, i) => {
        const y = top + i * dy, xl = X(i, -1), xr = X(i, 1), mid = (xl + xr) / 2;
        const back = twist && Math.cos(i * 0.62 + ph) < 0, op = back ? .45 : 1;
        API.mk('line', {x1: xl, y1: y, x2: mid, y2: y, stroke: COLB[p[0]], 'stroke-width': 12, opacity: op}, g);
        API.mk('line', {x1: mid, y1: y, x2: xr, y2: y, stroke: COLB[p[1]], 'stroke-width': 12, opacity: op}, g);
        if (Math.abs(xr - xl) > 40) { T(g, (xl + mid) / 2, y + 6, p[0], {size: 16, anchor: 'middle', weight: 700}); T(g, (mid + xr) / 2, y + 6, p[1], {size: 16, anchor: 'middle', weight: 700}); }
        [[xl, 1], [xr, -1]].forEach(([x, k]) => {
          API.mk('path', {d: `M${x - 9} ${y - 3} L${x} ${y - 10} L${x + 9} ${y - 3} L${x + 6} ${y + 8} L${x - 6} ${y + 8} Z`, fill: '#C4B5FD', stroke: API.COL.bfield, 'stroke-width': 1.5}, g);
          if (i < pairs.length - 1) API.mk('circle', {cx: (x + X(i + 1, k > 0 ? -1 : 1)) / 2, cy: y + dy / 2, r: 6, fill: '#F08A97', stroke: API.COL.plus, 'stroke-width': 1.5}, g);
        });
      });
      if (pairs.length && !twist) {
        API.mk('line', {x1: 40, y1: top, x2: 40, y2: top + Math.max(1, pairs.length - 1) * dy, stroke: API.COL.muted, 'stroke-width': 2, 'marker-end': ''}, g);
        T(g, 30, top - 14, '당–인산 ↓', {size: 15, anchor: 'start', fill: API.COL.muted});
        T(g, 310, top + Math.max(1, pairs.length - 1) * dy + 26, '↑ 인산–당(반대 방향)', {size: 15, anchor: 'end', fill: API.COL.muted});
      }
      drawSide();
    }
    function drawSide(){
      side.innerHTML = '';
      const x = 345;
      API.mk('rect', {x: x - 10, y: 20, width: 220, height: 230, rx: 10, fill: '#F6F9FC', stroke: '#C9D3DD', 'stroke-width': 2}, side);
      T(side, x, 46, '염기 수', {size: 18, weight: 700});
      const cnt = {A: 0, T: 0, G: 0, C: 0}; pairs.forEach(p => { cnt[p[0]]++; cnt[p[1]]++; });
      ['A', 'T', 'G', 'C'].forEach((b, i) => {
        const y = 78 + i * 34;
        API.mk('rect', {x, y: y - 16, width: 22, height: 20, rx: 4, fill: COLB[b]}, side);
        T(side, x + 30, y, `${b} ${NAME[b]}`, {size: 17});
        T(side, x + 200, y, String(cnt[b]), {size: 19, anchor: 'end', weight: 700});
      });
      T(side, x, 228, `염기쌍 ${pairs.length} / ${MAX}`, {size: 17, fill: API.COL.muted});
      API.mk('rect', {x: x - 10, y: 270, width: 220, height: 150, rx: 10, fill: '#FFFFFF', stroke: '#C9D3DD', 'stroke-width': 2}, side);
      T(side, x, 296, '배열 순서(왼쪽 가닥)', {size: 17, weight: 700});
      T(side, x, 326, pairs.map(p => p[0]).join('') || '—', {size: 19});
      T(side, x, 356, '마주 보는 가닥', {size: 17, weight: 700});
      T(side, x, 386, pairs.map(p => p[1]).join('') || '—', {size: 19});
    }
    function sync(){
      O('lb').querySelectorAll('[data-l]').forEach(b => b.classList.toggle('on', b.dataset.l === L));
      O('rb').querySelectorAll('[data-r]').forEach(b => b.classList.toggle('on', b.dataset.r === R));
      $('[data-act="twist"]').classList.toggle('on', twist);
    }
    O('lb').querySelectorAll('[data-l]').forEach(b => b.addEventListener('click', () => { L = b.dataset.l; sync(); }));
    O('rb').querySelectorAll('[data-r]').forEach(b => b.addEventListener('click', () => { R = b.dataset.r; sync(); }));
    $('[data-act="add"]').addEventListener('click', () => {
      if (!L || !R) { O('msg').textContent = '왼쪽과 오른쪽 염기를 하나씩 고르자.'; return; }
      if (pairs.length >= MAX) { O('msg').textContent = `염기쌍은 ${MAX}개까지 연결할 수 있다.`; return; }
      if (PAIR[L] !== R) { O('msg').textContent = `${L}(${NAME[L]})와 ${R}(${NAME[R]})는 홈이 맞지 않아 끼워지지 않는다. ${L}의 짝을 찾아보자.`; return; }
      pairs.push([L, R]); O('msg').textContent = `${L}–${R} 염기쌍을 연결했다. (당과 인산을 테이프로 붙임)`; L = R = ''; sync(); draw();
    });
    $('[data-act="twist"]').addEventListener('click', () => {
      twist = !twist; sync();
      if (stopA) { stopA(); stopA = null; }
      if (twist) stopA = API.loop(root, dt => { ph += dt * 1.2; draw(); }); else { ph = 0; draw(); }
      O('msg').textContent = twist ? '두 가닥이 꼬인 이중나선구조 — 뼈대(당–인산)는 바깥, 염기쌍은 안쪽' : '';
    });
    $('[data-act="sum"]').addEventListener('click', () => {
      if (pairs.length < 4) { O('msg').textContent = '염기쌍을 4개 이상 연결한 뒤 규칙을 찾아보자.'; return; }
      const c = {A: 0, T: 0, G: 0, C: 0}; pairs.forEach(p => { c[p[0]]++; c[p[1]]++; });
      O('msg').textContent = `A ${c.A}개 = T ${c.T}개, G ${c.G}개 = C ${c.C}개 → A는 항상 T와, G는 항상 C와 결합한다. 뉴클레오타이드의 인산이 다음 뉴클레오타이드의 당과 결합하는 방식이 반복된다.`;
    });
    $('[data-act="cmp"]').addEventListener('click', () => {
      if (pairs.length < 4) { O('msg').textContent = '염기쌍을 4개 이상 연결한 뒤 비교해 보자.'; return; }
      let seed = 7 + pairs.length, other = '';
      for (let i = 0; i < pairs.length; i++) { seed = (seed * 37 + 11) % 101; other += 'ATGC'[seed % 4]; }
      const mine = pairs.map(p => p[0]).join('');
      O('msg').textContent = `우리 모둠 ${mine} · 다른 모둠 ${other} → ${mine === other ? '우연히 같다!' : '염기 배열 순서가 다르다'} → 배열 순서에 따라 서로 다른 유전정보를 담는다.`;
    });
    $('[data-act="reset"]').addEventListener('click', () => { if (stopA) { stopA(); stopA = null; } L = R = ''; pairs = []; twist = false; ph = 0; O('msg').textContent = ''; sync(); draw(); });
    sync(); draw();
  }
};
