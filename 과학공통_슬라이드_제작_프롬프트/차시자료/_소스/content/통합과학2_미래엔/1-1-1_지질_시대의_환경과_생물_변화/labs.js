/* 1-1-1 지질 시대의 환경과 생물 변화 — 실험실 (덱 접두어 is2111) */
window.DECK_LABS = {
  /* 지질 시대 시간 띠: 시대를 고르면 실제 길이 띠에서 위치가 강조되고, 기후·수륙 분포(모식)·번성한 생물이 나온다(교과서 15–17쪽, 지도서 81쪽) */
  is2111era(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor || 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const E = [
      {n: '선캄브리아시대', s: '약 46억 년 전', p: 88.2, c: '#C9B8E8', cl: ['다양한 기후', '말기에는 매우 한랭'], tp: 1, map: 0,
       life: ['남세균', '스트로마톨라이트', '에디아카라 생물군', '다세포 생물(후기)'], ev: '광합성을 하는 남세균이 바다와 대기에 산소를 늘려 다양한 생물이 출현할 환경을 만들었다.'},
      {n: '고생대', s: '약 5억 3900만 년 전', p: 6.3, c: '#9FD3C7', cl: ['대체로 온난·습윤', '말기에는 한랭'], tp: 2, map: 1,
       life: ['삼엽충', '완족류', '어류', '양서류', '거대 곤충', '양치식물'], ev: '오존층이 자외선을 막아 생물이 육지로 퍼졌다. 말기에 판게아가 생기고 한랭해져 삼엽충 등 많은 생물이 멸종했다.'},
      {n: '중생대', s: '약 2억 5200만 년 전', p: 4.1, c: '#F3C77A', cl: ['전반적으로 온난', '(화산 활동 → 온실 효과)'], tp: 3, map: 2,
       life: ['공룡', '암모나이트', '해양 파충류', '겉씨식물'], ev: '판게아가 분리되며 서식지 환경이 다양해졌다. 말기의 급격한 환경 변화로 공룡과 암모나이트가 멸종했다.'},
      {n: '신생대', s: '약 6600만 년 전', p: 1.4, c: '#F4A9A0', cl: ['중기까지 온난', '말기 빙하기·간빙기 반복'], tp: 1, map: 3,
       life: ['화폐석', '매머드(포유류)', '속씨식물', '인류의 조상'], ev: '대서양이 넓어지고 히말라야산맥이 생겨 수륙 분포가 현재와 비슷해졌다. 인류의 조상이 출현했다.'}];
    const MAPS = [
      ['M60 230 Q80 210 100 230 Q90 250 60 230 Z', 'M150 200 Q175 190 185 215 Q165 230 150 200 Z'],
      ['M80 190 Q140 170 190 190 Q215 230 185 280 Q130 300 95 275 Q60 240 80 190 Z'],
      ['M70 190 Q130 175 200 192 Q210 215 180 228 Q120 232 85 222 Q60 210 70 190 Z', 'M95 245 Q150 238 200 250 Q205 285 170 298 Q120 302 95 285 Z'],
      ['M40 190 Q70 180 85 200 Q75 225 55 225 Z', 'M65 240 Q85 235 88 260 Q80 290 70 295 Q60 270 65 240 Z', 'M120 190 Q150 182 160 205 Q145 220 125 215 Z', 'M130 228 Q160 225 162 255 Q150 290 140 292 Q125 260 130 228 Z', 'M175 185 Q230 175 250 205 Q235 228 200 230 Q175 220 175 185 Z', 'M215 260 Q240 258 245 275 Q225 285 210 275 Z']];
    let k = -1, mode = 0, seen = new Set();
    const g = API.mk('g', {}, svg);
    function draw(){
      g.innerHTML = '';
      const W = 520; let x = 20;
      E.forEach((e, i) => {
        const w = mode ? W / 4 : W * e.p / 100;
        API.mk('rect', {x, y: 30, width: w, height: 50, fill: e.c, stroke: i === k ? API.COL.ink : 'none', 'stroke-width': i === k ? 4 : 0}, g);
        if (mode) T(g, x + w / 2, 61, e.n.replace('선캄브리아시대', '선캄브리아'), {size: 17, anchor: 'middle', weight: i === k ? 700 : 400});
        x += w;
      });
      API.mk('rect', {x: 20, y: 30, width: W, height: 50, fill: 'none', stroke: API.COL.ink, 'stroke-width': 1.5}, g);
      if (!mode) { T(g, 250, 61, '선캄브리아시대', {size: 18, anchor: 'middle'}); T(g, 20, 100, '46억 년 전', {size: 16}); T(g, 540, 100, '현재', {size: 16, anchor: 'end'}); }
      else T(g, 280, 100, '같은 폭으로 펼친 띠 — 실제 길이가 아님', {size: 16, anchor: 'middle', fill: API.COL.muted});
      if (k < 0) { T(g, 280, 250, '왼쪽에서 시대를 골라 보자', {size: 20, anchor: 'middle', fill: API.COL.muted}); return; }
      const e = E[k];
      T(g, 20, 140, e.n, {size: 26, weight: 700});
      T(g, 20, 166, `시작: ${e.s} · 전체의 ${e.p} %`, {size: 18});
      API.mk('rect', {x: 20, y: 176, width: 250, height: 136, rx: 10, fill: '#CFE3F7'}, g);
      MAPS[e.map].forEach(d => API.mk('path', {d, fill: '#E3D3B5', stroke: '#8C7A60', 'stroke-width': 2}, g));
      if (k === 1) T(g, 140, 245, '판게아', {size: 18, anchor: 'middle', weight: 700});
      T(g, 145, 330, '수륙 분포(모식)', {size: 16, anchor: 'middle', fill: API.COL.muted});
      // 온도계
      API.mk('rect', {x: 300, y: 184, width: 20, height: 110, rx: 10, fill: '#FFFFFF', stroke: API.COL.ink, 'stroke-width': 2}, g);
      const h = [0, 35, 65, 95][e.tp];
      API.mk('rect', {x: 304, y: 290 - h, width: 12, height: h, rx: 6, fill: e.tp === 1 ? '#1F6FD1' : '#D7263D'}, g);
      API.mk('circle', {cx: 310, cy: 300, r: 14, fill: e.tp === 1 ? '#1F6FD1' : '#D7263D'}, g);
      T(g, 335, 220, '기후', {size: 18, weight: 700});
      e.cl.forEach((s, j) => T(g, 335, 248 + j * 26, s, {size: 18}));
      // 생물 칩
      T(g, 20, 360, '번성한 생물', {size: 18, weight: 700});
      let cx = 20, cy = 372;
      e.life.forEach(s => {
        const w = s.length * 17 + 22;
        if (cx + w > 545) { cx = 20; cy += 34; }
        API.mk('rect', {x: cx, y: cy, width: w, height: 28, rx: 14, fill: e.c, stroke: '#8C99A6'}, g);
        T(g, cx + w / 2, cy + 20, s, {size: 17, anchor: 'middle'});
        cx += w + 8;
      });
    }
    function sync(){
      O('era').querySelectorAll('[data-p]').forEach(b => b.classList.toggle('on', +b.dataset.p === k));
      O('mode').querySelectorAll('[data-m]').forEach(b => b.classList.toggle('on', +b.dataset.m === mode));
    }
    function say(){
      if (k < 0) { O('msg').textContent = '시대를 고르면 그 시대의 환경과 생물이 나온다.'; return; }
      let s = E[k].ev;
      if (k === 3 && !mode) s += ' 실제 띠에서는 1.4 %라 거의 보이지 않는다 — 「같은 폭으로 펼치기」를 눌러 보자.';
      if (seen.size === 4) s += ' ✔ 네 시대를 모두 봤다: 환경이 크게 바뀔 때마다 번성하는 생물도 바뀌었다.';
      O('msg').textContent = s;
    }
    O('era').querySelectorAll('[data-p]').forEach(b => b.addEventListener('click', () => { k = +b.dataset.p; seen.add(k); sync(); draw(); say(); }));
    O('mode').querySelectorAll('[data-m]').forEach(b => b.addEventListener('click', () => { mode = +b.dataset.m; sync(); draw(); say(); }));
    sync(); draw(); say();
  },

  /* 대멸종 가설 평가: 시기와 가설을 고르면 증거 카드가 나오고, 학생이 「가장 유력/보조 요인/근거 약함」을 판단해 평가표를 채운다(교과서 18–19쪽, 지도서 83쪽 예시 답안) */
  is2111ext(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor || 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const PER = ['고생대 말', '중생대 말'], HYP = ['운석 충돌설', '화산 폭발설', '수륙 분포 변화설'], J = ['근거 약함', '보조 요인', '가장 유력'];
    const E = [
      [{ev: ['이 시기 경계 지층에서 뚜렷한 운석 구덩이나', '이리듐 농집층은 잘 알려져 있지 않다.'], a: 0},
       {ev: ['시베리아 지역에 대규모 용암층이 남아 있다.', '화산 활동이 약 100만 년 동안 이어졌다고 추정.'], a: 2},
       {ev: ['이 무렵 초대륙 판게아가 형성되었다.', '얕은 바다가 줄고 해류·기후가 변했을 수 있다.'], a: 1}],
      [{ev: ['중생대–신생대 경계 지층에 이리듐(Ir)이 많다.', '멕시코에서 큰 운석 구덩이가 발견되었다.'], a: 2},
       {ev: ['같은 무렵 인도 데칸 지역에 넓은 용암 대지가', '생겼다 — 환경 변화를 키웠다는 의견이 있다.'], a: 1},
       {ev: ['판게아의 분리는 수천만 년에 걸친 느린 변화라', '짧은 기간의 대멸종을 혼자 설명하기 어렵다.'], a: 0}]];
    const X = t => 60 + (6 - t) / 6 * 480, Y = n => 190 - n / 900 * 160;
    const PTS = [[5.39, 80], [5.0, 250], [4.5, 430], [4.45, 330], [4.2, 400], [3.8, 420], [3.72, 330], [3.3, 380], [2.6, 430], [2.52, 200], [2.3, 300], [2.01, 250], [1.5, 380], [1.0, 520], [0.66, 430], [0.4, 620], [0, 880]];
    const DIP = [[2.52, 200], [0.66, 430]];
    let p = -1, h = -1, rec = [[null, null, null], [null, null, null]];
    const g = API.mk('g', {}, svg);
    function draw(){
      g.innerHTML = '';
      API.mk('line', {x1: 60, y1: 190, x2: 540, y2: 190, stroke: API.COL.ink, 'stroke-width': 2}, g);
      API.mk('line', {x1: 60, y1: 20, x2: 60, y2: 190, stroke: API.COL.ink, 'stroke-width': 2}, g);
      API.mk('polyline', {points: PTS.map(([t, n]) => `${X(t)},${Y(n)}`).join(' '), fill: 'none', stroke: '#1F6FD1', 'stroke-width': 3}, g);
      T(g, 66, 34, '해양 생물 과의 수(모식)', {size: 16, fill: API.COL.muted});
      [[5.39, '5.39'], [2.52, '2.52'], [0.66, '0.66'], [0, '0']].forEach(([t, s]) => T(g, X(t), 210, s, {size: 16, anchor: 'middle'}));
      T(g, 300, 230, '시간(억 년 전)', {size: 16, anchor: 'middle', fill: API.COL.muted});
      DIP.forEach(([t, n], i) => API.mk('circle', {cx: X(t), cy: Y(n), r: i === p ? 10 : 6, fill: '#D7263D', opacity: i === p ? 1 : .45}, g));
      if (p >= 0) {
        const [t, n] = DIP[p];
        T(g, 150, 182, `● ${PER[p]} 대멸종 → 이후 다시 증가`, {size: 17, weight: 700, fill: '#D7263D'});
      }
      // 증거 카드
      API.mk('rect', {x: 10, y: 245, width: 540, height: 92, rx: 10, fill: '#FFF7DB', stroke: '#E08A2C', 'stroke-width': 2}, g);
      if (p < 0 || h < 0) T(g, 280, 298, '시기와 가설을 고르면 증거 카드가 나온다', {size: 18, anchor: 'middle', fill: API.COL.muted});
      else {
        T(g, 22, 270, `${PER[p]} · ${HYP[h]} — 증거`, {size: 18, weight: 700});
        E[p][h].ev.forEach((s, j) => T(g, 22, 297 + j * 26, s, {size: 18}));
      }
      // 평가표
      T(g, 10, 360, '평가표', {size: 17, weight: 700});
      HYP.forEach((s, j) => T(g, 220 + j * 120, 360, s.replace(' 변화설', ''), {size: 16, anchor: 'middle'}));
      PER.forEach((s, i) => {
        T(g, 10, 390 + i * 34, s, {size: 17});
        rec[i].forEach((r, j) => {
          const ok = r !== null && r === E[i][j].a;
          API.mk('rect', {x: 166 + j * 120, y: 370 + i * 34, width: 108, height: 28, rx: 6, fill: r === null ? '#F2F4F7' : ok ? '#E8F5EE' : '#FCE8EA', stroke: '#C9D3DD'}, g);
          T(g, 220 + j * 120, 390 + i * 34, r === null ? '—' : J[r], {size: 16, anchor: 'middle', fill: ok ? '#2E9E6A' : API.COL.ink});
        });
      });
    }
    function sync(){
      O('per').querySelectorAll('[data-p]').forEach(b => b.classList.toggle('on', +b.dataset.p === p));
      O('hyp').querySelectorAll('[data-h]').forEach(b => b.classList.toggle('on', +b.dataset.h === h));
    }
    O('per').querySelectorAll('[data-p]').forEach(b => b.addEventListener('click', () => { p = +b.dataset.p; O('msg').textContent = h < 0 ? '이제 살펴볼 가설을 고르자.' : '증거를 읽고 판단해 보자.'; sync(); draw(); }));
    O('hyp').querySelectorAll('[data-h]').forEach(b => b.addEventListener('click', () => { h = +b.dataset.h; O('msg').textContent = p < 0 ? '대멸종 시기를 먼저 고르자.' : '증거를 읽고 판단해 보자.'; sync(); draw(); }));
    O('judge').querySelectorAll('[data-j]').forEach(b => b.addEventListener('click', () => {
      if (p < 0 || h < 0) { O('msg').textContent = '시기와 가설을 먼저 고르자.'; return; }
      const j = +b.dataset.j, a = E[p][h].a; rec[p][h] = j;
      const done = rec.every((r, i) => r.every((x, jj) => x === E[i][jj].a));
      if (j === a) O('msg').textContent = `알맞은 판단! ${PER[p]}의 ${HYP[h]}은 「${J[a]}」.` + (done ? ' ✔ 평가표 완성: 고생대 말은 화산 폭발설, 중생대 말은 운석 충돌설이 증거로 가장 잘 뒷받침된다.' : ' 다른 가설도 평가해 보자.');
      else O('msg').textContent = `증거를 다시 읽어 보자. 그 시기의 지층·암석에 가설을 직접 뒷받침하는 흔적이 ${a === 2 ? '뚜렷하게 있다' : a === 1 ? '있지만 단독 원인으로 보기는 어렵다' : '거의 없다'}.`;
      draw();
    }));
    sync(); draw();
  }
};
