/* 3-2 반응 경로와 반응 엔탈피 — 실험실 (필수 탐구 물03-탐2 「중화 반응으로 헤스 법칙을 확인하는 실험하기」,
   교과서 78–79쪽 탐구: 실험 1 [경로 1] 용해 → 중화, 실험 2 [경로 2] 고체 NaOH + 염산)
   em32hess : 과정(용해·중화·직접 반응)·열량계(스타이로폼/유리 비커)·NaOH 질량·처음 온도를 고르고 「측정」
              → 온도–시간 곡선이 그려지고 최고 온도를 읽음 → Q = 4.2 × m × Δt → ΔH = −Q/n (kJ/mol)
              → 결과 표에 행이 쌓이고, 「ΔH 비교」 보기에서 경로 1(ΔH1 + ΔH2) 대 경로 2(ΔH3) 막대와 해석.
   기준값(지도서 79쪽 결과 예시, 간이 열량계): 용해 −41.50, 중화 −55.69, 직접 −97.68 kJ/mol(교과서 76쪽 −44.5, −55.8, −100.3보다 조금 작다).
   용액 질량: 용해 100 + w, 중화·직접 200 + w (g). 열량계 효율(덱 설정): 스타이로폼 1(지도서 예시와 같음), 유리 비커 0.80. 측정 잡음은 고정 수열(첫 측정 0). */
