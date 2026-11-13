/* 3-2 탄소 화합물의 화학 반응 — 실험실 (필수 탐구 반03-탐2 「음주 측정기 만들기, 은거울 반응 등 실험을 통해 작용기의 변화 탐구하기」)
   rm32ag  : 은거울 반응 — 시료(포도당·아세트알데하이드·에탄올·아세트산·증류수) × 물 중탕 온도 × KOH 유무
             ① 암모니아수(갈색 앙금 → 녹음) → ② 시료·KOH → ③ 중탕하며 흔들기 → 은 석출 정도–시간 곡선, 기록 표
             모의 값: 석출 정도 p = 1 − e^(−t/τ), τ(60 °C, KOH) 포도당 60 s, 아세트알데하이드 40 s, τ × 2^((60−T)/10), KOH 없으면 × 3. −CHO 없는 시료는 p = 0
   rm32bre : 음주 측정기 — 시료(에탄올·아세트알데하이드·아세트산·물) × 솜에 적신 양(1–8 방울)
             관 밀폐 → 초록 앞면 L(t) = L∞(1 − e^(−t/40)), L∞ = 11 mm × 방울(에탄올), 5.5 mm × 방울(아세트알데하이드), 0(아세트산·물), 상한 100 mm
             기록 → 표 + 초록 길이–방울 수 그래프 (모의 값 — plan.md 2절) */
