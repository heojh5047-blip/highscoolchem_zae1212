/* 고급화학 2-1-1a — 실험실
   ac211spd  : 속력 분포 (지도서 디지털 탐구 Ⅱ-1 ◆)
     · f(v) = 4π (M/2πRT)^{3/2} v² exp(−Mv²/2RT)  (M kg/mol, R 8.314) = 교과서 식(m/k_B)과 같음
     · v_p = √(2RT/M), v_rms = √(3RT/M), v>1000 m/s 분율 = 1 − erf(x) + (2x/√π)e^{−x²}, x = 1000/v_p
     · 곡선 고정(최대 3개)·기록 표(최근 6행)·상자 속 분자 40개(속도 성분 정규 분포, 고정 시드)
   ac211gasR : 기체 상수 측정 (필수 탐구 고화-탐09)
     · 2KClO3 → 2KCl + 3O2, n(O2) = m/122.55 × 3/2 × 분해율(0.985–1), 실제 V = nRT/P_O2 (T = t+273.15, R 0.082057)
     · 측정값: 질량 감소 ×(1+N(0,0.4 %)), 부피 ×(1+N(0,0.6 %)) 1 mL 단위 — 고정 시드
     · 계산: P = (대기압 − 수증기압)/760 (보정 끔이면 대기압/760), T = t + 273, R = PV/(nT) */
