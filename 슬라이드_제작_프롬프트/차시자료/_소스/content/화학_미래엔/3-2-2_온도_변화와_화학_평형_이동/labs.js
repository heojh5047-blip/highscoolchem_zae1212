/* 3-2-2 온도 변화와 화학 평형 이동 — 실험실
   cm322temp : 「온도 변화 실험실」 (화03-탐2 온도 부분)
   [코발트] [Co(H2O)6]2+ + 4Cl- ⇌ [CoCl4]2- + 6H2O, 정반응 흡열(덱 모의값 ΔH = +50 kJ).
            Co 0.1 M, 처음 Cl- 0.2 M(CoCl2), 염화 칼슘 한 숟가락 = Cl- +0.95 M(최대 5번).
            K25 = 1/3.8^4 (4숟가락에서 25 °C 파란 비율 50 %), K(T) = K25·exp(−6014(1/T − 1/298)).
            평형 x − K(0.1 − x)(Cl − 4x)^4 = 0 → 이분법. 직후 Q = 옛 x로 계산.
   [NO2]    2NO2 ⇌ N2O4, 정반응 발열 — 3-2-1 cm321 온도 모드와 같은 식: K(T) = 212·exp(6856(1/T − 1/298)) (ΔH = −57 kJ),
            밀봉 유리관(부피 일정) c = [NO2] + 2[N2O4] = 0.20 M, 2Kx² + x − c = 0.
   조작마다 기록 표에 행 추가(최대 4), 새 평형의 K를 그래프(K/K25, 로그)에 점으로, 2초 동안 평형으로(API.loop). */
