/* 3-3 다양한 고분자 화합물 — 실험실
   rm33poly : 중합 반응 — 단위체(에틸렌 / 글리신 / 테레프탈산 + 에틸렌 글리콜)를 하나씩 이음 (n = 1–8)
              첨가: 물 0, 분자량 = 단위체 합 / 축합: 물 n−1, 분자량 = 단위체 합 − 18(n−1)
              원소별 원자 수: 단위체 합 = 고분자 + 물 → 표 + 분자량–단위체 수 그래프 (plan.md 2절) */
(function(){
const INK='#16233D', MUT='#5B6B7F', FLD='#2E9E6A', BF='#7B4FC8', PLS='#D7263D', MIN='#1F6FD1';
const MONO={ // 원자 수, 분자량
  eth:{C:2,H:4,N:0,O:0,M:28,col:'#F08A5D',t:'에틸렌',tex:'\\ce{C2H4}'},
  gly:{C:2,H:5,N:1,O:2,M:75,col:'#B07CD8',t:'글리신',tex:'\\ce{C2H5NO2}'},
  tpa:{C:8,H:6,N:0,O:4,M:166,col:'#5AA9E6',t:'테레프탈산',tex:'\\ce{C8H6O4}'},
  eg :{C:2,H:6,N:0,O:2,M:62,col:'#F2C230',t:'에틸렌 글리콜',tex:'\\ce{C2H6O2}'}
};
const SYS={
  pe :{name:'폴리에틸렌',kind:'첨가',seq:i=>'eth',ser:{c:FLD,m:'s'}},
  gly:{name:'폴리펩타이드',kind:'축합',seq:i=>'gly',ser:{c:PLS,m:'d'}},
  pet:{name:'PET',kind:'축합',seq:i=>i%2?'eg':'tpa',ser:{c:BF,m:'t'}}
};
function marker(API,g,x,y,ser,r){ r=r||6; const c=ser.c;
  if(ser.m==='s') return API.mk('rect',{x:x-r,y:y-r,width:2*r,height:2*r,fill:c},g);
  if(ser.m==='t') return API.mk('polygon',{points:`${x},${y-r-1} ${x+r+1},${y+r} ${x-r-1},${y+r}`,fill:c},g);
  return API.mk('polygon',{points:`${x},${y-r-2} ${x+r+2},${y} ${x},${y+r+2} ${x-r-2},${y}`,fill:c},g); }
const clear=g=>{ while(g.firstChild) g.removeChild(g.firstChild); };
function fml(c){ // 원자 수 → 화학식 tex
  let s=''; [['C',c.C],['H',c.H],['N',c.N],['O',c.O]].forEach(([e,k])=>{ if(k>0) s+=e+(k>1?k:''); }); return '\\ce{'+s+'}'; }

window.DECK_LABS = {
  rm33poly(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg');
    const gA=API.mk('g',{},svg), gC=API.mk('g',{},svg), gW=API.mk('g',{},svg), gP=API.mk('g',{},svg);
    let s='pe', n=1, log=[], pts=[], flying=[];
    const NMAX=8, BX=i=>52+72*i, BY=88, WY=172, WX=k=>64+62*k;
    // ── 고정 그림: 칸, 범례, 그래프 축 ──
    API.mk('rect',{x:8,y:20,width:634,height:132,rx:14,fill:'#F7F9FB',stroke:'#D5DCE3','stroke-width':2},gA);
    API.mk('rect',{x:8,y:142,width:634,height:56,rx:12,fill:'#EEF4FB',stroke:'#C9D8EA','stroke-width':1.5,'stroke-dasharray':'6 5'},gA);
    API.texText(gA,18,44,'고분자 사슬',{size:18,anchor:'start',fill:MUT,mix:true});
    API.texText(gA,632,192,'떨어져 나간 물',{size:18,anchor:'end',fill:MIN,mix:true});
    const GX=86, GY=296, GW=520, GH=164, MM=800;
    const gx=k=>GX+(k-0.5)/NMAX*GW, gy=M=>GY+(1-M/MM)*GH;
    [0,400,800].forEach(M=>{ API.mk('line',{x1:GX,y1:gy(M),x2:GX+GW,y2:gy(M),stroke:'#E2E7EC','stroke-width':1.5},gA); API.texText(gA,GX-8,gy(M)+6,'$'+M+'$',{size:18,anchor:'end',fill:MUT,mix:true}); });
    for(let k=1;k<=NMAX;k++) API.texText(gA,gx(k),GY+GH+24,'$'+k+'$',{size:18,anchor:'middle',fill:MUT,mix:true});
    API.mk('line',{x1:GX,y1:GY-8,x2:GX,y2:GY+GH,stroke:MUT,'stroke-width':2},gA);
    API.mk('line',{x1:GX,y1:GY+GH,x2:GX+GW,y2:GY+GH,stroke:MUT,'stroke-width':2},gA);
    API.texText(gA,GX+6,GY-14,'고분자의 분자량',{size:18,anchor:'start',fill:MUT,mix:true});
    API.texText(gA,GX+GW,GY+GH+50,'이은 단위체 수',{size:18,anchor:'end',fill:MUT,mix:true});
    [['pe','폴리에틸렌',300],['gly','폴리펩타이드',425],['pet','PET',565]].forEach(([k,t,x])=>{ marker(API,gA,x,GY-20,SYS[k].ser); API.texText(gA,x+12,GY-14,t,{size:18,anchor:'start',fill:MUT,mix:true}); });
    function water(g,x,y,op){ const w=API.mk('g',{opacity:op==null?1:op},g);
      API.mk('line',{x1:x,y1:y,x2:x-12,y2:y+9,stroke:'#9AA5B1','stroke-width':4,'stroke-linecap':'round'},w);
      API.mk('line',{x1:x,y1:y,x2:x+12,y2:y+9,stroke:'#9AA5B1','stroke-width':4,'stroke-linecap':'round'},w);
      API.atom(w,x-12,y+9,8,'H','-',false); API.atom(w,x+12,y+9,8,'H','-',false); API.atom(w,x,y,12,'O','-',false); return w; }
    const sys=()=>SYS[s];
    const wN=()=>sys().kind==='첨가'?0:n-1;
    function sums(){ const t={C:0,H:0,N:0,O:0,M:0}; for(let i=0;i<n;i++){ const m=MONO[sys().seq(i)]; ['C','H','N','O','M'].forEach(e=>t[e]+=m[e]); } return t; }
    function poly(){ const t=sums(), w=wN(); return {C:t.C,H:t.H-2*w,N:t.N,O:t.O-w,M:t.M-18*w}; }
    function drawChain(){
      clear(gC);
      if(n>1) API.mk('line',{x1:BX(0),y1:BY,x2:BX(n-1),y2:BY,stroke:'#7E8B98','stroke-width':4},gC);
      if(n>1) API.mk('line',{x1:BX(n-2)+22,y1:BY,x2:BX(n-1)-22,y2:BY,stroke:FLD,'stroke-width':6,'stroke-linecap':'round'},gC);
      for(let i=0;i<n;i++){ const m=MONO[sys().seq(i)];
        API.mk('circle',{cx:BX(i),cy:BY,r:24,fill:m.col,stroke:INK,'stroke-opacity':.35,'stroke-width':1.5},gC); }
      // 이름 (단위체)
      const used=[...new Set(Array.from({length:n},(_,i)=>sys().seq(i)))];
      const L=Ov('leg'); L.innerHTML=used.map(k=>`<span style="color:${MONO[k].col};font-size:22px">●</span> ${MONO[k].t} ${API.tex(MONO[k].tex)}`).join('&emsp;&emsp;'); API.place(L,380,44);
    }
    function drawWater(){ clear(gW); const w=wN(); const settled=w-flying.length;
      for(let k=0;k<settled;k++) water(gW,WX(k),WY-6);
      flying.forEach(f=>water(gW,f.x+(WX(f.k)-f.x)*f.p,BY+(WY-6-BY)*f.p,.4+.6*f.p)); }
    function drawPts(){ clear(gP); pts.forEach(q=>marker(API,gP,gx(q.n)+(q.s==='gly'?6:q.s==='pet'?-6:0),gy(q.M),SYS[q.s].ser));
      const p=poly(); API.mk('circle',{cx:gx(n),cy:gy(p.M),r:7,fill:'none',stroke:INK,'stroke-width':2.5},gP); }
    function update(){
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===s));
      $('[data-act="add"]').disabled = n>=NMAX;
      const p=poly(), t=sums(), w=wN();
      O('n').textContent=n+' 개';
      O('w').textContent=w+' 개';
      O('M').textContent=p.M;
      let m;
      if(n===1) m='단위체가 하나뿐이다. ‘단위체 하나 잇기’를 눌러 사슬을 늘려 보자.';
      else if(sys().kind==='첨가') m='첨가 중합: 이중 결합 하나가 끊어지며 이어진다. 떨어져 나가는 분자가 없어 분자량이 28씩 는다.';
      else if(s==='gly') m='축합 중합: 이을 때마다 물 분자 하나가 떨어져 나가 분자량이 75 − 18 = 57씩 는다.';
      else m='축합 중합: 테레프탈산과 에틸렌 글리콜이 번갈아 이어지며, 이을 때마다 물 분자 하나가 떨어져 나간다.';
      O('msg').textContent=m;
      const A=Ov('atoms');
      A.innerHTML = '단위체 합 '+API.tex(fml(t))+'&ensp;=&ensp;고분자 '+API.tex(fml(p))+(w? '&ensp;+&ensp;'+API.tex('\\ce{'+(w>1?w:'')+'H2O}') : '');
      API.place(A,325,244);
      drawChain(); drawWater(); drawPts();
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${r.t}</td><td>${r.n}</td><td>${r.w}</td><td>${r.M}</td>`; tb.appendChild(tr); }); }
    const start=()=>{ n=1; flying=[]; };
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ s=b.dataset.s; start(); update(); }));
    $('[data-act="add"]').addEventListener('click',()=>{ if(n>=NMAX) return; n++;
      if(sys().kind==='축합') flying.push({k:n-2,x:(BX(n-2)+BX(n-1))/2,p:window.__STILL?1:0});
      flying=flying.filter(f=>f.p<1); update(); });
    $('[data-act="rec"]').addEventListener('click',()=>{ const p=poly();
      log.push({t:sys().name,n,w:wN(),M:p.M}); if(log.length>5) log.shift();
      pts=pts.filter(q=>!(q.s===s&&q.n===n)); pts.push({s,n,M:p.M}); renderLog(); update(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; pts=[]; s='pe'; start(); renderLog(); update(); });
    root._step=()=>{ flying=[]; update(); };
    if(!window.__STILL) API.loop(root,dt=>{ if(!flying.length) return;
      flying.forEach(f=>f.p=Math.min(1,f.p+dt*1.4)); flying=flying.filter(f=>f.p<1); drawWater(); });
    API.ready(()=>update());
    update();
  }
};
})();
