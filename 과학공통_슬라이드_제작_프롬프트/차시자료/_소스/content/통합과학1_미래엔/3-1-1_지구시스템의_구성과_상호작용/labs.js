/* 3-1-1 지구시스템의 구성과 상호작용 — 실험실 (덱 접두어 is1311) */
window.DECK_LABS = {
  /* 상호작용 찾기: 현상 카드를 보고 관계된 두 권역을 고르면 맞는지 알려 주고, 맞힌 쌍은 그림에 선으로 쌓인다(교과서 110쪽 그림 Ⅲ-9와 본문 예) */
  is1311sys(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const SP = ['기권', '수권', '지권', '생물권'];
    const POS = [[280, 50], [80, 170], [280, 290], [480, 170]];
    const COLS = ['#DDEEF8', '#CFE3F7', '#F3E6D6', '#E8F5EE'];
    // [현상, 권역 a, 권역 b, 설명]
    const Q = [['바다의 물이 증발해 구름이 된다', 0, 1, '수권의 물이 수증기가 되어 기권으로'],
               ['식물이 광합성으로 이산화 탄소를 흡수한다', 0, 3, '기권의 탄소가 생물권으로'],
               ['파도가 바닷가의 바위를 깎는다', 1, 2, '수권이 지권을 침식'],
               ['화산 폭발로 화산재와 화산 가스가 하늘을 덮는다', 0, 2, '지권의 물질이 기권으로'],
               ['바람이 해수면 위에서 계속 불어 해류가 생긴다', 0, 1, '기권의 운동이 수권을 움직임'],
               ['물고기가 바닷물에 녹은 산소로 호흡한다', 1, 3, '수권의 물질을 생물권이 이용'],
               ['나무뿌리가 바위 틈을 넓혀 바위를 쪼갠다', 2, 3, '생물권이 지권을 풍화'],
               ['강물이 흙과 모래를 바다로 운반한다', 1, 2, '수권이 지권의 물질을 운반']];
    let i = 0, pick = [], got = [];
    const g = API.mk('g', {}, svg);
    function draw(){
      g.innerHTML = '';
      got.forEach(k => { const [a, b] = [Q[k][1], Q[k][2]]; API.mk('line', {x1: POS[a][0], y1: POS[a][1], x2: POS[b][0], y2: POS[b][1], stroke: API.COL.field, 'stroke-width': 4, opacity: .55}, g); });
      if (pick.length === 2) API.mk('line', {x1: POS[pick[0]][0], y1: POS[pick[0]][1], x2: POS[pick[1]][0], y2: POS[pick[1]][1], stroke: API.COL.equi, 'stroke-width': 5, 'stroke-dasharray': '10 7'}, g);
      SP.forEach((n, k) => {
        const [x, y] = POS[k], on = pick.includes(k);
        API.mk('rect', {x: x - 66, y: y - 28, width: 132, height: 56, rx: 12, fill: COLS[k], stroke: on ? API.COL.equi : '#9FB0C2', 'stroke-width': on ? 4 : 2}, g);
        T(g, x, y + 7, n, {size: 21, anchor: 'middle', weight: 700});
      });
      T(g, 20, 360, `맞힌 현상 ${got.length} / ${Q.length}`, {size: 18, weight: 700});
      got.slice(-3).forEach((k, j) => T(g, 20, 386 + j * 22, `✓ ${Q[k][0]} (${SP[Q[k][1]]}–${SP[Q[k][2]]})`, {size: 15, fill: API.COL.muted}));
    }
    function show(){ O('card').textContent = Q[i][0]; pick = []; sync(); draw(); }
    function sync(){ O('sp').querySelectorAll('[data-p]').forEach(b => b.classList.toggle('on', pick.includes(+b.dataset.p))); }
    O('sp').querySelectorAll('[data-p]').forEach(b => b.addEventListener('click', () => {
      const p = +b.dataset.p;
      if (pick.includes(p)) pick = pick.filter(x => x !== p); else { pick.push(p); if (pick.length > 2) pick.shift(); }
      O('msg').textContent = ''; sync(); draw();
    }));
    $('[data-act="ok"]').addEventListener('click', () => {
      if (pick.length < 2) { O('msg').textContent = '권역을 두 개 고르자.'; return; }
      const q = Q[i], ok = pick.includes(q[1]) && pick.includes(q[2]);
      if (ok) { if (!got.includes(i)) got.push(i); O('msg').textContent = `정답! ${SP[q[1]]}–${SP[q[2]]}: ${q[3]}.${got.length === Q.length ? ' 모든 현상을 맞혔다 — 한 권역의 변화가 다른 권역으로 이어진다.' : ' 「다음 현상」을 눌러 보자.'}`; }
      else O('msg').textContent = `다시 생각해 보자. 이 현상에서 물질이나 에너지는 어디에서 어디로 움직일까?`;
      draw();
    });
    $('[data-act="next"]').addEventListener('click', () => { i = (i + 1) % Q.length; O('msg').textContent = ''; show(); });
    $('[data-act="reset"]').addEventListener('click', () => { i = 0; got = []; O('msg').textContent = ''; show(); });
    show();
  }
};
