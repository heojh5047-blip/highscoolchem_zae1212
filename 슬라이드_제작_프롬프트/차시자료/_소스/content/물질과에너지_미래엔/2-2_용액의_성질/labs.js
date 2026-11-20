/* 2-2 용액의 성질 — 실험실
   em22sensor : 온도 센서로 설탕물의 끓는점·어는점 측정 (필수 탐구 물02-탐1)
     · 실험 1 끓는점 / 실험 2 어는점, 몰랄 농도 0–2 m(0.25 간격)
     · 끓는점 T_b' = 100 + 0.51 m + ε, 어는점 T_f' = −1.86 m + ε (ε: 고정 시드 ±0.02 °C, m = 0이면 0)
     · 센서 곡선(0–10 분): 가열 — 25 °C에서 5 분에 끓기 시작, 끓는 동안 0.04 m °C/분 상승
                         냉각 — 한제 −12 °C로 지수 냉각 → 과냉각 1.2 °C → 어는점 → 0.08 m °C/분 하강
     · 「측정 시작」 → 곡선이 약 5 s 동안 그려짐, 「측정값 기록」 → 표·(나) 확대 그래프·(다) ΔT–m 그래프에 쌓임, 「초기화」 */
window.DECK_LABS = {
  em22sensor(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), still=()=>!!window.__STILL||document.documentElement.classList.contains('still');
    const KB=0.51, KF=1.86, RED='#D7263D', BLUE='#1F6FD1', MUT='#5B6B7F', GRID='#E2E7EC';
    const eps=(x,m)=>{ if(!m) return 0; const k=Math.round(m*4); return (((k*(x==='b'?7:13)+(x==='b'?4:2))%5)-2)*0.01; };
    const Tread=(x,m)=> x==='b' ? 100+KB*m+eps(x,m) : -KF*m+eps(x,m);
    function temp(x,m,t){
      const T=Tread(x,m);
      if(x==='b'){ const tb=5; return t<tb ? T-(T-25)*Math.pow(1-t/tb,1.5) : T+0.04*m*(t-tb); }
      const sc=T-1.2, tau=1.6, t1=-tau*Math.log((sc+12)/32);
      if(t<t1) return -12+32*Math.exp(-t/tau);
      if(t<t1+0.25) return sc+(T-sc)*(t-t1)/0.25;
      return T-0.08*m*(t-t1-0.25);
    }
    // 그래프 좌표
    const A={x0:66,x1:296,y0:176,y1:40}, B={x0:386,x1:616,y0:176,y1:40}, C={x0:66,x1:616,y0:378,y1:258};
    const RA={b:[20,110],f:[-15,25]}, RB={b:[99.6,101.6],f:[-5.2,0.6]};
    const ax=t=>A.x0+(A.x1-A.x0)*t/10, bx=t=>B.x0+(B.x1-B.x0)*(t-1)/9;
    const ay=(x,T)=>A.y0-(A.y0-A.y1)*(T-RA[x][0])/(RA[x][1]-RA[x][0]);
    const by=(x,T)=>B.y0-(B.y0-B.y1)*(T-RB[x][0])/(RB[x][1]-RB[x][0]);
    const cx=m=>C.x0+(C.x1-C.x0)*m/2, cy=d=>C.y0-(C.y0-C.y1)*d/4;
    // 고정 그림
    const base=API.mk('g',{},svg);
    const defs=API.mk('defs',{},svg); const cp=API.mk('clipPath',{id:'clip-em22-16'},defs); API.mk('rect',{x:B.x0,y:B.y1-6,width:B.x1-B.x0,height:B.y0-B.y1+6},cp);
    [A,B,C].forEach(P=>{ API.mk('line',{x1:P.x0,y1:P.y0,x2:P.x1+6,y2:P.y0,stroke:MUT,'stroke-width':2},base); API.mk('line',{x1:P.x0,y1:P.y0,x2:P.x0,y2:P.y1-8,stroke:MUT,'stroke-width':2},base); });
    API.texText(base,10,24,'(가) 센서 그래프 — 온도 [°C]',{size:18,mix:true});
    [0,5,10].forEach(t=>API.texText(base,ax(t),196,String(t),{size:18,anchor:'middle',fill:MUT}));
    API.texText(base,ax(2.5),216,'$t$ [분]',{size:18,anchor:'middle',mix:true});
    [1,4,7,10].forEach(t=>API.texText(base,bx(t),196,String(t),{size:18,anchor:'middle',fill:MUT}));
    API.texText(base,bx(2.5),216,'$t$ [분]',{size:18,anchor:'middle',mix:true});
    API.texText(base,10,240,'(다) 몰랄 농도와 온도 변화 — $\\Delta T$ [°C]',{size:18,mix:true});
    [0,0.5,1,1.5,2].forEach(m=>{ API.texText(base,cx(m),398,String(m),{size:18,anchor:'middle',fill:MUT}); });
    API.texText(base,C.x1,428,'몰랄 농도 [m]',{size:18,anchor:'end',mix:true});
    [1,2,3,4].forEach(d=>{ API.mk('line',{x1:C.x0,y1:cy(d),x2:C.x1,y2:cy(d),stroke:GRID,'stroke-width':1.5},base); });
    [0,1,2,3,4].forEach(d=>API.texText(base,C.x0-8,cy(d)+6,String(d),{size:18,anchor:'end',fill:MUT}));
    API.mk('circle',{cx:400,cy:233,r:6,fill:RED},base); API.texText(base,412,240,'끓는점 오름',{size:18,mix:true});
    API.mk('rect',{x:510,y:227,width:12,height:12,fill:BLUE},base); API.texText(base,528,240,'어는점 내림',{size:18,mix:true});
    // 실험별 눈금(둘 다 만들어 두고 켜고 끔)
    const tick={};
    ['b','f'].forEach(x=>{
      const gT=API.mk('g',{},svg); tick[x]=gT;
      const ta= x==='b'? [20,60,100] : [-10,0,20];
      ta.forEach(T=>{ API.mk('line',{x1:A.x0,y1:ay(x,T),x2:A.x1,y2:ay(x,T),stroke:GRID,'stroke-width':1.5},gT); API.texText(gT,A.x0-8,ay(x,T)+6,String(T),{size:18,anchor:'end',fill:MUT}); });
      const tb= x==='b'? [100,100.5,101,101.5] : [0,-2,-4];
      tb.forEach(T=>{ API.mk('line',{x1:B.x0,y1:by(x,T),x2:B.x1,y2:by(x,T),stroke:GRID,'stroke-width':1.5},gT); API.texText(gT,B.x0-8,by(x,T)+6,x==='b'?T.toFixed(1):String(T),{size:18,anchor:'end',fill:MUT}); });
      API.texText(gT,330,24,x==='b'?'(나) 끓는점 부근 확대':'(나) 어는점 부근 확대',{size:18,mix:true});
    });
    const g=API.mk('g',{},svg);
    let st={x:'b',prog:1}, log=[];
    const mval=()=>+I('m').value, fm=v=>v.toFixed(2).replace('-','−');
    function path(fx,fy,x,m,t0,t1,clip){ let d=''; for(let t=t0;t<=t1+1e-9;t+=0.05){ d+=(d?'L':'M')+fx(t).toFixed(1)+' '+fy(x,temp(x,m,t)).toFixed(1)+' '; } return d; }
    function fit(x){ const p=log.filter(r=>r.x===x&&r.m>0); if(p.length<2) return null; let a=0,b=0; p.forEach(r=>{a+=r.d*r.m;b+=r.m*r.m;}); return a/b; }
    function draw(){
      const x=st.x, m=mval(), col= x==='b'?RED:BLUE, done=st.prog>=1, tE=10*Math.min(1,st.prog);
      root.querySelectorAll('[data-x]').forEach(b=>b.classList.toggle('on',b.dataset.x===x));
      tick.b.style.display= x==='b'?'':'none'; tick.f.style.display= x==='f'?'':'none';
      O('m').textContent=m.toFixed(2)+' m';
      O('lbl').textContent= x==='b'?'끓는점(센서)':'어는점(센서)';
      const T=Tread(x,m), d=Math.abs(T-(x==='b'?100:0));
      if(done){ O('T').textContent=fm(T)+' °C'; O('dT').textContent=d.toFixed(2)+' °C'; }
      else { O('T').textContent='측정 중'; O('dT').textContent='—'; }
      while(g.firstChild) g.removeChild(g.firstChild);
      // (나) 지난 기록 곡선(같은 실험)
      const gb=API.mk('g',{'clip-path':'url(#clip-em22-16)'},g);
      log.filter(r=>r.x===x).slice(-4).forEach(r=>API.mk('path',{d:path(bx,by,x,r.m,1,10),fill:'none',stroke:col,'stroke-width':2,opacity:.35,'stroke-dasharray':'5 4'},gb));
      if(tE>0.05){
        API.mk('path',{d:path(ax,ay,x,m,0,tE),fill:'none',stroke:col,'stroke-width':3},g);
        if(tE>1.05) API.mk('path',{d:path(bx,by,x,m,1,tE),fill:'none',stroke:col,'stroke-width':3},gb);
        API.mk('circle',{cx:ax(tE),cy:ay(x,temp(x,m,tE)),r:5,fill:col},g);
      }
      if(done){ // 읽은 값 표시선
        API.mk('line',{x1:B.x0,y1:by(x,T),x2:B.x1,y2:by(x,T),stroke:col,'stroke-width':1.5,'stroke-dasharray':'3 4'},gb);
        const tr= x==='b'?5:(-1.6*Math.log((T-1.2+12)/32)+0.25);
        API.mk('circle',{cx:bx(tr),cy:by(x,T),r:6,fill:'#fff',stroke:col,'stroke-width':3},gb);
      }
      // (다) ΔT–m
      log.forEach(r=>{ if(r.x==='b') API.mk('circle',{cx:cx(r.m),cy:cy(r.d),r:6,fill:RED,stroke:'#fff','stroke-width':1.5},g); else API.mk('rect',{x:cx(r.m)-6,y:cy(r.d)-6,width:12,height:12,fill:BLUE,stroke:'#fff','stroke-width':1.5},g); });
      ['b','f'].forEach(k=>{ const s=fit(k), el=V(k==='b'?'kb':'kf');
        if(s){ API.mk('line',{x1:cx(0),y1:cy(0),x2:cx(2),y2:cy(2*s),stroke:k==='b'?RED:BLUE,'stroke-width':2,'stroke-dasharray':'6 5'},g);
          el.textContent=(k==='b'?'끓는점 오름':'어는점 내림')+' 기울기 ≈ '+s.toFixed(2); API.place(el,k==='b'?cx(1.62):cx(0.8),k==='b'?cy(2*s*0.81)-34:cy(s)-40,true); }
        else API.place(el,0,0,false); });
      // 해석 문장
      const msg=O('msg');
      if(!done) msg.textContent=`센서가 온도를 기록하는 중… (${tE.toFixed(1)} 분)`;
      else if(st.note) msg.textContent=st.note;
      else msg.textContent= x==='b' ? `끓기 시작해 온도가 거의 일정해진 구간의 처음 값이 끓는점 → ${fm(T)} °C` : `과냉각 뒤 온도가 다시 올라 평평해진 구간의 처음 값이 어는점 → ${fm(T)} °C`;
    }
    function table(){ const tb=O('log'); tb.innerHTML=''; log.slice(-3).forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${r.x==='b'?'끓는점':'어는점'}</td><td>${r.m.toFixed(2)} m</td><td>${fm(r.T)} °C</td><td>${r.d.toFixed(2)} °C</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-x]').forEach(b=>b.addEventListener('click',()=>{ st.x=b.dataset.x; st.prog=1; st.note=''; draw(); }));
    I('m').addEventListener('input',()=>{ st.prog=1; st.note=''; draw(); });
    $('[data-act="run"]').addEventListener('click',()=>{ st.prog= still()?1:0; st.note=''; draw(); });
    $('[data-act="rec"]').addEventListener('click',()=>{
      if(st.prog<1){ st.note=''; O('msg').textContent='측정이 끝난 뒤 기록하자.'; return; }
      const x=st.x, m=mval(), T=Tread(x,m), d=Math.abs(T-(x==='b'?100:0));
      log.push({x,m,T,d}); table();
      const s=fit(x), nm= x==='b'?'끓는점 오름':'어는점 내림';
      st.note= s ? `${nm} ÷ 몰랄 농도 ≈ ${s.toFixed(2)} (거의 일정) → ${nm}은 몰랄 농도에 비례한다.` : '농도를 바꿔 한 번 더 측정하고 기록해 보자.';
      draw(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; st.note=''; table(); draw(); });
    draw();
    API.loop(root,dt=>{ if(st.prog<1 && !still()){ st.prog=Math.min(1,st.prog+dt/5); draw(); } });
  }
};
