/* 3-3-3 세포 내 정보의 흐름 — 실험실 (덱 접두어 is1333) */
window.DECK_LABS = {
  /* 주사위 전사·번역: 주사위를 던져 3염기조합(교과서 158쪽 표)을 DNA 가닥에 이어 붙이고, 전사로 코돈, 번역으로 아미노산 모형 사슬을 만든다.
     주사위 값은 고정된 순서의 의사 난수(수업 재현용). 아미노산 모형 모양은 덱이 정함 */
  is1333dice(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400, 'font-family': o.mono ? 'monospace' : null}, par); t.textContent = str; return t; };
    const TRI = ['AGC', 'ACG', 'GTA', 'GAC', 'CCA', 'TAC'];
    const PAIR = {A: 'U', G: 'C', C: 'G', T: 'A'};
    const SHAPE = ['circle', 'square', 'tri', 'diamond', 'hex', 'star'];
    const COLS = ['#F08A97', '#7FB3E6', '#F7C548', '#8BD3A7', '#C4B5FD', '#E08A2C'];
    const MAX = 6;
    let seq = [], txd = false, tld = false, seed = 5;
    const g = API.mk('g', {}, svg);
    const roll = () => { seed = (seed * 13 + 7) % 17; return seed % 6; };
    function shape(par, k, x, y, r){
      const c = COLS[k], st = {fill: c, stroke: '#16233D', 'stroke-width': 1.5};
      if (SHAPE[k] === 'circle') API.mk('circle', Object.assign({cx: x, cy: y, r}, st), par);
      else if (SHAPE[k] === 'square') API.mk('rect', Object.assign({x: x - r, y: y - r, width: 2 * r, height: 2 * r}, st), par);
      else if (SHAPE[k] === 'tri') API.mk('path', Object.assign({d: `M${x} ${y - r} L${x + r} ${y + r} L${x - r} ${y + r} Z`}, st), par);
      else if (SHAPE[k] === 'diamond') API.mk('path', Object.assign({d: `M${x} ${y - r} L${x + r} ${y} L${x} ${y + r} L${x - r} ${y} Z`}, st), par);
      else if (SHAPE[k] === 'hex') API.mk('path', Object.assign({d: `M${x - r} ${y} L${x - r / 2} ${y - r} L${x + r / 2} ${y - r} L${x + r} ${y} L${x + r / 2} ${y + r} L${x - r / 2} ${y + r} Z`}, st), par);
      else API.mk('path', Object.assign({d: `M${x} ${y - r} L${x + r * .3} ${y - r * .3} L${x + r} ${y - r * .2} L${x + r * .45} ${y + r * .3} L${x + r * .6} ${y + r} L${x} ${y + r * .6} L${x - r * .6} ${y + r} L${x - r * .45} ${y + r * .3} L${x - r} ${y - r * .2} L${x - r * .3} ${y - r * .3} Z`}, st), par);
    }
    function draw(){
      g.innerHTML = '';
      // 표(주사위 · 3염기조합 · 코돈 · 모형)
      API.mk('rect', {x: 10, y: 10, width: 540, height: 120, rx: 10, fill: '#F6F9FC', stroke: '#C9D3DD', 'stroke-width': 2}, g);
      TRI.forEach((t, k) => {
        const x = 40 + k * 88;
        T(g, x, 36, String(k + 1), {size: 18, anchor: 'middle', weight: 700});
        T(g, x, 62, t, {size: 17, anchor: 'middle', mono: true});
        T(g, x, 88, t.split('').map(b => PAIR[b]).join(''), {size: 17, anchor: 'middle', mono: true, fill: API.COL.field});
        shape(g, k, x, 112, 9);
      });
      const L = ['DNA 가닥', 'RNA', '단백질'];
      L.forEach((l, i) => T(g, 20, 178 + i * 90, l, {size: 17, weight: 700}));
      seq.forEach((k, j) => {
        const x = 150 + j * 66;
        API.mk('rect', {x: x - 30, y: 156, width: 60, height: 34, rx: 6, fill: '#F1ECFB', stroke: API.COL.bfield}, g);
        T(g, x, 180, TRI[k], {size: 18, anchor: 'middle', mono: true});
        if (txd) { API.mk('rect', {x: x - 30, y: 246, width: 60, height: 34, rx: 6, fill: '#E8F5EE', stroke: API.COL.field}, g); T(g, x, 270, TRI[k].split('').map(b => PAIR[b]).join(''), {size: 18, anchor: 'middle', mono: true}); }
        if (tld) { if (j) API.mk('line', {x1: x - 50, y1: 350, x2: x - 16, y2: 350, stroke: '#16233D', 'stroke-width': 3}, g); shape(g, k, x, 350, 16); }
      });
      T(g, 20, 420, `염기쌍 규칙: A→U, G→C, C→G, T→A · 코돈 1개 = 아미노산 1개`, {size: 16, fill: API.COL.muted});
    }
    $('[data-act="roll"]').addEventListener('click', () => {
      if (seq.length >= MAX) { O('msg').textContent = `DNA 가닥은 ${MAX}칸까지 채울 수 있다.`; return; }
      const k = roll(); seq.push(k); txd = tld = false; draw();
      O('msg').textContent = `주사위 ${k + 1} → 3염기조합 ${TRI[k]}를 DNA 가닥에 이어 붙였다.`;
    });
    $('[data-act="undo"]').addEventListener('click', () => { seq.pop(); txd = tld = false; draw(); O('msg').textContent = ''; });
    $('[data-act="tx"]').addEventListener('click', () => {
      if (seq.length < 2) { O('msg').textContent = '주사위를 2번 이상 던져 DNA 가닥을 만들자.'; return; }
      txd = true; draw(); O('msg').textContent = `전사: ${seq.map(k => TRI[k]).join(' ')} → ${seq.map(k => TRI[k].split('').map(b => PAIR[b]).join('')).join(' ')} (T 대신 U)`;
    });
    $('[data-act="tl"]').addEventListener('click', () => {
      if (!txd) { O('msg').textContent = '번역하려면 먼저 전사로 RNA를 만들어야 한다.'; return; }
      tld = true; draw(); O('msg').textContent = `번역: 코돈 ${seq.length}개 → 아미노산 ${seq.length}개가 차례로 연결된 단백질(모형).`;
    });
    $('[data-act="other"]').addEventListener('click', () => {
      if (!tld) { O('msg').textContent = '번역까지 마친 뒤 비교해 보자.'; return; }
      let s2 = 11, o = []; for (let i = 0; i < seq.length; i++) { s2 = (s2 * 7 + 3) % 19; o.push(s2 % 6); }
      const same = o.join() === seq.join();
      O('msg').textContent = `다른 모둠 DNA: ${o.map(k => TRI[k]).join(' ')} → ${same ? '우연히 같다' : '3염기조합 순서가 달라 코돈 순서, 아미노산 배열 순서도 다르다'} → 서로 다른 단백질.`;
    });
    $('[data-act="reset"]').addEventListener('click', () => { seq = []; txd = tld = false; seed = 5; O('msg').textContent = ''; draw(); });
    draw();
  }
};
