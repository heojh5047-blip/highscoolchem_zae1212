/* 2-1-1 우주 초기에 생성된 원소 — 실험실 (덱 접두어 is1211) */
window.DECK_LABS = {
  /* 간이 분광기: 광원을 고르면 스펙트럼 띠가 보이고, 촬영해 기록한 줄을 쌓아 비교선으로 겹치는지 본다.
     선 위치는 실제 파장(gen.py와 같은 값), x = 40 + (λ − 400)/300 × 520 */
  is1211spec(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`);
    const svg = $('svg'), NS = 'http://www.w3.org/2000/svg';
    const LN = {H: [410.2, 434.0, 486.1, 656.3], He: [447.1, 471.3, 492.2, 501.6, 587.6, 667.8], Na: [589.0, 589.6]};
    const SRC = [
      {name: '백열등', kind: 'cont', el: [], d: '여러 색이 끊김 없이 이어진 연속 스펙트럼'},
      {name: '수소 방전관', kind: 'emit', el: ['H'], d: '어두운 바탕에 밝은 선 4개 — 수소의 방출 스펙트럼'},
      {name: '헬륨 방전관', kind: 'emit', el: ['He'], d: '어두운 바탕에 밝은 선 — 헬륨의 방출 스펙트럼(노란 선이 뚜렷)'},
      {name: '나트륨 등', kind: 'emit', el: ['Na'], d: '노란 선 두 개가 거의 붙어 있다 — 나트륨'},
      {name: '별', kind: 'abs', el: ['H', 'He'], d: '연속 스펙트럼 위에 검은 선 — 흡수 스펙트럼'}
    ];
    const X = l => 40 + (l - 400) / 300 * 520;
    const rgb = l => { let r, g, b;
      if (l < 440) [r, g, b] = [-(l - 440) / 60, 0, 1]; else if (l < 490) [r, g, b] = [0, (l - 440) / 50, 1];
      else if (l < 510) [r, g, b] = [0, 1, -(l - 510) / 20]; else if (l < 580) [r, g, b] = [(l - 510) / 70, 1, 0];
      else if (l < 645) [r, g, b] = [1, -(l - 645) / 65, 0]; else [r, g, b] = [1, 0, 0];
      const f = l < 420 ? 0.3 + 0.7 * (l - 380) / 40 : 1;
      return '#' + [r, g, b].map(c => Math.round(255 * Math.pow(c * f, 0.8)).toString(16).padStart(2, '0')).join(''); };
    const defs = API.mk('defs', {}, svg), gr = API.mk('linearGradient', {id: 'is1211-p17-g', x1: 0, y1: 0, x2: 1, y2: 0}, defs);
    for (let l = 400; l <= 700; l += 10) API.mk('stop', {offset: (l - 400) / 300, 'stop-color': rgb(l)}, gr);
    const lines = s => s.el.flatMap(e => LN[e]);
    function band(g, s, y, h){
      API.mk('rect', {x: 40, y, width: 520, height: h, fill: s.kind === 'emit' ? '#111111' : 'url(#is1211-p17-g)'}, g);
      lines(s).forEach(l => API.mk('rect', {x: X(l) - 1.5, y, width: 3, height: h, fill: s.kind === 'emit' ? rgb(l) : '#111111'}, g));
    }
    // 고정 부분: 위 띠 틀, 파장 눈금
    API.texText(svg, 40, 22, '지금 보이는 스펙트럼', {size: 18, mix: true});
    [400, 500, 600, 700].forEach(l => { API.mk('line', {x1: X(l), y1: 102, x2: X(l), y2: 110, stroke: API.COL.muted, 'stroke-width': 2}, svg); API.texText(svg, X(l), 130, String(l), {size: 18, anchor: 'middle'}); });
    API.texText(svg, 560, 150, '파장 [nm]', {size: 18, anchor: 'end', mix: true});
    API.texText(svg, 40, 182, '기록한 스펙트럼', {size: 18, mix: true});
    const now = API.mk('g', {}, svg), recG = API.mk('g', {}, svg), cmpG = API.mk('g', {}, svg);
    let cur = 0, rec = [], cmp = false;
    function draw(){
      root.querySelectorAll('[data-act^="s"]').forEach((b, i) => b.classList.toggle('on', i === cur));
      now.textContent = ''; band(now, SRC[cur], 34, 64);
      O('now').textContent = `${SRC[cur].name}: ${SRC[cur].d}`;
      recG.textContent = ''; cmpG.textContent = '';
      rec.forEach((i, k) => {
        const y = 196 + 56 * k; band(recG, SRC[i], y, 34);
        const t = document.createElementNS(NS, 'text'); t.setAttribute('x', 566); t.setAttribute('y', y + 24); t.setAttribute('font-size', 18); t.setAttribute('fill', '#16233D'); t.textContent = SRC[i].name.replace(' 방전관', ''); recG.appendChild(t);
      });
      if (cmp && rec.length) {
        const em = [...new Set(rec.filter(i => SRC[i].kind === 'emit').flatMap(i => lines(SRC[i])))];
        em.forEach(l => API.mk('line', {x1: X(l), y1: 190, x2: X(l), y2: 196 + 56 * rec.length - 18, stroke: API.COL.plus, 'stroke-width': 1.6, 'stroke-dasharray': '5 4'}, cmpG));
      }
    }
    function judge(){
      const has = n => rec.includes(n);
      if (!has(4)) return rec.length ? '별의 스펙트럼도 기록해 원소의 선과 비교해 보자.' : '';
      const m = [];
      if (has(1)) m.push('별의 검은 선 4개가 수소의 밝은 선과 같은 위치 → 별의 대기에 수소가 있다');
      if (has(2)) m.push('헬륨의 밝은 선 위치에도 별의 검은 선이 있다 → 헬륨도 있다');
      if (has(3)) m.push('나트륨의 노란 선 위치에는 별의 검은 선이 없다 → 이 별에서는 나트륨이 보이지 않는다');
      return m.length ? m.join('. ') + '.' : '수소·헬륨 방전관을 기록해 별과 비교해 보자.';
    }
    SRC.forEach((s, i) => $(`[data-act="s${i}"]`).addEventListener('click', () => { cur = i; draw(); }));
    $('[data-act="rec"]').addEventListener('click', () => {
      if (rec.includes(cur)) { O('msg').textContent = '이미 기록한 광원이다.'; return; }
      if (rec.length >= 4) rec.shift();
      rec.push(cur); draw(); O('msg').textContent = judge() || `${SRC[cur].name}을(를) 기록했다.`;
    });
    $('[data-act="cmp"]').addEventListener('click', () => { cmp = !cmp; draw(); O('msg').textContent = cmp ? (judge() || '방출선 위치에 빨간 점선을 그었다.') : ''; });
    $('[data-act="reset"]').addEventListener('click', () => { rec = []; cur = 0; cmp = false; O('msg').textContent = ''; draw(); });
    draw();
  }
};
