/* 4-1 화학 반응 속도 — 실험실
   em41rate : 센서로 반응 속도 측정 (필수 탐구 물04-탐1, 교과서 98–99쪽 「센서를 활용해 반응 속도를 측정하는 실험 설계하고 수행하기」)
     · 반응 Mg(s) + 2HCl(aq) -> MgCl2(aq) + H2(g), 25 °C, 염산 50 mL(처음 농도 C0 = 0.10–0.40 mol/L), 마그네슘 0.4 g(과량).
     · 모형(수업용 가정): 염산에 대해 일차, [HCl] = C0·e^(−kt), k = 1.0×10^-3 /s (지도서 예시 그래프의 시간 척도: 0.2 M에서 약 3500 s 동안 압력이 올라 거의 일정해짐).  H2 몰수 n = C0·0.050/2·(1 − e^(−kt)).
     · 압력 센서(가지 달린 삼각 플라스크 250 mL, 기체 공간 0.20 L): P = 101.3 + n·RT/0.20 (kPa), R = 8.31 kPa·L/(mol·K), T = 298.
     · 시간–농도 그래프: [H2] = n/0.20 = ΔP/(RT) (mol/L).  초기 H2 생성 속도 = C0·1.25×10^-4 mol/(L·s).
     · 측정점 100 s 간격(0–3500 s), 고정 시드 작은 오차. 「반응 시작」→ 측정점이 실시간으로 찍힘(1 s당 600 s). 「기록」→ 표·그래프에 쌓임. 「초기화」. */
