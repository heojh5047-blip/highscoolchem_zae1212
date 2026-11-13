window.DECK_LABS = {
  // 실습 타이머: data-min(분)에서 거꾸로 센다 (AUTHORING.md 6.1 시험을 마친 코드)
  ts1timer(root, API){
    const O = k => root.querySelector(`[data-o="${k}"]`), B = k => root.querySelector(`[data-act="${k}"]`);
    const full = (+root.dataset.min || 10) * 60;
    let left = full, endAt = 0, id = 0;
    const fmt = s => String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0');
    function show(){
      O('t').textContent = fmt(Math.max(0, Math.ceil(left)));
      O('msg').textContent = left <= 0 ? '시간이 끝났습니다 — 정리해 주세요' : id ? (left <= 60 ? '1분 남았습니다' : '진행 중') : (left < full ? '멈춤' : '시작을 누르세요');
      B('go').textContent = id ? '멈춤' : '시작';
    }
    function tick(){ left = (endAt - Date.now()) / 1000; if (left <= 0){ left = 0; clearInterval(id); id = 0; } show(); }
    B('go').addEventListener('click', () => { if (id){ clearInterval(id); id = 0; } else if (left > 0){ endAt = Date.now() + left * 1000; id = setInterval(tick, 250); } show(); });
    B('plus').addEventListener('click', () => { left += 60; if (id) endAt += 60000; show(); });
    B('reset').addEventListener('click', () => { clearInterval(id); id = 0; left = full; show(); });
    show();
  },
  // 유해화학물질 판단: 원고 초안 Ⅴ-2 표의 기준함량(%) — 0 = 해당 없음
  ts1hazard(root, API){
    const D = [ // [유독물질, 사고대비물질, 슬라이더 최댓값]
      [10, 10, 40], [10, 10, 100], [6, 35, 50], [5, 0, 50], [10, 10, 30], [10, 85, 100], [5, 98, 100], [1, 0, 10] ];
    const O = k => root.querySelector(`[data-o="${k}"]`), I = k => root.querySelector(`[data-i="${k}"]`);
    const fmt = v => (Math.round(v * 10) / 10).toString();
    function setMax(){ const d = D[+I('sub').value]; const r = I('c'); r.max = d[2]; r.step = d[2] / 200; if (+r.value > d[2]) r.value = d[2]; }
    function draw(){
      const d = D[+I('sub').value], c = +I('c').value;
      O('c').textContent = fmt(c) + ' %';
      O('t1').textContent = d[0] + ' %';
      O('t2').textContent = d[1] ? d[1] + ' %' : '해당 없음';
      let ok, msg;
      if (d[1] && c >= d[1]){ ok = '해당'; msg = '사고대비물질 기준 이상 — 취급 내용 기록 5년 보존'; }
      else if (c >= d[0]){ ok = '해당'; msg = '유독물질 기준 이상 — 표시(서식4)·주 1회 점검'; }
      else { ok = '해당하지 않음'; msg = '기준함량 미만'; }
      O('ok').textContent = ok; O('ok').style.color = ok === '해당' ? API.COL.plus : API.COL.field;
      O('msg').textContent = msg;
    }
    I('sub').addEventListener('change', () => { setMax(); draw(); });
    I('c').addEventListener('input', draw);
    root.querySelector('[data-act="reset"]').addEventListener('click', () => { I('sub').value = 0; setMax(); I('c').value = 9; draw(); });
    setMax(); draw();
  }
};
