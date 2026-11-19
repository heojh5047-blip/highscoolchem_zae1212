/* 고급화학 2-3-1 — 실험실
   ac231cell : 3D 단위세포(필수 탐구 고화-탐14, 지도서 Ⅱ-3 3D 모델링·충전율 합침)
     · 입방(모서리 1): 단순·체심·면심, NaCl·CsCl·ZnS / 육방 밀집(a = 1, c = √(8/3), 육각기둥 단위세포) — gen.py의 cells.py와 같은 좌표
     · 몫: 입방 = 경계 좌표 하나마다 ×1/2 (꼭짓점 1/8, 모서리 1/4, 면 1/2), 육각기둥 = 육각형 꼭짓점 1/3·변 1/2 × 윗·아랫면 1/2
     · 배위수: 가운데 원자(CENTER)에서 가장 가까운 이웃 수(금속 = 같은 원자, 이온 = 반대 전하), 3×3×3 칸까지 찾음
     · 원자 점유 비율 = N·(4/3)πr³ / V, r = 가장 가까운 거리/2 (육방: V = (3√3/2)a²c)
     · 이온 공 크기: 교과서 반지름(pm) Na⁺ 97, Cl⁻ 181, Cs⁺ 167, Zn²⁺ 74, S²⁻ 184 비율, 양이온–음이온이 맞닿을 때 100 %
   ac231ion : 이온 결정의 특성(필수 탐구 고화-탐15)
     · ① 힘 가하기: 위·아래 두 이온 층의 쿨롱 상호 작용 E(s) = (1/(2N+1)) Σ q_i q_j / √((j+s−i)² + 1), N = 40 (calc.py와 같음, 상대값)
     · ② 전기 전도성: 녹는점 KNO₃ 334 °C, NaCl 801 °C(이 장치 밖), 설탕 186 °C. 전류(모형 값) 용융 KNO₃ 150 mA × (1 + 0.002(t − 334)), 수용액 60 mA, 그 밖 0 — ×(1 + N(0, 2 %)) 고정 시드 103 */
