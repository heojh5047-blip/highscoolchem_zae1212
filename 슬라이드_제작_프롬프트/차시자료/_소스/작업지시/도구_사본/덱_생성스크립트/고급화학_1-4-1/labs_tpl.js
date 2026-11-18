/* 고급화학 1-4-1 탄소 화합물의 구조식과 탄화수소의 구조 — 실험실 (gen.py가 labs_tpl.js에 자료를 넣어 만든다)
   ac141model : 분자 모형 조립 실험실 (교과서 63쪽 탐구 활동 「포화와 불포화 탄화수소 구조 이성질체 분자 모형 만들기와 물리적 및 화학적 성질 차이 조사」)
     · 알케인 골격 조립: C4H10·C5H12·C6H14 — 조립판(6×3 격자점)에 탄소를 놓으면 이웃끼리 결합. 「확인」 → 탄소 수·이어짐·고리 검사 →
       탄소 골격 정규형(중심에서 뿌리 내린 괄호 문자열)으로 이성질체를 찾아 3차원 공-막대 모형·이름·축약 구조식·끓는점, 처음 찾은 것만 기록 표에 행.
     · 2-뷰텐 모형: 시스·트랜스-2-뷰텐(·뷰테인 비교) — 가운데 결합을 축으로 0–180° 돌리기, p 오비탈 겹침(100·|cos θ| %), 「성질 기록」.
     · 「그래프」: 기록한 이성질체의 끓는점 막대(분자식별). 「초기화」.
     · 자료(끓는점 °C, 1 atm): 덱 보충 문헌값·자체 지도서 30쪽(C6H14), 2-뷰텐 끓는점은 교과서 63쪽. */
