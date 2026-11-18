/* 고급화학 1-3-1 원자가 결합·분자 오비탈과 혼성 오비탈 — 실험실
   ac131bond : 결합각 측정 실험실 (자체 지도서 디지털 탐구 Ⅰ-3 「분자 모형 프로그램으로 결합각 측정하고 이론과 비교하기」)
     · 혼성 오비탈 모드: sp3·sp2·sp 혼성 오비탈(큰 엽 + 작은 뒤 엽)과 혼성하지 않은 p 오비탈(옅게), 혼성 오비탈 사이 각.
     · 분자 모형 모드: CH4, NH3, H2O, C2H6, BF3, C2H4, CO2, C2H2 공-막대 모형(끌어서 회전), 비공유 전자쌍 로브, 측정할 결합각.
     · 「측정(3회)」: 모형 좌표에서 결합각을 재고 고정 시드의 작은 오차(±0.6°, 선형 ±0.2°)를 더해 3번 → 평균. 기록 표에 행(최근 4행).
     · 「그래프」: 기록한 분자마다 혼성 예측각(점선 테)과 측정 평균(칠) 막대. 다시 누르면 모형.
     · 실험값: CH4 109.5, NH3 107, H2O 104.5, C2H6 H–C–C 111, BF3 120, C2H4 H–C–H 117, CO2 180, C2H2 180. */
