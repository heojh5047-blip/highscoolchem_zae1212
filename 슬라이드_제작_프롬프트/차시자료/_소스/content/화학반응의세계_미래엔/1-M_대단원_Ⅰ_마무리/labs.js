/* 1-M 대단원 Ⅰ 마무리 — 실험실
   rm19breath : 과학 글쓰기 11 — 호흡 빠르기와 혈액의 pH (덱이 만든 단순 모형)
     · CO2 생성 g: 휴식 1, 달리기 2 · 혈액 CO2 상대값 c = 100·g·12/r (%), 15–250 %
     · [HCO3-] 일정 가정 → pH = 7.40 − log10(c/100)
     · 판정: < 7.35 산증 쪽, 7.35–7.45 정상, > 7.45 알칼리증 쪽
     · 「기록」 → 표 최대 5행, 「초기화」 → 휴식 12회 */
window.DECK_LABS = {
  rm19breath(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=$('svg'), iR=$('[data-i="r"]');
    const FW='#2E9E6A', RV='#7B4FC8';
    let act='rest', log=[], cur=null;
    // ── 폐 ──
    API.mk('line',{x1:110,y1:28,x2:110,y2:92,stroke:'#C97A7A','stroke-width':12,'stroke-linecap':'round'},svg);
    const lungs=API.mk('g',{},svg);
    const L1=API.mk('ellipse',{cx:72,cy:150,rx:36,ry:62,fill:'#F7C9C9',stroke:'#C25A5A','stroke-width':3},lungs);
    const L2=API.mk('ellipse',{cx:148,cy:150,rx:36,ry:62,fill:'#F7C9C9',stroke:'#C25A5A','stroke-width':3},lungs);
    API.mk('path',{d:'M110 90 L80 112 M110 90 L140 112',stroke:'#C97A7A','stroke-width':7,fill:'none','stroke-linecap':'round'},svg);
    API.texText(svg,110,250,'폐',{size:19,anchor:'middle',fill:'#5B6B7F',mix:true});
    API.texText(svg,110,276,'날숨 $\\ce{CO2}$ ↑',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    const dots=[0,1,2,3,4,5].map(k=>API.mk('circle',{cx:110,cy:20,r:6,fill:'#8C99A6'},svg));
    // ── 평형 ──
    API.texText(svg,330,66,'① $\\ce{CO2 + H2O}$',{size:20,anchor:'middle',mix:true});
    API.texText(svg,540,66,'$\\ce{H2CO3}$',{size:20,anchor:'middle',mix:true});
    API.texText(svg,320,146,'② $\\ce{H2CO3 + H2O}$',{size:20,anchor:'middle',mix:true});
    API.texText(svg,562,146,'$\\ce{HCO3- + H3O+}$',{size:20,anchor:'middle',mix:true});
    API.texText(svg,475,26,'정반응',{size:18,anchor:'middle',fill:FW,mix:true});
    API.texText(svg,475,188,'역반응',{size:18,anchor:'middle',fill:RV,mix:true});
    const ga=API.mk('g',{},svg);
    // ── pH 계기 ──
    const X0=250, X1=620, px=p=>X0+(Math.max(7,Math.min(7.8,p))-7)/0.8*(X1-X0), GY=226;
    API.mk('rect',{x:X0,y:GY,width:px(7.35)-X0,height:20,fill:'#F7C9C9'},svg);
    API.mk('rect',{x:px(7.35),y:GY,width:px(7.45)-px(7.35),height:20,fill:'#BFE6CF'},svg);
    API.mk('rect',{x:px(7.45),y:GY,width:X1-px(7.45),height:20,fill:'#C9DDF6'},svg);
    API.mk('rect',{x:X0,y:GY,width:X1-X0,height:20,fill:'none',stroke:'#5B6B7F','stroke-width':1.5},svg);
    [7.0,7.2,7.4,7.6,7.8].forEach(v=>{ API.mk('line',{x1:px(v),y1:GY+20,x2:px(v),y2:GY+27,stroke:'#5B6B7F','stroke-width':1.5},svg);
      API.texText(svg,px(v),GY+48,v.toFixed(1),{size:18,anchor:'middle',mix:true}); });
    API.texText(svg,X0+40,GY-10,'산증',{size:18,anchor:'middle',fill:'#D7263D',mix:true});
    API.texText(svg,X1-50,GY-10,'알칼리증',{size:18,anchor:'middle',fill:'#1F6FD1',mix:true});
    API.texText(svg,X0-8,GY+17,'pH',{size:19,anchor:'end',mix:true});
    const needle=API.mk('path',{d:'',fill:'#16233D'},svg);
    function calc(){ const r=+iR.value, g=act==='run'?2:1; let c=100*g*12/r; c=Math.max(15,Math.min(250,c));
      const pH=7.40-Math.log10(c/100); const j=pH<7.35?'산증 쪽':pH>7.45?'알칼리증 쪽':'정상 범위'; return {r,c,pH,j}; }
    function draw(){ const v=calc();
      O('r').textContent=v.r+'회/분'; O('c').textContent=Math.round(v.c)+' %'; O('ph').textContent=v.pH.toFixed(2); O('j').textContent=v.j;
      const sh=v.c<95?'rev':v.c>105?'fw':'eq';
      O('msg').textContent=sh==='rev'?'혈액의 이산화 탄소가 줄어 ①·②의 평형이 역반응 쪽으로 이동 → 하이드로늄 이온 감소 → pH 증가'
        :sh==='fw'?'혈액의 이산화 탄소가 늘어 ①·②의 평형이 정반응 쪽으로 이동 → 하이드로늄 이온 증가 → pH 감소'
        :'이산화 탄소가 알맞게 배출되어 평형이 유지된다 → pH 거의 일정';
      while(ga.firstChild) ga.removeChild(ga.firstChild);
      const wf=sh==='fw'?6:2.5, wr=sh==='rev'?6:2.5;
      [[60,418,486],[140,424,480]].forEach(([y,a,b])=>{ API.arrow(ga,a,y-26,b,y-26,FW,wf); API.arrow(ga,b,y-12,a,y-12,RV,wr); });
      const x=px(v.pH); needle.setAttribute('d',`M${x-9} ${GY-24} L${x+9} ${GY-24} L${x} ${GY-2} Z`);
      cur={a:act==='run'?'달리기':'휴식',r:v.r,c:Math.round(v.c),pH:v.pH.toFixed(2),j:v.j};
    }
    function drawLog(){ O('log').innerHTML=log.map(r=>`<tr><td>${r.a}</td><td>${r.r}회/분</td><td>${r.c} %</td><td>${r.pH}</td><td>${r.j}</td></tr>`).join(''); }
    function setAct(a){ act=a; root.querySelectorAll('[data-act2]').forEach(b=>b.classList.toggle('rm19-act',b.dataset.act2===a)); draw(); }
    root.querySelectorAll('[data-act2]').forEach(b=>b.addEventListener('click',()=>setAct(b.dataset.act2)));
    iR.addEventListener('input',draw);
    $('[data-act="rec"]').addEventListener('click',()=>{ draw(); log.push(cur); if(log.length>5) log.shift(); drawLog(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; drawLog(); iR.value=12; setAct('rest'); });
    API.onShow&&API.onShow(draw);
    draw(); drawLog();
    let ph=0;
    API.loop(root,(dt,t)=>{ const r=+iR.value; ph=(ph+dt*r/60)%1; const s=1+0.12*Math.sin(ph*2*Math.PI);
      L1.setAttribute('rx',(36*s).toFixed(1)); L2.setAttribute('rx',(36*s).toFixed(1)); L1.setAttribute('ry',(62*s).toFixed(1)); L2.setAttribute('ry',(62*s).toFixed(1));
      const n=Math.max(1,Math.min(6,Math.round(r/5)));
      dots.forEach((d,k)=>{ const p=((t||0)*r/30+k/6)%1; d.setAttribute('cy',(24-p*20+6).toFixed(1)); d.setAttribute('cx',(110+(k%2?14:-14)*p).toFixed(1)); d.setAttribute('opacity',k<n?(1-p).toFixed(2):0); });
    });
  }
};