(function(){
function tempLab(root, API){
  const $=s=>root.querySelector(s), $$=s=>root.querySelectorAll(s), O=k=>$(`[data-o="${k}"]`);
  const svg=$('svg'), mk=API.mk;
  const RED=[217,96,138], BLUE=[59,111,209], NO2C='#B5562A', EQ='#E08A2C', MU='#5B6B7F', INK='#16233D', GL='#7E8B98';
  const CO=0.1, CL0=0.2, DCL=0.95, MAXN=5, K25C=1/Math.pow(3.8,4), K25N=212, CN=0.2, MAXR=4, NMOL=30;
  const mix=f=>`rgb(${RED.map((v,i)=>Math.round(v+(BLUE[i]-v)*f)).join(',')})`;
  const relC=t=>Math.exp(-6014*(1/(t+273)-1/298)), relN=t=>Math.exp(6856*(1/(t+273)-1/298));
  const KC=t=>K25C*relC(t), KN=t=>K25N*relN(t);
  // ---------- 고정 그림 ----------
  const BXL=20, BW=230, BTOP=110, BH=180, WTOP=BTOP+BH*0.22, CX=135;
  const bathG=mk('g',{},svg);
  const water=mk('path',{d:`M${BXL+4} ${WTOP} H${BXL+BW-4} V${BTOP+BH-8} Q${BXL+BW-4} ${BTOP+BH-3} ${BXL+BW-9} ${BTOP+BH-3} H${BXL+9} Q${BXL+4} ${BTOP+BH-3} ${BXL+4} ${BTOP+BH-8} Z`,fill:'#DDEEF8'},bathG);
  const deco=mk('g',{},bathG);
  // 시험관(코발트)
  const coG=mk('g',{},svg), TW=60, tr=TW/2, TT=30, TB=272;
  const liq=mk('path',{d:`M${CX-tr+3} 120 V${TB-tr} A${tr-3} ${tr-3} 0 0 0 ${CX+tr-3} ${TB-tr} V120 Z`,fill:mix(0)},coG);
  mk('path',{d:`M${CX-tr} ${TT} V${TB-tr} A${tr} ${tr} 0 0 0 ${CX+tr} ${TB-tr} V${TT}`,fill:'none',stroke:GL,'stroke-width':3.5},coG);
  mk('path',{d:`M${CX-tr-6} ${TT} H${CX+tr+6}`,stroke:GL,'stroke-width':3.5,'stroke-linecap':'round'},coG);
  // 밀봉 유리관(NO2)
  const nG=mk('g',{},svg), AX0=CX-55, AW=110, AT=36, AB=272;
  const gas=mk('rect',{x:AX0,y:AT,width:AW,height:AB-AT,rx:22,fill:NO2C,'fill-opacity':0.3},nG);
  const molG=mk('g',{},nG);
  mk('rect',{x:AX0,y:AT,width:AW,height:AB-AT,rx:22,fill:'none',stroke:GL,'stroke-width':3.5},nG);
  mk('path',{d:`M${CX-8} ${AT} V${AT-14}`,stroke:GL,'stroke-width':6,'stroke-linecap':'round'},nG);
  // 물중탕 테
  mk('path',{d:`M${BXL-6} ${BTOP-4} Q${BXL} ${BTOP} ${BXL} ${BTOP+8} V${BTOP+BH-8} Q${BXL} ${BTOP+BH} ${BXL+8} ${BTOP+BH} H${BXL+BW-8} Q${BXL+BW} ${BTOP+BH} ${BXL+BW} ${BTOP+BH-8} V${BTOP}`,fill:'none',stroke:GL,'stroke-width':3.5,'stroke-linejoin':'round'},svg);
  const info=mk('text',{x:14,y:22,'font-size':19,fill:INK,'font-weight':700},svg);
  // 수직선
  const NL={x0:300,x1:670,xc:485,y:48,per:61};
  const XL=l=>NL.xc+API.clamp(l,-3,3)*NL.per;
  const bgN=mk('g',{},svg);
  API.texText(bgN,NL.x0-6,20,'반응 지수 $Q$ (로그 눈금)',{size:18,anchor:'start',fill:INK,mix:true});
  API.arrow(bgN,NL.x0-8,NL.y,NL.x1+14,NL.y,'ink',2);
  [-3,-2,-1,0,1,2,3].forEach(l=>{ const x=XL(l); mk('path',{d:`M${x} ${NL.y-(l%3?5:8)} V${NL.y+(l%3?5:8)}`,stroke:INK,'stroke-width':2},bgN); });
  API.texText(bgN,XL(-3),NL.y+28,'$10^{-3}K$',{size:18,anchor:'middle',fill:INK,mix:true});
  API.texText(bgN,XL(3),NL.y+28,'$10^{3}K$',{size:18,anchor:'middle',fill:INK,mix:true});
  mk('path',{d:`M${NL.xc} ${NL.y-26} V${NL.y+10}`,stroke:INK,'stroke-width':3,'stroke-dasharray':'7 5'},bgN);
  API.texText(bgN,NL.xc+10,NL.y-12,'$K$',{size:21,anchor:'start',fill:INK,mix:true});
  API.texText(bgN,NL.x0,NL.y+60,'$Q<K$ 정반응 우세',{size:18,anchor:'start',fill:'#2E9E6A',mix:true});
  API.texText(bgN,NL.x1+10,NL.y+60,'역반응 우세 $Q>K$',{size:18,anchor:'end',fill:'#7B4FC8',mix:true});
  // 그래프 K/K25 – 온도
  const GX=t=>350+t/90*310, GY=l=>204-API.clamp(l,-2.2,2.2)*30;
  const bgG=mk('g',{},svg);
  mk('rect',{x:350,y:GY(2.2),width:310,height:GY(-2.2)-GY(2.2),fill:'#FBFCFD'},bgG);
  mk('path',{d:`M350 ${GY(0)} H660`,stroke:MU,'stroke-width':1.5,'stroke-dasharray':'5 5'},bgG);
  API.arrow(bgG,350,GY(-2.2),674,GY(-2.2),'ink',2); API.arrow(bgG,350,GY(-2.2),350,GY(2.2)-10,'ink',2);
  [[2,'$10^{2}$'],[0,'$1$'],[-2,'$10^{-2}$']].forEach(([l,s])=>{ mk('path',{d:`M344 ${GY(l)} H350`,stroke:INK,'stroke-width':2},bgG); API.texText(bgG,340,GY(l)+6,s,{size:18,anchor:'end',fill:INK,mix:true}); });
  [0,30,60,90].forEach(t=>{ mk('path',{d:`M${GX(t)} ${GY(-2.2)} V${GY(-2.2)+6}`,stroke:INK,'stroke-width':2},bgG); API.texText(bgG,GX(t),GY(-2.2)+22,t===90?'90 °C':String(t),{size:18,anchor:'middle',fill:INK,mix:true}); });
  API.texText(bgG,362,GY(2.2)+20,'새 평형의 $K$ (25 °C 값 = 1)',{size:18,anchor:'start',fill:MU,mix:true});
  const ptsG=mk('g',{},svg);
  // Q 점
  const qg=mk('g',{},svg);
  mk('circle',{cx:0,cy:NL.y,r:9,fill:EQ,stroke:'#fff','stroke-width':2},qg);
  API.texText(qg,0,NL.y-16,'$Q$',{size:19,anchor:'middle',fill:'#B45F06',mix:true});
  const dyn=mk('g',{},svg);
  // ---------- 상태 ----------
  let mode='co', rows=[], nexp=0, anim=null;
  const S={co:{T:25,n:0,x:0}, no2:{T:25,a:0,y:0}};
  const pts={co:[],no2:[]};
  let seed=11; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
  const slots=[]; for(let i=0;i<NMOL;i++) slots.push({u:rnd(),v:rnd(),a:Math.floor(rnd()*6)*30,w:1+rnd()*2,p:rnd()*6.28});
  let molKey='', molEls=[];
  function molecule(g,kind){ const r=6, d=1.35*r;
    if(kind==='a'){ [-67,67].forEach(b=>{ const q=(b-90)*Math.PI/180; API.atom(g,d*Math.cos(q),d*Math.sin(q),r,'O','-',false); }); API.atom(g,0,0,r,'N','-',false); }
    else { const dn=1.45*r; [-1,1].forEach(sd=>{ const nx=sd*dn/2, base=sd>0?0:180; [-62,62].forEach(b=>{ const q=(base+b)*Math.PI/180; API.atom(g,nx+d*Math.cos(q),d*Math.sin(q),r,'O','-',false); }); });
      [-1,1].forEach(sd=>API.atom(g,sd*dn/2,0,r,'N','-',false)); } }
  function buildMols(n){ const m=(NMOL-n)/2, key=n+'/'+m; if(key===molKey) return; molKey=key; molG.innerHTML=''; molEls=[];
    for(let i=0;i<n+m;i++){ const g=mk('g',{},molG); molecule(g,i<n?'a':'b'); molEls.push(g); } }
  function placeMols(t){ molEls.forEach((g,i)=>{ const s=slots[i], jx=Math.sin(t*s.w+s.p)*2.5, jy=Math.cos(t*s.w*1.3+s.p)*2.5;
      const x=AX0+18+s.u*(AW-36)+jx, y=AT+18+s.v*(AB-AT-36)+jy; g.setAttribute('transform',`translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${s.a})`); }); }
  // ---------- 화학 계산 ----------
  const clt=()=>CL0+DCL*S.co.n;
  function eqCo(K,Cl){ let lo=0, hi=Math.min(CO,Cl/4);
    for(let k=0;k<90;k++){ const x=(lo+hi)/2; if(x-K*(CO-x)*Math.pow(Cl-4*x,4)>0) hi=x; else lo=x; } return (lo+hi)/2; }
  const Qco=(x,Cl)=>x/Math.max(1e-30,(CO-x)*Math.pow(Math.max(1e-9,Cl-4*x),4));
  const eqGas=(c,K)=>{ const x=(-1+Math.sqrt(1+8*K*c))/(4*K); return [x,(c-x)/2]; };
  const coName=f=>f<0.2?'붉은색':f<0.4?'붉은 보라색':f<0.6?'보라색':f<0.8?'푸른 보라색':'파란색';
  const nName=a=>a<0.012?'아주 옅은 적갈색':a<0.04?'옅은 적갈색':a<0.07?'적갈색':'진한 적갈색';
  const fK=K=>K>=100?K.toFixed(0):K>=10?K.toFixed(1):K.toFixed(1);
  // ---------- 그리기 ----------
  function drawBath(T){ const cold=T<20, hot=T>40; deco.innerHTML='';
    water.setAttribute('fill', cold?'#E3EEFB':hot?'#FDE2E4':'#DDEEF8');
    if(cold) [[40,WTOP+10,12],[192,WTOP+16,-15],[46,WTOP+80,28],[196,WTOP+92,-8]].forEach(([x,y,a])=>mk('rect',{x:x-12,y:y-12,width:24,height:24,rx:5,fill:'#fff',stroke:'#9FC3DD','stroke-width':2,transform:`rotate(${a} ${x} ${y})`},deco));
    if(hot) [55,215].forEach(sx=>mk('path',{d:`M${sx} ${BTOP-10} q-8 -10 0 -20 q8 -10 0 -20`,fill:'none',stroke:MU,'stroke-width':2.5,'stroke-linecap':'round',opacity:.7},deco)); }
  function posQ(l,done){ qg.setAttribute('transform',`translate(${XL(l).toFixed(1)},0)`);
    if(!done && Math.abs(l)>0.02){ const xq=XL(l), s=l<0; API.arrow(dyn,xq+(s?12:-12),NL.y+14,NL.xc+(s?-6:6),NL.y+14,s?'field':'bfield',3); }
    O('q').textContent= done||Math.abs(l)<0.02 ? 'Q = K' : (l<0?(l<-3?'Q ≪ K':'Q < K'):(l>3?'Q ≫ K':'Q > K')); }
  function drawPts(){ ptsG.innerHTML=''; const p=pts[mode].slice().sort((u,v)=>u.t-v.t), col=mode==='co'?'#3B6FD1':NO2C;
    if(p.length>1) mk('path',{d:'M'+p.map(q=>`${GX(q.t).toFixed(1)} ${GY(q.l).toFixed(1)}`).join(' L'),fill:'none',stroke:col,'stroke-width':3},ptsG);
    p.forEach(q=>mk('circle',{cx:GX(q.t),cy:GY(q.l),r:6,fill:col,stroke:'#fff','stroke-width':1.5},ptsG)); }
  function draw(done){
    dyn.innerHTML=''; const st=S[mode];
    drawBath(st.T);
    if(mode==='co'){ const Cl=clt(), K=KC(st.T), f=st.x/CO; liq.setAttribute('fill',mix(f));
      posQ(Math.log10(Qco(st.x,Cl)/K),done);
      info.textContent=`${st.T} °C · 파란색 이온 ${Math.round(f*100)} %`; }
    else { const K=KN(st.T), c=st.a+2*st.y; gas.setAttribute('fill-opacity',(0.9*(1-Math.exp(-st.a/0.06))).toFixed(3));
      buildMols(2*Math.round((NMOL/2)*st.a/c)); placeMols(performance.now()/1000);
      posQ(Math.log10((st.y/(st.a*st.a))/K),done);
      info.textContent=`${st.T} °C · K = ${fK(K)}`; }
    drawPts(); }
  // ---------- 기록 ----------
  function log(r){ nexp++; rows.push([nexp,...r]); if(rows.length>MAXR) rows.shift(); const tb=O('log'); tb.innerHTML='';
    rows.forEach(rw=>{ const t=document.createElement('tr'); t.innerHTML=rw.map(v=>`<td>${v}</td>`).join(''); tb.appendChild(t); }); }
  const dirTxt=l=>Math.abs(l)<0.02?'이동 없음':l<0?'정반응':'역반응';
  const cmpTxt=l=>Math.abs(l)<0.02?'Q = K':l<0?'Q < K':'Q > K';
  const matTxt=()=>mode==='co'?'코발트':API.tex('\\ce{NO2}');
  function addPt(){ const st=S[mode], l=Math.log10(mode==='co'?relC(st.T):relN(st.T)); pts[mode]=pts[mode].filter(q=>q.t!==st.T); pts[mode].push({t:st.T,l}); }
  // ---------- 조작 ----------
  function finish(){ if(anim){ if(anim.kind==='co') S.co.x=anim.x1; else { S.no2.a=anim.ae; S.no2.y=(anim.c-anim.ae)/2; } } anim=null; }
  function addCa(){ finish(); const st=S.co;
    if(st.n>=MAXN){ O('msg').textContent='염화 칼슘을 충분히 넣었다. 이제 물중탕의 온도를 바꿔 보자.'; return; }
    const x0=st.x, f0=x0/CO; st.n++; const Cl=clt(), K=KC(st.T), l=Math.log10(Qco(x0,Cl)/K), x1=eqCo(K,Cl), f1=x1/CO;
    anim={kind:'co',t:0,x0,x1};
    O('msg').textContent=`염화 칼슘: 염화 이온의 농도 증가 → ${cmpTxt(l)} → 정반응이 우세하게 진행한다. 파란색 이온이 늘어 ${coName(f1)}이 된다.`+(f1-f0<0.03?' (아직 색 변화가 작다. 더 넣어 보자.)':'');
    log([matTxt(),'염화 칼슘 넣기',cmpTxt(l),dirTxt(l),coName(f1)]);
    draw(false); }
  function setT(t){ finish(); const st=S[mode];
    if(t===st.T){ O('msg').textContent=`이미 ${t} °C이다. 다른 온도를 골라 보자.`; return; }
    const T0=st.T; st.T=t; const up=t>T0; let l, m, col;
    if(mode==='co'){ const Cl=clt(), K=KC(t), x1=eqCo(K,Cl); l=Math.log10(Qco(st.x,Cl)/K); col=coName(x1/CO);
      anim={kind:'co',t:0,x0:st.x,x1};
      m= up ? `${T0} → ${t} °C: 온도를 높임 → K가 커짐 → Q < K → 에너지를 흡수하는 정반응(흡열)이 우세하게 진행한다. 파란색 이온이 늘어 ${col}이 된다.`
            : `${T0} → ${t} °C: 온도를 낮춤 → K가 작아짐 → Q > K → 에너지를 방출하는 역반응(발열)이 우세하게 진행한다. 붉은색 이온이 늘어 ${col}이 된다.`;
      if(Math.abs(x1-st.x)/CO<0.03) m+=' (염화 이온이 적어 색 변화가 작다. 먼저 염화 칼슘을 넣어 보자.)'; }
    else { const K=KN(t), K0=KN(T0), c=st.a+2*st.y, [ae]=eqGas(c,K); l=Math.log10((st.y/(st.a*st.a))/K); col=nName(ae);
      anim={kind:'no2',t:0,a0:st.a,ae,c};
      m= up ? `${T0} → ${t} °C: 온도를 높임 → K가 작아짐(${fK(K0)} → ${fK(K)}) → Q > K → 에너지를 흡수하는 역반응이 우세하게 진행한다. 이산화 질소가 늘어 적갈색이 진해진다.`
            : `${T0} → ${t} °C: 온도를 낮춤 → K가 커짐(${fK(K0)} → ${fK(K)}) → Q < K → 에너지를 방출하는 정반응이 우세하게 진행한다. 사산화 이질소가 늘어 색이 옅어진다.`; }
    O('msg').textContent=m;
    log([matTxt(),`${T0} → ${t} °C`,cmpTxt(l),dirTxt(l),col]);
    addPt(); draw(false); }
  function syncT(){ $$('[data-t]').forEach(b=>b.classList.toggle('cm322-act',+b.dataset.t===S[mode].T)); }
  function setMode(m){ finish(); mode=m;
    $$('[data-mode]').forEach(b=>b.classList.toggle('cm322-act',b.dataset.mode===m));
    $$('[data-pane]').forEach(p=>p.style.display=p.dataset.pane===m?'':'none');
    coG.style.display=m==='co'?'':'none'; nG.style.display=m==='co'?'none':'';
    O('msg').textContent= m==='co' ? '먼저 염화 칼슘을 넣어 보라색을 만들고, 얼음물·뜨거운 물에 담가 보자. 담그기 전에 색을 예측해 보자.' : '밀봉 유리관을 얼음물·뜨거운 물에 담가 보자. 정반응이 발열 반응이면 어느 쪽이 우세할까?';
    syncT(); draw(true); }
  function reset(){ rows=[]; nexp=0; O('log').innerHTML='';
    S.co.T=25; S.co.n=0; S.co.x=eqCo(KC(25),CL0);
    S.no2.T=25; const [a,y]=eqGas(CN,K25N); S.no2.a=a; S.no2.y=y;
    pts.co=[{t:25,l:0}]; pts.no2=[{t:25,l:0}];
    $('[data-i="t"]').value=50; O('tv').textContent='50 °C'; setMode(mode); }
  $$('[data-mode]').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.mode)));
  $$('[data-t]').forEach(b=>b.addEventListener('click',()=>{ setT(+b.dataset.t); syncT(); }));
  $('[data-act="ca"]').addEventListener('click',addCa);
  $('[data-act="dip"]').addEventListener('click',()=>{ setT(+$('[data-i="t"]').value); syncT(); });
  $('[data-act="reset"]').addEventListener('click',()=>{ mode='co'; reset(); });
  $('[data-i="t"]').addEventListener('input',e=>{ O('tv').textContent=e.target.value+' °C'; });
  reset();
  API.loop(root,(dt,t)=>{
    if(anim){ anim.t=Math.min(1,anim.t+dt/2); const e=1-Math.pow(1-anim.t,3), fin=anim.t>=1;
      if(anim.kind==='co') S.co.x=anim.x0+(anim.x1-anim.x0)*e;
      else { S.no2.a=anim.a0+(anim.ae-anim.a0)*e; S.no2.y=(anim.c-S.no2.a)/2; }
      draw(fin); if(fin) anim=null; }
    else if(mode==='no2') placeMols(t);
  });
}
window.DECK_LABS = { cm322temp(root,API){ tempLab(root,API); } };
})();
