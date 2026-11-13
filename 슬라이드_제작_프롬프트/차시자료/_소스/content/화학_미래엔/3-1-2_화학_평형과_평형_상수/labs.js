/* 3-1-2 화학 평형과 평형 상수 — 실험실
   cm312ratio : 농도비 규칙성 찾기 (필수 탐구 화03-탐1, 스프레드시트 활동 대신).
                실험 1–5 = 교과서 102쪽 평형 농도 자료. 후보식 ㉠ y/x, ㉡ y/x², ㉢ y/(2x), ㉣ y/x³ (x=[NO2], y=[N2O4]).
                [계산] → 고른 식의 열을 모든 행에 채움(스프레드시트 '아래로 채우기'). 일정성 = (최대−최소)/평균 %.
                [평형 농도 측정] → 처음 농도로 평형 계산: N 보존 c = a0 + 2·b0, 2Kx² + x − c = 0, K = 212(25 °C),
                측정 오차 ±0.5 %(고정 시드), 평형 농도 유효 숫자 세 자리, 농도비는 소수 첫째 자리(지도서 예시). 표 최대 8행(넘으면 덱이 추가한 가장 오래된 행을 지움).
                그래프: 가로 실험, 세로 '평균에 대한 비'(0.6–1.4, 범위 밖은 가장자리). ㉠과 ㉢은 평균에 대한 비가 같아 가로로 조금 비켜 그림. API.loop로 새 점이 커졌다 작아짐. */
