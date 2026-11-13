/* 1-4 염의 가수 분해 — 실험실
   rm14salt : 염 수용액의 액성 예측과 확인 (필수 탐구 반01-탐3, 교과서 23쪽 탐구)
     · 염 5가지(NaCl, CH3COONa, NH4Cl, HCOONa, NaClO) × 농도 0.1 M / 0.01 M.
     · 「내 예측」(산성·중성·염기성)을 고른 뒤 「이온화 상수로 계산」: 짝의 Ka(Kb) → Kb = Kw/Ka(Ka = Kw/Kb), 계산 pH(교과서 근사 √(CK)).
     · 측정: pH 시험지(정수), pH 측정기(소수 둘째 자리) — 참값 [X] = √(CK + Kw)에 고정 시드 잡음, 염기성 용액은 공기 중 CO2로 −0.1.
       「우리 모둠 기록」은 슬라이더 값(수업 실험의 시험지 pH)을 그대로 기록.
     · 측정할 때마다 표에 행(염·농도·내 예측·계산 pH·방법·측정 pH·액성·비교)이 쌓이고, pH 막대에 ◇ 계산 / ● 측정 / ■ 우리 모둠.
     · 비커 속 이온 그림은 가수 분해 비율을 실제보다 크게 그린 모형. */
window.DECK_LABS = {
  rm14salt(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), C=API.COL, mk=(t,a,p)=>API.mk(t,a,p), T=s=>API.tex(s), KW=1e-14;
    const PHC=['#E5323B','#EA4D35','#EF7A2E','#F4A52B','#F5C928','#E3D92E','#A8CF3A','#6DBE45','#3FA65A','#2E9A84','#2E7FB8','#3560A8','#4B4499','#5C338A','#4A2470'];
    // kind: 0 중성, 1 염기성(음이온 가수 분해), -1 산성(양이온 가수 분해)
    const S=[
      {f:'NaCl',kind:0,dis:'\\ce{NaCl -> Na+ + Cl-}',spec:['Na+','Cl-'],
       why:'나트륨 이온은 강염기의, 염화 이온은 강산의 짝이라 둘 다 물과 반응하지 않는다 → 중성'},
      {f:'CH3COONa',kind:1,Kp:1.8e-5,pair:'CH3COOH',ion:'CH3COO-',mol:'CH3COOH',dis:'\\ce{CH3COONa -> CH3COO- + Na+}',hyd:'\\ce{CH3COO- + H2O <=> CH3COOH + OH-}',spec:['Na+'],h:2,
       why:'아세트산 이온은 약산인 아세트산의 짝염기 → 물과 반응해 수산화 이온을 만든다 → 염기성'},
      {f:'NH4Cl',kind:-1,Kp:1.8e-5,pair:'NH3',ion:'NH4+',mol:'NH3',dis:'\\ce{NH4Cl -> NH4+ + Cl-}',hyd:'\\ce{NH4+ + H2O <=> NH3 + H3O+}',spec:['Cl-'],h:2,
       why:'암모늄 이온은 약염기인 암모니아의 짝산 → 물과 반응해 하이드로늄 이온을 만든다 → 산성'},
      {f:'HCOONa',kind:1,Kp:1.8e-4,pair:'HCOOH',ion:'HCOO-',mol:'HCOOH',dis:'\\ce{HCOONa -> HCOO- + Na+}',hyd:'\\ce{HCOO- + H2O <=> HCOOH + OH-}',spec:['Na+'],h:1,
       why:'폼산 이온은 약산인 폼산의 짝염기 — 폼산이 아세트산보다 강한 산이라 Kb가 더 작다 → 약한 염기성'},
      {f:'NaClO',kind:1,Kp:4.0e-8,pair:'HClO',ion:'ClO-',mol:'HClO',dis:'\\ce{NaClO -> Na+ + ClO-}',hyd:'\\ce{ClO- + H2O <=> HClO + OH-}',spec:['Na+'],h:3,
       why:'하이포아염소산 이온은 매우 약한 산의 짝염기라 Kb가 크다 → 염기성이 더 강하다'}];
    const CONC=[0.1,0.01], PRED=['산성','중성','염기성'];
    const sci=v=>{ const e=Math.floor(Math.log10(v)), m=v/Math.pow(10,e); return m.toFixed(1)+'\\times10^{'+e+'}'; };
    const kOf=s=>KW/S[s].Kp;
    function truePH(s,c){ const A=S[s]; if(!A.kind) return 7; const x=Math.sqrt(CONC[c]*kOf(s)+KW); return A.kind>0? 14+Math.log10(x) : -Math.log10(x); }
    function calcPH(s,c){ const A=S[s]; if(!A.kind) return 7; const x=Math.sqrt(CONC[c]*kOf(s)); return A.kind>0? 14+Math.log10(x) : -Math.log10(x); }
    const nature=p=>Math.abs(p-7)<0.5?1:(p<7?0:2);
    // ── 기하
    const BX=24, BW=150, BT=92, BB=246;           // 비커
    const PX=186, PY=140, PW=24, PH=80;            // 시험지
    const RX=368, RW=262, RY0=78, RD=34;           // pH 막대 행
    const X=p=>RX+(p+.5)/15*RW;
    const base=mk('g',{},svg);
    mk('rect',{x:BX+2,y:BT+26,width:BW-4,height:BB-BT-28,fill:'#DDEEF8'},base);
    mk('line',{x1:BX+2,y1:BT+26,x2:BX+BW-2,y2:BT+26,stroke:'#9FC3DD','stroke-width':2},base);
    mk('path',{d:`M${BX-8},${BT} L${BX},${BT+8} L${BX},${BB-10} Q${BX},${BB} ${BX+10},${BB} L${BX+BW-10},${BB} Q${BX+BW},${BB} ${BX+BW},${BB-10} L${BX+BW},${BT}`,fill:'none',stroke:'#7E8B98','stroke-width':3,'stroke-linejoin':'round'},base);
    mk('rect',{x:PX,y:PY,width:PW,height:PH,rx:2,fill:'#F6F1E3',stroke:C.muted,'stroke-width':1.2},base);
    const paper=mk('rect',{x:PX,y:PY,width:PW,height:PH/2,rx:2,fill:'none'},base);
    API.texText(base,PX+PW/2,PY-10,'\\text{시험지}',{size:18,anchor:'middle',fill:C.muted});
    // 오른쪽 pH 막대
    S.forEach((A,i)=>{ const y=RY0+i*RD; API.texText(base,RX-12,y+6,'\\ce{'+A.f+'}',{size:18,anchor:'end'});
      mk('line',{x1:RX,y1:y,x2:RX+RW,y2:y,stroke:'#D5DCE3','stroke-width':2},base); });
    const BY=RY0+5*RD-6;
    for(let i=0;i<15;i++) mk('rect',{x:RX+i*RW/15,y:BY,width:RW/15+.6,height:16,fill:PHC[i]},base);
    mk('rect',{x:RX,y:BY,width:RW,height:16,fill:'none',stroke:C.muted,'stroke-width':1.2},base);
    mk('line',{x1:X(7),y1:RY0-14,x2:X(7),y2:BY,stroke:C.grav,'stroke-width':1.5,'stroke-dasharray':'5 4'},base);
    [0,7,14].forEach(v=>API.texText(base,X(v),BY+36,String(v),{size:18,anchor:'middle',fill:C.muted}));
    API.texText(base,RX-12,BY+14,'\\text{pH}',{size:18,anchor:'end',fill:C.muted});
    // 범례(오른쪽 아래)
    const LY=318;
    mk('path',{d:`M${RX-60},${LY-6} l7,-7 l7,7 l-7,7 Z`,fill:'#fff',stroke:C.ink,'stroke-width':2},base); API.texText(base,RX-42,LY,'\\text{계산}',{size:18,anchor:'start'});
    mk('circle',{cx:RX+40,cy:LY-6,r:6,fill:C.equi},base); API.texText(base,RX+52,LY,'\\text{측정}',{size:18,anchor:'start'});
    mk('rect',{x:RX+122,y:LY-12,width:12,height:12,fill:C.field},base); API.texText(base,RX+140,LY,'\\text{우리 모둠}',{size:18,anchor:'start'});
    const partG=mk('g',{},svg), legG=mk('g',{},svg), markG=mk('g',{},svg);
    // ── 상태
    let seed=11; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    let st, parts=[];
    function init(){ st={s:0,c:0,pred:null,calc:false,rows:[],last:null,marks:{},msg:''}; seed=11; }
    function build(){
      while(partG.firstChild) partG.removeChild(partG.firstChild);
      while(legG.firstChild) legG.removeChild(legG.firstChild);
      parts=[]; const A=S[st.s], n=st.c?3:6, h=A.kind? (st.c? Math.ceil(A.h/2):A.h) : 0;
      let sd=5+st.s*7+st.c*3; const rr=()=>{ sd=(sd*16807)%2147483647; return sd/2147483647; };
      const slots=[]; for(let r=0;r<4;r++) for(let q=0;q<4;q++) slots.push([BX+22+q*35+(r%2)*10, 132+r*32]);
      for(let i=slots.length-1;i>0;i--){ const j=Math.floor(rr()*(i+1)); [slots[i],slots[j]]=[slots[j],slots[i]]; }
      let k=0; const add=(type,sign)=>{ const [x,y]=slots[k++]; const g=mk('g',{},partG);
        if(type==='spec'){ mk('circle',{cx:0,cy:0,r:12,fill:'#E3E7EC',stroke:C.grav,'stroke-width':2},g); sgn(g,sign,C.muted,5); }
        else if(type==='ion'){ const col=sign>0?C.plus:C.minus; mk('circle',{cx:0,cy:0,r:13,fill:sign>0?'#FBD5DA':'#D6E6FA',stroke:col,'stroke-width':2.5},g); sgn(g,sign,col,5.5); }
        else if(type==='mol'){ mk('rect',{x:-15,y:-9,width:30,height:18,rx:9,fill:'#E3E7EC',stroke:C.grav,'stroke-width':2},g); }
        else { const col=sign>0?C.plus:C.minus; mk('circle',{cx:0,cy:0,r:8.5,fill:col},g); sgn(g,sign,'#fff',4); }
        parts.push({g,x,y,ph:rr()*6.28,w:.8+rr()*.8}); g.setAttribute('transform',`translate(${x},${y})`); };
      function sgn(g,s,col,L){ mk('line',{x1:-L,y1:0,x2:L,y2:0,stroke:col,'stroke-width':2.2},g); if(s>0) mk('line',{x1:0,y1:-L,x2:0,y2:L,stroke:col,'stroke-width':2.2},g); }
      if(!A.kind){ for(let i=0;i<n;i++){ add('spec',1); add('spec',-1); } }
      else { const isg=A.kind>0?-1:1;
        for(let i=0;i<n;i++) add('spec',-isg);
        for(let i=0;i<n-h;i++) add('ion',isg);
        for(let i=0;i<h;i++){ add('mol',0); add('prod',A.kind>0?-1:1); } }
      // 범례 기호 + 글
      const L=[[BX+6,268],[BX+6,292],[BX+6,316]];
      const leg=(i,html,draw)=>{ draw(L[i][0],L[i][1]-6); Ov('lg'+(i+1)).innerHTML=html; API.place(Ov('lg'+(i+1)),L[i][0]+18,L[i][1]-18,true); };
      const hide=i=>API.place(Ov('lg'+(i+1)),0,0,false);
      const cc=(x,y,f,s)=>mk('circle',{cx:x,cy:y,r:7,fill:f,stroke:s,'stroke-width':2},legG);
      if(!A.kind){ leg(0,T('\\ce{Na+}')+', '+T('\\ce{Cl-}')+' 그대로',(x,y)=>cc(x,y,'#E3E7EC',C.grav)); hide(1); hide(2); }
      else {
        leg(0,T('\\ce{'+A.spec[0]+'}')+' — 그대로',(x,y)=>cc(x,y,'#E3E7EC',C.grav));
        leg(1,T('\\ce{'+A.ion+'}')+' → '+T('\\ce{'+A.mol+'}')+'(회색)',(x,y)=>cc(x,y,A.kind>0?'#D6E6FA':'#FBD5DA',A.kind>0?C.minus:C.plus));
        leg(2,T(A.kind>0?'\\ce{OH-}':'\\ce{H3O+}')+' 생성',(x,y)=>mk('circle',{cx:x,cy:y,r:6,fill:A.kind>0?C.minus:C.plus},legG)); }
    }
    function message(){
      if(st.msg) return st.msg;
      const A=S[st.s];
      if(st.pred===null) return `${CONC[st.c]} M 수용액에서 어느 이온이 물과 반응할까? 먼저 「내 예측」으로 액성을 고르자.`;
      if(!st.calc) return `내 예측: ${PRED[st.pred]}. 「이온화 상수로 계산」으로 근거를 확인하거나 바로 측정해 보자.`;
      return `${A.why}(계산 pH ${calcPH(st.s,st.c).toFixed(2)}). 이제 측정해 비교하자.`; }
    function paint(){
      const A=S[st.s];
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',+b.dataset.s===st.s));
      root.querySelectorAll('[data-c]').forEach(b=>b.classList.toggle('on',+b.dataset.c===st.c));
      root.querySelectorAll('[data-p]').forEach(b=>b.classList.toggle('on',+b.dataset.p===st.pred));
      O('my').textContent='pH '+$('[data-i="my"]').value;
      O('cp').textContent=st.calc? calcPH(st.s,st.c).toFixed(2) : '—';
      O('mp').textContent=st.last? st.last.txt+' ('+st.last.m+')' : '—';
      O('msg').textContent=message();
      Ov('eq').innerHTML=T(st.calc&&A.kind? A.hyd : A.dis); API.place(Ov('eq'),325,22,true);
      if(st.calc&&A.kind){ const isB=A.kind>0;
        Ov('k').innerHTML=T('\\ce{'+A.pair+'}')+' '+T((isB?'K_\\mathrm{a}=':'K_\\mathrm{b}=')+sci(A.Kp))+' → '+T('\\ce{'+A.ion+'}')+' '+T((isB?'K_\\mathrm{b}':'K_\\mathrm{a}')+'=\\dfrac{K_\\mathrm{w}}{'+(isB?'K_\\mathrm{a}':'K_\\mathrm{b}')+'}='+sci(kOf(st.s))); API.place(Ov('k'),14,40,true); }
      else if(st.calc){ Ov('k').innerHTML='가수 분해하는 이온 없음 → pH 7'; API.place(Ov('k'),14,40,true); }
      else API.place(Ov('k'),0,0,false);
      paper.setAttribute('fill',st.last&&st.last.s===st.s&&st.last.c===st.c? PHC[Math.max(0,Math.min(14,Math.round(st.last.p)))] : 'none');
      // 막대 표시
      while(markG.firstChild) markG.removeChild(markG.firstChild);
      Object.keys(st.marks).forEach(k=>{ const m=st.marks[k], y=RY0+(+k)*RD;
        if(m.calc!=null) mk('path',{d:`M${X(m.calc)-8},${y} L${X(m.calc)},${y-8} L${X(m.calc)+8},${y} L${X(m.calc)},${y+8} Z`,fill:'#fff',stroke:C.ink,'stroke-width':2.5},markG);
        if(m.meas!=null) mk('circle',{cx:X(m.meas),cy:y+13,r:6,fill:C.equi},markG);
        if(m.mine!=null) mk('rect',{x:X(m.mine)-6,y:y-19,width:12,height:12,fill:C.field},markG); });
      // 표
      const tb=O('log'); tb.innerHTML='';
      st.rows.slice(-4).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${T('\\ce{'+S[r.s].f+'}')}</td><td>${CONC[r.c]} M</td><td>${PRED[r.pred]}</td><td>${r.cp}</td><td>${r.m}</td><td>${r.txt}</td><td>${PRED[r.nat]}</td><td>${r.ok?'○':'✗'}</td>`; tb.appendChild(tr); });
    }
    function mark(s){ return st.marks[s]||(st.marks[s]={calc:null,meas:null,mine:null}); }
    function measure(kind){
      st.msg='';
      if(st.pred===null){ st.msg='먼저 「내 예측」(산성·중성·염기성)을 고르자 — 예측한 뒤에 측정해야 비교할 수 있다.'; paint(); return; }
      const A=S[st.s], tp=truePH(st.s,st.c), co2=A.kind>0?-0.1:0;
      let p, txt, m;
      if(kind==='paper'){ p=Math.max(0,Math.min(14,Math.round(tp+(rnd()-.5)*0.5+co2*.5))); txt=String(p); m='pH 시험지'; }
      else if(kind==='meter'){ p=tp+(rnd()-.5)*0.12+co2; txt=p.toFixed(2); m='pH 측정기'; }
      else { p=+$('[data-i="my"]').value; txt=String(p); m='우리 모둠'; }
      const nat=nature(p), ok=nat===st.pred, cp=calcPH(st.s,st.c);
      st.rows.push({s:st.s,c:st.c,pred:st.pred,cp:st.calc?cp.toFixed(2):'—',m,txt,nat,ok});
      st.last={s:st.s,c:st.c,p,txt,m};
      const mm=mark(st.s); if(kind==='mine') mm.mine=p; else mm.meas=p; if(st.calc) mm.calc=cp;
      const diff=st.calc? ` 계산값과의 차이 ${Math.abs(p-cp).toFixed(2)}${kind==='paper'?' — pH 시험지는 1 단위로만 읽는다.':kind==='meter'&&A.kind>0?' — 공기 중 이산화 탄소가 녹으면 조금 낮아진다.':'.'}` : ' (계산 pH와도 비교해 보자.)';
      st.msg=`측정 pH ${txt}(${PRED[nat]}) — 내 예측(${PRED[st.pred]})과 ${ok?'일치한다.':'다르다. 어느 이온이 가수 분해하는지 다시 생각해 보자.'}${diff}`;
      paint(); }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ st.s=+b.dataset.s; st.pred=null; st.calc=false; st.msg=''; build(); paint(); }));
    root.querySelectorAll('[data-c]').forEach(b=>b.addEventListener('click',()=>{ st.c=+b.dataset.c; st.calc=false; st.msg=''; build(); paint(); }));
    root.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{ st.pred=+b.dataset.p; st.msg=''; paint(); }));
    $('[data-act="calc"]').addEventListener('click',()=>{ st.calc=true; st.msg=''; mark(st.s).calc=calcPH(st.s,st.c); paint(); });
    $('[data-act="paper"]').addEventListener('click',()=>measure('paper'));
    $('[data-act="meter"]').addEventListener('click',()=>measure('meter'));
    $('[data-act="mine"]').addEventListener('click',()=>measure('mine'));
    $('[data-i="my"]').addEventListener('input',()=>{ O('my').textContent='pH '+$('[data-i="my"]').value; });
    $('[data-act="reset"]').addEventListener('click',()=>{ init(); $('[data-i="my"]').value=7; build(); paint(); });
    API.loop(root,(dt,t)=>{ parts.forEach(q=>{ q.g.setAttribute('transform',`translate(${(q.x+3*Math.sin(t*q.w+q.ph)).toFixed(1)},${(q.y+3*Math.cos(t*q.w*1.3+q.ph)).toFixed(1)})`); }); });
    init(); build(); paint();
    API.ready(()=>{ build(); paint(); });
  }
};
