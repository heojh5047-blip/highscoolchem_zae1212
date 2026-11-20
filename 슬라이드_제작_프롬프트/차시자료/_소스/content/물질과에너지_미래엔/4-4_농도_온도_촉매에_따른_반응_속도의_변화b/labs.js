/* 4-4b 농도, 온도, 촉매에 따른 반응 속도의 변화 (2) 촉매 — 실험실 (필수 탐구 물04-탐2 ③ 촉매)
   em44cat : 교과서 116쪽 탐구 「반응 속도에 영향을 주는 물질 알아보기」 + 117쪽 그림 IV-11(덱 보충: 묽은 인산 = 부촉매)
     · 10 % 과산화 수소수 10 mL + 세제, 넣는 물질: 없음 / KI(정촉매) / 묽은 인산(부촉매).
     · 모형(수업용 가정): 거품 눈금 V(t) = 10 + 90(1 − e^(−kt)) mL (100 mL에서 넘침), k = 0.0015 / 0.12 / 0.0003 s⁻¹. 30 s 관찰(3배 빠르게).
     · 에너지 도표·분포 곡선은 눈금 없는 모형 그림: 분포 f(E) ∝ √E·e^(−E/kT), kT = 1(온도 일정), 활성화 에너지 3.6 / 2.0 / 4.8.
       「반응할 수 있는 분자(그림 넓이)」 = 경계 오른쪽 넓이 비율. ΔH는 세 경우 모두 같다. KI 질량은 반응 전후 0.20 g 그대로. */
