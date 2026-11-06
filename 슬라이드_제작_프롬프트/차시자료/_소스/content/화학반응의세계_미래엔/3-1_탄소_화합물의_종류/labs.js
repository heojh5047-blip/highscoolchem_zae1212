/* 3-1 탄소 화합물의 종류 — 실험실
   rm31fg : 작용기와 성질 실험실 (필수 탐구 반03-탐1 「간단한 알코올, 알데하이드, 카복실산 분자를 화학식으로 표현하고 성질 탐구하기」)
     · 작용기(알케인/알코올/알데하이드/카복실산) × 탄소 수 1–6 → 이름, 분자식, 간단한 구조식, 구조식(그림), 끓는점, 25 °C 상태
     · 시험관: 물에 넣고 흔들기(용해성 → 층) → BTB 용액(액성 → 색) → 탄산수소 나트륨(카복실산이면 CO2 기포)
     · 「기록」→ 결과 표에 행(최근 5행)이 쌓이고, 끓는점–탄소 수 그래프에 계열별 점·선이 찍힌다. 「초기화」.
     · 자료 값(1 기압 끓는점 °C, 25 °C 물 100 g에 녹는 양 g): plan.md 0절 */
window.DECK_LABS = {
  rm31fg(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg'), fig=$('.lab-fig');
    const gS=API.mk('g',{},svg), gT=API.mk('g',{},svg), gB=API.mk('g',{},svg), gG=API.mk('g',{},svg);
    const INK='#16233D', MUT='#5B6B7F', EQ='#E08A2C';
    const BP={none:[-162,-89,-42,-0.5,36,69], OH:[65,78,97,118,138,157], CHO:[-19,20,49,75,103,131], COOH:[101,118,141,164,186,205]};
    // 물 100 g에 녹는 양(g), 999 = 섞임
    const SOL={none:[0,0,0,0,0,0], OH:[999,999,999,7.7,2.2,0.6], CHO:[999,999,31,7,1.2,0.6], COOH:[999,999,999,999,2.4,1.0]};
    const NAME={none:['메테인','에테인','프로페인','뷰테인','펜테인','헥세인'], OH:['메탄올','에탄올','1-프로판올','1-뷰탄올','1-펜탄올','1-헥산올'],
      CHO:['폼알데하이드','아세트알데하이드','프로판알','뷰탄알','펜탄알','헥산알'], COOH:['폼산','아세트산','프로판산','뷰탄산','펜탄산','헥산산']};
    const GRP={none:'',OH:'하이드록시기 −OH',CHO:'폼일기 −CHO',COOH:'카복실기 −COOH'};
    const SER={none:{c:'#8C99A6',m:'c',t:'알케인'},OH:{c:'#2E9E6A',m:'s',t:'알코올'},CHO:{c:'#7B4FC8',m:'t',t:'알데하이드'},COOH:{c:'#D7263D',m:'d',t:'카복실산'}};
    let st={f:'OH', water:false, btb:false, soda:false}, log=[], pts=[], bub=[];
    const pool=[];
    for(let i=0;i<24;i++){ const d=document.createElement('div'); d.className='ov mid'; d.style.fontSize='24px'; fig.appendChild(d); pool.push(d); }

    function mf(f,n){ // 분자식
      const sub=k=>k===1?'':k; let h, o=0;
      if(f==='none') h=2*n+2; else if(f==='OH'){ h=2*n+2; o=1; } else if(f==='CHO'){ h=2*n; o=1; } else { h=2*n; o=2; }
      return `C${sub(n)}H${h}`+(o?`O${sub(o)}`:'');
    }
    function cond(f,n){ // 시성식 (교과서 꼴: C2H5OH, CH3CHO, CH3COOH)
      const R=k=>k===0?'H':k===1?'CH3':`C${k}H${2*k+1}`;
      if(f==='none') return mf(f,n);
      if(f==='OH') return R(n)+'OH';
      return R(n-1)+(f==='CHO'?'CHO':'COOH');
    }
    function struct(f,n){ // 구조식 원자 좌표·결합
      const d=62, extra={none:1,OH:2,CHO:1,COOH:2}[f], w=d*(n+extra), x0=(620-w)/2, y0=128;
      const A=[], B=[]; let x=x0; A.push(['H',x,y0]); x+=d; const C=[];
      for(let k=0;k<n;k++){ A.push(['C',x,y0]); const ci=A.length-1; C.push(ci); B.push([k===0?ci-1:C[k-1],ci,1]);
        if(k===n-1&&(f==='CHO'||f==='COOH')){ A.push(['O',x,y0-d]); B.push([ci,A.length-1,2]); }
        else { A.push(['H',x,y0-d]); B.push([ci,A.length-1,1]); A.push(['H',x,y0+d]); B.push([ci,A.length-1,1]); }
        x+=d; }
      const ce=C[C.length-1]; let box=null;
      if(f==='none'){ A.push(['H',x,y0]); B.push([ce,A.length-1,1]); }
      else if(f==='OH'){ A.push(['O',x,y0]); const oi=A.length-1; B.push([ce,oi,1]); A.push(['H',x+d,y0]); B.push([oi,A.length-1,1]); box=[x-17,y0-17,d+34,34]; }
      else if(f==='CHO'){ A.push(['H',x,y0]); B.push([ce,A.length-1,1]); box=[x-d-17,y0-d-17,d+34,d+34]; }
      else { A.push(['O',x,y0]); const oi=A.length-1; B.push([ce,oi,1]); A.push(['H',x+d,y0]); B.push([oi,A.length-1,1]); box=[x-d-17,y0-d-17,2*d+34,d+34]; }
      return {A,B,box};
    }
    const solTxt=v=>v>=10?'잘 녹는다':v>=1?'조금 녹는다':'거의 녹지 않는다';
    const solShort=v=>v>=10?'잘 녹음':v>=1?'조금':'거의 X';

    function drawStruct(){
      while(gS.firstChild) gS.removeChild(gS.firstChild);
      const n=+I('n').value, f=st.f, s=struct(f,n);
      if(s.box) API.mk('rect',{x:s.box[0],y:s.box[1],width:s.box[2],height:s.box[3],rx:10,fill:EQ,'fill-opacity':.18,stroke:EQ,'stroke-width':1.5},gS);
      s.B.forEach(([i,j,o])=>{ const [,x1,y1]=s.A[i], [,x2,y2]=s.A[j], L=Math.hypot(x2-x1,y2-y1), ux=(x2-x1)/L, uy=(y2-y1)/L, px=-uy, py=ux;
        (o===1?[0]:[-3.5,3.5]).forEach(k=>API.mk('line',{x1:x1+ux*15+px*k,y1:y1+uy*15+py*k,x2:x2-ux*15+px*k,y2:y2-uy*15+py*k,stroke:INK,'stroke-width':3,'stroke-linecap':'round'},gS)); });
      pool.forEach((d,i)=>{ const a=s.A[i]; if(a){ if(d.dataset.el!==a[0]){ d.innerHTML=API.tex('\\mathrm{'+a[0]+'}'); d.dataset.el=a[0]; } API.place(d,a[1],a[2]); } else API.place(d,0,0,false); });
      const fg=Ov('fg'); if(s.box){ fg.textContent=GRP[f]; API.place(fg,s.box[0]+s.box[2]/2, f==='OH'? s.box[1]+s.box[3]+52 : s.box[1]+s.box[3]+52-62); } else API.place(fg,0,0,false);
      if(s.box && f!=='OH') API.place(fg,s.box[0]+s.box[2]/2, 128+62+22);
      if(f==='OH') API.place(fg,s.box[0]+s.box[2]/2, 128+30);
    }
    // 시험관
    const TX=100, TT=262, TH=200, TW=62, BOT=TT+TH;
    function tubePath(top){ return `M${TX-TW/2+3} ${top} L${TX-TW/2+3} ${BOT-TW/2} A${TW/2-3} ${TW/2-3} 0 0 0 ${TX+TW/2-3} ${BOT-TW/2} L${TX+TW/2-3} ${top} Z`; }
    function cur(){ const n=+I('n').value, f=st.f; return {n,f,bp:BP[f][n-1],sol:SOL[f][n-1],gas:BP[f][n-1]<25,acid:f==='COOH'}; }
    function drawTube(){
      while(gT.firstChild) gT.removeChild(gT.firstChild);
      const c=cur(), waterTop=BOT-110;
      const wcol = st.btb ? (c.acid? '#F2C230' : '#58B368') : '#DDEEF8';
      let msg='';
      if(!st.water){ API.mk('path',{d:tubePath(waterTop),fill:'#DDEEF8',stroke:'#9FC3DD','stroke-width':1.5},gT); msg='물 5 mL'; }
      else if(c.sol>=10){ API.mk('path',{d:tubePath(waterTop-22),fill:wcol,'fill-opacity':.85,stroke:'#9FC3DD','stroke-width':1.5},gT); msg='한 층 (섞임)'; }
      else if(c.gas){ API.mk('path',{d:tubePath(waterTop),fill:wcol,'fill-opacity':.85,stroke:'#9FC3DD','stroke-width':1.5},gT); msg='기체가 빠져나감'; }
      else { const th=c.sol>=1?12:24;
        API.mk('path',{d:tubePath(waterTop+ (c.sol>=1?10:0)),fill:wcol,'fill-opacity':.85,stroke:'#9FC3DD','stroke-width':1.5},gT);
        API.mk('rect',{x:TX-TW/2+3,y:waterTop+(c.sol>=1?10:0)-th,width:TW-6,height:th,fill:'#FFF3C9',stroke:'#C9A94A','stroke-width':1.5},gT);
        msg=c.sol>=1?'얇은 층이 남음':'두 층으로 나뉨'; }
      API.mk('path',{d:`M${TX-TW/2} ${TT} L${TX-TW/2} ${BOT-TW/2} A${TW/2} ${TW/2} 0 0 0 ${TX+TW/2} ${BOT-TW/2} L${TX+TW/2} ${TT}`,fill:'none',stroke:'#7E8B98','stroke-width':3},gT);
      const t=Ov('tube'); t.textContent=msg+(st.btb?(c.acid?' · 노랑':' · 초록'):''); API.place(t,TX,BOT+10);
      const g=Ov('gas'); if(st.soda){ g.textContent=c.acid?'기포: 이산화 탄소':'변화 없음'; API.place(g,TX,TT-34); } else API.place(g,0,0,false);
    }
    function drawBub(){
      while(gB.firstChild) gB.removeChild(gB.firstChild);
      bub.forEach(b=>API.mk('circle',{cx:b.x,cy:b.y,r:b.r,fill:'#fff','fill-opacity':.7,stroke:'#7E8B98','stroke-width':1.2},gB));
    }
    // 그래프
    const GX=300, GY=262, GW=300, GH=180, lo=-200, hi=250;
    const gx=n=>GX+(n-1)/5*GW, gy=v=>GY+(hi-v)/(hi-lo)*GH;
    const axisG=API.mk('g',{},svg);
    [-200,-100,0,100,200].forEach(v=>{ API.mk('line',{x1:GX,y1:gy(v),x2:GX+GW,y2:gy(v),stroke:'#E2E7EC','stroke-width':1.5},axisG); API.texText(axisG,GX-8,gy(v)+6,'$'+v+'$',{size:17,anchor:'end',fill:MUT,mix:true}); });
    [1,2,3,4,5,6].forEach(n=>API.texText(axisG,gx(n),GY+GH+22,'$'+n+'$',{size:17,anchor:'middle',fill:MUT,mix:true}));
    API.mk('line',{x1:GX,y1:GY-4,x2:GX,y2:GY+GH,stroke:MUT,'stroke-width':2},axisG);
    API.mk('line',{x1:GX,y1:GY+GH,x2:GX+GW,y2:GY+GH,stroke:MUT,'stroke-width':2},axisG);
    API.mk('line',{x1:GX,y1:gy(25),x2:GX+GW,y2:gy(25),stroke:EQ,'stroke-width':1.8,'stroke-dasharray':'6 5'},axisG);
    API.texText(axisG,GX+GW,gy(25)-6,'$25\\ {}^\\circ\\text{C}$',{size:17,anchor:'end',fill:EQ,mix:true});
    API.texText(axisG,GX-40,GY-14,'끓는점 [°C]',{size:18,anchor:'start',fill:MUT,mix:true});
    API.texText(axisG,GX+GW/2,GY+GH+46,'탄소 수',{size:18,anchor:'middle',fill:MUT,mix:true});
    ['none','OH','CHO','COOH'].forEach((f,i)=>{ const x=160, y=300+i*30; marker(axisG,x,y-6,f); API.texText(axisG,x+12,y,SER[f].t,{size:17,anchor:'start',fill:MUT,mix:true}); });
    function marker(g,x,y,f){ const c=SER[f].c, m=SER[f].m, r=6;
      if(m==='c') API.mk('circle',{cx:x,cy:y,r,fill:c},g);
      else if(m==='s') API.mk('rect',{x:x-r,y:y-r,width:2*r,height:2*r,fill:c},g);
      else if(m==='t') API.mk('polygon',{points:`${x},${y-r-1} ${x+r+1},${y+r} ${x-r-1},${y+r}`,fill:c},g);
      else API.mk('polygon',{points:`${x},${y-r-2} ${x+r+2},${y} ${x},${y+r+2} ${x-r-2},${y}`,fill:c},g); }
    function drawGraph(){
      while(gG.firstChild) gG.removeChild(gG.firstChild);
      ['none','OH','CHO','COOH'].forEach(f=>{ const p=pts.filter(q=>q.f===f).sort((a,b)=>a.n-b.n);
        if(p.length>1) API.mk('polyline',{points:p.map(q=>gx(q.n)+','+gy(q.v)).join(' '),fill:'none',stroke:SER[f].c,'stroke-width':2.5},gG);
        p.forEach(q=>marker(gG,gx(q.n),gy(q.v),f)); });
    }
    function update(reset){
      const c=cur();
      if(reset!==false){ st.water=false; st.btb=false; st.soda=false; bub=[]; }
      root.querySelectorAll('[data-f]').forEach(b=>b.classList.toggle('on',b.dataset.f===st.f));
      O('n').textContent=c.n+'개';
      O('name').textContent=NAME[c.f][c.n-1];
      $('[data-x="mf"]').innerHTML=API.tex('\\ce{'+mf(c.f,c.n)+'}')+' · '+API.tex('\\ce{'+cond(c.f,c.n)+'}');
      O('bp').textContent=(c.bp<0?'−'+Math.abs(c.bp):c.bp)+' °C · '+(c.gas?'기체':'액체');
      $('[data-act="btb"]').disabled=!st.water; $('[data-act="soda"]').disabled=!st.water;
      ['water','btb','soda'].forEach(k=>$(`[data-act="${k}"]`).classList.toggle('done',st[k]));
      let m='';
      if(!st.water) m='시료를 물에 넣고 흔들어 용해성부터 확인하자.';
      else {
        m='물에 '+solTxt(c.sol)+'. ';
        if(c.f==='none') m+='탄화수소는 물과 잘 섞이지 않는다.';
        else if(c.sol>=10) m+='작용기가 물 분자와 수소 결합한다.';
        else m+='탄화수소 부분이 커져 물에 덜 녹는다.';
        if(st.btb) m+= c.acid? ' BTB 노랑: −COOH가 H⁺를 내놓아 산성이다.' : ' BTB 초록: 중성이다.';
        if(st.soda) m+= c.acid? ' 이산화 탄소 기포가 생긴다.' : '';
      }
      if(st.btb && c.f!=='none' && c.n>1){ const lo2=BP.none[c.n-1]; if(c.f==='OH') m+=` 끓는점은 같은 탄소 수 알케인(${lo2<0?'−'+Math.abs(lo2):lo2} °C)보다 높다.`; if(c.f==='CHO') m+=` 끓는점은 같은 탄소 수 알코올(${BP.OH[c.n-1]} °C)보다 낮다.`; }
      O('msg').textContent=m;
      drawStruct(); drawTube(); drawBub(); drawGraph();
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${API.tex('\\ce{'+r.c+'}')}</td><td>${r.bp}</td><td>${r.sol}</td><td>${r.ac}</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-f]').forEach(b=>b.addEventListener('click',()=>{ st.f=b.dataset.f; update(); }));
    I('n').addEventListener('input',()=>update());
    $('[data-act="water"]').addEventListener('click',()=>{ st.water=true; update(false); });
    $('[data-act="btb"]').addEventListener('click',()=>{ if(!st.water) return; st.btb=true; update(false); });
    $('[data-act="soda"]').addEventListener('click',()=>{ if(!st.water) return; st.soda=true; update(false); });
    $('[data-act="rec"]').addEventListener('click',()=>{ const c=cur();
      if(!st.water||!st.btb){ O('msg').textContent='먼저 물에 넣고 BTB 용액으로 액성을 확인한 뒤 기록하자.'; return; }
      log.push({c:cond(c.f,c.n), bp:(c.bp<0?'−'+Math.abs(c.bp):c.bp)+' °C', sol:solShort(c.sol), ac:c.f==='none'?'—':c.acid?'산성':'중성'}); if(log.length>5) log.shift();
      pts=pts.filter(q=>!(q.f===c.f&&q.n===c.n)); pts.push({f:c.f,n:c.n,v:c.bp}); renderLog(); drawGraph(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; pts=[]; st.f='OH'; I('n').value=2; renderLog(); update(); });
    // 기포 (기체가 빠져나감 / 이산화 탄소)
    let seed=7; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    if(!window.__STILL) API.loop(root,dt=>{ const c=cur(), on=(st.water&&c.gas&&c.sol<10)||(st.soda&&c.acid);
      if(!on&&!bub.length) return;
      if(on && rnd()<dt*9) bub.push({x:TX-20+rnd()*40, y:BOT-14, r:2.5+rnd()*3});
      bub.forEach(b=>{ b.y-=dt*(55+b.r*8); }); bub=bub.filter(b=>b.y>TT+4); drawBub(); });
    API.ready(()=>{ pool.forEach(d=>{ d.dataset.el=''; }); update(false); });
    update();
  }
};