(function(){
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=Math.imul(a^(a>>>15),1|a); t=(t+Math.imul(t^(t>>>7),61|t))^t; return ((t^(t>>>14))>>>0)/4294967296; }; }
function gauss(r){ let u=0,v=0; while(u===0)u=r(); v=r(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||18,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
const CH=Math.sqrt(8/3), d2r=Math.PI/180, near=(a,b)=>Math.abs(a-b)<1e-6;
const FCC=[[0,0,0],[.5,.5,0],[.5,0,.5],[0,.5,.5]];
const CUB={sc:[[0,0,0,'M']],bcc:[[0,0,0,'M'],[.5,.5,.5,'M']],fcc:FCC.map(p=>[...p,'M']),
  nacl:FCC.map(p=>[...p,'Cl']).concat([[.5,0,0,'Na'],[0,.5,0,'Na'],[0,0,.5,'Na'],[.5,.5,.5,'Na']]),
  cscl:[[0,0,0,'Cl'],[.5,.5,.5,'Cs']],
  zns:FCC.map(p=>[...p,'S']).concat([[.25,.25,.25,'Zn'],[.75,.75,.25,'Zn'],[.75,.25,.75,'Zn'],[.25,.75,.75,'Zn']])};
const NAME={sc:'단순 입방',bcc:'체심 입방',fcc:'면심 입방',hcp:'육방 밀집',nacl:'NaCl',cscl:'CsCl',zns:'ZnS'};
const TEXN={nacl:'\\ce{NaCl}',cscl:'\\ce{CsCl}',zns:'\\ce{ZnS}'};
const Q={M:0,Na:1,Cl:-1,Cs:1,Zn:2,S:-2}, IR={Na:97,Cl:181,Cs:167,Zn:74,S:184};
const KN={Na:'나트륨 이온',Cl:'염화 이온',Cs:'세슘 이온',Zn:'아연 이온',S:'황화 이온'};
const ITEX={Na:'\\ce{Na+}',Cl:'\\ce{Cl-}',Cs:'\\ce{Cs+}',Zn:'\\ce{Zn^2+}',S:'\\ce{S^2-}'};
const COLI={M:['#9AA9BA','#5C6F82'],Cl:['#4CAF50','#2E7D32'],Na:['#8E5BD0','#5E3A96'],Cs:['#7A4FC0','#4E2F8A'],Zn:['#8FA3B8','#5C6F82'],S:['#E8C547','#A88A1E']};
const POSC={'꼭짓점':['#4F86C6','#2F5F98'],'면 중심':['#E8A33D','#A8701A'],'체심':['#C0504D','#86302E'],'내부':['#C0504D','#86302E'],'모서리':['#7AA95C','#4F7A36']};
const CENTER={sc:[[0,0,1],'M'],bcc:[[.5,.5,.5],'M'],fcc:[[.5,.5,1],'M'],hcp:[[0,0,CH],'M'],nacl:[[.5,.5,.5],'Na'],cscl:[[.5,.5,.5],'Cs'],zns:[[.25,.25,.25],'Zn']};
const HEX=[0,1,2,3,4,5].map(k=>[Math.cos(k*Math.PI/3),Math.sin(k*Math.PI/3)]);
function sitesOf(k){ const out=[];
  if(k==='hcp'){ const a2=[-.5,Math.sqrt(3)/2];
    for(let i=-3;i<=3;i++) for(let j=-3;j<=3;j++) for(let l=-1;l<=2;l++) [[0,0,0],[1/3,2/3,.5]].forEach(b=>out.push([[(i+b[0])+(j+b[1])*a2[0],(j+b[1])*a2[1],(l+b[2])*CH],'M']));
    return out; }
  for(let i=-1;i<=2;i++) for(let j=-1;j<=2;j++) for(let l=-1;l<=2;l++) CUB[k].forEach(b=>out.push([[b[0]+i,b[1]+j,b[2]+l],b[3]]));
  return out; }
function inHex(x,y){ let ins=true,onE=false; const onV=HEX.some(v=>near(v[0],x)&&near(v[1],y));
  for(let k=0;k<6;k++){ const [x1,y1]=HEX[k],[x2,y2]=HEX[(k+1)%6], cr=(x2-x1)*(y-y1)-(y2-y1)*(x-x1); if(cr<-1e-6) ins=false; if(Math.abs(cr)<1e-6) onE=true; }
  return [ins,onV,onE&&!onV]; }
function cellAtoms(k){ const out=[];
  sitesOf(k).forEach(([p,t])=>{
    if(k==='hcp'){ const [ins,v,e]=inHex(p[0],p[1]); if(!ins||p[2]<-1e-6||p[2]>CH+1e-6) return;
      const zb=near(p[2],0)||near(p[2],CH); const den=(v?3:e?2:1)*(zb?2:1);
      out.push({p,t,den,pl:(v&&zb)?'꼭짓점':zb?'면 중심':'내부'}); return; }
    if(!p.every(c=>c>-1e-6&&c<1+1e-6)) return;
    const nb=p.filter(c=>near(c,0)||near(c,1)).length;
    let pl=['내부','면 중심','모서리','꼭짓점'][nb]; if(nb===0&&p.every(c=>near(c,.5))) pl='체심';
    out.push({p,t,den:2**nb,pl}); });
  return out; }
const dist=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1],a[2]-b[2]);
function neigh(k){ const [c,ct]=CENTER[k], ion=Q[ct]!==0;
  const cand=sitesOf(k).filter(([p,t])=>dist(p,c)>1e-6&&(ion?Q[t]*Q[ct]<0:true)).map(([p,t])=>({p,t,d:dist(p,c)}));
  const dm=Math.min(...cand.map(x=>x.d)); return {c,ct,dm,list:cand.filter(x=>x.d<dm+1e-6)}; }
function frame(k){
  if(k==='hcp'){ const V=[]; [0,CH].forEach(z=>HEX.forEach(([x,y])=>V.push([x,y,z])));
    const E=[]; for(let i=0;i<6;i++){ E.push([i,(i+1)%6]); E.push([6+i,6+(i+1)%6]); E.push([i,i+6]); }
    const F=[[[0,0,-1],[0,1,2,3,4,5]],[[0,0,1],[6,7,8,9,10,11]]];
    for(let i=0;i<6;i++){ const m=(60*i+30)*d2r; F.push([[Math.cos(m),Math.sin(m),0],[i,(i+1)%6,i+6,6+(i+1)%6]]); }
    return {V,E,F,ctr:[0,0,CH/2]}; }
  const V=[]; [0,1].forEach(x=>[0,1].forEach(y=>[0,1].forEach(z=>V.push([x,y,z]))));
  const E=[]; for(let i=0;i<8;i++) for(let j=i+1;j<8;j++) if(V[i].filter((c,q)=>c!==V[j][q]).length===1) E.push([i,j]);
  const F=[[[0,-1,0],1,0],[[0,1,0],1,1],[[-1,0,0],0,0],[[1,0,0],0,1],[[0,0,-1],2,0],[[0,0,1],2,1]].map(([n,ax,v])=>[n,V.map((p,i)=>p[ax]===v?i:-1).filter(i=>i>=0)]);
  return {V,E,F,ctr:[.5,.5,.5]}; }
