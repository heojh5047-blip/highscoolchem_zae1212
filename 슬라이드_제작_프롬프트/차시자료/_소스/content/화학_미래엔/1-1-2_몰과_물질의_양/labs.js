/* 1-1-2 몰과 물질의 양 — 실험실
   cm112mass : 필수 탐구 화01-탐1 「다양한 물질의 몰질량을 탐색하고, 특정한 몰수에 해당하는 물질의 질량 측정하기」
     · 물질 6가지(교과서 탐구 물질) → 몰질량과 그 구성 식
     · 물질의 양 n (0.05–1.00 mol) → 필요한 질량 w = n × M, 입자 수 N = n × 6.02×10^23
     · 「영점 맞추기」 → 저울 0.00 g / 「덜어 담기」 → 1.6초 동안 더미가 자라며 저울 값이 오름
       저울 값 = (영점 안 했으면 용기 질량) + w + ε  (|ε| ≤ 0.03 g, 물질·양으로 정해지는 고정 시드)
     · 「측정 기록」 → 결과 표에 행이 쌓임(최근 6행), 「초기화」 */
window.DECK_LABS = {
  cm112mass(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const S={
      C:   {nm:'탄소', f:'\\ce{C}', M:12, rho:2.2, cont:'dish', col:'#3A3F47', st:'#1C1F24', mm:'\\ce{C}\\text{: }12\\ \\text{g/mol}', zc:'탄소 원자'},
      Cu:  {nm:'구리', f:'\\ce{Cu}', M:63.5, rho:8.96, cont:'dish', col:'#C8803A', st:'#8A5221', mm:'\\ce{Cu}\\text{: }63.5\\ \\text{g/mol}', zc:'구리 원자'},
      H2O: {nm:'물', f:'\\ce{H2O}', M:18, rho:1.00, cont:'beaker', col:'#CFE6F6', st:'#9FC3DD', mm:'\\ce{H2O}\\text{: }2\\times1+16=18\\ \\text{g/mol}', zc:'물 분자'},
      NaCl:{nm:'염화 나트륨', f:'\\ce{NaCl}', M:58.5, rho:2.16, cont:'dish', col:'#FFFFFF', st:'#9AA5B1', mm:'\\ce{NaCl}\\text{: }23+35.5=58.5\\ \\text{g/mol}', zc:'Na+Cl'},
      Glu: {nm:'포도당', f:'\\ce{C6H12O6}', M:180, rho:1.54, cont:'dish', col:'#FFFFFF', st:'#9AA5B1', mm:'\\ce{C6H12O6}\\text{: }6\\times12+12\\times1+6\\times16=180\\ \\text{g/mol}', zc:'포도당 분자'},
      EtOH:{nm:'에탄올', f:'\\ce{C2H5OH}', M:46, rho:0.79, cont:'beaker', col:'#EEF6FB', st:'#B9D3E6', mm:'\\ce{C2H5OH}\\text{: }2\\times12+6\\times1+16=46\\ \\text{g/mol}', zc:'에탄올 분자'}
    };
    const TARE={dish:32.40, beaker:48.60}, NA=6.02;
    const svg=$('svg');
    // ── 고정 그림: 저울·확대 원 ──
    const back=API.mk('g',{},svg);
    API.mk('rect',{x:40,y:228,width:260,height:60,rx:12,fill:'#E9EEF3',stroke:'#16233D','stroke-width':2.5},back);
    API.mk('rect',{x:98,y:240,width:144,height:38,rx:6,fill:'#1F2A3C'},back);
    API.mk('rect',{x:70,y:216,width:200,height:12,rx:4,fill:'#C9D3DD',stroke:'#16233D','stroke-width':2},back);
    API.mk('line',{x1:282,y1:196,x2:372,y2:176,stroke:'#5B6B7F','stroke-width':2,'stroke-dasharray':'6 5'},back);
    API.mk('circle',{cx:470,cy:140,r:102,fill:'#FFFFFF',stroke:'#5B6B7F','stroke-width':2.5},back);
    // 용기와 시료
    const dish=API.mk('g',{},svg), beak=API.mk('g',{},svg);
    API.mk('ellipse',{cx:170,cy:206,rx:86,ry:11,fill:'#F4F8FC',stroke:'#7E8B98','stroke-width':2.5},dish);
    const pile=API.mk('path',{d:'',stroke:'#9AA5B1','stroke-width':1.5},svg);
    const liq=API.mk('rect',{x:124,y:214,width:92,height:0},beak);
    API.mk('path',{d:'M120 118 V214 H220 V118',fill:'none',stroke:'#7E8B98','stroke-width':3},beak);
    for(let j=0;j<4;j++) API.mk('line',{x1:120,y1:134+j*20,x2:132,y2:134+j*20,stroke:'#5B6B7F','stroke-width':1.5},beak);
    // 확대 입자 모형 (처음에 모두 만들어 두고 보이기만 바꾼다 — 원자 라벨 KaTeX 때문)
    const Z={}; const zg=k=>{ Z[k]=API.mk('g',{style:'display:none'},svg); return Z[k]; };
    const hexPts=(d)=>[[0,0]].concat([0,60,120,180,240,300].map(a=>[d*Math.cos(a*Math.PI/180),d*Math.sin(a*Math.PI/180)]));
    zg('C'); hexPts(50).forEach(([x,y])=>API.atom(Z.C,470+x,140+y,24,'C'));
    zg('Cu'); hexPts(58).forEach(([x,y])=>API.atom(Z.Cu,470+x,140+y,28,'Cu'));
    zg('H2O'); [[430,105,0],[515,120,40],[465,185,-30]].forEach(([x,y,r])=>{ const d=32.8;
      [142.25,37.75].forEach(a=>{ const t=(a+r)*Math.PI/180; API.atom(Z.H2O,x+d*Math.cos(t),y+d*Math.sin(t),18,'H'); }); API.atom(Z.H2O,x,y,24,'O'); });
    zg('NaCl'); for(let r=0;r<3;r++) for(let c=0;c<3;c++){ const na=(r+c)%2===0; API.atom(Z.NaCl,416+c*54,86+r*54,na?19:32,na?'Na':'Cl','-'); }
    const blob=(g,x,y)=>{ API.mk('ellipse',{cx:x,cy:y,rx:62,ry:36,fill:'#F7F9FB',stroke:'#9AA5B1','stroke-width':2,'stroke-dasharray':'5 4'},g); };
    zg('Glu'); [[470,96],[470,186]].forEach(([x,y])=>{ blob(Z.Glu,x,y);
      [[-30,-8],[-10,-14],[10,-8],[30,-14],[-20,10],[20,10]].forEach(([dx,dy])=>API.atom(Z.Glu,x+dx,y+dy,10,'C','-'));
      [[-44,6],[0,16],[44,0],[-2,-26]].forEach(([dx,dy])=>API.atom(Z.Glu,x+dx,y+dy,10,'O','-')); });
    zg('EtOH'); [[470,96],[470,186]].forEach(([x,y])=>{ blob(Z.EtOH,x,y);
      [[-34,-6],[-34,18],[-50,4],[-2,-20],[-2,20],[42,-16]].forEach(([dx,dy])=>API.atom(Z.EtOH,x+dx,y+dy,9,'H','-'));
      [[-22,4],[4,0]].forEach(([dx,dy])=>API.atom(Z.EtOH,x+dx,y+dy,15,'C','-')); API.atom(Z.EtOH,x+28,y-4,14,'O','-'); });

    let st={k:'C', tared:false, phase:0, t:0, eps:0, read:0}, log=[];
    const nOf=()=>+I('n').value*0.05;
    const f2=v=>v.toFixed(2);
    const sci=v=>{ const e=Math.floor(Math.log10(v)+1e-9); const m=v/Math.pow(10,e); return {m:m.toFixed(2), e}; };
    const seed=(k,n)=>{ let h=0; for(const ch of k+n.toFixed(2)) h=(h*31+ch.charCodeAt(0))%9973; return ((h%61)-30)/1000; };   // −0.030 ~ +0.030
    function setSub(k){ st.k=k; st.tared=false; st.phase=0; st.t=0;
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===k)); draw(); }
    function calc(){ const s=S[st.k], n=nOf(), w=n*s.M; return {s,n,w,N:n*NA}; }
    function draw(){
      const {s,n,w}=calc(), u=st.phase===2?1:st.phase===1?(1-Math.pow(1-st.t,2)):0;
      O('n').textContent=n.toFixed(2)+' mol';
      O('M').textContent=(s.M%1?s.M.toFixed(1):s.M)+' g/mol';
      O('w').textContent=f2(w)+' g';
      // 용기
      const isB=s.cont==='beaker'; dish.style.display=isB?'none':''; beak.style.display=isB?'':'none';
      const V=w/s.rho*u;     // mL
      if(isB){ const h=Math.min(92,V/60*92); liq.setAttribute('y',(214-h).toFixed(1)); liq.setAttribute('height',h.toFixed(1)); liq.setAttribute('fill',s.col); pile.setAttribute('d',''); }
      else { const sz=u>0?Math.min(80,8+15*Math.cbrt(V)):0, h=sz*0.62;
        pile.setAttribute('d',sz?`M${170-sz} 205 Q170 ${(205-2*h).toFixed(1)} ${170+sz} 205 Z`:''); pile.setAttribute('fill',s.col); pile.setAttribute('stroke',s.st); }
      // 저울 값
      const tare=st.tared?0:TARE[s.cont];
      st.read=tare+(w+st.eps)*u;
      Ov('disp').textContent=f2(st.read)+' g'; API.place(Ov('disp'),170,242);
      // 확대 원
      Object.keys(Z).forEach(k=>Z[k].style.display=k===st.k?'':'none');
      Ov('f').innerHTML='확대: '+(st.k==='NaCl'?API.tex('\\ce{Na+}')+'(작은 공)과 '+API.tex('\\ce{Cl-}'):s.zc); API.place(Ov('f'),470,272);
      const N=sci(n*6.02e23);
      Ov('N').innerHTML='입자 수 '+API.tex(`${N.m}\\times10^{${N.e}}`)+'개'+(st.k==='NaCl'?' (화학식 단위)':''); API.place(Ov('N'),470,246);
      Ov('mm').innerHTML=API.tex(s.mm); API.place(Ov('mm'),12,8);
      const m=O('msg');
      if(st.phase===0) m.textContent=st.tared?`영점을 맞췄다. 「덜어 담기」로 ${f2(w)} g을 담자.`:`${s.cont==='dish'?'페트리 접시':'비커'}를 올렸다. 먼저 「영점 맞추기」를 누르자.`;
      else if(st.phase===1) m.textContent='덜어 담는 중…';
      else if(!st.tared) m.textContent=`영점을 맞추지 않아 용기 질량 ${f2(TARE[s.cont])} g이 함께 읽혔다. 물질을 다시 골라 영점부터 하자.`;
      else m.textContent=`계산값 ${f2(w)} g, 측정값 ${f2(st.read)} g (차이 ${(()=>{ const d=+f2(st.read)-+f2(w); return (d>=0?'+':'')+d.toFixed(2); })()} g). 같은 ${n.toFixed(2)} mol이면 입자 수는 물질과 관계없이 같다.`;
    }
    function renderLog(){
      O('log').innerHTML=log.slice(-6).map(r=>`<tr><td>${r.nm}</td><td>${r.M}</td><td>${r.n}</td><td>${r.w}</td><td>${r.read}</td><td>${API.tex(r.N)}</td><td>${r.tared?'○':'×'}</td></tr>`).join('')
        || '<tr><td colspan="7" class="c-muted">덜어 담은 뒤 「측정 기록」을 누르면 여기에 쌓인다.</td></tr>';
    }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>setSub(b.dataset.s)));
    I('n').addEventListener('input',()=>{ st.phase=0; st.t=0; draw(); });
    $('[data-act="tare"]').addEventListener('click',()=>{ if(st.phase!==0){ O('msg').textContent='용기를 비운 상태에서 영점을 맞춘다. 물질을 다시 고르자.'; return; } st.tared=true; draw(); });
    $('[data-act="pour"]').addEventListener('click',()=>{ const {n}=calc(); st.eps=seed(st.k,n); st.phase=1; st.t=0; draw(); });
    $('[data-act="rec"]').addEventListener('click',()=>{
      if(st.phase!==2){ O('msg').textContent='먼저 「덜어 담기」를 끝낸 뒤 기록하자.'; return; }
      const {s,n,w}=calc(), N=sci(n*6.02e23);
      log.push({nm:s.nm, M:(s.M%1?s.M.toFixed(1):s.M), n:n.toFixed(2), w:f2(w), read:f2(st.read), N:`${N.m}\\times10^{${N.e}}`, tared:st.tared}); renderLog();
    });
    $('[data-act="reset"]').addEventListener('click',()=>{ I('n').value=2; log=[]; renderLog(); setSub('C'); });
    API.loop(root,dt=>{ if(st.phase!==1) return; st.t+=dt/1.6; if(st.t>=1){ st.t=1; st.phase=2; } draw(); });
    API.ready(()=>{ renderLog(); draw(); });
    renderLog(); setSub('C');
  }
};
