/* 고급화학 2-2-1 — 실험실 (a·b 같은 파일)
   ac221vp : 물의 증기압 측정(필수 탐구 고화-탐11, a) · 증기압 → 증발열(고화-탐13, b) — data-mode="pt"|"cc"로 처음 그래프만 다름
     · 증기압: 앙투안 식 log10 P(mmHg) = A − B/(C + t) (물 8.07131/1730.63/233.426, 에탄올 8.20417/1642.89/230.300, 다이에틸 에터 6.92032/1064.07/228.80) × 0.133322 → kPa
     · 공기 방울(설계 오류): P_공기 = 1.2 kPa × (t+273.15)/293.15 를 더함
     · 측정값 = 참값 × (1 + N(0, 0.6 %)) — 고정 시드, 101.3 kPa를 넘으면 피스톤이 밀려 측정 불가(끓음)
     · ln P–1/T 그래프: 같은 액체 3점 이상이면 최소 제곱 직선, ΔH = −기울기 × 8.314
   ac221st : 표면 장력 측정(필수 탐구 고화-탐12, a)
     · γ(t) = γ20 + (dγ/dT)(t − 20) — 물 0.0728/−1.55e-4, 에탄올 0.0223/−0.83e-4, 아세톤 0.0237/−1.12e-4, 글리세롤 0.0634/−0.60e-4, 헥세인 0.0184/−1.02e-4 (N/m)
     · l = πd, F_max = 2lγ, 저울 감소량 Δm = F_max/g (g = 9.80) × (1 + N(0, 0.5 %)) 0.001 g, γ측정 = Δm·g/(2l)
     · 모세관(계산 모형): h = 2γ/(ρ g r) (접촉각 0, 유리를 적시는 액체) */
