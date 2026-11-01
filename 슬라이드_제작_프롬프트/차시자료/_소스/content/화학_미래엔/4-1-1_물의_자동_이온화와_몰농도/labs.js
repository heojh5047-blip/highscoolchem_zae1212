/* 4-1-1 물의 자동 이온화와 몰농도 — 실험실
   cm411kw  : [H3O+]와 [OH-]의 시소 (25 °C, Kw = 1.0×10^-14) — [H3O+] = 1.0×10^-k M, [OH-] = 1.0×10^-(14-k) M
   cm411std : 표준 용액 만들기 (필수 탐구 화04-탐2 「적절한 실험 도구를 사용하여 표준 용액 만들기」)
     · 용질 NaCl 58.5 / 포도당 C6H12O6 180 / CuSO4·5H2O 249.5 g/mol, 목표 몰농도 0.05–0.50 M, 부피 플라스크 100·250·500 mL
     · 7단계: 계산 → 달기(0.01 g 반올림) → 녹이기 → 옮기기 → 씻은 물 → 표선 → 섞기 → 농도 측정
     · 잘못된 조작: 씻은 물 생략(용질 4 % 남음), 표선 넘김(부피 +3 %), 위에서 봄(부피 −1 %), 흔들지 않음(측정값 ±8 %)
     · 측정값 = 실제 몰농도 × (1 + ε), ε 고정 시드 ±0.4 %. 「측정 기록」 → 표 누적(최근 5행), 「초기화」 */
