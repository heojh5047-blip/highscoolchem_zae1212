/* 3-2-1 농도·압력 변화와 화학 평형 이동 — 실험실
   cm321conc / cm321press : 「평형 이동 실험실」 (화03-탐2) — 같은 함수, 처음 모드만 다름.
   [농도] Cr2O7^2- + H2O ⇌ 2CrO4^2- + 2H+ (모의 K = 3e-15, 4 mL). 처음 용액 K2Cr2O7(Cr 0.2 M) / K2CrO4(Cr 0.1 M), K+ 0.2 M.
          넣기 한 번 = 1 M 0.1 mL → 알짜 염기 b ±0.025 M(부피 변화 무시).
          평형: C=[CrO4^2-] = 0.2 − Ct + b + h − Kw/h, D = (Ct − C)/2, C²h² = K·D → log h 이분법.
          넣은 직후: C, D 그대로, h' − Kw/h' = C − 0.2 + Ct − b' (중화만) → Q' = C²h'²/D.
   [압력] 2NO2 ⇌ N2O4, 25 °C K = 212, NO2 환산 0.010 mol(50 mL에서 0.2 M). 부피 V' → 농도 × V/V', Q = Q·V'/V.
          He · 피스톤 고정 → 그대로, He · 피스톤 자유 → 부피 2배. 평형 2Kx² + x − c = 0 (c = [NO2] + 2[N2O4]).
   [온도] 같은 주사기, K(T) = 212·exp(6856(1/T − 1/298)) (ΔH = −57 kJ, 덱 계산값) — 관찰만.
   조작마다 기록 표에 행 추가(최대 5), 2초 동안 평형으로(API.loop). */