function fr(n,d){ return d===1?String(n):`${n} × 1/${d}`; }

window.DECK_LABS = {
  ac231cell(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=root.querySelector('.lab-fig svg'), fig=root.querySelector('.lab-fig'), g=API.mk('g',{},svg);
    let st={k:'sc',yaw:28,pitch:18,cstep:0,coord:false,drag:null,idle:0}, log=[];
    let D=null;
    function prep(){ const k=st.k, A=cellAtoms(k), N=neigh(k), Fm=frame(k);
      // 자리별 묶음(음이온 먼저)
      const groups=[]; const key=a=>a.t+'|'+a.pl;
      const ord=['꼭짓점','모서리','면 중심','체심','내부'];
      const types=[...new Set(A.map(a=>a.t))].sort((a,b)=>Q[a]-Q[b]);
      types.forEach(t=>ord.forEach(pl=>{ const m=A.filter(a=>a.t===t&&a.pl===pl); if(m.length) groups.push({t,pl,n:m.length,den:m[0].den,keys:new Set(m.map(key))}); }));
      const tot={}; A.forEach(a=>tot[a.t]=(tot[a.t]||0)+1/a.den);
      // 공 반지름(맞닿을 때): 금속 = dm/2, 이온 = 교과서 반지름 비율로 양이온–음이온 거리에 맞춤
      const rt={};
      if(Q[N.ct]===0) rt.M=N.dm/2;
      else { const an=types.find(t=>Q[t]<0), ca=types.find(t=>Q[t]>0), s=N.dm/(IR[ca]+IR[an]); rt[ca]=IR[ca]*s; rt[an]=IR[an]*s; }
      let pf=null; if(Q[N.ct]===0){ const Vc=k==='hcp'?3*Math.sqrt(3)/2*CH:1; pf=tot.M*4/3*Math.PI*rt.M**3/Vc; }
      const ghosts=N.list.filter(x=>!A.some(a=>dist(a.p,x.p)<1e-6));
      D={A,N,Fm,groups,tot,rt,pf,types,ghosts,key};
    }
    function rot(p){ const c=D.Fm.ctr, a=st.yaw*d2r, b=st.pitch*d2r; const x=p[0]-c[0], y=p[1]-c[1], z=p[2]-c[2];
      const x1=x*Math.cos(a)-y*Math.sin(a), y1=x*Math.sin(a)+y*Math.cos(a); return [x1, y1*Math.cos(b)-z*Math.sin(b), y1*Math.sin(b)+z*Math.cos(b)]; }
    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      const sz=+I('sz').value/100, items=[];
      const pts=D.A.map(a=>a.p).concat(st.coord?D.ghosts.map(x=>x.p):[]).concat(D.Fm.V);
      const rmax=Math.max(...Object.values(D.rt))*sz, R=Math.max(...pts.map(p=>dist(p,D.Fm.ctr)))+rmax;
      const S=128/R, CX=280, CY=150, sc=p=>{ const v=rot(p); return [CX+v[0]*S, CY-v[2]*S, v[1]]; };
      // 모서리: 이웃 면이 모두 뒤를 보면 점선
      const back=D.Fm.F.map(([n])=>rot([n[0]+D.Fm.ctr[0],n[1]+D.Fm.ctr[1],n[2]+D.Fm.ctr[2]])[1]>1e-9);
      D.Fm.E.forEach(([i,j])=>{ const hid=D.Fm.F.every(([n,vs],fi)=>!(vs.includes(i)&&vs.includes(j))||back[fi]);
        const a=sc(D.Fm.V[i]), b=sc(D.Fm.V[j]);
        items.push({z:100+(a[2]+b[2])/2+(hid?.6:0),f:()=>API.mk('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:hid?'#5B6B7F':'#16233D','stroke-width':hid?1.5:2,'stroke-dasharray':hid?'5 4':null},g)}); });
      const cur=st.cstep>0&&st.cstep<=D.groups.length?D.groups[st.cstep-1]:null, done=st.cstep>D.groups.length;
      const isIon=D.types.some(t=>Q[t]!==0);
      D.A.forEach(a=>{ const [x,y,z]=sc(a.p), r=D.rt[a.t]*sz*S;
        let col=COLI[a.t]; if(!isIon&&st.cstep>0) col=POSC[a.pl]||col;
        const on=!cur||cur.keys.has(D.key(a)), isC=st.coord&&dist(a.p,D.N.c)<1e-6;
        items.push({z,f:()=>{ const gg=API.mk('g',{opacity:on?1:.22},g);
          API.mk('circle',{cx:x,cy:y,r,fill:col[0],stroke:col[1],'stroke-width':1.6},gg);
          API.mk('ellipse',{cx:x-.33*r,cy:y-.36*r,rx:.32*r,ry:.22*r,fill:'#fff',opacity:.55},gg);
          if(cur&&on) API.mk('circle',{cx:x,cy:y,r:r+4,fill:'none',stroke:'#E08A2C','stroke-width':3.5},gg);
          if(isC) API.mk('circle',{cx:x,cy:y,r:r+5,fill:'none',stroke:'#2E9E6A','stroke-width':3.5},gg); }}); });
      if(st.coord){ const c=sc(D.N.c);
        D.N.list.forEach(x=>{ const b=sc(x.p); items.push({z:(c[2]+b[2])/2,f:()=>API.mk('line',{x1:c[0],y1:c[1],x2:b[0],y2:b[1],stroke:'#2E9E6A','stroke-width':3.5,'stroke-linecap':'round'},g)}); });
        D.ghosts.forEach(x=>{ const [px,py,pz]=sc(x.p), r=D.rt[x.t]*sz*S, col=COLI[x.t];
          items.push({z:pz,f:()=>API.mk('circle',{cx:px,cy:py,r,fill:col[0],stroke:col[1],'stroke-width':1.6,'stroke-dasharray':'4 3',opacity:.45},g)}); }); }
      items.sort((a,b)=>b.z-a.z).forEach(it=>it.f());
    }
    function legend(){
      const isIon=D.types.some(t=>Q[t]!==0); let h='';
      if(isIon) h=D.types.map(t=>`<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:${COLI[t][0]};border:1.5px solid ${COLI[t][1]};vertical-align:-1px"></span> ${API.tex(ITEX[t])}`).join(' &nbsp; ');
      else if(st.cstep>0) h=[...new Set(D.A.map(a=>a.pl))].map(pl=>`<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:${POSC[pl][0]};vertical-align:-1px"></span> ${pl}`).join(' &nbsp; ')+' <span style="color:#5B6B7F">(색은 위치 구분 — 같은 원자)</span>';
      const L=V('leg'); L.innerHTML=h; L.style.transform='none'; API.place(L,8,6,!!h);
    }
    function totStr(html){ const ts=D.types;
      if(ts.length===1) return `${Math.round(D.tot[ts[0]]*1000)/1000}개`;
      const o=[...ts].sort((a,b)=>Q[b]-Q[a]);
      return html?o.map(t=>API.tex(ITEX[t])+' '+Math.round(D.tot[t])).join(' : '):'양이온 '+Math.round(D.tot[o[0]])+' : 음이온 '+Math.round(D.tot[o[1]]); }
    function readout(){
      O('sz').textContent=I('sz').value+' %'; O('pr').textContent=I('pr').value;
      root.querySelectorAll('[data-k]').forEach(b=>b.classList.toggle('on',b.dataset.k===st.k));
      root.querySelector('[data-act="coord"]').classList.toggle('on',st.coord);
      const G=D.groups, cn=D.N.list.length, pred=+I('pr').value;
      let big='—', msg='';
      if(st.cstep>0){
        const upto=G.slice(0,Math.min(st.cstep,G.length));
        const expr=D.types.map(t=>{ const m=upto.filter(x=>x.t===t); return m.length?(D.types.length>1?KN[t]+' ':'')+m.map(x=>fr(x.n,x.den)).join(' + '):''; }).filter(Boolean).join(' / ');
        if(st.cstep<=G.length){ const c=G[st.cstep-1]; big=`${c.pl} ${fr(c.n,c.den)} = ${Math.round(c.n/c.den*1000)/1000}`;
          msg=`${D.types.length>1?KN[c.t]+' — ':''}${c.pl}의 ${D.types.length>1?'이온':'원자'} ${c.n}개는 한 단위세포에 ${c.den===1?'온전히':'1/'+c.den+'씩'} 들어 있다. 지금까지: ${expr}. 「입자 수 세기」를 다시 눌러 다음 자리로.`; }
        else { big='입자 수 '+totStr(false); msg=`${expr} → 단위세포 속 ${totStr(false)}`+(D.types.length>1?` — 화학식의 비와 같다(전기적 중성).`:'.'); }
      }
      if(st.coord){ big=(st.cstep>0?big+' · ':'')+'배위수 '+cn; const ok=pred===cn;
        msg=(msg?msg+' ':'')+`가운데 원자(초록 테)에 가장 가까운 ${Q[D.N.ct]?'반대 전하 이온':'원자'} ${cn}개(흐린 점선 공은 이웃 단위세포). 내 예측 ${pred} → ${ok?'맞았다.':'다르다. 모형을 돌려 다시 세어 보자.'}`; }
      if(!st.cstep&&!st.coord) msg=`${NAME[st.k]} 단위세포. 끌어서 돌려 보고, 「입자 수 세기」와 「배위수 보기」로 확인하자.`+(D.pf!=null?` 공 크기를 100 %로 하면 원자가 맞닿는다.`:'');
      if(D.pf!=null&&+I('sz').value===100) msg+=` 원자 점유 비율 ${(D.pf*100).toFixed(1)} %.`;
      O('big').textContent=big; O('msg').textContent=msg;
      O('log').innerHTML=log.slice(-4).map((x,i)=>`<tr><td>${log.length-Math.min(4,log.length)+i+1}</td><td>${TEXN[x.k]?API.tex(TEXN[x.k]):NAME[x.k]}</td><td>${x.n}</td><td>${x.cn} (${x.pred}${x.pred===x.cn?' ○':' ×'})</td><td>${x.pf}</td></tr>`).join('');
      legend();
    }
    function update(){ readout(); draw(); }
    root.querySelectorAll('[data-k]').forEach(b=>b.addEventListener('click',()=>{ st.k=b.dataset.k; st.cstep=0; prep(); update(); }));
    root.querySelector('[data-act="count"]').addEventListener('click',()=>{ st.cstep=st.cstep>D.groups.length?1:st.cstep+1; update(); });
    root.querySelector('[data-act="coord"]').addEventListener('click',()=>{ st.coord=!st.coord; update(); });
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{
      const r={k:st.k,n:totStr(true),cn:D.N.list.length,pred:+I('pr').value,pf:D.pf!=null?(D.pf*100).toFixed(1)+' %':'—'};
      const i=log.findIndex(x=>x.k===r.k); if(i>=0) log.splice(i,1); log.push(r); update(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; st.k='sc'; st.cstep=0; st.coord=false; st.yaw=28; st.pitch=18; I('sz').value=40; I('pr').value=6; prep(); update(); });
    ['sz','pr'].forEach(k=>I(k).addEventListener('input',update));
    svg.style.cursor='grab'; svg.style.touchAction='none';
    svg.addEventListener('pointerdown',e=>{ st.drag={x:e.clientX,y:e.clientY}; svg.setPointerCapture(e.pointerId); svg.style.cursor='grabbing'; API.place(V('hint'),0,0,false); });
    svg.addEventListener('pointermove',e=>{ if(!st.drag) return; const k=fig.getBoundingClientRect().width/560||1;
      st.yaw+=(e.clientX-st.drag.x)/k*.6; st.pitch=API.clamp(st.pitch+(e.clientY-st.drag.y)/k*.6,-80,80); st.drag={x:e.clientX,y:e.clientY}; draw(); });
    const up=()=>{ st.drag=null; st.idle=0; svg.style.cursor='grab'; }; svg.addEventListener('pointerup',up); svg.addEventListener('pointercancel',up);
    API.place(V('hint'),490,272);
    prep(); update();
    if(!window.__STILL) API.loop(root,dt=>{ if(st.drag) return; st.idle+=dt; if(st.idle>1.5){ st.yaw+=dt*14; draw(); } });
  },

  ac231ion(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('.lab-fig svg');
    let st={m:'cut',cs:'salt',es:'kno3',shNow:0,gap:0}, log=[], rnd=rng(103);
    const gC=API.mk('g',{},svg), gE=API.mk('g',{},svg);
    // ── ① 힘 가하기
    const d=46, X0=98, Y0=80;
    const bgM=API.mk('rect',{x:60,y:50,width:440,height:200,rx:10,fill:'#E3EEFB',stroke:'none'},gC);
    const rowsB=API.mk('g',{},gC), rowT=API.mk('g',{},gC), elec=API.mk('g',{},gC), rep=API.mk('g',{},gC);
    const lbC=txt(API,gC,280,32,'',{size:19,w:700});
    function buildCut(){
      [rowsB,rowT,elec,rep].forEach(e=>{ while(e.firstChild) e.removeChild(e.firstChild); });
      const ion=st.cs==='salt'; bgM.setAttribute('visibility',ion?'hidden':'visible');
      for(let j=0;j<4;j++) for(let i=0;i<8;i++){ const x=X0+i*d, y=Y0+j*d;
        const sg=ion?((i+j)%2?'+':'-'):'+', par=j===0?rowT:rowsB;
        API.charge(par,x,y,ion?(sg==='+'?13:16):13,sg); }
      if(!ion){ const r=rng(5); for(let k=0;k<26;k++) API.mk('circle',{cx:70+r()*420,cy:58+r()*184,r:3.5,fill:'#1F6FD1'},elec); }
      txt(API,gC,40,Y0+6,'힘 →',{size:18,anchor:'middle'});
    }
    function Es(s,N=40){ let t=0; for(let i=-N;i<=N;i++){ const qi=(i%2===0)?1:-1; for(let j=-N;j<=N;j++){ const qj=-((j%2===0)?1:-1); t+=qi*qj/Math.hypot(j+s-i,1); } } return t/(2*N+1); }
    const ECACHE={}; [0,.25,.5,.75,1].forEach(s=>ECACHE[s]=Es(s));
    // ── ② 전기 전도성
    const bx=150,by=120,bw=200,bh=130;
    API.mk('path',{d:`M${bx} ${by} L${bx+10} ${by+bh} L${bx+bw-10} ${by+bh} L${bx+bw} ${by}`,fill:'#F7F8FA',stroke:'#7E8B98','stroke-width':3},gE);
    const melt=API.mk('path',{d:`M${bx+4} ${by+30} L${bx+12} ${by+bh-3} L${bx+bw-12} ${by+bh-3} L${bx+bw-4} ${by+30} Z`,fill:'#F5E6C8'},gE);
    const eL=bx+45, eR=bx+bw-45;
    [eL,eR].forEach(x=>API.mk('rect',{x:x-6,y:by-30,width:12,height:bh+10,rx:2,fill:'#3A3F47'},gE));
    txt(API,gE,eL,by-40,'(+)극',{size:18,fill:'#D7263D',w:700}); txt(API,gE,eR,by-40,'(−)극',{size:18,fill:'#1F6FD1',w:700});
    // 회로
    const W=(pts)=>API.mk('path',{d:'M'+pts.map(p=>p.join(' ')).join(' L'),fill:'none',stroke:'#16233D','stroke-width':2.5},gE);
    W([[eL,by-30],[eL,30],[255,30]]); W([[275,30],[420,30],[420,70]]); W([[420,112],[420,150],[eR+60,150]]); W([[eR,by-30],[eR,96],[eR+40,96],[eR+40,150],[eR+60,150]]);
    API.mk('line',{x1:255,y1:18,x2:255,y2:42,stroke:'#16233D','stroke-width':3},gE); API.mk('line',{x1:275,y1:24,x2:275,y2:36,stroke:'#16233D','stroke-width':6},gE);
    txt(API,gE,240,24,'+',{size:18,anchor:'end'}); txt(API,gE,265,62,'전원',{size:18});
    const bulb=API.mk('circle',{cx:420,cy:91,r:21,fill:'#FFFFFF',stroke:'#16233D','stroke-width':2.5},gE);
    API.mk('line',{x1:405,y1:76,x2:435,y2:106,stroke:'#16233D','stroke-width':1.5},gE); API.mk('line',{x1:405,y1:106,x2:435,y2:76,stroke:'#16233D','stroke-width':1.5},gE);
    txt(API,gE,456,96,'전구',{size:18,anchor:'start'});
    const flame=API.mk('path',{d:`M${bx+85} 286 Q${bx+90} 262 ${bx+100} 252 Q${bx+110} 262 ${bx+115} 286 Z`,fill:'#F2A65A',stroke:'#C2410C','stroke-width':2},gE);
    const tlab=txt(API,gE,bx+bw+20,by+bh-10,'',{size:19,anchor:'start'});
    const pg=API.mk('g',{},gE), parts=[];
    function buildParts(){
      while(pg.firstChild) pg.removeChild(pg.firstChild); parts.length=0; const r=rng(7);
      for(let j=0;j<3;j++) for(let i=0;i<6;i++){ const hx=bx+30+i*28, hy=by+48+j*26;
        const gg=API.mk('g',{},pg); let q=0;
        if(st.es==='sugar') API.mk('circle',{cx:0,cy:0,r:10,fill:'#E9E2D0',stroke:'#8C99A6','stroke-width':1.5},gg);
        else { q=(i+j)%2?1:-1; API.charge(gg,0,0,q>0?9:11,q>0?'+':'-'); }
        gg.setAttribute('transform',`translate(${hx} ${hy})`); parts.push({gg,hx,hy,x:hx,y:hy,q,vx:(r()-.5)*40,vy:(r()-.5)*40,ph:r()*6}); }
    }
    const MP={kno3:334,nacl:801,sugar:186}, NM={kno3:'질산 칼륨',nacl:'굵은 소금',sugar:'설탕'};
    function phase(){ const t=+I('t').value, aq=I('aq').checked; return aq?'수용액':(t>=MP[st.es]?'용융':'고체'); }
    function current(){ const ph=phase(), t=+I('t').value; if(st.es==='sugar') return 0;
      if(ph==='용융') return 150*(1+0.002*(t-334)); if(ph==='수용액') return 60; return 0; }
    function show(){
      root.querySelectorAll('[data-m]').forEach(b=>b.classList.toggle('on',b.dataset.m===st.m));
      root.querySelectorAll('[data-show]').forEach(e=>e.style.display=e.dataset.show===st.m?'':'none');
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===(st.m==='cut'?st.cs:st.es)));
      gC.setAttribute('visibility',st.m==='cut'?'visible':'hidden'); gE.setAttribute('visibility',st.m==='ec'?'visible':'hidden');
      const sh=+I('sh').value; O('sh').textContent=sh.toFixed(2);
      const t=+I('t').value, aq=I('aq').checked; O('t').textContent=aq?'— (수용액)':t+' °C';
      if(st.m==='cut'){
        O('rlab').textContent='윗층–아랫층 사이 힘';
        if(st.cs==='salt'){ const E=ECACHE[sh]; const att=E<-0.02, rp=E>0.02;
          O('big').textContent=att?'인력':rp?'반발 → 깨짐':'거의 0';
          O('msg').textContent=`상호 작용 에너지(상대값) ${E.toFixed(3)}. `+(att?'반대 전하가 마주 보아 서로 끌어당긴다.':rp?'같은 전하끼리 마주 보아 반발력이 생기고, 층이 평평한 면을 따라 떨어져 나간다.':'인력과 반발이 비슷해 결합이 크게 약해졌다.');
          lbC.textContent='굵은 소금(이온 결정)'; }
        else { O('big').textContent='인력 유지'; O('msg').textContent='금속 양이온 층이 밀려도 자유 전자(전자의 바다)가 계속 묶어 주므로 깨지지 않고 펴진다(연성·전성).'; lbC.textContent='구리(금속 결정)'; }
      } else {
        O('rlab').textContent='전류계 읽음'; const ph=phase(), I0=current();
        O('big').textContent=(I0>0?(I0*(1+0.0*0)).toFixed(0):'0')+' mA';
        bulb.setAttribute('fill',I0>1?'#FFE45C':'#FFFFFF'); flame.setAttribute('visibility',(!aq&&t>25)?'visible':'hidden');
        melt.setAttribute('fill',aq?'#DDEEF8':ph==='용융'?'#FBE9C6':'#F5E6C8');
        tlab.textContent=NM[st.es]+' · '+ph;
        let m='';
        if(st.es==='sugar') m=ph==='고체'?`설탕은 분자 결정이다. ${t} °C에서는 고체이다(녹는점 약 186 °C).`:`설탕이 ${ph==='용융'?'녹았지만':'녹아 있지만'} 움직이는 것은 전하가 없는 분자뿐이라 전류가 흐르지 않는다.`;
        else if(ph==='고체') m=`${NM[st.es]} 고체: 이온이 제자리에서 진동만 하므로 전류가 흐르지 않는다.`+(st.es==='nacl'&&!aq?' (녹는점 801 °C — 이 장치로는 녹일 수 없다)':` (녹는점 약 ${MP[st.es]} °C)`);
        else m=`${NM[st.es]} ${ph}: 양이온은 (−)극, 음이온은 (+)극 쪽으로 이동하며 전하를 옮겨 전구가 켜진다.`;
        O('msg').textContent=m;
      }
      O('log').innerHTML=log.slice(-4).map((x,i)=>`<tr><td>${log.length-Math.min(4,log.length)+i+1}</td><td>${x.a}</td><td>${x.b}</td><td>${x.c}</td><td>${x.d}</td></tr>`).join('');
    }
    function rec(){
      if(st.m==='cut'){ const sh=+I('sh').value, ion=st.cs==='salt', E=ECACHE[sh];
        log.push({a:'① 힘',b:ion?'굵은 소금':'구리',c:'밀림 '+sh.toFixed(2),d:ion?(E>0.02?'반발 → 깨짐':E<-0.02?'인력(그대로)':'약해짐'):'펴짐(안 깨짐)'}); }
      else { const ph=phase(), I0=current(), meas=I0>0?I0*(1+0.02*gauss(rnd)):0;
        log.push({a:'② 전도성',b:NM[st.es]+' · '+ph,c:I('aq').checked?'물에 녹임':I('t').value+' °C',d:`${meas.toFixed(0)} mA, 전구 ${meas>1?'켜짐':'꺼짐'}`}); }
      show(); }
    root.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>{ st.m=b.dataset.m; show(); }));
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ if(st.m==='cut'){ st.cs=b.dataset.s; buildCut(); } else { st.es=b.dataset.s; buildParts(); } show(); }));
    ['sh','t','aq'].forEach(k=>I(k).addEventListener('input',show)); I('aq').addEventListener('change',show);
    root.querySelector('[data-act="rec"]').addEventListener('click',rec);
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; rnd=rng(103); st={m:'cut',cs:'salt',es:'kno3',shNow:0,gap:0}; I('sh').value=0; I('t').value=25; I('aq').checked=false; buildCut(); buildParts(); place(1); show(); });
    function place(snap){
      const sh=+I('sh').value, ion=st.cs==='salt', rp=ion&&ECACHE[sh]>0.02;
      st.shNow=snap?sh:st.shNow+(sh-st.shNow)*0.12; st.gap=snap?(rp?22:0):st.gap+((rp?22:0)-st.gap)*0.12;
      rowT.setAttribute('transform',`translate(${(st.shNow*d).toFixed(1)} ${(-st.gap).toFixed(1)})`);
      while(rep.firstChild) rep.removeChild(rep.firstChild);
      if(rp&&st.gap>15) for(let i=0;i<7;i++){ const x=X0+(i+1)*d; API.arrow(rep,x,Y0-st.gap-18,x,Y0-st.gap-34,'plus',2.5); API.arrow(rep,x,Y0+d-20,x,Y0+d-6,'plus',2.5); }
    }
    buildCut(); buildParts(); place(1); show();
    let tt=0;
    API.loop(root,(dt)=>{ tt+=dt; if(st.m==='cut'){ place(false); return; }
      const ph=phase(), mob=ph!=='고체', drift=(st.es!=='sugar'&&mob)?28:0;
      parts.forEach(p=>{
        if(!mob){ p.x=p.hx+1.6*Math.sin(tt*14+p.ph); p.y=p.hy+1.6*Math.cos(tt*12+p.ph); }
        else { p.vx+=(Math.random()-.5)*120*dt; p.vy+=(Math.random()-.5)*120*dt; p.vx*=.96; p.vy*=.96;
          p.x+=(p.vx+p.q*drift)*dt; p.y+=p.vy*dt;
          if(p.x<bx+22) p.x=bx+bw-30; if(p.x>bx+bw-30) p.x=bx+22;
          if(p.y<by+44) {p.y=by+44; p.vy=Math.abs(p.vy);} if(p.y>by+bh-14){p.y=by+bh-14; p.vy=-Math.abs(p.vy);} }
        p.gg.setAttribute('transform',`translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})`); });
    });
  }
};
})();
