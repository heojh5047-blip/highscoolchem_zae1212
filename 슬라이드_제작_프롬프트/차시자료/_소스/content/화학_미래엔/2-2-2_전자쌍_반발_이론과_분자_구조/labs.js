/* 2-2-2 전자쌍 반발 이론과 분자 구조 — 실험실
   cm222model : 분자 구조 모델링 실험실 (필수 탐구 화02-탐2 「소프트웨어를 활용하여 분자 구조 모델링하기」)
     · 분자 고르기: 중심 원자(Be, B, C, N, O) × 결합 원자(H, F, Cl) — 결합 수는 옥텟(Be 2, B 3, C 4, N 3, O 2),
       비공유 전자쌍 = (원자가 전자 − 결합 수)/2. 다중 결합 분자 CO2, HCN, HCHO.
     · 전자쌍 고르기: 결합 원자 수(2–4) × 비공유 전자쌍 수(0–2), 허용 조합 (2,0)(3,0)(4,0)(3,1)(2,2).
     · 3차원 공-막대 모형: 끌어서 회전, 손을 떼면 천천히 돈다. 결합각은 모형 좌표에서 계산(측정)한다.
     · 결합각 값(교과서·문헌): 180, 120, 109.5, NH3 107, NCl3 107, NF3 102, H2O 104.5, OF2 103, HCHO H–C–O 122(약 120).
     · 「측정 기록」→ 결과 표에 행이 쌓인다(최근 4행). 「초기화」. */
