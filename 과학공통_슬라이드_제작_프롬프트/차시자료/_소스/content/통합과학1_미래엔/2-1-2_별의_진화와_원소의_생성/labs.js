/* 2-1-2 별의 진화와 원소의 생성 — 실험실 (덱 접두어 is1212) */
window.DECK_LABS = {
  /* 지구·사람 구성 성분 비교와 유래: 원소를 고르면 두 막대가 강조되고 유래 띠의 칸이 켜진다. 자료는 교과서 59쪽 질량비 */
  is1212comp(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`);
    const svg = $('svg');
    const ORG = ['빅뱅 직후', '별 내부 핵융합', '질량이 큰 별 내부 핵융합', '초신성 폭발'];
    // [이름, 지구 %, 사람 %, 유래 번호] — null은 자료에 따로 없음(기타에 포함)
    const E = [['철', 35.0, null, 2], ['산소', 30.0, 65.0, 2], ['규소', 15.0, null, 2], ['마그네슘', 13.0, null, 2], ['니켈', 2.4, null, 3], ['황', 1.9, null, 2],
               ['칼슘', 1.1, 1.5, 2], ['알루미늄', 1.1, null, 2], ['탄소', null, 18.5, 1], ['수소', null, 9.5, 0], ['질소', null, 3.3, 1], ['인', null, 1.0, 2]];
    const X0 = 110, K = 4.6, Y = i => 52 + i * 25;
    API.texText(svg, X0, 22, '질량비 [%]', {size: 18, mix: true});
    API.mk('rect', {x: 300, y: 8, width: 16, height: 12, fill: API.COL.ox}, svg); API.texText(svg, 322, 20, '지구', {size: 18, mix: true});
    API.mk('rect', {x: 390, y: 8, width: 16, height: 12, fill: API.COL.field}, svg); API.texText(svg, 412, 20, '사람', {size: 18, mix: true});
    const hl = API.mk('rect', {x: 4, width: 552, height: 24, rx: 4, fill: '#FFE45C', opacity: .45}, svg);
    E.forEach((e, i) => {
      API.texText(svg, X0 - 10, Y(i) + 12, e[0], {size: 18, anchor: 'end', mix: true});
      if (e[1] !== null) API.mk('rect', {x: X0, y: Y(i) + 1, width: e[1] * K, height: 10, fill: API.COL.ox}, svg);
      if (e[2] !== null) API.mk('rect', {x: X0, y: Y(i) + 12, width: e[2] * K, height: 10, fill: API.COL.field}, svg);
      if (e[1] === null && e[2] === null) return;
    });
    API.mk('line', {x1: X0, y1: 46, x2: X0, y2: Y(12), stroke: API.COL.muted, 'stroke-width': 2}, svg);
    [0, 20, 40, 60].forEach(v => API.texText(svg, X0 + v * K, Y(12) + 18, String(v), {size: 18, anchor: 'middle'}));
    // 유래 띠
    const oy = 390, ow = 132, cells = ORG.map((o, i) => API.mk('rect', {x: 10 + i * (ow + 4), y: oy, width: ow, height: 40, rx: 8, fill: '#F6F9FC', stroke: '#C9D3DD', 'stroke-width': 2}, svg));
    ORG.forEach((o, i) => API.texText(svg, 10 + i * (ow + 4) + ow / 2, oy + 27, o.replace('질량이 큰 별 내부 핵융합', '큰 별 핵융합').replace('별 내부 핵융합', '별 핵융합'), {size: 18, anchor: 'middle', mix: true}));
    let cur = -1, rec = [];
    O('els').innerHTML = E.map((e, i) => `<button class="btn" data-el="${i}">${e[0]}</button>`).join('');
    const pct = v => v === null ? '자료에 따로 없음' : v + ' %';
    function draw(){
      O('els').querySelectorAll('[data-el]').forEach((b, i) => b.classList.toggle('on', rec.includes(i)));
      if (cur < 0) { hl.setAttribute('y', -100); O('info').textContent = '원소를 눌러 보자.'; }
      else {
        const e = E[cur]; hl.setAttribute('y', Y(cur) - 1);
        O('info').textContent = `${e[0]} — 지구 ${pct(e[1])}, 사람 ${pct(e[2])} · 유래: ${ORG[e[3]]}`;
      }
      cells.forEach((c, i) => { const on = cur >= 0 && E[cur][3] === i; c.setAttribute('fill', on ? '#E8F5EE' : '#F6F9FC'); c.setAttribute('stroke', on ? API.COL.field : '#C9D3DD'); });
    }
    O('els').querySelectorAll('[data-el]').forEach(b => b.addEventListener('click', () => { cur = +b.dataset.el; if (!rec.includes(cur)) rec.push(cur); O('msg').textContent = ''; draw(); }));
    $('[data-act="sum"]').addEventListener('click', () => {
      if (rec.length < 3) { O('msg').textContent = '원소를 3개 이상 골라 본 뒤 정리하자.'; return; }
      const top = k => E.filter(e => e[k] !== null).sort((a, b) => b[k] - a[k]).slice(0, 4).map(e => e[0]).join(' > ');
      const g = ORG.map((o, i) => [o, rec.filter(r => E[r][3] === i).map(r => E[r][0])]).filter(x => x[1].length).map(x => `${x[0]}: ${x[1].join(', ')}`).join(' / ');
      O('msg').textContent = `지구 ${top(1)}, 사람 ${top(2)}. 고른 원소의 유래 — ${g}. 모두 우주의 역사에서 만들어진 원소이다.`;
    });
    $('[data-act="reset"]').addEventListener('click', () => { cur = -1; rec = []; O('msg').textContent = ''; draw(); });
    draw();
  }
};