window.DECK_LABS = {
  em41rate(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svgs=root.querySelectorAll('svg'), svg=svgs[0], svg2=svgs[1];
    const g=API.mk('g',{},svg), g2=API.mk('g',{},svg2);
    const K=0.0010, RT=8.31*298, TE=3500, DT=100, VG=0.20, VS=0.050;
    const X0=72, Y0=228, W=500, H=196;
    const RANGE={P:[100,240,20], C:[0,0.06,0.01]};
    let st={s:'P', run:null, prog:TE, runNo:0}, log=[];
    const n=(C,t)=>C*VS/2*(1-Math.exp(-K*t));
    const model=(s,C,t)=> s==='P' ? 101.3+n(C,t)*RT/VG : n(C,t)/VG;
    const slope=(s,C,t)=>{ const dn=C*VS/2*K*Math.exp(-K*t); return s==='P' ? dn*RT/VG : dn/VG; };
    const conv=s=> s==='P' ? 1/RT : 1;   // → H2 생성 속도 mol/(L·s)
    function rng(seed){ let x=seed>>>0||1; return ()=>{ x=(x*1664525+1013904223)>>>0; return x/4294967296; }; }
    function newRun(){
      const C=+I('c').value, s=st.s; st.runNo++;
      const r=rng(Math.round(C*100)*31+(s==='P'?7:13)+st.runNo*101);
      const amp=s==='P'?0.4:0.0002, pts=[];
      for(let t=0;t<=TE;t+=DT) pts.push([t, model(s,C,t)+(t?(r()*2-1)*amp:0)]);
      st.run={s, C, pts, f:1+(r()*2-1)*0.02};
    }
    const sci=(v,d=1)=>{ if(!v) return '0'; let e=Math.floor(Math.log10(Math.abs(v))), m=v/10**e; if(+m.toFixed(d)>=10){ m/=10; e++; } return API.tex(`${m.toFixed(d)}\\times10^{${e}}`); };
    const unit=s=> s==='P'?'kPa/s':'mol/(L·s)';
    const XX=t=>X0+t/TE*W, YY=(v,s)=>{ const [a,b]=RANGE[s]; return Y0-(v-a)/(b-a)*H; };
    function axes(s){
      const [a,b,d]=RANGE[s];
      for(let t=0;t<=TE;t+=500){ API.mk('line',{x1:XX(t),y1:Y0,x2:XX(t),y2:Y0-H,stroke:'#E6EBF0'},g);
        const tx=API.mk('text',{x:XX(t),y:Y0+22,'text-anchor':'middle','font-size':17,fill:API.COL.muted},g); tx.textContent=t; }
      for(let v=a;v<=b+1e-9;v+=d){ API.mk('line',{x1:X0,y1:YY(v,s),x2:X0+W,y2:YY(v,s),stroke:'#E6EBF0'},g);
        const tx=API.mk('text',{x:X0-8,y:YY(v,s)+6,'text-anchor':'end','font-size':17,fill:API.COL.muted},g); tx.textContent=(s==='P'?v.toFixed(0):v.toFixed(2)); }
      API.mk('line',{x1:X0,y1:Y0,x2:X0+W+10,y2:Y0,stroke:API.COL.muted,'stroke-width':2},g);
      API.mk('line',{x1:X0,y1:Y0,x2:X0,y2:Y0-H-8,stroke:API.COL.muted,'stroke-width':2},g);
    }
    function draw(){
      const C=+I('c').value, t=+I('t').value;
      O('c').textContent=C.toFixed(2)+' mol/L'; O('t').textContent=t+' s';
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===st.s));
      g.innerHTML='';
      const s=st.run?st.run.s:st.s; axes(s);
      Ov('yl').innerHTML=API.tex(s==='P'?'P\\ [\\text{kPa}]':'[\\ce{H2}]\\ [\\text{mol/L}]'); API.place(Ov('yl'),X0+44,4);
      Ov('xl').innerHTML=API.tex('t\\ [\\text{s}]'); API.place(Ov('xl'),X0+W+6,Y0-26);
      if(!st.run){ ['val','avg','ins','v0'].forEach(k=>O(k).textContent='–'); O('msg').textContent='「반응 시작」을 눌러 측정하자.'; drawSmall(); return; }
      const R=st.run, shown=R.pts.filter(p=>p[0]<=st.prog+1e-6);
      // 모형 곡선(진행한 데까지, 옅게) + 측정점
      let d=''; for(let u=0;u<=Math.min(st.prog,TE);u+=50) d+=(u?'L':'M')+XX(u).toFixed(1)+' '+YY(model(R.s,R.C,u),R.s).toFixed(1);
      if(d) API.mk('path',{d,fill:'none',stroke:'#9FB0C2','stroke-width':2},g);
      shown.forEach(p=>API.mk('circle',{cx:XX(p[0]),cy:YY(p[1],R.s),r:4,fill:'#fff',stroke:API.COL.ink,'stroke-width':2},g));
      const done=st.prog>=TE;
      if(t<=st.prog){
        const vt=R.pts[t/DT][1];
        O('val').textContent=R.s==='P'?vt.toFixed(1)+' kPa':vt.toFixed(4)+' mol/L';
        if(t+300<=st.prog){ const v2=R.pts[t/DT+3][1];
          API.mk('line',{x1:XX(t),y1:YY(vt,R.s),x2:XX(t+300),y2:YY(v2,R.s),stroke:API.COL.muted,'stroke-width':3,'stroke-dasharray':'7 5'},g);
          O('avg').innerHTML=sci(Math.abs(v2-vt)/300)+' '+unit(R.s); } else O('avg').textContent='–';
        const sl=slope(R.s,R.C,t)*R.f, y=model(R.s,R.C,t), t1=Math.max(0,t-600), t2=Math.min(TE,t+900);
        API.mk('line',{x1:XX(t1),y1:YY(y+sl*(t1-t),R.s),x2:XX(t2),y2:YY(y+sl*(t2-t),R.s),stroke:API.COL.plus,'stroke-width':3.5,'stroke-linecap':'round'},g);
        API.mk('circle',{cx:XX(t),cy:YY(y,R.s),r:6,fill:API.COL.plus},g);
        O('ins').innerHTML=sci(Math.abs(sl))+' '+unit(R.s);
      } else { O('val').textContent='측정 중…'; O('avg').textContent='–'; O('ins').textContent='–'; }
      const v0=Math.abs(slope(R.s,R.C,0))*R.f*conv(R.s);
      O('v0').innerHTML=sci(v0)+' mol/(L·s)';
      if(!done) O('msg').textContent='측정 중 … 100 s마다 측정값이 찍힌다.';
      else if(log.length>=2) O('msg').innerHTML=judge();
      else if(t>=600) O('msg').textContent='시간이 지날수록 접선의 기울기가 작아진다 — 염산의 농도가 줄어 반응이 느려진다.';
      else O('msg').textContent='「기록」을 누르고, 염산 농도만 바꾸어 다시 측정하자.';
      drawSmall();
    }
    function judge(){
      const a=log.reduce((m,r)=>r.C<m.C?r:m,log[0]), b=log.reduce((m,r)=>r.C>m.C?r:m,log[0]);
      if(a.C===b.C) return '같은 농도끼리는 초기 속도가 거의 같다(재현성). 이제 염산의 농도만 바꾸어 보자.';
      const xc=b.C/a.C, xv=b.v/a.v, m=Math.log(xv)/Math.log(xc);
      return `농도 ×${xc.toFixed(1)} → 초기 속도 ×${xv.toFixed(1)} → 초기 반응 속도가 염산의 농도에 ${Math.round(m)===1?'비례한다':'비례하지 않는다'}`;
    }
    function drawSmall(){
      g2.innerHTML='';
      const x0=58,y0=148,w=170,h=118, XS=c=>x0+c/0.4*w, YS=v=>y0-v/6e-5*h;
      API.mk('line',{x1:x0,y1:y0,x2:x0+w+8,y2:y0,stroke:API.COL.muted,'stroke-width':2},g2);
      API.mk('line',{x1:x0,y1:y0,x2:x0,y2:y0-h-8,stroke:API.COL.muted,'stroke-width':2},g2);
      [0,0.2,0.4].forEach(c=>{ const tx=API.mk('text',{x:XS(c),y:y0+19,'text-anchor':'middle','font-size':16,fill:API.COL.muted},g2); tx.textContent=c?c.toFixed(1):'0'; });
      [0,2e-5,4e-5,6e-5].forEach(v=>{ const tx=API.mk('text',{x:x0-6,y:YS(v)+5,'text-anchor':'end','font-size':16,fill:API.COL.muted},g2); tx.textContent=(v*1e5).toFixed(0); });
      const t1=API.mk('text',{x:x0+w+4,y:y0+38,'text-anchor':'end','font-size':16,fill:API.COL.ink},g2); t1.textContent='염산 농도 (mol/L)';
      const t2=API.mk('text',{x:x0+6,y:14,'font-size':16,fill:API.COL.ink},g2); t2.textContent='수소 생성 속도 (×0.00001)';
      if(log.length>=2){ const kk=log.reduce((s,r)=>s+r.C*r.v,0)/log.reduce((s,r)=>s+r.C*r.C,0);
        API.mk('line',{x1:XS(0),y1:YS(0),x2:XS(0.42),y2:YS(kk*0.42),stroke:API.COL.muted,'stroke-width':2,'stroke-dasharray':'6 4'},g2); }
      log.forEach(r=>API.mk('circle',{cx:XS(r.C),cy:YS(r.v),r:6,fill:API.COL.plus,stroke:'#fff','stroke-width':1.5},g2));
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${r.C.toFixed(2)}</td><td>${sci(r.p)}</td><td>${sci(r.v)}</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ st.s=b.dataset.s; draw(); }));
    I('c').addEventListener('input',draw); I('t').addEventListener('input',draw);
    $('[data-act="run"]').addEventListener('click',()=>{ newRun(); st.prog=0; draw(); });
    $('[data-act="rec"]').addEventListener('click',()=>{
      if(!st.run||st.prog<TE){ O('msg').textContent='측정이 끝난 뒤 기록하자.'; return; }
      const R=st.run; log.push({s:R.s,C:R.C,v:Math.abs(slope('C',R.C,0))*R.f,p:Math.abs(slope('P',R.C,0))*R.f}); if(log.length>5) log.shift();
      renderLog(); draw(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; st={s:'P',run:null,prog:TE,runNo:0}; I('c').value=0.2; I('t').value=0; renderLog(); newRun(); draw(); });
    API.loop(root,dt=>{ if(st.run&&st.prog<TE){ const before=Math.floor(st.prog/DT); st.prog=Math.min(TE,st.prog+dt*600); if(Math.floor(st.prog/DT)!==before||st.prog>=TE) draw(); } });
    newRun(); draw(); API.ready(draw);
  }
};