window.DECK_LABS = {
  ac131bond(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg'), fig=$('.lab-fig'), W=560, H=300, CX=280, CY=152;
    const g=API.mk('g',{},svg);
    const R={H:17,B:23,C:23,N:23,O:23,F:23};
    const BF='#7B4FC8', GR='#8C99A6';
    const d2r=x=>x*Math.PI/180, norm=v=>{const l=Math.hypot(...v); return v.map(c=>c/l);}, dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
    const RT=Math.sqrt(8)/3, TET=[[0,1,0]].concat([0,120,240].map(p=>[RT*Math.sin(d2r(p)),-1/3,RT*Math.cos(d2r(p))]));
    function trig(ang){ const c=(Math.cos(d2r(ang))+.5)/1.5, al=Math.acos(Math.sqrt(c)); return [0,120,240].map(p=>[Math.sin(al)*Math.sin(d2r(p)),-Math.cos(al),Math.sin(al)*Math.cos(d2r(p))]); }
    const sc=(v,k)=>v.map(c=>c*k), add=(a,b)=>a.map((c,i)=>c+b[i]);
    const HYB={
      sp3:{tex:'sp^3',n:4,dirs:TET,p:[],ang:'109.5°',arr:'정사면체',part:'2s 1개 + 2p 3개',msg:'s 오비탈 1개와 p 오비탈 3개가 섞여 똑같은 혼성 오비탈 4개가 생긴다 → 정사면체 배열, 109.5°. 혼성하지 않은 p 오비탈은 없다.'},
      sp2:{tex:'sp^2',n:3,dirs:[90,210,330].map(a=>[Math.cos(d2r(a)),0,Math.sin(d2r(a))]),p:[[0,1,0]],ang:'120°',arr:'삼각 평면',part:'2s 1개 + 2p 2개',msg:'s 1개와 p 2개가 섞여 혼성 오비탈 3개 → 한 평면에서 120°. 혼성하지 않은 p 오비탈 1개(옅은 것)는 평면에 수직이다.'},
      sp:{tex:'sp',n:2,dirs:[[1,0,0],[-1,0,0]],p:[[0,1,0],[0,0,1]],ang:'180°',arr:'선형',part:'2s 1개 + 2p 1개',msg:'s 1개와 p 1개가 섞여 혼성 오비탈 2개 → 반대 방향 180°. 혼성하지 않은 p 오비탈 2개는 서로 수직이고 혼성 오비탈에도 수직이다.'}
    };
    function MOL(nm){
      if(nm==='CH4') return {tex:'\\ce{CH4}',hyb:'sp3',dom:4,lone:0,exp:109.5,tri:[1,0,2],atoms:[['C',[0,0,0]]].concat(TET.map(d=>['H',sc(d,1.09)])),bonds:[[0,1,1],[0,2,1],[0,3,1],[0,4,1]],lp:[],what:'H–C–H'};
      if(nm==='NH3') return {tex:'\\ce{NH3}',hyb:'sp3',dom:4,lone:1,exp:107,tri:[1,0,2],atoms:[['N',[0,0,0]]].concat(trig(107).map(d=>['H',sc(d,1.01)])),bonds:[[0,1,1],[0,2,1],[0,3,1]],lp:[[0,[0,1,0]]],what:'H–N–H'};
      if(nm==='H2O'){ const h=d2r(104.5/2); return {tex:'\\ce{H2O}',hyb:'sp3',dom:4,lone:2,exp:104.5,tri:[1,0,2],atoms:[['O',[0,0,0]],['H',sc([-Math.sin(h),-Math.cos(h),0],.96)],['H',sc([Math.sin(h),-Math.cos(h),0],.96)]],bonds:[[0,1,1],[0,2,1]],lp:[[0,norm([0,.62,.78])],[0,norm([0,.62,-.78])]],what:'H–O–H'}; }
      if(nm==='C2H6'){ const c=Math.cos(d2r(111)), s=Math.sin(d2r(111)), at=[['C',[-.77,0,0]],['C',[.77,0,0]]], bd=[[0,1,1]];
        [90,210,330].forEach(p=>{at.push(['H',add([-.77,0,0],sc([-c,s*Math.cos(d2r(p)),s*Math.sin(d2r(p))],1.09))]); bd.push([0,at.length-1,1]);});
        [30,150,270].forEach(p=>{at.push(['H',add([.77,0,0],sc([c,s*Math.cos(d2r(p)),s*Math.sin(d2r(p))],1.09))]); bd.push([1,at.length-1,1]);});
        return {tex:'\\ce{C2H6}',hyb:'sp3',dom:4,lone:0,exp:111,tri:[2,0,1],atoms:at,bonds:bd,lp:[],what:'H–C–C'}; }
      if(nm==='BF3') return {tex:'\\ce{BF3}',hyb:'sp2',dom:3,lone:0,exp:120,tri:[1,0,2],atoms:[['B',[0,0,0]]].concat([90,210,330].map(a=>['F',[1.31*Math.cos(d2r(a)),1.31*Math.sin(d2r(a)),0]])),bonds:[[0,1,1],[0,2,1],[0,3,1]],lp:[],what:'F–B–F'};
      if(nm==='C2H4'){ const a=d2r(58.5), at=[['C',[-.67,0,0]],['C',[.67,0,0]]];
        [-1,1].forEach(sx=>[1,-1].forEach(sy=>at.push(['H',[sx*(.67+1.09*Math.cos(a)),sy*1.09*Math.sin(a),0]])));
        return {tex:'\\ce{C2H4}',hyb:'sp2',dom:3,lone:0,exp:117,tri:[2,0,3],atoms:at,bonds:[[0,1,2],[0,2,1],[0,3,1],[1,4,1],[1,5,1]],lp:[],what:'H–C–H'}; }
      if(nm==='CO2') return {tex:'\\ce{CO2}',hyb:'sp',dom:2,lone:0,exp:180,tri:[1,0,2],atoms:[['C',[0,0,0]],['O',[-1.16,0,0]],['O',[1.16,0,0]]],bonds:[[0,1,2],[0,2,2]],lp:[],what:'O–C–O'};
      return {tex:'\\ce{C2H2}',hyb:'sp',dom:2,lone:0,exp:180,tri:[2,0,1],atoms:[['C',[-.6,0,0]],['C',[.6,0,0]],['H',[-1.66,0,0]],['H',[1.66,0,0]]],bonds:[[0,1,3],[0,2,1],[1,3,1]],lp:[],what:'H–C–C'};
    }
    const PRED={sp3:109.5,sp2:120,sp:180};
    let st={mode:'hyb', h:'sp3', p:'CH4', yaw:25, pitch:-16, drag:null, idle:0, view:'model'};
    let log=[], seed=20261117;
    const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647-.5; };
    const pool=[]; function lab(i){ while(pool.length<=i){ const d=document.createElement('div'); d.className='ov mid'; fig.appendChild(d); pool.push(d);} return pool[i]; }
    function hideLabs(from){ for(let i=from;i<pool.length;i++) API.place(pool[i],0,0,false); }

    function rot(v){ const a=d2r(st.yaw), b=d2r(st.pitch); let [x,y,z]=v;
      [x,z]=[x*Math.cos(a)+z*Math.sin(a),-x*Math.sin(a)+z*Math.cos(a)]; [y,z]=[y*Math.cos(b)-z*Math.sin(b),y*Math.sin(b)+z*Math.cos(b)]; return [x,y,z]; }
    function lobePath(d,L,Wf,minL){ const v=rot(norm(d)), k=Math.hypot(v[0],v[1]), ux=k>1e-6?v[0]/k:1, uy=k>1e-6?-v[1]/k:0, px=-uy, py=ux, Ls=L*Math.max(k,minL||.42), pts=[];
      for(let i=0;i<=60;i++){ const th=d2r(-90+3*i), rho=Ls*Math.cos(th)**2, a=rho*Math.cos(th), b=Wf*L*Math.cos(th)**2*Math.sin(th); pts.push((CX+ux*a+px*b).toFixed(1)+' '+(CY+uy*a+py*b).toFixed(1)); }
      return {d:'M'+pts.join(' L')+' Z', z:v[2], tip:[CX+ux*Ls*.58, CY+uy*Ls*.58]}; }
    function arc(a,b,ra,cx,cy){ const om=Math.acos(Math.max(-1,Math.min(1,dot(a,b)))), pts=[];
      for(let k=0;k<=24;k++){ const t=k/24; let v;
        if(Math.abs(om-Math.PI)<1e-3){ const perp=[0,1,0]; v=a.map((c,i)=>c*Math.cos(Math.PI*t)+perp[i]*Math.sin(Math.PI*t)); }
        else { const s1=Math.sin((1-t)*om)/Math.sin(om), s2=Math.sin(t*om)/Math.sin(om); v=a.map((c,i)=>s1*c+s2*b[i]); }
        const r=rot(v); pts.push([cx+r[0]*ra, cy-r[1]*ra]); }
      API.mk('path',{d:'M'+pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L'),fill:'none',stroke:'#5B6B7F','stroke-width':2.2},g);
      const m=pts[12], vx=m[0]-cx, vy=m[1]-cy, n=Math.hypot(vx,vy)||1; return [cx+vx/n*(n+30), cy+vy/n*(n+30)]; }

    function drawHyb(){
      const H_=HYB[st.h], items=[]; let li=0;
      H_.dirs.forEach(d=>{ const big=lobePath(d,112,.62), sm=lobePath(d.map(c=>-c),40,.9);
        items.push({z:big.z,f:()=>{ API.mk('path',{d:big.d,fill:BF,'fill-opacity':.30,stroke:BF,'stroke-width':1.8},g); const l=lab(li++); l.textContent='+'; l.style.cssText='font-size:21px;font-weight:700'; API.place(l,big.tip[0],big.tip[1]); }});
        items.push({z:sm.z,f:()=>API.mk('path',{d:sm.d,fill:GR,'fill-opacity':.30,stroke:GR,'stroke-width':1.8},g)}); });
      H_.p.forEach(d=>[1,-1].forEach(sg=>{ const lb=lobePath(d.map(c=>c*sg),84,.55);
        items.push({z:lb.z,f:()=>{ const col=sg>0?BF:GR; API.mk('path',{d:lb.d,fill:col,'fill-opacity':.30,stroke:col,'stroke-width':1.8,opacity:.5},g); const l=lab(li++); l.textContent=sg>0?'+':'−'; l.style.cssText='font-size:19px;font-weight:700;opacity:.6'; API.place(l,lb.tip[0],lb.tip[1]); }}); }));
      items.sort((p,q)=>p.z-q.z).forEach(it=>it.f());
      API.mk('circle',{cx:CX,cy:CY,r:5,fill:'#16233D'},g);
      const [lx,ly]=arc(norm(H_.dirs[0]),norm(H_.dirs[1]),44,CX,CY); Ov('ang').textContent=H_.ang; API.place(Ov('ang'),lx,ly-12);
      hideLabs(li);
    }
    function drawMol(){
      const M=MOL(st.p), S=78, items=[], pos=[];
      const ctr=M.atoms.reduce((s,a)=>add(s,a[1]),[0,0,0]).map(c=>c/M.atoms.length);
      M.atoms.forEach(a=>{ const v=rot(a[1].map((c,i)=>c-ctr[i])); pos.push({x:CX+v[0]*S,y:CY-v[1]*S,z:v[2],r:R[a[0]],el:a[0]}); });
      M.bonds.forEach(([i,j,o])=>{ const a=pos[i], b=pos[j]; items.push({z:(a.z+b.z)/2-.001,f:()=>{ const dx=b.x-a.x, dy=b.y-a.y, n=Math.hypot(dx,dy)||1, px=-dy/n, py=dx/n;
        ({1:[0],2:[-4.5,4.5],3:[-7,0,7]})[o].forEach(t=>API.mk('line',{x1:a.x+px*t,y1:a.y+py*t,x2:b.x+px*t,y2:b.y+py*t,stroke:'#9AA5B1','stroke-width':o===1?7:5,'stroke-linecap':'round'},g)); }}); });
      if(I('lp').checked) M.lp.forEach(([c,d])=>{ const v=rot(d), ll=S*.78, ex=v[0]*ll, ey=-v[1]*ll, pl=Math.hypot(ex,ey), p0=pos[c];
        items.push({z:p0.z+v[2]*.6,f:()=>{ const ang=Math.atan2(ey,ex)*180/Math.PI, cx=p0.x+ex*.62, cy=p0.y+ey*.62;
          API.mk('ellipse',{cx,cy,rx:Math.max(pl*.62,20),ry:21,transform:`rotate(${ang} ${cx} ${cy})`,fill:'#E08A2C','fill-opacity':.18,stroke:'#E08A2C','stroke-width':1.5},g);
          const ux=pl>1e-6?ex/pl:1, uy=pl>1e-6?ey/pl:0, tip=pl>8?.85:0, bx=p0.x+ex*tip, by=p0.y+ey*tip;
          [-1,1].forEach(s=>API.mk('circle',{cx:bx-uy*6*s,cy:by+ux*6*s,r:4,fill:'#16233D'},g)); }}); });
      pos.forEach(p=>items.push({z:p.z+.002,f:()=>API.atom(g,p.x,p.y,p.r,p.el,'-',false)}));
      items.sort((p,q)=>p.z-q.z).forEach(it=>it.f());
      const [i,c,j]=M.tri, A_=M.atoms, a=norm(A_[i][1].map((v,k)=>v-A_[c][1][k])), b=norm(A_[j][1].map((v,k)=>v-A_[c][1][k]));
      const [lx,ly]=arc(a,b,38,pos[c].x,pos[c].y); Ov('ang').textContent=(Math.round(M.exp*2)/2)+'°'; API.place(Ov('ang'),lx,ly-12);
      pos.forEach((p,k)=>{ const l=lab(k), dark=['C','N','O','B'].includes(p.el); l.style.cssText=`font-size:${p.el==='H'?18:21}px;font-weight:700;color:${p.el==='B'||!dark?'#16233D':'#fff'}`;
        l.innerHTML=API.tex(`\\mathrm{${p.el}}`); const hid=pos.some((q,m)=>m!==k&&q.z>p.z+.05&&Math.hypot(q.x-p.x,q.y-p.y)<q.r*.85); API.place(l,p.x,p.y,!hid); });
      hideLabs(pos.length);
    }
    function drawGraph(){
      Ov('ang').textContent=''; API.place(Ov('ang'),0,0,false);
      const x0=70, yb=250, base=90, s=2.0; let li=0;
      API.mk('line',{x1:x0,y1:yb,x2:540,y2:yb,stroke:'#5B6B7F','stroke-width':1.6},g); API.mk('line',{x1:x0,y1:yb,x2:x0,y2:30,stroke:'#5B6B7F','stroke-width':1.6},g);
      [90,120,150,180].forEach(v=>{ const y=yb-(v-base)*s; API.mk('line',{x1:x0-6,y1:y,x2:x0,y2:y,stroke:'#5B6B7F','stroke-width':1.4},g); if(v>90) API.mk('line',{x1:x0,y1:y,x2:540,y2:y,stroke:'#E2E7EC','stroke-width':1},g);
        const l=lab(li++); l.textContent=String(v); l.style.cssText='font-size:18px'; API.place(l,x0-22,y); });
      const t=lab(li++); t.textContent='결합각 (°)'; t.style.cssText='font-size:18px;white-space:nowrap'; API.place(t,x0+50,16);
      if(!log.length){ const m=lab(li++); m.textContent='측정한 분자가 없다 — 「측정(3회)」을 눌러 보자'; m.style.cssText='font-size:19px;color:#5B6B7F;white-space:nowrap'; API.place(m,300,150); }
      log.forEach((r,k)=>{ const x=110+k*100;
        API.mk('rect',{x,y:yb-(r.pred-base)*s,width:30,height:(r.pred-base)*s,fill:'#fff',stroke:'#5B6B7F','stroke-width':2,'stroke-dasharray':'5 3'},g);
        API.mk('rect',{x:x+32,y:yb-(r.mean-base)*s,width:30,height:(r.mean-base)*s,fill:'#16233D'},g);
        const l=lab(li++); l.innerHTML=API.tex(r.tex); l.style.cssText='font-size:19px'; API.place(l,x+31,yb+18); });
      const lg=lab(li++); lg.textContent='점선: 혼성 예측 · 칠: 측정 평균'; lg.style.cssText='font-size:18px;color:#5B6B7F;white-space:nowrap'; API.place(lg,400,16);
      hideLabs(li);
    }
    function draw(){ while(g.firstChild) g.removeChild(g.firstChild);
      if(st.view==='graph') return drawGraph();
      if(st.mode==='hyb') drawHyb(); else drawMol(); }

    function update(){
      root.querySelectorAll('[data-h]').forEach(b=>b.classList.toggle('on',b.dataset.h===st.h));
      root.querySelectorAll('[data-p]').forEach(b=>b.classList.toggle('on',b.dataset.p===st.p));
      root.querySelector('[data-act="rec"]').disabled=(st.mode!=='mol');
      if(st.mode==='hyb'){ const H_=HYB[st.h];
        O('k1').textContent='참여 오비탈'; O('v1').textContent=H_.part;
        O('k2').textContent='혼성 오비탈 · 배열'; O('v2').innerHTML=API.tex(H_.tex)+` ${H_.n}개 · ${H_.arr}`;
        O('k3').textContent='혼성 오비탈 사이 각'; O('v3').textContent=H_.ang;
        Ov('f').innerHTML=API.tex(H_.tex+'\\ \\text{혼성}'); O('msg').textContent=H_.msg;
      } else { const M=MOL(st.p);
        O('k1').textContent='전자 영역 · 비공유 전자쌍'; O('v1').textContent=`${M.dom} · ${M.lone}`;
        O('k2').textContent='중심 원자의 혼성'; O('v2').innerHTML=API.tex(HYB[M.hyb].tex)+` (${HYB[M.hyb].arr})`;
        O('k3').textContent='측정할 각'; O('v3').textContent=`${M.what} (실험값 ${M.exp}°)`;
        Ov('f').innerHTML=API.tex(M.tex);
        O('msg').textContent = M.lone? `비공유 전자쌍 ${M.lone}개가 결합 전자쌍을 더 세게 밀어 결합각이 109.5°보다 작다(${M.exp}°).`
          : M.p==='C2H4' || st.p==='C2H4' ? '혼성 예측은 120°이지만, 2중 결합 쪽 전자 밀도가 커서 H–C–H 각은 조금 작다(117°).'
          : st.p==='C2H6' ? '두 C 모두 정사면체 배열 — H–C–C 각은 109.5°에 가깝다(111°).'
          : `혼성 예측 ${PRED[M.hyb]}°와 같은 결합각을 갖는다.`;
      }
      API.place(Ov('f'),16,10); draw();
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${API.tex(r.tex)}</td><td>${API.tex(HYB[r.hyb].tex)}</td><td>${r.lone}</td><td>${r.mean.toFixed(1)}°</td><td>${r.exp}°</td>`; tb.appendChild(tr); }); }

    root.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>{ st.mode=b.dataset.m; st.view='model';
      root.querySelectorAll('[data-m]').forEach(x=>x.classList.toggle('on',x===b));
      root.querySelector('[data-set="hyb"]').style.display=st.mode==='hyb'?'':'none';
      root.querySelector('[data-set="mol"]').style.display=st.mode==='mol'?'':'none'; update(); }));
    root.querySelectorAll('[data-h]').forEach(b=>b.addEventListener('click',()=>{ st.h=b.dataset.h; st.view='model'; update(); }));
    root.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{ st.p=b.dataset.p; st.view='model'; update(); }));
    I('lp').addEventListener('change',draw);
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ if(st.mode!=='mol') return; const M=MOL(st.p);
      const [i,c,j]=M.tri, A_=M.atoms, a=norm(A_[i][1].map((v,k)=>v-A_[c][1][k])), b=norm(A_[j][1].map((v,k)=>v-A_[c][1][k]));
      const th=Math.acos(Math.max(-1,Math.min(1,dot(a,b))))*180/Math.PI, amp=th>179?0.4:1.2;
      const reads=[0,1,2].map(()=>Math.min(180,th+rnd()*amp)), mean=reads.reduce((s,x)=>s+x,0)/3;
      log.push({tex:M.tex,hyb:M.hyb,lone:M.lone,mean,exp:M.exp,pred:PRED[M.hyb]}); if(log.length>4) log.shift(); renderLog();
      O('msg').textContent=`측정 ${reads.map(x=>x.toFixed(1)).join(', ')}° → 평균 ${mean.toFixed(1)}°, 실험값 ${M.exp}°와 ${Math.abs(mean-M.exp).toFixed(1)}° 차이`;
      if(st.view==='graph') draw(); });
    root.querySelector('[data-act="graph"]').addEventListener('click',()=>{ st.view=st.view==='graph'?'model':'graph';
      root.querySelector('[data-act="graph"]').classList.toggle('on',st.view==='graph'); API.place(Ov('f'),16,10,st.view!=='graph'); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; seed=20261117; renderLog(); st={...st,mode:'hyb',h:'sp3',p:'CH4',yaw:25,pitch:-16,view:'model'};
      root.querySelectorAll('[data-m]').forEach(x=>x.classList.toggle('on',x.dataset.m==='hyb'));
      root.querySelector('[data-act="graph"]').classList.remove('on');
      root.querySelector('[data-set="hyb"]').style.display=''; root.querySelector('[data-set="mol"]').style.display='none'; I('lp').checked=true; update(); });
    svg.style.touchAction='none'; svg.style.cursor='grab';
    svg.addEventListener('pointerdown',e=>{ if(st.view==='graph') return; st.drag={x:e.clientX,y:e.clientY}; svg.setPointerCapture(e.pointerId); svg.style.cursor='grabbing'; API.place(Ov('hint'),0,0,false); });
    svg.addEventListener('pointermove',e=>{ if(!st.drag) return; const k=fig.getBoundingClientRect().width/W||1;
      st.yaw+=(e.clientX-st.drag.x)/k*.6; st.pitch=API.clamp(st.pitch-(e.clientY-st.drag.y)/k*.6,-85,85); st.drag={x:e.clientX,y:e.clientY}; draw(); });
    const up=()=>{ st.drag=null; st.idle=0; svg.style.cursor='grab'; };
    svg.addEventListener('pointerup',up); svg.addEventListener('pointercancel',up);
    API.place(Ov('hint'),W-80,H-20);
    API.ready(()=>update());
    update();
    if(!window.__STILL) API.loop(root,dt=>{ if(st.drag||st.view==='graph') return; st.idle+=dt; if(st.idle>1.5){ st.yaw+=dt*18; draw(); } });
  }
};
