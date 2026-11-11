/* 2-3 삼투 현상 — 실험실
   em23osmo : 농도와 삼투 현상의 관계를 찾기 위한 실험 설계·수행 (필수 탐구 물02-탐2)
     · 조작 변인 고르기(튜브 속 농도 / 비커 속 농도 / 튜브 길이 / 물의 온도) — 나머지는 통제 변인(기준값)
     · 종속 변인 고르기(빨대 속 물 높이 변화 h [cm] / 튜브 질량 변화 Δm [g])
     · 튜브로 들어온 물의 부피 V [mL]: dV/dt = K·L·fT·(c튜브·V0/(V0+V) − c비커), K = 0.0135, V0 = 20 mL,
       fT = 1 + 0.02(t − 25), 0.05 분 간격으로 0 → 20 분 적분.  h = 3V (하한 −3 cm), Δm = V (물 1 g/mL)
     · 측정 오차: 값마다 고정 시드 ±0.1
     · 「실험 시작」 → 약 5 s 동안 두 장치·시간 그래프가 변함, 「결과 기록」 → 표·결과 그래프에 쌓임, 「초기화」 */
window.DECK_LABS = {
  em23osmo(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), still=()=>!!window.__STILL||document.documentElement.classList.contains('still');
    const INK='#16233D', EQ='#E08A2C', MUT='#5B6B7F', GRID='#E2E7EC', GLASS='#7E8B98', WAT='#DDEEF8', WTOP='#9FC3DD', SOL='#8FB8DE', SOLS='#5B8DB8', RUB='#8C6D46';
    const BASE={ci:0.5,co:0,L:15,T:25};
    const MODE={
      ci:{name:'튜브 속 농도',min:0,max:1,step:0.1,a:0.2,b:0.6,f:v=>v.toFixed(1)+' M'},
      co:{name:'비커 속 농도',min:0,max:1,step:0.1,a:0,b:0.3,f:v=>v.toFixed(1)+' M'},
      L:{name:'튜브 길이',min:5,max:20,step:5,a:10,b:15,f:v=>v.toFixed(0)+' cm'},
      T:{name:'물의 온도',min:10,max:40,step:5,a:15,b:35,f:v=>v.toFixed(0)+' °C'}};
    const YR={h:[-4,20],m:[-6,8]};
    function sim(p){ // 0, 0.5, …, 20 분의 V
      const K=0.0135,V0=20,fT=1+0.02*(p.T-25),out=[0]; let v=0;
      for(let i=1;i<=400;i++){ v+=0.05*K*p.L*fT*(p.ci*V0/(V0+v)-p.co); v=Math.max(v,-0.8*V0); if(i%10===0) out.push(v); }
      return out; }
    const eps=k=>{ let s=0; for(const c of k) s=(s*31+c.charCodeAt(0))%9973; return ((s%5)-2)*0.05; };
    const meas=(v,y,key)=> y==='h' ? Math.max(-3,3*v) + (v? eps(key+y):0) : v + (v? eps(key+y):0);
    // 좌표
    const DEV=[{cx:82,c:INK,n:'(가)',ov:'ca'},{cx:222,c:EQ,n:'(나)',ov:'cb'}], BY=196, TT=116, TB=180, H0=108, PX=5.5;
    const A={x0:372,x1:620,y0:196,y1:50}, C={x0:74,x1:620,y0:416,y1:314};
    const XR={ci:[-1,1],co:[-1,1],L:[0,20],T:[0,40]};
    const ax=t=>A.x0+(A.x1-A.x0)*t/20, ay=(y,v)=>A.y0-(A.y0-A.y1)*(v-YR[y][0])/(YR[y][1]-YR[y][0]);
    const cxp=(m,x)=>C.x0+(C.x1-C.x0)*(x-XR[m][0])/(XR[m][1]-XR[m][0]), cyp=(y,v)=>C.y0-(C.y0-C.y1)*(v-YR[y][0])/(YR[y][1]-YR[y][0]);
    // 고정 그림
    const base=API.mk('g',{},svg);
    DEV.forEach(d=>{ const x=d.cx-55,w=110,y=BY-104;
      API.mk('rect',{x:x+2,y:y+18,width:w-4,height:84,fill:WAT},base); API.mk('line',{x1:x+2,y1:y+18,x2:x+w-2,y2:y+18,stroke:WTOP,'stroke-width':2},base);
      API.mk('path',{d:`M${x-6} ${y} Q${x} ${y} ${x} ${y+8} V${BY-8} Q${x} ${BY} ${x+8} ${BY} H${x+w-8} Q${x+w} ${BY} ${x+w} ${BY-8} V${y}`,fill:'none',stroke:GLASS,'stroke-width':3,'stroke-linejoin':'round'},base);
      API.texText(base,d.cx,BY+20,d.n,{size:19,anchor:'middle',fill:d.c,mix:true}); });
    [A,C].forEach(P=>{ API.mk('line',{x1:P.x0,y1:P.y0,x2:P.x1+6,y2:P.y0,stroke:MUT,'stroke-width':2},base); API.mk('line',{x1:P.x0,y1:P.y0,x2:P.x0,y2:P.y1-8,stroke:MUT,'stroke-width':2},base); });
    [0,10,20].forEach(t=>API.texText(base,ax(t),A.y0+20,String(t),{size:18,anchor:'middle',fill:MUT}));
    API.texText(base,A.x1,A.y0+42,'$t$ [분]',{size:18,anchor:'end',mix:true});
    API.mk('line',{x1:A.x0+150,y1:A.y1-14,x2:A.x0+172,y2:A.y1-14,stroke:INK,'stroke-width':3},base); API.texText(base,A.x0+176,A.y1-8,'(가)',{size:18,mix:true});
    API.mk('line',{x1:A.x0+212,y1:A.y1-14,x2:A.x0+234,y2:A.y1-14,stroke:EQ,'stroke-width':3},base); API.texText(base,A.x0+238,A.y1-8,'(나)',{size:18,mix:true});
    // y 눈금(종속 변인별), x 눈금(조작 변인별) — 미리 만들고 켜고 끔
    const ytk={}, xtk={};
    ['h','m'].forEach(y=>{ const gY=API.mk('g',{},svg); ytk[y]=gY; const tk= y==='h'?[0,10,20]:[-5,0,5];
      tk.forEach(v=>{ [[A,ay],[C,cyp]].forEach(([P,f])=>{ API.mk('line',{x1:P.x0,y1:f(y,v),x2:P.x1,y2:f(y,v),stroke:v?GRID:'#AEB8C2','stroke-width':1.5},gY); API.texText(gY,P.x0-8,f(y,v)+6,String(v),{size:18,anchor:'end',fill:MUT}); }); });
      API.texText(gY,A.x0-40,20,y==='h'?'$h$ [cm]':'$\\Delta m$ [g]',{size:18,mix:true});
      API.texText(gY,10,290,y==='h'?'결과: 20분 뒤 빨대 속 물 높이 변화 $h$ [cm]':'결과: 20분 뒤 튜브 질량 변화 $\\Delta m$ [g]',{size:18,mix:true}); });
    ['ci','L','T'].forEach(m=>{ const gX=API.mk('g',{},svg); xtk[m]=gX; const tk= m==='ci'?[-1,-0.5,0,0.5,1]: m==='L'?[0,5,10,15,20]:[0,10,20,30,40];
      tk.forEach(v=>API.texText(gX,cxp(m,v),C.y0+22,String(v),{size:18,anchor:'middle',fill:MUT}));
      API.texText(gX,C.x1,C.y0+50,m==='ci'?'농도 차 (튜브 − 비커) [M]':m==='L'?'튜브 길이 [cm]':'물의 온도 [°C]',{size:18,anchor:'end',mix:true}); });
    xtk.co=xtk.ci;
    const g=API.mk('g',{},svg), top=API.mk('g',{},svg);
    DEV.forEach(d=>{ API.mk('rect',{x:d.cx-7,y:14,width:14,height:TT+8-14,fill:'none',stroke:GLASS,'stroke-width':2.5},top);
      API.mk('rect',{x:d.cx-10,y:TT,width:20,height:7,rx:2,fill:RUB},top);
      API.mk('line',{x1:d.cx-14,y1:H0,x2:d.cx-8,y2:H0,stroke:'#D7263D','stroke-width':2},top); });
    API.texText(top,20,H0+6,'처음',{size:18,mix:true,fill:'#D7263D'});
    let st={m:'ci',y:'h',prog:1,note:''}, log=[];
    const val=k=>+I(k).value;
    function params(v){ const p=Object.assign({},BASE); p[st.m]=v; return p; }
    function setMode(m){ st.m=m; const M=MODE[m]; ['a','b'].forEach(k=>{ const i=I(k); i.min=M.min; i.max=M.max; i.step=M.step; i.value=M[k]; }); }
    function dc(p){ return p.ci-p.co; }
    function draw(){
      const m=st.m,y=st.y,M=MODE[m],done=st.prog>=1,ti=Math.round(40*Math.min(1,st.prog));
      root.querySelectorAll('[data-v]').forEach(b=>b.classList.toggle('on',b.dataset.v===m));
      root.querySelectorAll('[data-y]').forEach(b=>b.classList.toggle('on',b.dataset.y===y));
      ytk.h.style.display= y==='h'?'':'none'; ytk.m.style.display= y==='m'?'':'none';
      ['ci','L','T'].forEach(k=>xtk[k].style.display= (k===m||(k==='ci'&&m==='co'))?'':'none');
      O('la').textContent='(가) '+M.name; O('lb').textContent='(나) '+M.name;
      const va=val('a'), vb=val('b'); O('a').textContent=M.f(va); O('b').textContent=M.f(vb);
      const ctl=[]; if(m!=='ci') ctl.push('튜브 속 0.5 M'); if(m!=='co') ctl.push('비커 속 증류수'); if(m!=='L') ctl.push('튜브 15 cm'); if(m!=='T') ctl.push('물 25 °C');
      O('ctrl').textContent='통제 변인: '+ctl.join(' · ')+' · 20 mL · 20분';
      while(g.firstChild) g.removeChild(g.firstChild);
      const res=[va,vb].map((v,i)=>{ const p=params(v), s=sim(p); return {p,s,key:m+v.toFixed(2)}; });
      res.forEach((r,i)=>{ const d=DEV[i], vol=r.s[ti], hh=Math.max(-3,3*vol);
        const rx=15*(1+0.5*vol/20), ry=(TB-TT)/2;
        API.mk('ellipse',{cx:d.cx,cy:(TT+TB)/2+4,rx:Math.max(9,rx),ry:ry,fill:SOL,stroke:SOLS,'stroke-width':2.5},g);
        API.mk('line',{x1:d.cx-6,y1:TB+8,x2:d.cx+6,y2:TB+8,stroke:RUB,'stroke-width':4},g);
        const ly=Math.min(TT+2,H0-PX*hh); API.mk('rect',{x:d.cx-5,y:ly,width:10,height:TT+6-ly,fill:SOL},g);
        V(d.ov).innerHTML=`튜브 ${r.p.ci.toFixed(1)} M<br>비커 ${r.p.co.toFixed(1)} M`; API.place(V(d.ov),d.cx,BY+50,true);
        // 시간 그래프
        let path=''; for(let k=0;k<=ti;k++){ const vv= y==='h'?Math.max(-3,3*r.s[k]):r.s[k]; path+=(k?'L':'M')+ax(k*0.5).toFixed(1)+' '+ay(y,vv).toFixed(1)+' '; }
        API.mk('path',{d:path,fill:'none',stroke:d.c,'stroke-width':3},g);
        const vv= y==='h'?hh:vol; API.mk('circle',{cx:ax(ti*0.5),cy:ay(y,vv),r:5,fill:d.c},g); });
      // 결과 그래프: 기록 점
      const pts=log.filter(r=>r.m===m&&r.y===y), xv=r=> (m==='ci'||m==='co')?r.dc:r.v;
      if(pts.length>=2){ const sp=pts.slice().sort((a,b)=>xv(a)-xv(b)); API.mk('polyline',{points:sp.map(r=>cxp(m,xv(r)).toFixed(1)+','+cyp(y,r.val).toFixed(1)).join(' '),fill:'none',stroke:MUT,'stroke-width':2,'stroke-dasharray':'6 5'},g); }
      pts.forEach(r=>API.mk('circle',{cx:cxp(m,xv(r)),cy:cyp(y,r.val),r:6,fill:r.d===0?INK:EQ,stroke:'#fff','stroke-width':1.5},g));
      // 해석
      const msg=O('msg'), un= y==='h'?' cm':' g', ma=meas(res[0].s[40],y,res[0].key), mb=meas(res[1].s[40],y,res[1].key);
      if(!done) msg.textContent=`실험 중… (${(ti*0.5).toFixed(1)}분)`;
      else if(st.note) msg.textContent=st.note;
      else if(va===vb) msg.textContent='두 장치의 조작 변인 값이 같다 — 값을 다르게 해야 비교할 수 있다.';
      else { const big= mb>ma?'(나)':'(가)', txt=`20분 뒤 (가) ${ma.toFixed(1)}${un}, (나) ${mb.toFixed(1)}${un}. `;
        if(m==='ci'||m==='co'){ const neg=[ma,mb].some(v=>v<0)?' 비커 쪽이 더 진한 장치는 물이 튜브 밖으로 더 많이 이동했다(튜브가 쪼그라듦).':'';
          msg.textContent=txt+`농도 차가 더 큰 ${big}에서 삼투 현상이 더 잘 일어났다.`+neg; }
        else msg.textContent=txt+(m==='L'?'튜브가 길수록(막이 넓을수록) 물이 더 많이 들어왔다':'온도가 높을수록 물이 더 빨리 들어왔다')+' — 이 설계로는 농도와의 관계를 알 수 없다.'; }
    }
    function table(){ const tb=O('log'); tb.innerHTML=''; log.slice(-2).forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${r.d?'(나)':'(가)'}</td><td>${MODE[r.m].f(r.v)}</td><td>${r.dc.toFixed(1)} M</td><td>${r.val.toFixed(1)} ${r.y==='h'?'cm':'g'}</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-v]').forEach(b=>b.addEventListener('click',()=>{ setMode(b.dataset.v); st.prog=1; st.note=''; draw(); }));
    root.querySelectorAll('[data-y]').forEach(b=>b.addEventListener('click',()=>{ st.y=b.dataset.y; st.note=''; draw(); }));
    ['a','b'].forEach(k=>I(k).addEventListener('input',()=>{ st.prog=1; st.note=''; draw(); }));
    $('[data-act="run"]').addEventListener('click',()=>{ st.prog= still()?1:0; st.note=''; draw(); });
    $('[data-act="rec"]').addEventListener('click',()=>{
      if(st.prog<1){ O('msg').textContent='실험이 끝난 뒤(20분) 기록하자.'; return; }
      [val('a'),val('b')].forEach((v,d)=>{ const p=params(v), s=sim(p), key=st.m+v.toFixed(2);
        if(!log.some(r=>r.m===st.m&&r.y===st.y&&r.v===v)) log.push({m:st.m,y:st.y,v,d,dc:dc(p),val:meas(s[40],st.y,key)}); });
      table(); const n=log.filter(r=>r.m===st.m&&r.y===st.y).length;
      st.note= n>=3 ? (st.m==='ci'||st.m==='co' ? `기록 ${n}개: 농도 차가 클수록 측정값이 커진다 → 농도 차가 클수록 삼투 현상이 잘 일어난다.` : `기록 ${n}개: 조작 변인을 설탕물의 농도로 바꾸어 다시 설계해 보자.`) : '값을 바꾸어 한 번 더 실험하고 기록해 보자.';
      draw(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; st.note=''; table(); draw(); });
    setMode('ci'); draw();
    API.loop(root,dt=>{ if(st.prog<1 && !still()){ st.prog=Math.min(1,st.prog+dt/5); draw(); } });
  }
};
