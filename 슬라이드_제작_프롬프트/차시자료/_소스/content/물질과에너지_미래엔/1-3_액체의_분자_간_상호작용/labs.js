/* 1-3 액체의 분자 간 상호작용 — 실험실
   em13bp : 필수 탐구 물01-탐2 「수소 화합물의 끓는점에 영향을 주는 요인 추론하기」(교과서 26쪽 탐구)
     · 족(14–17)·주기(2–5) 고르기 → 분자량·끓는점(CRC)·극성·작용하는 분자 간 상호작용
     · 「그래프에 찍기」: 점(족별 모양·색) + 같은 족 선 + 기록 표(최근 4행)
     · 「경향 연장」: 3–5주기 점을 분자량에 대한 직선(최소 제곱)으로 맞춰 2주기 분자량까지 연장 → 예상값과 실제값 비교(수소 결합)
   em13vp : 해 보기(28쪽) 「여러 가지 액체의 증기 압력 곡선 해석하기」를 넓힌 모의실험
     · 앙투안 식 log10 P(mmHg) = A − B/(C + t)로 증기압, 외부 압력에서의 끓는점 t = B/(A − log10 P) − C
     · 온도·외부 압력 슬라이더 → 증기압 ≥ 외부 압력이면 끓음(비커에 기포, API.loop) */