window.DECK_LABS = {
  cm312ratio(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('svg');
    const BOOK=[[0.047,0.467],[0.051,0.551],[0.046,0.448],[0.045,0.428],[0.053,0.595]];
    const K=212, MAXR=8;
    const F={a:{f:(x,y)=>y/x,col:'#E08A2C',sh:'c',nm:'㉠'}, b:{f:(x,y)=>y/(x*x),col:'#16233D',sh:'d',nm:'㉡'},
             c:{f:(x,y)=>y/(2*x),col:'#0E7490',sh:'s',nm:'㉢'}, d:{f:(x,y)=>y/(x*x*x),col:'#8C99A6',sh:'m',nm:'㉣'}};
    const G={x0:70,x1:660,y0:170,y1:36}, OFF={a:-7,b:0,c:7,d:0}, LO=0.6, HI=1.4;
    let rows, done, sel='a', seed, nexp, pulse=0, newIdx=-1, note='';
    const rnd=()=>{ seed=(seed+0x6D2B79F5)|0; let z=Math.imul(seed^(seed>>>15),1|seed); z=(z+Math.imul(z^(z>>>7),61|z))^z; return ((z^(z>>>14))>>>0)/4294967296; };
    const sig3=v=>{ if(v===0) return '0'; const p=Math.floor(Math.log10(Math.abs(v))); return (Math.round(v/Math.pow(10,p-2))*Math.pow(10,p-2)); };
    const fmt=v=>{ if(v>=1000) return String(Math.round(sig3(v))); if(v>=1) return v.toFixed(1); return v.toFixed(3); };  // 지도서 예시처럼 소수 첫째 자리(211.4)
    const fc=v=>v>=0.1? v.toFixed(3) : v.toPrecision(3);  // 교과서 값(0.047)은 그대로, 새 측정값은 유효 숫자 세 자리
    // 고정 그림: 격자·축·라벨(처음 한 번만 — texText는 처음 그린 것만 KaTeX로 바뀐다)
    const bg=API.mk('g',{},svg);
    [0.8,1.0,1.2].forEach(v=>{ const y=G.y0-(G.y0-G.y1)*(v-LO)/(HI-LO);
      API.mk('path',{d:`M${G.x0} ${y} H${G.x1}`,stroke:v===1?'#5B6B7F':'#E2E7EC','stroke-width':v===1?1.5:1.5,'stroke-dasharray':v===1?'6 5':''},bg);
      API.texText(bg,G.x0-8,y+6,v.toFixed(1),{size:18,anchor:'end',fill:'#16233D',mix:true}); });
    API.arrow(bg,G.x0,G.y0,G.x1+10,G.y0,'ink',2); API.arrow(bg,G.x0,G.y0,G.x0,G.y1-8,'ink',2);
    API.texText(bg,G.x0+8,G.y1-14,'평균에 대한 비',{size:18,anchor:'start',fill:'#16233D',mix:true});
    API.texText(bg,G.x0-8,G.y0+24,'실험',{size:18,anchor:'end',fill:'#16233D',mix:true});
    const xl=[]; for(let i=0;i<MAXR;i++) xl.push(API.texText(bg,0,G.y0+22,String(i+1),{size:18,anchor:'middle',fill:'#16233D',mix:true}));
    const gr=API.mk('g',{},svg);
    const X=i=>G.x0+40+i*(G.x1-G.x0-70)/(MAXR-1);
    const Yv=r=>G.y0-(G.y0-G.y1)*(API.clamp(r,LO,HI)-LO)/(HI-LO);
    function mark(g,sh,x,y,col,r){
      if(sh==='c') API.mk('circle',{cx:x,cy:y,r:r,fill:'#fff',stroke:col,'stroke-width':3},g);
      else if(sh==='d') API.mk('circle',{cx:x,cy:y,r:r,fill:col},g);
      else if(sh==='s') API.mk('rect',{x:x-r,y:y-r,width:2*r,height:2*r,fill:'#fff',stroke:col,'stroke-width':3},g);
      else API.mk('path',{d:`M${x} ${y-r-2} L${x+r+2} ${y} L${x} ${y+r+2} L${x-r-2} ${y} Z`,fill:'#fff',stroke:col,'stroke-width':3},g);
    }
    function stats(k){ const v=rows.map(r=>F[k].f(r.x,r.y)); const m=v.reduce((s,a)=>s+a,0)/v.length; return {v,m,sp:(Math.max(...v)-Math.min(...v))/m*100}; }
    function render(){
      O('a0').textContent=(+I('a0').value).toFixed(2)+' mol/L'; O('b0').textContent=(+I('b0').value).toFixed(2)+' mol/L';
      root.querySelectorAll('[data-k]').forEach(b=>b.classList.toggle('on',b.dataset.k===sel));
      root.querySelectorAll('th[data-h]').forEach(h=>h.classList.toggle('cm312-on',h.dataset.h===sel));
      const tb=O('log'); tb.innerHTML='';
      rows.forEach((r,i)=>{ const tr=document.createElement('tr'); if(i===newIdx) tr.className='cm312-new';
        tr.innerHTML=`<td>${r.n}</td><td>${r.n<=5?r.x.toFixed(3):fc(r.x)}</td><td>${r.n<=5?r.y.toFixed(3):fc(r.y)}</td>`+['a','b','c','d'].map(k=>`<td>${done[k]?fmt(F[k].f(r.x,r.y)):''}</td>`).join('');
        tb.appendChild(tr); });
      xl.forEach((t,i)=>{ t.setAttribute('x',X(i)); t.style.display=i<rows.length?'':'none'; });
      gr.innerHTML='';
      ['a','c','d','b'].forEach(k=>{ if(!done[k]) return; const s=stats(k), c=F[k].col;
        API.mk('polyline',{points:s.v.map((v,i)=>`${X(i)+OFF[k]},${Yv(v/s.m)}`).join(' '),fill:'none',stroke:c,'stroke-width':k==='b'?3.5:2.5},gr);
        s.v.forEach((v,i)=>mark(gr,F[k].sh,X(i)+OFF[k],Yv(v/s.m),c,i===newIdx?6+3*pulse:6)); });
      let lx=G.x1-210; ['a','b','c','d'].forEach(k=>{ if(!done[k]) return; mark(gr,F[k].sh,lx,G.y1-20,F[k].col,6);
        const t=API.mk('text',{x:lx+12,y:G.y1-14,'font-size':18,fill:F[k].col,'font-weight':700},gr); t.textContent=F[k].nm; lx+=52; });
      if(!done[sel]){ O('spread').textContent='—'; O('msg').textContent=note||`${F[sel].nm} 수식을 골랐다. [계산]을 눌러 모든 실험의 값을 채워 보자.`; return; }
      const s=stats(sel); O('spread').textContent='차이 '+s.sp.toFixed(1)+' %';
      const dv=s.v.map(v=>+fmt(v)), df=Math.max(...dv)-Math.min(...dv);
      let m=`${F[sel].nm}: 최댓값과 최솟값의 차이 ${df>=100?Math.round(df):df.toFixed(1)}(평균의 ${s.sp.toFixed(1)} %) → `+(s.sp<5?`처음 농도와 관계없이 거의 일정하다(평균 ${fmt(s.m)}).`:'실험마다 달라 일정하지 않다.');
      if(['a','b','c','d'].every(k=>done[k])){ const best=['a','b','c','d'].sort((p,q)=>stats(p).sp-stats(q).sp)[0]; m+=` 가장 일정한 식: ${F[best].nm}`; }
      O('msg').textContent=m;
    }
    function reset(){ rows=BOOK.map((r,i)=>({n:i+1,x:r[0],y:r[1]})); done={}; sel='a'; seed=11; note=''; nexp=5; newIdx=-1; render(); }
    function measure(){
      const a0=+I('a0').value, b0=+I('b0').value, c=a0+2*b0;
      if(c<=0){ O('msg').textContent='넣은 기체가 없다. 처음 농도를 0보다 크게 하자.'; return; }
      let x=(-1+Math.sqrt(1+8*K*c))/(4*K), y=(c-x)/2;
      x=+(x*(1+(rnd()-.5)*0.01)).toPrecision(3); y=+(y*(1+(rnd()-.5)*0.01)).toPrecision(3);
      nexp++; rows.push({n:nexp,x,y}); if(rows.length>MAXR) rows.splice(5,1);
      newIdx=rows.length-1; pulse=1; render();
      note=`실험 ${nexp}: 평형 농도를 측정했다. 수식을 골라 [계산]해 보자.`; render();
    }
    root.querySelectorAll('[data-k]').forEach(b=>b.addEventListener('click',()=>{ sel=b.dataset.k; note=''; render(); }));
    root.querySelector('[data-act="calc"]').addEventListener('click',()=>{ done[sel]=true; note=''; render(); });
    root.querySelector('[data-act="meas"]').addEventListener('click',measure);
    root.querySelector('[data-act="reset"]').addEventListener('click',reset);
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',()=>{ O('a0').textContent=(+I('a0').value).toFixed(2)+' mol/L'; O('b0').textContent=(+I('b0').value).toFixed(2)+' mol/L'; }));
    reset();
    API.loop(root,(dt)=>{ if(pulse>0){ pulse=Math.max(0,pulse-dt*0.8); render(); } });
  }
};