window.DECK_LABS = {
  cm411kw(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Vv=k=>root.querySelector(`[data-v="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg'), X0=96, Y0=30, U=24, YB=Y0+14*U;
    const base=API.mk('g',{},svg);
    // 눈금 (정적)
    API.mk('line',{x1:X0,y1:Y0,x2:X0,y2:YB,stroke:API.COL.muted,'stroke-width':2},base);
    for(let e=0;e<=14;e++){ const y=Y0+e*U; API.mk('line',{x1:X0-(e%2?4:8),y1:y,x2:X0,y2:y,stroke:API.COL.muted,'stroke-width':2},base);
      if(e%2===0) API.texText(base,X0-12,y+7,`10^{${e?'-'+e:'0'}}`,{size:18,anchor:'end',fill:API.COL.muted}); }
    API.mk('line',{x1:X0,y1:Y0+7*U,x2:400,y2:Y0+7*U,stroke:API.COL.muted,'stroke-width':1.6,'stroke-dasharray':'6 5'},base);
    API.texText(base,402,Y0+7*U+6,'\\text{중성}',{size:18,anchor:'start',fill:API.COL.muted});
    API.texText(base,210,YB+26,'[\\ce{H3O+}]',{size:20,anchor:'middle',fill:API.COL.plus});
    API.texText(base,330,YB+26,'[\\ce{OH-}]',{size:20,anchor:'middle',fill:API.COL.minus});
    // 비커
    API.mk('path',{d:'M430,222 L434,230 V352 H540 V230 L544,222',fill:'none',stroke:'#7E8B98','stroke-width':2.6,'stroke-linejoin':'round'},base);
    API.mk('rect',{x:435.5,y:250,width:103,height:100.5,fill:'#F4F9FD'},base);
    API.texText(base,487,214,'\\text{이온 (모식)}',{size:18,anchor:'middle',fill:API.COL.muted});
    const g=API.mk('g',{},svg);
    const barH=API.mk('rect',{x:175,width:70,fill:API.COL.plus,opacity:.85},g);
    const barO=API.mk('rect',{x:295,width:70,fill:API.COL.minus,opacity:.85},g);
    const ions=API.mk('g',{},svg);
    let k=7, hH=7, hO=7;
    const fmt=e=>`1.0\\times10^{-${e}}\\ \\text{M}`;
    const PTS=[[452,268],[478,262],[506,270],[526,292],[500,300],[466,296],[448,326],[476,330],[506,334],[528,322],[488,282],[458,312]];
    function draw(){
      k=+I('k').value; O('k').textContent=`k = ${k}`;
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',+b.dataset.s===k));
      Vv('h').innerHTML=API.tex(fmt(k)); Vv('oh').innerHTML=API.tex(fmt(14-k)); Vv('p').innerHTML=API.tex('1.0\\times10^{-14}');
      const kind=k<7?'산성':k>7?'염기성':'중성'; O('kind').textContent=kind;
      O('kind').style.color=k<7?API.COL.plus:k>7?API.COL.minus:API.COL.ink;
      O('msg').textContent = k===7 ? '두 이온의 농도가 같다 → 중성. 막대 길이의 합은 늘 14칸이다.'
        : `하이드로늄 이온 농도가 수산화 이온 농도보다 ${k<7?'크다':'작다'} → ${kind}. 한쪽이 10배 커지면 다른 쪽은 10배 작아진다 — 곱은 늘 같다.`;
      ions.innerHTML=''; const nH=API.clamp(3+Math.round((7-k)/2),1,6), nO=API.clamp(3+Math.round((k-7)/2),1,6);
      for(let i=0;i<nH+nO;i++){ const [x,y]=PTS[i]; API.charge(ions,x,y,10,i<nH?'+':'-'); }
    }
    function bars(){ barH.setAttribute('y',YB-hH*U); barH.setAttribute('height',hH*U); barO.setAttribute('y',YB-hO*U); barO.setAttribute('height',hO*U); }
    I('k').addEventListener('input',draw);
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ I('k').value=b.dataset.s; draw(); }));
    draw(); hH=14-k; hO=k; bars();
    API.loop(root,dt=>{ const tH=14-k, tO=k; if(Math.abs(hH-tH)<.005&&Math.abs(hO-tO)<.005) return;
      const a=Math.min(1,dt*6); hH+=(tH-hH)*a; hO+=(tO-hO)*a; bars(); });
    if(window.__STILL){ hH=14-k; hO=k; bars(); }
    root.__kwSync=()=>{ hH=14-k; hO=k; bars(); };
  },

  cm411std(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), E=k=>root.querySelector(`[data-e="${k}"]`);
    const svg=$('svg');
    const SOL={NaCl:{tex:'\\ce{NaCl}',mm:58.5,col:'#DDEEF8'},Glc:{tex:'\\ce{C6H12O6}',mm:180,col:'#DDEEF8'},Cu:{tex:'\\ce{CuSO4*5H2O}',mm:249.5,col:'#3E8ED0'}};
    const STEPS=['처음','① 질량 계산','② 저울로 달기','③ 비커에서 녹이기','④ 부피 플라스크로 옮기기','⑤ 씻은 물 옮기기','⑥ 표선까지 물 채우기','⑦ 마개 닫고 섞기'];
    let st={u:'NaCl',V:250,step:0,meas:null,lvl:0,seed:1}, log=[];
    // 고정 시드 난수
    function rnd(){ let t=(st.seed+=0x6D2B79F5); t=Math.imul(t^t>>>15,t|1); t^=t+Math.imul(t^t>>>7,t|61); return ((t^t>>>14)>>>0)/4294967296; }
    // 부피 플라스크 모양
    const FX=448, FB=288, R=68, HW=13, cy=FB-R*.86, yj=cy-Math.sqrt(R*R-HW*HW), hb=Math.sqrt(R*R-(FB-cy)**2), TOP=36, MARK=cy-102;
    const fd=`M${FX-HW},${TOP} L${FX-HW},${yj} A${R},${R} 0 0 0 ${FX-hb},${FB} L${FX+hb},${FB} A${R},${R} 0 0 0 ${FX+HW},${yj} L${FX+HW},${TOP}`;
    const defs=API.mk('defs',{},svg), cp=API.mk('clipPath',{id:'clip-cm411-28'},defs); API.mk('path',{d:fd+' Z'},cp);
    const g=API.mk('g',{},svg);
    const liqG=API.mk('g',{'clip-path':'url(#clip-cm411-28)'},svg);
    const liq=API.mk('rect',{x:FX-R-2,width:2*R+4,fill:'#DDEEF8'},liqG), liqTop=API.mk('rect',{x:FX-R-2,width:2*R+4,fill:'#FFFFFF',opacity:0},liqG);
    const dotsG=API.mk('g',{},liqG);
    API.mk('path',{d:fd,fill:'none',stroke:'#7E8B98','stroke-width':2.6,'stroke-linejoin':'round'},svg);
    API.mk('line',{x1:FX-HW-6,y1:MARK,x2:FX+HW+6,y2:MARK,stroke:API.COL.ink,'stroke-width':2},svg);
    API.texText(svg,FX+HW+10,MARK+6,'\\text{표선}',{size:18,anchor:'start'});
    const top=API.mk('g',{},svg);
    const vol=()=>st.V, mm=()=>SOL[st.u].mm, Mt=()=>+I('M').value;
    const calc=()=>Mt()*vol()/1000*mm(), weighed=()=>Math.round(calc()*100)/100;
    function real(){ const loss=E('wash').checked?.04:0, dv=(E('over').checked?.03:0)-(E('above').checked?.01:0);
      return weighed()/mm()*(1-loss)/(vol()/1000*(1+dv)); }
    function target(){ // 단계별 액면 (플라스크 부피 비율 0–1, 1 = 표선)
      const s=st.step; if(s<4) return 0; if(s===4) return .45; if(s===5) return E('wash').checked?.45:.6;
      return 1+(E('over').checked?.10:0)-(E('above').checked?.05:0); }
    const yOf=f=>{ // 0 = 바닥, 1 = 표선 (부피 대신 높이로 단순화)
      const yBulbTop=cy-R*.75; if(f<=.8) return FB-(FB-yBulbTop)*f/.8; return yBulbTop-(yBulbTop-MARK)*(f-.8)/.2; };
    function scene(){
      g.innerHTML=''; top.innerHTML=''; const s=st.step, u=SOL[st.u];
      // 저울
      API.mk('rect',{x:20,y:200,width:150,height:62,rx:8,fill:'#EEF2F6',stroke:API.COL.ink,'stroke-width':2},g);
      API.mk('rect',{x:53,y:190,width:84,height:10,rx:2,fill:'#C9D3DD',stroke:API.COL.ink,'stroke-width':2},g);
      API.mk('path',{d:'M57,190 L65,180 L125,180 L133,190 Z',fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':2},g);
      API.mk('rect',{x:38,y:216,width:114,height:32,rx:4,fill:'#E3F2E9',stroke:API.COL.ink,'stroke-width':1.5},g);
      if(s===2) API.mk('path',{d:'M77,181 Q95,162 113,181 Z',fill:st.u==='Cu'?'#5FA3DD':'#F4F6F8',stroke:API.COL.muted,'stroke-width':1.5},g);
      Ov('bal').textContent=(s===2?weighed().toFixed(2):'0.00')+' g'; API.place(Ov('bal'),95,232);
      // 비커
      API.mk('path',{d:'M206,196 L210,204 V286 H290 V204 L294,196',fill:'none',stroke:'#7E8B98','stroke-width':2.6,'stroke-linejoin':'round'},g);
      const bl = s===3?232 : (s===4||(s>=5&&E('wash').checked))?280 : s>=5?284:null;
      if(bl) API.mk('rect',{x:211.5,y:bl,width:77,height:284.5-bl,fill:s===3?u.col:'#DDEEF8',opacity:s===3&&st.u==='Cu'?.55:1},g);
      if(s===3||(s>=4&&E('wash').checked)){ const n=s===3?7:2; for(let i=0;i<n;i++) API.mk('circle',{cx:222+i*10,cy:s===3?250+(i%3)*12:281,r:3.5,fill:API.COL.equi,opacity:.8},g); }
      if(s===3) API.mk('line',{x1:240,y1:150,x2:262,y2:280,stroke:'#7E8B98','stroke-width':5,'stroke-linecap':'round'},g);
      if(s===3) API.texText(g,250,140,'\\text{녹이기}',{size:18,anchor:'middle',fill:API.COL.muted});
      // 깔때기·씻기병·스포이트·마개
      if(s===4||s===5) API.mk('path',{d:`M${FX-26},14 L${FX+26},14 L${FX+5},40 L${FX+5},60 L${FX-5},60 L${FX-5},40 Z`,fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':2.2},top);
      if(s===5&&!E('wash').checked){ API.mk('rect',{x:330,y:40,width:40,height:52,rx:8,fill:'#EEF6FB',stroke:'#7E8B98','stroke-width':2.2},top);
        API.mk('path',{d:'M350,40 V28 H378 L392,40',fill:'none',stroke:'#7E8B98','stroke-width':3,'stroke-linecap':'round'},top);
        API.mk('path',{d:'M394,42 Q410,40 424,22',fill:'none',stroke:'#9FC3DD','stroke-width':3,'stroke-dasharray':'5 4'},top); }
      if(s===5&&E('wash').checked) API.texText(top,350,80,'\\text{씻은 물 생략}',{size:18,anchor:'middle',fill:API.COL.plus});
      if(s===6){ API.mk('rect',{x:FX-6,y:2,width:12,height:30,rx:3,fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':2},top);
        if(E('above').checked){ API.mk('path',{d:'M352,72 Q368,60 384,72 Q368,84 352,72 Z',fill:'#FFFFFF',stroke:API.COL.ink,'stroke-width':2},top); API.mk('line',{x1:388,y1:76,x2:FX-HW,y2:MARK,stroke:API.COL.muted,'stroke-width':1.4,'stroke-dasharray':'4 4'},top); }
        else { API.mk('path',{d:`M352,${MARK} Q368,${MARK-12} 384,${MARK} Q368,${MARK+12} 352,${MARK} Z`,fill:'#FFFFFF',stroke:API.COL.ink,'stroke-width':2},top); API.mk('line',{x1:388,y1:MARK,x2:FX-HW-8,y2:MARK,stroke:API.COL.muted,'stroke-width':1.4,'stroke-dasharray':'4 4'},top); } }
      if(s===7) API.mk('rect',{x:FX-HW-3,y:TOP-14,width:2*HW+6,height:16,rx:3,fill:'#C9D3DD',stroke:'#7E8B98','stroke-width':2},top);
      // 용액 색
      const M=real(), cu=st.u==='Cu';
      liq.setAttribute('fill',cu?u.col:'#DDEEF8'); liq.setAttribute('opacity',cu?API.clamp(.18+M*1.4,.2,.92):1);
      const unmixed = s>=6 && (s===6 || E('mix').checked);
      liqTop.setAttribute('opacity', unmixed? .55:0);
      dotsG.innerHTML=''; if(!cu && s>=4){ const n=Math.round(API.clamp(M*40,3,14)); for(let i=0;i<n;i++){ const a=i*2.4, rr=12+((i*37)%46);
        API.mk('circle',{cx:FX+Math.cos(a)*rr, cy:(unmixed? FB-14-((i*13)%26) : cy+Math.sin(a)*rr*.75), r:4,fill:API.COL.equi,opacity:.85},dotsG); } }
      Ov('stage').textContent=STEPS[s]+(s<7?`  (${s}/7)`:'  (7/7) — 농도를 측정하자'); API.place(Ov('stage'),280,14);
      // 버튼·출력
      $('[data-act="next"]').disabled = s>=7; $('[data-act="measure"]').disabled = s<7; $('[data-act="rec"]').disabled = st.meas==null;
      O('calc').textContent = s>=1 ? `${(Mt()*vol()/1000).toFixed(4).replace(/0+$/,'').replace(/\.$/,'')} mol · ${calc().toFixed(3)} g` : '— (다음 단계 ▶)';
      O('meas').textContent = st.meas==null ? '—' : `${st.meas.toPrecision(3)} M`;
      O('M').textContent=Mt().toFixed(2)+' M';
      root.querySelectorAll('[data-u]').forEach(b=>b.classList.toggle('on',b.dataset.u===st.u));
      root.querySelectorAll('[data-v]').forEach(b=>b.classList.toggle('on',+b.dataset.v===st.V));
    }
    function lvl(){ const y=yOf(st.lvl); liq.setAttribute('y',y); liq.setAttribute('height',FB-y+2); liqTop.setAttribute('y',y); liqTop.setAttribute('height',Math.max(0,(FB-y)*.45)); }
    function msgFor(){
      const err=[]; if(E('wash').checked) err.push('씻은 물을 넣지 않아 비커에 용질이 남았다(용질의 양 감소)');
      if(E('over').checked) err.push('표선을 넘겨 용액의 부피가 커졌다'); if(E('above').checked) err.push('표선을 위에서 보아 물이 덜 채워졌다(부피 감소)');
      const d=(real()/Mt()-1)*100;
      let m = err.length? err.join(', ')+` → 몰농도가 목표보다 ${d<0?'작다':'크다'}.` : '바른 조작 — 목표 몰농도와 거의 같다(측정 오차 수준).';
      if(E('mix').checked) m+=' 흔들지 않아 위아래 농도가 달라 잴 때마다 값이 크게 달라진다.';
      return m; }
    function reset(){ st.step=0; st.meas=null; st.lvl=0; lvl(); scene(); O('msg').textContent='목표를 정하고 「다음 단계 ▶」로 표준 용액을 만들어 보자. 잘못된 조작을 골라 비교할 수도 있다.'; }
    $('[data-act="next"]').addEventListener('click',()=>{ if(st.step>=7) return; st.step++; st.meas=null; scene();
      if(st.step===1) O('msg').textContent=`n = MV = ${Mt().toFixed(2)} M × ${(vol()/1000).toFixed(3)} L, 질량 = n × ${mm()} g/mol`;
      else if(st.step===2) O('msg').textContent=`전자저울은 0.01 g까지 → ${weighed().toFixed(2)} g을 단다.`;
      else if(st.step===7) O('msg').textContent='마개를 닫고 뒤집어 섞었다. 「농도 측정」을 누르자.';
      else O('msg').textContent=STEPS[st.step]+'.'; if(window.__STILL){ st.lvl=target(); lvl(); } });
    $('[data-act="measure"]').addEventListener('click',()=>{ if(st.step<7) return; const sp=E('mix').checked?.08:.004;
      st.meas=real()*(1+(rnd()*2-1)*sp); scene(); O('msg').textContent=msgFor(); });
    function renderLog(){ const tb=O('log'); tb.innerHTML=''; log.forEach(r=>{ const tr=document.createElement('tr');
      tr.innerHTML=`<td>${API.tex(r.tex)}</td><td>${r.M}</td><td>${r.w}</td><td>${r.op}</td><td>${r.m}</td><td>${r.e}</td>`; tb.appendChild(tr); }); }
    $('[data-act="rec"]').addEventListener('click',()=>{ if(st.meas==null) return;
      const ops=[['wash','씻은 물 ×'],['over','표선 넘김'],['above','위에서 봄'],['mix','안 흔듦']].filter(([k])=>E(k).checked).map(x=>x[1]);
      const e=(st.meas/Mt()-1)*100;
      log.push({tex:SOL[st.u].tex,M:Mt().toFixed(2)+' M',w:weighed().toFixed(2)+' g',op:ops.join(', ')||'바름',m:st.meas.toPrecision(3)+' M',e:(e>=0?'+':'−')+Math.abs(e).toFixed(1)+' %'});
      if(log.length>5) log.shift(); renderLog(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); st.u='NaCl'; st.V=250; I('M').value=.1; st.seed=1;
      ['wash','over','above','mix'].forEach(k=>E(k).checked=false); reset(); });
    root.querySelectorAll('[data-u]').forEach(b=>b.addEventListener('click',()=>{ st.u=b.dataset.u; reset(); }));
    root.querySelectorAll('[data-v]').forEach(b=>b.addEventListener('click',()=>{ st.V=+b.dataset.v; reset(); }));
    I('M').addEventListener('input',reset);
    ['wash','over','above','mix'].forEach(k=>E(k).addEventListener('change',()=>{ scene(); if(st.meas!=null) O('msg').textContent=msgFor(); }));
    reset();
    API.loop(root,dt=>{ const t=target(); if(Math.abs(st.lvl-t)<.002) return; st.lvl+=(t-st.lvl)*Math.min(1,dt*3); lvl(); });
  }
};
