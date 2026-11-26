/* 1-M 대단원 Ⅰ 마무리 — 실험실
   em19dive : 과학 글쓰기 09 — 수심과 기체 조성에 따른 부분 압력
     · 전체 압력 P = 1 + d/10 (기압, 대기압 1 + 수압), 부분 압력 P_i = X_i P
     · 공기: X(O2) 0.21, X(N2) 0.78 (기타 0.01) — 슬라이더 잠금 / 트라이믹스: X(N2) = 1 − X(O2) − X(He)
     · 한계선: 산소 1.4 기압(plus), 산소 1 기압(equi 점선, 오래 노출), 질소 3.4 기압(bfield)
     · 「기록」 → 표 최대 5행, 「초기화」 → 공기 40 m */
window.DECK_LABS = {
  em19dive(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), iD=$('[data-i="d"]'), iO=$('[data-i="xo"]'), iH=$('[data-i="xh"]');
    let gas='air', log=[], cur=null;
    // ── 바다 단면 ──
    const SX0=70, SX1=190, SY0=34, M=3; // 1 m = 3 px, 80 m → y 274
    const sy=d=>SY0+M*d;
    const gs=API.mk('g',{},svg);
    const defs=API.mk('defs',{},gs), lg=API.mk('linearGradient',{id:'grad-em19-lab',x1:0,y1:0,x2:0,y2:1},defs);
    API.mk('stop',{offset:0,'stop-color':'#DDEEF8'},lg); API.mk('stop',{offset:1,'stop-color':'#7FA9CC'},lg);
    API.mk('rect',{x:SX0,y:SY0,width:SX1-SX0,height:M*80,fill:'url(#grad-em19-lab)'},gs);
    API.mk('path',{d:`M${SX0} ${SY0} Q${SX0+15} ${SY0-7} ${SX0+30} ${SY0} T${SX0+60} ${SY0} T${SX0+90} ${SY0} T${SX1} ${SY0}`,fill:'none',stroke:'#5B8FBF','stroke-width':2.5},gs);
    [0,20,40,60,80].forEach(d=>{ API.mk('line',{x1:SX0-6,y1:sy(d),x2:SX0,y2:sy(d),stroke:'#5B6B7F','stroke-width':1.5},gs);
      API.texText(svg,SX0-10,sy(d)+(d===80?-2:7),d+' m',{size:18,anchor:'end',mix:true}); });
    API.texText(svg,SX0-10,20,'수심',{size:18,anchor:'end',fill:'#5B6B7F',mix:true});
    const diver=API.mk('g',{},svg);
    API.mk('path',{d:'M-24 0 L-40 -9 L-40 9 Z',fill:'#16233D'},diver);
    API.mk('ellipse',{cx:0,cy:0,rx:25,ry:8,fill:'#1F6FD1'},diver);
    API.mk('rect',{x:-16,y:-17,width:26,height:9,rx:4,fill:'#E08A2C'},diver);
    API.mk('circle',{cx:29,cy:-2,r:8.5,fill:'#FFD9B3',stroke:'#16233D','stroke-width':2},diver);
    const bub=[0,.33,.66].map(ph=>({ph,c:API.mk('circle',{cx:0,cy:0,r:4,fill:'#FFFFFF','fill-opacity':.85,stroke:'#7FB6D9','stroke-width':1.6},svg)}));
    let dy=sy(40);
    // ── 부분 압력 막대 ──
    const AX=262, Y0=262, YT=30, PMAX=9, py=p=>Y0-(Y0-YT)*p/PMAX;
    const ga=API.mk('g',{},svg);
    [0,3,6,9].forEach(v=>{ API.mk('line',{x1:AX-6,y1:py(v),x2:AX,y2:py(v),stroke:'#5B6B7F','stroke-width':1.5},ga);
      if(v) API.mk('line',{x1:AX,y1:py(v),x2:620,y2:py(v),stroke:'#E2E7EC','stroke-width':1.5},ga);
      API.texText(svg,AX-10,py(v)+7,String(v),{size:18,anchor:'end',mix:true}); });
    API.mk('line',{x1:AX,y1:Y0,x2:620,y2:Y0,stroke:'#5B6B7F','stroke-width':2},ga);
    API.mk('line',{x1:AX,y1:Y0,x2:AX,y2:YT-8,stroke:'#5B6B7F','stroke-width':2},ga);
    API.texText(svg,AX+8,18,'부분 압력 $P$ [atm]',{size:18,anchor:'start',fill:'#5B6B7F',mix:true});
    const BARS=[{k:'o',x:290,f:'#F6B9AE',s:'#E5533D',tex:'$\\ce{O2}$'},{k:'n',x:410,f:'#C9D2F4',s:'#4F6BD8',tex:'$\\ce{N2}$'},{k:'h',x:530,f:'#F3E3B5',s:'#C99A2E',tex:'$\\ce{He}$'}];
    const gb=API.mk('g',{},svg);
    BARS.forEach(b=>{ b.r=API.mk('rect',{x:b.x,y:Y0,width:70,height:0,fill:b.f,stroke:b.s,'stroke-width':2.5},gb);
      API.texText(svg,b.x+35,288,b.tex,{size:19,anchor:'middle',mix:true}); });
    const tot=API.mk('line',{x1:AX,y1:Y0,x2:600,y2:Y0,stroke:'#5B6B7F','stroke-width':2,'stroke-dasharray':'8 6'},svg);
    const totL=API.mk('text',{x:604,y:Y0,'font-size':18,fill:'#5B6B7F','font-weight':700},svg); totL.textContent='전체';
    const lim=API.mk('g',{},svg);
    API.mk('line',{x1:284,y1:py(1.4),x2:366,y2:py(1.4),stroke:'#D7263D','stroke-width':3},lim);
    API.mk('line',{x1:284,y1:py(1),x2:366,y2:py(1),stroke:'#E08A2C','stroke-width':3,'stroke-dasharray':'7 5'},lim);
    API.mk('line',{x1:404,y1:py(3.4),x2:486,y2:py(3.4),stroke:'#7B4FC8','stroke-width':3},lim);
    API.texText(svg,369,py(1.4)-2,'1.4',{size:18,anchor:'start',fill:'#D7263D',mix:true});
    API.texText(svg,369,py(1)+16,'1',{size:18,anchor:'start',fill:'#E08A2C',mix:true});
    API.texText(svg,489,py(3.4)+6,'3.4',{size:18,anchor:'start',fill:'#7B4FC8',mix:true});
    // ── 계산 ──
    function fr(){
      if(gas==='air') return {o:.21,n:.78,h:0};
      let o=+iO.value, h=+iH.value; if(o+h>100){ h=100-o; iH.value=h; }
      return {o:o/100,h:h/100,n:(100-o-h)/100};
    }
    function judge(po,pn){
      const a=[]; if(pn>=3.4) a.push('마취 위험'); if(po>1.4) a.push('산소 독성'); else if(po>=1) a.push('폐 주의');
      return a.length?a.join(', '):'안전';
    }
    function draw(){
      const d=+iD.value, x=fr(), P=1+d/10, po=x.o*P, pn=x.n*P, ph=x.h*P;
      iO.disabled=iH.disabled=(gas==='air'); if(gas==='air'){ iO.value=21; iH.value=0; }
      O('d').textContent=d+' m'; O('xo').textContent=x.o.toFixed(2); O('xh').textContent=x.h.toFixed(2);
      O('xn').textContent=x.n.toFixed(2)+(gas==='air'?' (기타 0.01)':'');
      O('p').textContent=P.toFixed(1)+' 기압';
      [[BARS[0],po,'vo'],[BARS[1],pn,'vn'],[BARS[2],ph,'vh']].forEach(([b,v,k])=>{
        b.r.setAttribute('y',py(v).toFixed(1)); b.r.setAttribute('height',(Y0-py(v)).toFixed(1));
        const el=V(k); el.textContent=v.toFixed(2); API.place(el,b.x+35,py(v)-14,true); });
      tot.setAttribute('y1',py(P)); tot.setAttribute('y2',py(P)); totL.setAttribute('y',py(P)+6);
      const j=judge(po,pn); const m=[];
      if(pn>=3.4) m.push(`질소 ${pn.toFixed(2)} 기압 ≥ 3.4 — 질소 마취 위험`);
      if(po>1.4) m.push(`산소 ${po.toFixed(2)} 기압 > 1.4 — 산소 독성 위험`);
      else if(po>=1) m.push(`산소 ${po.toFixed(2)} 기압 ≥ 1 — 오래 머물면 폐 손상 주의`);
      O('msg').textContent=m.length?m.join(' / '):`산소 ${po.toFixed(2)}, 질소 ${pn.toFixed(2)} 기압 — 두 기체 모두 안전 범위`;
      cur={d,gas:gas==='air'?'공기':'트라이믹스',x,po,pn,j};
    }
    function drawLog(){ O('log').innerHTML=log.map(r=>`<tr><td>${r.d} m</td><td>${r.gas}</td><td>${r.x.o.toFixed(2)}</td><td>${r.x.n.toFixed(2)}</td><td>${r.x.h.toFixed(2)}</td><td>${r.po.toFixed(2)}</td><td>${r.pn.toFixed(2)}</td><td>${r.j}</td></tr>`).join(''); }
    function setGas(g){ gas=g; root.querySelectorAll('[data-gas]').forEach(b=>b.classList.toggle('em19-act',b.dataset.gas===g));
      if(g==='tri'&&+iH.value===0){ iO.value=17; iH.value=60; } draw(); }
    root.querySelectorAll('[data-gas]').forEach(b=>b.addEventListener('click',()=>setGas(b.dataset.gas)));
    [iD,iO,iH].forEach(i=>i.addEventListener('input',draw));
    $('[data-act="rec"]').addEventListener('click',()=>{ draw(); log.push(cur); if(log.length>5) log.shift(); drawLog(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; drawLog(); iD.value=40; iO.value=21; iH.value=0; setGas('air'); });
    API.onShow&&API.onShow(draw);
    draw(); drawLog();
    function place(t){ diver.setAttribute('transform',`translate(128,${dy.toFixed(1)})`);
      bub.forEach(b=>{ const p=((t||0)*0.5+b.ph)%1, yb=dy-14-(dy-14-SY0)*p; b.c.setAttribute('cx',(150+6*Math.sin(p*12)).toFixed(1)); b.c.setAttribute('cy',yb.toFixed(1)); b.c.setAttribute('opacity',dy>SY0+20?(1-p).toFixed(2):0); }); }
    dy=sy(+iD.value); place(0);
    API.loop(root,(dt,t)=>{ const ty=sy(+iD.value); dy+=(ty-dy)*Math.min(1,dt*3); place(t); });
  }
};
