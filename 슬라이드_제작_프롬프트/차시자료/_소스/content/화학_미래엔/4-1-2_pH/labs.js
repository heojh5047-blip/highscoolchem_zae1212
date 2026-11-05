/* 4-1-2 pH — 실험실
   cm412dil : 희석과 pH (필수 탐구 화04-탐1 「강산이나 강염기 희석 시 몰 농도에 따른 pH 데이터를 수집하여 그래프로 표현하고 해석하기」)
     · 용액 0.1 M 염산 / 0.1 M NaOH 수용액, 「10배 희석」(1 mL → 10 mL) 최대 9번 → 비커 A–J (0.1 M … 1×10^-10 M)
     · 이론 pH: 물의 자동 이온화를 함께 넣은 식 [H+] = (C + √(C² + 4Kw)) / 2 (염기는 [OH-]로 같은 식, pH = 14.00 − pOH), Kw = 1.0×10^-14 (25 °C)
     · 측정 pH = 이론 + 고정 오차표(아주 묽은 쪽은 7을 넘지 않게)
     · 「pH 측정」 → 표 누적(최근 6행) + 막대그래프(염산 plus, NaOH minus), 「이론값 보기」 → 빈 원·표 칸, 「초기화」 */
window.DECK_LABS = {
  cm412dil(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), KW=1e-14, N=10, L='ABCDEFGHIJ';
    const ERR={a:[.07,.04,-.03,.05,.09,.06,-.04,-.03,-.02,-.01], b:[-.06,-.03,.04,-.05,-.08,-.05,.04,.03,.02,.01]};
    const NAME={a:'염산',b:'수산화 나트륨 수용액'};
    const COLS={a:API.COL.plus,b:API.COL.minus};
    const thPH=(s,k)=>{ const C=0.1*Math.pow(10,-k), h=(C+Math.sqrt(C*C+4*KW))/2; return s==='a'? -Math.log10(h) : 14+Math.log10(h); };
    const msPH=(s,k)=>Math.round((thPH(s,k)+ERR[s][k])*100)/100;
    // ── 좌표
    const BX=i=>22+i*60, BW=40, BB=118, BH=56;            // 비커
    const X0=70, Y0=412, TOP=180, S=(Y0-TOP)/14, CX=k=>97+k*50, PY=p=>Y0-p*S;
    const base=API.mk('g',{},svg);
    // 그래프 틀 (정적)
    for(let p=0;p<=14;p+=2){ const y=PY(p);
      if(p) API.mk('line',{x1:X0,y1:y,x2:604,y2:y,stroke:'#E1E6EC','stroke-width':1.2},base);
      API.texText(base,X0-10,y+6,String(p),{size:18,anchor:'end',fill:API.COL.muted}); }
    API.mk('line',{x1:X0,y1:PY(7),x2:604,y2:PY(7),stroke:API.COL.grav,'stroke-width':2,'stroke-dasharray':'7 5'},base);
    API.texText(base,604,PY(7)-8,'\\text{중성}',{size:18,anchor:'end',fill:API.COL.grav});
    API.mk('line',{x1:X0,y1:Y0,x2:606,y2:Y0,stroke:API.COL.ink,'stroke-width':2},base);
    API.mk('line',{x1:X0,y1:Y0,x2:X0,y2:TOP-12,stroke:API.COL.ink,'stroke-width':2},base);
    API.texText(base,X0+8,TOP-11,'\\text{pH}',{size:19,anchor:'start',fill:API.COL.ink});
    for(let k=0;k<N;k++){ API.mk('line',{x1:CX(k),y1:Y0,x2:CX(k),y2:Y0+5,stroke:API.COL.ink,'stroke-width':1.5},base);
      if(k%2===0) API.texText(base,CX(k),Y0+26,`10^{-${k+1}}`,{size:18,anchor:'middle',fill:API.COL.ink}); }
    API.texText(base,610,Y0+52,'\\text{몰농도}\\ [\\text{M}]',{size:19,anchor:'end',fill:API.COL.ink});
    // 비커 줄
    const hi=API.mk('rect',{y:BB-BH-14,width:BW+16,height:BH+40,rx:8,fill:'#FFF8D6'},base);
    const liqs=[];
    for(let i=0;i<N;i++){ const x=BX(i);
      liqs.push(API.mk('rect',{x:x+1.5,width:BW-3,fill:'#DDEEF8'},base));
      API.mk('path',{d:`M${x-4},${BB-BH-3} L${x},${BB-BH+4} L${x},${BB} L${x+BW},${BB} L${x+BW},${BB-BH+4} L${x+BW+4},${BB-BH-3}`,fill:'none',stroke:'#7E8B98','stroke-width':2.2,'stroke-linejoin':'round'},base);
      API.texText(base,x+BW/2,BB+22,`\\text{${L[i]}}`,{size:19,anchor:'middle',fill:API.COL.ink}); }
    // 측정기 전극·표시창, 피펫, 막대
    const prb=API.mk('g',{},svg);
    API.mk('rect',{x:-40,y:2,width:80,height:30,rx:6,fill:'#E3F2E9',stroke:API.COL.ink,'stroke-width':1.5},prb);
    API.mk('rect',{x:-4,y:32,width:8,height:62,rx:3,fill:'#C9D3DD',stroke:API.COL.ink,'stroke-width':1.2},prb);
    API.mk('ellipse',{cx:0,cy:98,rx:6,ry:8,fill:'#F4F9FD',stroke:API.COL.ink,'stroke-width':1.2},prb);
    const pip=API.mk('g',{},svg);
    API.mk('rect',{x:-3,y:0,width:6,height:46,rx:2,fill:'#F4F9FD',stroke:'#7E8B98','stroke-width':1.6},pip);
    API.mk('rect',{x:-6,y:-12,width:12,height:14,rx:5,fill:'#D94A6A',stroke:'#8E2A3E','stroke-width':1.2},pip);
    const barsG=API.mk('g',{},svg), thG=API.mk('g',{},svg);
    let st={s:'a',k:0,made:1,th:false}, rec=[], anim=null;   // rec: {s,k,m,t,bar,h}
    function liqLevel(i,f){ const h=(BH-18)*f; liqs[i].setAttribute('y',BB-h); liqs[i].setAttribute('height',Math.max(0,h-1.5)); }
    function drawBeakers(){ for(let i=0;i<N;i++) liqLevel(i, i<st.made? (anim&&i===anim.to? anim.f:1) : 0);
      hi.setAttribute('x',BX(st.k)-8); }
    function probe(){ const x=BX(st.k)+BW/2, r=rec.find(q=>q.s===st.s&&q.k===st.k);
      prb.setAttribute('transform',`translate(${x},0)`); prb.style.display=anim?'none':'';
      Ov('disp').textContent = r? `pH ${r.m.toFixed(2)}` : 'pH –'; API.place(Ov('disp'),x,6,!anim); }
    const conc=k=>`1\\times10^{-${k+1}}`;
    function graph(){ thG.innerHTML='';
      rec.forEach(r=>{ const off=r.s==='a'?-10:10, x=CX(r.k)+off;
        r.bar.setAttribute('x',x-9); r.bar.setAttribute('y',PY(r.h)); r.bar.setAttribute('height',Math.max(0,r.h*S));
        if(st.th){ API.mk('circle',{cx:x,cy:PY(r.t),r:5.5,fill:'#fff',stroke:API.COL.ink,'stroke-width':2},thG); } });
      if(st.th) ['a','b'].forEach(s=>{ const pts=rec.filter(r=>r.s===s).sort((p,q)=>p.k-q.k).map(r=>`${CX(r.k)+(s==='a'?-10:10)},${PY(r.t)}`);
        if(pts.length>1) API.mk('polyline',{points:pts.join(' '),fill:'none',stroke:API.COL.ink,'stroke-width':1.6,'stroke-dasharray':'5 4'},thG); }); }
    function table(){ const tb=O('log'); tb.innerHTML='';
      rec.slice(-6).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${L[r.k]}</td><td style="color:${COLS[r.s]}">${r.s==='a'?'염산':API.tex('\\ce{NaOH}')}</td><td>${API.tex(conc(r.k))}</td><td><b>${r.m.toFixed(2)}</b></td><td>${st.th? r.t.toFixed(2):'—'}</td>`; tb.appendChild(tr); }); }
    function out(){ root.querySelector('[data-v="cur"]').innerHTML=`${L[st.k]} · ${API.tex(conc(st.k)+'\\ \\text{M}')}`;
      const r=rec.find(q=>q.s===st.s&&q.k===st.k); O('pH').textContent = r? r.m.toFixed(2) : '—';
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===st.s));
      $('[data-act="dil"]').disabled = st.k>=N-1 || !!anim; $('[data-act="th"]').classList.toggle('on',st.th); }
    function all(){ drawBeakers(); probe(); graph(); table(); out(); }
    function interp(r){ const prev=rec.filter(q=>q.s===r.s&&q.k===r.k-1)[0], up=r.s==='a';
      let m = `비커 ${L[r.k]}(${NAME[r.s]}): 측정 pH ${r.m.toFixed(2)}.`;
      if(prev){ const d=r.m-prev.m; m+=` 앞 용액보다 10배 묽다 → pH가 ${Math.abs(d).toFixed(2)} ${d>0?'커졌다':'작아졌다'}.`; }
      if(r.k>=5) m+=` 아주 묽어져 물의 자동 이온화로 생기는 ${up?'수소 이온':'수산화 이온'}을 무시할 수 없다 → pH가 7에 다가가고 7을 ${up?'넘지':'밑돌지'} 않는다.`;
      else if(prev) m+=` 10배 희석마다 pH가 약 1씩 ${up?'커진다':'작아진다'}.`;
      return m; }
    function intro(){ O('msg').textContent='「pH 측정」으로 비커 A의 pH를 재고, 「10배 희석 ▶」으로 다음 비커를 만들어 또 재자. 기록은 표와 막대그래프에 쌓인다.'; }
    $('[data-act="dil"]').addEventListener('click',()=>{ if(st.k>=N-1||anim) return;
      const from=st.k; st.k++; st.made=Math.max(st.made,st.k+1);
      O('msg').textContent=`비커 ${L[from]}에서 1 mL를 덜어 10 mL 부피 플라스크에서 묽혀 비커 ${L[st.k]}에 넣었다 → 몰농도는 비커 ${L[from]}의 10분의 1. 「pH 측정」을 누르자.`;
      anim = window.__STILL? null : {from,to:st.k,t:0,f:0}; all(); });
    $('[data-act="meas"]').addEventListener('click',()=>{ if(anim) return;
      if(rec.find(q=>q.s===st.s&&q.k===st.k)){ O('msg').textContent=`비커 ${L[st.k]}는 이미 기록했다. 「10배 희석 ▶」으로 다음 비커를 만들자.`; return; }
      const r={s:st.s,k:st.k,m:msPH(st.s,st.k),t:thPH(st.s,st.k),h:window.__STILL?msPH(st.s,st.k):0};
      r.bar=API.mk('rect',{width:18,fill:COLS[st.s],opacity:.85},barsG); rec.push(r);
      O('msg').textContent=interp(r); all(); });
    $('[data-act="th"]').addEventListener('click',()=>{ st.th=!st.th; all();
      if(st.th&&rec.length) O('msg').textContent='빈 원 = 이론 pH. 측정값과 이론값의 차이는 0.1보다 작다 — 희석·측정 오차 수준.'; });
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ if(anim) return; st.s=b.dataset.s; st.k=0; st.made=1; all();
      O('msg').textContent=`0.1 M ${st.s==='a'?'염산':'수산화 나트륨 수용액'}으로 바꾸었다. 비커 A부터 다시 측정하자. 앞의 기록은 비교를 위해 남겨 둔다.`; }));
    $('[data-act="reset"]').addEventListener('click',()=>{ rec.forEach(r=>r.bar.remove()); rec=[]; anim=null; st={s:'a',k:0,made:1,th:false}; all(); intro(); });
    API.loop(root,dt=>{
      let busy=false;
      if(anim){ busy=true; anim.t+=dt/1.3; const t=Math.min(1,anim.t);
        const a=Math.min(1,t/0.6), x=BX(anim.from)+BW/2+(BX(anim.to)-BX(anim.from))*a, y=40-Math.sin(Math.PI*a)*30;
        pip.setAttribute('transform',`translate(${x},${y})`); pip.style.display='';
        anim.f = t<0.6? 0 : (t-0.6)/0.4; liqLevel(anim.to,anim.f);
        if(t>=1){ anim=null; pip.style.display='none'; all(); } }
      rec.forEach(r=>{ if(Math.abs(r.h-r.m)>.005){ busy=true; r.h+=(r.m-r.h)*Math.min(1,dt*5); } });
      if(busy) graph();
    });
    pip.style.display='none'; all(); intro(); API.ready(()=>all());
  }
};