(function(){
function shiftLab(root, API, startMode){
  const $=s=>root.querySelector(s), $$=s=>root.querySelectorAll(s), O=k=>$(`[data-o="${k}"]`);
  const svg=$('svg'), mk=API.mk;
  const OR=[232,121,43], YE=[242,194,48], NO2C='#B5562A', EQ='#E08A2C', MU='#5B6B7F', INK='#16233D', GL='#7E8B98';
  const KC=3e-15, KW=1e-14, DB=0.025, NN=0.010, K25=212, MAXR=4, NMOL=30;
  const mix=(f)=>`rgb(${OR.map((v,i)=>Math.round(v+(YE[i]-v)*f)).join(',')})`;
  const KT=t=>K25*Math.exp(6856*(1/(t+273)-1/298));
  // ---------- 고정 그림 ----------
  const NL={x0:290,x1:670,xc:480,y:70,per:63};
  const XL=l=>NL.xc+API.clamp(l,-3,3)*NL.per;
  const bgC=mk('g',{},svg), bgP=mk('g',{},svg), bath=mk('g',{},svg);
  svg.insertBefore(bath,bgC);
  // 시험관
  const TX=120, TT=40, TB=262, TW=72, tr=TW/2;
  const liq=mk('path',{d:`M${TX-tr+3} 110 V${TB-tr} A${tr-3} ${tr-3} 0 0 0 ${TX+tr-3} ${TB-tr} V110 Z`,fill:mix(0)},bgC);
  mk('path',{d:`M${TX-tr} ${TT} V${TB-tr} A${tr} ${tr} 0 0 0 ${TX+tr} ${TB-tr} V${TT}`,fill:'none',stroke:GL,'stroke-width':3.5},bgC);
  mk('path',{d:`M${TX-tr-6} ${TT} H${TX+tr+6}`,stroke:GL,'stroke-width':3.5,'stroke-linecap':'round'},bgC);
  const sol=[mk('g',{},bgC),mk('g',{},bgC)];
  API.texText(sol[0],TX,292,'$\\ce{K2Cr2O7(aq)}$',{size:19,anchor:'middle',fill:INK,mix:true});
  API.texText(sol[1],TX,292,'$\\ce{K2CrO4(aq)}$',{size:19,anchor:'middle',fill:INK,mix:true});
  const BX=340, BW=290, BY1=166, BY2=204;
  API.texText(bgC,BX-10,BY1+18,'$\\ce{Cr2O7^2-}$',{size:19,anchor:'end',fill:INK,mix:true});
  API.texText(bgC,BX-10,BY2+18,'$\\ce{CrO4^2-}$',{size:19,anchor:'end',fill:INK,mix:true});
  API.texText(bgC,BX,157,'크로뮴 중 비율',{size:18,anchor:'start',fill:MU,mix:true});
  [0,50,100].forEach(v=>{ const x=BX+v/100*BW; mk('path',{d:`M${x} 232 V238`,stroke:MU,'stroke-width':2},bgC);
    API.texText(bgC,x,258,v+' %',{size:18,anchor:'middle',fill:MU,mix:true}); });
  // 주사기
  const SX=120, SW=170, ST=60, SB=262, x0=SX-SW/2, HV=v=>v*1.9; // 100 mL → 190 px
  const gas=mk('rect',{x:x0,y:0,width:SW,height:0,fill:NO2C,'fill-opacity':0.3},bgP);
  const molG=mk('g',{},bgP), heG=mk('g',{},bgP);
  for(let k=1;k<10;k++){ const yy=SB-HV(k*10); mk('path',{d:`M${x0+SW-14} ${yy} H${x0+SW-2}`,stroke:MU,'stroke-width':1.5},bgP); }
  mk('path',{d:`M${x0} ${ST-10} V${SB} H${x0+SW} V${ST-10}`,fill:'none',stroke:GL,'stroke-width':3.5},bgP);
  mk('rect',{x:SX-18,y:SB,width:36,height:14,rx:3,fill:'#2B2F36'},bgP);
  const pist=mk('g',{},bgP);
  mk('rect',{x:x0+2,y:0,width:SW-4,height:12,rx:2,fill:'#3A3F47'},pist); mk('rect',{x:SX-5,y:-46,width:10,height:46,fill:'#8C99A6'},pist); mk('rect',{x:SX-34,y:-56,width:68,height:12,rx:4,fill:'#5B6B7F'},pist);
  const clampL=mk('path',{d:'',stroke:'#D7263D','stroke-width':5,'stroke-linecap':'round'},bgP);
  API.texText(bgP,BX-10,BY1+18,'$[\\ce{NO2}]$',{size:19,anchor:'end',fill:INK,mix:true});
  API.texText(bgP,BX-10,BY2+18,'$[\\ce{N2O4}]$',{size:19,anchor:'end',fill:INK,mix:true});
  API.texText(bgP,BX,157,'몰농도 (mol/L)',{size:18,anchor:'start',fill:MU,mix:true});
  const PMAX=0.4;
  [0,0.2,0.4].forEach(v=>{ const x=BX+v/PMAX*BW; mk('path',{d:`M${x} 232 V238`,stroke:MU,'stroke-width':2},bgP);
    API.texText(bgP,x,258,v.toFixed(1),{size:18,anchor:'middle',fill:MU,mix:true}); });
  // 수직선(공통)
  const bgN=mk('g',{},svg);
  API.texText(bgN,NL.x0-6,24,'반응 지수 $Q$ (로그 눈금)',{size:18,anchor:'start',fill:INK,mix:true});
  API.arrow(bgN,NL.x0-8,NL.y,NL.x1+14,NL.y,'ink',2);
  [-3,-2,-1,0,1,2,3].forEach(l=>{ const x=XL(l); mk('path',{d:`M${x} ${NL.y-(l%3?5:8)} V${NL.y+(l%3?5:8)}`,stroke:INK,'stroke-width':2},bgN); });
  API.texText(bgN,XL(-3),NL.y+36,'$10^{-3}K$',{size:18,anchor:'middle',fill:INK,mix:true});
  API.texText(bgN,XL(3),NL.y+36,'$10^{3}K$',{size:18,anchor:'middle',fill:INK,mix:true});
  mk('path',{d:`M${NL.xc} ${NL.y-30} V${NL.y+10}`,stroke:INK,'stroke-width':3,'stroke-dasharray':'7 5'},bgN);
  API.texText(bgN,NL.xc+10,NL.y-26,'$K$',{size:21,anchor:'start',fill:INK,mix:true});
  API.texText(bgN,NL.x0,NL.y+63,'$Q<K$ 정반응 우세',{size:18,anchor:'start',fill:'#2E9E6A',mix:true});
  API.texText(bgN,NL.x1+10,NL.y+63,'역반응 우세 $Q>K$',{size:18,anchor:'end',fill:'#7B4FC8',mix:true});
  const qg=mk('g',{},svg);
  mk('circle',{cx:0,cy:NL.y,r:9,fill:EQ,stroke:'#fff','stroke-width':2},qg);
  API.texText(qg,0,NL.y-16,'$Q$',{size:19,anchor:'middle',fill:'#B45F06',mix:true});
  const dyn=mk('g',{},svg);
  const info=mk('text',{x:BX,y:290,'font-size':19,fill:MU},svg);
  // ---------- 상태 ----------
  let mode, rows=[], nexp=0, anim=null;
  const S={sol:0, Ct:0.2, b:0, h:0, C:0, nOH:0, nH:0, V:50, T:25, a:0, y:0, he:0, heFix:false};
  // 분자 자리(고정 시드)
  let seed=7; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
  const slots=[]; for(let i=0;i<NMOL;i++) slots.push({u:rnd(),v:rnd(),a:Math.floor(rnd()*6)*30,w:1+rnd()*2,p:rnd()*6.28});
  const heSlots=[]; for(let i=0;i<14;i++) heSlots.push({u:rnd(),v:rnd(),w:1.5+rnd()*2,p:rnd()*6.28});
  let molKey='', molEls=[];
  function molecule(g,kind){ const r=6, d=1.35*r;
    if(kind==='a'){ [-67,67].forEach(b=>{ const q=(b-90)*Math.PI/180; API.atom(g,d*Math.cos(q),d*Math.sin(q),r,'O','-',false); }); API.atom(g,0,0,r,'N','-',false); }
    else { const dn=1.45*r; [-1,1].forEach(sd=>{ const nx=sd*dn/2, base=sd>0?0:180; [-62,62].forEach(b=>{ const q=(base+b)*Math.PI/180; API.atom(g,nx+d*Math.cos(q),d*Math.sin(q),r,'O','-',false); }); });
      [-1,1].forEach(sd=>API.atom(g,sd*dn/2,0,r,'N','-',false)); } }
  function buildMols(n){ const m=(NMOL-n)/2, key=n+'/'+m; if(key===molKey) return; molKey=key; molG.innerHTML=''; molEls=[];
    for(let i=0;i<n+m;i++){ const g=mk('g',{},molG); molecule(g,i<n?'a':'b'); molEls.push(g); } }
  function placeMols(t){ const yp=SB-12-HV(S.V), H=SB-(yp+12);
    molEls.forEach((g,i)=>{ const s=slots[i], jx=Math.sin(t*s.w+s.p)*2.5, jy=Math.cos(t*s.w*1.3+s.p)*2.5;
      const x=x0+16+s.u*(SW-32)+jx, y=yp+12+12+s.v*Math.max(0,H-24)+jy; g.setAttribute('transform',`translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${s.a})`); });
    [...heG.children].forEach((c,i)=>{ const s=heSlots[i], x=x0+12+s.u*(SW-24)+Math.sin(t*s.w+s.p)*3, y=yp+12+10+s.v*Math.max(0,H-20)+Math.cos(t*s.w+s.p)*3; c.setAttribute('cx',x.toFixed(1)); c.setAttribute('cy',y.toFixed(1)); }); }
  // ---------- 화학 계산 ----------
  const Cof=h=>S.Ct===0.2? S.b+h-KW/h : 0.1+S.b+h-KW/h;
  function eqConc(){ let lo=-15, hi=1;
    for(let k=0;k<80;k++){ const lm=(lo+hi)/2, h=Math.pow(10,lm), C=API.clamp(Cof(h),0,S.Ct), f=C*C*h*h-KC*(S.Ct-C)/2; if(f>0) hi=lm; else lo=lm; }
    const h=Math.pow(10,(lo+hi)/2); return {h, C:API.clamp(Cof(h),0,S.Ct)}; }
  const Qc=(C,h)=>C*C*h*h/Math.max(1e-30,(S.Ct-C)/2);
  const eqGas=(c,K)=>{ const x=(-1+Math.sqrt(1+8*K*c))/(4*K); return [x,(c-x)/2]; };
  const colName=fy=>fy<0.15?'주황색':fy>0.85?'노란색':fy<0.5?'주황색(노란빛)':'노란색(주황빛)';
  const fmtQ=q=>q>=100?q.toFixed(0):q>=10?q.toFixed(1):q.toFixed(2);
  // ---------- 그리기 ----------
  function drawConc(C,h,lq,done){
    const fy=C/S.Ct; liq.setAttribute('fill',mix(fy));
    dyn.innerHTML='';
    [[1-fy,'#E8792B',BY1],[fy,'#F2C230',BY2]].forEach(([v,c,yy])=>{ mk('rect',{x:BX,y:yy,width:Math.max(1,v*BW),height:24,rx:3,fill:c,stroke:'#9A6A1A','stroke-width':1.2},dyn);
      const t=mk('text',{x:BX+Math.min(v*BW,BW-40)+8,y:yy+19,'font-size':19,fill:INK},dyn); t.textContent=Math.round(v*100)+' %'; });
    posQ(lq,done);
    info.textContent=`넣은 횟수: 염기 ${S.nOH}회 · 산 ${S.nH}회`;
  }
  function drawGas(a,y,K,done){
    const yp=SB-12-HV(S.V); pist.setAttribute('transform',`translate(0,${yp})`);
    gas.setAttribute('y',yp+12); gas.setAttribute('height',SB-yp-12); gas.setAttribute('fill-opacity',(0.9*(1-Math.exp(-a/0.06))).toFixed(3));
    clampL.setAttribute('d',S.heFix?`M${x0-22} ${yp-2} H${x0+SW+22}`:'');
    const c=a+2*y; buildMols(2*Math.round((NMOL/2)*a/c)); placeMols(performance.now()/1000);
    dyn.innerHTML='';
    [[a,NO2C,NO2C,BY1],[y,'#fff',INK,BY2]].forEach(([v,fc,sc,yy])=>{ mk('rect',{x:BX,y:yy,width:Math.max(1,Math.min(v,PMAX)/PMAX*BW),height:24,rx:3,fill:fc,'fill-opacity':fc==='#fff'?1:0.8,stroke:sc,'stroke-width':2},dyn);
      const t=mk('text',{x:BX+Math.min(v,PMAX)/PMAX*BW+8,y:yy+19,'font-size':19,fill:INK},dyn); t.textContent=v.toFixed(4); });
    posQ(Math.log10((y/(a*a))/K),done);
    info.textContent=`${S.T} °C · 부피 ${S.V} mL · K = ${K>=100?K.toFixed(0):K.toFixed(1)}`+(S.he?' · He 들어 있음':'');
    bath.innerHTML='';
    if(mode==='temp'||S.T!==25){ const col=S.T<25?'#E3EEFB':S.T>25?'#FDE2E4':'#F4F6F8'; mk('rect',{x:x0-22,y:150,width:SW+44,height:132,rx:10,fill:col,stroke:S.T<25?'#9FC3DD':'#E8A0A8','stroke-width':2},bath);
      if(S.T<25) for(let k=0;k<4;k++) mk('rect',{x:x0-16+k*58,y:250,width:16,height:16,rx:3,fill:'#fff',stroke:'#9FC3DD','stroke-width':1.5},bath); }
  }
  function posQ(l,done){ qg.setAttribute('transform',`translate(${XL(l).toFixed(1)},0)`);
    if(!done && Math.abs(l)>0.02){ const xq=XL(l), s=l<0; API.arrow(dyn,xq+(s?12:-12),NL.y+14,NL.xc+(s?-6:6),NL.y+14,s?'field':'bfield',3); }
    O('q').textContent= done||Math.abs(l)<0.02 ? 'Q = K' : (l<0?(l<-3?'Q ≪ K':'Q < K'):(l>3?'Q ≫ K':'Q > K')); }
  function redraw(done){ if(mode==='conc') drawConc(S.C,S.h,Math.log10(Qc(S.C,S.h)/KC),done!==false); else drawGas(S.a,S.y,KT(S.T),done!==false); }
  // ---------- 기록 ----------
  function log(r){ nexp++; rows.push([nexp,...r]); if(rows.length>MAXR) rows.shift(); const tb=O('log'); tb.innerHTML='';
    rows.forEach(rw=>{ const t=document.createElement('tr'); t.innerHTML=rw.map(v=>`<td>${v}</td>`).join(''); tb.appendChild(t); }); }
  const dirTxt=l=>Math.abs(l)<0.02?'이동 없음':l<0?'정반응':'역반응';
  const cmpTxt=l=>Math.abs(l)<0.02?'Q = K':l<0?'Q < K':'Q > K';
  // ---------- 조작 ----------
  function finish(){ if(anim&&anim.kind==='gas'){ S.a=anim.ae; S.y=(anim.c-anim.ae)/2; } anim=null; }
  function addConc(sign){ // sign +1 염기, −1 산
    finish(); const C0=S.C, fy0=C0/S.Ct;
    S.b+=sign*DB; if(sign>0) S.nOH++; else S.nH++;
    const s=C0-0.2+S.Ct-S.b, h1=(s+Math.sqrt(s*s+4*KW))/2, l1=Math.log10(Qc(C0,h1)/KC);
    const e=eqConc();
    anim={kind:'conc',t:0,C0,h0:h1,C1:e.C,h1:e.h,l0:l1};
    const fy1=e.C/S.Ct, small=Math.abs(fy1-fy0)<0.03;
    O('msg').textContent= sign>0
      ? `수산화 나트륨 수용액: 수산화 이온이 수소 이온과 중화 → [H+] 감소 → ${cmpTxt(l1)} → 정반응이 우세하게 진행한다. 크로뮴산 이온이 늘어 노란색 쪽으로 변한다.`+(small?' (이미 대부분 노란색이라 색 변화는 거의 없다.)':'')
      : `염산: [H+] 증가 → ${cmpTxt(l1)} → 역반응이 우세하게 진행한다. 다이크로뮴산 이온이 늘어 주황색 쪽으로 변한다.`+(small?' (이미 대부분 주황색이라 색 변화는 거의 없다.)':'');
    log(['농도',API.tex(sign>0?'\\ce{NaOH(aq)}':'\\ce{HCl(aq)}')+' 넣기',cmpTxt(l1),dirTxt(l1),colName(fy1)]);
    S.C=e.C; S.h=e.h; drawConc(C0,h1,l1,false);
  }
  function gasChange(kind){
    finish(); const K=KT(S.T); let V1=S.V, label, varn='압력';
    if(kind==='vol'){ V1=+$('[data-i="v"]').value; if(V1===S.V){ O('msg').textContent='바꿀 부피가 지금 부피와 같다. 슬라이더로 다른 부피를 고르자.'; return; } label=`부피 ${S.V} → ${V1} mL`; }
    else if(kind==='hefix'){ S.he=1; S.heFix=true; label='He · 피스톤 고정'; }
    else if(kind==='hefree'){ if(S.V>50){ O('msg').textContent='부피가 100 mL를 넘게 되므로 먼저 부피를 50 mL 이하로 줄이자.'; return; } V1=S.V*2; S.he=1; S.heFix=false; label=`He · 자유(${S.V}→${V1} mL)`; }
    const f=S.V/V1, a0=S.a*f, y0=S.y*f; S.V=V1; S.a=a0; S.y=y0;
    heG.innerHTML=''; if(S.he) for(let i=0;i<10;i++) mk('circle',{r:5,fill:'#CFE8F5',stroke:'#7FA9C2','stroke-width':1.5},heG);
    startGas(K,label,varn,f);
  }
  function setT(t){ finish(); if(t===S.T){ O('msg').textContent=`이미 ${t} °C이다. 다른 온도를 골라 보자.`; return; } const T0=S.T; S.T=t; startGas(KT(t),`${T0} → ${t} °C`,'온도'); }
  function startGas(K,label,varn,f){
    const l1=Math.log10((S.y/(S.a*S.a))/K), c=S.a+2*S.y, [ae,ye]=eqGas(c,K);
    anim={kind:'gas',t:0,a0:S.a,ae,c,K};
    const pre= varn==='온도' ? `온도가 바뀌어 K가 ${K>=100?K.toFixed(0):K.toFixed(1)}(으)로 바뀜 → ` : f===1 ? '부피가 그대로라 농도가 변하지 않음 → ' : f>1 ? '부피 감소(압력 증가) → 농도 증가 → ' : '부피 증가(압력 감소) → 농도 감소 → ';
    const q1=S.y/(S.a*S.a);
    let m=pre+`Q(${fmtQ(q1)}) ${Math.abs(l1)<0.02?'=':l1<0?'<':'>'} K(${K>=100?K.toFixed(0):K.toFixed(1)}) → `;
    if(Math.abs(l1)<0.02) m+='평형이 이동하지 않는다.';
    else if(l1<0) m+='전체 기체 분자 수가 감소하는 정반응이 우세하게 진행한다. 적갈색이 옅어진다.';
    else m+='전체 기체 분자 수가 증가하는 역반응이 우세하게 진행한다. 적갈색이 진해진다.';
    if(varn==='온도') m+=' (까닭은 다음 시간 02에서)';
    O('msg').textContent=m;
    const obs= Math.abs(l1)<0.02?'색 그대로': l1<0?'연해짐, 분자 수 감소':'진해짐, 분자 수 증가';
    log([varn,label,cmpTxt(l1),dirTxt(l1),obs]);
    if(Math.abs(l1)<0.02){ anim=null; redraw(true); } else drawGas(S.a,S.y,K,false);
  }
  // ---------- 모드·초기화 ----------
  function setMode(m){ finish(); mode=m;
    $$('[data-mode]').forEach(b=>b.classList.toggle('cm321-act',b.dataset.mode===m));
    $$('[data-pane]').forEach(p=>p.style.display=p.dataset.pane===m?'':'none');
    bgC.style.display=m==='conc'?'':'none'; bgP.style.display=m==='conc'?'none':''; bath.style.display=m==='conc'?'none':'';
    O('msg').textContent= m==='conc' ? '처음 용액을 고르고, 수산화 나트륨 수용액이나 염산을 넣어 보자.' : m==='press' ? '바꿀 부피를 고르고 [부피 바꾸기]를 누르자. 헬륨을 넣어 볼 수도 있다.' : '주사기를 담글 물의 온도를 골라 보자.';
    redraw(true); }
  function setSol(i){ finish(); S.sol=i; S.Ct=i?0.1:0.2; S.b=0; S.nOH=0; S.nH=0; const e=eqConc(); S.C=e.C; S.h=e.h;
    $$('[data-sol]').forEach(b=>b.classList.toggle('cm321-act',+b.dataset.sol===i)); sol[0].style.display=i?'none':''; sol[1].style.display=i?'':'none'; if(mode==='conc'){ anim=null; redraw(true); } }
  function resetGas(){ S.V=50; S.T=25; S.he=0; S.heFix=false; heG.innerHTML=''; const [a,y]=eqGas(NN/(S.V/1000),K25); S.a=a; S.y=y; $('[data-i="v"]').value=25; O('v').textContent='25 mL';
    $$('[data-t]').forEach(b=>b.classList.toggle('cm321-act',+b.dataset.t===25)); }
  function reset(){ rows=[]; nexp=0; O('log').innerHTML=''; setSol(0); resetGas(); setMode(mode||startMode); }
  $$('[data-mode]').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.mode)));
  $$('[data-sol]').forEach(b=>b.addEventListener('click',()=>setSol(+b.dataset.sol)));
  $$('[data-t]').forEach(b=>b.addEventListener('click',()=>{ setT(+b.dataset.t); $$('[data-t]').forEach(x=>x.classList.toggle('cm321-act',x===b)); }));
  $('[data-act="oh"]').addEventListener('click',()=>addConc(1));
  $('[data-act="h"]').addEventListener('click',()=>addConc(-1));
  $('[data-act="vol"]').addEventListener('click',()=>gasChange('vol'));
  $('[data-act="hefix"]').addEventListener('click',()=>gasChange('hefix'));
  $('[data-act="hefree"]').addEventListener('click',()=>gasChange('hefree'));
  $('[data-act="reset"]').addEventListener('click',()=>{ mode=null; reset(); });
  $('[data-i="v"]').addEventListener('input',e=>{ O('v').textContent=e.target.value+' mL'; });
  mode=startMode; reset();
  API.loop(root,(dt,t)=>{
    if(anim){ anim.t=Math.min(1,anim.t+dt/(anim.kind==='conc'?1.5:2)); const e=1-Math.pow(1-anim.t,3), fin=anim.t>=1;
      if(anim.kind==='conc'){ const C=anim.C0+(anim.C1-anim.C0)*e, lh=Math.log10(anim.h0)+(Math.log10(anim.h1)-Math.log10(anim.h0))*e;
        drawConc(C,Math.pow(10,lh),anim.l0*(1-e),fin); }
      else { const a=anim.a0+(anim.ae-anim.a0)*e, y=(anim.c-a)/2; S.a=a; S.y=y; drawGas(a,y,anim.K,fin); }
      if(fin) anim=null; }
    else if(mode!=='conc') placeMols(t);
  });
}
window.DECK_LABS = {
  cm321conc(root,API){ shiftLab(root,API,'conc'); },
  cm321press(root,API){ shiftLab(root,API,'press'); }
};
})();
