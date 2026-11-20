/* 1-1b 기체의 성질 (2) 이상 기체 방정식과 활용 — 실험실
   em11pvnt : 해 보기(13쪽) 「기체의 압력, 온도, 양(mol), 부피의 관계 확인하기」 모의실험
     · T, n, V를 정하면 P = nRT/V (R 0.082). 용기 폭 ∝ V, 분자 수 12n, 속력 ∝ √T, 압력계 바늘. 「측정 기록」→ 조건 표(최근 4행)와 PV/nT
   em11gasid : 탐구(16–17쪽, 필수 탐구 물01-탐1) 「기체의 종류를 확인할 수 있는 실험을 설계하고 수행하기」
     · 용기 1(산소 32), 용기 2(헬륨 4) · 측정할 값 w, V, T, P를 고름(설계) — 빠지면 M을 구하지 못함 · 수증기압 빼기(기본 켬)
     · 모을 부피 100–500 mL, 실험실 온도 15–30 °C. 측정: V(5 mL 눈금), w(0.01 g 저울, 물기 오차 0–0.01 g), 대기압 758–762 mmHg(고정 시드)
     · 실제 질량 w = M·(P대기 − P수증기)·V/(R·T). 계산 M = wRT/PV. 결과 표(최근 5행) + 몰질량 눈금(산소 32, 헬륨 4 표시)에 용기별 평균 */
