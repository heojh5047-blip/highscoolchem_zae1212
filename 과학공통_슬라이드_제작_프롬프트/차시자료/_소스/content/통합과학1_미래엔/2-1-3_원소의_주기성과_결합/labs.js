/* 2-1-3 원소의 주기성과 결합 — 실험실 (덱 접두어 is1213) */
window.DECK_LABS = {
  /* 같은 족 유사성 실험 설계: 성질·원소·안전 조건을 고르고 실험하면 장면과 기록이 나온다. 반응 세기 Li < Na < K는 덱이 정한 시각 차이 */
  is1213alk(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    // 다시 그릴 때마다 바뀌는 글자는 일반 SVG 글자로 쓴다(texText는 처음 한 번만 조판됨)
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const MET = ['리튬', '나트륨', '칼륨'], SYMB = ['Li', 'Na', 'K'], SAFE = ['보안경', '실험복', '장갑', '핀셋', '쌀알 크기'];
    const OBS = [['광택 → 흐려짐', '광택 → 빨리 흐려짐', '광택 → 매우 빨리 흐려짐'],
                 ['기체 발생, 붉게 변함', '물 위를 돌며 격렬, 붉게 변함', '매우 격렬, 붉게 변함']];
    let p = -1, m = -1, safe = new Set(), rec = [], stopA = null, t0 = 0;
    const scene = API.mk('g', {}, svg), table = API.mk('g', {}, svg);
    function drawTable(){
      table.innerHTML = '';
      API.mk('rect', {x: 10, y: 250, width: 540, height: 180, rx: 10, fill: '#F6F9FC', stroke: '#C9D3DD', 'stroke-width': 2}, table);
      T(table, 24, 276, '기록', {size: 18, mix: true, weight: 700});
      T(table, 120, 276, '원소', {size: 18, mix: true}); T(table, 220, 276, '성질', {size: 18, mix: true}); T(table, 300, 276, '관찰', {size: 18, mix: true});
      rec.slice(-5).forEach((r, i) => {
        const y = 304 + i * 25;
        T(table, 120, y, MET[r[1]], {size: 18, mix: true});
        T(table, 220, y, r[0] ? '물·염기성' : '산소', {size: 18, mix: true});
        T(table, 300, y, OBS[r[0]][r[1]], {size: 17, mix: true});
      });
    }
    function drawScene(k){   // k: 0–1 진행 정도
      scene.innerHTML = '';
      if (p < 0 || m < 0) { T(scene, 280, 120, '성질과 원소를 고르자', {size: 20, mix: true, anchor: 'middle', fill: API.COL.muted}); return; }
      const sp = [0.5, 1, 1.8][m];
      if (p === 0) {
        API.mk('rect', {x: 120, y: 150, width: 320, height: 40, rx: 8, fill: '#E6EBF0', stroke: '#9FB0C2', 'stroke-width': 2}, scene);
        API.mk('rect', {x: 200, y: 100, width: 90, height: 50, fill: '#AEB7C0'}, scene);
        const dull = Math.min(1, k * sp);
        const c = Math.round(244 - 70 * dull);
        API.mk('rect', {x: 290, y: 100, width: 26, height: 50, fill: `rgb(${c},${c + 2},${c + 4})`, stroke: '#8C99A6'}, scene);
        T(scene, 280, 225, `${MET[m]} 단면: ${dull < .3 ? '은백색 광택' : dull < .9 ? '흐려지는 중' : '광택이 사라짐'}`, {size: 19, mix: true, anchor: 'middle'});
        T(scene, 280, 40, '페트리접시 위에서 핀셋으로 잡고 칼로 자름', {size: 18, mix: true, anchor: 'middle', fill: API.COL.muted});
      } else {
        API.mk('path', {d: 'M120 60 L120 190 Q120 205 135 205 L425 205 Q440 205 440 190 L440 60', fill: 'none', stroke: API.COL.muted, 'stroke-width': 3}, scene);
        const pink = Math.min(1, k * sp * 1.2);
        API.mk('rect', {x: 123, y: 90, width: 314, height: 112, fill: '#DDEEF8'}, scene);
        API.mk('rect', {x: 123, y: 90, width: 314, height: 112, fill: '#F5A3C7', opacity: (pink * .85).toFixed(2)}, scene);
        const size = Math.max(0, 1 - k * 0.9);
        const x = 280 + Math.sin(k * 12 * sp) * 110 * Math.min(1, sp);
        if (size > 0.05) API.mk('ellipse', {cx: x, cy: 90, rx: 14 * size + 2, ry: 6 * size + 1, fill: '#BFC7CF', stroke: '#5B6B7F'}, scene);
        for (let i = 0; i < 2 + m * 2; i++) if (size > 0.05) API.mk('circle', {cx: x - 14 + i * 9, cy: 74 - (i % 2) * 10 - ((k * 40 * sp + i * 7) % 20), r: 3, fill: '#FFFFFF', stroke: '#9FB0C2'}, scene);
        if (m === 2 && k > .1 && k < .7) API.mk('path', {d: `M${x - 8} 84 Q${x} 54 ${x + 8} 84 Z`, fill: '#C084FC', opacity: .8}, scene);
        T(scene, 280, 232, `${MET[m]} + 물(페놀프탈레인): ${pink > .5 ? '붉게 변함 → 염기성' : '반응 중'}`, {size: 19, mix: true, anchor: 'middle'});
        T(scene, 280, 40, '쌀알 크기 조각을 핀셋으로 넣음', {size: 18, mix: true, anchor: 'middle', fill: API.COL.muted});
      }
    }
    function sync(){
      O('prop').querySelectorAll('[data-p]').forEach(b => b.classList.toggle('on', +b.dataset.p === p));
      O('met').querySelectorAll('[data-m]').forEach(b => b.classList.toggle('on', +b.dataset.m === m));
      O('safe').querySelectorAll('[data-s]').forEach(b => b.classList.toggle('on', safe.has(+b.dataset.s)));
    }
    const stop = () => { if (stopA) { stopA(); stopA = null; } };
    O('prop').querySelectorAll('[data-p]').forEach(b => b.addEventListener('click', () => { p = +b.dataset.p; stop(); sync(); drawScene(0); O('msg').textContent = ''; }));
    O('met').querySelectorAll('[data-m]').forEach(b => b.addEventListener('click', () => { m = +b.dataset.m; stop(); sync(); drawScene(0); O('msg').textContent = ''; }));
    O('safe').querySelectorAll('[data-s]').forEach(b => b.addEventListener('click', () => { const s = +b.dataset.s; safe.has(s) ? safe.delete(s) : safe.add(s); sync(); }));
    $('[data-act="run"]').addEventListener('click', () => {
      if (p < 0 || m < 0) { O('msg').textContent = '확인할 성질과 원소를 먼저 고르자.'; return; }
      const miss = SAFE.filter((s, i) => !safe.has(i));
      if (miss.length) { O('msg').textContent = `설계에 빠진 안전 조건: ${miss.join(', ')} — 알칼리 금속은 물과 격렬하게 반응하므로 모두 넣어야 한다.`; return; }
      stop(); t0 = 0;
      const key = p + ',' + m; if (!rec.some(r => r[0] + ',' + r[1] === key)) rec.push([p, m]);
      drawTable();
      O('msg').textContent = `${MET[m]}(${SYMB[m]}): ${OBS[p][m]}`;
      stopA = API.loop(root, dt => { t0 += dt / 3; drawScene(Math.min(1, t0)); if (t0 >= 1) stop(); });
    });
    $('[data-act="sum"]').addEventListener('click', () => {
      const by = [0, 1].map(q => rec.filter(r => r[0] === q).map(r => MET[r[1]]));
      const q = by[0].length >= by[1].length ? 0 : 1;
      if (by[q].length < 2) { O('msg').textContent = '같은 성질로 원소를 2가지 이상 실험해야 유사성을 비교할 수 있다.'; return; }
      O('msg').textContent = `${by[q].join(', ')} 모두 ${q ? '물과 격렬하게 반응하고 수용액이 염기성(붉은색)을 띤다' : '자른 단면의 광택이 공기 중에서 빠르게 사라진다(산소와 반응)'} → 같은 족(1족) 원소는 화학적 성질이 비슷하다. 반응의 세기는 조금씩 다르다.`;
    });
    $('[data-act="reset"]').addEventListener('click', () => { stop(); p = -1; m = -1; safe = new Set(); rec = []; O('msg').textContent = ''; sync(); drawTable(); drawScene(0); });
    sync(); drawTable(); drawScene(0);
  },

  /* 전자 배치 모형: 원자 번호 1–18을 고르면 보어 모형, 전자 배치, 주기·족·원자가 전자, 1–3주기 표의 위치가 나온다 */
  is1213bohr(root, API){
    const $ = s => root.querySelector(s), O = k => $(`[data-o="${k}"]`), svg = $('svg');
    // 다시 그릴 때마다 바뀌는 글자는 일반 SVG 글자로 쓴다(texText는 처음 한 번만 조판됨)
    const T = (par, x, y, str, o = {}) => { const t = API.mk('text', {x, y, 'font-size': o.size || 18, 'text-anchor': o.anchor === 'middle' ? 'middle' : o.anchor === 'end' ? 'end' : 'start', fill: o.fill || API.COL.ink, 'font-weight': o.weight || 400}, par); t.textContent = str; return t; };
    const SYM = 'H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar'.split(' ');
    const NAME = '수소 헬륨 리튬 베릴륨 붕소 탄소 질소 산소 플루오린 네온 나트륨 마그네슘 알루미늄 규소 인 황 염소 아르곤'.split(' ');
    const shells = z => [Math.min(z, 2)].concat(z > 2 ? [Math.min(z - 2, 8)] : [], z > 10 ? [z - 10] : []);
    const pos = z => { if (z <= 2) return [1, z === 1 ? 1 : 18]; const p = z <= 10 ? 2 : 3, k = z - (p === 2 ? 2 : 10); return [p, k <= 2 ? k : k + 10]; };
    const col = g => g <= 2 ? g - 1 : g - 11;   // 1,2,13–18 → 0–7
    let cur = 0, picked = [];
    O('zs').innerHTML = SYM.map((s, i) => `<button class="btn" data-z="${i + 1}">${i + 1} ${s}</button>`).join('');
    const model = API.mk('g', {}, svg), mini = API.mk('g', {}, svg);
    // 1–3주기 표(8칸 × 3줄)
    const MX = 290, MY = 300, C = 32;
    function drawMini(){
      mini.innerHTML = '';
      ['1', '2', '13', '14', '15', '16', '17', '18'].forEach((g, i) => T(mini, MX + i * C + C / 2, MY - 6, g, {size: 16, anchor: 'middle', fill: API.COL.muted}));
      for (let z = 1; z <= 18; z++) {
        const [p, g] = pos(z), x = MX + col(g) * C, y = MY + (p - 1) * C;
        const on = z === cur, was = picked.includes(z);
        API.mk('rect', {x, y, width: C, height: C, fill: on ? '#FFE45C' : was ? '#E8F0FB' : '#FFFFFF', stroke: '#9FB0C2'}, mini);
        T(mini, x + C / 2, y + 22, SYM[z - 1], {size: 17, mix: true, anchor: 'middle'});
      }
      T(mini, MX - 8, MY + 60, '1–3주기', {size: 17, mix: true, anchor: 'end', fill: API.COL.muted});
    }
    function drawModel(){
      model.innerHTML = '';
      if (!cur) { T(model, 150, 150, '원자 번호를 고르자', {size: 20, mix: true, anchor: 'middle', fill: API.COL.muted}); return; }
      const cx = 150, cy = 150, r1 = 40, sh = shells(cur);
      sh.forEach((n, i) => {
        const r = r1 * (i + 1), last = i === sh.length - 1;
        API.mk('circle', {cx, cy, r, fill: 'none', stroke: last ? API.COL.equi : '#9FB0C2', 'stroke-width': last ? 3 : 1.5, 'stroke-dasharray': last ? '7 5' : null}, model);
        for (let k = 0; k < n; k++) {
          let t;
          if (i === 0) t = -Math.PI / 2 + Math.PI * k;
          else { const d = k % 4, base = -Math.PI / 2 + d * Math.PI / 2; t = base + (n > 4 + d ? (k < 4 ? -0.24 : 0.24) : 0); }
          API.mk('circle', {cx: cx + r * Math.cos(t), cy: cy + r * Math.sin(t), r: 6, fill: API.COL.minus}, model);
        }
      });
      API.mk('circle', {cx, cy, r: 24, fill: API.COL.plus}, model);
      T(model, cx, cy + 8, cur + '+', {size: 21, anchor: 'middle', fill: '#FFFFFF'});
      const [p, g] = pos(cur);
      T(model, 300, 60, `${NAME[cur - 1]}(${SYM[cur - 1]})`, {size: 24, mix: true, weight: 700});
      T(model, 300, 98, `전자 배치: ${sh.join(', ')}`, {size: 20, mix: true});
      T(model, 300, 132, `${p}주기 ${g}족`, {size: 20, mix: true});
      T(model, 300, 166, g === 18 ? '18족: 바깥 껍질이 꽉 참' : `원자가 전자: ${sh[sh.length - 1]}개`, {size: 20, mix: true, fill: API.COL.ox});
    }
    function draw(){
      O('zs').querySelectorAll('[data-z]').forEach(b => b.classList.toggle('on', +b.dataset.z === cur));
      drawModel(); drawMini();
      if (!cur) O('info').textContent = '원자 번호를 눌러 보자.';
      else { const [p, g] = pos(cur), sh = shells(cur); O('info').textContent = `${NAME[cur - 1]}: 껍질 ${sh.length}개(→ ${p}주기), ${g === 18 ? '가장 바깥 전자 ' + sh[sh.length - 1] + '개로 안정' : '원자가 전자 ' + sh[sh.length - 1] + '개'}(→ ${g}족)`; }
    }
    O('zs').querySelectorAll('[data-z]').forEach(b => b.addEventListener('click', () => { cur = +b.dataset.z; if (!picked.includes(cur)) picked.push(cur); O('msg').textContent = ''; draw(); }));
    $('[data-act="cmp"]').addEventListener('click', () => {
      const groups = {};
      picked.forEach(z => { const g = pos(z)[1]; (groups[g] = groups[g] || []).push(z); });
      const hit = Object.entries(groups).filter(e => e[1].length >= 2);
      if (!hit.length) { O('msg').textContent = '같은 족 원소를 2개 이상 골라 보자(예: 3번과 11번).'; return; }
      O('msg').textContent = hit.map(([g, zs]) => `${g}족 ${zs.map(z => SYM[z - 1]).join('·')}: ${+g === 18 ? '가장 바깥 껍질이 꽉 참(2 또는 8)' : '원자가 전자 ' + shells(zs[0]).slice(-1)[0] + '개로 같음'}, 껍질 수는 ${zs.map(z => shells(z).length).join('·')}`).join(' / ') + ' → 같은 족은 원자가 전자 수가 같아 성질이 비슷하다.';
    });
    $('[data-act="reset"]').addEventListener('click', () => { cur = 0; picked = []; O('msg').textContent = ''; draw(); });
    draw();
  }
};
