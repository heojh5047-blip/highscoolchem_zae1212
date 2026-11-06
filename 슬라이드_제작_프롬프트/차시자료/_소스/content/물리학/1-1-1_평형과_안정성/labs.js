/* 1-1-1 평형과 안정성 — 실험실
   lever111  : 지레·시소 평형 실험실. 양쪽 돌림힘을 비교해 막대(시소 판)가 기울거나 수평으로 돌아오는 모습을
               감쇠 진동으로 움직인다. θ'' = ω²(θ*−θ) − 2ζωθ' (ω=4 s⁻¹, ζ=0.6), θ* = 0(평형) 또는 ±한계각.
               θ (+) = 시계 반대 방향 = 왼쪽이 내려감.
               한계각: 지레는 받침점 양옆의 멈춤대에 닿는 각(12°), 시소는 판 끝이 땅에 닿는 각.
               평형이 아닐 때는 멈춤대(땅)도 막대를 떠받치므로 받침점의 힘 N을 전체 무게로 표시하지 않는다.
   topple111 : 안정성 실험실. 받침점(블록의 왼쪽 아래 모서리)을 축으로 기울인 블록을 손에서 놓으면
               φ'' = −g·d(φ)/k², d = (b/2)cosφ − h·sinφ, k² = (b²+H²)/12 + (b/2)² + h² 로 돌아오거나 쓰러진다. */
