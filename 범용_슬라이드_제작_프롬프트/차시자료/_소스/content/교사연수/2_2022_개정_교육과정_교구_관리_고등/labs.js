window.DECK_LABS = {
  // 실습 타이머 (AUTHORING.md 6.1)
  'ts2h-timer'(root, API){
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
  // 수량 계산기: 2022 기준 — 기준 실 수(학급 수 구간, 원고 초안 제2부 Ⅱ-2), 4학생당 1 = 올림(n/4), 학생당 1 = n, 실험실당 k = k × 실 수
  'ts2h-calc'(root, API){
    const O = k => root.querySelector(`[data-o="${k}"]`), I = k => root.querySelector(`[data-i="${k}"]`);
    const lim = root.dataset.level === 'm' ? [10, 23, 31] : [10, 24, 30];   // 중: 10·23·31 / 고: 10·24·30
    const D = { cls: +I('cls').value, n: +I('n').value };
    function draw(){
      const cls = +I('cls').value, n = +I('n').value;
      const rooms = cls <= lim[0] ? 1 : cls <= lim[1] ? 2 : cls <= lim[2] ? 3 : 4;
      O('cls').textContent = cls + '학급'; O('n').textContent = n + '명';
      O('rooms').textContent = rooms + '실';
      O('msg').textContent = ['', lim[0] + '학급 이하', (lim[0] + 1) + '~' + lim[1] + '학급', (lim[1] + 1) + '~' + lim[2] + '학급', (lim[2] + 1) + '학급 이상'][rooms] + ' 구간';
      O('g4').textContent = Math.ceil(n / 4) + '개'; O('s1').textContent = n + '개';
      O('ext').textContent = 4 * rooms + '개'; O('blk').textContent = 2 * rooms + '개';
    }
    root.querySelectorAll('input').forEach(i => i.addEventListener('input', draw));
    root.querySelector('[data-act="reset"]').addEventListener('click', () => { I('cls').value = D.cls; I('n').value = D.n; draw(); });
    draw();
  }
};
