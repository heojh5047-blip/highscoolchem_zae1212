/* 4-2 일차 반응의 반감기 — 실험실
   em42half : 처음 농도를 바꾸어 반감기 찾기 (덱 보충 모의실험, 교과서 102–103쪽 해 보기·그림 IV-3과 연습 해 보기 자료)
     · 반응 N: 2N2O5(g) -> 4NO2(g) + O2(g), t½ = 100 s (교과서 그림 IV-3) / 반응 A: A(g) -> B(g), t½ = 50 s (연습 해 보기)
     · 모형: 일차 반응 [A] = [A]0 × (1/2)^(t / t½)  (적분 속도식은 화면에 쓰지 않음 — 반감기마다 절반)
     · 측정점: t½/4 간격, 고정 시드의 작은 오차(±0.5 % of [A]0). 반감기는 측정점을 직선으로 이어 [A]0/2, [A]0/4를 지나는 시각으로 구함
     · 분자 상자: 처음 분자 수 = round([A]0 × 250). 분자마다 수명 τ = −t½·log2(u)(u는 층화한 난수) → 시각 t에 τ < t인 분자는 반응함(점선)
     · 「반응 시작」→ 6초 동안 4 t½까지 진행 · 「기록」→ 표에 쌓임 · 두 처음 농도를 기록하면 해석 문장 */
