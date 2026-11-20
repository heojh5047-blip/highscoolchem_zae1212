/* 1-5 완충 작용 — 실험실
   rm15buf : 물과 완충 용액에 산·염기를 넣을 때의 pH 변화 비교 (필수 탐구 반01-탐4, 교과서 24–25쪽 탐구)
     · 액체 4가지(각 50 mL): 증류수 / 0.2 M 아세트산 / 0.2 M 아세트산 나트륨 / 완충 용액(아세트산·아세트산 나트륨 각 0.1 M).
     · 0.2 M 수산화 나트륨 수용액·염산을 1 mL, 5 mL씩 넣는다(한 비커에 30 mL까지). 반대 시약을 넣으면 새 비커로 다시 담는다(교과서 과정 4).
     · 참값 pH: 전하 균형 [H3O+] + [Na+] = [Cl-] + [OH-] + C·Ka/(Ka + [H3O+]) 를 이분법으로 풂(부피 변화 포함). Ka = 1.8e-5, Kw = 1.0e-14.
       화면에는 식을 보이지 않는다(범위 제한: 복잡한 pH 계산 지양).
     · 「pH 측정」은 참값 + 고정 시드 잡음(±0.03). 「우리 모둠 기록」은 슬라이더 값(수업 실험의 측정기 pH).
     · 측정할 때마다 표에 행(액체·넣은 것·측정 pH·처음과의 차이·내 예측·비교)이 쌓이고, 그래프(가로: 넣은 부피, 왼쪽 HCl / 오른쪽 NaOH)에 점이 찍혀 선으로 이어진다.
     · 비커 입자 모형: 입자 1개 = 0.25 mmol. 넣은 H3O+은 먼저 CH3COO-과, OH-은 먼저 CH3COOH과 반응(화학량론). Na+, Cl-, 물은 그리지 않음. */