window.DECK_LABS = {
  cm222model(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg'), fig=$('.lab-fig'), W=560, H=300, CX=280, CY=158;
    const g=API.mk('g',{},svg);
    const R={H:17,Be:23,B:23,C:23,N:23,O:23,F:23,Cl:27,X:23};
    const VAL={Be:2,B:3,C:4,N:5,O:6}, NB={Be:2,B:3,C:4,N:3,O:2};
    const BAD={Be:['H'],B:['H'],O:['Cl']};
    const ANG={NH3:107,NF3:102,NCl3:107,H2O:104.5,OF2:103};
    const GEO={2:'선형',3:'평면 삼각형',4:'정사면체'};
    const SHAPE={'2,0':'선형','3,0':'평면 삼각형','4,0':'정사면체','3,1':'삼각뿔','2,2':'굽은 형'};
    const ANG0={'2,0':180,'3,0':120,'4,0':109.5,'3,1':107,'2,2':104.5};
    let st={mode:'mol', c:'C', t:'H', p:null, yaw:25, pitch:-16, drag:null, idle:0};
    let mol=null, log=[];
    const labels=[];

    const norm=v=>{ const l=Math.hypot(...v); return v.map(c=>c/l); };
    const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
    function dirs(nb,nl,ang){
      const d=x=>x*Math.PI/180;
      if(nb===2&&nl===0) return [[[-1,0,0],[1,0,0]],[]];
      if(nb===3&&nl===0) return [[90,210,330].map(a=>[Math.cos(d(a)),Math.sin(d(a)),0]),[]];
      if(nb===4&&nl===0){ const r=Math.sqrt(8)/3; return [[[0,1,0]].concat([0,120,240].map(p=>[r*Math.sin(d(p)),-1/3,r*Math.cos(d(p))])),[]]; }
      if(nb===3&&nl===1){ const c=(Math.cos(d(ang))+.5)/1.5, al=Math.acos(Math.sqrt(c));
        return [[0,120,240].map(p=>[Math.sin(al)*Math.sin(d(p)),-Math.cos(al),Math.sin(al)*Math.cos(d(p))]),[[0,1,0]]]; }
      if(nb===2&&nl===2){ const h=d(ang/2); return [[[-Math.sin(h),-Math.cos(h),0],[Math.sin(h),-Math.cos(h),0]],[norm([0,.62,.78]),norm([0,.62,-.78])]]; }
      return null;
    }

    function build(){
      if(st.mode==='vsepr'){
        const nb=+I('nb').value, nl=+I('nl').value, key=nb+','+nl;
        O('nb').textContent=nb+'개'; O('nl').textContent=nl+'개';
        if(!SHAPE[key]) return {bad: nb+nl>4? '전자쌍이 5개 이상인 조합은 옥텟 규칙을 넘어 이 단원에서 다루지 않는다.' : '결합 원자 2개 + 비공유 전자쌍 1개는 다중 결합이 있어야 생기는 조합으로, 이 단원에서 다루지 않는다.', nb, nl, tex:`\\mathrm{AB}_{${nb}}`};
        const ang=ANG0[key], [bd,ld]=dirs(nb,nl,ang);
        return {tex:`\\mathrm{AB}_{${nb}}`+(nl?`\\ (\\text{비공유 }${nl})`:''), name:`AB${nb}`+(nl?`(비공유 ${nl})`:''), center:'X', cl:'\\mathrm{A}',
          atoms:bd.map(v=>({el:'X',lab:'\\mathrm{B}',v,o:1})), lone:ld, nb, nl, ang, angTxt:fmtA(ang), shape:SHAPE[key], geo:GEO[nb+nl]};
      }
      if(st.p){
        if(st.p==='CO2') return {tex:'\\ce{CO2}', name:'CO2', center:'C', atoms:[{el:'O',v:[-1,0,0],o:2},{el:'O',v:[1,0,0],o:2}], lone:[], nb:2, nl:0, ang:180, angTxt:'180°', shape:'선형', geo:'선형', multi:'이중 결합 2개'};
        if(st.p==='HCN') return {tex:'\\ce{HCN}', name:'HCN', center:'C', atoms:[{el:'H',v:[-1,0,0],o:1},{el:'N',v:[1,0,0],o:3}], lone:[], nb:2, nl:0, ang:180, angTxt:'180°', shape:'선형', geo:'선형', multi:'단일 결합 1개 + 삼중 결합 1개'};
        const a=x=>[Math.cos(x*Math.PI/180),Math.sin(x*Math.PI/180),0];
        return {tex:'\\ce{HCHO}', name:'HCHO', center:'C', atoms:[{el:'O',v:a(90),o:2},{el:'H',v:a(212),o:1},{el:'H',v:a(328),o:1}], lone:[], nb:3, nl:0, ang:122, angTxt:'약 120°', shape:'평면 삼각형', geo:'평면 삼각형', multi:'단일 결합 2개 + 이중 결합 1개'};
      }
      const c=st.c, t=st.t, nb=NB[c], nl=(VAL[c]-nb)/2, key=nb+','+nl;
      const formula = (c==='N'&&t==='H')? '\\ce{NH3}' : (c==='O'&&t==='H')? '\\ce{H2O}' : `\\ce{${c}${t}${nb}}`;
      const plain = (c==='N'&&t==='H')? 'NH3' : (c==='O'&&t==='H')? 'H2O' : `${c}${t}${nb}`;
      const ang = ANG[plain] || ANG0[key];
      const [bd,ld]=dirs(nb,nl,ang);
      return {tex:formula, name:plain, center:c, atoms:bd.map(v=>({el:t,v,o:1})), lone:ld, nb, nl, ang, angTxt:fmtA(ang), shape:SHAPE[key], geo:GEO[nb+nl], exc: c==='Be'||c==='B'};
    }
    function fmtA(a){ return (Math.round(a*2)/2).toString().replace(/\.0$/,'')+'°'; }

    function rot(v){
      const a=st.yaw*Math.PI/180, b=st.pitch*Math.PI/180;
      let [x,y,z]=v; [x,z]=[x*Math.cos(a)+z*Math.sin(a), -x*Math.sin(a)+z*Math.cos(a)];
      [y,z]=[y*Math.cos(b)-z*Math.sin(b), y*Math.sin(b)+z*Math.cos(b)];
      return [x,y,z];
    }

    function setLabels(){
      labels.forEach(l=>l.remove()); labels.length=0;
      if(!mol||mol.bad) return;
      const mkL=(el,lab)=>{ const d=document.createElement('div'); d.className='ov mid';
        const dark=['C','N','O','Cl'].includes(el); d.style.cssText=`font-size:${el==='H'?18:21}px;font-weight:700;color:${dark?'#fff':'#16233D'}`;
        d.innerHTML=API.tex(lab||`\\mathrm{${el}}`); fig.appendChild(d); labels.push(d); };
      mkL(mol.center, mol.cl); mol.atoms.forEach(a=>mkL(a.el,a.lab));
    }

    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      if(!mol) return;
      if(mol.bad){ API.atom(g,CX,CY,R.X,'X','-',true); labels.forEach(l=>API.place(l,0,0,false)); API.place(Ov('ang'),0,0,false); return; }
      const L=105, items=[], pos=[{x:CX,y:CY,z:0,r:R[mol.center]}];
      mol.atoms.forEach(a=>{ const v=rot(a.v), l=L*(a.el==='H'?.82:1); const x=CX+v[0]*l, y=CY-v[1]*l;
        pos.push({x,y,z:v[2],r:R[a.el]});
        items.push({z:v[2]*.5, k:0, f:()=>{ const dx=x-CX, dy=y-CY, n=Math.hypot(dx,dy)||1, px=-dy/n, py=dx/n;
          ({1:[0],2:[-4.5,4.5],3:[-7,0,7]})[a.o].forEach(o=>API.mk('line',{x1:CX+px*o,y1:CY+py*o,x2:x+px*o,y2:y+py*o,stroke:'#9AA5B1','stroke-width':a.o===1?7:5,'stroke-linecap':'round'},g)); }});
        items.push({z:v[2], k:2, f:()=>API.atom(g,x,y,R[a.el],a.el,'-',false)}); });
      if(I('lp').checked) mol.lone.forEach(d0=>{ const v=rot(d0), ll=L*.62, ex=v[0]*ll, ey=-v[1]*ll, pl=Math.hypot(ex,ey);
        items.push({z:v[2]*.6, k:1, f:()=>{ const ang=Math.atan2(ey,ex)*180/Math.PI, cx=CX+ex*.62, cy=CY+ey*.62;
          API.mk('ellipse',{cx,cy,rx:Math.max(pl*.62,20),ry:21,transform:`rotate(${ang} ${cx} ${cy})`,fill:'#E08A2C','fill-opacity':.18,stroke:'#E08A2C','stroke-width':1.5},g);
          const ux=pl>1e-6?ex/pl:1, uy=pl>1e-6?ey/pl:0, tip=pl>8?.85:0, bx=CX+ex*tip, by=CY+ey*tip;
          [-1,1].forEach(s=>API.mk('circle',{cx:bx-uy*6*s,cy:by+ux*6*s,r:4,fill:'#16233D'},g)); }}); });
      items.push({z:0, k:3, f:()=>API.atom(g,CX,CY,R[mol.center],mol.center,'-',false)});
      items.sort((p,q)=>p.z+.001*p.k-(q.z+.001*q.k)).forEach(it=>it.f());
      // 결합각 호 (결합 원자 0, 1)
      // 결합각 호: 라벨이 원자와 가장 덜 겹치는 두 결합을 고른다(바꿀 때는 15 px 이상 나아질 때만 — 깜빡임 방지)
      const lp=(i,j)=>{ const u=rot(mol.atoms[i].v), w=rot(mol.atoms[j].v), s=u.map((c,k)=>c+w[k]), n0=Math.hypot(...s);
        const m=n0<1e-6? rot([0,1,0]) : s.map(c=>c/n0); const x=CX+m[0]*40, y=CY-m[1]*40, vx=x-CX, vy=y-CY, n=Math.hypot(vx,vy)||1;
        return [CX+vx/n*(n+34), CY+vy/n*(n+34)]; };
      const sc=pr=>{ const [x,y]=lp(...pr); return Math.min(...pos.map(q=>Math.hypot(q.x-x,q.y-y)-q.r)); };
      if(mol.name==='HCHO') st.pair=[0,1];
      else { const prs=[]; for(let i=0;i<mol.atoms.length;i++) for(let j=i+1;j<mol.atoms.length;j++) prs.push([i,j]);
        const bestP=prs.reduce((p,q)=>sc(q)>sc(p)?q:p); if(!st.pair||st.pair[1]>=mol.atoms.length||sc(bestP)>sc(st.pair)+15) st.pair=bestP; }
      const [i0,i1]=st.pair, a=rot(mol.atoms[i0].v), b=rot(mol.atoms[i1].v), om=Math.acos(Math.max(-1,Math.min(1,dot(a,b)))), ra=40, pts=[];
      for(let k=0;k<=24;k++){ const t=k/24; let v;
        if(Math.abs(om-Math.PI)<1e-3){ const perp=rot([0,1,0]); v=a.map((c,i)=>c*Math.cos(Math.PI*t)+perp[i]*Math.sin(Math.PI*t)); }
        else { const s1=Math.sin((1-t)*om)/Math.sin(om), s2=Math.sin(t*om)/Math.sin(om); v=a.map((c,i)=>s1*c+s2*b[i]); }
        pts.push([CX+v[0]*ra, CY-v[1]*ra]); }
      API.mk('path',{d:'M'+pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L'),fill:'none',stroke:'#5B6B7F','stroke-width':2.2},g);
      const [lx,ly]=lp(i0,i1); API.place(Ov('ang'), lx, ly-12);
      // 원자 라벨: 앞 원자에 가려진 원자는 숨김
      labels.forEach((l,i)=>{ const p=pos[i], hid=pos.some((q,j)=>j!==i&&q.z>p.z+.05&&Math.hypot(q.x-p.x,q.y-p.y)<q.r*.85);
        API.place(l,p.x,p.y,!hid); });
    }

    function update(){
      mol=build(); st.pair=null;
      root.querySelectorAll('[data-c]').forEach(b=>b.classList.toggle('on',!st.p&&b.dataset.c===st.c));
      root.querySelectorAll('[data-t]').forEach(b=>{ b.classList.toggle('on',!st.p&&b.dataset.t===st.t); b.disabled=(BAD[st.c]||[]).includes(b.dataset.t); });
      root.querySelectorAll('[data-p]').forEach(b=>b.classList.toggle('on',st.p===b.dataset.p));
      Ov('f').innerHTML=API.tex(mol.tex); API.place(Ov('f'),16,10);
      if(mol.bad){
        O('pairs').textContent=`${mol.nb} · ${mol.nl}`; O('geo').textContent='—'; O('shape').textContent='—';
        O('msg').textContent=mol.bad; Ov('ang').textContent='';
      } else {
        O('pairs').textContent=`${mol.nb} · ${mol.nl}`; O('geo').textContent=mol.geo;
        O('shape').textContent=`${mol.shape} · ${mol.angTxt}`;
        Ov('ang').textContent=mol.angTxt;
        let msg = mol.nl===0 ? `비공유 전자쌍이 없어 분자 구조가 전자쌍 배치(${mol.geo})와 같다.`
          : `비공유 전자쌍 ${mol.nl}개가 공유 전자쌍을 더 세게 밀어 결합각이 109.5°보다 작다.`;
        if(mol.multi) msg=`${mol.multi} → 전자쌍 묶음 ${mol.nb}개. `+msg;
        if(mol.exc) msg+=` (${mol.center}는 옥텟 규칙의 예외)`;
        O('msg').textContent=msg;
      }
      setLabels(); draw();
    }

    // 버튼·입력
    root.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>{ st.mode=b.dataset.m;
      root.querySelectorAll('[data-m]').forEach(x=>x.classList.toggle('on',x===b));
      root.querySelector('[data-set="mol"]').style.display=st.mode==='mol'?'':'none';
      root.querySelector('[data-set="vsepr"]').style.display=st.mode==='vsepr'?'':'none'; update(); }));
    root.querySelectorAll('[data-c]').forEach(b=>b.addEventListener('click',()=>{ st.c=b.dataset.c; st.p=null; if((BAD[st.c]||[]).includes(st.t)) st.t='F'; update(); }));
    root.querySelectorAll('[data-t]').forEach(b=>b.addEventListener('click',()=>{ if(b.disabled) return; st.t=b.dataset.t; st.p=null; update(); }));
    root.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{ st.p=b.dataset.p; update(); }));
    ['nb','nl'].forEach(k=>I(k).addEventListener('input',update));
    I('lp').addEventListener('change',draw);
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${API.tex(r.tex)}</td><td>${r.nb}</td><td>${r.nl}</td><td>${r.ang}</td><td>${r.shape}</td>`; tb.appendChild(tr); }); }
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ if(!mol||mol.bad) return;
      // 측정: 모형 좌표에서 첫 두 결합 사이의 각을 잰다
      const [i0,i1]=st.pair||[0,1], m=Math.acos(dot(norm(mol.atoms[i0].v),norm(mol.atoms[i1].v)))*180/Math.PI;
      const ang = mol.name==='HCHO' ? '약 120°' : fmtA(m);
      log.push({tex:mol.tex,nb:mol.nb,nl:mol.nl,ang,shape:mol.shape}); if(log.length>4) log.shift(); renderLog(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); st={...st,mode:'mol',c:'C',t:'H',p:null,yaw:25,pitch:-16};
      root.querySelectorAll('[data-m]').forEach(x=>x.classList.toggle('on',x.dataset.m==='mol'));
      root.querySelector('[data-set="mol"]').style.display=''; root.querySelector('[data-set="vsepr"]').style.display='none';
      I('nb').value=3; I('nl').value=1; I('lp').checked=true; update(); });
    // 끌어서 회전
    svg.style.touchAction='none'; svg.style.cursor='grab';
    svg.addEventListener('pointerdown',e=>{ st.drag={x:e.clientX,y:e.clientY}; svg.setPointerCapture(e.pointerId); svg.style.cursor='grabbing'; API.place(Ov('hint'),0,0,false); });
    svg.addEventListener('pointermove',e=>{ if(!st.drag) return; const sc=fig.getBoundingClientRect().width/W||1;
      st.yaw+=(e.clientX-st.drag.x)/sc*.6; st.pitch=API.clamp(st.pitch-(e.clientY-st.drag.y)/sc*.6,-85,85);
      st.drag={x:e.clientX,y:e.clientY}; draw(); });
    const up=()=>{ st.drag=null; st.idle=0; svg.style.cursor='grab'; };
    svg.addEventListener('pointerup',up); svg.addEventListener('pointercancel',up);
    API.place(Ov('hint'),W-80,H-28);
    API.ready(()=>update());
    update();
    if(!window.__STILL) API.loop(root,dt=>{ if(st.drag) return; st.idle+=dt; if(st.idle>1.5){ st.yaw+=dt*18; draw(); } });
  }
};