window.DECK_LABS = {
  em13bp(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=root.querySelector('svg');
    const D=[ // 족, 주기, 식, 분자량, 끓는점, 극성, 수소 결합
      [14,2,'CH4',16,-161.5,0,0],[14,3,'SiH4',32,-111.9,0,0],[14,4,'GeH4',77,-88.5,0,0],[14,5,'SnH4',123,-52.0,0,0],
      [15,2,'NH3',17,-33.3,1,1],[15,3,'PH3',34,-87.7,1,0],[15,4,'AsH3',78,-62.5,1,0],[15,5,'SbH3',125,-17.0,1,0],
      [16,2,'H2O',18,100.0,1,1],[16,3,'H2S',34,-60.3,1,0],[16,4,'H2Se',81,-41.3,1,0],[16,5,'H2Te',130,-2.0,1,0],
      [17,2,'HF',20,19.5,1,1],[17,3,'HCl',36.5,-85.0,1,0],[17,4,'HBr',81,-66.7,1,0],[17,5,'HI',128,-35.4,1,0]];
    const GC={14:'#16233D',15:'#7B4FC8',16:'#2E9E6A',17:'#E08A2C'};
    const LOFF={CH4:[-12,8,'end'],SiH4:[-12,16,'end'],GeH4:[0,28,'middle'],SnH4:[-12,10,'end'],NH3:[-12,6,'end'],PH3:[-12,0,'end'],AsH3:[-10,-12,'end'],SbH3:[-12,4,'end'],
      H2O:[14,8,'start'],H2S:[12,-6,'start'],H2Se:[0,-14,'middle'],H2Te:[12,4,'start'],HF:[14,6,'start'],HCl:[12,16,'start'],HBr:[12,18,'start'],HI:[12,10,'start']};
    const x0=70,x1=560,y0=268,y1=22, fx=v=>x0+v*(x1-x0)/140, fy=v=>y0-(v+200)*(y0-y1)/350;
    const gA=API.mk('g',{},svg), gL=API.mk('g',{},svg), gE=API.mk('g',{},svg), gP=API.mk('g',{},svg), gT=API.mk('g',{},svg);
    // 축
    for(let v=0;v<=140;v+=20){ API.mk('line',{x1:fx(v),y1:y0,x2:fx(v),y2:y1,stroke:'#E3E8EE','stroke-width':1},gA); API.mk('line',{x1:fx(v),y1:y0,x2:fx(v),y2:y0+6,stroke:'#5B6B7F','stroke-width':2},gA); API.texText(gA,fx(v),y0+24,String(v),{size:18,anchor:'middle'}); }
    for(let v=-200;v<=150;v+=50){ API.mk('line',{x1:x0,y1:fy(v),x2:x1,y2:fy(v),stroke:'#E3E8EE','stroke-width':1},gA); API.mk('line',{x1:x0-6,y1:fy(v),x2:x0,y2:fy(v),stroke:'#5B6B7F','stroke-width':2},gA); API.texText(gA,x0-10,fy(v)+6,String(v).replace('-','−'),{size:18,anchor:'end'}); }
    API.mk('line',{x1:x0,y1:y0,x2:x1,y2:y0,stroke:'#5B6B7F','stroke-width':2},gA); API.mk('line',{x1:x0,y1:y0,x2:x0,y2:y1,stroke:'#5B6B7F','stroke-width':2},gA);
    API.texText(gA,x1+20,y0+6,'분자량',{size:19,anchor:'start',mix:true}); API.texText(gA,x0+8,y1+14,'끓는점 [°C]',{size:19,anchor:'start',mix:true});
    function marker(g,x,y,gr,r,fill,extra){ const c=GC[gr], f=fill||c, a=Object.assign({stroke:c,'stroke-width':2,fill:f},extra||{});
      if(gr===14) return API.mk('circle',Object.assign({cx:x,cy:y,r},a),g);
      if(gr===15) return API.mk('rect',Object.assign({x:x-r,y:y-r,width:2*r,height:2*r},a),g);
      if(gr===16) return API.mk('polygon',Object.assign({points:`${x},${y-r-2} ${x+r+1},${y+r-1} ${x-r-1},${y+r-1}`},a),g);
      return API.mk('polygon',Object.assign({points:`${x},${y-r-2} ${x+r+2},${y} ${x},${y+r+2} ${x-r-2},${y}`},a),g); }
    [14,15,16,17].forEach((g,i)=>{ const lx=280+i*72, ly=250; API.mk('line',{x1:lx,y1:ly,x2:lx+26,y2:ly,stroke:GC[g],'stroke-width':3},gA); marker(gA,lx+13,ly,g,6); API.texText(gA,lx+32,ly+7,`\\text{${g}족}`,{size:19,anchor:'start'}); });
    // 화합물 라벨 (처음에 모두 만들고 숨김)
    const lab={}; D.forEach(r=>{ const [dx,dy,an]=LOFF[r[2]]; const t=API.texText(gT,fx(r[3])+dx,fy(r[4])+dy,`\\ce{${r[2]}}`,{size:18,anchor:an}); t.style.display='none'; lab[r[2]]=t; });
    // 경향 연장 라벨 (HTML 겹침)
    let grp=16, on=new Set(), log=[], ext=false;
    const cur=()=>D.find(r=>r[0]===grp&&r[1]===+I('per').value);
    function fit(g){ const pts=D.filter(r=>r[0]===g&&r[1]>=3); if(!pts.every(r=>on.has(r[2]))) return null;
      const n=pts.length, mx=pts.reduce((s,r)=>s+r[3],0)/n, my=pts.reduce((s,r)=>s+r[4],0)/n;
      const b=pts.reduce((s,r)=>s+(r[3]-mx)*(r[4]-my),0)/pts.reduce((s,r)=>s+(r[3]-mx)**2,0); return {b,a:my-b*mx}; }
    function draw(){
      const c=cur();
      O('per').textContent=`${c[1]}주기`;
      Ov('f').innerHTML=API.tex(`\\ce{${c[2]}}`); O('mw').textContent=`분자량 ${c[3]}`;
      O('bp').textContent=`${c[4].toFixed(1).replace('-','−')} °C`;
      O('kind').textContent=(c[5]?'극성 분자':'무극성 분자 (정사면체형)')+' · 작용하는 힘: 분산력'+(c[5]?' + 쌍극자·쌍극자 힘':'')+(c[6]?' + 수소 결합':'');
      // 점과 선
      gL.innerHTML=''; gP.innerHTML=''; gE.innerHTML='';
      [14,15,16,17].forEach(g=>{ const pts=D.filter(r=>r[0]===g&&on.has(r[2])).sort((a,b)=>a[3]-b[3]);
        if(pts.length>1) API.mk('polyline',{points:pts.map(r=>`${fx(r[3]).toFixed(1)},${fy(r[4]).toFixed(1)}`).join(' '),fill:'none',stroke:GC[g],'stroke-width':3},gL); });
      D.forEach(r=>{ const v=on.has(r[2]); lab[r[2]].style.display=v?'':'none'; if(v) marker(gP,fx(r[3]),fy(r[4]),r[0],7); });
      API.mk('circle',{cx:fx(c[3]),cy:fy(c[4]),r:14,fill:'none',stroke:'#D7263D','stroke-width':2.5,'stroke-dasharray':'5 4'},gP);
      const res=[];
      if(ext){ [14,15,16,17].forEach(g=>{ const f=fit(g), p2=D.find(r=>r[0]===g&&r[1]===2); if(!f||!on.has(p2[2])) return;
          const pred=f.a+f.b*p2[3], top=D.find(r=>r[0]===g&&r[1]===5);
          API.mk('line',{x1:fx(top[3]),y1:fy(f.a+f.b*top[3]),x2:fx(p2[3]),y2:fy(pred),stroke:GC[g],'stroke-width':2,'stroke-dasharray':'6 5'},gE);
          marker(gE,fx(p2[3]),fy(pred),g,7,'#fff');
          if(p2[6]) API.arrow(gE,fx(p2[3])-14,fy(pred)-4,fx(p2[3])-14,fy(p2[4])+10,'#D7263D',2.5);
          res.push({g,nm:p2[2],pred,act:p2[4],hb:p2[6]}); }); }
      table();
      // 해석 문장
      const n=on.size; let m;
      if(!n) m='족과 주기를 고르고 「그래프에 찍기」를 눌러 보자. 한 족의 2~5주기를 모두 찍으면 경향이 보인다.';
      else if(ext&&res.length){ const f=v=>Math.round(v).toString().replace('-','−'); m='경향에서 예상한 2주기 끓는점 → 실제: '+res.map(q=>`${q.g}족 ${f(q.pred)} → ${f(q.act)} °C`+(q.hb?'(수소 결합)':'')).join(', ')+'. 수소 결합이 있는 2주기 화합물만 예상보다 훨씬 높다.'; }
      else if(ext) m='경향을 연장하려면 한 족의 2~5주기를 모두 찍자(「모두 찍기」).';
      else if([...on].some(s=>['NH3','H2O','HF'].includes(s))&&n>=6) m='분자량이 가장 작은 2주기의 암모니아, 물, 플루오린화 수소의 끓는점이 예외적으로 높다. 「경향 연장」으로 경향에서 얼마나 벗어나는지 보자.';
      else if([14,15,16,17].some(g=>D.filter(r=>r[0]===g&&r[1]>=3).every(r=>on.has(r[2])))) m='같은 족에서 3~5주기는 분자량이 클수록 끓는점이 높다 → 분자량이 클수록 분산력이 강하다.';
      else m=`점 ${n}개를 찍었다. 같은 족의 다른 주기도 찍어 비교해 보자.`;
      O('msg').textContent=m;
    }
    function table(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-4).forEach((r,i)=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${log.length-Math.min(log.length,4)+i+1}</td><td>${API.tex(`\\ce{${r[2]}}`)}</td><td>${r[0]}</td><td>${r[3]}</td><td>${r[4].toFixed(1).replace('-','−')}</td><td>${r[5]?'극성':'무극성'}</td><td>${r[6]?'○':'×'}</td>`;
        tb.appendChild(tr); }); }
    root.querySelectorAll('[data-g]').forEach(b=>b.addEventListener('click',()=>{ grp=+b.dataset.g; root.querySelectorAll('[data-g]').forEach(x=>x.classList.toggle('on',x===b)); draw(); }));
    I('per').addEventListener('input',draw);
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const c=cur(); on.add(c[2]); log.push(c); draw(); });
    root.querySelector('[data-act="all"]').addEventListener('click',()=>{ D.forEach(r=>{ if(!on.has(r[2])){ on.add(r[2]); log.push(r);} }); draw(); });
    const extB=root.querySelector('[data-act="ext"]');
    extB.addEventListener('click',()=>{ ext=!ext; extB.classList.toggle('on',ext); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ on.clear(); log=[]; ext=false; extB.classList.remove('on'); grp=16; I('per').value=2; root.querySelectorAll('[data-g]').forEach(x=>x.classList.toggle('on',x.dataset.g==='16')); draw(); });
    draw(); API.ready(draw); API.onShow(draw);
    // 고른 점의 테두리가 천천히 돈다(보일 때만)
    if(!window.__STILL) API.loop(root,(dt,t)=>{ const ring=gP.lastChild; if(ring) ring.setAttribute('stroke-dashoffset',(-t*20).toFixed(1)); });
  },

  em13vp(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('svg');
    const L=[['다이에틸 에터','ether',6.92032,1064.07,228.8,'#7B4FC8'],['에탄올','ethanol',8.20417,1642.89,230.3,'#E08A2C'],['물','water',8.07131,1730.63,233.426,'#0E7490'],['아세트산','acetic',7.38782,1533.313,222.309,'#2E9E6A']];
    const vp=(q,t)=>Math.pow(10,q[2]-q[3]/(q[4]+t)), bpt=(q,P)=>q[3]/(q[2]-Math.log10(P))-q[4];
    const x0=72,x1=450,y0=280,y1=20, fx=v=>x0+v*(x1-x0)/130, fy=v=>y0-v*(y0-y1)/1600;
    const gA=API.mk('g',{},svg), gV=API.mk('g',{},svg), gB=API.mk('g',{},svg), gQ=API.mk('g',{},svg);
    for(let v=0;v<=100;v+=20){ API.mk('line',{x1:fx(v),y1:y0,x2:fx(v),y2:y1,stroke:'#E3E8EE','stroke-width':1},gA); API.texText(gA,fx(v),y0+24,String(v),{size:18,anchor:'middle'}); }
    for(let v=0;v<=1600;v+=400){ API.mk('line',{x1:x0,y1:fy(v),x2:x1,y2:fy(v),stroke:'#E3E8EE','stroke-width':1},gA); API.texText(gA,x0-8,fy(v)+6,String(v),{size:18,anchor:'end'}); }
    API.mk('line',{x1:x0,y1:y0,x2:x1,y2:y0,stroke:'#5B6B7F','stroke-width':2},gA); API.mk('line',{x1:x0,y1:y0,x2:x0,y2:y1,stroke:'#5B6B7F','stroke-width':2},gA);
    API.texText(gA,x1,y0+44,'$t$ [°C]',{size:19,anchor:'end',mix:true}); API.texText(gA,x0+8,y1+14,'증기압 [mmHg]',{size:19,anchor:'start',mix:true});
    const lpos=[[50,1300],[56,900],[115,1250],[118,560]];
    L.forEach((q,i)=>{ const pts=[]; for(let t=0;t<=130;t+=1){ const p=vp(q,t); if(p>1600){ pts.push([fx(bpt(q,1600)),fy(1600)]); break; } pts.push([fx(t),fy(p)]); }
      API.mk('polyline',{points:pts.map(p=>p.map(v=>v.toFixed(1)).join(',')).join(' '),fill:'none',stroke:q[5],'stroke-width':3.5},gA);
      API.texText(gA,fx(lpos[i][0]),fy(lpos[i][1]),`\\text{${q[0]}}`,{size:18,anchor:(i===3||i===0)?'start':'end',fill:q[5]}); });
    // 비커 4개
    const bx=490, by=[30,100,170,240];
    const bub=L.map(()=>[]);
    L.forEach((q,i)=>{ const y=by[i];
      API.mk('path',{d:`M${bx} ${y} V${y+50} Q${bx} ${y+56} ${bx+6} ${y+56} H${bx+64} Q${bx+70} ${y+56} ${bx+70} ${y+50} V${y}`,fill:'#F8FBFD',stroke:'#7E8B98','stroke-width':2.5},gB);
      API.mk('rect',{x:bx+2,y:y+18,width:66,height:36,rx:4,fill:'#EAF2F8'},gB);
      API.texText(gB,bx+82,y+34,`\\text{${q[0]}}`,{size:19,anchor:'start',fill:q[5]});
      for(let k=0;k<5;k++){ const c=API.mk('circle',{cx:bx+10+k*12,cy:y+50,r:4,fill:'#fff',stroke:q[5],'stroke-width':1.6},gB); c.style.display='none'; bub[i].push({c,ph:k*0.2+i*0.07}); } });
    const st=()=>({t:+I('t').value,P:+I('P').value});
    let boil=[false,false,false,false];
    function draw(){
      const s=st(), Pm=s.P*760;
      O('t').textContent=`${s.t} °C`; O('P').textContent=`${s.P.toFixed(1)} 기압 (${Math.round(Pm)} mmHg)`;
      gQ.innerHTML='';
      API.mk('line',{x1:x0,y1:fy(Pm),x2:x1,y2:fy(Pm),stroke:'#16233D','stroke-width':2.5,'stroke-dasharray':'8 6'},gQ);
      API.mk('line',{x1:fx(s.t),y1:y0,x2:fx(s.t),y2:y1,stroke:'#D7263D','stroke-width':2},gQ);
      const rows=[]; const names=[];
      L.forEach((q,i)=>{ const p=vp(q,s.t), b=bpt(q,Pm); boil[i]=p>=Pm;
        if(b<=130) API.mk('circle',{cx:fx(b),cy:fy(Pm),r:6,fill:q[5],stroke:'#fff','stroke-width':1.5},gQ);
        if(p<=1600) API.mk('circle',{cx:fx(s.t),cy:fy(p),r:5,fill:'#fff',stroke:q[5],'stroke-width':2.5},gQ);
        rows.push(`<tr><td>${q[0]}</td><td>${p>=10000?'1만 이상':Math.round(p)} mmHg</td><td>${b.toFixed(0)} °C</td><td>${boil[i]?'<b class="c-plus">끓음</b>':'끓지 않음'}</td></tr>`);
        if(boil[i]) names.push(q[0]); });
      O('tb').innerHTML=rows.join('');
      O('nb').textContent=names.length?names.join(', '):'없음';
      const w=L[2], bw=bpt(w,Pm);
      O('msg').textContent=`외부 압력 ${s.P.toFixed(1)} 기압에서 끓는점: `+L.map(q=>`${q[0]} ${bpt(q,Pm).toFixed(0)} °C`).join(', ')+`. `+(Math.abs(s.P-1)<0.05?'1 기압에서의 끓는점이 기준 끓는점이다.':s.P>1?`외부 압력이 1 기압보다 크면 끓는점이 높아진다(물 100 → ${bw.toFixed(0)} °C).`:`외부 압력이 1 기압보다 작으면 끓는점이 낮아진다(물 100 → ${bw.toFixed(0)} °C).`);
      bub.forEach((B,i)=>B.forEach(b=>b.c.style.display=boil[i]?'':'none'));
    }
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',draw));
    root.querySelectorAll('[data-pp]').forEach(b=>b.addEventListener('click',()=>{ I('P').value=b.dataset.pp; draw(); }));
    draw();
    if(!window.__STILL) API.loop(root,(dt,t)=>{ bub.forEach((B,i)=>{ if(!boil[i]) return; const y=by[i]; B.forEach(b=>{ const f=((t*0.9+b.ph)%1); b.c.setAttribute('cy',(y+50-f*30).toFixed(1)); }); }); });
  }
};