window.DECK_LABS = {
  em32hess(root, API){
    const P={
      dis:{name:'용해',path:'경로 1 ①',H:41.50,m:w=>100+w,T:['T1','T2']},
      neu:{name:'중화',path:'경로 1 ②',H:55.69,m:w=>200+w,T:['T3','T4']},
      dir:{name:'직접 반응',path:'경로 2',H:97.68,m:w=>200+w,T:['T5','T6']}
    };
    const CAL={foam:{name:'스타이로폼',eff:1,k:0.01},glass:{name:'유리 비커',eff:0.80,k:0.06}};
    const NOISE=[0,0.1,-0.1,0.2,0,-0.2,0.1,-0.1];
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), Ov=k=>$(`[data-ov="${k}"]`), I=k=>$(`[data-i="${k}"]`);
    const svg=$('svg'), g=API.mk('g',{},svg), W=640, H=230;
    const X0=262, X1=620, Y0=196, Y1=22, TMIN=15, TMAX=40;
    let st, cnt, last, log, run;
    function init(){ st={p:'dis',c:'foam',view:'tt'}; cnt={dis:0,neu:0,dir:0}; last={foam:{},glass:{}}; log=[]; run=null; I('w').value=4; I('t0').value=22; }
    const r1=v=>Math.round(v*10)/10, f1=v=>v.toFixed(1).replace('-','−');
    const w=()=>+I('w').value, t0=()=>+I('t0').value;
    function measureOf(p,c,wv,noise){
      const n=wv/40, m=P[p].m(wv), dtTrue=P[p].H*n*1000/(4.2*m), dt=r1(dtTrue*CAL[c].eff+noise);
      const qJ=4.2*m*dt, qk=Math.round(qJ/10)/100, h=-r1(qk/n);
      return {p,c,w:wv,n,m,dt,qJ,qk,h};
    }
    const Tcurve=(s,T0,dt,k)=> s<40? T0+dt*(1-Math.pow(1-s/40,2)) : T0+dt-k*(s-40);
    const xs=s=>X0+(X1-X0)*s/120, yt=T=>Y0-(Y0-Y1)*(API.clamp(T,TMIN,TMAX)-TMIN)/(TMAX-TMIN);
    function controls(){
      root.querySelectorAll('[data-p]').forEach(b=>b.classList.toggle('on',b.dataset.p===st.p));
      root.querySelectorAll('[data-c]').forEach(b=>b.classList.toggle('on',b.dataset.c===st.c));
      root.querySelectorAll('[data-v]').forEach(b=>b.classList.toggle('on',b.dataset.v===st.view));
      O('w').textContent=`${w().toFixed(1)} g (${(w()/40).toPrecision(2)} mol)`;
      O('t0').textContent=`${f1(t0())} °C`;
    }
    function readout(r){
      if(!r){ O('dt').textContent='측정 전'; O('q').textContent='–'; O('h').textContent='–'; return; }
      const T0=r.T0;
      O('dt').textContent=`${f1(T0)} → ${f1(T0+r.dt)} °C (Δt ${f1(r.dt)})`;
      O('q').textContent=`4.2 × ${r.m} × ${f1(r.dt)} = ${Math.round(r.qJ)} J`;
      O('h').textContent=`−${r.qk.toFixed(2)} ÷ ${r.n.toPrecision(2)} = ${f1(r.h)} kJ/mol`;
    }
    function hessMsg(){
      const L=last[st.c];
      if(!(L.dis&&L.neu&&L.dir)){ const miss=['dis','neu','dir'].filter(k=>!L[k]).map(k=>P[k].name).join(', ');
        return `${CAL[st.c].name} 열량계로 아직 측정하지 않은 과정: ${miss}. 세 과정을 모두 측정하면 두 경로를 비교할 수 있다.`; }
      const s=r1(L.dis.h+L.neu.h), d=Math.abs(s-L.dir.h)/Math.abs(L.dir.h)*100;
      let m=`경로 1: ΔH1 + ΔH2 = ${f1(L.dis.h)} + (${f1(L.neu.h)}) = ${f1(s)} kJ/mol, 경로 2: ΔH3 = ${f1(L.dir.h)} kJ/mol → 차이 ${d.toFixed(1)} %. 반응 경로가 달라도 반응 엔탈피의 총합은 거의 같다(헤스 법칙).`;
      if(st.c==='glass') m+=' 유리 비커는 열 손실로 값의 크기가 작지만 두 경로의 합은 비슷하다.';
      return m;
    }
    function drawCal(T){
      const cg=API.mk('g',{transform:'translate(14,8) scale(.85)'},g), mk=(t,a)=>API.mk(t,a,cg);
      mk('path',{d:'M40 92 L50 226 Q51 236 62 236 L178 236 Q189 236 190 226 L200 92 Z',fill:st.c==='foam'?'#F4F1EA':'#F3F7FA',stroke:st.c==='foam'?'#C9C2B4':'#7E8B98','stroke-width':2.5});
      mk('path',{d:'M44 132 L52 226 Q53 232 62 232 L178 232 Q187 232 188 226 L196 132 Z',fill:'#DDEEF8'});
      if(st.c==='foam') mk('rect',{x:32,y:80,width:176,height:14,rx:3,fill:'#E8E2D6',stroke:'#C9C2B4','stroke-width':2});
      mk('line',{x1:84,y1:56,x2:84,y2:214,stroke:'#7E8B98','stroke-width':3});
      mk('ellipse',{cx:84,cy:216,rx:16,ry:4,fill:'none',stroke:'#7E8B98','stroke-width':3});
      const tx=150, top=22, bot=222;
      mk('rect',{x:tx-7,y:top,width:14,height:bot-top+6,rx:7,fill:'#fff',stroke:'#7E8B98','stroke-width':2});
      const yy=bot-(bot-top-14)*(API.clamp(T,TMIN,TMAX)-TMIN)/(TMAX-TMIN);
      mk('rect',{x:tx-2.5,y:yy,width:5,height:bot-yy,fill:'#E0664F'}); mk('circle',{cx:tx,cy:bot,r:9,fill:'#E0664F'});
      const t=API.mk('text',{x:14+.85*(tx+14),y:8+.85*Math.max(yy+6,40),'font-size':19,fill:'#B42318','font-weight':700},g); t.textContent=`${f1(T)} °C`;
    }
    function drawTT(){
      const mk=(t,a)=>API.mk(t,a,g);
      for(let T=TMIN;T<=TMAX;T+=5){ mk('line',{x1:X0,y1:yt(T),x2:X1,y2:yt(T),stroke:'#E2E7EC','stroke-width':1});
        const t=mk('text',{x:X0-8,y:yt(T)+6,'text-anchor':'end','font-size':18,fill:'#5B6B7F'}); t.textContent=T; }
      for(let s=0;s<=120;s+=40){ const t=mk('text',{x:xs(s),y:Y0+22,'text-anchor':'middle','font-size':18,fill:'#5B6B7F'}); t.textContent=s; }
      API.arrow(g,X0,Y0+4,X0,Y1-14,'#5B6B7F',2.5); API.arrow(g,X0-4,Y0,X1+14,Y0,'#5B6B7F',2.5);
      Ov('ya').innerHTML=API.tex('T')+' [°C]'; API.place(Ov('ya'),X0+8,0,true);
      Ov('xa').innerHTML=API.tex('t')+' [s]'; API.place(Ov('xa'),X1-30,Y0-28,true);
      let T=t0();
      const cur=run||(log.length&&log[log.length-1].show?log[log.length-1]:null);
      if(cur){ const smax=run?run.s:120; let d=''; for(let s=0;s<=smax;s+=2){ const v=Tcurve(s,cur.T0,cur.dt,CAL[cur.c].k); d+=(s?'L':'M')+xs(s).toFixed(1)+' '+yt(v).toFixed(1)+' '; T=v; }
        mk('path',{d,fill:'none',stroke:'#D7263D','stroke-width':3});
        if(!run||run.s>=40){ mk('line',{x1:X0,y1:yt(cur.T0+cur.dt),x2:xs(40),y2:yt(cur.T0+cur.dt),stroke:'#5B6B7F','stroke-width':1.5,'stroke-dasharray':'5 5'});
          mk('circle',{cx:xs(40),cy:yt(cur.T0+cur.dt),r:5,fill:'#D7263D'});
          const t=mk('text',{x:xs(40)+10,y:yt(cur.T0+cur.dt)-10,'font-size':18,fill:'#16233D'}); t.textContent=`최고 ${f1(cur.T0+cur.dt)} °C`; }
        if(!run) T=cur.T0+cur.dt;
      }
      drawCal(T);
    }
    function drawCmp(){
      const mk=(t,a)=>API.mk(t,a,g), AX=110, Z=34, S=1.4, y=v=>Z+S*v; // v = |ΔH|
      for(let v=0;v<=120;v+=20){ mk('line',{x1:AX,y1:y(v),x2:W-20,y2:y(v),stroke:'#E2E7EC','stroke-width':1});
        const t=mk('text',{x:AX-8,y:y(v)+6,'text-anchor':'end','font-size':18,fill:'#5B6B7F'}); t.textContent=v?'−'+v:'0'; }
      API.arrow(g,AX,Z-4,AX,H-8,'#5B6B7F',2.5); mk('line',{x1:AX,y1:Z,x2:W-20,y2:Z,stroke:'#5B6B7F','stroke-width':2.5});
      Ov('ya').innerHTML=API.tex('\\Delta H')+' [kJ/mol]'; API.place(Ov('ya'),AX+8,H-30,true);
      API.place(Ov('xa'),0,0,false);
      const L=last[st.c], bar=(x,v0,v1,col)=>mk('rect',{x,y:y(v0),width:110,height:Math.max(S*(v1-v0),0),fill:col});
      const lab=(x,yy,s,col)=>{ const t=mk('text',{x,y:yy,'text-anchor':'middle','font-size':19,fill:col||'#16233D','font-weight':700}); t.textContent=s; };
      lab(275,Z-10,'경로 1 (① + ②)','#1F6FD1'); lab(475,Z-10,'경로 2','#C2410C');
      if(L.dis){ bar(220,0,-L.dis.h,'#8DB8EC'); lab(275,y(-L.dis.h/2)+7,f1(L.dis.h)); }
      if(L.neu){ const a=L.dis?-L.dis.h:0; bar(220,a,a-L.neu.h,'#1F6FD1'); lab(275,y(a-L.neu.h/2)+7,f1(L.neu.h),'#fff'); }
      if(L.dir){ bar(420,0,-L.dir.h,'#C2410C'); lab(475,y(-L.dir.h/2)+7,f1(L.dir.h),'#fff'); }
      if(L.dis&&L.neu){ const s=r1(L.dis.h+L.neu.h); lab(275,y(-s)+22,'합 '+f1(s)); }
      if(!(L.dis||L.neu||L.dir)){ const t=mk('text',{x:(AX+W)/2,y:140,'text-anchor':'middle','font-size':20,fill:'#5B6B7F'}); t.textContent=`${CAL[st.c].name} 열량계로 측정한 값이 아직 없다`; }
    }
    function draw(){ while(g.firstChild) g.removeChild(g.firstChild); st.view==='tt'?drawTT():drawCmp(); }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-3).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${P[r.p].name}</td><td>${CAL[r.c].name}</td><td>${r.w.toFixed(1)}</td><td>${f1(r.T0)}→${f1(r.T0+r.dt)}</td><td>${f1(r.dt)}</td><td>${r.qk.toFixed(2)}</td><td>${f1(r.h)}</td>`; tb.appendChild(tr); }); }
    function finish(){
      const r=run; run=null; r.show=true; log.forEach(x=>x.show=false); log.push(r); last[r.c][r.p]=r; renderLog(); readout(r);
      let m=`${P[r.p].name}(${P[r.p].path}): 온도가 ${f1(r.dt)} °C 올라갔다 → 발열, ΔH ${f1(r.h)} kJ/mol.`;
      const L=last[r.c]; if(L.dis&&L.neu&&L.dir) m=hessMsg(); else if(r.c==='glass') m+=' 유리 비커는 열이 빠져나가 온도 변화가 작게 측정된다.';
      O('msg').textContent=m; draw();
    }
    function start(){
      if(run) return;
      const noise=NOISE[cnt[st.p]%NOISE.length]; cnt[st.p]++;
      run=Object.assign(measureOf(st.p,st.c,w(),noise),{T0:t0(),s:0});
      O('msg').textContent=`${P[st.p].name} 측정 중… 최고 온도를 기다린다.`;
      if(window.__STILL){ run.s=120; finish(); } else draw();
    }
    root.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{ if(run) return; st.p=b.dataset.p; controls(); }));
    root.querySelectorAll('[data-c]').forEach(b=>b.addEventListener('click',()=>{ if(run) return; st.c=b.dataset.c; controls(); draw(); if(st.view==='cmp') O('msg').textContent=hessMsg(); }));
    root.querySelectorAll('[data-v]').forEach(b=>b.addEventListener('click',()=>{ st.view=b.dataset.v; controls(); draw(); if(st.view==='cmp') O('msg').textContent=hessMsg(); }));
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',()=>{ controls(); if(!run){ log.forEach(x=>x.show=false); draw(); } }));
    $('[data-act="run"]').addEventListener('click',start);
    $('[data-act="reset"]').addEventListener('click',()=>{ init(); controls(); renderLog(); readout(null); O('msg').textContent='과정과 조건을 고르고 「측정」을 누르자.'; draw(); });
    API.loop(root,dt=>{ if(!run) return; run.s=Math.min(120,run.s+dt*48); if(run.s>=120) finish(); else draw(); });
    init(); controls(); readout(null); O('msg').textContent='과정과 조건을 고르고 「측정」을 누르자.';
    API.ready(()=>draw()); API.onShow(s=>{ if(s===root.closest('.slide')) draw(); });
    draw();
  }
};