window.DECK_LABS = {
  ac141model(root, API){
    /*@@DATA@@*/
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('.lab-fig svg'), fig=$('.lab-fig'), W=560, H=300, CX=280, CY=150;
    const g=API.mk('g',{},svg);
    const bsvg=root.querySelector('svg[data-board]'), bg=API.mk('g',{},bsvg);
    const R={H:15,C:21};
    const d2r=x=>x*Math.PI/180, norm=v=>{const l=Math.hypot(...v); return v.map(c=>c/l);}, sub=(a,b)=>a.map((c,i)=>c-b[i]), add=(a,b)=>a.map((c,i)=>c+b[i]), mul=(a,k)=>a.map(c=>c*k), dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
    const mn=v=>String(v).replace('-','−'), NN={4:2,5:3,6:5}, FT={4:'\\ce{C4H10}',5:'\\ce{C5H12}',6:'\\ce{C6H14}'};
    const BUI={cis:{name:'시스-2-뷰텐',bp:3.7,mp:'−139',pol:'극성'},trans:{name:'트랜스-2-뷰텐',bp:0.9,mp:'−106',pol:'무극성'},butane:{name:'뷰테인',bp:'−0.5'}};
    const GX=6, GY=3, GS=50, GX0=90, GY0=24;
    let st={mode:'alk', n:5, cells:new Set(), cur:null, bu:'cis', th:0, yaw:0, pitch:-18, drag:null, idle:0, view:'model'};
    let log=[], found={};
    const pool=[]; function lab(i){ while(pool.length<=i){ const d=document.createElement('div'); d.className='ov mid'; fig.appendChild(d); pool.push(d);} return pool[i]; }
    function hideLabs(from){ for(let i=from;i<pool.length;i++) API.place(pool[i],0,0,false); }
    const clear=el=>{ while(el.firstChild) el.removeChild(el.firstChild); };
    // ── 정규형 (gen.py chem.py와 같은 알고리즘)
    function canon(nodes,adj){
      const cr=(v,p)=>'('+adj[v].filter(w=>w!==p).map(w=>cr(w,v)).sort().join('')+')';
      const deg={}; nodes.forEach(v=>deg[v]=adj[v].length); let leaves=nodes.filter(v=>deg[v]<=1), rem=nodes.length; const out=new Set();
      while(rem>2){ const nl=[]; leaves.forEach(v=>{ out.add(v); rem--; adj[v].forEach(w=>{ if(!out.has(w)){ deg[w]--; if(deg[w]===1) nl.push(w);} }); }); leaves=nl; }
      return nodes.filter(v=>!out.has(v)).map(c=>cr(c,null)).sort()[0];
    }
    function analyze(){
      const nodes=[...st.cells], adj={}; nodes.forEach(k=>adj[k]=[]); let ne=0;
      nodes.forEach(k=>{ const [x,y]=k.split(',').map(Number); [[1,0],[0,1]].forEach(([dx,dy])=>{ const q=`${x+dx},${y+dy}`; if(st.cells.has(q)){ adj[k].push(q); adj[q].push(k); ne++; } }); });
      return {nodes,adj,ne};
    }
    function connected(nodes,adj){ if(!nodes.length) return false; const seen=new Set([nodes[0]]), s=[nodes[0]]; while(s.length){ const v=s.pop(); adj[v].forEach(w=>{ if(!seen.has(w)){ seen.add(w); s.push(w);} }); } return seen.size===nodes.length; }
    // ── 조립판
    function drawBoard(){
      clear(bg); const {nodes,adj}=analyze();
      nodes.forEach(k=>{ const [x,y]=k.split(',').map(Number); adj[k].forEach(q=>{ if(q>k){ const [x2,y2]=q.split(',').map(Number);
        API.mk('line',{x1:GX0+x*GS,y1:GY0+y*GS,x2:GX0+x2*GS,y2:GY0+y2*GS,stroke:'#9AA5B1','stroke-width':8,'stroke-linecap':'round'},bg); } }); });
      for(let y=0;y<GY;y++) for(let x=0;x<GX;x++){ const k=`${x},${y}`, px=GX0+x*GS, py=GY0+y*GS;
        if(st.cells.has(k)) API.atom(bg,px,py,19,'C','',false);
        else API.mk('circle',{cx:px,cy:py,r:9,fill:'#fff',stroke:'#8C99A6','stroke-width':2,'stroke-dasharray':'3 3'},bg);
        const hit=API.mk('circle',{cx:px,cy:py,r:26,fill:'transparent','data-c':k,style:'cursor:pointer'},bg);
        hit.addEventListener('click',e=>{ e.stopPropagation(); if(st.cells.has(k)) st.cells.delete(k); else st.cells.add(k); st.view='model'; drawBoard(); status(); }); }
    }
    function status(){
      const k=st.cells.size, m=Object.keys(found).filter(x=>DB[x].n===st.n).length;
      O('stat').textContent=`탄소 ${k} / ${st.n}개 · 찾은 이성질체 ${m} / ${NN[st.n]}`;
    }
    // ── 3차원 모형
    function rot(v){ const a=d2r(st.yaw), b=d2r(st.pitch); let [x,y,z]=v;
      [x,z]=[x*Math.cos(a)+z*Math.sin(a),-x*Math.sin(a)+z*Math.cos(a)]; [y,z]=[y*Math.cos(b)-z*Math.sin(b),y*Math.sin(b)+z*Math.cos(b)]; return [x,y,z]; }
    function rotAxis(p,o,u,t){ const v=sub(p,o), c=Math.cos(t), s=Math.sin(t), d=dot(u,v), cr=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
      return add(o,add(add(mul(v,c),mul(cr,s)),mul(u,d*(1-c)))); }
    function lobePath(o,d,L,Wf){ const v=rot(norm(d)), k=Math.hypot(v[0],v[1]), ux=k>1e-6?v[0]/k:1, uy=k>1e-6?-v[1]/k:0, px=-uy, py=ux, Ls=L*Math.max(k,.3), pts=[];
      for(let i=0;i<=60;i++){ const th=d2r(-90+3*i), rho=Ls*Math.cos(th)**2, a=rho*Math.cos(th), b=Wf*L*Math.cos(th)**2*Math.sin(th); pts.push((o[0]+ux*a+px*b).toFixed(1)+' '+(o[1]+uy*a+py*b).toFixed(1)); }
      return {d:'M'+pts.join(' L')+' Z', z:v[2], tip:[o[0]+ux*Ls*.6,o[1]+uy*Ls*.6]}; }
    function curModel(){
      if(st.mode==='alk') return st.cur? {atoms:DB[st.cur].atoms.map(a=>[a[0],a[1].slice()]),bonds:DB[st.cur].bonds}: null;
      const M=BU[st.bu], A=M.atoms.map(a=>[a[0],a[1].slice()]); const o=A[M.ax[0]][1], u=norm(sub(A[M.ax[1]][1],o)), t=d2r(st.th);
      M.side.forEach(i=>{ A[i][1]=rotAxis(A[i][1],o,u,t); }); return {atoms:A,bonds:M.bonds,u,o};
    }
    function drawModel(){
      const M=curModel(); let li=0;
      if(!M){ const m=lab(li++); m.textContent='골격을 만들고 「확인」을 누르자'; m.style.cssText='font-size:20px;color:#5B6B7F;white-space:nowrap'; API.place(m,CX,CY); hideLabs(li); return; }
      const S=st.mode==='alk'?62:74, items=[], pos=[];
      const ctr=M.atoms.reduce((s,a)=>add(s,a[1]),[0,0,0]).map(c=>c/M.atoms.length);
      M.atoms.forEach(a=>{ const v=rot(sub(a[1],ctr)); pos.push({x:CX+v[0]*S,y:CY-v[1]*S,z:v[2],r:R[a[0]],el:a[0]}); });
      M.bonds.forEach(([i,j,o])=>{ const a=pos[i], b=pos[j]; items.push({z:(a.z+b.z)/2-.001,f:()=>{ const dx=b.x-a.x, dy=b.y-a.y, n=Math.hypot(dx,dy)||1, px=-dy/n, py=dx/n;
        ({1:[0],2:[-4.5,4.5]})[o].forEach(t=>API.mk('line',{x1:a.x+px*t,y1:a.y+py*t,x2:b.x+px*t,y2:b.y+py*t,stroke:'#9AA5B1','stroke-width':o===1?7:5,'stroke-linecap':'round'},g)); }}); });
      if(st.mode==='bu' && st.bu!=='butane' && I('p').checked){
        const nz=[0,0,1], n2=rotAxis(nz,[0,0,0],M.u,d2r(st.th));
        [[1,nz],[2,n2]].forEach(([ai,d])=>[1,-1].forEach(sg=>{ const p=pos[ai], lb=lobePath([p.x,p.y],mul(d,sg),70,.5), col=sg>0?'#7B4FC8':'#8C99A6';
          items.push({z:p.z+lb.z*.9,f:()=>API.mk('path',{d:lb.d,fill:col,'fill-opacity':.28,stroke:col,'stroke-width':1.6},g)}); }));
      }
      pos.forEach(p=>items.push({z:p.z+.002,f:()=>API.atom(g,p.x,p.y,p.r,p.el,'-',false)}));
      items.sort((p,q)=>p.z-q.z).forEach(it=>it.f());
      pos.forEach((p,k)=>{ if(p.el!=='C') return; const l=lab(li++); l.style.cssText='font-size:19px;font-weight:700;color:#fff'; l.innerHTML=API.tex('\\mathrm{C}');
        const hid=pos.some((q,m)=>m!==k&&q.z>p.z+.05&&Math.hypot(q.x-p.x,q.y-p.y)<q.r*.9); API.place(l,p.x,p.y,!hid); });
      hideLabs(li);
    }
    function drawGraph(){
      let li=0; const x0=70, yb=236, tmin=-20, tmax=80, s=(yb-40)/(tmax-tmin), Y=t=>yb-(t-tmin)*s;
      API.mk('line',{x1:x0,y1:Y(0),x2:545,y2:Y(0),stroke:'#5B6B7F','stroke-width':1.6},g); API.mk('line',{x1:x0,y1:yb,x2:x0,y2:30,stroke:'#5B6B7F','stroke-width':1.6},g);
      [-20,0,20,40,60,80].forEach(v=>{ const y=Y(v); API.mk('line',{x1:x0-6,y1:y,x2:x0,y2:y,stroke:'#5B6B7F','stroke-width':1.4},g); if(v!==0) API.mk('line',{x1:x0,y1:y,x2:545,y2:y,stroke:'#E2E7EC','stroke-width':1},g);
        const l=lab(li++); l.textContent=mn(v); l.style.cssText='font-size:18px'; API.place(l,x0-22,y); });
      const t=lab(li++); t.textContent='끓는점 (°C)'; t.style.cssText='font-size:18px;white-space:nowrap'; API.place(t,x0+48,14);
      if(!log.length){ const m=lab(li++); m.textContent='기록한 이성질체가 없다'; m.style.cssText='font-size:19px;color:#5B6B7F;white-space:nowrap'; API.place(m,300,140); hideLabs(li); return; }
      const groups=[]; log.slice().sort((a,b)=>a.n-b.n||b.bp-a.bp).forEach(r=>{ let gr=groups.find(x=>x.key===r.gk); if(!gr){ gr={key:r.gk,tex:r.ft,items:[]}; groups.push(gr);} gr.items.push(r); });
      let x=x0+16; const nb=log.length, bw=Math.max(18,Math.min(34,(470-16*groups.length)/nb-6));
      groups.forEach(gr=>{ const gx=x;
        gr.items.forEach((r,ri)=>{ const y1=Y(Math.max(r.bp,0)), y2=Y(Math.min(r.bp,0));
          API.mk('rect',{x,y:y1,width:bw,height:Math.max(2,y2-y1),fill:'#16233D'},g);
          const v=lab(li++); v.textContent=mn(r.bp); v.style.cssText='font-size:17px'; API.place(v,x+bw/2,r.bp>=0?y1-12:y2+12);
          const tl=lab(li++); tl.textContent=r.tag; tl.style.cssText='font-size:17px;color:#5B6B7F;white-space:nowrap'; API.place(tl,x+bw/2,yb+14+(gr.key==='b'&&ri===1?18:0)); x+=bw+6; });
        const gl=lab(li++); gl.innerHTML=API.tex(gr.tex); gl.style.cssText='font-size:18px'; API.place(gl,(gx+x-6)/2,yb+(gr.key==='b'?52:38)); x+=16; });
      const lg=lab(li++); lg.textContent='막대 아래: 가지 수 (2-뷰텐은 시스·트랜스)'; lg.style.cssText='font-size:17px;color:#5B6B7F;white-space:nowrap'; API.place(lg,380,14);
      hideLabs(li);
    }
    function draw(){ clear(g); if(st.view==='graph') return drawGraph(); drawModel(); }
    function readout(){
      if(st.mode==='alk'){ const D=st.cur&&DB[st.cur];
        O('k1').textContent='이름'; O('v1').textContent=D?D.name:'—';
        O('k2').textContent='축약 구조식'; O('v2').innerHTML=D?API.tex(D.tex):'—';
        O('k3').textContent='끓는점'; O('v3').textContent=D?`${mn(D.bp)} °C`:'—';
        Ov('f').innerHTML=API.tex(FT[st.n]);
      } else { const B=BUI[st.bu], isB=st.bu==='butane', c=Math.abs(Math.cos(d2r(st.th)));
        O('k1').textContent='가운데 결합'; O('v1').textContent=isB?'단일 결합 (σ)':'2중 결합 (σ + π)';
        O('k2').textContent='π 결합 겹침'; O('v2').textContent=isB?'π 결합 없음 · σ 겹침 그대로':(st.th===90?'0 % — 끊어짐':`${Math.round(100*c)} %`);
        O('k3').textContent='끓는점'; O('v3').textContent=`${B.bp} °C`+(B.mp!==undefined?` · 녹는점 ${B.mp} °C`:'');
        Ov('f').innerHTML=API.tex(isB?'\\ce{C4H10}':'\\ce{C4H8}');
        const other=st.bu==='cis'?'트랜스':'시스';
        O('msg').textContent= isB? '단일 결합(σ)은 돌려도 겹침이 그대로 — 실온에서 자유롭게 돌아 모양만 바뀌는 같은 분자이다.'
          : st.th===0? (st.bu==='cis'?'시스: 두 메틸기가 2중 결합의 같은 쪽 — 끓는점 3.7 °C, 극성 분자.':'트랜스: 두 메틸기가 2중 결합의 반대쪽 — 끓는점 0.9 °C, 무극성 분자.')
          : st.th<90? `돌릴수록 두 p 오비탈이 나란하지 않아 π 결합의 겹침이 줄어든다(${Math.round(100*c)} %).`
          : st.th===90? 'p 오비탈이 서로 수직 → π 결합이 끊어진다. 약 264 kJ/mol(612 − 348)이 필요해 실온에서는 일어나지 않는다.'
          : `π 결합을 끊고 다시 만들어야만 ${other} 모양이 된다 — 그래서 시스와 트랜스는 서로 다른 화합물이다.`;
      }
      API.place(Ov('f'),16,10,st.view!=='graph');
    }
    function update(){
      root.querySelectorAll('[data-n]').forEach(b=>b.classList.toggle('on',+b.dataset.n===st.n));
      root.querySelectorAll('[data-b]').forEach(b=>b.classList.toggle('on',b.dataset.b===st.bu));
      O('th').textContent=`${st.th}°`; readout(); status(); draw();
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-4).forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${API.tex(r.ft)}</td><td>${r.name}</td><td>${r.note}</td><td>${mn(r.bp)} °C</td>`; tb.appendChild(tr); }); }
    function check(){
      st.view='model'; root.querySelector('[data-act="graph"]').classList.remove('on');
      const {nodes,adj,ne}=analyze(), k=nodes.length;
      if(k!==st.n){ O('msg').textContent=`탄소를 ${st.n}개 놓자 (지금 ${k}개).`; return; }
      if(!connected(nodes,adj)){ O('msg').textContent='모든 탄소가 결합으로 이어져야 한다 — 떨어진 탄소가 있다.'; return; }
      if(ne!==k-1){ O('msg').textContent='고리가 생겼다 — 고리 모양은 CnH2n이라 알케인(CnH2n+2)이 아니다. 네모로 붙은 곳을 떼어 보자.'; return; }
      const key=canon(nodes,adj), D=DB[key];
      if(!D){ O('msg').textContent='자료에 없는 골격이다.'; return; }
      st.cur=key; st.yaw=0; st.pitch=-18; st.idle=0;
      if(found[key]) O('msg').textContent=`이미 찾은 ${D.name}이다 — 사슬을 꺾거나 뒤집어 그린 같은 분자(가장 긴 사슬과 가지 자리가 같다).`;
      else { found[key]=1; log.push({n:D.n,gk:'a'+D.n,ft:FT[D.n],name:D.name,note:`가지 ${D.br}`,tag:String(D.br),bp:D.bp}); renderLog();
        const m=Object.keys(found).filter(x=>DB[x].n===st.n).length;
        O('msg').textContent= m===NN[st.n]? `새 이성질체: ${D.name}. 탄소 ${st.n}개 알케인의 구조 이성질체 ${NN[st.n]}개를 모두 찾았다!` : `새 이성질체: ${D.name} (H ${2*st.n+2}개는 자동으로 채움). 다른 골격도 만들어 보자.`; }
      update();
    }
    root.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>{ st.mode=b.dataset.m; st.view='model'; st.yaw=st.mode==='alk'?0:15; st.pitch=st.mode==='alk'?-18:62; st.idle=0;
      root.querySelectorAll('[data-m]').forEach(x=>x.classList.toggle('on',x===b));
      root.querySelectorAll('[data-set]').forEach(x=>x.style.display=x.dataset.set===st.mode?'':'none');
      root.querySelector('[data-act="graph"]').classList.remove('on');
      if(st.mode==='alk') O('msg').textContent='조립판의 점을 눌러 탄소를 놓자. 이웃한 탄소끼리 결합한다.'; update(); }));
    root.querySelectorAll('[data-n]').forEach(b=>b.addEventListener('click',()=>{ st.n=+b.dataset.n; st.cells=new Set(); st.cur=null; st.view='model'; drawBoard(); O('msg').textContent=`탄소 ${st.n}개로 서로 다른 골격을 만들어 보자.`; update(); }));
    root.querySelectorAll('[data-b]').forEach(b=>b.addEventListener('click',()=>{ st.bu=b.dataset.b; st.th=0; I('th').value=0; st.view='model'; update(); }));
    I('th').addEventListener('input',()=>{ st.th=+I('th').value; st.view='model'; update(); });
    I('p').addEventListener('change',draw);
    root.querySelector('[data-act="check"]').addEventListener('click',check);
    root.querySelector('[data-act="clear"]').addEventListener('click',()=>{ st.cells=new Set(); drawBoard(); status(); O('msg').textContent='조립판을 비웠다.'; });
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ if(st.bu==='butane'){ O('msg').textContent='뷰테인은 비교용 — 시스·트랜스-2-뷰텐을 기록하자.'; return; }
      const key='bu-'+st.bu; if(found[key]){ O('msg').textContent='이미 기록했다.'; return; } found[key]=1; const B=BUI[st.bu];
      log.push({n:4.5,gk:'b',ft:'\\ce{C4H8}',name:B.name,note:B.pol.split(' ')[0],tag:st.bu==='cis'?'시스':'트랜스',bp:B.bp}); renderLog(); O('msg').textContent=`${B.name}의 성질을 기록했다.`; });
    root.querySelector('[data-act="graph"]').addEventListener('click',()=>{ st.view=st.view==='graph'?'model':'graph';
      root.querySelector('[data-act="graph"]').classList.toggle('on',st.view==='graph'); API.place(Ov('hint'),W-80,H-18,st.view!=='graph'); readout(); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; found={}; renderLog(); st={...st,mode:'alk',n:4,cells:new Set(),cur:null,bu:'cis',th:0,yaw:0,pitch:-18,view:'model',idle:0}; I('th').value=0; I('p').checked=true;
      root.querySelectorAll('[data-m]').forEach(x=>x.classList.toggle('on',x.dataset.m==='alk')); root.querySelectorAll('[data-set]').forEach(x=>x.style.display=x.dataset.set==='alk'?'':'none');
      root.querySelector('[data-act="graph"]').classList.remove('on'); O('msg').textContent='조립판의 점을 눌러 탄소를 놓자. 이웃한 탄소끼리 결합한다.'; drawBoard(); update(); });
    svg.style.touchAction='none'; svg.style.cursor='grab';
    svg.addEventListener('pointerdown',e=>{ if(st.view==='graph') return; st.drag={x:e.clientX,y:e.clientY}; svg.setPointerCapture(e.pointerId); svg.style.cursor='grabbing'; API.place(Ov('hint'),0,0,false); });
    svg.addEventListener('pointermove',e=>{ if(!st.drag) return; const k=fig.getBoundingClientRect().width/W||1;
      st.yaw+=(e.clientX-st.drag.x)/k*.6; st.pitch=API.clamp(st.pitch-(e.clientY-st.drag.y)/k*.6,-85,85); st.drag={x:e.clientX,y:e.clientY}; draw(); });
    const up=()=>{ st.drag=null; st.idle=0; svg.style.cursor='grab'; };
    svg.addEventListener('pointerup',up); svg.addEventListener('pointercancel',up);
    API.place(Ov('hint'),W-80,H-18);
    // 처음: C5H12, 펜테인 골격을 놓아 둔다(확인 전)
    st.n=5; ['0,1','1,1','2,1','3,1','4,1'].forEach(k=>st.cells.add(k));
    O('msg').textContent='조립판의 점을 눌러 탄소를 놓자. 이웃한 탄소끼리 결합한다. 다 놓으면 「확인」.';
    drawBoard(); API.ready(()=>update()); update();
    if(!window.__STILL) API.loop(root,dt=>{ if(st.drag||st.view==='graph'||(st.mode==='alk'&&!st.cur)) return; st.idle+=dt; if(st.idle>1.5){ st.yaw+=dt*16; draw(); } });
  }
};
