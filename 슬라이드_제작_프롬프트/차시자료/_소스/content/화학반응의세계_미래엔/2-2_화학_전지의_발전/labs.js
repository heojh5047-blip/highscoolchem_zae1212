/* 2-2 화학 전지의 발전 — 실험실
   rm22cell : 실용 전지 탐색기 (자료실 — 해 보기 「화학 전지의 발전 과정 조사하기」를 돕는 도구, S11)
     · 전지 8개 버튼 → 분류·개발 시기·(−)극(산화 전극)·(+)극(환원 전극)·전해질·쓰임 표시, 그림의 극 물질·전해질 바뀜
     · 전자 점은 (−)극 → 도선 → (+)극으로 계속 흐르고(API.loop), 전해질 속 양이온은 (+)극 쪽, 음이온은 (−)극 쪽으로 이동
     · 「조사 기록」→ 기록 표에 행이 쌓임(최근 5행), 서로 다른 전지 3가지 이상이면 공통 구조 문장 · 「초기화」 기록 지움 */
window.DECK_LABS = {
  rm22cell(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const B={
      volta:  {nm:'볼타 전지', cls:'초기 화학 전지', yr:'1800년', neg:'아연', nt:'\\ce{Zn}', pos:'구리', pt:'\\ce{Cu}', el:'산 용액(헝겊)', et:'산 용액을 적신 헝겊', use:'전기 실험', nc:'#C9D3DD', pc:'#E6C29C', ec:'#EFE6C8', ion:'both'},
      daniell:{nm:'다니엘 전지', cls:'초기 화학 전지', yr:'1836년', neg:'아연', nt:'\\ce{Zn}', pos:'구리', pt:'\\ce{Cu}', el:'황산 아연·황산 구리(II) 수용액, 염다리', et:'\\ce{ZnSO4(aq)} | 염다리 | \\ce{CuSO4(aq)}', use:'전신(통신)', nc:'#C9D3DD', pc:'#E6C29C', ec:'#DDEEF8', ion:'both'},
      lead:   {nm:'납축전지', cls:'이차 전지', yr:'1859년', neg:'납', nt:'\\ce{Pb}', pos:'이산화 납', pt:'\\ce{PbO2}', el:'묽은 황산', et:'묽은 황산 \\ce{H2SO4(aq)}', use:'자동차 시동·조명', nc:'#8C99A6', pc:'#5A3B2E', ec:'#DDEEF8', ion:'both'},
      mn:     {nm:'망가니즈 건전지', cls:'일차 전지', yr:'1866년', neg:'아연', nt:'\\ce{Zn}', pos:'이산화 망가니즈', pt:'\\ce{MnO2}', el:'염화 암모늄 반죽', et:'\\ce{NH4Cl} 반죽', use:'손전등, 리모컨', nc:'#C9D3DD', pc:'#3D3A36', ec:'#EFE6C8', ion:'both'},
      button: {nm:'단추형 전지(산화 은)', cls:'일차 전지', yr:'1947년(수은 전지)', neg:'아연', nt:'\\ce{Zn}', pos:'산화 은', pt:'\\ce{Ag2O}', el:'수산화 칼륨 수용액', et:'\\ce{KOH} 수용액', use:'손목시계', nc:'#C9D3DD', pc:'#6B6F75', ec:'#EFE6C8', ion:'both'},
      nimh:   {nm:'니켈·금속 수소화물 전지', cls:'이차 전지', yr:'1970년', neg:'수소 저장 합금', nt:'수소 저장 합금', pos:'수산화 산화 니켈', pt:'\\ce{NiOOH}', el:'수산화 칼륨 수용액', et:'\\ce{KOH} 수용액', use:'휴대용 기기, 캠코더', nc:'#AEB8C2', pc:'#556B4E', ec:'#DDEEF8', ion:'both'},
      li:     {nm:'리튬 이온 전지', cls:'이차 전지', yr:'1985년', neg:'흑연', nt:'흑연 \\ce{C}', pos:'리튬 금속 산화물', pt:'\\ce{LiCoO2} 등', el:'리튬 염 + 유기 용매', et:'리튬 염 + 유기 용매 (\\ce{Li+} 이동)', use:'스마트폰, 노트북, 전기 자동차', nc:'#4A4F57', pc:'#7D8FA6', ec:'#E8EEF6', ion:'cat'},
      fuel:   {nm:'수소 연료 전지', cls:'연료 전지', yr:'1960년대', neg:'수소 공급 전극', nt:'\\ce{H2} 공급', pos:'산소 공급 전극', pt:'\\ce{O2} 공급', el:'수소 이온이 이동하는 전해질', et:'전해질 (\\ce{H+} 이동)', use:'우주선, 수소 자동차', nc:'#4A4F57', pc:'#4A4F57', ec:'#EFE6C8', ion:'cat'}
    };
    const svg=$('svg'), gs=API.mk('g',{},svg), gd=API.mk('g',{},svg), gi=API.mk('g',{},svg), ge=API.mk('g',{},svg), gw=API.mk('g',{},svg);
    let cur='volta', log=[], t0=0;
    const W=(t,a,g)=>API.mk(t,a,g||gs);
    // 고정 부분: 도선·전구·전자 이동 화살표 (D1·D28 — 전자 화살표는 도선 위 minus)
    W('path',{d:'M140 92 V44 H262 M298 44 H420 V92',fill:'none',stroke:API.COL.ink,'stroke-width':3,'stroke-linejoin':'round'});
    W('circle',{cx:280,cy:44,r:32,fill:'#FFE45C',opacity:.55});
    W('circle',{cx:280,cy:44,r:18,fill:'#FFFFFF',stroke:API.COL.ink,'stroke-width':3});
    W('line',{x1:267,y1:31,x2:293,y2:57,stroke:API.COL.ink,'stroke-width':2.4}); W('line',{x1:267,y1:57,x2:293,y2:31,stroke:API.COL.ink,'stroke-width':2.4});
    API.arrow(gs,166,30,232,30,API.COL.minus,3); API.arrow(gs,328,30,394,30,API.COL.minus,3);
    API.place(V('e1'),199,0); API.place(V('e2'),361,0);
    API.place(V('pn'),140,262); API.place(V('pp'),420,262);
    // 전자 점: (−)극 위 → 도선 → (+)극 위 (경로 길이 기준)
    const P=[[140,92],[140,44],[420,44],[420,92]];
    const seg=[48,280,48], LEN=376;
    function at(s){ s=((s%LEN)+LEN)%LEN; if(s<seg[0]) return [140,92-s]; s-=seg[0]; if(s<seg[1]) return [140+s,44]; s-=seg[1]; return [420,44+s]; }
    const dots=[]; for(let i=0;i<12;i++) dots.push(W('circle',{r:5,fill:API.COL.minus},ge));
    // 이온 (전해질 안)
    const IONS=[{s:'+',x:190,y:128},{s:'+',x:300,y:158},{s:'+',x:240,y:186},{s:'-',x:350,y:132},{s:'-',x:220,y:160},{s:'-',x:330,y:186}];
    const ionG=IONS.map(o=>{ const g=API.mk('g',{},gi); API.charge(g,0,0,8,o.s); return g; });
    function drawIons(t){
      const kind=B[cur].ion;
      IONS.forEach((o,i)=>{ const g=ionG[i];
        if(kind==='cat' && o.s==='-'){ g.setAttribute('display','none'); return; }
        g.removeAttribute('display');
        const span=200, base=o.x-180, d=(o.s==='+'?1:-1)*t*14;   // 양이온 → (+)극, 음이온 → (−)극
        const x=180+(((base+d)%span)+span)%span;
        g.setAttribute('transform',`translate(${x} ${o.y})`); });
    }
    function drawDots(t){ dots.forEach((c,i)=>{ const [x,y]=at(i*(LEN/12)+t*40); const hide=(x>262&&x<298&&y===44); c.setAttribute('cx',x); c.setAttribute('cy',y); c.setAttribute('opacity',hide?0:1); }); }
    function draw(){
      const b=B[cur];
      while(gd.firstChild) gd.firstChild.remove(); while(gw.firstChild) gw.firstChild.remove();
      const D=(t,a)=>API.mk(t,a,gd);
      D('rect',{x:70,y:102,width:420,height:124,rx:10,fill:b.ec,stroke:'#9AA5B1','stroke-width':2});
      D('rect',{x:124,y:92,width:32,height:124,rx:3,fill:b.nc,stroke:API.COL.ox,'stroke-width':3});
      D('rect',{x:404,y:92,width:32,height:124,rx:3,fill:b.pc,stroke:API.COL.rd,'stroke-width':3});
      if(cur==='daniell'){ D('line',{x1:280,y1:104,x2:280,y2:192,stroke:'#B9A98A','stroke-width':10}); }
      if(cur==='fuel'){
        API.arrow(gw,6,128,118,128,API.COL.ink,3); API.arrow(gw,554,128,442,128,API.COL.ink,3);
        V('g1').innerHTML=API.tex('\\ce{H2}'); V('g2').innerHTML=API.tex('\\ce{O2}');
        API.place(V('g1'),44,110); API.place(V('g2'),516,110);
      } else { API.place(V('g1'),0,0,false); API.place(V('g2'),0,0,false); }
      const mix=s=>s.replace(/\\ce\{[^}]*\}/g,m=>API.tex(m));
      V('mn').innerHTML=mix(b.nt); V('mp').innerHTML=mix(b.pt); V('me').innerHTML=mix(b.et);
      API.place(V('mn'),140,230); API.place(V('mp'),420,230); API.place(V('me'),280,198);
      O('cls').textContent=b.cls; O('yr').textContent=b.yr; O('neg').textContent=b.neg; O('pos').textContent=b.pos; O('el').textContent=b.el; O('use').textContent=b.use;
      if(!O('msg').dataset.keep) O('msg').textContent=`${b.nm}: 방전할 때 (−)극(${b.neg})에서 산화, (+)극(${b.pos})에서 환원이 일어나고, 전자는 도선을, 이온은 전해질을 지난다.`;
      root.querySelectorAll('[data-b]').forEach(x=>x.classList.toggle('on',x.dataset.b===cur));
      const t=window.__STILL?0:(performance.now()/1000-t0); drawIons(t); drawDots(t);
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-5).forEach(k=>{ const b=B[k], tr=document.createElement('tr'); tr.innerHTML=`<td>${b.nm}</td><td>${b.cls}</td><td>${b.neg}</td><td>${b.pos}</td><td>${b.el}</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-b]').forEach(x=>x.addEventListener('click',()=>{ cur=x.dataset.b; delete O('msg').dataset.keep; draw(); }));
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{
      log.push(cur); renderLog();
      const n=new Set(log).size, m=O('msg');
      m.textContent = n>=3 ? `기록한 ${n}가지 전지 모두 (−)극(산화 전극), (+)극(환원 전극), 전해질로 이루어져 있다 — 극의 물질과 전해질만 다르다.`
                           : `기록한 전지 ${n}가지 — 다른 전지도 골라 기록해 보자 (${n}/3).`;
      m.dataset.keep='1'; });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); cur='volta'; delete O('msg').dataset.keep; draw(); });
    API.onShow&&API.onShow(()=>draw());
    draw();
    if(!window.__STILL) API.loop(root,(dt,t)=>{ const s=performance.now()/1000-t0; drawIons(s); drawDots(s); });
  }
};
