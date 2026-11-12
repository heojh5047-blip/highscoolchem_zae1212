/* 2-2-3 분자 구조에 따른 물질의 성질 — 실험실
   cm223dipole : 분자의 극성 모의실험 (교과서 79쪽 해 보기 ① 과정 2 대신)
     · 분자 11개, 3차원 공-막대 모형(끌어서 회전), 결합의 쌍극자 모멘트 화살표(⟼, 길이 ∝ 전기음성도 차이 — 모식도)
     · 「쌍극자 모멘트 합하기」 → 3차원 벡터 합을 같은 시점으로 투영해 오른쪽 아래 칸에(plus 굵게), |합| < 0.05 → 0
     · 「판단 기록」 → 표 행 누적(최근 4행), 「초기화」
   cm223field : 전기장 속 분자 배열 (교과서 80쪽 해 보기 ② 과정 2 대신)
     · F2, HF, HCl, N2 · 전압 걸기 · 극 바꾸기 · 극성 분자는 δ+(H) 쪽이 (−)극을 향해 정렬, 무극성은 무질서
     · 정렬 정도 = 8개 분자 cos(목표 방향과의 각) 평균 · 「관찰 기록」 표 누적 · 「초기화」
   전기음성도(교과서 그림 II-3): H 2.2, B 2.0, C 2.6, N 3.0, O 3.4, F 4.0, Cl 3.2 */