window.DECK_LABS = {
  em44cat(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svgs=root.querySelectorAll('svg'), g1=API.mk('g',{},svgs[0]), g2=API.mk('g',{},svgs[1]), g3=API.mk('g',{},svgs[2]);
    const C={
      none:{name:'넣지 않음',ea:3.6,k:0.0015,col:API.COL.ink,eaTxt:'그대로(기준)',m:'–',rate:'기준'},
      ki:{name:'KI',ea:2.0,k:0.12,col:API.COL.field,eaTxt:'낮아짐',m:'0.20 g → 0.20 g',rate:'매우 빠름'},
      h3po4:{name:'묽은 인산',ea:4.8,k:0.0003,col:API.COL.bfield,eaTxt:'높아짐',m:'인산 → 그대로 남음',rate:'더 느림'}};
    let st={c:'none',run:null}, log=[];
    const f=(E,kT)=>E<=0?0:2/Math.sqrt(Math.PI)*Math.pow(kT,-1.5)*Math.sqrt(E)*Math.exp(-E/kT);
    function frac(ea){ let s=0; const h=(14-ea)/3000; for(let i=0;i<3000;i++) s+=f(ea+(i+.5)*h,1)*h; return s; }
    function txt(g,x,y,s,o={}){ const t=API.mk('text',{x,y,'text-anchor':o.a||'middle','font-size':o.size||18,fill:o.fill||API.COL.muted},g); t.textContent=s; return t; }
    const Vof=(c,t)=>Math.min(100,10+90*(1-Math.exp(-C[c].k*t)));
    // 1. 눈금실린더
    const YB=250, PXML=2.2, yv=v=>YB-v*PXML;
    function drawCyl(){
      g1.innerHTML='';
      const R=st.run, V=R?Vof(R.c,R.t):10;
      API.mk('rect',{x:30,y:252,width:90,height:10,rx:3,fill:'#9FB0C2'},g1);
      API.mk('rect',{x:45,y:20,width:60,height:232,rx:4,fill:'#fff',stroke:'#7E8B98','stroke-width':2.5},g1);
      API.mk('rect',{x:47,y:yv(10),width:56,height:10*PXML,fill:'#DDEEF8'},g1);
      if(V>10.3){ API.mk('rect',{x:47,y:yv(V),width:56,height:(V-10)*PXML,fill:'#F4F1EA'},g1);
        const n=Math.floor((V-10)/6); for(let i=0;i<n;i++) API.mk('circle',{cx:56+(i%4)*13,cy:yv(10)-8-Math.floor(i/4)*13,r:4.5,fill:'#fff',stroke:'#C9C2B0','stroke-width':1.2},g1); }
      if(R&&!R.done){ const nb=R.c==='ki'?8:1; for(let i=0;i<nb;i++){ const ph=((R.t*0.9+i*0.37)%1); API.mk('circle',{cx:54+((i*17)%44),cy:yv(10)+20-ph*20,r:2.5,fill:'#fff',stroke:'#9FC3DD','stroke-width':1},g1); } }
      for(let v=20;v<=100;v+=20){ API.mk('line',{x1:105,y1:yv(v),x2:96,y2:yv(v),stroke:API.COL.muted,'stroke-width':1.5},g1); txt(g1,128,yv(v)+6,String(v)); }
      txt(g1,128,16,'mL');
      if(V>=100) txt(g1,75,14,'넘침!',{fill:API.COL.plus,size:18});
      return V;
    }
    // 2. 에너지 도표
    const EX0=34,EY0=258,yR=172,yP=215;
    const yT=ea=>yR-ea/3.6*76;
    function ed(ea){ const x0=40,x1=110,xp=160,x2=210,x3=248,a=.55*(xp-x1),b=.55*(x2-xp),t=yT(ea);
      return `M${x0} ${yR} L${x1} ${yR} C${x1+a} ${yR} ${xp-a} ${t} ${xp} ${t} C${xp+b} ${t} ${x2-b} ${yP} ${x2} ${yP} L${x3} ${yP}`; }
    function dim(g,x,y1,y2,col){ API.mk('line',{x1:x,y1:y1+3,x2:x,y2:y2-3,stroke:col,'stroke-width':2.5},g);
      API.mk('polygon',{points:`${x},${y1} ${x-5},${y1+10} ${x+5},${y1+10}`,fill:col},g); API.mk('polygon',{points:`${x},${y2} ${x-5},${y2-10} ${x+5},${y2-10}`,fill:col},g); }
    function drawE(){
      g2.innerHTML='';
      API.mk('line',{x1:EX0,y1:EY0,x2:EX0+212,y2:EY0,stroke:API.COL.muted,'stroke-width':2},g2);
      API.mk('line',{x1:EX0,y1:EY0,x2:EX0,y2:30,stroke:API.COL.muted,'stroke-width':2},g2);
      API.mk('path',{d:ed(3.6),fill:'none',stroke:API.COL.ink,'stroke-width':3},g2);
      API.mk('line',{x1:56,y1:yT(3.6),x2:155,y2:yT(3.6),stroke:API.COL.muted,'stroke-width':1.3,'stroke-dasharray':'4 4'},g2);
      dim(g2,58,yT(3.6),yR,API.COL.equi);
      const c=C[st.c];
      if(st.c!=='none'){ API.mk('path',{d:ed(c.ea),fill:'none',stroke:c.col,'stroke-width':3,'stroke-dasharray':st.c==='ki'?'9 6':'13 5 3 5'},g2);
        API.mk('line',{x1:86,y1:yT(c.ea),x2:155,y2:yT(c.ea),stroke:API.COL.muted,'stroke-width':1.3,'stroke-dasharray':'4 4'},g2);
        dim(g2,88,yT(c.ea),yR,c.col); }
      API.mk('line',{x1:100,y1:yR,x2:240,y2:yR,stroke:API.COL.muted,'stroke-width':1.3,'stroke-dasharray':'4 4'},g2);
      txt(g2,70,yR+24,'반응물',{fill:API.COL.ink}); txt(g2,228,yP-10,'생성물',{fill:API.COL.ink});
      API.place(Ov('e1'),62,(yT(3.6)+yR)/2-14,true);
      const e2=Ov('e2'); e2.style.color=c.col; API.place(e2,92,(yT(c.ea)+yR)/2-6,st.c!=='none');
      API.place(Ov('ey'),EX0+6,0); API.place(Ov('ex'),EX0+96,EY0+1);
    }
    // 3. 분포 곡선
    const DX=28,DY=238,DW=212,DH=196,EMAX=7,FMAX=0.52, PX=E=>DX+E/EMAX*DW, PY=v=>DY-v/FMAX*DH;
    function curve(from){ let d=''; for(let i=0;i<=120;i++){ const E=from+(EMAX-from)*i/120; d+=(i?'L':'M')+PX(E).toFixed(1)+' '+PY(f(E,1)).toFixed(1); } return d; }
    function drawD(){
      g3.innerHTML='';
      const c=C[st.c];
      API.mk('path',{d:curve(c.ea)+` L${PX(EMAX)} ${DY} L${PX(c.ea)} ${DY} Z`,fill:c.col===API.COL.ink?API.COL.equi:c.col,opacity:.3},g3);
      API.mk('line',{x1:DX,y1:DY,x2:DX+DW+8,y2:DY,stroke:API.COL.muted,'stroke-width':2},g3);
      API.mk('line',{x1:DX,y1:DY,x2:DX,y2:DY-DH-4,stroke:API.COL.muted,'stroke-width':2},g3);
      API.mk('path',{d:curve(0),fill:'none',stroke:API.COL.ink,'stroke-width':3},g3);
      API.mk('line',{x1:PX(3.6),y1:DY,x2:PX(3.6),y2:DY-150,stroke:API.COL.equi,'stroke-width':2.5,'stroke-dasharray':'6 5'},g3);
      if(st.c!=='none') API.mk('line',{x1:PX(c.ea),y1:DY,x2:PX(c.ea),y2:DY-170,stroke:c.col,'stroke-width':2.5,'stroke-dasharray':'6 5'},g3);
      const d1=Ov('d1'); d1.style.color=st.c==='none'?'#B8661A':c.col; API.place(d1,PX(c.ea)+4,DY-176);
      API.place(Ov('dy'),DX+6,0); API.place(Ov('dx'),DX+DW-104,DY+6);
    }
    const fr={}; for(const k in C) fr[k]=frac(C[k].ea);
    function renderLog(){
      O('log').innerHTML=log.map((r,i)=>`<tr${i===log.length-1?' class="hl"':''}><td>${C[r.c].name}</td><td>${C[r.c].eaTxt}</td><td>${r.V>=100?'100 (넘침)':r.V.toFixed(0)}</td><td>${C[r.c].rate}</td></tr>`).join('')||'<tr><td colspan="4">아직 관찰 기록이 없다</td></tr>';
    }
    function labels(){
      const c=C[st.c];
      Ov('e1').innerHTML=API.tex('E_\\mathrm{a}');
      Ov('e2').innerHTML=API.tex(st.c==='ki'?"E_\\mathrm{a}'":"E_\\mathrm{a}''");
      Ov('d1').innerHTML=API.tex(st.c==='none'?'E_\\mathrm{a}':(st.c==='ki'?"E_\\mathrm{a}'":"E_\\mathrm{a}''"));
      Ov('ey').innerHTML='엔탈피'; Ov('ex').innerHTML='반응의 진행'; Ov('dy').innerHTML='분자 수'; Ov('dx').innerHTML='운동 에너지';
    }
    function draw(){
      root.querySelectorAll('[data-c]').forEach(b=>b.classList.toggle('on',b.dataset.c===st.c));
      const c=C[st.c], R=st.run;
      O('ea').textContent=c.eaTxt; O('fr').textContent=(fr[st.c]*100).toFixed(1)+' %';
      const V=drawCyl();
      O('v').textContent=R? (V>=100?'100 mL (넘침)':V.toFixed(0)+' mL')+(R.done?'':` · ${R.t.toFixed(0)} s`) : '10 mL (처음)';
      O('m').textContent=c.m;
      labels(); drawE(); drawD();
    }
    function finish(){
      const R=st.run; R.done=true; const V=Vof(R.c,30);
      log.push({c:R.c,V}); if(log.length>5) log.shift(); renderLog();
      const msg={none:'거의 변화가 없다 — 실온에서 과산화 수소는 아주 천천히 분해된다.',
        ki:'거품이 순식간에 솟아오른다! KI는 활성화 에너지를 낮추어 분해를 빠르게 하고, 반응 뒤에도 그대로 남는다 → 정촉매.',
        h3po4:'넣지 않을 때보다도 기포가 적다. 활성화 에너지가 커져 반응할 수 있는 분자가 줄었다 → 부촉매.'}[R.c];
      const all=new Set(log.map(r=>r.c)).size;
      O('msg').textContent=msg+(all>=2?'\n온도가 같아 분포 곡선은 그대로이고, 경계(활성화 에너지)만 바뀌었다.':'');
    }
    root.querySelectorAll('[data-c]').forEach(b=>b.addEventListener('click',()=>{ if(st.run&&!st.run.done) return; st.c=b.dataset.c; st.run=null; O('msg').textContent='「넣고 30 s 관찰」을 눌러 보자.'; draw(); }));
    root.querySelector('[data-act="run"]').addEventListener('click',()=>{ if(st.run&&!st.run.done) return; st.run={c:st.c,t:0,done:false}; O('msg').textContent='관찰 중… (3배 빠르게)'; draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ st={c:'none',run:null}; log=[]; renderLog(); O('msg').textContent='넣을 물질을 고르고 「넣고 30 s 관찰」을 눌러 보자.'; draw(); });
    API.loop(root,dt=>{ const R=st.run; if(!R||R.done) return; R.t=Math.min(30,R.t+dt*3); if(R.t>=30) finish(); draw(); });
    renderLog(); O('msg').textContent='넣을 물질을 고르고 「넣고 30 s 관찰」을 눌러 보자.'; draw();
    API.ready(()=>draw());
  }
};
