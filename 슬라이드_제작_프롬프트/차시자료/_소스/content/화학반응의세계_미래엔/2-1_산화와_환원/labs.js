/* 2-1 산화와 환원 — 실험실
   rm21metal : 금속과 금속 이온 수용액의 반응 (해 보기)
     · 금속판 Mg, Zn, Cu, Ag × 수용액 MgSO4, ZnSO4, CuSO4, AgNO3
     · 전자를 잃기 쉬운 정도 Mg 4 > Zn 3 > Cu 2 > Ag 1 — 금속 > 이온 금속이면 반응
     · 반응하면 1.1초마다 사건: 판 표면 원자 1개 → 양이온으로 떠남, 그 전자 수만큼 용액 이온이 판에 원자로 붙음(최대 4사건)
     · 「측정 기록」→ 결과 표에 행이 쌓임(최근 5행) · 「다시 넣기」 입자 처음으로 · 「초기화」 기록까지 지움 */
window.DECK_LABS = {
  rm21metal(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), g=API.mk('g',{},svg);
    const ACT={Mg:4,Zn:3,Cu:2,Ag:1}, Q={Mg:2,Zn:2,Cu:2,Ag:1};
    const NM={Mg:'마그네슘',Zn:'아연',Cu:'구리',Ag:'은'}, IGA={Mg:'마그네슘이',Zn:'아연이',Cu:'구리가',Ag:'은이'}, TOP={Mg:'마그네슘은',Zn:'아연은',Cu:'구리는',Ag:'은은'};
    const SOL={Mg:'MgSO4',Zn:'ZnSO4',Cu:'CuSO4',Ag:'AgNO3'};
    const PLATE={Mg:'#BFE3CC',Zn:'#C9D3DD',Cu:'#E6C29C',Ag:'#E3E6EA'};
    const ION=s=>s+(Q[s]===2?'^2+':'+');
    const KMAX=4, CX=395, CY=150, CR=118, SX=290, RA=15, RI=13;
    let st={m:'Zn',s:'Cu'}, P=null, log=[];
    // 고정 시드 난수
    let seed=7; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    const clip=API.mk('clipPath',{id:'clip-rm21-lab'},API.mk('defs',{},svg)); API.mk('circle',{cx:CX,cy:CY,r:CR},clip);
    const reacts=()=>st.m!==st.s && ACT[st.m]>ACT[st.s];
    const inZoom=(x,y)=>Math.hypot(x-CX,y-CY)<CR-RI-4 && x>SX+RI+20;
    function freePos(){ for(let i=0;i<200;i++){ const x=SX+40+rnd()*200, y=CY-100+rnd()*200; if(inZoom(x,y)) return [x,y]; } return [420,150]; }
    function init(){
      seed=7;
      const rows=[]; for(let y=CY-90;y<=CY+90;y+=30) rows.push(y);
      P={rows, plate:rows.map(y=>({x:SX-RA,y,on:true})), back:rows.map(y=>({x:SX-3*RA,y})),
         ions:[], dep:[], fly:[], k:0, t:0, ne:0};
      for(let i=0;i<8;i++){ const [x,y]=freePos(); P.ions.push({el:st.s,x,y,vx:0,vy:0,kind:'sol'}); }
      for(let i=0;i<5;i++){ const [x,y]=freePos(); P.ions.push({el:'X',x,y,vx:0,vy:0,kind:'an'}); }
      if(window.__STILL && reacts()) for(let i=0;i<KMAX;i++) event(true);
    }
    function event(instant){
      if(P.k>=KMAX) return;
      const order=[3,2,4,1,5,0,6], a=P.plate[order[P.k]]; a.on=false;
      const ne=Q[st.m], need=ne/Q[st.s];
      P.ions.push({el:st.m,x:a.x+(instant?90:6),y:a.y,vx:2.5,vy:0,kind:'out'});
      const cands=P.ions.filter(o=>o.kind==='sol').sort((p,q)=>Math.hypot(p.x-a.x,p.y-a.y)-Math.hypot(q.x-a.x,q.y-a.y)).slice(0,need);
      cands.forEach((o,j)=>{ const slot=P.dep.length+P.fly.length; const tx=SX+RA, ty=P.rows[(order[(slot)%7])];
        o.kind='go'; if(instant){ o.kind='dead'; P.dep.push({el:st.s,x:tx,y:ty}); } else P.fly.push({o,tx,ty,t:0,ex:a.x,ey:a.y}); });
      P.ions=P.ions.filter(o=>o.kind!=='dead');
      P.k++; P.ne+=ne;
    }
    function solColor(){
      let n=P.ions.filter(o=>o.el==='Cu'&&o.kind!=='an').length + P.fly.filter(f=>f.o.el==='Cu').length;
      return Math.min(.5,n*.05);
    }
    function draw(){
      while(g.firstChild) g.firstChild.remove();
      const mk=(t,a)=>API.mk(t,a,g);
      // 비커
      const op=solColor();
      mk('rect',{x:22,y:130,width:166,height:158,rx:8,fill:'#DDEEF8'});
      if(op>0) mk('rect',{x:22,y:130,width:166,height:158,rx:8,fill:'#3E8ED0','fill-opacity':op});
      mk('path',{d:'M14 90 H20 V280 Q20 290 30 290 H180 Q190 290 190 280 V90 H196',fill:'none',stroke:'#7E8B98','stroke-width':3});
      mk('rect',{x:85,y:60,width:40,height:220,rx:3,fill:PLATE[st.m],stroke:'#7E8B98','stroke-width':2});
      const nd=P.dep.length;
      for(let i=0;i<nd*2;i++){ const y=150+i*14, x=i%2?128:82; if(y<276) mk('circle',{cx:x,cy:y,r:5.5,fill:API.ATOM[st.s][0],stroke:API.ATOM[st.s][1],'stroke-width':1.2}); }
      mk('line',{x1:125,y1:170,x2:CX-CR*.93,y2:CY-CR*.37,stroke:'#5B6B7F','stroke-width':1.5});
      mk('line',{x1:125,y1:200,x2:CX-CR*.93,y2:CY+CR*.37,stroke:'#5B6B7F','stroke-width':1.5});
      // 확대 원
      const z=mk('g',{'clip-path':'url(#clip-rm21-lab)'});
      API.mk('rect',{x:CX-CR,y:CY-CR,width:2*CR,height:2*CR,fill:'#FFFFFF'},z);
      if(op>0) API.mk('rect',{x:CX-CR,y:CY-CR,width:2*CR,height:2*CR,fill:'#3E8ED0','fill-opacity':op*.6},z);
      API.mk('rect',{x:CX-CR,y:CY-CR,width:SX-(CX-CR),height:2*CR,fill:PLATE[st.m]},z);
      P.back.forEach(a=>API.atom(z,a.x,a.y,RA,st.m,'-'));
      P.plate.forEach(a=>{ if(a.on) API.atom(z,a.x,a.y,RA,st.m,'-'); else API.atom(z,a.x,a.y,RA,st.m,'-',true); });
      P.dep.forEach(a=>API.atom(z,a.x,a.y,RA,a.el,'-'));
      const ionG=o=>{ if(o.kind==='an'){ API.mk('circle',{cx:o.x,cy:o.y,r:9,fill:'#C9D3DD',stroke:'#8C99A6','stroke-width':2},z); return; }
        API.atom(z,o.x,o.y,RI,o.el,'-'); API.mk('circle',{cx:o.x,cy:o.y,r:RI+2,fill:'none',stroke:'#D7263D','stroke-width':2.2},z); };
      P.ions.filter(o=>o.kind!=='go').forEach(ionG); P.fly.forEach(f=>ionG(f.o));
      P.fly.forEach(f=>{ if(f.t<.6){ const u=f.t/.6; API.mk('circle',{cx:f.ex+(f.o.x-f.ex)*u,cy:f.ey+(f.o.y-f.ey)*u,r:5,fill:'#1F6FD1'},z); } });
      mk('circle',{cx:CX,cy:CY,r:CR,fill:'none',stroke:'#5B6B7F','stroke-width':3});
      O('ne').textContent = reacts()? `잃은 전자 ${P.ne}개 = 얻은 전자 ${P.ne}개` : '0개';
    }
    function update(){
      root.querySelectorAll('[data-m]').forEach(b=>b.classList.toggle('on',b.dataset.m===st.m));
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===st.s));
      init();
      const m=st.m, s=st.s, r=reacts();
      O('rx').textContent = m===s? '반응하지 않는다 (같은 금속)' : r? '반응한다' : '반응하지 않는다';
      O('ox').textContent = r? NM[m] : '—';
      O('rd').textContent = r? NM[s]+' 이온' : '—';
      O('msg').textContent = m===s? '같은 금속과 그 이온은 반응하지 않는다.'
        : r? `${IGA[m]} ${NM[s]}보다 전자를 잃기 쉬워, ${TOP[m]} 산화되고 ${NM[s]} 이온은 환원된다.`
        : `${TOP[m]} ${NM[s]}보다 전자를 잃기 어려워 반응하지 않는다.`;
      const n=Q[m]/Q[s], c=n>1?n:'';
      const ox=`\\ce{${m} -> ${ION(m)} + 2e-}`, rd= n>1? `\\ce{2${ION(s)} + 2e- -> 2${s}}` : `\\ce{${ION(s)} + 2e- -> ${s}}`;
      const all=`\\ce{${m} + ${c}${ION(s)} -> ${ION(m)} + ${c}${s}}`;
      const eq=Ov('eq');
      eq.innerHTML = r? `<span style="color:#C2410C;font-weight:700">산화</span> ${API.tex(ox)}<br><span style="color:#0E7490;font-weight:700">환원</span> ${API.tex(rd)}<br><b>전체</b> ${API.tex(all)}`
        : `${API.tex(`\\ce{${m}}`)} + ${API.tex(`\\ce{${ION(s)}}`)}: 변화 없음`;
      API.place(eq,6,4);
      const leg=Ov('leg'), dot=(c,ring)=>`<span style="display:inline-block;width:13px;height:13px;border-radius:50%;background:${c};border:2px solid ${ring};vertical-align:-1px"></span>`;
      leg.innerHTML=`${dot(API.ATOM[m][0],API.ATOM[m][1])} ${API.tex(`\\ce{${m}}`)} &nbsp;${dot(API.ATOM[s][0],'#D7263D')} ${API.tex(`\\ce{${ION(s)}}`)} &nbsp;${dot('#C9D3DD','#8C99A6')} 음이온 · 빨간 테 = 양이온`;
      API.place(leg,214,276);
      draw();
    }
    root.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>{ st.m=b.dataset.m; update(); }));
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ st.s=b.dataset.s; update(); }));
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${API.tex('\\ce{'+r.m+'}')}</td><td>${API.tex('\\ce{'+SOL[r.s]+'}')}</td><td>${r.r?'○':'×'}</td><td>${r.r?API.tex('\\ce{'+r.m+'}'):'—'}</td><td>${r.r?API.tex('\\ce{'+ION(r.s)+'}'):'—'}</td>`; tb.appendChild(tr); }); }
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ log.push({m:st.m,s:st.s,r:reacts()}); if(log.length>5) log.shift(); renderLog(); });
    root.querySelector('[data-act="again"]').addEventListener('click',update);
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); st={m:'Zn',s:'Cu'}; update(); });
    API.onShow&&API.onShow(()=>update());
    update();
    if(!window.__STILL) API.loop(root,dt=>{
      dt=Math.min(dt,.05); P.t+=dt;
      if(reacts() && P.k<KMAX && P.t>1.1*(P.k+1)) event(false);
      P.ions.forEach(o=>{
        if(o.kind==='go') return; if(o.kind==='out'){ o.x+=o.vx*dt*30; o.vx*=.985; if(o.vx<.4) o.kind='free'; }
        else { o.vx=API.clamp(o.vx+(rnd()-.5)*.6,-1.2,1.2); o.vy=API.clamp(o.vy+(rnd()-.5)*.6,-1.2,1.2);
          const nx=o.x+o.vx*dt*30, ny=o.y+o.vy*dt*30; if(inZoom(nx,ny)){ o.x=nx; o.y=ny; } else { o.vx*=-1; o.vy*=-1; } }
      });
      P.fly=P.fly.filter(f=>{ f.t+=dt; const k=Math.min(1,dt*2.2); f.o.x+=(f.tx-f.o.x)*k; f.o.y+=(f.ty-f.o.y)*k;
        if(Math.hypot(f.tx-f.o.x,f.ty-f.o.y)<1.5){ P.dep.push({el:f.o.el,x:f.tx,y:f.ty}); P.ions=P.ions.filter(o=>o!==f.o); return false; } return true; });
      draw();
    });
  }
};
