/* 2-4 전기 분해 — 실험실
   rm24plate : 금속 제품 표면에 도금하기 (필수 탐구 반02-탐2)
     · 도금할 금속(은: 은판 + 은 이온 용액 / 구리: 구리판 + 황산 구리(II) 수용액), 도금할 물체(구리 펜던트 / 철 숟가락),
       물체 연결((−)극 / (+)극), 건전지 수 1–3개(1.5–4.5 V), 도금 시간 0–20분
     · 전류 = (전압 − 0.5 V) ÷ 50 Ω (설정마다 고정된 ±2 % 오차), 흐른 전자의 양 = 전류 × 시간 ÷ 96500 C/mol
     · 석출 질량 = 전자의 양 ÷ (이온의 전하 수) × 몰질량(은 108, 구리 63.5, 철 56 g/mol) (±1 % 저울 오차)
     · 「측정·기록」→ 기록 표(최근 3행) + 그래프(흐른 전자의 양–석출 질량)에 점, 「초기화」 */
window.DECK_LABS = {
  rm24plate(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const MET={Ag:{nm:'은',M:108,n:1,f:'#DDE1E6',s:'#8C99A6',coat:'#E4E8EC',sol:'\\ce{K[Ag(CN)2]}\\ \\text{용액}',sc:'#DDEEF8',so:1,plate:'은판'},
               Cu:{nm:'구리',M:63.5,n:2,f:'#E6C29C',s:'#B0835A',coat:'#C8743F',sol:'\\ce{CuSO4(aq)}',sc:'#3E8ED0',so:.3,plate:'구리판'}};
    const OBJ={Cu:{nm:'구리 펜던트',M:63.5,n:2,f:'#D9925E',s:'#A0623A'},Fe:{nm:'철 숟가락',M:56,n:2,f:'#8C8F94',s:'#5B6B7F'}};
    let m='Ag', ob='Cu', cn='n', log=[];
    const ap=$('svg.rm24-ap'), gr=$('svg.rm24-gr'), gd=API.mk('g',{},ap), ge=API.mk('g',{},ap), gg=API.mk('g',{},gr);
    const eds=[]; for(let i=0;i<8;i++) eds.push(API.mk('circle',{r:4.5,fill:API.COL.minus},ge));
    const ids=[]; for(let i=0;i<5;i++) ids.push(API.mk('circle',{r:6,fill:'#FDE2E4',stroke:API.COL.plus,'stroke-width':2},ge));
    let cur=0;
    const hash=s=>[...s].reduce((a,c)=>(a*31+c.charCodeAt(0))%9973,7);
    function model(){
      const k=+$('[data-i="k"]').value, t=+$('[data-i="t"]').value, h=hash(m+ob+cn+k+t);
      const V=1.5*k, I=(V-0.5)/50*(1+((h%41)-20)/1000);           // A
      const ne=I*t*60/96500*1000;                                    // mmol
      const wm=1+(((h>>3)%21)-10)/1000;
      const dep=ne/MET[m].n*MET[m].M*wm;                             // mg, 석출되는 입힐 금속
      let dm, da, ions;
      if(cn==='n'){ dm=dep; da=-ne/MET[m].n*MET[m].M; ions=`${MET[m].nm} 이온 수 일정 — 녹아 나온 만큼 석출`; }
      else { dm=-ne/OBJ[ob].n*OBJ[ob].M*wm; da=dep;
        ions = (m===ob) ? `${MET[m].nm} 이온 수 일정 — 물체가 녹아 이온을 채움` : `${MET[m].nm} 이온 감소, ${ob==='Cu'?'구리':'철'} 이온 생김`; }
      if(t===0) ions='변화 없음';
      return {k,t,V,I,ne,dm,da,ions,dep};
    }
    const f1=x=>(x>0?'+':x<0?'−':'')+Math.abs(x).toFixed(1);
    function draw(){
      const q=model(); cur=q.t>0?q.I:0;
      while(gd.firstChild) gd.firstChild.remove();
      const D=(t,a)=>API.mk(t,a,gd);
      D('rect',{x:82,y:84,width:356,height:82,fill:MET[m].sc,'fill-opacity':MET[m].so});
      D('path',{d:'M74 64 H80 V158 Q80 168 90 168 H430 Q440 168 440 158 V64 H446',fill:'none',stroke:'#7E8B98','stroke-width':3,'stroke-linejoin':'round'});
      D('path',{d:'M150 48 V24 H252 M268 24 H370 V48',fill:'none',stroke:API.COL.ink,'stroke-width':3});
      D('line',{x1:268,y1:4,x2:268,y2:44,stroke:API.COL.ink,'stroke-width':3}); D('line',{x1:252,y1:13,x2:252,y2:35,stroke:API.COL.ink,'stroke-width':6});
      D('path',{d:'M278 8 H290 M284 2 V14',stroke:API.COL.plus,'stroke-width':3}); D('path',{d:'M230 8 H242',stroke:API.COL.minus,'stroke-width':3});
      const xo = cn==='n'?150:370, xp = cn==='n'?370:150;           // 물체 / 금속판 위치
      // 금속판
      const pl = cn==='n' ? Math.min(10,-q.da/12) : 0, pw=24-pl;
      D('rect',{x:xp-pw/2,y:48,width:pw,height:112,rx:3,fill:MET[m].f,stroke:MET[m].s,'stroke-width':2});
      if(cn==='p' && q.da>0) D('rect',{x:xp-14,y:76,width:28,height:84,rx:4,fill:MET[m].coat,'fill-opacity':Math.min(1,q.da/20),stroke:MET[m].s,'stroke-width':1.5});
      // 물체
      const O1=OBJ[ob], cov = cn==='n' ? Math.min(1,q.dm/(m==='Ag'?20:8)) : 0;
      const shape=(f,s,op,sw)=>{ if(ob==='Cu'){ D('circle',{cx:xo,cy:128,r:22,fill:f,'fill-opacity':op,stroke:s,'stroke-width':sw}); }
        else { D('rect',{x:xo-4,y:56,width:8,height:72,rx:3,fill:f,'fill-opacity':op,stroke:s,'stroke-width':sw}); D('ellipse',{cx:xo,cy:142,rx:14,ry:20,fill:f,'fill-opacity':op,stroke:s,'stroke-width':sw}); } };
      D('line',{x1:xo,y1:48,x2:xo,y2:ob==='Cu'?106:58,stroke:'#5B6B7F','stroke-width':3});
      shape(O1.f,O1.s,1,2.5);
      if(cov>0) shape(MET[m].coat,MET[m].s,cov,3);
      if(cn==='p' && q.dm<0){ const np=Math.min(9,Math.round(-q.dm/3)); for(let i=0;i<np;i++){ const a=i*2.4, r=ob==='Cu'?12:9; D('circle',{cx:xo+Math.cos(a)*r,cy:(ob==='Cu'?128:142)+Math.sin(a)*r,r:2.6,fill:'#3A3F47'}); } }
      // 전자 화살표: (+)극 → 전원 (+)단자, 전원 (−)단자 → (−)극 (왼쪽으로)
      const on=cur>0;
      if(on){ API.arrow(gd,350,38,292,38,API.COL.minus,3); API.arrow(gd,232,38,172,38,API.COL.minus,3); }
      API.place(V('e1'),320,54,on); API.place(V('e2'),202,54,on);
      V('mL').textContent = cn==='n'? O1.nm : MET[m].plate; V('mR').textContent = cn==='n'? MET[m].plate : O1.nm;
      API.place(V('mL'),88,40); API.place(V('mR'),432,40);
      V('sol').innerHTML=API.tex(MET[m].sol); API.place(V('sol'),260,152);
      API.place(V('pL'),150,186); API.place(V('pR'),370,186);
      V('vm').textContent=(1.5*q.k).toFixed(1)+' V'; API.place(V('vm'),260,58);
      O('k').textContent=`${q.k}개 · ${(1.5*q.k).toFixed(1)} V`; O('t').textContent=q.t+'분';
      O('i').textContent=(q.t>0?Math.round(q.I*1000):0)+' mA'; O('ne').textContent=q.ne.toFixed(2)+' mmol';
      O('dm').textContent=f1(q.dm)+' mg'; O('da').textContent=f1(q.da)+' mg'; O('ions').textContent=q.ions;
      let msg;
      if(q.t===0) msg='도금 시간을 늘려 전류를 흘려 보자. 전원이 켜져야 산화·환원 반응이 일어난다.';
      else if(cn==='p') msg=`물체가 (+)극(산화 전극)에 연결되어 ${O1.nm}의 금속이 산화되어 녹아 나온다(${f1(q.dm)} mg). ${MET[m].nm}은 (−)극의 ${MET[m].plate}에 석출된다 — 도금 실패, 연결을 바꾸자.`;
      else if(m==='Cu' && ob==='Cu') msg=`구리 펜던트에 구리가 ${q.dm.toFixed(1)} mg 석출된다(환원). 같은 금속이라 색은 그대로지만 질량은 늘어난다.`;
      else msg=`(−)극 ${O1.nm} 표면에서 ${MET[m].nm} 이온이 전자를 얻어 ${MET[m].nm}으로 석출(환원), (+)극 ${MET[m].plate}은 산화되어 녹는다. 표면의 ${Math.round(cov*100)} %가 ${m==='Ag'?'은색':'구리색'}${cov>=1?' — 도금 완료':''}.`;
      if(!O('msg').dataset.keep) O('msg').textContent=msg;
      ['m','b','c'].forEach(kk=>root.querySelectorAll(`[data-${kk}]`).forEach(x=>x.classList.toggle('on', x.dataset[kk]===({m,b:ob,c:cn})[kk])));
      graph(); tick(window.__STILL?0:performance.now()/1000);
    }
    function graph(){
      while(gg.firstChild) gg.firstChild.remove();
      const X=n=>60+n/1.2*440, Y=w=>104-w/120*94;
      ['Ag','Cu'].forEach(k=>{ if(!log.some(r=>r.m===k&&r.ok)) return;
        const s=MET[k].M/MET[k].n, n1=Math.min(1.2,120/s);
        API.mk('line',{x1:X(0),y1:Y(0),x2:X(n1),y2:Y(n1*s),stroke:k==='Ag'?'#16233D':'#B0835A','stroke-width':2,'stroke-dasharray':'6 5',opacity:.6},gg); });
      log.forEach(r=>{ if(!r.ok||r.ne<=0) return; const x=X(r.ne), y=Y(Math.min(120,r.dm));
        if(r.m==='Ag') API.mk('circle',{cx:x,cy:y,r:6,fill:'#16233D'},gg); else API.mk('rect',{x:x-6,y:y-6,width:12,height:12,fill:'#B0835A'},gg); });
    }
    function tick(t){
      const on=cur>0, sp=on?cur*1000/80:0;   // 80 mA에서 1
      // 전자: x 370 → 150 (y 48→24, 24 위 왼쪽, 24→48)
      const L=24+220+24;
      eds.forEach((c,i)=>{ if(!on){ c.setAttribute('opacity',0); return; }
        const s=(i*L/8+t*44*sp)%L; let x,y;
        if(s<24){ x=370; y=48-s; } else if(s<244){ x=370-(s-24); y=24; } else { x=150; y=24+(s-244); }
        c.setAttribute('cx',x); c.setAttribute('cy',y); c.setAttribute('opacity',(y===24&&x>244&&x<276)?0:1); });
      ids.forEach((c,i)=>{ if(!on){ c.setAttribute('opacity',0); return; }
        const s=(i*190/5+t*30*sp)%190; c.setAttribute('cx',356-s); c.setAttribute('cy',100+((i*23)%50)); c.setAttribute('opacity',1); });
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-3).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${r.n}</td><td>${MET[r.m].nm}</td><td>${r.ok?'(−)극':'(+)극'}</td><td>${r.k}개</td><td>${r.t}분</td><td>${r.ne.toFixed(2)}</td><td>${f1(r.dm)}</td><td>${r.ok&&r.ne>0?(r.dm/r.ne).toFixed(0):'—'}</td>`; tb.appendChild(tr); }); }
    const on=(sel,fn)=>root.querySelectorAll(sel).forEach(x=>x.addEventListener('click',()=>{ fn(x); delete O('msg').dataset.keep; draw(); }));
    on('[data-m]',x=>m=x.dataset.m); on('[data-b]',x=>ob=x.dataset.b); on('[data-c]',x=>cn=x.dataset.c);
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',()=>{ delete O('msg').dataset.keep; draw(); }));
    $('[data-act="rec"]').addEventListener('click',()=>{
      const q=model();
      log.push({n:log.length+1,m,ok:cn==='n',k:q.k,t:q.t,ne:q.ne,dm:q.dm,key:m+ob+cn+q.k+q.t});
      renderLog(); draw();
      const good=log.filter(r=>r.ok&&r.ne>0), nk=new Set(good.map(r=>r.key)).size, msg=O('msg');
      const avg=k=>{ const a=good.filter(r=>r.m===k); return a.length? (a.reduce((s,r)=>s+r.dm/r.ne,0)/a.length).toFixed(0) : null; };
      if(!cn.startsWith('n')) msg.textContent='물체를 (+)극에 연결한 기록이다 — 물체의 질량이 줄었다. 도금하려면 물체를 (−)극에 연결해야 한다.';
      else if(nk>=3){ const a=avg('Ag'), c=avg('Cu');
        msg.textContent=`기록 ${nk}가지: 석출 질량 ÷ 흐른 전자의 양이 ${a?'은 약 '+a:''}${a&&c?', ':''}${c?'구리 약 '+c:''} (mg/mmol)로 일정 → 석출 질량은 흐른 전자의 양에 비례한다.${a&&c?' 은 이온은 전자 1개, 구리 이온은 전자 2개로 원자 1개가 된다.':' 다른 금속으로도 비교해 보자.'}`; }
      else msg.textContent=`기록 ${nk}가지 — 건전지 수와 시간을 바꾸어 더 측정해 보자 (${nk}/3).`;
      msg.dataset.keep='1'; });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); m='Ag'; ob='Cu'; cn='n'; $('[data-i="k"]').value=3; $('[data-i="t"]').value=10; delete O('msg').dataset.keep; draw(); });
    API.onShow&&API.onShow(()=>draw());
    API.ready&&API.ready(()=>draw());
    draw();
    if(!window.__STILL) API.loop(root,()=>tick(performance.now()/1000));
  }
};
