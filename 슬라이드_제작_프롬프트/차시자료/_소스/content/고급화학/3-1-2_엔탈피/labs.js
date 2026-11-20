/* 고급화학 3-1-2 — 실험실
   ac312hess : ◆ 디지털 탐구 Ⅲ-1 「온도 센서로 중화열을 측정하여 헤스 법칙 확인하기」
     · 실험 ① NaOH(s) 2.00 g + 물 100 mL (용해) ② 1.0 M NaOH 50 mL + 1.0 M HCl 50 mL (중화) ③ NaOH(s) 2.00 g + 0.50 M HCl 100 mL (직접 반응)
     · 모형 참값 ΔH: ① −44.5 ② −55.8 ③ −100.3 kJ/mol (①+② = ③), n = 0.0500 mol, 용액 질량 102/100/102 g, c = 4.18 J/(g·°C)
     · 열량계 효율(뚜껑 덮음 0.98 / 안 덮음 0.92), 냉각 기울기(0.010 / 0.035 °C/s), 오름 시간 상수 τ(① 14 s ② 3 s ③ 8 s)
       T(t) = T0 + ΔTeff(1 − e^{−(t−30)/τ}) − k(t − 30)  (t ≥ 30 s, 혼합 30 s) + 고정 시드 센서 잡음 ±0.03 °C
     · 보정 함: 90–180 s 냉각 구간 최소 제곱 직선을 30 s로 연장 / 보정 안 함: 측정 최고 온도
     · q = m × 4.18 × ΔT, ΔH = −q / n */
