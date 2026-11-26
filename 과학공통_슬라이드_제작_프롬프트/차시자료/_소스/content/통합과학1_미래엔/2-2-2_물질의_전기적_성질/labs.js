/* 2-2-2 물질의 전기적 성질 — 실험실 (덱 접두어 is1222) */
window.DECK_LABS = {
  /* 여러 가지 물체의 전기적 성질 비교: 물체를 회로에 끼우고 스위치를 닫으면 디지털 전류계 값과 전자 흐름이 보인다. 값은 지도서 예시(클립 1.764 A, 연필심 0.719 A, LED 정방향 0.036 A) */
  is1222circ(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const OBJ = ['클립', '연필심', '지우개', '나무 막대', '발광 다이오드'];
    const AMP = [1.764, 0.719, 0, 0, null];
    let k = -1, fwd = true, closed = false, rec = {}, stopA = null;
    const amp = () => k < 0 ? 0 : (k === 4 ? (fwd ? 0.036 : 0) : AMP[k]);
    const fig = API.mk('g', {}, svg), tab = API.mk('g', {}, svg);
    // 회로 경로(시계 방향): 전지(왼쪽) → 위 → 전류계 → 오른쪽 → 아래 물체 → 왼쪽
    const P = [[60, 60], [500, 60], [500, 230], [60, 230]];
    const per = 2 * (440 + 170);
    const along = d => { d = ((d % per) + per) % per; if (d < 440) return [60 + d, 60]; d -= 440; if (d < 170) return [500, 60 + d]; d -= 170; if (d < 440) return [500 - d, 230]; d -= 440; return [60, 230 - d]; };
    const dots = [];
    function draw(){
      fig.innerHTML = ''; dots.length = 0;
      API.mk('path', {d: 'M60 60 H500 V230 H60 Z', fill: 'none', stroke: '#5B6B7F', 'stroke-width': 4}, fig);
      // 전지
      API.mk('rect', {x: 40, y: 120, width: 40, height: 56, rx: 6, fill: '#F7C548', stroke: '#C2410C', 'stroke-width': 2}, fig);
      T(fig, 60, 154, '1.5 V', {size: 16, anchor: 'middle'});
      // 스위치
      API.mk('rect', {x: 150, y: 50, width: 70, height: 20, fill: '#FFFFFF'}, fig);
      API.mk('circle', {cx: 150, cy: 60, r: 5, fill: '#16233D'}, fig); API.mk('circle', {cx: 220, cy: 60, r: 5, fill: '#16233D'}, fig);
      API.mk('line', {x1: 150, y1: 60, x2: closed ? 220 : 210, y2: closed ? 60 : 30, stroke: '#16233D', 'stroke-width': 4}, fig);
      T(fig, 185, 92, '스위치', {size: 16, anchor: 'middle', fill: API.COL.muted});
      // 디지털 전류계
      API.mk('rect', {x: 300, y: 30, width: 130, height: 60, rx: 8, fill: '#16233D'}, fig);
      T(fig, 365, 70, closed ? amp().toFixed(3) + ' A' : '0.000 A', {size: 22, anchor: 'middle', fill: '#8BD3A7', weight: 700});
      T(fig, 365, 112, '디지털 전류계', {size: 16, anchor: 'middle', fill: API.COL.muted});
      // 물체 자리(아래)
      API.mk('rect', {x: 190, y: 214, width: 180, height: 32, fill: '#FFFFFF'}, fig);
      API.mk('path', {d: 'M178 222 l14 8 l-14 8 Z', fill: '#D7263D'}, fig); API.mk('path', {d: 'M382 222 l-14 8 l14 8 Z', fill: '#1F6FD1'}, fig);
      if (k < 0) T(fig, 280, 236, '물체를 고르자', {size: 17, anchor: 'middle', fill: API.COL.muted});
      else if (k === 0) API.mk('path', {d: 'M200 230 H350 Q362 230 362 220 Q362 210 350 210 H215 Q205 210 205 218 Q205 226 215 226 H340', fill: 'none', stroke: '#8C99A6', 'stroke-width': 4}, fig);
      else if (k === 1) API.mk('rect', {x: 200, y: 225, width: 160, height: 10, rx: 3, fill: '#3A3F47'}, fig);
      else if (k === 2) API.mk('rect', {x: 220, y: 214, width: 120, height: 32, rx: 6, fill: '#F08A97', stroke: '#D7263D'}, fig);
      else if (k === 3) API.mk('rect', {x: 195, y: 222, width: 170, height: 16, rx: 3, fill: '#C8A27A', stroke: '#8B5E34'}, fig);
      else {
        const on = closed && fwd;
        API.mk('path', {d: 'M262 212 q18 -26 36 0 v24 h-36 Z', fill: on ? '#FF4D5E' : '#F6C0C6', stroke: '#D7263D', 'stroke-width': 2}, fig);
        if (on) API.mk('circle', {cx: 280, cy: 214, r: 30, fill: '#FF4D5E', opacity: .25}, fig);
        API.mk('line', {x1: 200, y1: 230, x2: 262, y2: 230, stroke: '#8C99A6', 'stroke-width': 3}, fig); API.mk('line', {x1: 298, y1: 230, x2: 360, y2: 230, stroke: '#8C99A6', 'stroke-width': 3}, fig);
        T(fig, 280, 268, fwd ? '긴 다리 → (+) 쪽' : '방향을 바꿈', {size: 16, anchor: 'middle', fill: API.COL.muted});
      }
      if (closed && amp() > 0) for (let i = 0; i < 14; i++) dots.push(API.mk('circle', {r: 5, fill: API.COL.minus}, fig));
      place(0);
    }
    function place(t){ const sp = 40 + amp() * 110; dots.forEach((d, i) => { const [x, y] = along(per - (i * per / dots.length + t * sp)); d.setAttribute('cx', x.toFixed(1)); d.setAttribute('cy', y.toFixed(1)); const hid = (y < 70 && x > 290 && x < 440) || (x < 70 && y > 110 && y < 186) || (y > 200 && x > 190 && x < 370); d.setAttribute('opacity', hid ? 0 : 1); }); }
    function drawTab(){
      tab.innerHTML = '';
      API.mk('rect', {x: 10, y: 286, width: 540, height: 146, rx: 10, fill: '#F6F9FC', stroke: '#C9D3DD', 'stroke-width': 2}, tab);
      T(tab, 24, 310, '물체', {size: 17, weight: 700}); T(tab, 250, 310, '전류 [A]', {size: 17, weight: 700}); T(tab, 380, 310, '결과', {size: 17, weight: 700});
      OBJ.forEach((n, i) => {
        const y = 334 + i * 22; T(tab, 24, y, n, {size: 16});
        let v = '', r = '';
        if (i === 4) { const a = rec['4f'], b = rec['4r']; if (a !== undefined || b !== undefined) { v = [a !== undefined ? a.toFixed(3) : '', b !== undefined ? b.toFixed(3) : ''].filter(Boolean).join(' / '); r = (a !== undefined && b !== undefined) ? '방향에 따라 다름' : (a || b) ? '흐름' : '흐르지 않음'; } }
        else if (rec[i] !== undefined) { v = rec[i].toFixed(3); r = rec[i] > 0 ? '흐름' : '흐르지 않음'; }
        T(tab, 250, y, v, {size: 16}); T(tab, 380, y, r, {size: 16, fill: r === '흐름' ? API.COL.minus : r ? API.COL.muted : API.COL.ink});
      });
    }
    const stop = () => { if (stopA) { stopA(); stopA = null; } };
    function sync(){
      O('obj').querySelectorAll('[data-k]').forEach(b => b.classList.toggle('on', +b.dataset.k === k));
      $('[data-act="flip"]').disabled = k !== 4;
      $('[data-act="sw"]').textContent = closed ? '스위치 열기' : '스위치 닫기';
    }
    O('obj').querySelectorAll('[data-k]').forEach(b => b.addEventListener('click', () => { k = +b.dataset.k; closed = false; stop(); sync(); draw(); O('msg').textContent = ''; }));
    $('[data-act="flip"]').addEventListener('click', () => { fwd = !fwd; closed = false; stop(); sync(); draw(); O('msg').textContent = '다이오드의 연결 방향을 바꿨다.'; });
    $('[data-act="sw"]').addEventListener('click', () => {
      if (k < 0) { O('msg').textContent = '먼저 회로에 연결할 물체를 고르자.'; return; }
      closed = !closed; stop(); sync(); draw();
      if (!closed) { O('msg').textContent = '스위치를 열었다.'; return; }
      const a = amp(); rec[k === 4 ? (fwd ? '4f' : '4r') : k] = a; drawTab();
      O('msg').textContent = `${OBJ[k]}${k === 4 ? (fwd ? '(정방향)' : '(역방향)') : ''}: ${a.toFixed(3)} A → ${a > 0 ? '전류가 흐른다' : '전류가 흐르지 않는다'}`;
      if (a > 0) { let t = 0; stopA = API.loop(root, dt => { t += dt; place(t); }); }
    });
    $('[data-act="sum"]').addEventListener('click', () => {
      const need = [0, 1, 2, 3].filter(i => rec[i] === undefined).map(i => OBJ[i]);
      if (need.length || (rec['4f'] === undefined && rec['4r'] === undefined)) { O('msg').textContent = `아직 측정하지 않은 물체가 있다: ${need.concat(rec['4f'] === undefined && rec['4r'] === undefined ? ['발광 다이오드'] : []).join(', ')}`; return; }
      const both = rec['4f'] !== undefined && rec['4r'] !== undefined;
      O('msg').textContent = `전류가 흐름: 클립, 연필심 / 흐르지 않음: 지우개, 나무 막대 / 발광 다이오드: ${both ? '방향에 따라 흐르기도, 흐르지 않기도 한다 → 반도체' : '방향을 바꿔서도 측정해 보자'}`;
    });
    $('[data-act="reset"]').addEventListener('click', () => { stop(); k = -1; fwd = true; closed = false; rec = {}; O('msg').textContent = ''; sync(); draw(); drawTab(); });
    sync(); draw(); drawTab();
  }
};