window.DECK_LABS = {
  cm223dipole(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg'), fig=$('.lab-fig'), W=560, H=300, CX=230, CY=160;
    const g=API.mk('g',{},svg);
    const R={H:18,B:24,C:24,N:24,O:24,F:24,Cl:29};
    const CHI={H:2.2,B:2.0,C:2.6,N:3.0,O:3.4,F:4.0,Cl:3.2};
    const d2r=x=>x*Math.PI/180, norm=v=>{ const l=Math.hypot(...v)||1; return v.map(c=>c/l); };
    const pl=a=>[Math.cos(d2r(a)),Math.sin(d2r(a)),0];
    const tet=()=>{ const r=Math.sqrt(8)/3; return [[0,1,0]].concat([0,120,240].map(p=>[r*Math.sin(d2r(p)),-1/3,r*Math.cos(d2r(p))])); };
    const pyr=(ang)=>{ const c=(Math.cos(d2r(ang))+.5)/1.5, al=Math.acos(Math.sqrt(c)); return [0,120,240].map(p=>[Math.sin(al)*Math.sin(d2r(p)),-Math.cos(al),Math.sin(al)*Math.cos(d2r(p))]); };
    const bent=(ang)=>{ const h=d2r(ang/2); return [[-Math.sin(h),-Math.cos(h),0],[Math.sin(h),-Math.cos(h),0]]; };
    const T=[[-1,0,0],[1,0,0]];
    const M={
      H2:{tex:'\\ce{H2}', c:'H', at:[['H',[1,0,0],1]], shape:'선형(이원자 분자)', di:true},
      HF:{tex:'\\ce{HF}', c:'H', at:[['F',[1,0,0],1]], shape:'선형(이원자 분자)', di:true},
      HCl:{tex:'\\ce{HCl}', c:'H', at:[['Cl',[1,0,0],1]], shape:'선형(이원자 분자)', di:true},
      CO2:{tex:'\\ce{CO2}', c:'C', at:[['O',T[0],2],['O',T[1],2]], shape:'선형'},
      HCN:{tex:'\\ce{HCN}', c:'C', at:[['H',T[0],1],['N',T[1],3]], shape:'선형'},
      H2O:{tex:'\\ce{H2O}', c:'O', at:bent(104.5).map(v=>['H',v,1]), lone:[norm([0,.62,.78]),norm([0,.62,-.78])], shape:'굽은 형'},
      BCl3:{tex:'\\ce{BCl3}', c:'B', at:[90,210,330].map(a=>['Cl',pl(a),1]), shape:'평면 삼각형'},
      CH2O:{tex:'\\ce{CH2O}', c:'C', at:[['O',pl(90),2],['H',pl(212),1],['H',pl(328),1]], shape:'평면 삼각형'},
      NH3:{tex:'\\ce{NH3}', c:'N', at:pyr(107).map(v=>['H',v,1]), lone:[[0,1,0]], shape:'삼각뿔'},
      CH4:{tex:'\\ce{CH4}', c:'C', at:tet().map(v=>['H',v,1]), shape:'정사면체'},
      CH3Cl:{tex:'\\ce{CH3Cl}', c:'C', at:tet().map((v,i)=>[i?'H':'Cl',v,1]), shape:'정사면체'}
    };
    let st={m:'NH3', yaw:30, pitch:-18, drag:null, idle:0, added:false};
    let log=[]; const labels=[];
    function rot(v){ let [x,y,z]=v; const a=d2r(st.yaw); [x,z]=[x*Math.cos(a)+z*Math.sin(a), -x*Math.sin(a)+z*Math.cos(a)];
      const b=d2r(st.pitch); [y,z]=[y*Math.cos(b)-z*Math.sin(b), y*Math.sin(b)+z*Math.cos(b)]; return [x,y,z]; }
    const mol=()=>M[st.m];
    function sumVec(){ const m=mol(); const s=[0,0,0]; m.at.forEach(([el,v])=>{ const d=CHI[el]-CHI[m.c], u=norm(v); for(let k=0;k<3;k++) s[k]+=u[k]*d; }); return s; }
    const polarBond=()=>mol().at.some(([el])=>Math.abs(CHI[el]-CHI[mol().c])>1e-6);
    function setLabels(){ labels.forEach(l=>l.remove()); labels.length=0; const m=mol();
      const mkL=el=>{ const d=document.createElement('div'); d.className='ov mid'; const dark=['C','N','O','Cl','B'].includes(el);
        d.style.cssText=`font-size:${el==='H'?18:21}px;font-weight:700;color:${dark?'#fff':'#16233D'}`; d.innerHTML=API.tex(`\\mathrm{${el}}`); fig.appendChild(d); labels.push(d); };
      mkL(m.c); m.at.forEach(([el])=>mkL(el)); }
    function arrowT(x1,y1,x2,y2,col,w){ API.arrow(g,x1,y1,x2,y2,col,w); const L=Math.hypot(x2-x1,y2-y1)||1, ux=(x2-x1)/L, uy=(y2-y1)/L, tx=x1+ux*L*.15, ty=y1+uy*L*.15, h=w>3?9:7;
      API.mk('line',{x1:tx-uy*h,y1:ty+ux*h,x2:tx+uy*h,y2:ty-ux*h,stroke:col,'stroke-width':w,'stroke-linecap':'round'},g); }
    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      const m=mol(), L=110;
      // 위치(투영) — 이원자 분자는 가운데로
      let pos=[{el:m.c,x:0,y:0,z:0}];
      m.at.forEach(([el,v])=>{ const r=rot(norm(v)), l=L*(el==='H'&&!m.di?.82:1); pos.push({el,x:r[0]*l,y:-r[1]*l,z:r[2],v:r}); });
      let ox=CX, oy=CY; if(m.di){ ox=CX-(pos[1].x)/2; oy=CY-(pos[1].y)/2; }
      pos.forEach(p=>{ p.x+=ox; p.y+=oy; });
      // 상자(합)
      API.mk('rect',{x:392,y:172,width:160,height:120,rx:10,fill:'#fff',stroke:'#D5DCE3','stroke-width':2},g);
      const items=[], c=pos[0];
      m.at.forEach(([el,v,o],i)=>{ const p=pos[i+1];
        items.push({z:p.z*.5,k:0,f:()=>{ const dx=p.x-c.x, dy=p.y-c.y, n=Math.hypot(dx,dy)||1, px=-dy/n, py=dx/n;
          ({1:[0],2:[-4.5,4.5],3:[-7,0,7]})[o].forEach(q=>API.mk('line',{x1:c.x+px*q,y1:c.y+py*q,x2:p.x+px*q,y2:p.y+py*q,stroke:'#9AA5B1','stroke-width':o===1?7:5,'stroke-linecap':'round'},g)); }});
        items.push({z:p.z,k:2,f:()=>API.atom(g,p.x,p.y,R[el],el,'-',false)}); });
      (m.lone||[]).forEach(d0=>{ const v=rot(d0), ll=L*.62, ex=v[0]*ll, ey=-v[1]*ll, pl_=Math.hypot(ex,ey);
        items.push({z:v[2]*.6,k:1,f:()=>{ const ang=Math.atan2(ey,ex)*180/Math.PI, cx=c.x+ex*.62, cy=c.y+ey*.62;
          API.mk('ellipse',{cx,cy,rx:Math.max(pl_*.62,20),ry:21,transform:`rotate(${ang} ${cx} ${cy})`,fill:'#E08A2C','fill-opacity':.18,stroke:'#E08A2C','stroke-width':1.5},g);
          const ux=pl_>1e-6?ex/pl_:1, uy=pl_>1e-6?ey/pl_:0, tip=pl_>8?.85:0, bx=c.x+ex*tip, by=c.y+ey*tip;
          [-1,1].forEach(s=>API.mk('circle',{cx:bx-uy*6*s,cy:by+ux*6*s,r:4,fill:'#16233D'},g)); }}); });
      items.push({z:0,k:3,f:()=>API.atom(g,c.x,c.y,R[m.c],m.c,'-',false)});
      items.sort((p,q)=>p.z+.001*p.k-(q.z+.001*q.k)).forEach(it=>it.f());
      // 결합의 쌍극자 모멘트 화살표
      if(I('arr').checked){
        const gx=pos.reduce((s,p)=>s+p.x,0)/pos.length, gy=pos.reduce((s,p)=>s+p.y,0)/pos.length;
        m.at.forEach(([el],i)=>{ const p=pos[i+1], d=CHI[el]-CHI[m.c]; if(Math.abs(d)<1e-6) return;
          const dx=p.x-c.x, dy=p.y-c.y, n=Math.hypot(dx,dy); if(n<8) return; const ux=dx/n, uy=dy/n; let px=-uy, py=ux;
          const mx=(c.x+p.x)/2, my=(c.y+p.y)/2; let sd=px*(mx-gx)+py*(my-gy); if(Math.abs(sd)<1e-3) sd=py<0?1:-1; sd=sd>=0?1:-1;
          const ln=Math.max(28,46*Math.abs(d))*(n/(L*(el==='H'&&!m.di?.82:1))), s=d>0?1:-1, ax=mx+px*24*sd, ay=my+py*24*sd;
          arrowT(ax-ux*ln/2*s, ay-uy*ln/2*s, ax+ux*ln/2*s, ay+uy*ln/2*s, '#16233D', 3); });
      }
      // 합
      const sv=sumVec(), mag=Math.hypot(...sv);
      if(st.added && mag>=.05){ const r=rot(sv), L2=Math.min(80,40*mag+24), n=Math.hypot(r[0],r[1]);
        if(n/mag>.15){ const ux=r[0]/n, uy=-r[1]/n, k=L2*(n/mag); arrowT(472-ux*k/2,240-uy*k/2,472+ux*k/2,240+uy*k/2,'#D7263D',5); }
        else API.mk('circle',{cx:472,cy:240,r:9,fill:'#D7263D'},g); }
      API.place(Ov('zero'),472,240,st.added&&mag<.05); API.place(Ov('sl'),402,176,true);
      labels.forEach((l,i)=>{ const p=pos[i], hid=pos.some((q,j)=>j!==i&&q.z>p.z+.05&&Math.hypot(q.x-p.x,q.y-p.y)<R[q.el]*.85); API.place(l,p.x,p.y,!hid); });
    }
    function update(){
      const m=mol(), mag=Math.hypot(...sumVec()), pb=polarBond();
      root.querySelectorAll('[data-m]').forEach(b=>b.classList.toggle('on',b.dataset.m===st.m));
      Ov('f').innerHTML=API.tex(m.tex); API.place(Ov('f'),16,10);
      O('shape').textContent=m.shape; O('bond').textContent=pb?'극성 공유 결합':'무극성 공유 결합';
      if(!st.added){ O('sum').textContent='예측해 보자'; O('pol').textContent='?';
        O('msg').textContent='결합의 쌍극자 모멘트 화살표를 보고 합이 0이 될지 예측한 뒤 「쌍극자 모멘트 합하기」를 눌러 보자.'; }
      else { const zero=mag<.05; O('sum').textContent=zero?'0':'0이 아님'; O('pol').textContent=zero?'무극성 분자':'극성 분자';
        O('msg').textContent= !pb ? '무극성 공유 결합뿐이라 쌍극자 모멘트가 없다 → 무극성 분자.'
          : zero ? (m.di?'':'극성 공유 결합이 있지만 대칭 구조라 결합의 쌍극자 모멘트가 모두 상쇄된다 → 무극성 분자.')
          : (m.di ? '극성 공유 결합 하나 → 그 결합의 쌍극자 모멘트가 곧 분자의 쌍극자 모멘트다 → 극성 분자.'
                  : '결합의 쌍극자 모멘트가 상쇄되지 않고 합이 남는다 → 극성 분자.'); }
      setLabels(); draw();
    }
    root.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>{ st.m=b.dataset.m; st.added=false; update(); }));
    I('arr').addEventListener('change',draw);
    root.querySelector('[data-act="add"]').addEventListener('click',()=>{ st.added=true; update(); });
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${API.tex(r.tex)}</td><td>${r.shape}</td><td>${r.bond}</td><td>${r.pol}</td>`; tb.appendChild(tr); }); }
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const m=mol(), mag=Math.hypot(...sumVec());
      log.push({tex:m.tex, shape:m.shape.replace('(이원자 분자)',''), bond:polarBond()?'극성':'무극성', pol: st.added?(mag<.05?'무극성 분자':'극성 분자'):'(합하기 전)'}); if(log.length>4) log.shift(); renderLog(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); st={...st,m:'NH3',yaw:30,pitch:-18,added:false}; I('arr').checked=true; update(); });
    svg.style.touchAction='none'; svg.style.cursor='grab';
    svg.addEventListener('pointerdown',e=>{ st.drag={x:e.clientX,y:e.clientY}; svg.setPointerCapture(e.pointerId); svg.style.cursor='grabbing'; API.place(Ov('hint'),0,0,false); });
    svg.addEventListener('pointermove',e=>{ if(!st.drag) return; const sc=fig.getBoundingClientRect().width/W||1;
      st.yaw+=(e.clientX-st.drag.x)/sc*.6; st.pitch=API.clamp(st.pitch-(e.clientY-st.drag.y)/sc*.6,-85,85); st.drag={x:e.clientX,y:e.clientY}; draw(); });
    const up=()=>{ st.drag=null; st.idle=0; svg.style.cursor='grab'; };
    svg.addEventListener('pointerup',up); svg.addEventListener('pointercancel',up);
    API.place(Ov('hint'),80,H-16);
    API.ready(()=>update());
    update();
    if(!window.__STILL) API.loop(root,dt=>{ if(st.drag) return; st.idle+=dt; if(st.idle>1.5){ st.yaw+=dt*16; draw(); } });
  },

  cm223field(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg'), fig=$('.lab-fig'), W=600, H=300;
    const R={H:18,F:24,N:24,Cl:29};
    const MOL={F2:{a:'F',b:'F',tex:'\\ce{F2}',polar:false,d:48}, HF:{a:'H',b:'F',tex:'\\ce{HF}',polar:true,d:46}, HCl:{a:'H',b:'Cl',tex:'\\ce{HCl}',polar:true,d:52}, N2:{a:'N',b:'N',tex:'\\ce{N2}',polar:false,d:46}};
    let seed=11; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    const P0=[[150,80],[290,70],[430,90],[110,170],[250,165],[400,180],[180,250],[340,245]];
    let st={m:'F2', flip:false}, ms=[], log=[];
    const gP=API.mk('g',{},svg), g=API.mk('g',{},svg);
    function init(){ seed=11; ms=P0.map(([x,y])=>({x,y,x0:x,y0:y,a:rnd()*360,w:(rnd()-.5)*120,ph:rnd()*6})); }
    function target(){ return st.flip?180:0; } // a = 0 → 원자 a(H)가 왼쪽, b가 오른쪽
    function plates(){ while(gP.firstChild) gP.removeChild(gP.firstChild);
      const on=I('on').checked, lc=st.flip?'#D7263D':'#1F6FD1', rc=st.flip?'#1F6FD1':'#D7263D';
      API.mk('rect',{x:20,y:40,width:16,height:240,fill:'#8C99A6'},gP); API.mk('rect',{x:W-36,y:40,width:16,height:240,fill:'#8C99A6'},gP);
      if(on){ for(let k=0;k<6;k++){ const y=60+k*40; const s=(x,col,plus)=>{ API.mk('line',{x1:x-6,y1:y,x2:x+6,y2:y,stroke:col,'stroke-width':3},gP); if(plus) API.mk('line',{x1:x,y1:y-6,x2:x,y2:y+6,stroke:col,'stroke-width':3},gP); };
        s(48,lc,st.flip); s(W-48,rc,!st.flip); } }
      const L=Ov('pl'), Rr=Ov('pr'); L.textContent=st.flip?'(+)극':'(−)극'; Rr.textContent=st.flip?'(−)극':'(+)극';
      L.style.color=on?lc:'#5B6B7F'; Rr.style.color=on?rc:'#5B6B7F'; API.place(L,30,18); API.place(Rr,W-30,18); }
    function draw(){ while(g.firstChild) g.removeChild(g.firstChild); const m=MOL[st.m];
      ms.forEach(p=>{ const t=p.a*Math.PI/180, ux=Math.cos(t), uy=Math.sin(t), x1=p.x-ux*m.d/2, y1=p.y-uy*m.d/2, x2=p.x+ux*m.d/2, y2=p.y+uy*m.d/2;
        API.mk('line',{x1,y1,x2,y2,stroke:'#9AA5B1','stroke-width':7,'stroke-linecap':'round'},g);
        API.atom(g,x1,y1,R[m.a],m.a,'-',false); API.atom(g,x2,y2,R[m.b],m.b,'-',false);
        const i=ms.indexOf(p); API.place(labs[2*i],x1,y1); API.place(labs[2*i+1],x2,y2); }); }
    const labs=[]; function setLabels(){ labs.forEach(l=>l.remove()); labs.length=0; const m=MOL[st.m];
      ms.forEach(()=>[m.a,m.b].forEach(el=>{ const d=document.createElement('div'); d.className='ov mid'; const dark=['N','Cl'].includes(el);
        d.style.cssText=`font-size:${el==='H'?18:20}px;font-weight:700;color:${dark?'#fff':'#16233D'}`; d.innerHTML=API.tex(`\\mathrm{${el}}`); fig.appendChild(d); labs.push(d); })); }
    const aligned=()=>{ const m=MOL[st.m]; return m.polar && I('on').checked; };
    function degree(){ if(!MOL[st.m].polar) return null; const t=target(); return ms.reduce((s,p)=>s+Math.cos((p.a-t)*Math.PI/180),0)/ms.length; }
    function settle(){ // 정지 캡처·조작 직후: 정렬 상태를 바로 보여 줌
      if(aligned()){ const t=target(); ms.forEach((p,i)=>{ p.a=t+((i*37)%17-8); }); } }
    function readout(){ const m=MOL[st.m], on=I('on').checked, dg=degree();
      O('pol').textContent=m.polar?'극성 분자':'무극성 분자';
      O('fld').textContent=on?(st.flip?'있음 (왼쪽 판 (+)극)':'있음 (왼쪽 판 (−)극)'):'없음';
      O('arr').textContent=aligned()?'일정한 방향':'무질서';
      O('deg').textContent=dg===null?'— (무극성)':Math.round(Math.max(0,dg)*100)+' %';
      O('msg').textContent= !on ? '전압을 걸지 않으면 극성 분자도 무질서하게 움직인다. 「평행판에 전압 걸기」를 눌러 보자.'
        : m.polar ? `부분 양전하(δ+)를 띤 H 쪽이 (−)극을, 부분 음전하(δ−)를 띤 ${m.b} 쪽이 (+)극을 향해 정렬한다.`
        : '부분 전하가 없어 전기장의 영향을 받지 않는다 → 전압을 걸어도 무질서하다.'; }
    function update(){ root.querySelectorAll('[data-m]').forEach(b=>b.classList.toggle('on',b.dataset.m===st.m)); setLabels(); plates(); readout(); draw(); }
    root.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>{ st.m=b.dataset.m; init(); if(window.__STILL) settle(); update(); }));
    I('on').addEventListener('change',()=>{ if(window.__STILL) settle(); update(); });
    root.querySelector('[data-act="flip"]').addEventListener('click',()=>{ st.flip=!st.flip; if(window.__STILL) settle(); update(); });
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${API.tex(r.tex)}</td><td>${r.on}</td><td>${r.left}</td><td>${r.arr}</td>`; tb.appendChild(tr); }); }
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const on=I('on').checked;
      log.push({tex:MOL[st.m].tex, on:on?'걸음':'안 걺', left:on?(st.flip?'(+)극':'(−)극'):'—', arr:aligned()?'일정한 방향':'무질서'}); if(log.length>4) log.shift(); renderLog(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); st={m:'F2',flip:false}; I('on').checked=false; init(); update(); });
    init(); update();
    API.ready(()=>update());
    if(!window.__STILL) API.loop(root,(dt,t)=>{ const al=aligned(), tg=target();
      ms.forEach((p,i)=>{
        if(al){ let d=((tg-p.a)%360+540)%360-180; p.a+=d*Math.min(1,dt*2.2)+Math.sin(t*3+p.ph)*dt*30; }
        else { p.a+=p.w*dt; if(rnd()<dt*.6) p.w=(rnd()-.5)*160; }
        p.x=p.x0+Math.sin(t*.8+p.ph)*10; p.y=p.y0+Math.cos(t*.7+p.ph*1.3)*8; });
      readout(); draw(); });
  }
};