(function(){
const INK='#16233D', MUT='#5B6B7F', EQ='#E08A2C', OX='#C2410C', RD='#0E7490', ORG='#F2B32A', GRN='#3E9A6A';
const SER={eth:{c:'#2E9E6A',m:'s',t:'에탄올'}, ald:{c:'#7B4FC8',m:'t',t:'아세트알데하이드'}, glu:{c:'#E08A2C',m:'c',t:'포도당'}, ace:{c:'#D7263D',m:'d',t:'아세트산'}, wat:{c:'#8C99A6',m:'o',t:'증류수'}};
function marker(API,g,x,y,s,r){ r=r||6; const c=SER[s].c, m=SER[s].m;
  if(m==='c') return API.mk('circle',{cx:x,cy:y,r,fill:c},g);
  if(m==='o') return API.mk('circle',{cx:x,cy:y,r,fill:'#fff',stroke:c,'stroke-width':2.5},g);
  if(m==='s') return API.mk('rect',{x:x-r,y:y-r,width:2*r,height:2*r,fill:c},g);
  if(m==='t') return API.mk('polygon',{points:`${x},${y-r-1} ${x+r+1},${y+r} ${x-r-1},${y+r}`,fill:c},g);
  return API.mk('polygon',{points:`${x},${y-r-2} ${x+r+2},${y} ${x},${y+r+2} ${x-r-2},${y}`,fill:c},g); }
const clear=g=>{ while(g.firstChild) g.removeChild(g.firstChild); };

window.DECK_LABS = {
  rm32ag(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg');
    const gA=API.mk('g',{},svg), gV=API.mk('g',{},svg), gC=API.mk('g',{},svg);
    const NAME={glu:'포도당',ald:'아세트알데하이드',eth:'에탄올',ace:'아세트산',wat:'증류수'};
    const FG={glu:'\\ce{-CHO}, \\ce{-OH}',ald:'\\ce{-CHO}',eth:'\\ce{-OH}',ace:'\\ce{-COOH}',wat:'—'};
    const BASE={glu:60, ald:40};
    let st, runs=[];
    const fresh=()=>({drops:0, added:false, heat:false, t:0, done:false});
    st=fresh(); let s='glu', koh=true;
    const T=()=>+I('T').value;
    const tau=()=>BASE[s]? BASE[s]*Math.pow(2,(60-T())/10)*(koh?1:3) : Infinity;
    const pOf=(t,ta)=>isFinite(ta)? 1-Math.exp(-t/ta) : 0;
    let seed=11; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };

    // ── 그래프 축 ──
    const GX=345, GY=40, GW=270, GH=210, TM=300;
    const gx=t=>GX+t/TM*GW, gy=p=>GY+(1-p)*GH;
    [0,.5,1].forEach(p=>{ API.mk('line',{x1:GX,y1:gy(p),x2:GX+GW,y2:gy(p),stroke:'#E2E7EC','stroke-width':1.5},gA); API.texText(gA,GX-8,gy(p)+6,'$'+(p*100)+'$',{size:18,anchor:'end',fill:MUT,mix:true}); });
    [0,100,200,300].forEach(t=>API.texText(gA,gx(t),GY+GH+24,'$'+t+'$',{size:18,anchor:'middle',fill:MUT,mix:true}));
    API.mk('line',{x1:GX,y1:GY-6,x2:GX,y2:GY+GH,stroke:MUT,'stroke-width':2},gA);
    API.mk('line',{x1:GX,y1:GY+GH,x2:GX+GW,y2:GY+GH,stroke:MUT,'stroke-width':2},gA);
    API.mk('line',{x1:GX,y1:gy(.5),x2:GX+GW,y2:gy(.5),stroke:EQ,'stroke-width':1.6,'stroke-dasharray':'6 5'},gA);
    API.texText(gA,GX+4,GY-14,'은 석출 정도 [%]',{size:18,anchor:'start',fill:MUT,mix:true});
    API.texText(gA,GX+GW,GY+GH+50,'시간 [s]',{size:18,anchor:'end',fill:MUT,mix:true});
    // ── 유리병·중탕 그림 ──
    const VX=110, VY=110, VW=90, VH=150;
    function drawVial(){
      clear(gV);
      const p=pOf(st.t,tau());
      if(st.heat){ API.mk('path',{d:`M30 80 V${VY+VH+30} q0 10 10 10 H${VX+VW+70} q10 0 10 -10 V80`,fill:'#FDE2E4','fill-opacity':.8,stroke:'#7E8B98','stroke-width':3},gV);
        API.mk('rect',{x:33,y:118,width:VX+VW+74-33,height:VH+48-36,fill:'#F9C9CF','fill-opacity':.6},gV); }
      const lh = st.added? 110 : (st.drops? 70 : 60);
      const top=VY+VH-lh;
      const tint = p>0? `rgb(${Math.round(238-130*p)},${Math.round(243-130*p)},${Math.round(248-128*p)})` : '#EEF3F8';
      API.mk('rect',{x:VX+3,y:top,width:VW-6,height:lh-3,rx:6,fill:tint},gV);
      const ppt = st.added? 0 : (st.drops===0?0: st.drops<=2?1: st.drops<=4?.5:0);
      if(ppt>0) API.mk('ellipse',{cx:VX+VW/2,cy:VY+VH-14,rx:30*ppt+8,ry:8,fill:'#7A4E2D','fill-opacity':.65},gV);
      if(p>0.01){ const op=Math.min(1,p*1.05);
        [[VX+3,top-2,8,lh+1],[VX+VW-11,top-2,8,lh+1],[VX+3,VY+VH-10,VW-6,8]].forEach(([x,y,w,h])=>API.mk('rect',{x,y,width:w,height:h,rx:3,fill:'#AEB4BD','fill-opacity':op,stroke:'#8A919C','stroke-width':1,'stroke-opacity':op},gV)); }
      API.mk('path',{d:`M${VX} ${VY} V${VY+VH-8} q0 8 8 8 h${VW-16} q8 0 8 -8 V${VY}`,fill:'none',stroke:'#7E8B98','stroke-width':3},gV);
      if(st.added) API.mk('rect',{x:VX-4,y:VY-20,width:VW+8,height:22,rx:4,fill:INK},gV);
      // 온도 글자
      const v=Ov('vial');
      let tx = !st.drops? '질산 은 수용액 5 mL' : !st.added? (ppt>0?'갈색 앙금 생김':'앙금이 모두 녹음 (투명)') : !st.heat? '시료 2 mL + '+(koh?'KOH 2 mL':'KOH 없음') : (p>=.5?'은거울 생김':p>.05?'벽이 검게 흐려짐':'변화 거의 없음');
      v.textContent=tx+(st.heat?' · '+T()+' °C':''); API.place(v,VX+VW/2,VY+VH+44);
      // 곡선
      clear(gC);
      runs.forEach(r=>{ const pts=[]; for(let t=0;t<=TM;t+=10) pts.push(gx(t)+','+gy(pOf(t,r.tau)));
        API.mk('polyline',{points:pts.join(' '),fill:'none',stroke:SER[r.s].c,'stroke-width':2.5},gC);
        marker(API,gC,gx(TM),gy(pOf(TM,r.tau)),r.s,5); });
      if(st.heat){ const pts=[]; for(let t=0;t<=st.t;t+=5) pts.push(gx(t)+','+gy(pOf(t,tau()))); pts.push(gx(st.t)+','+gy(p));
        API.mk('polyline',{points:pts.join(' '),fill:'none',stroke:INK,'stroke-width':3,'stroke-dasharray':'7 4'},gC);
        API.mk('circle',{cx:gx(st.t),cy:gy(p),r:5,fill:INK},gC); }
      const e=Ov('eq');
      if(st.heat && p>.05){ e.innerHTML=`<span style="color:${OX}">산화 ${API.tex('\\ce{-CHO -> -COOH}')}</span><br><span style="color:${RD}">환원 ${API.tex('\\ce{Ag+ -> Ag}')}</span>`; API.place(e,175,6); }
      else API.place(e,0,0,false);
    }
    function update(){
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===s));
      O('T').textContent=T()+' °C';
      const k=$('[data-act="koh"]'); k.classList.toggle('on',koh); k.textContent=koh?'KOH 넣음':'KOH 안 넣음'; k.disabled=st.added;
      $('[data-act="nh3"]').disabled=st.added; $('[data-act="add"]').disabled=st.added||st.drops<1; $('[data-act="heat"]').disabled=!st.added||st.heat;
      ['nh3','add','heat'].forEach((a,i)=>$(`[data-act="${a}"]`).classList.toggle('done',[st.drops>=5,st.added,st.heat][i]));
      const p=pOf(st.t,tau());
      O('t').textContent=st.heat? Math.round(st.t)+' s' : '—';
      O('p').textContent=st.heat? Math.round(p*100)+' %' : '—';
      let m='';
      if(!st.drops) m='① 질산 은 수용액에 진한 암모니아수를 한 방울씩 넣자.';
      else if(!st.added) m= st.drops<5? '갈색 앙금(산화 은)이 생겼다. 앙금이 모두 녹을 때까지 암모니아수를 더 넣자.' : '앙금이 모두 녹았다. ② 시료와 수산화 칼륨 수용액을 넣고 뚜껑을 닫자.';
      else if(!st.heat) m='③ 뜨거운 물에 넣고 흔들자. 온도를 바꿔 볼 수도 있다.';
      else if(BASE[s]){ m= p>=.5? NAME[s]+'의 포밀기(−CHO)가 산화되어 카복실기(−COOH)가 되고, 은 이온(Ag⁺)은 환원되어 벽에 은거울을 만든다.' : '벽이 점점 검게 흐려진다. 은이 석출되는 중이다.';
        if(st.done) m+= T()<50? ' 온도가 낮아 느리다.' : '';
        if(!koh) m+=' KOH가 없어 OH⁻이 부족해 느리다.'; }
      else m= st.done? NAME[s]+'에는 포밀기(−CHO)가 없어 은 이온을 환원시키지 못한다. 은거울이 생기지 않는다.' : '흔들며 관찰하는 중…';
      if(st.heat && !st.done && BASE[s]===undefined) m='흔들며 관찰하는 중… 벽에 변화가 있는지 보자.';
      O('msg').textContent=m;
      drawVial();
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      runs.slice(-4).forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${NAME[r.s]}</td><td>${r.s==='wat'?'—':API.tex(FG[r.s])}</td><td>${r.T} °C</td><td>${r.koh?'O':'X'}</td><td>${r.res}</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ s=b.dataset.s; st=fresh(); update(); }));
    I('T').addEventListener('input',()=>{ if(st.heat){ st.t=0; st.done=false; } update(); });
    $('[data-act="koh"]').addEventListener('click',()=>{ if(st.added) return; koh=!koh; update(); });
    $('[data-act="nh3"]').addEventListener('click',()=>{ if(st.added) return; st.drops=Math.min(8,st.drops+1); update(); });
    $('[data-act="add"]').addEventListener('click',()=>{ if(st.drops<5){ O('msg').textContent='갈색 앙금이 남아 있다. 암모니아수를 더 넣어 앙금을 모두 녹인 뒤 넣자.'; return; } st.added=true; update(); });
    $('[data-act="heat"]').addEventListener('click',()=>{ if(!st.added) return; st.heat=true; st.t=0; st.done=false; update(); });
    $('[data-act="rec"]').addEventListener('click',()=>{
      if(!st.heat){ O('msg').textContent='③ 중탕하며 흔들기까지 한 뒤 기록하자.'; return; }
      const ta=tau(), p=pOf(st.t,ta);
      if(!st.done && p<.5){ O('msg').textContent='아직 관찰 중이다. 은거울이 생기거나 300 s가 지난 뒤 기록하자.'; return; }
      let res;
      if(isFinite(ta) && ta*Math.LN2<=TM){ const t50=ta*Math.LN2*(1+(rnd()-.5)*.06); res=Math.round(t50)+' s'; }
      else res=isFinite(ta)?'300 s 안에 안 생김':'안 생김';
      runs.push({s,T:T(),koh,tau:ta,res}); if(runs.length>5) runs.shift(); renderLog(); update(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ runs=[]; s='glu'; koh=true; I('T').value=60; st=fresh(); renderLog(); update(); });
    root._step=(sec)=>{ if(st.heat&&!st.done){ st.t=Math.min(TM,st.t+sec); if(st.t>=TM) st.done=true; update(); } };
    if(!window.__STILL) API.loop(root,dt=>{ if(st.heat&&!st.done){ st.t=Math.min(TM,st.t+dt*30); if(st.t>=TM) st.done=true; if(pOf(st.t,tau())>=.5 && BASE[s]) st.done = st.done || false; update(); } });
    API.ready(()=>update());
    update();
  },

  rm32bre(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg');
    const gA=API.mk('g',{},svg), gT=API.mk('g',{},svg), gP=API.mk('g',{},svg);
    const NAME={eth:'에탄올',ald:'아세트알데하이드',ace:'아세트산',wat:'물'};
    const K={eth:11, ald:5.5, ace:0, wat:0};
    const CHG={eth:'\\ce{-OH -> -CHO}', ald:'\\ce{-CHO -> -COOH}', ace:'', wat:''};
    let s='eth', st={run:false,t:0,done:false}, log=[], pts=[];
    const TM=180;
    const n=()=>+I('n').value;
    const noise=(ss,nn)=>{ const h=(ss.charCodeAt(0)*31+nn*17)%31; return (h-15)/10; };
    const Linf=()=>Math.min(100, K[s]*n());
    const Lnow=()=>{ const L=Linf()*(1-Math.exp(-st.t/40)); return L>0? Math.max(0,Math.min(100, L+(st.done?noise(s,n()):0))) : 0; };
    // 관 (실리카 젤 0–100 mm)
    const X0=100, X1=480, PX=(X1-X0)/100, TY=66;
    API.mk('rect',{x:X0-26,y:TY-34,width:X1-X0+130,height:68,rx:16,fill:'#F7F9FB',stroke:'#7E8B98','stroke-width':3},gA);
    API.mk('rect',{x:X0-56,y:TY-30,width:36,height:60,rx:8,fill:INK},gA);
    API.mk('rect',{x:X1+98,y:TY-30,width:36,height:60,rx:8,fill:INK},gA);
    for(let mm=0;mm<=100;mm+=20){ const x=X1-mm*PX; API.mk('line',{x1:x,y1:TY+36,x2:x,y2:TY+46,stroke:MUT,'stroke-width':2},gA); API.texText(gA,x,TY+68,'$'+mm+'$',{size:18,anchor:'middle',fill:MUT,mix:true}); }
    API.texText(gA,X0-30,TY+68,'[mm]',{size:18,anchor:'end',fill:MUT,mix:true});
    API.texText(gA,X1+50,TY+68,'솜',{size:18,anchor:'middle',fill:MUT,mix:true});
    // 그래프
    const GX=90, GY=200, GW=500, GH=210;
    const gx=k=>GX+(k-0.5)/8*GW, gy=L=>GY+(1-L/100)*GH;
    [0,50,100].forEach(L=>{ API.mk('line',{x1:GX,y1:gy(L),x2:GX+GW,y2:gy(L),stroke:'#E2E7EC','stroke-width':1.5},gA); API.texText(gA,GX-8,gy(L)+6,'$'+L+'$',{size:18,anchor:'end',fill:MUT,mix:true}); });
    for(let k=1;k<=8;k++) API.texText(gA,gx(k),GY+GH+24,'$'+k+'$',{size:18,anchor:'middle',fill:MUT,mix:true});
    API.mk('line',{x1:GX,y1:GY-6,x2:GX,y2:GY+GH,stroke:MUT,'stroke-width':2},gA);
    API.mk('line',{x1:GX,y1:GY+GH,x2:GX+GW,y2:GY+GH,stroke:MUT,'stroke-width':2},gA);
    API.texText(gA,GX+4,GY-14,'초록 길이 [mm]',{size:18,anchor:'start',fill:MUT,mix:true});
    API.texText(gA,GX+GW,GY+GH+52,'솜에 적신 양 [방울]',{size:18,anchor:'end',fill:MUT,mix:true});
    ['eth','ald','ace','wat'].forEach((k,i)=>{ const x=GX+[10,120,320,440][i], y=GY+GH+84; marker(API,gA,x,y-6,k); API.texText(gA,x+12,y,k==='wat'?'물':SER[k].t,{size:18,anchor:'start',fill:MUT,mix:true}); });
    let bub=[]; let seed=5; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    function drawTube(){
      clear(gT);
      API.mk('rect',{x:X0,y:TY-26,width:X1-X0,height:52,rx:8,fill:ORG},gT);
      const L=Lnow();
      if(L>0) API.mk('rect',{x:X1-L*PX,y:TY-26,width:L*PX,height:52,rx:8,fill:GRN},gT);
      for(let k=0;k<11;k++) API.mk('circle',{cx:X0+20+42*k,cy:TY-8+16*(k%2),r:4,fill:'#fff','fill-opacity':.45},gT);
      API.mk('path',{d:`M${X1+18} ${TY} q10 -24 30 -14 q18 -16 36 0 q20 -4 22 16 q4 20 -14 24 q-14 14 -34 6 q-24 10 -36 -8 q-12 -6 -4 -24z`,fill:'#FFFFFF',stroke:'#9AA5B1','stroke-width':2},gT);
      if(st.run) bub.forEach(b=>API.mk('circle',{cx:b.x,cy:b.y,r:3,fill:K[s]>0?'#9FB0C2':'#C9D3DD','fill-opacity':.8},gT));
    }
    function drawPts(){ clear(gP); pts.forEach(q=>marker(API,gP,gx(q.n)+(q.s==='ald'?6:q.s==='ace'?-6:0),gy(q.L),q.s)); }
    function update(){
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===s));
      O('n').textContent=n()+' 방울';
      const g=$('[data-act="go"]'); g.disabled=st.run&&!st.done; g.classList.toggle('done',st.run);
      O('t').textContent=st.run? Math.round(st.t)+' s' : '—';
      const L=Lnow(); O('L').textContent=st.run? L.toFixed(1)+' mm' : '—';
      let m;
      if(!st.run) m='솜에 시료를 적시고 관을 밀폐해 실리카 젤을 관찰하자.';
      else if(!st.done) m='기체가 관 안으로 퍼지며 반응하는 중…';
      else if(s==='eth') m='에탄올이 산화되어 아세트알데하이드가 되고(−OH → −CHO), 노란색 다이크로뮴산 이온이 환원되어 초록색 크로뮴 이온이 된다. 양이 많을수록 초록 부분이 길다.';
      else if(s==='ald') m='아세트알데하이드가 산화되어 아세트산이 된다(−CHO → −COOH). 산화 한 단계만 남아 에탄올보다 초록 부분이 짧다.';
      else if(s==='ace') m='아세트산의 −COOH는 더 산화되기 어렵다. 다이크로뮴산 이온이 환원되지 않아 노란색 그대로다.';
      else m='물에는 산화될 탄소 화합물이 없다. 색이 변하지 않는다(대조 실험).';
      O('msg').textContent=m;
      drawTube();
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${NAME[r.s]}</td><td>${r.n}</td><td>${r.L}</td><td>${r.c?API.tex(r.c):'변화 없음'}</td>`; tb.appendChild(tr); }); }
    const stop=()=>{ st={run:false,t:0,done:false}; bub=[]; };
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ s=b.dataset.s; stop(); update(); }));
    I('n').addEventListener('input',()=>{ stop(); update(); });
    $('[data-act="go"]').addEventListener('click',()=>{ st={run:true,t:0,done:false}; bub=[]; update(); });
    $('[data-act="rec"]').addEventListener('click',()=>{
      if(!st.done){ O('msg').textContent='관을 밀폐하고 관찰이 끝난 뒤(180 s) 기록하자.'; return; }
      const L=+Lnow().toFixed(1);
      log.push({s,n:n(),L:L.toFixed(1),c:CHG[s]}); if(log.length>4) log.shift();
      pts=pts.filter(q=>!(q.s===s&&q.n===n())); pts.push({s,n:n(),L}); renderLog(); drawPts(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; pts=[]; s='eth'; I('n').value=4; stop(); renderLog(); drawPts(); update(); });
    root._step=(sec)=>{ if(st.run&&!st.done){ st.t=Math.min(TM,st.t+sec); if(st.t>=TM) st.done=true; update(); } };
    if(!window.__STILL) API.loop(root,dt=>{ if(!(st.run&&!st.done)) return;
      st.t=Math.min(TM,st.t+dt*36); if(st.t>=TM){ st.done=true; bub=[]; }
      if(rnd()<dt*10) bub.push({x:X1+10, y:TY-14+rnd()*28});
      bub.forEach(b=>{ b.x-=dt*120; }); bub=bub.filter(b=>b.x>X1-Math.max(30,Lnow()*PX));
      update(); });
    API.ready(()=>update());
    update();
  }
};
})();
