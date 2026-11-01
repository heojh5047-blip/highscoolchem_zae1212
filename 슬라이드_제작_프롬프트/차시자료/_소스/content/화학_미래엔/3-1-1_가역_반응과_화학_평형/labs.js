/* 3-1-1 가역 반응과 화학 평형 — 실험실
   cm311eq    : 평형에 도달하기 (2NO2 ⇌ N2O4 입자 상자). N 원자 수 보존(n + 2m 일정).
                정반응 확률 = kf·n(n−1)/2·dt (가까운 NO2 두 개가 결합), 역반응 = kr·m·dt (N2O4가 둘로 갈라짐).
                kr/kf = 10 → NO2 60개로 시작하면 평형 근처 NO2 약 20, N2O4 약 20. 고정 시드 난수.
                출력: 상자(미시) + 상자 색(거시, NO2 수에 비례) + 분자 수–시간, 반응 속도–시간(2 s 이동 평균),
                누적 반응 횟수, 판정 문장, 측정 기록 표(최근 4행).
   cm311water : 물 옮기기 동적 평형 모형. 관에 담기는 물 = V × (d/D)², D = 25 mm, 두 방향 동시에.
                읽은 값 ±0.2 mL 오차(고정 시드). 표 누적(최근 5행), 부피–횟수 그래프. */
