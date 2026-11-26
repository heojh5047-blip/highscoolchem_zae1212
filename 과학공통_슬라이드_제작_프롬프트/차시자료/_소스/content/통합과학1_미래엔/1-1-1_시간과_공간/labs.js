/* 1-1-1 시간과 공간 — 실험실 (덱 접두어 is1111) */
window.DECK_LABS = {
  /* 규모 사다리: 10^n m 보기 창을 옮기며 물체를 기록하고, 가장 작은 것·큰 것의 크기 차이(10^k 배)와 측정 방법을 비교 */
  is1111scale(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), I = k => $(`[data-i="${k}"]`);
    const svg = $('svg');
    // 물체 자료(plan.md 22장 표): 이름, 크기 m(가수, 지수), 측정 방법
    const OBJ = [
      ['수소 원자', 1, -10, 'X선'],
      ['바이러스', 1, -7, '전자 현미경'],
      ['적혈구', 7, -6, '광학 현미경'],
      ['동전 두께', 1.5, -3, '디지털 자'],
      ['DVD', 1.2, -1, '자'],
      ['농구대', 3.05, 0, '줄자'],
      ['첨성대', 9.51, 0, '레이저 길이 측정기'],
      ['에베레스트산', 8.848, 3, '위성 위치 측정'],
      ['지구 반지름', 6.4, 6, '인공위성 관측'],
      ['지구–달 거리', 3.84, 8, '레이저 왕복 시간'],
      ['태양 지름', 1.39, 9, '거리와 겉보기 크기'],
      ['우리은하', 9.5, 20, '별의 회전 반경']
    ].map(([name, a, e, how]) => ({name, a, e, how, L: Math.log10(a) + e}));
    // 사다리 좌표: log10(크기) −10 → y 410, 21 → y 30
    const AX = 180, Y = L => 410 - (L + 10) * 380 / 31;
    // 배경 띠(미시 쪽 아래, 거시 쪽 위 — 경계값을 정하지 않으려고 흐리게 이어 칠함)
    const defs = API.mk('defs', {}, svg);
    const gr = API.mk('linearGradient', {id: 'is1111-p22-band', x1: 0, y1: 1, x2: 0, y2: 0}, defs);
    API.mk('stop', {offset: '0', 'stop-color': API.COL.bfield, 'stop-opacity': .16}, gr);
    API.mk('stop', {offset: '.45', 'stop-color': '#FFFFFF', 'stop-opacity': 0}, gr);
    API.mk('stop', {offset: '.55', 'stop-color': '#FFFFFF', 'stop-opacity': 0}, gr);
    API.mk('stop', {offset: '1', 'stop-color': API.COL.equi, 'stop-opacity': .16}, gr);
    API.mk('rect', {x: 100, y: 30, width: 450, height: 380, rx: 10, fill: 'url(#is1111-p22-band)'}, svg);
    API.texText(svg, 540, 402, '미시 세계', {size: 19, anchor: 'end', fill: API.COL.bfield, mix: true});
    API.texText(svg, 540, 50, '거시 세계', {size: 19, anchor: 'end', fill: API.COL.ox, mix: true});
    // 보기 창(움직임)
    const win = API.mk('rect', {x: 112, width: 430, rx: 8, fill: 'rgba(46,158,106,.10)', stroke: API.COL.field, 'stroke-width': 3}, svg);
    // 축과 눈금
    API.arrow(svg, AX, 420, AX, 18, API.COL.muted, 2.5);
    [-10, -6, -2, 2, 6, 10, 14, 18].forEach(e => {
      API.mk('line', {x1: AX - 8, y1: Y(e), x2: AX + 8, y2: Y(e), stroke: API.COL.muted, 'stroke-width': 2.5}, svg);
      API.texText(svg, AX - 14, Y(e) + 7, `10^{${e}}`, {size: 18, anchor: 'end'});
    });
    for (let e = -10; e <= 21; e++) API.mk('line', {x1: AX - 4, y1: Y(e), x2: AX + 4, y2: Y(e), stroke: API.COL.muted, 'stroke-width': 1.2}, svg);
    API.texText(svg, AX - 14, 26, '[m]', {size: 18, anchor: 'end', mix: true});
    // 사람 기준선 약 1.7 m
    const yH = Y(Math.log10(1.7));
    API.mk('line', {x1: 112, y1: yH, x2: AX, y2: yH, stroke: API.COL.ink, 'stroke-width': 2, 'stroke-dasharray': '5 4'}, svg);
    // 물체 점과 이름표(이름표는 겹치지 않게 26 px 간격으로 펼치고 지시선으로 잇는다)
    const sorted = [...OBJ].sort((p, q) => p.L - q.L);
    let lastY = 1e9;
    sorted.forEach(o => { o.ly = Math.min(Y(o.L) + 6, lastY - 26); lastY = o.ly; });
    const shift = Math.max(0, 40 - sorted[sorted.length - 1].ly);   // 위로 넘치면 아래로 밀기
    sorted.forEach(o => { o.ly += shift; });
    OBJ.forEach(o => {
      API.mk('line', {x1: AX, y1: Y(o.L), x2: 262, y2: o.ly - 6, stroke: API.COL.muted, 'stroke-width': 1.2}, svg);
      o.dot = API.mk('circle', {cx: AX, cy: Y(o.L), r: 6, fill: '#FFFFFF', stroke: API.COL.ink, 'stroke-width': 2.5}, svg);
      API.texText(svg, 268, o.ly, o.name, {size: 18, mix: true});
    });
    let rec = [];
    const fmt = o => `${o.a}\\times10^{${o.e}}`;
    const inView = n => OBJ.filter(o => Math.abs(o.L - n) <= 1.5);
    function draw(){
      const n = +I('n').value;
      O('n').textContent = `10^${n} m`;
      const y1 = Y(Math.min(21, n + 1.5)), y2 = Y(Math.max(-10, n - 1.5));
      win.setAttribute('y', y1); win.setAttribute('height', y2 - y1);
      const v = inView(n);
      O('inview').textContent = v.length ? v.map(o => o.name).join(', ') : '없음 — 슬라이더를 더 움직여 보자';
      OBJ.forEach(o => o.dot.setAttribute('fill', rec.includes(o) ? API.COL.field : '#FFFFFF'));
      O('rows').innerHTML = rec.slice(-6).map((o, i) => `<tr><td>${rec.length - Math.min(6, rec.length) + i + 1}</td><td>${o.name}</td><td>${API.tex(fmt(o))}</td><td>${o.how}</td></tr>`).join('');
    }
    I('n').addEventListener('input', draw);
    $('[data-act="rec"]').addEventListener('click', () => {
      const n = +I('n').value, v = inView(n).filter(o => !rec.includes(o)).sort((p, q) => Math.abs(p.L - n) - Math.abs(q.L - n));
      if (!v.length) { O('msg').textContent = '보기 창 안에 새로 기록할 물체가 없다.'; return; }
      rec.push(v[0]); O('msg').textContent = `${v[0].name}: 약 ${v[0].a}×10^${v[0].e} m를 기록했다.`; draw();
    });
    $('[data-act="cmp"]').addEventListener('click', () => {
      if (rec.length < 2) { O('msg').textContent = '물체를 2개 이상 기록한 뒤 비교하자.'; return; }
      const s = rec.reduce((p, q) => p.L < q.L ? p : q), b = rec.reduce((p, q) => p.L > q.L ? p : q);
      const k = Math.round(b.L - s.L);
      O('msg').textContent = `가장 큰 ${b.name} ÷ 가장 작은 ${s.name} = 약 10^${k} 배. 크기가 이만큼 다르니 같은 도구로 잴 수 없다 — 작은 쪽은 ${s.how}, 큰 쪽은 ${b.how}(으)로 잰다.`;
    });
    $('[data-act="reset"]').addEventListener('click', () => { rec = []; I('n').value = 0; O('msg').textContent = ''; draw(); });
    draw();
  }
};