window.DECK_LABS = {
  em11pvnt(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('svg'), R=0.082;
    const gBox=API.mk('g',{},svg), gP=API.mk('g',{},svg), gG=API.mk('g',{},svg);
    let parts=[], log=[], box={x:30,y:40,w:300,h:190};
    const prng=(s=>()=>{ s=(s*48271)%2147483647; return s/2147483647; })(5);
    const st=()=>({T:+I('T').value, n:+I('n').value, V:+I('V').value});
    function draw(){
      const s=st(), P=s.n*R*s.T/s.V;
      box.w=40+s.V*9.5; gBox.innerHTML=''; gG.innerHTML='';
      const f=API.clamp((s.T-200)/400,0,1), mix=(a,b)=>Math.round(a+(b-a)*f);
      API.mk('rect',{x:box.x,y:box.y,width:box.w,height:box.h,fill:`rgb(${mix(227,253)},${mix(238,226)},${mix(251,228)})`,stroke:'#7E8B98','stroke-width':3},gBox);
      API.mk('rect',{x:box.x+box.w,y:box.y-6,width:12,height:box.h+12,rx:2,fill:'#B7C2CE',stroke:'#7E8B98','stroke-width':2},gBox);
      // 압력계
      const cx=560, cy=150, r=80, a0=Math.PI*0.8, a1=Math.PI*2.2, ang=a0+(a1-a0)*API.clamp(P/8,0,1);
      API.mk('circle',{cx,cy,r,fill:'#fff',stroke:'#7E8B98','stroke-width':3},gG);
      for(let k=0;k<=8;k++){ const a=a0+(a1-a0)*k/8; API.mk('line',{x1:cx+(r-12)*Math.cos(a),y1:cy+(r-12)*Math.sin(a),x2:cx+r*Math.cos(a),y2:cy+r*Math.sin(a),stroke:'#5B6B7F','stroke-width':2},gG); }
      API.mk('line',{x1:cx,y1:cy,x2:cx+(r-18)*Math.cos(ang),y2:cy+(r-18)*Math.sin(ang),stroke:'#D7263D','stroke-width':4,'stroke-linecap':'round'},gG);
      API.mk('circle',{cx,cy,r:6,fill:'#16233D'},gG);
      API.mk('path',{d:`M${box.x+box.w/2} ${box.y} V20 H${cx} V${cy-r}`,fill:'none',stroke:'#7E8B98','stroke-width':4},gG);
      const want=Math.round(12*s.n);
      while(parts.length<want) parts.push({x:box.x+10+prng()*(box.w-20), y:box.y+10+prng()*(box.h-20), a:prng()*6.283, el:API.mk('circle',{r:8,fill:'#6C8EBF',stroke:'#3E5F8F','stroke-width':1.5},gP)});
      while(parts.length>want) parts.pop().el.remove();
      parts.forEach(p=>{ p.x=API.clamp(p.x,box.x+9,box.x+box.w-9); if(window.__STILL) p.x=box.x+10+prng()*(box.w-20); p.el.setAttribute('cx',p.x.toFixed(1)); p.el.setAttribute('cy',p.y.toFixed(1)); });
      draw.sp=60*Math.sqrt(s.T/300);
      O('T').textContent=s.T+' K'; O('n').textContent=s.n.toFixed(2)+' mol'; O('V').textContent=s.V.toFixed(1)+' L';
      O('P').textContent=P.toFixed(2)+' atm';
    }
    function table(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-4).forEach((r,i)=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>조건 ${log.length-Math.min(log.length,4)+i+1}</td><td>${r.P.toFixed(2)}</td><td>${r.T}</td><td>${r.n.toFixed(2)}</td><td>${r.V.toFixed(1)}</td><td>${(r.P*r.V/(r.n*r.T)).toFixed(3)}</td>`; tb.appendChild(tr); });
      if(log.length>=2){ const a=log[log.length-2], b=log[log.length-1];
        O('msg').textContent=`PV/nT 값이 조건에 관계없이 약 ${(b.P*b.V/(b.n*b.T)).toFixed(3)}로 일정하다. 바로 앞 조건보다 압력이 ${(b.P/a.P).toFixed(2)}배가 되었다.`; }
      else O('msg').textContent='세 값을 정하고 「측정 기록」을 눌러 조건을 쌓아 보자. 온도와 양을 각각 2배로 하면?'; }
    ['T','n','V'].forEach(k=>I(k).addEventListener('input',draw));
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const s=st(); log.push({...s,P:Math.round(s.n*R*s.T/s.V*100)/100}); if(log.length>8) log.shift(); table(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ I('T').value=300; I('n').value=1; I('V').value=20; log=[]; draw(); table(); });
    draw(); table();
    if(!window.__STILL) API.loop(root,dt=>{ dt=Math.min(dt,.05); const sp=draw.sp;
      parts.forEach(p=>{ p.x+=Math.cos(p.a)*sp*dt; p.y+=Math.sin(p.a)*sp*dt;
        if(p.x<box.x+9){p.x=box.x+9;p.a=Math.PI-p.a;} if(p.x>box.x+box.w-9){p.x=box.x+box.w-9;p.a=Math.PI-p.a;}
        if(p.y<box.y+9){p.y=box.y+9;p.a=-p.a;} if(p.y>box.y+box.h-9){p.y=box.y+box.h-9;p.a=-p.a;}
        p.el.setAttribute('cx',p.x.toFixed(1)); p.el.setAttribute('cy',p.y.toFixed(1)); }); });
  },

  em11gasid(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=root.querySelector('svg'), R=0.082, MM={1:32,2:4};
    const PW=[[15,12.8],[20,17.5],[25,23.8],[30,31.8]];
    const pw=t=>{ for(let i=0;i<PW.length-1;i++){ const [a,pa]=PW[i],[b,pb]=PW[i+1]; if(t<=b) return pa+(pb-pa)*(t-a)/(b-a); } return 31.8; };
    let c=1, log=[], seed=13, anim=0, gas=0;
    const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    const gApp=API.mk('g',{},svg), gB=API.mk('g',{},svg), gS=API.mk('g',{},svg);
    const CYX=170, CYW=50, CYT=24, CYB=200;          // 눈금실린더 (500 mL = CYB-CYT-20 px)
    const SX=330, SW=310, SY=130;                    // 몰질량 눈금 0–40
    const MX=v=>SX+v/40*SW;
    function app(){
      gApp.innerHTML='';
      API.mk('rect',{x:80,y:140,width:230,height:80,fill:'#DDEEF8'},gApp);
      API.mk('path',{d:'M74 118 V226 H316 V118',fill:'none',stroke:'#7E8B98','stroke-width':3},gApp);
      const gh=(CYB-CYT-20)*gas/500;
      API.mk('rect',{x:CYX,y:CYT,width:CYW,height:CYB-CYT,fill:'#DDEEF8'},gApp);
      API.mk('rect',{x:CYX,y:CYT,width:CYW,height:gh,fill:'#F7F9FB'},gApp);
      API.mk('path',{d:`M${CYX} ${CYB} V${CYT} H${CYX+CYW} V${CYB}`,fill:'none',stroke:'#7E8B98','stroke-width':3},gApp);
      for(let k=0;k<=5;k++){ const y=CYT+(CYB-CYT-20)*k/5; API.mk('line',{x1:CYX,y1:y,x2:CYX+12,y2:y,stroke:'#5B6B7F','stroke-width':1.5},gApp); }
      API.mk('rect',{x:16,y:110,width:40,height:78,rx:8,fill:c===1?'#C9D3DD':'#D9E6EE',stroke:'#7E8B98','stroke-width':2},gApp);
      API.mk('rect',{x:30,y:98,width:12,height:12,fill:'#8C99A6'},gApp);
      API.mk('path',{d:`M36 98 Q40 60 110 70 Q150 80 150 150 Q150 196 ${CYX+20} 194`,fill:'none',stroke:'#B0661A','stroke-width':4},gApp);
    }
    function scale(){
      gS.innerHTML='';
      API.arrow(gS,SX,SY,SX+SW+16,SY,'muted',2);
      [0,10,20,30,40].forEach(v=>{ API.mk('line',{x1:MX(v),y1:SY,x2:MX(v),y2:SY+7,stroke:'#5B6B7F','stroke-width':2},gS); });
      [[4,'#E08A2C'],[32,'#2E9E6A']].forEach(([v,col])=>{ API.mk('line',{x1:MX(v),y1:SY-50,x2:MX(v),y2:SY,stroke:col,'stroke-width':2,'stroke-dasharray':'5 4'},gS); });
      ['1','2'].forEach(k=>{ const rows=log.filter(r=>r.c==+k&&r.M); if(!rows.length){ API.place(Ov(k==='1'?'ma':'mb'),0,0,false); return; }
        const m=rows.reduce((s,r)=>s+r.M,0)/rows.length, y=k==='1'?SY-30:SY-62;
        API.mk('circle',{cx:MX(Math.min(m,40)),cy:SY,r:8,fill:k==='1'?'#16233D':'#7B4FC8'},gS);
        const ov=Ov(k==='1'?'ma':'mb'); ov.textContent=`용기 ${k} 평균 ${m.toFixed(1)}`; ov.style.color=k==='1'?'#16233D':'#7B4FC8'; API.place(ov,API.clamp(MX(Math.min(m,40)),SX+60,SX+SW-60),k==='1'?SY+40:SY-80); });
    }
    function labels(){ }
    function update(){ O('Vt').textContent=I('Vt').value+' mL'; O('tc').textContent=I('tc').value+' °C ('+(+I('tc').value+273)+' K)'; root.querySelectorAll('[data-c]').forEach(b=>b.classList.toggle('on',+b.dataset.c===c)); app(); }
    function table(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-5).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>용기 ${r.c}</td><td>${r.w??'—'}</td><td>${r.V??'—'}</td><td>${r.T??'—'}</td><td>${r.P??'—'}</td><td>${r.M?r.M.toFixed(1):'?'}</td>`; tb.appendChild(tr); }); scale(); }
    root.querySelectorAll('[data-c]').forEach(b=>b.addEventListener('click',()=>{ c=+b.dataset.c; gas=0; update(); }));
    ['Vt','tc'].forEach(k=>I(k).addEventListener('input',update));
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{
      const m={}; root.querySelectorAll('[data-m]').forEach(x=>m[x.dataset.m]=x.checked);
      const t=+I('tc').value, T=t+273, Vt=+I('Vt').value, Patm=758+Math.round(rnd()*4), Pw=pw(t);
      const V=Math.round((Vt+(rnd()-.5)*8)/5)*5;
      const wTrue=MM[c]*((Patm-Pw)/760)*(V/1000)/(R*T);
      const w=Math.round((wTrue+rnd()*0.01)*100)/100;
      const Pg=(Patm-(m.pw?Pw:0))/760;
      const row={c, w:m.w?w.toFixed(2):null, V:m.V?V:null, T:m.t?T:null, P:m.P?Pg.toFixed(3):null, M:null};
      const miss=['w','V','t','P'].filter(k=>!m[k]).map(k=>({w:'질량 w',V:'부피 V',t:'온도 T',P:'압력 P'})[k]);
      if(!miss.length && w>0) row.M=w*R*T/(Pg*V/1000);
      log.push(row); if(log.length>10) log.shift();
      gas=V; anim=1.2; app(); table();
      if(miss.length) O('msg').textContent=`M = wRT/PV를 구하려면 ${miss.join(', ')}도 측정해야 한다. 측정할 값을 다시 설계하자.`;
      else { const rows=log.filter(r=>r.c===c&&r.M), avg=rows.reduce((s,r)=>s+r.M,0)/rows.length, near=Math.abs(avg-32)<Math.abs(avg-4)?'산소(32 g/mol)':'헬륨(4 g/mol)';
        O('msg').textContent=`용기 ${c}: 평균 몰질량 약 ${avg.toFixed(1)} g/mol → ${near}에 가깝다.`+(m.pw?'':' (수증기압을 빼지 않으면 몰질량이 조금 작게 나온다.)')+(c===2?' 질량 감소가 작아 저울 눈금(0.01 g) 오차가 크다.':''); }
    });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; c=1; gas=0; seed=13; I('Vt').value=450; I('tc').value=20;
      root.querySelectorAll('[data-m]').forEach(x=>x.checked=x.dataset.m==='pw'); update(); table(); O('msg').textContent='측정할 값을 고르고 「기체 모으고 측정」을 누르자.'; });
    update(); table(); O('msg').textContent='측정할 값을 고르고 「기체 모으고 측정」을 누르자.';
    (()=>{ [['0',0],['10',10],['20',20],['30',30],['40',40]].forEach(([s,v])=>{ API.texText(svg,MX(v),SY+28,s,{size:18,anchor:'middle'}); });
      API.texText(svg,SX+SW,SY+60,'$M$ [g/mol]',{size:19,anchor:'end',mix:true}); API.texText(svg,MX(32),SY-56,'산소',{size:18,anchor:'middle',mix:true,fill:'#2E9E6A'}); API.texText(svg,MX(4)+6,SY-56,'헬륨',{size:18,anchor:'start',mix:true,fill:'#A65A10'}); })();
    if(!window.__STILL) API.loop(root,dt=>{ if(anim<=0) return; anim-=dt;
      gB.innerHTML=''; for(let k=0;k<4;k++){ const y=196-((1.2-anim)*120+k*30)%60; API.mk('circle',{cx:CYX+22+k%2*8,cy:y,r:4,fill:'#fff',stroke:'#9FC3DD','stroke-width':1.5},gB); } if(anim<=0) gB.innerHTML=''; });
  }
};