(function(){
const M='−';
const fx=(v,d)=>(v<0?M:'')+Math.abs(v).toFixed(d);
window.DECK_LABS = {
  ac312hess(root, API){
    const EX={a:{name:'① 용해',H:44.5,m:102.0,tau:14},b:{name:'② 중화',H:55.8,m:100.0,tau:3},c:{name:'③ 직접 반응',H:100.3,m:102.0,tau:8}};
    const LID={on:{name:'덮음',eff:0.98,k:0.010},off:{name:'안 덮음',eff:0.92,k:0.035}};
    const COR={on:'보정',off:'보정 안 함'};
    const N=0.0500, CS=4.18, TMIX=30, TEND=180, TMIN=16, TMAX=40;
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), Ov=k=>$(`[data-ov="${k}"]`), I=k=>$(`[data-i="${k}"]`);
    const svg=$('.lab-fig svg'), g=API.mk('g',{},svg), W=640, H=232;
    const X0=262, X1=620, Y0=196, Y1=20;
    const xs=t=>X0+(X1-X0)*t/TEND, yt=T=>Y0-(Y0-Y1)*(API.clamp(T,TMIN,TMAX)-TMIN)/(TMAX-TMIN);
    let st, cnt, log, last, run, cur;
    function init(){ st={e:'a',lid:'on',cor:'on',view:'tt'}; cnt=0; log=[]; last={}; run=null; cur=null; I('t0').value=22; }
    function simulate(e,lid,T0,seed){
      const E=EX[e], Lc=LID[lid], dTe=N*E.H*1000/(E.m*CS)*Lc.eff; let s=seed; const rnd=()=>{ s=(s*16807)%2147483647; return s/2147483647; };
      const pts=[]; for(let t=0;t<=TEND;t++){ let T=t<TMIX?T0:T0+dTe*(1-Math.exp(-(t-TMIX)/E.tau))-Lc.k*(t-TMIX); T+= (rnd()-.5)*0.06; pts.push(Math.round(T*100)/100); }
      return pts;
    }
    function analyze(e,lid,cor,T0set,pts){
      const E=EX[e]; let t0=0; for(let t=0;t<TMIX;t++) t0+=pts[t]; t0/=TMIX;
      let mx=-1e9, tm=0; pts.forEach((T,t)=>{ if(T>mx){mx=T;tm=t;} });
      let sx=0,sy=0,sxx=0,sxy=0,n=0; for(let t=90;t<=TEND;t++){ sx+=t; sy+=pts[t]; sxx+=t*t; sxy+=t*pts[t]; n++; }
      const b=(n*sxy-sx*sy)/(n*sxx-sx*sx), a=(sy-b*sx)/n, pk=a+b*TMIX;
      const dT=(cor==='on'?pk:mx)-t0, q=E.m*CS*dT, h=-q/1000/N;
      return {e,lid,cor,T0:t0,Tmax:mx,tm,pk,a,b,dT,q,h,pts};
    }
    function controls(){
      root.querySelectorAll('[data-e]').forEach(b=>b.classList.toggle('on',b.dataset.e===st.e));
      root.querySelectorAll('[data-l]').forEach(b=>b.classList.toggle('on',b.dataset.l===st.lid));
      root.querySelectorAll('[data-c]').forEach(b=>b.classList.toggle('on',b.dataset.c===st.cor));
      root.querySelectorAll('[data-v]').forEach(b=>b.classList.toggle('on',b.dataset.v===st.view));
      O('t0').textContent=`${(+I('t0').value).toFixed(1)} °C`;
    }
    function readout(r){
      if(!r){ O('tt').textContent='측정 전'; O('dt').textContent='–'; O('q').textContent='–'; O('h').textContent='–'; return; }
      O('tt').textContent=`${r.T0.toFixed(2)} → ${r.Tmax.toFixed(2)} °C`;
      O('dt').textContent=`${r.dT.toFixed(2)} °C (${COR[r.cor]})`;
      O('q').textContent=`${EX[r.e].m.toFixed(0)} × 4.18 × ${r.dT.toFixed(2)} = ${Math.round(r.q)} J`;
      O('h').textContent=`${fx(r.h,1)} kJ/mol`;
    }
    const key=()=>st.lid+'|'+st.cor;
    function hessMsg(){
      const L=last[key()]||{};
      if(!(L.a&&L.b&&L.c)){ const miss=['a','b','c'].filter(k=>!L[k]).map(k=>EX[k].name).join(', ');
        return `뚜껑 ${LID[st.lid].name}·${COR[st.cor]} 조건에서 아직 측정하지 않은 실험: ${miss}. 같은 조건으로 세 실험을 모두 측정하면 두 경로를 비교할 수 있다.`; }
      const s=L.a.h+L.b.h, d=Math.abs(s-L.c.h)/Math.abs(L.c.h)*100;
      let m=`경로 1: ΔH1 + ΔH2 = ${fx(L.a.h,1)} + (${fx(L.b.h,1)}) = ${fx(s,1)} kJ/mol, 경로 2: ΔH3 = ${fx(L.c.h,1)} kJ/mol → 상대 오차 ${d.toFixed(1)} %.`;
      if(st.cor==='off') m+=' 보정하지 않으면 온도가 천천히 오르는 반응(용해)에서 열 손실이 커서 두 경로의 값이 어긋난다.';
      else if(d<2) m+=' 반응 경로가 달라도 반응 엔탈피의 합은 같다(헤스 법칙).';
      if(st.lid==='off') m+=' 뚜껑이 없으면 열이 빠져나가 세 값의 크기가 모두 작다.';
      return m;
    }
    function drawCal(T){
      const cg=API.mk('g',{transform:'translate(6,6) scale(.82)'},g), mk=(t,a)=>API.mk(t,a,cg);
      mk('path',{d:'M30 92 L210 92 L196 262 L44 262 Z',fill:'#F3F5F8',stroke:'#16233D','stroke-width':2.5});
      mk('path',{d:'M46 100 L194 100 L184 252 L56 252 Z',fill:'#FFFFFF',stroke:'#16233D','stroke-width':2});
      mk('path',{d:'M51 160 L189 160 L184 252 L56 252 Z',fill:'#DDEEF8'});
      if(st.lid==='on') mk('rect',{x:24,y:78,width:192,height:15,rx:4,fill:'#E6EBF0',stroke:'#16233D','stroke-width':2});
      mk('line',{x1:150,y1:30,x2:150,y2:236,stroke:'#16233D','stroke-width':4}); mk('circle',{cx:150,cy:240,r:6,fill:'#16233D'});
      mk('path',{d:'M150 30 L150 16 L246 16',fill:'none',stroke:'#16233D','stroke-width':2});
      if(st.lid==='off'&&run) for(let i=0;i<3;i++) mk('path',{d:`M${80+i*28} 86 q-8 -14 0 -28`,fill:'none',stroke:'#E08A2C','stroke-width':2.5});
      const t=API.mk('text',{x:6+.82*120,y:6+.82*292,'font-size':20,'text-anchor':'middle',fill:'#B42318','font-weight':700},g); t.textContent=`${T.toFixed(2)} °C`;
    }
    function drawTT(){
      const mk=(t,a)=>API.mk(t,a,g);
      for(let T=TMIN;T<=TMAX;T+=4){ mk('line',{x1:X0,y1:yt(T),x2:X1,y2:yt(T),stroke:'#E2E7EC','stroke-width':1});
        const t=mk('text',{x:X0-8,y:yt(T)+6,'text-anchor':'end','font-size':18,fill:'#5B6B7F'}); t.textContent=T; }
      for(let s=0;s<=TEND;s+=30){ const t=mk('text',{x:xs(s),y:Y0+22,'text-anchor':'middle','font-size':18,fill:'#5B6B7F'}); t.textContent=s; }
      API.arrow(g,X0,Y0+4,X0,Y1-14,'#5B6B7F',2.5); API.arrow(g,X0-4,Y0,X1+14,Y0,'#5B6B7F',2.5);
      Ov('ya').innerHTML=API.tex('T')+' [°C]'; API.place(Ov('ya'),X0+8,0,true);
      Ov('xa').innerHTML=API.tex('t')+' [s]'; API.place(Ov('xa'),X1-34,Y0-30,true);
      let T=+I('t0').value;
      const r=run||cur;
      if(r){ const smax=run?Math.floor(run.s):TEND; let d=''; for(let t=0;t<=smax;t++){ d+=(t?'L':'M')+xs(t).toFixed(1)+' '+yt(r.pts[t]).toFixed(1)+' '; } T=r.pts[smax];
        mk('path',{d,fill:'none',stroke:'#D7263D','stroke-width':2.5});
        mk('line',{x1:xs(TMIX),y1:Y0,x2:xs(TMIX),y2:yt(r.pts[0])-6,stroke:'#C2410C','stroke-width':1.5,'stroke-dasharray':'4 3'});
        if(!run){
          mk('circle',{cx:xs(r.tm),cy:yt(r.Tmax),r:5,fill:'#D7263D'});
          if(r.cor==='on'){ mk('line',{x1:xs(TMIX),y1:yt(r.pk),x2:xs(TEND),y2:yt(r.a+r.b*TEND),stroke:'#2E9E6A','stroke-width':2,'stroke-dasharray':'6 4'});
            mk('circle',{cx:xs(TMIX),cy:yt(r.pk),r:5,fill:'#2E9E6A'});
            const t=mk('text',{x:xs(TMIX)-8,y:yt(r.pk)-10,'font-size':18,fill:'#2E9E6A','font-weight':700,'text-anchor':'start'}); t.textContent=`보정 ${r.pk.toFixed(2)} °C`; }
          const t2=mk('text',{x:xs(r.tm)+8,y:yt(r.Tmax)+(r.cor==='on'?24:-10),'font-size':18,fill:'#D7263D','text-anchor':'start'}); t2.textContent=`최고 ${r.Tmax.toFixed(2)} °C`;
        }
      }
      drawCal(T);
    }
    function drawCmp(){
      const mk=(t,a)=>API.mk(t,a,g), AX=120, Z=30, S=1.6, y=v=>Z+S*v;
      for(let v=0;v<=100;v+=20){ mk('line',{x1:AX,y1:y(v),x2:W-20,y2:y(v),stroke:'#E2E7EC','stroke-width':1});
        const t=mk('text',{x:AX-8,y:y(v)+6,'text-anchor':'end','font-size':18,fill:'#5B6B7F'}); t.textContent=v?M+v:'0'; }
      API.arrow(g,AX,Z-4,AX,H-8,'#5B6B7F',2.5); mk('line',{x1:AX,y1:Z,x2:W-20,y2:Z,stroke:'#5B6B7F','stroke-width':2.5});
      Ov('ya').innerHTML=API.tex('\\Delta H')+' [kJ/mol]'; API.place(Ov('ya'),AX+8,H-30,true);
      API.place(Ov('xa'),0,0,false);
      const L=last[key()]||{}, bar=(x,v0,v1,col)=>mk('rect',{x,y:y(v0),width:120,height:Math.max(S*(v1-v0),0),fill:col});
      const lab=(x,yy,s,col)=>{ const t=mk('text',{x,y:yy,'text-anchor':'middle','font-size':19,fill:col||'#16233D','font-weight':700}); t.textContent=s; };
      lab(270,Z-10,'경로 1 (① + ②)','#1F6FD1'); lab(480,Z-10,'경로 2 (③)','#C2410C');
      if(L.a){ bar(210,0,-L.a.h,'#8DB8EC'); lab(270,y(-L.a.h/2)+7,fx(L.a.h,1)); }
      if(L.b){ const a0=L.a?-L.a.h:0; bar(210,a0,a0-L.b.h,'#1F6FD1'); lab(270,y(a0-L.b.h/2)+7,fx(L.b.h,1),'#fff'); }
      if(L.c){ bar(420,0,-L.c.h,'#C2410C'); lab(480,y(-L.c.h/2)+7,fx(L.c.h,1),'#fff'); }
      if(L.a&&L.b) lab(370,y(-(L.a.h+L.b.h))+6,'합 '+fx(L.a.h+L.b.h,1));
      if(!(L.a||L.b||L.c)){ const t=mk('text',{x:(AX+W)/2,y:130,'text-anchor':'middle','font-size':20,fill:'#5B6B7F'}); t.textContent='이 조건(뚜껑·보정)으로 측정한 값이 아직 없다'; }
    }
    function draw(){ while(g.firstChild) g.removeChild(g.firstChild); st.view==='tt'?drawTT():drawCmp(); }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-4).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${r.no}</td><td>${EX[r.e].name}</td><td>${LID[r.lid].name}</td><td>${r.cor==='on'?'함':'안 함'}</td><td>${r.T0.toFixed(2)}</td><td>${r.Tmax.toFixed(2)}</td><td>${r.dT.toFixed(2)}</td><td>${Math.round(r.q)}</td><td>${fx(r.h,1)}</td>`; tb.appendChild(tr); }); }
    function finish(){
      const r=run; run=null; cur=r; log.push(r); r.no=log.length; (last[r.lid+'|'+r.cor]=last[r.lid+'|'+r.cor]||{})[r.e]=r; renderLog(); readout(r);
      let m=`${EX[r.e].name}: 온도가 ${r.dT.toFixed(2)} °C 올라갔다(${COR[r.cor]}) → 발열, ΔH = ${fx(r.h,1)} kJ/mol.`;
      const L=last[key()]; if(L.a&&L.b&&L.c) m=hessMsg(); else if(r.lid==='off') m+=' 뚜껑이 없어 열이 빠져나가 온도가 빨리 내려간다.';
      O('msg').textContent=m; draw();
    }
    function start(){
      if(run) return; cnt++;
      const T0=+I('t0').value, pts=simulate(st.e,st.lid,T0,cnt*7919+13);
      run=Object.assign(analyze(st.e,st.lid,st.cor,T0,pts),{s:0});
      O('msg').textContent=`${EX[st.e].name} 측정 중… 30 s에 섞고 180 s까지 기록한다.`;
      if(window.__STILL){ run.s=TEND; finish(); } else draw();
    }
    const pick=(attr,k)=>root.querySelectorAll(`[data-${attr}]`).forEach(b=>b.addEventListener('click',()=>{ if(run) return; st[k]=b.dataset[attr]; controls(); if(k!=='e'){ draw(); O('msg').textContent=hessMsg(); } }));
    pick('e','e'); pick('l','lid'); pick('c','cor');
    root.querySelectorAll('[data-v]').forEach(b=>b.addEventListener('click',()=>{ st.view=b.dataset.v; controls(); draw(); if(st.view==='cmp') O('msg').textContent=hessMsg(); }));
    I('t0').addEventListener('input',()=>{ controls(); if(!run){ cur=null; readout(null); draw(); } });
    $('[data-act="run"]').addEventListener('click',start);
    $('[data-act="reset"]').addEventListener('click',()=>{ init(); controls(); renderLog(); readout(null); O('msg').textContent='실험과 조건을 고르고 「측정 시작」을 누르자.'; draw(); });
    API.loop(root,dt=>{ if(!run) return; run.s=Math.min(TEND,run.s+dt*60); if(run.s>=TEND) finish(); else draw(); });
    init(); controls(); readout(null); O('msg').textContent='실험과 조건을 고르고 「측정 시작」을 누르자.';
    API.ready(()=>draw()); API.onShow(s=>{ if(s===root.closest('.slide')) draw(); });
    draw();
  }
};
})();
