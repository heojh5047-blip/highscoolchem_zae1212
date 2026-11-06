/* 3-2-3 일상생활 속의 화학 평형 이동 — 실험실
   cm323nh3 : 「암모니아 합성 조건 실험실」 N2 + 3H2 ⇌ 2NH3 (정반응 발열, 기체 분자 수 감소)
   평형 자료: N2:H2 = 1:3 혼합물의 평형 혼합물 속 NH3 몰 % (하버 공정 문헌 자료), 압력·온도 선형 보간.
   평형 수득률 x = 2y/(1+y) (y = NH3 몰분율, 반응한 N2의 비율). Kp는 쓰지 않는다.
   반응 속도(상대값, 450 °C·촉매 = 100) = 100·exp(−80000/R·(1/T − 1/723)), 촉매 없음은 exp(−150000/RT)배.
   한 번 지날 때 수득률 = x·(1 − exp(−2r/100)) — 덱 모의값.
   반응 용기 모형: 처음 N2 6 + H2 18, NH3 n = 2·round(6x) → N2 6 − n/2, H2 18 − 3n/2 (N 12, H 36 보존). */
(function(){
function nh3Lab(root, API){
  const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`);
  const svg=$('svg'), mk=API.mk, INK='#16233D', MU='#5B6B7F', EQ='#E08A2C', GR='#B8C2CC';
  const PS=[10,100,200,300,400], TS=[200,300,400,500,600];
  const YT={200:[50.7,81.5,89.0,89.9,94.6],300:[14.7,52.0,66.7,71.0,79.7],400:[3.9,25.1,38.7,47.8,55.4],500:[1.2,10.6,18.3,25.9,31.9],600:[0.5,4.5,8.8,13.8,18.4]};
  function lin(xs,ys,x){ if(x<=xs[0]) return ys[0]; for(let i=1;i<xs.length;i++) if(x<=xs[i]) return ys[i-1]+(ys[i]-ys[i-1])*(x-xs[i-1])/(xs[i]-xs[i-1]); return ys[ys.length-1]; }
  const yAt=(T,P)=>lin(TS,TS.map(t=>lin(PS,YT[t],P)),T)/100;
  const conv=(T,P)=>{ const y=yAt(T,P); return 2*y/(1+y); };
  const rate=(T,cat)=>{ const K=T+273; return 100*Math.exp(-80000/8.314*(1/K-1/723))*(cat?1:Math.exp(-150000/(8.314*K))); };
  const once=(T,P,cat)=>conv(T,P)*(1-Math.exp(-2*rate(T,cat)/100));
  const pct=v=>v>=0.995?'100 %':v<0.005?'0 %':Math.round(v*100)+' %';
  const fr=r=>r>=10?Math.round(r).toString():r>=0.1?r.toFixed(1):'거의 0';
  // ---------- 그래프 ----------
  const GX=P=>70+P/400*320, GY=v=>250-v*210;
  const bg=mk('g',{},svg);
  mk('rect',{x:70,y:GY(1),width:320,height:210,fill:'#FBFCFD'},bg);
  [0.25,0.5,0.75,1].forEach(v=>mk('path',{d:`M70 ${GY(v)} H390`,stroke:'#E2E7EC','stroke-width':1},bg));
  API.arrow(bg,70,250,404,250,'ink',2); API.arrow(bg,70,250,70,22,'ink',2);
  [0,50,100].forEach(v=>{ mk('path',{d:`M64 ${GY(v/100)} H70`,stroke:INK,'stroke-width':2},bg); API.texText(bg,60,GY(v/100)+6,String(v),{size:18,anchor:'end',fill:INK,mix:true}); });
  [0,100,200,300,400].forEach(P=>{ mk('path',{d:`M${GX(P)} 250 V256`,stroke:INK,'stroke-width':2},bg); API.texText(bg,GX(P),274,String(P),{size:18,anchor:'middle',fill:INK,mix:true}); });
  API.texText(bg,80,22,'평형 수득률 [%]',{size:18,anchor:'start',fill:INK,mix:true});
  API.texText(bg,404,296,'압력 [기압]',{size:18,anchor:'end',fill:INK,mix:true});
  const curve=T=>{ let d=''; for(let P=10;P<=400;P+=10) d+=(d?' L':'M')+GX(P).toFixed(1)+' '+GY(conv(T,P)).toFixed(1); return d; };
  TS.forEach(T=>{ mk('path',{d:curve(T),fill:'none',stroke:GR,'stroke-width':2},bg);
    if(T!==300&&T!==500) API.texText(bg,396,GY(conv(T,400))+6,T+' °C',{size:18,anchor:'start',fill:MU,mix:true}); });
  const cur=mk('path',{fill:'none',stroke:INK,'stroke-width':4},svg);
  const ptsG=mk('g',{},svg);
  const dot=mk('circle',{r:9,fill:EQ,stroke:'#fff','stroke-width':2},svg);
  // ---------- 반응 용기 ----------
  const RX=480, RY=40, RW=200, RH=190;
  mk('rect',{x:RX,y:RY,width:RW,height:RH,rx:22,fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':4},svg);
  const catG=mk('g',{},svg);
  [0,1,2,3].forEach(i=>mk('path',{d:`M${RX+20} ${RY+RH-58+i*14} H${RX+RW-20}`,stroke:'#8C99A6','stroke-width':2},catG));
  [0,1,2,3,4,5].forEach(i=>mk('path',{d:`M${RX+30+i*28} ${RY+RH-64} V${RY+RH-12}`,stroke:'#8C99A6','stroke-width':2},catG));
  const molG=mk('g',{},svg);
  API.texText(svg,RX+RW/2,RY-12,'반응 용기 (평형 혼합물)',{size:18,anchor:'middle',fill:INK,mix:true});
  API.atom(svg,RX+20,RY+RH+24,9,'H','-',false); API.texText(svg,RX+34,RY+RH+30,'H',{size:18,anchor:'start',fill:INK,mix:true});
  API.atom(svg,RX+70,RY+RH+24,12,'N','-',false); API.texText(svg,RX+88,RY+RH+30,'N',{size:18,anchor:'start',fill:INK,mix:true});
  const vtxt=mk('text',{x:RX+RW,y:RY+RH+60,'font-size':18,fill:MU,'text-anchor':'end'},svg);
  let seed=7; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
  const slots=[]; for(let i=0;i<24;i++) slots.push({u:rnd(),v:rnd(),a:rnd()*360,w:1+rnd()*2,p:rnd()*6.28});
  function mol(g,k){ if(k==='n2'){ API.atom(g,-9,0,12,'N','-',false); API.atom(g,9,0,12,'N','-',false); }
    else if(k==='h2'){ API.atom(g,-6.5,0,9,'H','-',false); API.atom(g,6.5,0,9,'H','-',false); }
    else { API.atom(g,-14,9,9,'H','-',false); API.atom(g,14,9,9,'H','-',false); API.atom(g,0,-15,9,'H','-',false); API.atom(g,0,0,12,'N','-',false); } }
  let key='', els=[];
  function build(n){ const a=6-n/2, b=18-3*n/2, k=n+'/'+a+'/'+b; if(k===key) return; key=k; molG.innerHTML=''; els=[];
    const kinds=[]; for(let i=0;i<n;i++) kinds.push('nh3'); for(let i=0;i<a;i++) kinds.push('n2'); for(let i=0;i<b;i++) kinds.push('h2');
    kinds.forEach(kd=>{ const g=mk('g',{},molG); mol(g,kd); els.push(g); }); }
  function place(t){ els.forEach((g,i)=>{ const s=slots[i], j=state.cat?3:2;
    const x=RX+28+s.u*(RW-56)+Math.sin(t*s.w+s.p)*j, y=RY+28+s.v*(RH-56)+Math.cos(t*s.w*1.3+s.p)*j;
    g.setAttribute('transform',`translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${s.a.toFixed(0)})`); }); }
  // ---------- 상태 ----------
  const state={T:450,P:200,cat:true}; let rows=[], nexp=0, recs=[];
  function msg(){ const {T,P,cat}=state, x=conv(T,P), o=once(T,P,cat); let m;
    if(!cat) m='촉매가 없으면 반응이 너무 느려 한 번 지날 때 거의 얻지 못한다. 촉매는 평형 수득률은 바꾸지 않는다.';
    else if(T<=300) m=`평형 수득률은 ${pct(x)}로 크지만 반응 속도가 느려 한 번 지날 때 `+(o<0.01?'거의 얻지 못한다.':`${pct(o)}만 얻는다.`);
    else if(T>=550) m=`반응은 빠르지만 온도가 높아 흡열 반응인 역반응 쪽으로 평형이 이동해 평형 수득률이 ${pct(x)}로 작다.`;
    else m=`온도가 알맞아 반응 속도와 평형 수득률이 균형을 이룬다(한 번 지날 때 ${pct(o)}).`;
    if(P>=300) m+=' 압력이 커 수득률은 크지만 매우 튼튼한(비싼) 반응 용기가 필요하다.';
    else if(P<=50) m+=' 압력이 낮아 기체 분자 수가 많은 역반응 쪽으로 치우쳐 평형 수득률이 작다.';
    return m; }
  function draw(){ const {T,P,cat}=state, x=conv(T,P);
    O('tv').textContent=T+' °C'; O('pv').textContent=P+' 기압';
    O('y').textContent=pct(x);
    O('sub').textContent=`반응 속도 ${fr(rate(T,cat))} · 한 번 지날 때 ${pct(once(T,P,cat))}`;
    O('msg').textContent=msg();
    cur.setAttribute('d',curve(T)); dot.setAttribute('cx',GX(P)); dot.setAttribute('cy',GY(x));
    catG.style.display=cat?'':'none';
    const b=$('[data-act="cat"]'); b.textContent=cat?'촉매 있음':'촉매 없음'; b.classList.toggle('cm323-act',cat);
    vtxt.textContent= P<100?'필요한 용기: 보통':P<300?'필요한 용기: 튼튼한 용기':'필요한 용기: 매우 튼튼(비용 큼)';
    build(2*Math.round(6*x)); place(performance.now()/1000);
    ptsG.innerHTML=''; recs.forEach(r=>mk('circle',{cx:GX(r.P),cy:GY(r.x),r:5,fill:INK,stroke:'#fff','stroke-width':1.5},ptsG)); }
  function rec(){ const {T,P,cat}=state; nexp++;
    rows.push([nexp,T+' °C',P+' 기압',cat?'있음':'없음',pct(conv(T,P)),pct(once(T,P,cat))]); if(rows.length>4) rows.shift();
    recs.push({P,x:conv(T,P)}); const tb=O('log'); tb.innerHTML='';
    rows.forEach(rw=>{ const t=document.createElement('tr'); t.innerHTML=rw.map(v=>`<td>${v}</td>`).join(''); tb.appendChild(t); });
    draw(); }
  function reset(){ state.T=450; state.P=200; state.cat=true; rows=[]; nexp=0; recs=[]; O('log').innerHTML='';
    $('[data-i="t"]').value=450; $('[data-i="p"]').value=200; draw(); }
  $('[data-i="t"]').addEventListener('input',e=>{ state.T=+e.target.value; draw(); });
  $('[data-i="p"]').addEventListener('input',e=>{ state.P=+e.target.value; draw(); });
  $('[data-act="cat"]').addEventListener('click',()=>{ state.cat=!state.cat; draw(); });
  $('[data-act="rec"]').addEventListener('click',rec);
  $('[data-act="reset"]').addEventListener('click',reset);
  reset();
  API.loop(root,(dt,t)=>place(t));
}
window.DECK_LABS = { cm323nh3(root,API){ nh3Lab(root,API); } };
})();
