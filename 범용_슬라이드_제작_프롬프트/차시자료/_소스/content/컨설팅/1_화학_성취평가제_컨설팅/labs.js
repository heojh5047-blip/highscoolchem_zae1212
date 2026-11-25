window.DECK_LABS = {
  // 기대 점수 계산기: 기대 점수 = 배점 × 기대 정답률, 합계 ÷ 배점 합(20) × 100 = 100점 환산 (자료 11쪽)
  cs1exp(root, API){
    const ins = [...root.querySelectorAll('input[data-i]')], O = k => root.querySelector(`[data-o="${k}"]`);
    const def = ins.map(i => +i.value);
    const f2 = v => (Math.round(v * 100) / 100).toFixed(2);
    function draw(){
      let sum = 0, tot = 0;
      ins.forEach((i, k) => { const b = +i.dataset.b, r = +i.value, s = b * r / 100; sum += s; tot += b; O('r' + k).textContent = r + '%'; O('s' + k).textContent = f2(s); });
      O('sum').textContent = f2(sum); O('conv').textContent = f2(sum / tot * 100) + '점';
    }
    ins.forEach(i => i.addEventListener('input', draw));
    root.querySelector('[data-act="reset"]').addEventListener('click', () => { ins.forEach((i, k) => i.value = def[k]); draw(); });
    draw();
  }
};