window.DECK_LABS = {
  cm311eq(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('svg');
    const BX0=12, BY0=12, BX1=300, BY1=262, R=9;
    const G1={x0:372,y0:185,x1:628,y1:30}, G2={x0:372,y0:400,x1:628,y1:245}, TW=40;
    const KF=0.012, KR=0.12, SPEED=46;
    let seed=7; const rnd=()=>{ seed=(seed*1103515245+12345)%2147483648; return seed/2147483648; };
    const tint=API.mk('rect',{x:BX0,y:BY0,width:BX1-BX0,height:BY1-BY0,rx:14,fill:'#B5562A','fill-opacity':0},svg);
    API.mk('rect',{x:BX0,y:BY0,width:BX1-BX0,height:BY1-BY0,rx:14,fill:'none',stroke:'#7E8B98','stroke-width':3},svg);
    const molG=API.mk('g',{},svg), fx=API.mk('g',{},svg), gr=API.mk('g',{},svg);
    let mols=[], t=0, run=false, ev=[], totF=0, totR=0, hist=[], log=[], flashes=[];
    function mkMol(type,x,y){
      const g=API.mk('g',{},molG), m={type,x,y,a:rnd()*360,va:(rnd()-.5)*120,g};
      const ang=rnd()*Math.PI*2; m.vx=Math.cos(ang)*SPEED; m.vy=Math.sin(ang)*SPEED;
      const d=1.35*R;
      if(type==='a'){ [-67,67].forEach(s=>{ const q=(-90+s)*Math.PI/180; API.atom(g,d*Math.cos(q),d*Math.sin(q),R,'O','-'); }); API.atom(g,0,0,R,'N','-'); }
      else { const dn=1.45*R; [-1,1].forEach(sd=>{ const nx=sd*dn/2, base=sd>0?0:180; [-62,62].forEach(s=>{ const q=(base+s)*Math.PI/180; API.atom(g,nx+d*Math.cos(q),d*Math.sin(q),R,'O','-'); }); });
        [-1,1].forEach(sd=>API.atom(g,sd*dn/2,0,R,'N','-')); }
      mols.push(m); return m;
    }
    function pos(m){ m.g.setAttribute('transform',`translate(${m.x.toFixed(1)},${m.y.toFixed(1)}) rotate(${m.a.toFixed(0)})`); }
    const cnt=()=>{ let a=0,b=0; mols.forEach(m=>m.type==='a'?a++:b++); return [a,b]; };
    function reset(){
      run=false; t=0; ev=[]; totF=0; totR=0; hist=[]; seed=7;
      mols.forEach(m=>m.g.remove()); mols=[]; while(fx.firstChild) fx.removeChild(fx.firstChild);
      const a0=+I('a0').value, b0=+I('b0').value;
      O('a0').textContent=a0+'개'; O('b0').textContent=b0+'개';
      for(let i=0;i<a0;i++) mkMol('a',BX0+24+rnd()*(BX1-BX0-48),BY0+24+rnd()*(BY1-BY0-48));
      for(let i=0;i<b0;i++) mkMol('b',BX0+28+rnd()*(BX1-BX0-56),BY0+28+rnd()*(BY1-BY0-56));
      mols.forEach(pos); hist.push([0,a0,b0]);
      root.querySelector('[data-act="run"]').textContent='시작';
      update();
    }
    function step(dt){
      t+=dt;
      mols.forEach(m=>{ m.x+=m.vx*dt; m.y+=m.vy*dt; m.a+=m.va*dt;
        const r=m.type==='a'?18:24;
        if(m.x<BX0+r){m.x=BX0+r;m.vx=Math.abs(m.vx);} if(m.x>BX1-r){m.x=BX1-r;m.vx=-Math.abs(m.vx);}
        if(m.y<BY0+r){m.y=BY0+r;m.vy=Math.abs(m.vy);} if(m.y>BY1-r){m.y=BY1-r;m.vy=-Math.abs(m.vy);} });
      let [n,mm]=cnt();
      // 정반응
      let pf=KF*n*(n-1)/2*dt;
      while(pf>0){ if(rnd()<Math.min(pf,1)){ const A=mols.filter(q=>q.type==='a'); if(A.length<2) break;
          const p=A[Math.floor(rnd()*A.length)]; let best=null,bd=1e9; A.forEach(q=>{ if(q!==p){ const d=Math.hypot(q.x-p.x,q.y-p.y); if(d<bd){bd=d;best=q;} } });
          const x=(p.x+best.x)/2, y=(p.y+best.y)/2; [p,best].forEach(q=>{ q.g.remove(); mols.splice(mols.indexOf(q),1); });
          const nm=mkMol('b',x,y); pos(nm); ev.push([t,1]); totF++; flash(x,y); }
        pf-=1; }
      // 역반응
      let pr=KR*mm*dt;
      while(pr>0){ if(rnd()<Math.min(pr,1)){ const B=mols.filter(q=>q.type==='b'); if(!B.length) break;
          const p=B[Math.floor(rnd()*B.length)]; p.g.remove(); mols.splice(mols.indexOf(p),1);
          const a1=mkMol('a',p.x-10,p.y), a2=mkMol('a',p.x+10,p.y); a2.vx=-a1.vx; a2.vy=-a1.vy; pos(a1); pos(a2); ev.push([t,-1]); totR++; flash(p.x,p.y); }
        pr-=1; }
      mols.forEach(pos);
      const [a,b]=cnt(); if(!hist.length||t-hist[hist.length-1][0]>=0.25) hist.push([t,a,b]);
      ev=ev.filter(e=>e[0]>t-2);
      flashes=flashes.filter(f=>{ f.life-=dt; if(f.life<=0){ f.el.remove(); return false; } f.el.setAttribute('opacity',(f.life/0.4).toFixed(2)); return true; });
      if(t>=TW){ run=false; root.querySelector('[data-act="run"]').textContent='시작'; }
    }
    function flash(x,y){ const el=API.mk('circle',{cx:x,cy:y,r:16,fill:'#FFE45C','fill-opacity':.6},fx); flashes.push({el,life:.4}); }
    function rates(){ const f=ev.filter(e=>e[1]>0).length, r=ev.length-f, w=Math.min(2,Math.max(t,0.001)); return [f/w,r/w]; }
    function rateHist(){ const out=[]; for(let i=0;i<hist.length;i++){ const [tt,a,b]=hist[i]; out.push([tt,KF*a*(a-1)/2,KR*b]); } return out; }
    function eqState(){
      if(t<6) return null; const rec=hist.filter(h=>h[0]>=t-4); if(rec.length<4) return null;
      const as=rec.map(h=>h[1]), mean=as.reduce((s,v)=>s+v,0)/as.length; const tot=as[0]+2*rec[0][2];
      const first=hist.filter(h=>h[0]>=t-8&&h[0]<t-4).map(h=>h[1]); if(first.length<3) return null;
      const m0=first.reduce((s,v)=>s+v,0)/first.length;
      if(Math.abs(mean-m0)<=Math.max(1.5,tot*0.04)) return [mean,rec.map(h=>h[2]).reduce((s,v)=>s+v,0)/rec.length];
      return null;
    }
    function drawGraphs(){
      while(gr.firstChild) gr.removeChild(gr.firstChild);
      [G1,G2].forEach(G=>{ API.arrow(gr,G.x0,G.y0,G.x1+6,G.y0,'#16233D',2); API.arrow(gr,G.x0,G.y0,G.x0,G.y1-12,'#16233D',2);
        [10,20,30,40].forEach(s=>{ const x=G.x0+(G.x1-G.x0)*s/TW; API.mk('line',{x1:x,y1:G.y0,x2:x,y2:G.y0+5,stroke:'#16233D','stroke-width':1.5},gr); }); });
      const [a0,b0]=[hist[0][1],hist[0][2]], maxN=Math.max(20,a0+2*b0);
      const X=(G,tt)=>G.x0+(G.x1-G.x0)*tt/TW;
      const Y1=v=>G1.y0-(G1.y0-G1.y1)*v/maxN;
      const pl=(pts,col,dash,G)=>{ if(pts.length<2) return; API.mk('path',{d:'M'+pts.map(p=>X(G,p[0]).toFixed(1)+' '+p[1].toFixed(1)).join(' L'),fill:'none',stroke:col,'stroke-width':3,'stroke-dasharray':dash||'none'},gr); };
      pl(hist.map(h=>[h[0],Y1(h[1])]),'#B5562A',null,G1); pl(hist.map(h=>[h[0],Y1(h[2])]),'#16233D','9 5',G1);
      const rh=rateHist(), maxR=Math.max(2,...rh.map(r=>Math.max(r[1],r[2])));
      const Y2=v=>G2.y0-(G2.y0-G2.y1)*v/maxR;
      pl(rh.map(h=>[h[0],Y2(h[1])]),'#2E9E6A',null,G2); pl(rh.map(h=>[h[0],Y2(h[2])]),'#7B4FC8','9 5',G2);
      const eq=eqState();
      if(eq){ const x=X(G1,Math.max(0,t-4)); [G1,G2].forEach(G=>API.mk('rect',{x,y:G.y1,width:Math.max(0,X(G,t)-x),height:G.y0-G.y1,fill:'#FFE45C','fill-opacity':.25},gr)); }
      const last=hist[hist.length-1], lr=rh[rh.length-1];
      API.place(Ov('la'),Math.min(X(G1,last[0])+22,612),Y1(last[1])-24); API.place(Ov('lb'),Math.min(X(G1,last[0])+26,606),Y1(last[2])+2);
      API.place(Ov('lf'),Math.min(X(G2,lr[0])+30,598),Y2(lr[1])-26); API.place(Ov('lr'),Math.min(X(G2,lr[0])+30,598),Y2(lr[2])+4);
      return eq;
    }
    function update(){
      const [a,b]=cnt(), tot=hist.length?hist[0][1]+2*hist[0][2]:1;
      tint.setAttribute('fill-opacity',(0.55*a/Math.max(40,tot)).toFixed(3));
      O('cnt').textContent=`${a}개 · ${b}개`; O('tot').textContent=`${totF}회 · ${totR}회`;
      const eq=drawGraphs(), [rf,rr]=rates();
      let msg;
      if(a+b===0) msg='분자를 넣어 주자.';
      else if(t===0) msg='「시작」을 눌러 분자 수와 색의 변화를 관찰하자.';
      else if(eq) msg='평형 상태: 분자 수와 색은 일정하지만, 정반응과 역반응은 같은 빠르기로 계속 일어난다(누적 횟수가 계속 는다).';
      else if(rf>rr) msg='정반응이 더 빠르다 → 이산화 질소가 줄고 색이 옅어진다.';
      else msg='역반응이 더 빠르다 → 이산화 질소가 늘고 색이 진해진다.';
      O('msg').textContent=msg;
    }
    root.querySelector('[data-act="run"]').addEventListener('click',e=>{ if(cnt()[0]+cnt()[1]===0) return; if(t>=TW) reset(); run=!run; e.currentTarget.textContent=run?'일시 정지':'시작'; });
    root.querySelector('[data-act="reset"]').addEventListener('click',reset);
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{
      const eq=eqState(), [a,b]=cnt();
      log.push({s:`${hist[0][1]} · ${hist[0][2]}`, e: eq? `${Math.round(eq[0])} · ${Math.round(eq[1])}` : `${a} · ${b} (평형 전)`, t:t.toFixed(1)+' s'});
      if(log.length>4) log.shift();
      const tb=O('log'); tb.innerHTML=''; log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${r.s}</td><td>${r.e}</td><td>${r.t}</td>`; tb.appendChild(tr); });
    });
    ['a0','b0'].forEach(k=>I(k).addEventListener('input',reset));
    API.place(Ov('t1'),G1.x0+44,2); API.place(Ov('t2'),G2.x0+76,217);
    API.place(Ov('tx'),G1.x1-20,G1.y0+8); API.place(Ov('tx2'),G2.x1-20,G2.y0+8); API.place(Ov('leg'),(BX0+BX1)/2,BY1+12);
    reset();
    // 정지 모드(캡처·인쇄)에서는 미리 20 s를 계산해 보여 준다
    if(window.__STILL){ for(let i=0;i<400;i++) step(0.05); update(); }
    let acc=0;
    API.loop(root,dt=>{ if(!run) return; step(dt); acc+=dt; if(acc>0.1){ acc=0; update(); } });
    root.__test={step:(s)=>{ for(let i=0;i<s*20;i++) step(0.05); update(); }, cnt, get t(){return t;}, eqState};
  },

  cm311water(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('svg'), g=API.mk('g',{},svg), D=25, TOT=50, NMAX=30;
    let start='A', VA=50, VB=0, n=0, hist=[], log=[], last=[0,0], seed=3, anim=0;
    const rnd=()=>{ seed=(seed*1103515245+12345)%2147483648; return seed/2147483648; };
    const read=v=>Math.max(0,Math.min(TOT,v+(rnd()-.5)*0.4));
    function reset(){ VA=start==='A'?TOT:0; VB=TOT-VA; n=0; last=[0,0]; seed=3; log=[]; hist=[[0,VA,VB]]; renderLog(); draw(); }
    function once(){ if(n>=NMAX) return; const fa=(+I('da').value/D)**2, fb=(+I('db').value/D)**2;
      const a=fa*VA, b=fb*VB; VA=VA-a+b; VB=VB+a-b; n++; last=[a,b];
      const ra=read(VA); hist.push([n,ra,TOT-ra]); log.push([n,ra,TOT-ra,a,b]); if(log.length>5) log.shift(); anim=1; }
    function renderLog(){ const tb=O('log'); tb.innerHTML=''; log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${r[0]}</td><td>${r[1].toFixed(1)}</td><td>${r[2].toFixed(1)}</td><td>${r[3].toFixed(1)}</td><td>${r[4].toFixed(1)}</td>`; tb.appendChild(tr); }); }
    function cyl(x,v,y0,h,w){
      API.mk('rect',{x:x-w/2-10,y:y0+h,width:w+20,height:8,rx:3,fill:'#C9D3DD',stroke:'#7E8B98','stroke-width':2},g);
      const wh=h*v/100; if(v>0) API.mk('rect',{x:x-w/2+2,y:y0+h-wh,width:w-4,height:wh,fill:'#BFDDF2'},g);
      API.mk('path',{d:`M${x-w/2} ${y0} V${y0+h} H${x+w/2} V${y0}`,fill:'none',stroke:'#7E8B98','stroke-width':2.5},g);
      for(let k=1;k<10;k++){ const yy=y0+h-h*k/10; API.mk('line',{x1:x+w/2-(k%5?8:14),y1:yy,x2:x+w/2,y2:yy,stroke:'#5B6B7F','stroke-width':1.2},g); }
    }
    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      const da=+I('da').value, db=+I('db').value; O('da').textContent=da+' mm'; O('db').textContent=db+' mm';
      const y0=40,h=220;
      cyl(70,VA*2,y0,h,52); cyl(190,VB*2,y0,h,52);
      // 관 (두께 = 지름에 비례)
      const ta=da*1.3, tb=db*1.3, lift=anim*30;
      API.mk('rect',{x:70-ta/2,y:y0-14-lift,width:ta,height:h+10,fill:'#FFFFFF','fill-opacity':.45,stroke:'#16233D','stroke-width':1.5},g);
      API.mk('rect',{x:190-tb/2,y:y0-14-lift,width:tb,height:h+10,fill:'#FFFFFF','fill-opacity':.45,stroke:'#16233D','stroke-width':1.5},g);
      API.arrow(g,88,10,172,10,'#2E9E6A',3); API.arrow(g,172,28,88,28,'#7B4FC8',3);
      API.place(Ov('ca'),70,y0+h+10); API.place(Ov('cb'),190,y0+h+10);
      // 그래프
      const X0=300,Y0=258,X1=618,Y1=24, Xn=k=>X0+(X1-X0)*k/NMAX, Yv=v=>Y0-(Y0-Y1)*v/TOT;
      API.arrow(g,X0,Y0,X1+8,Y0,'#16233D',2); API.arrow(g,X0,Y0,X0,Y1-10,'#16233D',2);
      [10,20,30,40,50].forEach(v=>API.mk('line',{x1:X0-5,y1:Yv(v),x2:X0,y2:Yv(v),stroke:'#16233D','stroke-width':1.5},g));
      [10,20,30].forEach(k=>API.mk('line',{x1:Xn(k),y1:Y0,x2:Xn(k),y2:Y0+5,stroke:'#16233D','stroke-width':1.5},g));
      const pl=(i,col,dash)=>{ API.mk('path',{d:'M'+hist.map(p=>Xn(p[0]).toFixed(1)+' '+Yv(p[i]).toFixed(1)).join(' L'),fill:'none',stroke:col,'stroke-width':3,'stroke-dasharray':dash||'none'},g);
        hist.forEach(p=>API.mk('circle',{cx:Xn(p[0]),cy:Yv(p[i]),r:3.5,fill:col},g)); };
      pl(1,'#16233D'); pl(2,'#0E7490','9 5');
      const L=hist[hist.length-1];
      API.place(Ov('la'),Math.min(Xn(L[0])+14,610),Yv(L[1])-(L[1]>L[2]?26:-2)); API.place(Ov('lb'),Math.min(Xn(L[0])+14,610),Yv(L[2])-(L[2]>=L[1]?26:-2));
      API.place(Ov('ya'),X0+40,0); API.place(Ov('xa'),X1-30,Y0+10);
      O('n').textContent=n+'회'; O('v').textContent=`${L[1].toFixed(1)} mL · ${L[2].toFixed(1)} mL`;
      O('mv').textContent=n?`${last[0].toFixed(1)} mL · ${last[1].toFixed(1)} mL`:'—';
      let msg;
      if(n===0) msg='「1회 옮기기」를 눌러 두 방향으로 동시에 물을 옮겨 보자.';
      else if(Math.abs(last[0]-last[1])<=0.3) msg='두 방향으로 옮기는 양이 거의 같다 → 부피는 일정하지만 옮기기는 계속된다(동적 평형 모형).';
      else if(last[0]>last[1]) msg='A → B로 옮기는 양이 더 많다 → A의 물이 줄고 B의 물이 는다.';
      else msg='B → A로 옮기는 양이 더 많다 → B의 물이 줄고 A의 물이 는다.';
      if(n>=NMAX) msg+=' (30회까지 기록)';
      O('msg').textContent=msg;
    }
    root.querySelector('[data-act="one"]').addEventListener('click',()=>{ once(); renderLog(); draw(); });
    root.querySelector('[data-act="five"]').addEventListener('click',()=>{ for(let i=0;i<5;i++) once(); renderLog(); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',reset);
    root.querySelectorAll('[data-st]').forEach(b=>b.addEventListener('click',()=>{ start=b.dataset.st; root.querySelectorAll('[data-st]').forEach(x=>x.classList.toggle('on',x===b)); reset(); }));
    ['da','db'].forEach(k=>I(k).addEventListener('input',reset));
    reset();
    if(window.__STILL){ for(let i=0;i<12;i++) once(); anim=0; renderLog(); draw(); }
    API.loop(root,dt=>{ if(anim>0){ anim=Math.max(0,anim-dt*2.5); draw(); } });
  }
};