(function(){
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=Math.imul(a^(a>>>15),1|a); t=(t+Math.imul(t^(t>>>7),61|t))^t; return ((t^(t>>>14))>>>0)/4294967296; }; }
function gauss(r){ let u=0,v=0; while(u===0)u=r(); v=r(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
function erf(x){ const t=1/(1+0.3275911*x); return 1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-x*x); }
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||18,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
const RG=8.314;
const GASES={He:{n:'헬륨',M:4.00},N2:{n:'질소',M:28.02},O2:{n:'산소',M:32.00},CO2:{n:'이산화 탄소',M:44.01}};
const PW={15:12.8,16:13.6,17:14.5,18:15.5,19:16.5,20:17.5,21:18.7,22:19.8,23:21.1,24:22.4,25:23.8,26:25.2,27:26.7,28:28.3,29:30.0,30:31.8};

window.DECK_LABS = {
  ac211spd(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('.lab-fig svg'), box=root.querySelector('svg.ac211-box');
    let st={gas:'N2'}, pins=[], log=[], rnd=rng(20261119);
    const g=API.mk('g',{},svg), gb=API.mk('g',{},box);
    const X0=70,Y0=250,W=500,H=210;
    const f=(v,T,M)=>{ const a=M/1000/(2*RG*T); return 4*Math.PI*Math.pow(a/Math.PI,1.5)*v*v*Math.exp(-a*v*v); };
    const vp=(T,M)=>Math.sqrt(2*RG*T/(M/1000)), vr=(T,M)=>Math.sqrt(3*RG*T/(M/1000));
    const fast=(T,M)=>{ const x=1000/vp(T,M); return 1-erf(x)+2*x/Math.sqrt(Math.PI)*Math.exp(-x*x); };
    // 분자 40개
    const N=40, mol=[]; for(let i=0;i<N;i++) mol.push({x:10+rnd()*400,y:10+rnd()*76,ux:gauss(rnd),uy:gauss(rnd),uz:gauss(rnd),el:API.mk('circle',{r:5,stroke:'#B4561C','stroke-width':1},gb)});
    function cur(){ return {gas:st.gas,T:+I('T').value,M:GASES[st.gas].M}; }
    function nice(x){ for(const c of [1000,1500,2000,3000,4000,5000,6000]) if(c>=x) return c; return 8000; }
    function draw(){
      const c=cur(); O('T').textContent=c.T+' K';
      root.querySelectorAll('[data-gas]').forEach(b=>b.classList.toggle('on',b.dataset.gas===st.gas));
      while(g.firstChild) g.removeChild(g.firstChild);
      const all=pins.concat([c]);
      const xm=nice(Math.max(...all.map(p=>3.2*vp(p.T,p.M)))), fmax=Math.max(...all.map(p=>f(vp(p.T,p.M),p.T,p.M)));
      const ym=Math.ceil(fmax*1.15/0.0005)*0.0005;
      const X=v=>X0+v/xm*W, Y=y=>Y0-y/ym*H;
      for(let i=0;i<=5;i++){ const v=xm*i/5; API.mk('line',{x1:X(v),y1:Y0,x2:X(v),y2:Y0-H,stroke:'#E2E7EC'},g); txt(API,g,X(v),Y0+22,String(Math.round(v))); }
      const ny=Math.round(ym/0.0005); const stp=ny>8?2:1;
      for(let i=0;i<=ny;i+=stp){ const y=i*0.0005; API.mk('line',{x1:X0,y1:Y(y),x2:X0+W,y2:Y(y),stroke:'#E2E7EC'},g); txt(API,g,X0-8,Y(y)+6,y===0?'0':y.toFixed(4),{anchor:'end'}); }
      API.mk('line',{x1:X0,y1:Y0,x2:X0+W+8,y2:Y0,stroke:'#5B6B7F','stroke-width':2},g); API.mk('line',{x1:X0,y1:Y0,x2:X0,y2:Y0-H-8,stroke:'#5B6B7F','stroke-width':2},g);
      txt(API,g,X0+W,Y0+44,'속력 v (m/s)',{anchor:'end',fill:'#5B6B7F'}); txt(API,g,6,22,'f(v) (s/m)',{anchor:'start',fill:'#5B6B7F'});
      // 1000 m/s 경계
      if(1000<xm){ API.mk('line',{x1:X(1000),y1:Y0,x2:X(1000),y2:Y0-H,stroke:'#E08A2C','stroke-width':1.5,'stroke-dasharray':'5 4'},g); txt(API,g,X(1000)+4,Y0-H+14,'1000 m/s',{anchor:'start',fill:'#E08A2C'}); }
      const path=(p,col,w,dash)=>{ const pts=[]; for(let i=0;i<=200;i++){ const v=xm*i/200; pts.push(X(v).toFixed(1)+' '+Y(f(v,p.T,p.M)).toFixed(1)); } return API.mk('path',{d:'M'+pts.join(' L'),fill:'none',stroke:col,'stroke-width':w,...(dash?{'stroke-dasharray':dash}:{})},g); };
      // 현재 곡선의 1000 m/s 초과 음영
      { const pts=[]; for(let i=0;i<=120;i++){ const v=1000+(xm-1000)*i/120; pts.push(X(v).toFixed(1)+' '+Y(f(v,c.T,c.M)).toFixed(1)); }
        if(1000<xm) API.mk('path',{d:`M${X(1000)} ${Y0} L`+pts.join(' L')+` L${X(xm)} ${Y0} Z`,fill:'#FFE45C','fill-opacity':.35,stroke:'none'},g); }
      pins.forEach((p,i)=>{ path(p,'#5B6B7F',2.2,'7 5'); const v=vp(p.T,p.M); txt(API,g,X(v)+6,Y(f(v,p.T,p.M))-8,`${GASES[p.gas].n} ${p.T} K`,{anchor:'start',fill:'#5B6B7F'}); });
      path(c,'#16233D',3.5); const v0=vp(c.T,c.M);
      API.mk('circle',{cx:X(v0),cy:Y(f(v0,c.T,c.M)),r:5,fill:'#E08A2C'},g);
      txt(API,g,X(v0)+8,Y(f(v0,c.T,c.M))-10,`${GASES[c.gas].n} ${c.T} K`,{anchor:'start',w:700});
      const vrms=vr(c.T,c.M);
      O('big').textContent=Math.round(vrms)+' m/s';
      let m=`최빈 속력 ${Math.round(v0)} m/s, 봉우리 높이 ${f(v0,c.T,c.M).toFixed(5)} s/m, 1000 m/s보다 빠른 분자 ${(100*fast(c.T,c.M)).toFixed(1)} %.`;
      if(pins.length){ const p=pins[pins.length-1]; const rv=v0/vp(p.T,p.M), rh=f(v0,c.T,c.M)/f(vp(p.T,p.M),p.T,p.M);
        m+=` 고정한 곡선(${GASES[p.gas].n} ${p.T} K)보다 봉우리 속력 ${rv.toFixed(2)}배, 높이 ${rh.toFixed(2)}배 — 넓이는 둘 다 1.`; }
      else m+=' 「곡선 고정」 뒤 온도나 기체를 바꾸어 비교하자.';
      O('msg').textContent=m;
      O('log').innerHTML=log.map(r=>`<tr><td>${r.n}</td><td>${r.T}</td><td>${r.vp}</td><td>${r.vr}</td><td>${r.h}</td><td>${r.fa}</td></tr>`).join('');
    }
    root.querySelectorAll('[data-gas]').forEach(b=>b.addEventListener('click',()=>{st.gas=b.dataset.gas;draw();}));
    I('T').addEventListener('input',draw);
    root.querySelector('[data-act="pin"]').addEventListener('click',()=>{ const c=cur(); if(!pins.some(p=>p.gas===c.gas&&p.T===c.T)){ pins.push(c); if(pins.length>3) pins.shift(); } draw(); });
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const c=cur(), v=vp(c.T,c.M);
      log.push({n:GASES[c.gas].n,T:c.T,vp:Math.round(v),vr:Math.round(vr(c.T,c.M)),h:f(v,c.T,c.M).toFixed(5),fa:(100*fast(c.T,c.M)).toFixed(1)+' %'}); if(log.length>6) log.shift(); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ pins=[]; log=[]; st.gas='N2'; I('T').value=300; draw(); });
    draw();
    API.loop(root,(dt)=>{
      const c=cur(), s=Math.sqrt(RG*c.T/(c.M/1000)); // 성분 표준 편차 (m/s)
      const k=0.05; // 화면 px/s per m/s
      mol.forEach(p=>{
        const vx=p.ux*s, vy=p.uy*s, sp=s*Math.sqrt(p.ux*p.ux+p.uy*p.uy+p.uz*p.uz);
        p.x+=vx*k*dt; p.y+=vy*k*dt;
        if(p.x<6){p.x=6;p.ux=Math.abs(p.ux);} if(p.x>414){p.x=414;p.ux=-Math.abs(p.ux);}
        if(p.y<6){p.y=6;p.uy=Math.abs(p.uy);} if(p.y>90){p.y=90;p.uy=-Math.abs(p.uy);}
        p.el.setAttribute('cx',p.x.toFixed(1)); p.el.setAttribute('cy',p.y.toFixed(1)); p.el.setAttribute('fill',sp>1000?'#D7263D':'#F2A65A');
      });
    });
    mol.forEach(p=>{ p.el.setAttribute('cx',p.x.toFixed(1)); p.el.setAttribute('cy',p.y.toFixed(1)); p.el.setAttribute('fill','#F2A65A'); });
  },

  ac211gasR(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('.lab-fig svg');
    let log=[], rnd=rng(79), last=null;
    // 정적: 수조·실린더(500 mL)
    const s0=API.mk('g',{},svg);
    API.mk('rect',{x:250,y:150,width:300,height:90,rx:6,fill:'#DDEEF8',stroke:'#7E8B98','stroke-width':2},s0);
    API.mk('line',{x1:252,y1:168,x2:548,y2:168,stroke:'#9FC3DD','stroke-width':2},s0);
    API.mk('rect',{x:370,y:18,width:60,height:200,fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':2.2},s0);
    for(let i=0;i<=10;i++){ API.mk('line',{x1:370,y1:200-i*17,x2:i%2?380:388,y2:200-i*17,stroke:'#5B6B7F','stroke-width':1.2},s0); if(i%2===0) txt(API,s0,394,200-i*17+6,String(i*50),{anchor:'start',size:16,fill:'#5B6B7F'}); }
    API.mk('path',{d:'M60 110 L40 70 L40 40 L250 40 L250 214 L392 214',fill:'none',stroke:'#16233D','stroke-width':3},s0);
    API.mk('rect',{x:46,y:104,width:110,height:34,rx:16,fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':2,transform:'rotate(-18 100 120)'},s0);
    txt(API,s0,104,172,'시료 + 촉매',{size:17,fill:'#5B6B7F'});
    const g=API.mk('g',{},svg), water=API.mk('rect',{x:371,y:19,width:58,height:198,fill:'#DDEEF8'},g), lvl=API.mk('line',{x1:370,x2:430,stroke:'#9FC3DD','stroke-width':2},g);
    const tx=[txt(API,g,470,40,'',{anchor:'start',size:19}),txt(API,g,470,66,'',{anchor:'start',size:19}),txt(API,g,470,92,'',{anchor:'start',size:19}),txt(API,g,470,118,'',{anchor:'start',size:19})];
    txt(API,s0,30,224,'시험관 질량 감소 = 산소 질량',{anchor:'start',size:17,fill:'#5B6B7F'});
    function setLevel(mL){ const y=200-Math.min(mL,500)/50*17; water.setAttribute('y',y); water.setAttribute('height',217-y); lvl.setAttribute('y1',y); lvl.setAttribute('y2',y); }
    function show(){
      const m=+I('m').value, t=+I('t').value, pa=+I('pa').value;
      O('m').textContent=m.toFixed(2)+' g'; O('t').textContent=t+' °C'; O('pa').textContent=pa+' mmHg';
      O('log').innerHTML=log.map((r,i)=>`<tr><td>${i+1}</td><td>${r.dm.toFixed(3)}</td><td>${r.V}</td><td>${r.t}</td><td>${r.P.toFixed(1)}</td><td>${r.R.toFixed(4)}</td></tr>`).join('');
    }
    function idle(){ last=null; setLevel(0); tx.forEach(e=>e.textContent=''); O('big').textContent='—'; O('msg').textContent='시료 질량·물의 온도·대기압을 정하고 「실험하기」를 누르자.'; show(); }
    function run(){
      const m=+I('m').value, t=+I('t').value, pa=+I('pa').value, corr=I('corr').checked, pw=PW[t];
      const n=m/122.55*1.5*(0.985+0.015*rnd());
      const Vtrue=n*0.082057*(t+273.15)/((pa-pw)/760)*1000;
      const dm=Math.round(n*32.00*(1+0.004*gauss(rnd))*1000)/1000;
      const V=Math.round(Vtrue*(1+0.006*gauss(rnd)));
      const P=corr?pa-pw:pa, R=(P/760)*(V/1000)/((dm/32.00)*(t+273));
      log.push({dm,V,t,P,R}); if(log.length>6) log.shift();
      setLevel(V);
      tx[0].textContent=`질량 감소 ${dm.toFixed(3)} g`; tx[1].textContent=`모은 부피 ${V} mL`;
      tx[2].textContent=`수증기압 ${pw.toFixed(1)} mmHg`; tx[3].textContent=`산소 압력 ${corr?(pa-pw).toFixed(1):pa+' (보정 안 함)'} mmHg`;
      O('big').textContent=R.toFixed(4)+' atm·L/(mol·K)';
      const avg=log.reduce((a,r)=>a+r.R,0)/log.length; let er=(R-0.08206)/0.08206*100; if(Math.abs(er)<0.05) er=0;
      O('msg').textContent=`이번 값의 오차 ${er>=0?'+':''}${er.toFixed(1)} % (기준 0.08206). 지금까지 ${log.length}회 평균 ${avg.toFixed(4)}.`+(corr?'':' 수증기압을 빼지 않아 산소 압력을 크게 잡았다 → R이 커진다.');
      show();
    }
    ['m','t','pa','corr'].forEach(k=>I(k).addEventListener(k==='corr'?'change':'input',idle));
    root.querySelector('[data-act="run"]').addEventListener('click',run);
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; rnd=rng(79); I('m').value=0.50; I('t').value=25; I('pa').value=760; I('corr').checked=true; idle(); });
    idle();
  }
};
})();
