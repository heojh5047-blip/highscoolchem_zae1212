/* 4-4a 농도, 온도, 촉매에 따른 반응 속도의 변화 (1) — 실험실 (필수 탐구 물04-탐2)
   em44conc : 교과서 108–109쪽 탐구 「농도에 따른 반응 속도 측정하기」(아이오딘 시계 반응, 12홈판)
     · 홈 ①–④: KIO3(aq) 0.5/1.0/1.5/2.0 mL + 증류수 → 2.0 mL, 상대 농도 1–4. 통제: 25 °C, NaHSO3·녹말 2.0 mL, 전체 4.0 mL.
     · 모형: 색이 변할 때까지 걸린 시간 t = 지도서 예시 값 3.66 / 1.70 / 0.85 / 0.50 s × (1 ± 3 % 고정 시드 오차). 반응 속도 = 1/t.
     · 「섞고 측정」→ 초시계가 실제 시간으로 흐르고, t에 이르면 용액이 청람색으로 변함 → 표·그래프(반응 속도–상대 농도)에 쌓임.
   em44temp : 교과서 112–113쪽 탐구 「온도에 따른 반응 속도 측정하기」(CaCl2 + NaHCO3, 레이저)
     · 모형: 레이저 빛이 사라질 때까지 걸린 시간 t — 지도서 예시 값 (1.8 °C, 151 s)·(18 °C, 39 s)·(40 °C, 9 s)를 지나도록 ln t를 1/T에 대해 구간별 직선으로 이음(양 끝은 연장) × (1 ± 3 %). 25 → 35 °C 약 1.9배(약 2배).
     · 분포 곡선은 모형 그림(눈금 없음): f(E) ∝ √E·e^(−E/kT), kT = 1 + 0.015(t − 18), E_a = 3.6 (온도와 관계없이 고정). */