window.DECK_LABS = {
  em42half(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg[data-v="g"]'), box=$('svg[data-v="box"]');
    const g=API.mk('g',{},svg), gb=API.mk('g',{},box);
    const RX={N:{T:100, name:'N2O5 분해', y:'[\\ce{N2O5}]'}, A:{T:50, name:'A → B', y:'[\\ce{A}]'}};
    const X0=78, Y0=236, W=520, H=190, YMAX=0.12;
    let st={r:'N', run:null, prog:0, runNo:0}, log=[];
    function rng(seed){ let x=seed>>>0||1; return ()=>{ x=(x*1664525+1013904223)>>>0; return x/4294967296; }; }
    function newRun(){
      const c0=+I('c').value, T=RX[st.r].T; st.runNo++;
      const r=rng(Math.round(c0*100)*37+T+st.runNo*101), pts=[];
      for(let k=0;k<=16;k++){ const t=k*T/4; pts.push([t, c0*Math.pow(0.5,t/T)+(k?(r()*2-1)*0.005*c0:0)]); }
      const N=Math.round(c0*250), us=[];
      for(let i=0;i<N;i++) us.push((i+0.5)/N);
      for(let i=N-1;i>0;i--){ const j=Math.floor(r()*(i+1)); [us[i],us[j]]=[us[j],us[i]]; }
      const pos=[]; let tries=0;
      while(pos.length<N && tries<5000){ tries++; const x=14+r()*202, y=14+r()*126; if(pos.every(p=>(p[0]-x)**2+(p[1]-y)**2>15*15)) pos.push([x,y,r()*6.28]); }
      while(pos.length<N) pos.push([14+r()*202,14+r()*126,r()*6.28]);
      st.run={r:st.r, c0, T, pts, tau:us.map(u=>-T*Math.log2(u)), pos};
      st.prog=0;
    }
    function cross(pts, target){
      for(let k=1;k<pts.length;k++){ const [t1,c1]=pts[k-1], [t2,c2]=pts[k];
        if(c1>=target && c2<target) return t1+(c1-target)/(c1-c2)*(t2-t1); }
      return null;
    }
    const XX=t=>X0+t/(4*st.run.T)*W, YY=c=>Y0-c/YMAX*H;
    function axes(T){
      for(let k=0;k<=4;k++){ const x=X0+k/4*W; API.mk('line',{x1:x,y1:Y0,x2:x,y2:Y0-H,stroke:'#E6EBF0'},g);
        const tx=API.mk('text',{x,y:Y0+24,'text-anchor':'middle','font-size':18,fill:API.COL.muted},g); tx.textContent=k*T; }
      for(let v=0;v<=0.12001;v+=0.02){ const y=Y0-v/YMAX*H; API.mk('line',{x1:X0,y1:y,x2:X0+W,y2:y,stroke:'#E6EBF0'},g);
        const tx=API.mk('text',{x:X0-8,y:y+6,'text-anchor':'end','font-size':18,fill:API.COL.muted},g); tx.textContent=v?v.toFixed(2):'0'; }
      API.mk('line',{x1:X0,y1:Y0,x2:X0+W+12,y2:Y0,stroke:API.COL.muted,'stroke-width':2},g);
      API.mk('line',{x1:X0,y1:Y0,x2:X0,y2:Y0-H-10,stroke:API.COL.muted,'stroke-width':2},g);
    }
    function drawBox(){
      gb.innerHTML='';
      API.mk('rect',{x:3,y:3,width:224,height:166,rx:10,fill:'#fff',stroke:'#7E8B98','stroke-width':2},gb);
      if(!st.run) return;
      const R=st.run, tt=performance.now()/1000; let left=0;
      R.pos.forEach((p,i)=>{
        const on=R.tau[i]>st.prog; if(on) left++;
        const jx=on?Math.sin(tt*3+p[2])*1.6:0, jy=on?Math.cos(tt*2.6+p[2])*1.6:0;
        API.mk('circle',on?{cx:p[0]+jx,cy:p[1]+jy,r:6,fill:API.COL.ink}:{cx:p[0],cy:p[1],r:6,fill:'none',stroke:'#9AA5B1','stroke-width':1.5,'stroke-dasharray':'3 2'},gb);
      });
      const tx=API.mk('text',{x:115,y:160,'text-anchor':'middle','font-size':17,fill:API.COL.muted},gb); tx.textContent=`남은 분자 ${left} / ${R.pos.length}`;
    }
    const fmtT=v=>v==null?'–':Math.round(v)+' s';
    function draw(){
      const c=+I('c').value;
      O('c').textContent=c.toFixed(2)+' mol/L';
      root.querySelectorAll('[data-r]').forEach(b=>b.classList.toggle('on',b.dataset.r===st.r));
      if(!st.run) newRun();
      const R=st.run; g.innerHTML=''; axes(R.T);
      Ov('yl').innerHTML=API.tex(RX[R.r].y+'\\ [\\text{mol/L}]'); API.place(Ov('yl'),X0+12,0);
      Ov('xl').innerHTML=API.tex('t\\ [\\text{s}]'); API.place(Ov('xl'),X0+W+16,Y0-36);
      const shown=R.pts.filter(p=>p[0]<=st.prog+1e-6), done=st.prog>=4*R.T-1e-6;
      let d=''; for(let u=0;u<=Math.min(st.prog,4*R.T);u+=R.T/40) d+=(u?'L':'M')+XX(u).toFixed(1)+' '+YY(R.c0*Math.pow(.5,u/R.T)).toFixed(1);
      if(d) API.mk('path',{d,fill:'none',stroke:'#9FB0C2','stroke-width':2},g);
      shown.forEach(p=>API.mk('circle',{cx:XX(p[0]),cy:YY(p[1]),r:4.5,fill:'#fff',stroke:API.COL.ink,'stroke-width':2},g));
      const t1=cross(R.pts,R.c0/2), t2a=cross(R.pts,R.c0/4);
      const h1=(t1!=null&&st.prog>=t1)?t1:null, h2=(t2a!=null&&st.prog>=t2a)?t2a-t1:null;
      [['m1',h1,0,t1,R.c0/2],['m2',h2,t1,t2a,R.c0/4]].forEach(([k,h,a,b,cc])=>{
        if(h==null){ API.place(Ov(k),0,0,false); return; }
        API.mk('line',{x1:X0,y1:YY(cc),x2:XX(b),y2:YY(cc),stroke:API.COL.muted,'stroke-width':1.6,'stroke-dasharray':'5 5'},g);
        API.mk('line',{x1:XX(b),y1:Y0,x2:XX(b),y2:YY(cc),stroke:API.COL.muted,'stroke-width':1.6,'stroke-dasharray':'5 5'},g);
        const y=Y0-14; API.mk('line',{x1:XX(a)+3,y1:y,x2:XX(b)-3,y2:y,stroke:API.COL.ink,'stroke-width':2},g);
        API.mk('polygon',{points:`${XX(a)},${y} ${XX(a)+9},${y-4.5} ${XX(a)+9},${y+4.5}`,fill:API.COL.ink},g);
        API.mk('polygon',{points:`${XX(b)},${y} ${XX(b)-9},${y-4.5} ${XX(b)-9},${y+4.5}`,fill:API.COL.ink},g);
        Ov(k).innerHTML=API.tex('t_{1/2}'); API.place(Ov(k),(XX(a)+XX(b))/2,y-30);
      });
      O('t').textContent=Math.round(Math.min(st.prog,4*R.T))+' s';
      O('now').textContent=(R.c0*Math.pow(.5,Math.min(st.prog,4*R.T)/R.T)).toFixed(4)+' mol/L';
      O('h1').textContent=fmtT(h1); O('h2').textContent=fmtT(h2);
      if(st.prog===0) O('msg').textContent='「반응 시작」을 눌러 농도 변화를 측정해 보자.';
      else if(!done) O('msg').textContent='반응 중 … 남은 분자 수가 줄어들수록 줄어드는 빠르기도 느려진다.';
      else if(judgeable()) O('msg').textContent=judge();
      else O('msg').textContent=`첫째·둘째 반감기가 모두 약 ${R.T} s로 같다. 「기록」을 누르고 처음 농도만 바꾸어 다시 해 보자.`;
      drawBox();
    }
    function judgeable(){ const rs=log.filter(x=>x.r===st.r); return rs.length>=2 && new Set(rs.map(x=>x.c0.toFixed(2))).size>=2; }
    function judge(){
      const rs=log.filter(x=>x.r===st.r), cs=[...new Set(rs.map(x=>x.c0.toFixed(2)))].join(', ');
      const avg=rs.reduce((s,x)=>s+x.h1+x.h2,0)/(2*rs.length);
      return `처음 농도 ${cs} mol/L — 반감기는 모두 약 ${Math.round(avg)} s → 일차 반응의 반감기는 처음 농도에 관계없이 일정하다.`;
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(x=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${x.r==='N'?API.tex('\\ce{N2O5}'):API.tex('\\ce{A}')}</td><td>${x.c0.toFixed(2)}</td><td>${Math.round(x.h1)} s</td><td>${Math.round(x.h2)} s</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-r]').forEach(b=>b.addEventListener('click',()=>{ st.r=b.dataset.r; newRun(); draw(); }));
    I('c').addEventListener('input',()=>{ newRun(); draw(); });
    $('[data-act="run"]').addEventListener('click',()=>{ newRun(); st.prog=1e-3; draw(); });
    $('[data-act="rec"]').addEventListener('click',()=>{
      const R=st.run; if(!R||st.prog<4*R.T-1e-6){ O('msg').textContent='반응이 끝난 뒤 기록하자.'; return; }
      const t1=cross(R.pts,R.c0/2), t2=cross(R.pts,R.c0/4);
      log.push({r:R.r,c0:R.c0,h1:t1,h2:t2-t1}); if(log.length>5) log.shift();
      renderLog(); draw(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; st={r:'N',run:null,prog:0,runNo:0}; I('c').value=0.10; renderLog(); draw(); });
    API.loop(root,dt=>{ const R=st.run; if(R&&st.prog>0&&st.prog<4*R.T){ st.prog=Math.min(4*R.T,st.prog+dt*4*R.T/6); draw(); } else drawBox(); });
    // 정지 화면(인쇄·캡처)용: 끝난 상태를 보여 준다
    newRun(); st.prog=4*st.run.T; draw(); API.ready(draw);
  }
};