window.DECK_LABS = {
  rm15buf(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), C=API.COL, mk=(t,a,p)=>API.mk(t,a,p), T=s=>API.tex(s), KA=1.8e-5, KW=1e-14, CR=0.2, V0=50, VMAX=30;
    // ha·ac: 처음 양(mmol, 50 mL 안), na: 염에서 온 Na+(mmol)
    const S=[
      {nm:'증류수',ha:0,ac:0,na:0,col:C.grav,dash:'6 5',w:3},
      {nm:'아세트산',ha:10,ac:0,na:0,col:C.plus,dash:null,w:3},
      {nm:'아세트산 나트륨',ha:0,ac:10,na:10,col:C.minus,dash:null,w:3},
      {nm:'완충 용액',ha:5,ac:5,na:5,col:C.ink,dash:null,w:4.5}];
    const PRED=['크게 변한다','거의 변하지 않는다'];
    function truePH(s,vb,va){
      const A=S[s], V=V0+vb+va, Ct=(A.ha+A.ac)/V, Na=(A.na+CR*vb)/V, Cl=CR*va/V;
      let lo=-15, hi=1, m=0;
      for(let i=0;i<90;i++){ m=(lo+hi)/2; const H=Math.pow(10,m); const f=H+Na-Cl-KW/H-Ct*KA/(KA+H); if(f>0) hi=m; else lo=m; }
      return -m; }
    function amounts(s,vb,va){
      const A=S[s]; let ha=A.ha, ac=A.ac, fh=0, fo=0;
      const nb=CR*vb, na=CR*va;
      if(nb>0){ const d=Math.min(nb,ha); ha-=d; ac+=d; fo=nb-d; }
      if(na>0){ const d=Math.min(na,ac); ac-=d; ha+=d; fh=na-d; }
      return {ha,ac,fh,fo}; }
    // ── 기하
    const BX=18, BW=212, BT=58, BB=244, LV=86;
    const GX0=300, GX1=628, GY0=262, GY1=36;
    const GX=v=>GX0+(v+VMAX)/(2*VMAX)*(GX1-GX0), GY=p=>GY0-p/14*(GY0-GY1);
    const base=mk('g',{},svg);
    mk('rect',{x:BX+2,y:LV,width:BW-4,height:BB-LV-2,fill:'#DDEEF8'},base);
    mk('line',{x1:BX+2,y1:LV,x2:BX+BW-2,y2:LV,stroke:'#9FC3DD','stroke-width':2},base);
    mk('path',{d:`M${BX-8},${BT} L${BX},${BT+8} L${BX},${BB-10} Q${BX},${BB} ${BX+10},${BB} L${BX+BW-10},${BB} Q${BX+BW},${BB} ${BX+BW},${BB-10} L${BX+BW},${BT}`,fill:'none',stroke:'#7E8B98','stroke-width':3,'stroke-linejoin':'round'},base);
    // 그래프 축
    mk('line',{x1:GX0,y1:GY0,x2:GX1+10,y2:GY0,stroke:C.muted,'stroke-width':2},base);
    const xm=GX(0);
    mk('line',{x1:xm,y1:GY0,x2:xm,y2:GY1-10,stroke:C.muted,'stroke-width':2},base);
    mk('path',{d:`M${xm},${GY1-18} L${xm-5},${GY1-8} L${xm+5},${GY1-8} Z`,fill:C.muted},base);
    mk('line',{x1:GX0,y1:GY(7),x2:GX1,y2:GY(7),stroke:C.grav,'stroke-width':1.5,'stroke-dasharray':'5 4'},base);
    [0,7,14].forEach(v=>{ mk('line',{x1:xm-5,y1:GY(v),x2:xm,y2:GY(v),stroke:C.muted,'stroke-width':2},base); });
    [7,14].forEach(v=>API.texText(base,xm-9,GY(v)+7,String(v),{size:18,anchor:'end',fill:C.muted}));
    API.texText(base,xm+8,GY1-4,'\\text{pH}',{size:18,anchor:'start',fill:C.muted});
    [-30,-20,-10,10,20,30].forEach(v=>{ mk('line',{x1:GX(v),y1:GY0,x2:GX(v),y2:GY0+6,stroke:C.muted,'stroke-width':2},base);
      API.texText(base,GX(v),GY0+26,String(Math.abs(v)),{size:18,anchor:'middle',fill:C.muted}); });
    API.texText(base,xm,GY0+26,'0',{size:18,anchor:'middle',fill:C.muted});
    API.texText(base,GX(-15),GY0+52,'\\leftarrow\\ \\ce{HCl}',{size:18,anchor:'middle',fill:C.plus});
    API.texText(base,GX(15),GY0+52,'\\ce{NaOH}\\ \\rightarrow',{size:18,anchor:'middle',fill:C.minus});
    API.texText(base,GX1+8,GY0-10,'V\\ [\\text{mL}]',{size:18,anchor:'end',fill:C.muted});
    // 그래프 범례(액체별 선)
    S.forEach((A,i)=>{ const y=GY1+10+i*22, x=GX0+4;
      const ln=mk('line',{x1:x,y1:y,x2:x+26,y2:y,stroke:A.col,'stroke-width':A.w},base); if(A.dash) ln.setAttribute('stroke-dasharray','4 3');
      API.texText(base,x+32,y+6,'\\text{'+A.nm+'}',{size:18,anchor:'start',fill:C.ink}); });
    const partG=mk('g',{},svg), legG=mk('g',{},svg), plotG=mk('g',{},svg);
    // ── 상태
    let seed=7; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    let st, parts=[];
    function init(){ st={s:0,pred:null,vb:[0,0,0,0],va:[0,0,0,0],p0:[null,null,null,null],pts:[[],[],[],[]],mine:[[],[],[],[]],rows:[],last:null,msg:''}; seed=7; }
    const addTxt=s=>st.vb[s]? `NaOH ${st.vb[s]} mL` : st.va[s]? `HCl ${st.va[s]} mL` : '없음';
    const addLong=s=>st.vb[s]||st.va[s]? '0.2 M '+addTxt(s) : '없음 (50 mL)';
    function build(){
      while(partG.firstChild) partG.removeChild(partG.firstChild);
      while(legG.firstChild) legG.removeChild(legG.firstChild);
      parts=[]; const s=st.s, am=amounts(s,st.vb[s],st.va[s]);
      const q=n=>Math.round(n/0.25+1e-9);
      const list=[]; for(let i=0;i<q(am.ha);i++) list.push('ha'); for(let i=0;i<q(am.ac);i++) list.push('ac');
      for(let i=0;i<q(am.fh);i++) list.push('h'); for(let i=0;i<q(am.fo);i++) list.push('o');
      let sd=3+s*11; const rr=()=>{ sd=(sd*16807)%2147483647; return sd/2147483647; };
      const slots=[]; for(let r=0;r<8;r++) for(let c=0;c<8;c++) slots.push([BX+20+c*24.5+(r%2)*8, LV+16+r*19.5]);
      for(let i=slots.length-1;i>0;i--){ const j=Math.floor(rr()*(i+1)); [slots[i],slots[j]]=[slots[j],slots[i]]; }
      list.forEach((k,i)=>{ const [x,y]=slots[i%slots.length]; const g=mk('g',{},partG);
        if(k==='ha') mk('rect',{x:-10,y:-6,width:20,height:12,rx:6,fill:'#E3E7EC',stroke:C.grav,'stroke-width':1.8},g);
        else if(k==='ac'){ mk('circle',{cx:0,cy:0,r:7,fill:'#D6E6FA',stroke:C.minus,'stroke-width':1.8},g); mk('line',{x1:-3.5,y1:0,x2:3.5,y2:0,stroke:C.minus,'stroke-width':1.8},g); }
        else { const col=k==='h'?C.plus:C.minus; mk('circle',{cx:0,cy:0,r:7,fill:col},g); mk('line',{x1:-3.5,y1:0,x2:3.5,y2:0,stroke:'#fff','stroke-width':1.8},g); if(k==='h') mk('line',{x1:0,y1:-3.5,x2:0,y2:3.5,stroke:'#fff','stroke-width':1.8},g); }
        g.setAttribute('transform',`translate(${x},${y})`); parts.push({g,x,y,ph:rr()*6.28,w:.7+rr()*.8}); });
      // 범례
      const L=[[BX+8,272],[BX+8,296],[BX+8,320]];
      const place=(i,html)=>{ Ov('lg'+(i+1)).innerHTML=html; API.place(Ov('lg'+(i+1)),L[i][0]+16,L[i][1]-17,true); };
      mk('rect',{x:L[0][0]-6,y:L[0][1]-12,width:14,height:9,rx:4,fill:'#E3E7EC',stroke:C.grav,'stroke-width':1.5},legG);
      mk('circle',{cx:L[1][0]+1,cy:L[1][1]-7,r:6,fill:'#D6E6FA',stroke:C.minus,'stroke-width':1.5},legG);
      place(0,T('\\ce{CH3COOH}')+' '+q(am.ha)+'개');
      place(1,T('\\ce{CH3COO-}')+' '+q(am.ac)+'개');
      if(am.fo>0){ mk('circle',{cx:L[2][0]+1,cy:L[2][1]-7,r:6,fill:C.minus},legG); place(2,'남은 '+T('\\ce{OH-}')+' '+q(am.fo)+'개'); }
      else if(am.fh>0){ mk('circle',{cx:L[2][0]+1,cy:L[2][1]-7,r:6,fill:C.plus},legG); place(2,'남은 '+T('\\ce{H3O+}')+' '+q(am.fh)+'개'); }
      else place(2,'<span class="c-muted">입자 1개 = 0.25 mmol, '+T('\\ce{Na+}')+' 생략</span>');
    }
    function why(s,am,isBase){
      if(s===0) return '넣은 이온과 반응할 물질이 없다';
      if(s===1) return isBase? (am.fo>0?'아세트산이 다 소모되었다':'넣은 수산화 이온을 아세트산이 중화했다(이때 아세트산 이온이 생긴다)') : '하이드로늄 이온과 반응할 아세트산 이온이 거의 없다';
      if(s===2) return isBase? '수산화 이온과 반응할 아세트산이 없다' : (am.fh>0?'아세트산 이온이 다 소모되었다':'넣은 하이드로늄 이온을 아세트산 이온이 받았다(염기성은 사라지고 아세트산이 생긴다)');
      if(isBase) return am.fo>0? '아세트산이 다 소모되어 완충 작용의 한계를 넘었다' : '넣은 수산화 이온을 아세트산이 중화했다';
      return am.fh>0? '아세트산 이온이 다 소모되어 완충 작용의 한계를 넘었다' : '넣은 하이드로늄 이온을 아세트산 이온이 받았다'; }
    function message(){
      if(st.msg) return st.msg;
      if(st.p0[st.s]===null) return `${S[st.s].nm} 50 mL — 먼저 처음 pH를 측정하자.`;
      if(st.pred===null) return `${S[st.s].nm}의 처음 pH ${st.p0[st.s].toFixed(2)}. 「내 예측」을 고르고 수산화 나트륨이나 염산을 넣어 보자.`;
      return `내 예측: ${PRED[st.pred]}. 수산화 나트륨이나 염산을 넣고 「pH 측정」을 누르자.`; }
    function paint(){
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',+b.dataset.s===st.s));
      root.querySelectorAll('[data-p]').forEach(b=>b.classList.toggle('on',+b.dataset.p===st.pred));
      O('my').textContent='pH '+(+$('[data-i="my"]').value).toFixed(1);
      O('add').textContent=addLong(st.s);
      O('mp').textContent=st.last&&st.last.s===st.s? st.last.txt : '—';
      O('msg').textContent=message();
      // 그래프
      while(plotG.firstChild) plotG.removeChild(plotG.firstChild);
      S.forEach((A,i)=>{ const pts=st.pts[i].slice().sort((a,b)=>a.v-b.v);
        if(pts.length>1){ const ln=mk('path',{d:'M'+pts.map(p=>GX(p.v).toFixed(1)+' '+GY(p.p).toFixed(1)).join(' L'),fill:'none',stroke:A.col,'stroke-width':A.w,'stroke-linejoin':'round'},plotG); if(A.dash) ln.setAttribute('stroke-dasharray',A.dash); }
        pts.forEach(p=>mk('circle',{cx:GX(p.v),cy:GY(p.p),r:i===3?6:5,fill:i===0?'#fff':A.col,stroke:A.col,'stroke-width':2},plotG));
        st.mine[i].forEach(p=>mk('rect',{x:GX(p.v)-5,y:GY(p.p)-5,width:10,height:10,fill:C.field},plotG)); });
      const v=st.vb[st.s]-st.va[st.s];
      mk('line',{x1:GX(v),y1:GY0-4,x2:GX(v),y2:GY0+4,stroke:S[st.s].col,'stroke-width':5},plotG);
      // 표
      const tb=O('log'); tb.innerHTML='';
      st.rows.slice(-5).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${S[r.s].nm}</td><td>${r.add}</td><td>${r.txt}</td><td>${r.d}</td><td>${r.pred}</td><td>${r.ok}</td>`; tb.appendChild(tr); });
    }
    function record(kind){
      st.msg='';
      const s=st.s, vb=st.vb[s], va=st.va[s], v=vb-va, am=amounts(s,vb,va);
      let p, txt;
      if(kind==='mine'){ p=+$('[data-i="my"]').value; txt=p.toFixed(1)+' (모둠)'; }
      else { p=Math.max(0,Math.min(14,truePH(s,vb,va)+(rnd()-.5)*0.06)); txt=p.toFixed(2); }
      if(v===0&&kind!=='mine') st.p0[s]=p;
      let d='—', ok='—';
      if(v!==0&&st.p0[s]!==null){ const dd=p-st.p0[s]; d=(dd>=0?'+':'−')+Math.abs(dd).toFixed(2);
        if(st.pred!==null) ok=((Math.abs(dd)>=1)===(st.pred===0))?'○':'✗'; }
      st.rows.push({s,add:addTxt(s),txt,d,pred:st.pred===null?'—':PRED[st.pred],ok});
      if(kind==='mine') st.mine[s].push({v,p}); else { st.pts[s]=st.pts[s].filter(q=>Math.abs(q.v-v)>1e-9); st.pts[s].push({v,p}); }
      st.last={s,txt};
      if(v===0) st.msg=`${S[s].nm} 처음 pH ${txt}. 이제 「내 예측」을 고르고 수산화 나트륨이나 염산을 넣어 보자.`;
      else if(st.p0[s]===null) st.msg=`측정 pH ${txt}. 처음 pH를 측정하지 않아 변화량을 알 수 없다 — 「새 비커」로 처음 pH부터 측정하자.`;
      else { const dd=Math.abs(p-st.p0[s]);
        st.msg=`${S[s].nm}: 처음 ${st.p0[s].toFixed(2)} → ${txt}, ${dd.toFixed(2)}만큼 변했다 — ${why(s,am,vb>0)}.`+(ok==='—'?'':` 내 예측과 ${ok==='○'?'일치한다':'다르다'}.`); }
      paint(); }
    function add(code){
      st.msg=''; const s=st.s, isB=code[0]==='b', amt=+code.slice(1);
      if(isB&&st.va[s]>0 || !isB&&st.vb[s]>0){ st.vb[s]=0; st.va[s]=0; st.msg='반대 시약이 들어 있어 새 비커에 50 mL를 다시 담았다(교과서 과정 4). '; }
      const cur=isB?st.vb[s]:st.va[s];
      if(cur+amt>VMAX){ st.msg=`한 비커에는 ${VMAX} mL까지 넣는다 — 「새 비커」로 다시 시작하자.`; paint(); return; }
      if(isB) st.vb[s]=cur+amt; else st.va[s]=cur+amt;
      const am=amounts(s,st.vb[s],st.va[s]);
      st.msg+=`${isB?'수산화 나트륨 수용액':'염산'} ${amt} mL를 넣었다(모두 ${cur+amt} mL). 비커 속 입자 변화를 보고 「pH 측정」을 누르자.`+(s===0?'':` (${why(s,am,isB)})`);
      build(); paint(); }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ st.s=+b.dataset.s; st.msg=''; build(); paint(); }));
    root.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{ st.pred=+b.dataset.p; st.msg=''; paint(); }));
    root.querySelectorAll('[data-add]').forEach(b=>b.addEventListener('click',()=>add(b.dataset.add)));
    $('[data-act="meas"]').addEventListener('click',()=>record('meter'));
    $('[data-act="mine"]').addEventListener('click',()=>record('mine'));
    $('[data-act="fresh"]').addEventListener('click',()=>{ st.vb[st.s]=0; st.va[st.s]=0; st.msg=`새 비커에 ${S[st.s].nm} 50 mL를 담았다.`; build(); paint(); });
    $('[data-i="my"]').addEventListener('input',()=>{ O('my').textContent='pH '+(+$('[data-i="my"]').value).toFixed(1); });
    $('[data-act="reset"]').addEventListener('click',()=>{ init(); $('[data-i="my"]').value=7; build(); paint(); });
    API.loop(root,(dt,t)=>{ parts.forEach(q=>{ q.g.setAttribute('transform',`translate(${(q.x+2.5*Math.sin(t*q.w+q.ph)).toFixed(1)},${(q.y+2.5*Math.cos(t*q.w*1.3+q.ph)).toFixed(1)})`); }); });
    init(); build(); paint();
    API.ready(()=>{ build(); paint(); });
  }
};
