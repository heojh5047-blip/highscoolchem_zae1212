/* 1-2-1 측정과 측정 표준 — 실험실 (덱 접두어 is1121) */
window.DECK_LABS = {
  /* 측정 표준 찾기: 장소를 골라 사례를 기록하면, 쓰인 기본량별 개수가 막대그래프로 쌓이고 정리 문장이 나온다 */
  is1121std(root, API){
    const $ = s => root.querySelector(s), O = k => root.querySelector(`[data-o="${k}"]`) || root.parentElement.querySelector(`[data-o="${k}"]`);
    const svg = $('svg');
    const Q = ['시간', '길이', '질량', '전류', '온도'];
    const QC = [API.COL.bfield, API.COL.field, API.COL.plus, API.COL.equi, API.COL.ox];
    // 사례 자료(plan.md 17장 표)
    const P = [
      ['교실', [['칠판·창문 크기 정하기', [1], '맞는 칠판·창문을 주문할 수 없다'], ['수업 시작 종 시각', [0], '반마다 수업 시간이 어긋난다'], ['냉난방기 설정 온도', [4], '같은 26 ℃가 기기마다 다르다']]],
      ['보건실', [['체온계로 열 재기', [4], '열이 나는지 판단할 수 없다'], ['키·몸무게 재기', [1, 2], '성장 기록을 비교할 수 없다']]],
      ['급식실', [['식재료 저울', [2], '정해진 양을 넣을 수 없다'], ['오븐 온도·조리 시간', [4, 0], '음식이 덜 익거나 탄다']]],
      ['운동장', [['100 m 트랙', [1], '기록을 비교할 수 없다'], ['초시계로 달리기 기록', [0], '기록이 공정하지 않다']]],
      ['마트', [['고기 무게로 값 매기기', [2], '공정한 거래가 어렵다'], ['신발 치수', [1], '신어 보지 않고는 살 수 없다']]],
      ['집', [['충전기 정격 전류 확인', [3], '기기가 고장 나거나 위험하다'], ['일기 예보 기온·강수량', [4, 0, 1], '옷차림·야외 활동을 정하기 어렵다']]]
    ];
    // 막대그래프 틀: 원점 (70,340), 막대 폭 56, 간격 80, 1개 = 40 px (최대 7)
    const X = i => 110 + 76 * i, Y = n => 340 - 40 * n;
    const grid = API.mk('g', {stroke: '#E2E7EC', 'stroke-width': 1.5}, svg);
    for (let n = 1; n <= 7; n++) API.mk('line', {x1: 70, y1: Y(n), x2: 470, y2: Y(n)}, grid);
    API.arrow(svg, 70, 340, 474, 340, API.COL.muted, 2.5);
    API.arrow(svg, 70, 340, 70, 32, API.COL.muted, 2.5);
    [1, 3, 5, 7].forEach(n => API.texText(svg, 60, Y(n) + 6, String(n), {size: 18, anchor: 'end'}));
    API.texText(svg, 82, 30, '사례 수', {size: 18, mix: true});
    Q.forEach((q, i) => API.texText(svg, X(i), 370, q, {size: 19, anchor: 'middle', fill: QC[i], mix: true}));
    const bars = Q.map((q, i) => API.mk('rect', {x: X(i) - 26, width: 52, y: 340, height: 0, rx: 4, fill: QC[i]}, svg));
    let place = 0, rec = [];
    function draw(){
      root.querySelectorAll('[data-act^="p"]').forEach((b, i) => b.classList.toggle('on', i === place));
      O('cases').innerHTML = P[place][1].map((c, j) => `<button class="btn is1121-case${rec.some(r => r.c === c) ? ' on' : ''}" data-case="${j}">${c[0]}</button>`).join('');
      O('cases').querySelectorAll('[data-case]').forEach(b => b.addEventListener('click', () => {
        const c = P[place][1][+b.dataset.case];
        if (rec.some(r => r.c === c)) { O('msg').textContent = '이미 기록한 사례다.'; return; }
        rec.push({c, p: P[place][0]}); O('msg').textContent = `${P[place][0]}: ${c[0]} → ${c[1].map(k => Q[k]).join(', ')}의 측정 표준`; draw();
      }));
      const cnt = Q.map((q, i) => rec.filter(r => r.c[1].includes(i)).length);
      bars.forEach((b, i) => { const n = Math.min(cnt[i], 7); b.setAttribute('y', Y(n)); b.setAttribute('height', 340 - Y(n)); });
      O('rows').innerHTML = rec.slice(-5).map((r, i) => `<tr><td>${rec.length - Math.min(5, rec.length) + i + 1}</td><td>${r.c[0]}</td><td>${r.c[1].map(k => Q[k]).join(', ')}</td><td>${r.c[2]}</td></tr>`).join('');
      return cnt;
    }
    for (let i = 0; i < P.length; i++) $(`[data-act="p${i}"]`).addEventListener('click', () => { place = i; draw(); });
    $('[data-act="sum"]').addEventListener('click', () => {
      const cnt = draw();
      if (rec.length < 3) { O('msg').textContent = '사례를 3개 이상 기록한 뒤 정리하자.'; return; }
      const mx = Math.max(...cnt), top = Q.filter((q, i) => cnt[i] === mx).join('·');
      const places = [...new Set(rec.map(r => r.p))].length;
      O('msg').textContent = `${places}곳에서 사례 ${rec.length}개를 찾았다. 가장 많이 쓰인 기본량은 ${top}. 모든 사례가 측정 표준을 바탕으로 하며, 표준이 없으면 소통과 공정한 거래가 어려워진다.`;
    });
    $('[data-act="reset"]').addEventListener('click', () => { rec = []; place = 0; O('msg').textContent = ''; draw(); });
    draw();
  }
};
