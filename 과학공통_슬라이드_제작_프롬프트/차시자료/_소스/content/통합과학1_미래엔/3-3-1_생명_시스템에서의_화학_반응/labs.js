/* 3-3-1 생명 시스템에서의 화학 반응 — 실험실 (덱 접두어 is1331) */
window.DECK_LABS = {
  /* 카탈레이스 실험: 홈 1–3에 기질(과산화 수소수·에탄올)과 첨가물(증류수·감자즙)을 넣으면 거품(산소) 여부와 효소–기질 결합 모습이 보인다.
     홈 2에 과산화 수소수를 더 넣으면 다시 거품 → 효소 재사용. 교과서 147쪽 탐구 */
  is1331cat(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const NS = {h2o2: '과산화 수소수', eth: '에탄올'}, NA = {water: '증류수', juice: '감자즙'};
    let W = [{s: null, a: null}, {s: null, a: null}, {s: null, a: null}], cur = -1, more = 0, bub = [], stopA = null;
    const g = API.mk('g', {}, svg), zoom = API.mk('g', {}, svg), fx = API.mk('g', {}, svg);
    const X = i => 100 + i * 180, Y = 120;
    const foams = i => W[i].s === 'h2o2' && W[i].a === 'juice';
    function draw(){
      g.innerHTML = '';
      API.mk('rect', {x: 10, y: 40, width: 540, height: 160, rx: 18, fill: '#F6F9FC', stroke: '#9FB0C2', 'stroke-width': 3}, g);
      W.forEach((w, i) => {
        const on = i === cur;
        API.mk('circle', {cx: X(i), cy: Y, r: 62, fill: w.s ? (w.a === 'juice' ? '#F3E9C8' : '#EEF4F8') : '#FFFFFF', stroke: on ? API.COL.equi : '#9FB0C2', 'stroke-width': on ? 5 : 2.5}, g);
        T(g, X(i), 28, `홈 ${i + 1}`, {size: 18, anchor: 'middle', weight: 700});
        T(g, X(i), 226, w.s ? NS[w.s] : '—', {size: 16, anchor: 'middle'});
        T(g, X(i), 248, w.a ? '+ ' + NA[w.a] : '', {size: 16, anchor: 'middle'});
        if (w.s && w.a) T(g, X(i), 274, foams(i) ? '거품 발생 ◯' : '거품 없음 ×', {size: 17, anchor: 'middle', fill: foams(i) ? API.COL.plus : API.COL.muted, weight: 700});
      });
    }
    function drawZoom(){
      zoom.innerHTML = '';
      API.mk('rect', {x: 10, y: 292, width: 540, height: 144, rx: 12, fill: '#FFFFFF', stroke: '#C9D3DD', 'stroke-width': 2}, zoom);
      T(zoom, 24, 316, '확대해 보면', {size: 16, fill: API.COL.muted});
      if (cur < 0 || !W[cur].s || !W[cur].a) { T(zoom, 280, 370, '홈을 고르고 용액을 넣어 보자', {size: 17, anchor: 'middle', fill: API.COL.muted}); return; }
      const w = W[cur];
      if (w.a === 'water') { T(zoom, 280, 370, '카탈레이스가 없다 → 과산화 수소가 거의 분해되지 않는다', {size: 17, anchor: 'middle'}); return; }
      API.mk('path', {d: 'M140 400 Q140 350 175 350 L175 372 L205 372 L205 350 Q240 350 240 400 Q240 430 190 430 Q140 430 140 400 Z', fill: '#8BD3A7', stroke: API.COL.field, 'stroke-width': 2.5}, zoom);
      T(zoom, 190, 424, '카탈레이스', {size: 15, anchor: 'middle', fill: '#1D6B47'});
      if (w.s === 'h2o2') { API.mk('rect', {x: 177, y: 336, width: 26, height: 36, rx: 4, fill: '#F7C548', stroke: '#C2410C', 'stroke-width': 2}, zoom); T(zoom, 270, 380, '모양이 맞아 결합 → 물 + 산소(거품)', {size: 17}); }
      else { API.mk('circle', {cx: 300, cy: 360, r: 16, fill: '#C4B5FD', stroke: API.COL.bfield, 'stroke-width': 2}, zoom); API.mk('path', {d: 'M222 344 l40 32 M262 344 l-40 32', stroke: API.COL.plus, 'stroke-width': 3}, zoom); T(zoom, 330, 368, '에탄올: 모양이 맞지 않아 결합 ×', {size: 17}); }
    }
    function spawn(){
      if (stopA) { stopA(); stopA = null; }
      bub = [];
      stopA = API.loop(root, dt => {
        fx.innerHTML = '';
        W.forEach((w, i) => { if (foams(i) && (i !== 1 || true)) { const rate = i === 1 && more ? 1 : 1; if (Math.random() < dt * 30 * rate) bub.push({x: X(i) - 40 + Math.random() * 80, y: Y + 40, r: 3 + Math.random() * 5, i}); } });
        bub.forEach(b => { b.y -= dt * 40; });
        bub = bub.filter(b => b.y > Y - 70);
        bub.forEach(b => API.mk('circle', {cx: b.x, cy: b.y, r: b.r, fill: '#FFFFFF', stroke: '#9FB0C2', 'stroke-width': 1.2}, fx));
      });
    }
    function sync(){ O('well').querySelectorAll('[data-w]').forEach(b => b.classList.toggle('on', +b.dataset.w === cur)); }
    O('well').querySelectorAll('[data-w]').forEach(b => b.addEventListener('click', () => { cur = +b.dataset.w; sync(); drawZoom(); O('msg').textContent = ''; }));
    O('sub').querySelectorAll('[data-s]').forEach(b => b.addEventListener('click', () => {
      if (cur < 0) { O('msg').textContent = '먼저 홈을 고르자.'; return; }
      W[cur].s = b.dataset.s; draw(); drawZoom(); O('msg').textContent = `홈 ${cur + 1}에 ${NS[b.dataset.s]} 3 mL를 넣었다.`;
    }));
    O('add').querySelectorAll('[data-a]').forEach(b => b.addEventListener('click', () => {
      if (cur < 0 || !W[cur].s) { O('msg').textContent = '홈을 고르고 먼저 과산화 수소수나 에탄올을 넣자.'; return; }
      W[cur].a = b.dataset.a; draw(); drawZoom(); spawn();
      O('msg').textContent = `홈 ${cur + 1}: ${NS[W[cur].s]} + ${NA[W[cur].a]} → ${foams(cur) ? '거품(산소)이 발생한다!' : '거품이 생기지 않는다.'}`;
    }));
    $('[data-act="more"]').addEventListener('click', () => {
      if (!foams(1)) { O('msg').textContent = '홈 2에 과산화 수소수 + 감자즙을 먼저 넣어 반응이 끝나게 하자.'; return; }
      more++; spawn(); O('msg').textContent = '감자즙을 더 넣지 않았는데도 다시 거품이 난다 → 반응 뒤 카탈레이스가 그대로 남아 재사용된다.';
    });
    $('[data-act="sum"]').addEventListener('click', () => {
      const ok = W[0].s === 'h2o2' && W[0].a === 'water' && W[1].s === 'h2o2' && W[1].a === 'juice' && W[2].s === 'eth' && W[2].a === 'juice';
      if (!ok) { O('msg').textContent = '교과서 표대로 홈 1(과산화 수소수 + 증류수), 홈 2(과산화 수소수 + 감자즙), 홈 3(에탄올 + 감자즙)을 모두 채우자.'; return; }
      O('msg').textContent = '홈 1·2 비교: 카탈레이스가 있으면 과산화 수소가 빠르게 분해된다. 홈 2·3 비교: 카탈레이스는 에탄올을 분해하지 않는다(특정 반응물과만 결합).' + (more ? ' 더 넣어도 거품 → 효소는 재사용된다.' : ' 「더 넣기」도 해 보자.');
    });
    $('[data-act="reset"]').addEventListener('click', () => { if (stopA) { stopA(); stopA = null; } W = [{s: null, a: null}, {s: null, a: null}, {s: null, a: null}]; cur = -1; more = 0; bub = []; fx.innerHTML = ''; O('msg').textContent = ''; sync(); draw(); drawZoom(); });
    draw(); drawZoom();
  }
};