window.DECK_LABS = {
  em44conc(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svgs=root.querySelectorAll('svg'), g1=API.mk('g',{},svgs[0]), g2=API.mk('g',{},svgs[1]);
    const VOL=['','0.5 + 1.5 mL','1.0 + 1.0 mL','1.5 + 0.5 mL','2.0 + 0 mL'], MARK=['','①','②','③','④'], TC=[0,3.66,1.70,0.85,0.50], CD=0.6;
    let st={w:1,run:null,n:0}, log=[];
    function rng(seed){ let x=seed>>>0||1; return ()=>{ x=(x*1664525+1013904223)>>>0; return x/4294967296; }; }
    const X0=62,Y0=205,W=290,H=158, XX=c=>X0+c/4*W, YY=v=>Y0-v/2.5*H;
    function txt(g,x,y,s,o={}){ const t=API.mk('text',{x,y,'text-anchor':o.a||'middle','font-size':o.size||19,fill:o.fill||API.COL.muted,'font-weight':o.w||400},g); t.textContent=s; return t; }
    function drawWell(){
      g1.innerHTML='';
      const R=st.run, t=R?R.t:0, tc=R?R.tc:1e9;
      const p=R? API.clamp((t-tc)/CD,0,1):0;   // 색 변화(0.6 s 동안)
      txt(g1,125,22,'홈 '+MARK[R?R.w:st.w],{fill:API.COL.ink,size:20,w:700});
      API.mk('path',{d:'M45 34 L45 150 Q45 166 61 166 L189 166 Q205 166 205 150 L205 34',fill:'#fff',stroke:'#7E8B98','stroke-width':3},g1);
      if(R){ API.mk('rect',{x:47,y:64,width:156,height:100,rx:12,fill:'#EEF6FB'},g1);
        API.mk('rect',{x:47,y:64,width:156,height:100,rx:12,fill:'#22306E',opacity:(0.92*p).toFixed(3)},g1); }
      else API.mk('rect',{x:47,y:112,width:156,height:52,rx:10,fill:'#BFDDF2'},g1);
      // 초시계
      API.mk('circle',{cx:125,cy:208,r:32,fill:'#fff',stroke:API.COL.ink,'stroke-width':3},g1);
      API.mk('rect',{x:119,y:170,width:12,height:8,fill:API.COL.ink},g1);
      const a=(t%10)/10*2*Math.PI;
      API.mk('line',{x1:125,y1:208,x2:125+24*Math.sin(a),y2:208-24*Math.cos(a),stroke:API.COL.plus,'stroke-width':3,'stroke-linecap':'round'},g1);
      API.mk('circle',{cx:125,cy:208,r:4,fill:API.COL.ink},g1);
    }
    function drawGraph(){
      g2.innerHTML='';
      for(let c=0;c<=4;c++){ API.mk('line',{x1:XX(c),y1:Y0,x2:XX(c),y2:Y0-H,stroke:'#E6EBF0'},g2); txt(g2,XX(c),Y0+22,String(c)); }
      for(let v=0;v<=2.501;v+=0.5){ API.mk('line',{x1:X0,y1:YY(v),x2:X0+W,y2:YY(v),stroke:'#E6EBF0'},g2); txt(g2,X0-8,YY(v)+6,v.toFixed(1),{a:'end'}); }
      API.mk('line',{x1:X0,y1:Y0,x2:X0+W+10,y2:Y0,stroke:API.COL.muted,'stroke-width':2},g2);
      API.mk('line',{x1:X0,y1:Y0,x2:X0,y2:Y0-H-8,stroke:API.COL.muted,'stroke-width':2},g2);
      const xs=new Set(log.map(r=>r.w));
      if(xs.size>=2){ const s=[...log].sort((a,b)=>a.w-b.w);
        API.mk('path',{d:s.map((r,i)=>(i?'L':'M')+XX(r.w).toFixed(1)+' '+YY(r.v).toFixed(1)).join(' '),fill:'none',stroke:API.COL.ink,'stroke-width':2,'stroke-dasharray':'7 5',opacity:.6},g2); }
      log.forEach((r,i)=>API.mk('circle',{cx:XX(r.w),cy:YY(r.v),r:6,fill:i===log.length-1?API.COL.plus:'#fff',stroke:API.COL.ink,'stroke-width':2},g2));
      API.place(Ov('yl'),X0+8,0); API.place(Ov('xl'),X0+W-92,Y0-30);
    }
    function renderLog(){
      O('log').innerHTML=log.map((r,i)=>`<tr${i===log.length-1?' class="hl"':''}><td>${MARK[r.w]}</td><td>${r.w}</td><td>${r.t.toFixed(2)}</td><td>${r.v.toFixed(2)}</td></tr>`).join('')||'<tr><td colspan="4">아직 측정값이 없다</td></tr>';
    }
    function draw(){
      root.querySelectorAll('[data-w]').forEach(b=>b.classList.toggle('on',+b.dataset.w===st.w));
      O('vol').textContent=VOL[st.w]; O('rc').textContent=String(st.w);
      const R=st.run;
      O('clk').textContent=R? (Math.min(R.t,R.tc)).toFixed(2)+' s' : '0.00 s';
      O('rate').textContent=R&&R.done? (1/R.tc).toFixed(2)+' /s' : '–';
      drawWell(); drawGraph();
    }
    function finish(){
      const R=st.run; R.done=true;
      log.push({w:R.w,t:R.tc,v:1/R.tc}); if(log.length>6) log.shift(); renderLog();
      const ws=[...new Set(log.map(r=>r.w))].sort();
      O('msg').textContent=`홈 ${MARK[R.w]}: ${R.tc.toFixed(2)} s 만에 청람색으로 변했다.\n`+
        (ws.length>=3? '상대 농도가 클수록 걸린 시간이 짧다 — 농도가 클수록 반응 속도가 빠르다.' : '다른 홈도 측정해 비교해 보자.');
    }
    root.querySelectorAll('[data-w]').forEach(b=>b.addEventListener('click',()=>{ if(st.run&&!st.run.done) return; st.w=+b.dataset.w; st.run=null; O('msg').textContent='「섞고 측정」을 눌러 보자.'; draw(); }));
    root.querySelector('[data-act="run"]').addEventListener('click',()=>{
      if(st.run&&!st.run.done) return;
      st.n++; const r=rng(st.w*97+st.n*131);
      st.run={w:st.w,t:0,tc:TC[st.w]*(1+(r()*2-1)*0.03),done:false};
      O('msg').textContent='섞었다! 색이 변할 때까지 지켜보자.'; draw();
    });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ st={w:1,run:null,n:0}; log=[]; renderLog(); O('msg').textContent='홈을 고르고 「섞고 측정」을 눌러 보자.'; draw(); });
    API.loop(root,dt=>{
      const R=st.run; if(!R||R.t>=R.tc+CD) return;
      R.t+=dt; if(!R.done&&R.t>=R.tc) finish(); draw();
    });
    const setLab=()=>{ Ov('yl').innerHTML='반응 속도 [1/s]'; Ov('xl').innerHTML='상대 농도'; };
    setLab(); renderLog(); O('msg').textContent='홈을 고르고 「섞고 측정」을 눌러 보자.'; draw();
    API.ready(()=>{ setLab(); draw(); });
  },

  em44temp(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=root.querySelector('[data-i="T"]');
    const svgs=root.querySelectorAll('svg'), g1=API.mk('g',{},svgs[0]), g2=API.mk('g',{},svgs[1]), g3=API.mk('g',{},svgs[2]);
    let st={run:null,n:0}, log=[];
    function rng(seed){ let x=seed>>>0||1; return ()=>{ x=(x*1664525+1013904223)>>>0; return x/4294967296; }; }
    function txt(g,x,y,s,o={}){ const t=API.mk('text',{x,y,'text-anchor':o.a||'middle','font-size':o.size||19,fill:o.fill||API.COL.muted},g); t.textContent=s; return t; }
    const PT=[[1.8,151],[18,39],[40,9]].map(([c,t])=>[1/(c+273.15),Math.log(t)]);
    const tcOf=T=>{ const x=1/(T+273.15), [a,b]=x>PT[1][0]?[PT[0],PT[1]]:[PT[1],PT[2]]; return Math.exp(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])); };
    // 분포 곡선 (모형)
    const DX=40,DY=212,DW=372,DH=178,EMAX=7,FMAX=0.72,EA=3.6;
    const f=(E,kT)=>E<=0?0:2/Math.sqrt(Math.PI)*Math.pow(kT,-1.5)*Math.sqrt(E)*Math.exp(-E/kT);
    const kTof=T=>1+0.015*(T-18);
    const PX=E=>DX+E/EMAX*DW, PY=v=>DY-v/FMAX*DH;
    function curve(kT,from=0){ let d=''; for(let i=0;i<=140;i++){ const E=from+(EMAX-from)*i/140; d+=(i?'L':'M')+PX(E).toFixed(1)+' '+PY(f(E,kT)).toFixed(1); } return d; }
    function area(kT){ let s=0; const h=(12-EA)/2000; for(let i=0;i<2000;i++) s+=f(EA+(i+.5)*h,kT)*h; return s; }
    function drawDist(T){
      g2.innerHTML='';
      API.mk('line',{x1:DX,y1:DY,x2:DX+DW+8,y2:DY,stroke:API.COL.muted,'stroke-width':2},g2);
      API.mk('line',{x1:DX,y1:DY,x2:DX,y2:DY-DH-6,stroke:API.COL.muted,'stroke-width':2},g2);
      const kT=kTof(T), col=T>18?API.COL.plus:(T<18?API.COL.minus:API.COL.ink);
      API.mk('path',{d:curve(kT,EA)+` L${PX(EMAX)} ${DY} L${PX(EA)} ${DY} Z`,fill:col,opacity:.25},g2);
      API.mk('path',{d:curve(1),fill:'none',stroke:API.COL.muted,'stroke-width':2.5,'stroke-dasharray':'7 6'},g2);
      API.mk('path',{d:curve(kT),fill:'none',stroke:col,'stroke-width':3.5},g2);
      API.mk('line',{x1:PX(EA),y1:DY,x2:PX(EA),y2:DY-DH+10,stroke:API.COL.equi,'stroke-width':2.5,'stroke-dasharray':'7 6'},g2);
      txt(g2,DX+DW,24,'점선: 18 °C',{a:'end'}); txt(g2,DX+DW,46,`실선: ${T} °C`,{a:'end',fill:col});
      API.place(Ov('ea'),PX(EA)+6,DY-DH+2); API.place(Ov('ky'),DX+8,0); API.place(Ov('kx'),DX+DW-110,DY+6);
      return area(kT)/area(1);
    }
    function drawFlask(p){
      g1.innerHTML='';
      API.mk('rect',{x:86,y:4,width:28,height:34,rx:5,fill:'#2F343B'},g1);
      API.mk('line',{x1:100,y1:38,x2:100,y2:132,stroke:API.COL.plus,'stroke-width':3,opacity:.85},g1);
      const body='M84 60 L84 100 L36 196 Q32 208 46 208 L154 208 Q168 208 164 196 L116 100 L116 60';
      API.mk('path',{d:body,fill:'#fff',stroke:'#7E8B98','stroke-width':3},g1);
      const liq='M70 132 L130 132 L164 196 Q168 208 154 208 L46 208 Q32 208 36 196 Z';
      API.mk('path',{d:liq,fill:'#EEF6FB'},g1);
      API.mk('path',{d:liq,fill:'#E2DED4',opacity:(0.95*p).toFixed(3)},g1);
      API.mk('line',{x1:100,y1:132,x2:100,y2:226,stroke:API.COL.plus,'stroke-width':3,opacity:(0.85*(1-p)).toFixed(3)},g1);
      API.mk('path',{d:body,fill:'none',stroke:'#7E8B98','stroke-width':3},g1);
      API.mk('ellipse',{cx:100,cy:216,rx:78,ry:7,fill:'#DDEEF8',stroke:'#9FC3DD','stroke-width':2},g1);
      API.mk('rect',{x:8,y:223,width:184,height:12,fill:'#fff',stroke:'#C9D3DD','stroke-width':2},g1);
      API.mk('ellipse',{cx:100,cy:229,rx:11,ry:4,fill:API.COL.plus,opacity:(0.9*(1-p)).toFixed(3)},g1);
      txt(g1,100,252,p>=1?'빛이 사라짐':'흰 종이',{fill:p>=1?API.COL.plus:API.COL.muted});
    }
    const GX=56,GY=150,GW=250,GH=104, gx=T=>GX+T/50*GW, gy=v=>GY-v/0.24*GH;
    function drawGraph(){
      g3.innerHTML='';
      for(let T=0;T<=50;T+=10){ API.mk('line',{x1:gx(T),y1:GY,x2:gx(T),y2:GY-GH,stroke:'#E6EBF0'},g3); txt(g3,gx(T),GY+21,String(T)); }
      for(let v=0;v<=0.2401;v+=0.08){ API.mk('line',{x1:GX,y1:gy(v),x2:GX+GW,y2:gy(v),stroke:'#E6EBF0'},g3); txt(g3,GX-7,gy(v)+6,v.toFixed(2),{a:'end'}); }
      API.mk('line',{x1:GX,y1:GY,x2:GX+GW+8,y2:GY,stroke:API.COL.muted,'stroke-width':2},g3);
      API.mk('line',{x1:GX,y1:GY,x2:GX,y2:GY-GH-6,stroke:API.COL.muted,'stroke-width':2},g3);
      const s=[...log].sort((a,b)=>a.T-b.T);
      if(s.length>=2) API.mk('path',{d:s.map((r,i)=>(i?'L':'M')+gx(r.T).toFixed(1)+' '+gy(r.v).toFixed(1)).join(' '),fill:'none',stroke:API.COL.ink,'stroke-width':2,'stroke-dasharray':'6 5',opacity:.6},g3);
      log.forEach((r,i)=>API.mk('circle',{cx:gx(r.T),cy:gy(r.v),r:5.5,fill:i===log.length-1?API.COL.plus:'#fff',stroke:API.COL.ink,'stroke-width':2},g3));
      API.place(Ov('gy'),GX+6,0); API.place(Ov('gx'),GX+GW-72,0);
    }
    function renderLog(){
      O('log').innerHTML=log.map((r,i)=>`<tr${i===log.length-1?' class="hl"':''}><td>${r.T}</td><td>${r.t.toFixed(0)}</td><td>${r.v<0.01?r.v.toFixed(4):r.v.toFixed(3)}</td></tr>`).join('')||'<tr><td colspan="3">아직 측정값이 없다</td></tr>';
    }
    let ratio=1;
    function draw(){
      const T=+I.value; O('T').textContent=T+' °C';
      root.querySelectorAll('[data-p]').forEach(b=>b.classList.toggle('on',+b.dataset.p===T));
      const R=st.run;
      O('clk').textContent=R? Math.min(R.t,R.tc).toFixed(1)+' s':'0.0 s';
      O('rate').textContent=R&&R.done? (1/R.tc<0.01?(1/R.tc).toFixed(4):(1/R.tc).toFixed(3))+' /s':'–';
      drawFlask(R? API.clamp(R.t/R.tc,0,1):0);
      ratio=drawDist(R?R.T:T); drawGraph();
    }
    function finish(){
      const R=st.run; R.done=true;
      log.push({T:R.T,t:R.tc,v:1/R.tc}); if(log.length>6) log.shift(); renderLog();
      const more=ratio>1.05?'많다':(ratio<0.95?'적다':'같다');
      O('msg').textContent=`${R.T} °C: ${R.tc.toFixed(0)} s 만에 레이저 빛이 사라졌다.\n색칠한 넓이(활성화 에너지 이상의 에너지를 가진 분자 수)가 18 °C보다 ${more}.`+
        (new Set(log.map(r=>r.T)).size>=3?'\n온도가 높을수록 걸린 시간이 짧다 — 반응 속도가 빠르다.':'');
    }
    I.addEventListener('input',()=>{ if(st.run&&!st.run.done) return; st.run=null; draw(); });
    root.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{ if(st.run&&!st.run.done) return; I.value=b.dataset.p; st.run=null; draw(); }));
    root.querySelector('[data-act="run"]').addEventListener('click',()=>{
      if(st.run&&!st.run.done) return;
      const T=+I.value; st.n++; const r=rng(T*53+st.n*89+7), tc=tcOf(T)*(1+(r()*2-1)*0.03);
      st.run={T,t:0,tc,sp:Math.max(8,tc/7),done:false};
      O('msg').textContent='섞었다! 레이저 빛이 사라질 때까지 기다리자(초시계 빠르게).'; draw();
    });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ st={run:null,n:0}; log=[]; I.value=18; renderLog(); O('msg').textContent='온도를 고르고 「섞고 측정」을 눌러 보자.'; draw(); });
    API.loop(root,dt=>{
      const R=st.run; if(!R||R.done) return;
      R.t+=dt*R.sp; if(R.t>=R.tc) finish(); draw();
    });
    const setLab=()=>{ Ov('ea').innerHTML=API.tex('E_\\mathrm{a}'); Ov('ky').innerHTML='분자 수'; Ov('kx').innerHTML='운동 에너지'; Ov('gy').innerHTML='반응 속도 [1/s]'; Ov('gx').innerHTML='온도 [°C]'; };
    setLab(); renderLog(); O('msg').textContent='온도를 고르고 「섞고 측정」을 눌러 보자.'; draw();
    API.ready(()=>{ setLab(); draw(); });
  }
};