(function(){
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=Math.imul(a^(a>>>15),1|a); t=(t+Math.imul(t^(t>>>7),61|t))^t; return ((t^(t>>>14))>>>0)/4294967296; }; }
function gauss(r){ let u=0,v=0; while(u===0)u=r(); v=r(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||18,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
function fitL(pts){ const n=pts.length, mx=pts.reduce((a,p)=>a+p[0],0)/n, my=pts.reduce((a,p)=>a+p[1],0)/n;
  let sxx=0,sxy=0,syy=0; pts.forEach(p=>{ sxx+=(p[0]-mx)**2; sxy+=(p[0]-mx)*(p[1]-my); syy+=(p[1]-my)**2; });
  const b=sxy/sxx, a=my-b*mx, r2=syy>0?(sxy*sxy)/(sxx*syy):1; return {a,b,r2}; }
const LQ={water:{n:'물',A:8.07131,B:1730.63,C:233.426,col:'#1F6FD1'},ethanol:{n:'에탄올',A:8.20417,B:1642.89,C:230.300,col:'#2E9E6A'},ether:{n:'다이에틸 에터',A:6.92032,B:1064.07,C:228.80,col:'#E08A2C'}};
const pk=(l,t)=>Math.pow(10,LQ[l].A-LQ[l].B/(LQ[l].C+t))*0.133322;
const fmtP=p=>p<10?p.toFixed(2):p.toFixed(1);
const ST={water:{n:'물',g:0.0728,dg:-1.55e-4,rho:998},ethanol:{n:'에탄올',g:0.0223,dg:-0.83e-4,rho:789},acetone:{n:'아세톤',g:0.0237,dg:-1.12e-4,rho:784},glycerol:{n:'글리세롤',g:0.0634,dg:-0.60e-4,rho:1261},hexane:{n:'헥세인',g:0.0184,dg:-1.02e-4,rho:655}};

window.DECK_LABS = {
  ac221vp(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=root.querySelector('.lab-fig svg'), app=root.querySelector('svg.ac221-app');
    const MODE0=root.dataset.mode||'pt';
    let st={liq:'water',mode:MODE0}, log=[], rnd=rng(88);
    // ── 장치 그림(정적)
    const a0=API.mk('g',{},app);
    const bath=API.mk('rect',{x:8,y:40,width:292,height:84,rx:6,fill:'#E3EEFB',stroke:'#7E8B98','stroke-width':2},a0);
    API.mk('rect',{x:40,y:68,width:190,height:30,rx:3,fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':2},a0);
    API.mk('rect',{x:42,y:70,width:26,height:26,fill:'#DDEEF8'},a0);
    API.mk('rect',{x:224,y:64,width:9,height:38,fill:'#C9D2DB',stroke:'#16233D','stroke-width':1.5},a0);
    API.mk('line',{x1:233,y1:83,x2:292,y2:83,stroke:'#16233D','stroke-width':4},a0);
    API.mk('path',{d:'M40 83 L22 83 L22 12 L360 12 L360 20',fill:'none',stroke:'#5B6B7F','stroke-width':3},a0);
    API.mk('circle',{cx:360,cy:62,r:42,fill:'#FFFFFF',stroke:'#16233D','stroke-width':2.5},a0);
    for(let i=0;i<=6;i++){ const ang=(-210+i*40)*Math.PI/180, c=Math.cos(ang), s=Math.sin(ang);
      API.mk('line',{x1:360+34*c,y1:62+34*s,x2:360+40*c,y2:62+40*s,stroke:'#5B6B7F','stroke-width':1.5},a0); }
    txt(API,a0,360,96,'kPa',{size:18,fill:'#5B6B7F'});
    API.mk('line',{x1:270,y1:30,x2:270,y2:112,stroke:'#7E8B98','stroke-width':4,'stroke-linecap':'round'},a0);
    API.mk('circle',{cx:270,cy:114,r:6,fill:'#D7263D'},a0);
    const needle=API.mk('line',{x1:360,y1:62,x2:360,y2:30,stroke:'#D7263D','stroke-width':3,'stroke-linecap':'round'},a0);
    API.mk('circle',{cx:360,cy:62,r:4,fill:'#16233D'},a0);
    const air=API.mk('circle',{cx:80,cy:78,r:5,fill:'#FFFFFF',stroke:'#5B6B7F','stroke-width':1.5},a0);
    const gm=API.mk('g',{},app); const mols=[];
    for(let i=0;i<30;i++) mols.push({x:74+rnd()*144,y:72+rnd()*22,vx:(rnd()-.5)*60,vy:(rnd()-.5)*60,el:API.mk('circle',{r:3.2,fill:'#F2A65A',stroke:'#B4561C','stroke-width':1},gm)});
    // ── 그래프
    const g=API.mk('g',{},svg); const X0=70,Y0=222,W=500,H=180;
    function cur(){ const t=+I('t').value, pv=pk(st.liq,t), pa=I('air').checked?1.2*(t+273.15)/293.15:0; return {t,pv,pa,P:pv+pa}; }
    function axes(){
      const pt=st.mode==='pt';
      const xs=pt?[0,20,40,60,80,100]:[2.7,2.9,3.1,3.3,3.5], ys=pt?[0,20,40,60,80,100]:[0,1,2,3,4,5];
      const xr=pt?[0,100]:[2.7,3.6], yr=pt?[0,110]:[-0.6,5.2];
      const X=v=>X0+(v-xr[0])/(xr[1]-xr[0])*W, Y=v=>Y0-(v-yr[0])/(yr[1]-yr[0])*H;
      xs.forEach(v=>{ API.mk('line',{x1:X(v),y1:Y0,x2:X(v),y2:Y0-H,stroke:'#E2E7EC','stroke-width':1},g); txt(API,g,X(v),Y0+22,pt?String(v):v.toFixed(1),{size:18}); });
      ys.forEach(v=>{ API.mk('line',{x1:X0,y1:Y(v),x2:X0+W,y2:Y(v),stroke:'#E2E7EC','stroke-width':1},g); txt(API,g,X0-8,Y(v)+6,String(v),{size:18,anchor:'end'}); });
      API.mk('line',{x1:X0,y1:Y0,x2:X0+W+6,y2:Y0,stroke:'#5B6B7F','stroke-width':2},g); API.mk('line',{x1:X0,y1:Y0,x2:X0,y2:Y0-H-6,stroke:'#5B6B7F','stroke-width':2},g);
      API.place(V('xpt'),X0+W-70,Y0-32,pt); API.place(V('ypt'),X0+90,2,pt); API.place(V('xcc'),X0+W-90,Y0-32,!pt); API.place(V('ycc'),X0+90,2,!pt);
      return {X,Y,pt};
    }
    function draw(){
      g.innerHTML=''; const c=cur(), A=axes(), L=LQ[st.liq];
      O('t').textContent=c.t+' °C';
      root.querySelectorAll('[data-liq]').forEach(b=>b.classList.toggle('on',b.dataset.liq===st.liq));
      root.querySelectorAll('[data-act="pt"],[data-act="cc"]').forEach(b=>b.classList.toggle('on',b.dataset.act===st.mode));
      // 장치
      const w=Math.min(1,(c.t-10)/80); bath.setAttribute('fill',`rgb(${Math.round(227+26*w)},${Math.round(238-12*w)},${Math.round(251-23*w)})`);
      const over=c.P>101.3, ang=(-210+Math.min(c.P,120)/120*240)*Math.PI/180;
      needle.setAttribute('x2',360+32*Math.cos(ang)); needle.setAttribute('y2',62+32*Math.sin(ang));
      air.setAttribute('visibility',I('air').checked?'visible':'hidden');
      const nm=Math.max(1,Math.min(30,Math.round(c.pv/101.3*30+1)));
      mols.forEach((m,i)=>m.el.setAttribute('visibility',i<nm?'visible':'hidden'));
      O('big').textContent=over?'101.3 kPa 초과':(fmtP(c.P)+' kPa');
      // 그래프 점
      if(A.pt){ API.mk('line',{x1:X0,y1:A.Y(101.3),x2:X0+W,y2:A.Y(101.3),stroke:'#5B6B7F','stroke-width':1.5,'stroke-dasharray':'6 4'},g); txt(API,g,X0+W-4,A.Y(101.3)-6,'대기압 101.3 kPa',{size:18,anchor:'end',fill:'#5B6B7F'}); }
      let fitMsg='';
      Object.keys(LQ).forEach(k=>{
        const rows=log.filter(r=>r.liq===k).sort((a,b)=>a.t-b.t); if(!rows.length) return;
        const col=LQ[k].col, pts=rows.map(r=>A.pt?[A.X(r.t),A.Y(r.P)]:[A.X(r.it),A.Y(r.ln)]);
        if(A.pt&&pts.length>1) API.mk('polyline',{points:pts.map(p=>p.join(',')).join(' '),fill:'none',stroke:col,'stroke-width':2.5},g);
        if(!A.pt&&rows.length>=3){ const F=fitL(rows.map(r=>[r.it,r.ln])), x1=2.72, x2=3.58;
          API.mk('line',{x1:A.X(x1),y1:A.Y(F.a+F.b*x1),x2:A.X(x2),y2:A.Y(F.a+F.b*x2),stroke:col,'stroke-width':2.5,'stroke-dasharray':'8 5'},g);
          const dH=-F.b*1000*8.314/1000;
          if(k===st.liq) fitMsg=` 추세선 기울기 ${Math.round(F.b*1000)} K (결정 계수 ${F.r2.toFixed(4)}) → 증발열 ΔH = ${dH.toFixed(1)} kJ/mol.`; }
        pts.forEach(p=>API.mk('circle',{cx:p[0],cy:p[1],r:5.5,fill:'#FFFFFF',stroke:col,'stroke-width':2.5},g));
      });
      // 문장
      let m;
      if(over) m=`${L.n}의 증기압이 대기압보다 커져 피스톤이 밀려 나간다 — 이 온도에서는 끓으므로 측정할 수 없다.`;
      else m=`${L.n} ${c.t} °C: 증기압 ${fmtP(c.pv)} kPa`+(c.pa?` + 공기 ${c.pa.toFixed(1)} kPa (공기 방울 때문에 크게 읽힘)`:'')+'.';
      if(A.pt) m+=' 「측정·기록」으로 여러 온도를 재어 증기압 곡선을 그리자.';
      else m+= fitMsg || ` 같은 액체를 3개 온도 이상 기록하면 추세선과 증발열이 나온다.`;
      if(!A.pt&&fitMsg&&I('air').checked) m+=' 공기 방울이 있으면 기울기가 완만해져 증발열이 작게 나온다.';
      O('msg').textContent=m;
      O('log').innerHTML=log.slice(-4).map((r,i)=>`<tr><td>${log.length-Math.min(4,log.length)+i+1}</td><td>${LQ[r.liq].n}</td><td>${r.t}</td><td>${fmtP(r.P)}</td><td>${r.it.toFixed(3)}</td><td>${r.ln.toFixed(3)}</td></tr>`).join('');
    }
    root.querySelectorAll('[data-liq]').forEach(b=>b.addEventListener('click',()=>{ st.liq=b.dataset.liq; draw(); }));
    I('t').addEventListener('input',draw); I('air').addEventListener('change',draw);
    root.querySelector('[data-act="pt"]').addEventListener('click',()=>{ st.mode='pt'; draw(); });
    root.querySelector('[data-act="cc"]').addEventListener('click',()=>{ st.mode='cc'; draw(); });
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const c=cur(); if(c.P>101.3){ draw(); return; }
      const P=Math.round(c.P*(1+0.006*gauss(rnd))*(c.P<10?100:10))/(c.P<10?100:10), T=c.t+273.15;
      log=log.filter(r=>!(r.liq===st.liq&&r.t===c.t)); log.push({liq:st.liq,t:c.t,P,it:1000/T,ln:Math.log(P)}); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; rnd=rng(88); st={liq:'water',mode:MODE0}; I('t').value=20; I('air').checked=false; draw(); });
    draw();
    API.loop(root,(dt)=>{ const c=cur(), sp=0.6+Math.min(c.t,90)/60;
      mols.forEach(m=>{ m.x+=m.vx*sp*dt; m.y+=m.vy*sp*dt; if(m.x<72){m.x=72;m.vx=Math.abs(m.vx);} if(m.x>220){m.x=220;m.vx=-Math.abs(m.vx);} if(m.y<72){m.y=72;m.vy=Math.abs(m.vy);} if(m.y>94){m.y=94;m.vy=-Math.abs(m.vy);} m.el.setAttribute('cx',m.x.toFixed(1)); m.el.setAttribute('cy',m.y.toFixed(1)); }); });
    mols.forEach(m=>{ m.el.setAttribute('cx',m.x.toFixed(1)); m.el.setAttribute('cy',m.y.toFixed(1)); });
  },

  ac221st(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('.lab-fig svg');
    let st={liq:'water'}, log=[], rnd=rng(91), anim=null, lastDm=null;
    const s0=API.mk('g',{},svg);
    // 스탠드·도르래
    API.mk('line',{x1:40,y1:24,x2:300,y2:24,stroke:'#16233D','stroke-width':4},s0); API.mk('line',{x1:56,y1:24,x2:56,y2:250,stroke:'#16233D','stroke-width':4},s0);
    API.mk('circle',{cx:220,cy:40,r:13,fill:'#E9ECEF',stroke:'#16233D','stroke-width':2.5},s0);
    txt(API,s0,252,46,'도르래',{size:18,anchor:'start',fill:'#5B6B7F'});
    // 비커
    API.mk('path',{d:'M150 120 L150 206 Q150 214 158 214 L292 214 Q300 214 300 206 L300 120',fill:'none',stroke:'#7E8B98','stroke-width':2.5},s0);
    const liq=API.mk('rect',{x:152,y:150,width:146,height:62,fill:'#DDEEF8'},s0);
    API.mk('line',{x1:152,y1:150,x2:298,y2:150,stroke:'#9FC3DD','stroke-width':2},s0);
    // 저울
    API.mk('rect',{x:120,y:214,width:210,height:44,rx:6,fill:'#F1F3F5',stroke:'#16233D','stroke-width':2.5},s0);
    API.mk('rect',{x:175,y:224,width:100,height:26,rx:3,fill:'#16233D'},s0);
    const rd=txt(API,s0,225,244,'0.000 g',{size:18,fill:'#9BE7A6'});
    // 움직이는 부분: 실·원통·액체 막
    const gm=API.mk('g',{},svg);
    const str1=API.mk('line',{x1:233,y1:40,x2:233,y2:120,stroke:'#16233D','stroke-width':1.5},gm);
    API.mk('line',{x1:207,y1:40,x2:120,y2:24,stroke:'#16233D','stroke-width':1.5},gm);
    const cyl=API.mk('g',{},gm);
    API.mk('line',{x1:233,y1:120,x2:203,y2:140,stroke:'#16233D','stroke-width':1.3},cyl); API.mk('line',{x1:233,y1:120,x2:263,y2:140,stroke:'#16233D','stroke-width':1.3},cyl);
    API.mk('rect',{x:201,y:140,width:64,height:10,fill:'none',stroke:'#8C99A6','stroke-width':3},cyl);
    const film=API.mk('path',{d:'',fill:'#BFDDF2',stroke:'#9FC3DD','stroke-width':1.5},gm);
    // 모세관
    const s1=API.mk('g',{},svg);
    API.mk('rect',{x:440,y:196,width:150,height:50,fill:'#DDEEF8',stroke:'#7E8B98','stroke-width':2},s1);
    const tube=API.mk('rect',{x:507,y:24,width:16,height:212,fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':2},s1);
    const col=API.mk('path',{d:'',fill:'#DDEEF8',stroke:'#9FC3DD','stroke-width':1.5},s1);
    const ht=txt(API,s1,515,262,'',{size:18}); txt(API,s1,445,40,'모세관',{size:18,anchor:'start',fill:'#5B6B7F'});
    const hl=API.mk('line',{x1:538,y1:196,x2:538,y2:196,stroke:'#E08A2C','stroke-width':2.5},s1);
    const gam=(l,t)=>ST[l].g+ST[l].dg*(t-20);
    function setLift(p){ // p 0–1: 당김 진행
      const lift=p*26, y=140-lift, det=p>0.86;
      cyl.setAttribute('transform',`translate(0 ${-lift})`); str1.setAttribute('y2',120-lift);
      if(!det&&p>0){ const top=150-lift+10, d=`M201 ${top} L196 150 L270 150 L265 ${top} Z`; film.setAttribute('d',d); film.setAttribute('visibility','visible'); }
      else film.setAttribute('visibility','hidden');
      return det;
    }
    function show(){
      const t=+I('t').value, d=+I('d').value, rr=+I('r').value, L=ST[st.liq], gg=gam(st.liq,t);
      O('t').textContent=t+' °C'; O('d').textContent=d.toFixed(1)+' cm'; O('r').textContent=rr.toFixed(1)+' mm';
      root.querySelectorAll('[data-liq]').forEach(b=>b.classList.toggle('on',b.dataset.liq===st.liq));
      // 모세관 높이 (mm) = 2γ/(ρ g r)
      const r=rr/2/1000, h=2*gg/(L.rho*9.80*r)*1000, px=Math.min(h*2.2,170), top=196-px, w=Math.max(4,rr*6);
      tube.setAttribute('x',515-w/2-2); tube.setAttribute('width',w+4);
      col.setAttribute('d',`M${515-w/2} 236 L${515-w/2} ${top} Q515 ${top+w*0.8} ${515+w/2} ${top} L${515+w/2} 236 Z`);
      hl.setAttribute('y1',top); hl.setAttribute('y2',196); ht.textContent=`h ≈ ${h.toFixed(1)} mm`;
      O('log').innerHTML=log.slice(-4).map((x,i)=>`<tr><td>${log.length-Math.min(4,log.length)+i+1}</td><td>${ST[x.liq].n}</td><td>${x.t}</td><td>${x.l.toFixed(3)}</td><td>${x.F.toFixed(4)}</td><td>${x.g.toFixed(4)}</td><td>${x.lit.toFixed(4)}</td></tr>`).join('');
      return {t,d,gg,h,L};
    }
    function idle(){ anim=null; lastDm=null; setLift(0); rd.textContent='0.000 g'; O('big').textContent='—';
      const c=show(); O('msg').textContent=`${c.L.n} ${c.t} °C. 「천천히 당기기」로 원통이 떨어지기 직전의 저울 감소량을 재자. 이 관에서는 모세관 높이 약 ${c.h.toFixed(0)} mm(계산 모형).`; }
    function pull(){
      const c=show(), l=Math.PI*c.d/100, F=2*l*c.gg, dm=Math.round(F/9.80*1000*(1+0.005*gauss(rnd))*1000)/1000;
      const Fm=dm/1000*9.80, gm_=Fm/(2*l), er=(gm_-c.gg)/c.gg*100;
      log.push({liq:st.liq,t:c.t,l,F:Fm,g:gm_,lit:c.gg}); lastDm=dm; show();
      O('big').textContent=gm_.toFixed(4)+' N/m';
      const same=log.filter(x=>x.liq!==st.liq); let cmp='';
      if(same.length){ const o=same[same.length-1]; cmp=` 앞서 잰 ${ST[o.liq].n}(${o.g.toFixed(4)} N/m)보다 ${gm_>o.g?'크다':'작다'}.`; }
      O('msg').textContent=`저울 감소량 최대 ${dm.toFixed(3)} g → 최대 힘 ${Fm.toFixed(4)} N, γ = ${gm_.toFixed(4)} N/m (문헌값 ${c.gg.toFixed(4)}, 차이 ${er>=0?'+':''}${er.toFixed(1)} %).`+cmp+` 모세관 높이 약 ${c.h.toFixed(0)} mm.`;
      anim={p:0,dm};
    }
    root.querySelectorAll('[data-liq]').forEach(b=>b.addEventListener('click',()=>{ st.liq=b.dataset.liq; idle(); }));
    ['t','d','r'].forEach(k=>I(k).addEventListener('input',idle));
    root.querySelector('[data-act="pull"]').addEventListener('click',pull);
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; rnd=rng(91); st.liq='water'; I('t').value=20; I('d').value=6.6; I('r').value=1.0; idle(); });
    idle();
    API.loop(root,(dt)=>{ if(!anim) return; anim.p=Math.min(1,anim.p+dt/2.4);
      const det=setLift(anim.p); rd.textContent=det?`최대 −${anim.dm.toFixed(3)} g`:`−${(anim.dm*Math.min(1,anim.p/0.86)).toFixed(3)} g`;
      if(anim.p>=1) anim=null; });
  }
};
})();
