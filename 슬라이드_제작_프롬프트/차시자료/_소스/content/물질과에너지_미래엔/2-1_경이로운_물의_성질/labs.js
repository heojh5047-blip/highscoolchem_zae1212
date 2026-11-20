/* 2-1 경이로운 물의 성질 — 실험실
   em21heat : 같은 열을 받을 때 온도 변화 비교(비열) — 선택 실험실
     · 물질(물 4.2, 에탄올 2.5 — 교과서 47쪽, 식용유 2.0 J/(g·°C)), 질량 100 g, 가열 장치 50 W, 처음 온도 20.0 °C
     · q = 50 t, Δt = q/(c·100) + 측정 오차(고정 시드, ±0.2 °C), 계산 비열 c = q/(100 Δt)
     · 「측정 기록」→ 표에 행이 쌓이고(최근 5행) 그래프에 점이 찍힌다. 「초기화」. */
window.DECK_LABS = {
  em21heat(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg');
    const SUB={w:{nm:'물',c:4.2,fill:'#DDEEF8',col:'#1F6FD1'}, e:{nm:'에탄올',c:2.5,fill:'#F4F6F8',col:'#E08A2C'}, o:{nm:'식용유',c:2.00,fill:'#F6E3A1',col:'#7B4FC8'}};
    const P=50, M=100, T0=20;
    const gx0=290, gx1=580, gy0=250, gy1=30;
    const GX=t=>gx0+(gx1-gx0)*t/240, GY=T=>gy0-(gy0-gy1)*(T-20)/60;
    const TY=T=>212-(T-20)*2.4;   // 온도계 액주
    let st={s:'w'}, log=[], pts=[];
    const noise=(s,t)=>{ let h=(s.charCodeAt(0)*131+t*7919)%1000; h=(h*9301+49297)%233280; return Math.round((h/233280-.5)*4)/10; };   // −0.2…+0.2
    // 고정 그림(축·눈금·범례)은 처음 한 번만
    const base=API.mk('g',{},svg);
    API.mk('rect',{x:20,y:246,width:170,height:22,rx:4,fill:'#5B6B7F'},base);
    API.mk('line',{x1:gx0,y1:gy0,x2:gx1+8,y2:gy0,stroke:'muted','stroke-width':2},base);
    API.mk('line',{x1:gx0,y1:gy0,x2:gx0,y2:gy1-10,stroke:'muted','stroke-width':2},base);
    [20,40,60,80].forEach(T=>{ API.mk('line',{x1:gx0-5,y1:GY(T),x2:gx1,y2:GY(T),stroke:'#E2E7EC','stroke-width':1.5},base); API.texText(base,gx0-9,GY(T)+6,String(T),{size:18,anchor:'end',fill:'#5B6B7F'}); });
    [0,120,240].forEach(t=>{ API.texText(base,GX(t),gy0+24,String(t),{size:18,anchor:'middle',fill:'#5B6B7F'}); });
    API.texText(base,GX(180),gy0+24,'$t$ [s]',{size:19,anchor:'middle',mix:true});
    API.texText(base,gx0+6,gy1-12,'온도 [°C]',{size:19,mix:true});
    [['w',0],['e',1],['o',2]].forEach(([k,i])=>{ const x=gx0+86+i*72; API.mk('circle',{cx:x,cy:gy1+12,r:6,fill:SUB[k].col},base); API.texText(base,x+10,gy1+18,SUB[k].nm,{size:18,mix:true}); });
    const g=API.mk('g',{},svg);
    let bub=[];
    function cur(){ const t=+I('t').value, s=SUB[st.s], q=P*t, dth=q/(s.c*M), dt=t? Math.max(.1,dth+noise(st.s,t)) : 0; return {t,s,q,dt,T:T0+dt,c:t? q/(M*dt):null}; }
    function draw(){
      const r=cur();
      O('t').textContent=r.t+' s'; O('q').textContent=r.q+' J'; O('T').textContent=r.T.toFixed(1)+' °C'; O('dt').textContent=r.dt.toFixed(1)+' °C';
      O('c').textContent=r.c? r.c.toFixed(2)+' J/(g·°C)' : '—';
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===st.s));
      O('msg').textContent = !r.t ? '가열 시간을 늘려 보자.' :
        st.s==='w' ? '물은 비열이 커서 같은 열을 받아도 온도가 가장 천천히 오른다.' :
        `${r.s.nm}${st.s==='e'?'은':'는'} 같은 시간 가열하면 물보다 온도 변화가 약 ${(4.2/r.s.c).toFixed(1)}배 크다 → 비열이 물보다 작다.`;
      while(g.firstChild) g.removeChild(g.firstChild);
      // 비커·액체
      const lv=150;
      API.mk('rect',{x:42,y:lv,width:126,height:94,fill:r.s.fill},g);
      API.mk('line',{x1:42,y1:lv,x2:168,y2:lv,stroke:'#9FC3DD','stroke-width':2},g);
      API.mk('path',{d:'M34 110 Q40 110 40 116 V238 Q40 244 46 244 H164 Q170 244 170 238 V110',fill:'none',stroke:'#7E8B98','stroke-width':3},g);
      if(r.t){ bub.forEach(b=>API.mk('circle',{cx:b.x,cy:b.y,r:2.5,fill:'#9FB0C2'},g)); API.mk('rect',{x:24,y:268,width:162,height:5,fill:'#D7263D',opacity:.7},g); }
      // 온도계
      API.mk('rect',{x:144,y:40,width:12,height:180,rx:6,fill:'#fff',stroke:'#16233D','stroke-width':2},g);
      API.mk('rect',{x:147,y:TY(Math.min(r.T,80)),width:6,height:224-TY(Math.min(r.T,80)),fill:'#D7263D'},g);
      API.mk('circle',{cx:150,cy:226,r:9,fill:'#D7263D',stroke:'#16233D','stroke-width':2},g);
      // 이론선(현재 물질)
      API.mk('line',{x1:GX(0),y1:GY(20),x2:GX(240),y2:GY(20+P*240/(r.s.c*M)),stroke:r.s.col,'stroke-width':2,'stroke-dasharray':'6 5',opacity:.7},g);
      pts.forEach(p=>API.mk('circle',{cx:GX(p.t),cy:GY(p.T),r:6,fill:SUB[p.s].col,stroke:'#fff','stroke-width':1.5},g));
      API.mk('circle',{cx:GX(r.t),cy:GY(Math.min(r.T,80)),r:7,fill:'#fff',stroke:r.s.col,'stroke-width':3},g);
    }
    function table(){ const tb=O('log'); tb.innerHTML=''; log.slice(-5).forEach(x=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${x.nm}</td><td>${x.t} s</td><td>${x.q} J</td><td>${x.dt} °C</td><td>${x.c}</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ st.s=b.dataset.s; draw(); }));
    I('t').addEventListener('input',draw);
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const r=cur(); log.push({nm:r.s.nm,t:r.t,q:r.q,dt:r.dt.toFixed(1),c:r.c?r.c.toFixed(2):'—'}); pts.push({s:st.s,t:r.t,T:r.T}); table(); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; pts=[]; table(); draw(); });
    for(let i=0;i<10;i++) bub.push({x:52+((i*37)%106), y:160+((i*53)%78), v:8+(i%4)*3});
    draw();
    if(!window.__STILL) API.loop(root,dt=>{ if(!+I('t').value) return; bub.forEach(b=>{ b.y-=b.v*dt; if(b.y<156) b.y=238; }); draw(); });
  }
};