window.DECK_LABS = {
  lever111(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const C=API.COL, BLUE='#1F6FD1', svg=$('svg');
    const I=k=>root.querySelector(`[data-i="${k}"]`);
    const btns=[...root.querySelectorAll('.d111-mode .btn')];
    let mode='lever', th=0, om=0, target=0, settled=false;
    const W={ omega:4, zeta:0.6 };
    // ── 지레 장면 (받침점 PL) ──
    const PL={x:280,y:170}, HALF=258, TICK=48, BH=14, STOP=30;   // BH: 막대 두께의 절반, STOP: 멈춤대까지의 거리
    const LIM={ lever:12*Math.PI/180, seesaw:Math.asin(73.5/252) };   // 시소: 판 끝(252 px)이 땅(73.5 px 아래)에 닿는 각
    const gL=API.mk('g',{},svg);
    API.mk('ellipse',{cx:280,cy:382,rx:80,ry:10,fill:'#2E3B52'},gL);
    API.mk('rect',{x:276,y:PL.y,width:8,height:212,fill:'#D5DDE5'},gL);
    // 멈춤대: 막대가 한계각만큼 기울면 아래면이 닿는 자리
    const sY=PL.y+BH*Math.cos(LIM.lever)+STOP*Math.sin(LIM.lever), sX=STOP*Math.cos(LIM.lever)-BH*Math.sin(LIM.lever);
    API.mk('rect',{x:PL.x-sX-8,y:sY+5,width:2*sX+16,height:5,rx:2,fill:'#9FB0C2'},gL);
    [-1,1].forEach(sg=>API.mk('rect',{x:PL.x+sg*sX-5,y:sY,width:10,height:6,rx:2,fill:C.muted},gL));
    const barG=API.mk('g',{},gL);
    API.mk('rect',{x:PL.x-HALF,y:PL.y-BH,width:2*HALF,height:2*BH,rx:7,fill:'#FFFFFF',stroke:'#9FB0C2','stroke-width':2},barG);
    for(let k=1;k<=5;k++) [-1,1].forEach(sg=>{ const x=PL.x+sg*k*TICK;
      API.mk('circle',{cx:x,cy:PL.y,r:12,fill:'#FFFFFF',stroke:C.muted,'stroke-width':1.5},barG);
      API.texText(barG,x,PL.y+6,String(k),{size:17,anchor:'middle'}); });
    API.mk('circle',{cx:PL.x,cy:PL.y,r:6,fill:C.muted},barG);
    const dynL=API.mk('g',{},gL);

    // ── 시소 장면 (받침점 PS) ──
    const PS={x:280,y:217}, PX=80, GROUND=290;  // 80 px = 1 m
    const gS=API.mk('g',{style:'display:none'},svg);
    API.mk('rect',{x:20,y:292,width:520,height:8,fill:'#EEF2F6'},gS);
    API.mk('line',{x1:20,y1:292,x2:540,y2:292,stroke:'#9FB0C2','stroke-width':3},gS);
    API.mk('polygon',{points:`${PS.x},${PS.y} ${PS.x-30},290 ${PS.x+30},290`,fill:'#C9D3DD',stroke:'#9FB0C2','stroke-width':2},gS);
    const plankG=API.mk('g',{},gS);
    API.mk('rect',{x:PS.x-252,y:PS.y-12,width:504,height:12,rx:4,fill:'#E8C99A',stroke:'#B8925A','stroke-width':2},plankG);
    for(let k=1;k<=6;k++) [-1,1].forEach(sg=>{ const x=PS.x+sg*k*PX/2, big=k%2===0;
      API.mk('line',{x1:x,y1:PS.y-12,x2:x,y2:PS.y-(big?4:8),stroke:'#8C6A3E','stroke-width':big?2:1.2},plankG); });
    const dynS=API.mk('g',{},gS);

    // 위치 변환: s = 막대를 따라 받침점에서의 거리(오른쪽 +), d = 막대 윗면 쪽으로 수직 거리
    const at=(P,s,d)=>[P.x+s*Math.cos(th)-d*Math.sin(th), P.y-s*Math.sin(th)-d*Math.cos(th)];
    const curve=(g,P,R,ccw,hi)=>{            // 내려가는 쪽 위의 주황 곡선 화살표 (알짜 돌림힘 방향)
      const deg=Math.PI/180, base=-th;      // 막대 각도 반영(화면 좌표에서 시계 방향 +)
      const s=hi?30:0;                      // hi: 시소 — 사람 머리와 겹치지 않게 더 위쪽에 그린다
      const a0=ccw? base-(125-s)*deg : base-(55+s)*deg, a1=ccw? base-(160-s)*deg : base-(20+s)*deg;
      const p0=[P.x+R*Math.cos(a0),P.y+R*Math.sin(a0)], p1=[P.x+R*Math.cos(a1),P.y+R*Math.sin(a1)];
      API.mk('path',{d:`M${p0[0].toFixed(1)} ${p0[1].toFixed(1)} A${R} ${R} 0 0 ${ccw?0:1} ${p1[0].toFixed(1)} ${p1[1].toFixed(1)}`,fill:'none',stroke:C.equi,'stroke-width':3,'stroke-linecap':'round'},g);
      const t= ccw? [Math.sin(a1),-Math.cos(a1)] : [-Math.sin(a1),Math.cos(a1)];
      API.arrow(g,p1[0]-14*t[0],p1[1]-14*t[1],p1[0]+3*t[0],p1[1]+3*t[1],C.equi,3);
    };
    const person=(g,hx,hy,s,dir)=>{          // 앉은 사람(엉덩이 hx,hy, 크기 s, dir=+1 이면 오른쪽을 봄)
      const c='#7C8FA6', fy=Math.min(hy+20*s,GROUND-4*s);   // 발은 땅 아래로 들어가지 않는다
      API.mk('line',{x1:hx,y1:hy,x2:hx,y2:hy-42*s,stroke:c,'stroke-width':10*s,'stroke-linecap':'round'},g);
      API.mk('path',{d:`M${hx} ${hy} L${hx+dir*24*s} ${hy} L${hx+dir*28*s} ${fy} M${hx} ${hy-34*s} L${hx+dir*18*s} ${hy-14*s}`,fill:'none',stroke:c,'stroke-width':6.5*s,'stroke-linecap':'round','stroke-linejoin':'round'},g);
      API.mk('circle',{cx:hx,cy:hy-56*s,r:12*s,fill:c},g);
    };

    function vals(){
      if(mode==='lever'){ const La=+I('La').value, Ln=+I('Ln').value, Ra=+I('Ra').value, Rn=+I('Rn').value;
        return {La,Ln,Ra,Rn,tL:0.1*La*Ln,tR:0.1*Ra*Rn,N:Ln+Rn,eq:La*Ln===Ra*Rn}; }
      const mA=+I('mA').value, mB=+I('mB').value, xA=+I('xA').value, xB=+I('xB').value, g=9.8;
      const tL=mA*g*xA, tR=mB*g*xB; return {mA,mB,xA,xB,tL,tR,N:(mA+mB)*g,eq:Math.abs(tL-tR)<0.5};
    }

    function render(){
      const v=vals(), deg=th*180/Math.PI;
      if(mode==='lever'){
        barG.setAttribute('transform',`rotate(${(-deg).toFixed(3)} ${PL.x} ${PL.y})`);
        while(dynL.firstChild) dynL.removeChild(dynL.firstChild);
        [[-1,v.La,v.Ln],[1,v.Ra,v.Rn]].forEach(([sg,a,n])=>{ if(!n) return;
          const [hx,hy]=at(PL,sg*a*TICK,-BH);
          API.mk('line',{x1:hx,y1:hy,x2:hx,y2:hy+22,stroke:C.muted,'stroke-width':1.5},dynL);
          for(let j=0;j<n;j++) API.mk('rect',{x:hx-13,y:hy+22+13*j,width:26,height:13,rx:2,fill:'#E3C77A',stroke:'#C8A94B','stroke-width':1.5},dynL);
          const y0=hy+22+13*n; API.arrow(dynL,hx,y0+2,hx,y0+4+11*n,BLUE,3.5); });
        const L=11*v.N;
        // 받침점의 힘 N: 평형(수평)일 때만 전체 무게와 같다. 기울어 멈춤대에 닿으면 멈춤대도 막대를 떠받친다.
        if(L>0 && v.eq){ API.arrow(dynL,PL.x,PL.y+18+L,PL.x,PL.y+10,C.ink,4); API.place(Ov('lN'),PL.x+22,PL.y+12+L*0.5); }
        else API.place(Ov('lN'),0,0,false);
        if(!v.eq) curve(dynL,PL,150,v.tL>v.tR);
        API.place(Ov('pv'),PL.x,PL.y-48);
        API.place(Ov('nA'),0,0,false); API.place(Ov('nB'),0,0,false);
      } else {
        plankG.setAttribute('transform',`rotate(${(-deg).toFixed(3)} ${PS.x} ${PS.y})`);
        while(dynS.firstChild) dynS.removeChild(dynS.firstChild);
        const sA=0.75+0.35*(v.mA-30)/60, sB=0.75+0.35*(v.mB-30)/60;
        const [ax,ay]=at(PS,-v.xA*PX,12), [bx,by]=at(PS,v.xB*PX,12);
        person(dynS,ax,ay,sA,1); person(dynS,bx,by,sB,-1);
        const wArrow=(x,y,m)=>{ const y1=Math.min(y+4+0.8*m,GROUND-3), y0=Math.min(y+2,y1-18);   // 무게 화살표는 땅 위에서 멈춘다
          API.arrow(dynS,x,y0,x,y1,BLUE,3.5); };
        wArrow(ax,ay,v.mA); wArrow(bx,by,v.mB);
        const L=Math.min(70,0.04*v.N);
        if(v.eq){ API.arrow(dynS,PS.x,PS.y+L+4,PS.x,PS.y+2,C.ink,4); API.place(Ov('lN'),PS.x+20,PS.y+L*0.45); }
        else API.place(Ov('lN'),0,0,false);
        if(!v.eq) curve(dynS,PS,170,v.tL>v.tR,true);
        API.place(Ov('pv'),PS.x+66,PS.y+44);
        API.place(Ov('nA'),ax,ay-56*sA-12*sA-26); API.place(Ov('nB'),bx,by-56*sB-12*sB-26);
      }
    }

    const fmtT=x=>x===0?'0 N·m':mode==='lever'?(Math.round(x*10)/10).toFixed(1)+' N·m':Math.round(x)+' N·m';
    function update(){
      const v=vals();
      if(mode==='lever'){ O('La').textContent='눈금 '+v.La; O('Ra').textContent='눈금 '+v.Ra; O('Ln').textContent=v.Ln+'개'; O('Rn').textContent=v.Rn+'개'; }
      else { O('mA').textContent=v.mA+' kg'; O('mB').textContent=v.mB+' kg'; O('xA').textContent=v.xA.toFixed(2)+' m'; O('xB').textContent=v.xB.toFixed(2)+' m'; }
      O('N').textContent=v.eq?(mode==='lever'?v.N:Math.round(v.N))+' N':'— (평형 아님)';
      O('tL').textContent=fmtT(v.tL); O('tR').textContent=fmtT(v.tR);
      const m=O('msg'), stop=mode==='lever'?'멈춤대에 닿는다':'판 끝이 땅에 닿는다';
      if(v.eq){ m.className='kind d111-msg d111-ok'; m.textContent='평형: 양쪽 돌림힘이 같다 → 수평을 유지한다'; target=0; }
      else if(v.tL>v.tR){ m.className='kind d111-msg rep'; m.textContent='시계 반대 방향 돌림힘이 크다 → 왼쪽이 내려가 '+stop; target=LIM[mode]; }
      else { m.className='kind d111-msg rep'; m.textContent='시계 방향 돌림힘이 크다 → 오른쪽이 내려가 '+stop; target=-LIM[mode]; }
      settled=false; render();
    }
    function setMode(m){
      mode=m; btns.forEach(b=>b.classList.toggle('on',b.dataset.m===m));
      root.querySelectorAll('[data-set]').forEach(d=>d.style.display=d.dataset.set===m?'':'none');
      gL.style.display=m==='lever'?'':'none'; gS.style.display=m==='seesaw'?'':'none';
      update();
    }
    btns.forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.m)));
    root.querySelectorAll('input[type=range]').forEach(i=>i.addEventListener('input',update));
    // 처음 열었을 때는 이미 기울어진 상태(목표 각)로 보여 준다
    setMode('lever'); th=target; render();
    API.onShow(s=>{ if(s===root.closest('.slide')) render(); });
    API.loop(root,dt=>{
      if(settled||!dt) return;
      const a=W.omega*W.omega*(target-th)-2*W.zeta*W.omega*om;
      om+=a*dt; th+=om*dt;
      if(Math.abs(target-th)<1e-4 && Math.abs(om)<1e-4){ th=target; om=0; settled=true; }
      render();
    });
  },

  topple111(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const C=API.COL, BLUE='#1F6FD1', svg=$('svg'), D2R=Math.PI/180;
    const ib=$('[data-i="b"]'), iH=$('[data-i="H"]'), ith=$('[data-i="th"]');
    const segs=[...root.querySelectorAll('.d111-seg .btn')];
    const P={x:330,y:360}, S=1.8, SLOW=0.55;   // 1.8 px = 1 cm · 수업에서 보기 쉽게 실제보다 느리게(0.55배) 움직인다
    let c=0.5, phi=15*D2R, om=0, run=false, result='';

    API.mk('rect',{x:10,y:360,width:540,height:30,fill:'#EEF2F6'},svg);
    API.mk('line',{x1:10,y1:360,x2:550,y2:360,stroke:'#9FB0C2','stroke-width':3},svg);
    // 범례: 처음 자리(회색 점선), 쓰러지는 경계(주황 점선)
    API.mk('rect',{x:18,y:16,width:16,height:16,fill:'none',stroke:'#9FB0C2','stroke-width':1.8,'stroke-dasharray':'4 3'},svg);
    API.texText(svg,40,31,'서 있던 자리',{size:18,mix:true,fill:C.muted});
    API.mk('rect',{x:164,y:16,width:16,height:16,fill:'none',stroke:C.equi,'stroke-width':1.8,'stroke-dasharray':'4 3'},svg);
    API.texText(svg,186,31,'쓰러지는 경계 (경계 각도로 기울인 자리)',{size:18,mix:true,fill:C.equi});
    const g=API.mk('g',{},svg);
    const COLS=['#C9B8E0','#A8D8EA','#B7E1B5','#F6E3A1','#F2B8C6'];

    const pt=(x,y,f)=>[P.x+x*Math.cos(f)-y*Math.sin(f), P.y-(x*Math.sin(f)+y*Math.cos(f))];
    const sizes=()=>{ const b=+ib.value, H=+iH.value; return {b,H,h:c*H}; };
    const dOf=(f,s)=>(s.b/2)*Math.cos(f)-s.h*Math.sin(f);              // cm, 받침점 안쪽(+)
    const fmt=v=>(v>=0?'+':'−')+Math.abs(v).toFixed(1)+' cm';

    function blockRect(gp,s,f,style){
      const t=API.mk('g',{transform:`rotate(${(-f/D2R).toFixed(3)} ${P.x} ${P.y})`},gp);
      const w=s.b*S, hh=s.H*S;
      if(style==='solid'){
        const n=Math.max(1,Math.round(s.H/20)), lh=hh/n;
        for(let i=0;i<n;i++){ const y=P.y-(i+1)*lh, mid=(i+0.5)/n;
          let fill=COLS[i%COLS.length];
          if(c===0.25 && mid<0.4) fill='#9FB4CC'; if(c===0.75 && mid>0.6) fill='#9FB4CC';
          API.mk('rect',{x:P.x,y:y.toFixed(1),width:w,height:lh.toFixed(1),fill,stroke:C.muted,'stroke-width':1.3},t); }
      } else API.mk('rect',{x:P.x,y:P.y-hh,width:w,height:hh,fill:'none',stroke:style,'stroke-width':1.8,'stroke-dasharray':'6 5'},t);
      return t;
    }

    function draw(){
      const s=sizes(), tc=Math.atan((s.b/2)/s.h), d=dOf(phi,s);
      while(g.firstChild) g.removeChild(g.firstChild);
      blockRect(g,s,0,'#9FB0C2');                                   // 서 있던 자리
      if(tc<85*D2R) blockRect(g,s,tc,C.equi);
      blockRect(g,s,phi,'solid');
      if(!run && !result){                                          // 손가락으로 붙잡고 있음
        const [fx,fy]=pt(s.b*S,s.H*S*0.92,phi);
        API.mk('rect',{x:fx+2,y:fy-11,width:66,height:22,rx:11,fill:'#E3CBB3',stroke:'#B89C80','stroke-width':2},g);
      }
      const [gx,gy]=pt(s.b*S/2,s.h*S,phi);
      API.mk('line',{x1:gx,y1:gy,x2:gx,y2:P.y,stroke:C.muted,'stroke-width':2,'stroke-dasharray':'6 4'},g);
      const ay=Math.min(gy+60,P.y-3);                                // 무게 화살표는 바닥선에서 멈춘다
      if(ay-gy>14) API.arrow(g,gx,gy+3,gx,ay,BLUE,4);
      API.mk('circle',{cx:gx,cy:gy,r:8,fill:'#FFFFFF'},g); API.mk('circle',{cx:gx,cy:gy,r:5.5,fill:C.ink},g);
      API.mk('circle',{cx:P.x,cy:P.y,r:6,fill:C.ink,stroke:'#FFFFFF','stroke-width':2},g);
      if(Math.abs(d)>0.3 && phi>0.5*D2R && phi<89*D2R){             // 중력에 의한 돌림힘의 방향
        const [tx,ty]=pt(s.b*S,s.H*S,phi), R=Math.hypot(tx-P.x,ty-P.y)+22, a=Math.atan2(ty-P.y,tx-P.x), cw=d>0;
        const a0=cw?a-11*D2R:a+11*D2R, a1=cw?a+11*D2R:a-11*D2R;
        const p0=[P.x+R*Math.cos(a0),P.y+R*Math.sin(a0)], p1=[P.x+R*Math.cos(a1),P.y+R*Math.sin(a1)];
        API.mk('path',{d:`M${p0[0].toFixed(1)} ${p0[1].toFixed(1)} A${R.toFixed(1)} ${R.toFixed(1)} 0 0 ${cw?1:0} ${p1[0].toFixed(1)} ${p1[1].toFixed(1)}`,fill:'none',stroke:C.equi,'stroke-width':3.5,'stroke-linecap':'round'},g);
        const t=cw?[-Math.sin(a1),Math.cos(a1)]:[Math.sin(a1),-Math.cos(a1)];
        API.arrow(g,p1[0]-15*t[0],p1[1]-15*t[1],p1[0]+3*t[0],p1[1]+3*t[1],C.equi,3.5);
      }
      API.place(Ov('pv'),P.x-6,P.y+8);
      API.place(Ov('cg'),gx+(gx>P.x-40?62:-62),(!run&&!result)?gy+16:gy-16);   // 손가락으로 잡고 있을 때는 점의 아래쪽(손가락이 위쪽에 있다)
      O('d').textContent=result==='fall'?'— (쓰러짐)':fmt(d);
      return {s,tc,d};
    }
    function update(reset){
      if(reset){ run=false; result=''; om=0; phi=+ith.value*D2R; }
      const s=sizes(), tc=Math.atan((s.b/2)/s.h);
      O('b').textContent=s.b+' cm'; O('H').textContent=s.H+' cm'; O('th').textContent=ith.value+'°';
      O('h').textContent=(Math.round(s.h*10)/10)+' cm'; O('tc').textContent=(tc/D2R).toFixed(1)+'°';
      segs.forEach(b=>b.classList.toggle('on',+b.dataset.c===c));
      const r=draw(), m=O('msg');
      if(result==='back'){ m.className='kind d111-msg d111-ok'; m.textContent='제자리로 돌아왔다'; }
      else if(result==='fall'){ m.className='kind d111-msg rep'; m.textContent='쓰러졌다'; }
      else if(Math.abs(r.d)<=0.3){ m.className='kind d111-msg'; m.textContent='경계: 아슬아슬한 평형'; }
      else if(r.d>0){ m.className='kind d111-msg d111-ok'; m.textContent='수선이 받침점 안쪽 → 손을 떼면 돌아온다'; }
      else { m.className='kind d111-msg rep'; m.textContent='수선이 받침점 바깥 → 손을 떼면 쓰러진다'; }
    }
    [ib,iH,ith].forEach(i=>i.addEventListener('input',()=>update(true)));
    segs.forEach(b=>b.addEventListener('click',()=>{ c=+b.dataset.c; update(true); }));
    $('[data-b="go"]').addEventListener('click',()=>{ if(result) update(true); run=true; update(false); });
    $('[data-b="reset"]').addEventListener('click',()=>update(true));
    update(true);
    API.onShow(s=>{ if(s===root.closest('.slide')) draw(); });
    API.loop(root,dt=>{
      if(!run||!dt) return;
      const s=sizes(), m=0.01, k2=((s.b*m)**2+(s.H*m)**2)/12+(s.b*m/2)**2+(s.h*m)**2;
      for(let i=0;i<4;i++){ const h=SLOW*dt/4, a=-9.8*dOf(phi,s)*m/k2; om+=a*h; phi+=om*h;
        if(phi<=0){ phi=0; om=-0.3*om; if(Math.abs(om)<0.05){ om=0; run=false; result='back'; break; } }
        if(phi>=Math.PI/2){ phi=Math.PI/2; om=0; run=false; result='fall'; break; } }
      if(run) draw(); else update(false);
    });
  }
};
