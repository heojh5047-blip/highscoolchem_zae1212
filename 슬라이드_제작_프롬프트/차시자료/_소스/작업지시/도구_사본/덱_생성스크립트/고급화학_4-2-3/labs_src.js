/* 고급화학 4-2-3 — 실험실 (gen.py가 a/b 덱의 labs.js로 나눠 쓴다)
   공통: pH는 전하 균형 [H3O+] + [Na+] = [OH-] + [Cl-] + C·Ka/(Ka + [H3O+])를 이분법으로 정확히 푼다(부피 변화 포함).
         Ka(CH3COOH) = 1.8×10⁻⁵, Kw = 1.0×10⁻¹⁴, 측정값 = 참값 + 고정 시드 잡음.
   a  ac423titr : ◆ 지도서 디지털 탐구 Ⅳ-3 「pH 센서로 적정 곡선을 그려 식초 속 아세트산의 pKa와 농도 구하기」
        · 시료 25.0 mL: 0.100 M 염산 / 0.100 M 아세트산 / 10배 희석한 식초(참값 0.0820 M — 원액 0.820 M, 약 4.9 %). 표준 용액 0.100 M NaOH.
        · +5.0·+1.0·+0.2 mL 넣을 때마다 (V, pH) 측정(잡음 ±0.02) → 표(ΔpH/ΔV)·그래프에 쌓임. 시료를 바꾸면 앞 곡선은 회색 점선으로 남음.
        · ΔpH/ΔV가 가장 큰 구간의 가운데 = 당량점 Ve → 산의 농도 = 0.100 × Ve / 25.0. 반당량점 Ve/2의 pH(기록점 선형 보간) = pKa.
        · 지시약(메틸 오렌지 3.1–4.4, BTB 6.0–7.6, 페놀프탈레인 8.2–10.0): 비커 색, 그래프 변색 띠, 종말점(변색이 끝나는 pH에 닿는 부피)과 당량점 비교.
   b  ac423buf : 교과서 228쪽 탐구 활동 「완충 용액의 조성과 완충 용량 사이의 상관관계 실험 설계 및 실험」
        · 50.0 mL 완충 용액: [CH3COOH]·[CH3COONa]를 0.010–0.20 M에서 고름(조작 변인), 또는 증류수(비교).
        · 1.0 M HCl·NaOH를 0.1·1.0 mL(= 0.1·1.0 mmol)씩 넣음 → pH 측정(잡음 ±0.01). 산과 염기는 다른 비커(새 비커 자동).
        · 처음 pH ± 1에 이를 때까지 넣은 양(기록점 사이 선형 보간) = 완충 용량 → 조성별 표에 쌓임, 그래프에 조성별 곡선. */
(function(){
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=Math.imul(a^(a>>>15),1|a); t=(t+Math.imul(t^(t>>>7),61|t))^t; return ((t^(t>>>14))>>>0)/4294967296; }; }
function gauss(r){ let u=0,v=0; while(u===0)u=r(); v=r(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
const KW=1e-14, KA=1.8e-5;
function phMix(na,ct,cl,vol){ const Na=na/vol, Ct=ct/vol, Cl=cl/vol; let lo=-15.5, hi=1.5;
  for(let i=0;i<90;i++){ const m=(lo+hi)/2, h=Math.pow(10,m), f=h+Na-KW/h-Cl-Ct*KA/(KA+h); if(f>0) hi=m; else lo=m; } return -(lo+hi)/2; }
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||18,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
const f2=v=>v.toFixed(2);
function mix(c1,c2,t){ t=Math.max(0,Math.min(1,t)); const a=[1,3,5].map(i=>parseInt(c1.substr(i,2),16)), b=[1,3,5].map(i=>parseInt(c2.substr(i,2),16)); return 'rgb('+a.map((v,i)=>Math.round(v+(b[i]-v)*t)).join(',')+')'; }
/*@@A*/
  ac423titr(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=$('.lab-fig svg'), C=API.COL, mk=(t,a,p)=>API.mk(t,a,p);
    const SAMP=[{n:'0.100 M 염산',C:0.100,weak:false},{n:'0.100 M 아세트산',C:0.100,weak:true},{n:'희석한 식초',C:0.0820,weak:true,vin:true}];
    const IND=[null,{n:'메틸 오렌지',lo:3.1,hi:4.4,c1:'#D93A2B',c2:'#F2C230'},{n:'BTB',lo:6.0,hi:7.6,c1:'#E3C83A',c2:'#2F6DB5'},{n:'페놀프탈레인',lo:8.2,hi:10.0,c1:'#F4F7FA',c2:'#E0409A'}];
    const VA=25.0, CB=0.100, VMAX=40;
    const trueP=(a,V)=>{ const S=SAMP[a], vol=(VA+V)/1000; return S.weak? phMix(CB*V/1000,S.C*VA/1000,0,vol) : phMix(CB*V/1000,0,S.C*VA/1000,vol); };
    // 기하: 장치(0–190), 그래프
    const AX=244, AY=262, AW=392, AH=232, X=v=>AX+v/VMAX*AW, Y=p=>AY-Math.max(0,Math.min(14,p))/14*AH;
    const base=mk('g',{},svg);
    const BX=96, YT=14, Y0=24, PPM=4.2, STOP=Y0+40*PPM+12, TIP=STOP+14;
    mk('rect',{x:14,y:286,width:160,height:7,rx:2,fill:C.muted},base);
    mk('rect',{x:22,y:6,width:6,height:282,fill:'#AEB8C2',stroke:C.muted,'stroke-width':1},base);
    mk('line',{x1:26,y1:120,x2:BX-10,y2:120,stroke:C.muted,'stroke-width':4,'stroke-linecap':'round'},base);
    const bLiq=mk('rect',{x:BX-6.5,width:13,fill:'#E8F0F9'},base);
    mk('path',{d:`M${BX-8},${YT} L${BX-8},${STOP-6} M${BX+8},${YT} L${BX+8},${STOP-6}`,fill:'none',stroke:'#7E8B98','stroke-width':2.2},base);
    for(let v=0;v<=40;v+=10){ const y=Y0+v*PPM; mk('line',{x1:BX-8,y1:y,x2:BX-1,y2:y,stroke:C.muted,'stroke-width':1.4},base); }
    mk('path',{d:`M${BX-8},${STOP-6} L${BX-3},${STOP} L${BX-2},${TIP} L${BX+2},${TIP} L${BX+3},${STOP} L${BX+8},${STOP-6}`,fill:'none',stroke:'#7E8B98','stroke-width':2},base);
    mk('rect',{x:BX+4,y:STOP-4,width:12,height:6,rx:2,fill:C.minus},base);
    API.texText(base,BX+14,30,'\\ce{NaOH}',{size:18,anchor:'start',fill:C.minus});
    const KX=46, KYt=212, KYb=282, KWd=104;
    const kLiq=mk('rect',{x:KX+2,width:KWd-4,fill:'#DDEEF8'},base);
    mk('path',{d:`M${KX},${KYt} L${KX},${KYb} L${KX+KWd},${KYb} L${KX+KWd},${KYt}`,fill:'none',stroke:'#7E8B98','stroke-width':2.6},base);
    mk('rect',{x:KX+66,y:150,width:10,height:120,rx:4,fill:'#EEF3F7',stroke:'#7E8B98','stroke-width':1.6},base);
    mk('path',{d:`M${KX+71},150 L${KX+71},136 L180,136`,fill:'none',stroke:C.ink,'stroke-width':1.6},base);
    API.texText(base,186,130,'\\text{pH}',{size:18,anchor:'start',fill:C.muted});
    const drop=mk('ellipse',{cx:BX,rx:3,ry:4,fill:'#9FC3DD',opacity:0},base); let dropT=-9;
    // 그래프 틀
    const gx=mk('g',{},svg);
    [0,10,20,30,40].forEach(v=>{ mk('line',{x1:X(v),y1:AY,x2:X(v),y2:AY-AH,stroke:'#E2E7EC','stroke-width':1},gx); API.texText(gx,X(v),AY+24,String(v),{size:18,anchor:'middle',fill:C.muted}); });
    [0,7,14].forEach(p=>{ mk('line',{x1:AX,y1:Y(p),x2:AX+AW,y2:Y(p),stroke:'#E2E7EC','stroke-width':1},gx); API.texText(gx,AX-8,Y(p)+6,String(p),{size:18,anchor:'end',fill:C.muted}); });
    mk('line',{x1:AX,y1:AY,x2:AX+AW+8,y2:AY,stroke:C.muted,'stroke-width':2},gx); mk('line',{x1:AX,y1:AY,x2:AX,y2:AY-AH-8,stroke:C.muted,'stroke-width':2},gx);
    API.texText(gx,AX+8,AY-AH-4,'\\text{pH}',{size:18,anchor:'start',fill:C.muted});
    API.texText(gx,AX+AW-4,AY-10,'V_{\\ce{NaOH}}\\ [\\text{mL}]',{size:18,anchor:'end',fill:C.muted});
    const bandG=mk('g',{},svg), prevG=mk('g',{},svg), lineP=mk('path',{fill:'none',stroke:C.ink,'stroke-width':2.4,'stroke-linejoin':'round'},svg), ptsG=mk('g',{},svg), mkG=mk('g',{},svg);
    let st, rnd, prev=null, shown=0;
    function init(keepPrev){ const a=st?st.a:0, ind=st?st.ind:0; st={a,ind,rows:[],msg:''}; rnd=rng(4230+a); st.rows.push({v:0,p:meas(0)}); shown=0; if(!keepPrev) prev=null; }
    function meas(V){ return trueP(st.a,V)+0.01*gauss(rnd); }
    const V=()=>st.rows[st.rows.length-1].v;
    function analyse(){
      const rs=st.rows.slice().sort((a,b)=>a.v-b.v); let best=null;
      for(let i=1;i<rs.length;i++){ const dv=rs[i].v-rs[i-1].v; if(dv<=0) continue; const s=(rs[i].p-rs[i-1].p)/dv; if(!best||s>best.s) best={s,a:rs[i-1],b:rs[i],dp:rs[i].p-rs[i-1].p}; }
      if(!best||best.dp<1.5) return null;
      const ve=(best.a.v+best.b.v)/2, h=ve/2; let ph=null;
      for(let i=1;i<rs.length;i++) if(rs[i-1].v<=h&&rs[i].v>=h){ const t=(h-rs[i-1].v)/((rs[i].v-rs[i-1].v)||1); ph=rs[i-1].p+t*(rs[i].p-rs[i-1].p); break; }
      return {ve,h,ph,w:best.b.v-best.a.v};
    }
    function endV(ind){ // 지시약 변색이 끝나는 pH(hi)에 닿는 부피
      let lo=0, hi=VMAX; if(trueP(st.a,0)>=ind.hi) return 0;
      for(let i=0;i<50;i++){ const m=(lo+hi)/2; if(trueP(st.a,m)<ind.hi) lo=m; else hi=m; } return (lo+hi)/2; }
    function message(){
      if(st.msg) return st.msg;
      const S=SAMP[st.a], eq=analyse(), I=IND[st.ind];
      if(st.rows.length===1) return `${S.n} 25.0 mL의 처음 pH를 기록했다. 0.100 M NaOH를 넣으며 pH를 기록하자. pH가 빠르게 변하기 시작하면 0.2 mL씩 넣는다.`;
      if(!eq) return V()<5? 'pH가 천천히 오른다. 계속 넣어 곡선을 얻자.' : 'pH가 빠르게 오르기 시작하면 0.2 mL씩 넣고, pH가 11을 넘을 때까지 계속하자.';
      const c=CB*eq.ve/VA;
      let s=`ΔpH/ΔV가 가장 큰 곳 → 당량점 ≈ ${f2(eq.ve)} mL, 산의 농도 = 0.100 M × ${f2(eq.ve)} ÷ 25.0 = ${c.toFixed(4)} M.`;
      if(S.vin) s+=` 원래 식초 = 10 × ${c.toFixed(4)} = ${(10*c).toFixed(3)} M(약 ${(10*c*60.05/10).toFixed(1)} %).`;
      if(eq.ph!==null){ s+= S.weak? ` 반당량점 ${f2(eq.h)} mL의 pH ≈ ${eq.ph.toFixed(2)} → pKa ≈ ${eq.ph.toFixed(2)} (문헌 4.74).` : ` 강산은 완충 구간이 없어 반당량점 pH(${eq.ph.toFixed(2)})가 pKa가 아니다.`; }
      if(eq.w>0.45) s+=' 당량점 근처 점 사이가 넓다 — 0.2 mL씩 넣으면 더 정확하다.';
      if(I){ const ve=CB? S.C*VA/CB : 0, vend=endV(I); s+= Math.abs(vend-ve)<0.3? ` ${I.n}: 종말점 ≈ 당량점 — 알맞은 지시약.` : ` ${I.n}: ${f2(vend)} mL에서 이미 변색 → 농도를 실제보다 작게 구한다. 알맞지 않다.`; }
      return s;
    }
    function indColor(p){ const I=IND[st.ind]; if(!I) return '#DDEEF8'; return mix(I.c1,I.c2,(p-I.lo)/(I.hi-I.lo)); }
    function paint(){
      const S=SAMP[st.a], last=st.rows[st.rows.length-1];
      O('v').textContent=f2(last.v)+' mL'; O('ph').textContent=last.p.toFixed(2); O('n').textContent=st.rows.length+'개';
      O('msg').textContent=message();
      root.querySelectorAll('[data-a]').forEach(b=>b.classList.toggle('on',+b.dataset.a===st.a));
      root.querySelectorAll('[data-ind]').forEach(b=>b.classList.toggle('on',+b.dataset.ind===st.ind));
      const lv=KYb-6-(VA+last.v)*1.0; kLiq.setAttribute('y',lv); kLiq.setAttribute('height',KYb-2-lv); kLiq.setAttribute('fill',indColor(last.p));
      while(bandG.firstChild) bandG.removeChild(bandG.firstChild);
      const I=IND[st.ind]; if(I){ mk('rect',{x:AX,y:Y(I.hi),width:AW,height:Y(I.lo)-Y(I.hi),fill:I.c2,opacity:.25},bandG); mk('rect',{x:AX,y:Y((I.lo+I.hi)/2),width:AW,height:Y(I.lo)-Y((I.lo+I.hi)/2),fill:I.c1,opacity:.25},bandG); txt(API,bandG,AX+AW-4,Y(I.hi)-5,`${I.n} ${I.lo}–${I.hi}`,{size:18,anchor:'end',w:700}); }
      while(prevG.firstChild) prevG.removeChild(prevG.firstChild);
      if(prev&&prev.length>1) mk('path',{d:prev.map((r,i)=>(i?'L':'M')+X(r.v).toFixed(1)+' '+Y(r.p).toFixed(1)).join(' '),fill:'none',stroke:C.grav,'stroke-width':2.4,'stroke-dasharray':'6 4'},prevG);
      const rs=st.rows.slice().sort((a,b)=>a.v-b.v);
      lineP.setAttribute('d',rs.length>1? rs.map((r,i)=>(i?'L':'M')+X(r.v).toFixed(1)+' '+Y(r.p).toFixed(1)).join(' '):'');
      while(ptsG.firstChild) ptsG.removeChild(ptsG.firstChild);
      rs.forEach(r=>mk('circle',{cx:X(r.v),cy:Y(r.p),r:3.8,fill:'#FFFFFF',stroke:C.ink,'stroke-width':1.6},ptsG));
      while(mkG.firstChild) mkG.removeChild(mkG.firstChild);
      const eq=analyse();
      if(eq){ mk('line',{x1:X(eq.ve),y1:AY,x2:X(eq.ve),y2:AY-AH,stroke:C.plus,'stroke-width':2,'stroke-dasharray':'5 4'},mkG);
        if(eq.ph!==null&&S.weak){ mk('line',{x1:X(eq.h),y1:AY,x2:X(eq.h),y2:Y(eq.ph),stroke:C.equi,'stroke-width':2,'stroke-dasharray':'5 4'},mkG); mk('circle',{cx:X(eq.h),cy:Y(eq.ph),r:6,fill:C.equi},mkG); } }
      const tb=O('log'); tb.innerHTML='';
      st.rows.slice(-5).forEach((r,i,arr)=>{ const k=st.rows.length-arr.length+i, pr=k>0?st.rows[k-1]:null, d=pr&&r.v>pr.v?(r.p-pr.p)/(r.v-pr.v):null;
        const tr=document.createElement('tr'); tr.innerHTML=`<td>${k+1}</td><td>${S.n}</td><td>${f2(r.v)}</td><td>${r.p.toFixed(2)}</td><td>${d===null?'—':d.toFixed(2)}</td>`; tb.appendChild(tr); });
      if(window.__STILL) shown=last.v; level(shown);
    }
    function level(v){ const y=Y0+v*PPM; bLiq.setAttribute('y',y); bLiq.setAttribute('height',Math.max(0,STOP-6-y)); }
    function add(u){ st.msg=''; const v=Math.round((V()+u)*100)/100;
      if(v>VMAX+1e-9){ st.msg='뷰렛 눈금 40 mL까지만 넣을 수 있다 — 「초기화」 하자.'; paint(); return; }
      st.rows.push({v,p:meas(v)}); dropT=0; paint(); }
    root.querySelectorAll('[data-add]').forEach(b=>b.addEventListener('click',()=>add(+b.dataset.add)));
    root.querySelectorAll('[data-ind]').forEach(b=>b.addEventListener('click',()=>{ st.ind=+b.dataset.ind; st.msg=''; paint(); }));
    root.querySelectorAll('[data-a]').forEach(b=>b.addEventListener('click',()=>{ const a=+b.dataset.a; if(a===st.a&&st.rows.length===1) return;
      prev=st.rows.length>1? st.rows.slice().sort((x,y)=>x.v-y.v): prev; st.a=a; init(true);
      st.msg=`${SAMP[a].n} 25.0 mL로 새로 적정한다. 앞 곡선은 회색 점선으로 남겨 비교한다.`; paint(); }));
    $('[data-act="reset"]').addEventListener('click',()=>{ st.a=0; st.ind=0; init(false); paint(); });
    API.loop(root,(dt)=>{ const t=V(); if(Math.abs(shown-t)>1e-3){ shown+=(t-shown)*Math.min(1,dt*6); level(shown); }
      if(dropT>-9){ dropT+=dt; const q=dropT/.35; if(q>=1){ dropT=-9; drop.setAttribute('opacity',0); } else { drop.setAttribute('cy',TIP+4+(+kLiq.getAttribute('y')-TIP-4)*q*q); drop.setAttribute('opacity',1); } } });
    st=null; init(false); paint();
  },
/*@@B*/
  ac423buf(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('.lab-fig svg'), C=API.COL, mk=(t,a,p)=>API.mk(t,a,p);
    const V0=0.050, CADD=1.0, COLS=['#16233D','#2E9E6A','#7B4FC8','#E08A2C'];
    const AX=70, AY=250, AW=560, AH=222, Y=p=>AY-Math.max(0,Math.min(14,p))/14*AH;
    const truePH=(c,m)=>{ const vol=V0+Math.abs(m)/1000/CADD; const nHA=c.ha*V0, nA=c.a*V0; return phMix(nA+(m>0?m/1000:0),nHA+nA,m<0?-m/1000:0,vol); };
    const gx=mk('g',{},svg), bandG=mk('g',{},svg), crvG=mk('g',{},svg);
    let st, rnd, XM=2;
    const X=m=>AX+AW/2+m/XM*AW/2;
    function frame(){
      while(gx.firstChild) gx.removeChild(gx.firstChild);
      [-XM,-XM/2,0,XM/2,XM].forEach(m=>{ mk('line',{x1:X(m),y1:AY,x2:X(m),y2:AY-AH,stroke:'#E2E7EC','stroke-width':1},gx); txt(API,gx,X(m),AY+22,String(Math.abs(m)),{size:18,fill:C.muted}); });
      [0,2,4,6,8,10,12,14].forEach(p=>{ mk('line',{x1:AX,y1:Y(p),x2:AX+AW,y2:Y(p),stroke:'#E2E7EC','stroke-width':1},gx); txt(API,gx,AX-8,Y(p)+6,String(p),{size:18,anchor:'end',fill:C.muted}); });
      mk('line',{x1:AX,y1:AY,x2:AX+AW+6,y2:AY,stroke:C.muted,'stroke-width':2},gx); mk('line',{x1:AX,y1:AY,x2:AX,y2:AY-AH-6,stroke:C.muted,'stroke-width':2},gx);
      mk('line',{x1:X(0),y1:AY,x2:X(0),y2:AY-AH,stroke:C.muted,'stroke-width':1.5,'stroke-dasharray':'4 4'},gx);
      txt(API,gx,AX+8,AY-AH-2,'pH',{size:18,anchor:'start',fill:C.muted});
      txt(API,gx,X(-XM/2),AY+44,'← 넣은 HCl (mmol)',{size:18,fill:C.plus}); txt(API,gx,X(XM/2),AY+44,'넣은 NaOH (mmol) →',{size:18,fill:C.minus});
    }
    const fc=v=>v<0.1-1e-9? v.toFixed(3) : v.toFixed(2);
    const key=c=>c.water?'증류수':`${fc(c.ha)} / ${fc(c.a)}`;
    function init(){ st={c:{ha:0.10,a:0.10,water:false},recs:{},order:[],side:0,log:[],msg:'',nc:0}; rnd=rng(4231); XM=2; ensure(); }
    function shownRecs(){ const R=cur(), ks=st.order.slice(-4); if(!ks.includes(R.k)) ks.push(R.k); return ks.slice(-4).map(k=>st.recs[k]); }
    const capTxt=(r,v)=>v===null?'—':(r.c.water?'&lt; '+f2(v):f2(v));
    function cur(){ return st.recs[key(st.c)]; }
    function ensure(){ const k=key(st.c); if(!st.recs[k]){ const c=Object.assign({},st.c); if(c.water){ c.ha=0; c.a=0; }
        const p0=c.water?7.00:truePH(c,0); st.recs[k]={c,k,p0:Math.round((p0+0.01*gauss(rnd))*100)/100,acid:[{m:0,p:0}],base:[{m:0,p:0}],col:null,capA:null,capB:null}; st.recs[k].acid[0].p=st.recs[k].p0; st.recs[k].base[0].p=st.recs[k].p0; }
      st.side=0; }
    function meas(c,m){ if(c.water&&m===0) return 7.00; const p=c.water? phMix(m>0?m/1000:0,0,m<0?-m/1000:0,V0+Math.abs(m)/1000) : truePH(c,m); return Math.round((p+0.01*gauss(rnd))*100)/100; }
    function capOf(arr,p0){ for(let i=1;i<arr.length;i++){ const d1=Math.abs(arr[i-1].p-p0), d2=Math.abs(arr[i].p-p0); if(d2>=1){ const t=(1-d1)/((d2-d1)||1); return Math.abs(arr[i-1].m+t*(arr[i].m-arr[i-1].m)); } } return null; }
    function message(){
      if(st.msg) return st.msg; const R=cur();
      const done=st.order.map(k=>st.recs[k]).filter(r=>r.capA!==null&&r.capB!==null&&!r.c.water);
      if(R.c.water&&(R.capA!==null||R.capB!==null)) return `증류수는 ${f2(R.capA!==null?R.capA:R.capB)} mmol만 넣어도 pH가 ${f2(Math.abs((st.side<0?R.acid:R.base).slice(-1)[0].p-R.p0))}만큼 변한다 — 완충 작용이 없다.`;
      if(R.acid.length===1&&R.base.length===1) return `${R.c.water?'증류수':'완충 용액'} 50.0 mL, 처음 pH ${f2(R.p0)}. 1.0 M HCl이나 NaOH를 넣으며 pH가 처음보다 1 바뀔 때까지 기록하자.`;
      let s='';
      if(R.capA===null||R.capB===null) s=`${key(R.c)}: ${R.capA!==null?`산 쪽 완충 용량 ${f2(R.capA)} mmol. `:''}${R.capB!==null?`염기 쪽 완충 용량 ${f2(R.capB)} mmol. `:''}처음 pH ± 1에 이를 때까지 산 쪽과 염기 쪽을 모두 재자(산과 염기는 다른 비커).`;
      else s=`${key(R.c)}: 산 쪽 ${f2(R.capA)} mmol, 염기 쪽 ${f2(R.capB)} mmol.`;
      if(done.length>=2){ const a=done.reduce((x,y)=>(x.c.ha+x.c.a)<(y.c.ha+y.c.a)?x:y), b=done.reduce((x,y)=>(x.c.ha+x.c.a)>(y.c.ha+y.c.a)?x:y);
        if(b!==a){ const rc=(b.c.ha+b.c.a)/(a.c.ha+a.c.a), rk=(b.capA+b.capB)/(a.capA+a.capB); s+=` 비교: 짝산+짝염기 농도가 ${rc.toFixed(1)}배이면 완충 용량(산+염기)도 약 ${rk.toFixed(1)}배 — 농도가 높을수록 완충 용량이 크다.`; } }
      if(!R.c.water&&R.capA!==null&&R.capB!==null&&Math.abs(R.c.ha-R.c.a)>1e-9) s+= R.c.ha>R.c.a? ' 짝산이 더 많으면 염기를 더 많이 견딘다.' : ' 짝염기가 더 많으면 산을 더 많이 견딘다.';
      return s;
    }
    function paint(){
      const R=cur();
      root.querySelectorAll('[data-ha]').forEach(b=>b.classList.toggle('on',!st.c.water&&Math.abs(+b.dataset.ha-st.c.ha)<1e-9));
      root.querySelectorAll('[data-ba]').forEach(b=>b.classList.toggle('on',!st.c.water&&Math.abs(+b.dataset.ba-st.c.a)<1e-9));
      $('[data-act="water"]').classList.toggle('on',st.c.water);
      const arr=st.side<0?R.acid:(st.side>0?R.base:null), last=arr?arr[arr.length-1]:{m:0,p:R.p0};
      O('comp').textContent=R.c.water?'증류수 50.0 mL':`${key(R.c)} M`; O('p0').textContent=f2(R.p0);
      O('add').textContent=last.m===0?'없음':(last.m<0?`HCl ${f2(-last.m)} mmol`:`NaOH ${f2(last.m)} mmol`);
      O('ph').textContent=f2(last.p); O('dp').textContent=(last.p-R.p0>=0?'+':'')+f2(last.p-R.p0);
      // x 범위
      let mx=0; shownRecs().forEach(r=>{ r.acid.concat(r.base).forEach(q=>mx=Math.max(mx,Math.abs(q.m))); });
      XM=[1,2,5,10,15,20].find(v=>v>=mx*1.05)||20; frame();
      while(bandG.firstChild) bandG.removeChild(bandG.firstChild);
      mk('rect',{x:AX,y:Y(R.p0+1),width:AW,height:Y(R.p0-1)-Y(R.p0+1),fill:'#FFE45C',opacity:.3},bandG);
      txt(API,bandG,AX+6,Y(R.p0+1)-5,'처음 pH ± 1',{size:18,anchor:'start',w:700});
      while(crvG.firstChild) crvG.removeChild(crvG.firstChild);
      shownRecs().forEach((r,j)=>{ const k=r.k, col=r.col||COLS[st.nc%4]; if(!r.col&&r.acid.length+r.base.length<=2) return;
        [r.acid,r.base].forEach(a=>{ if(a.length<2) return; mk('path',{d:a.map((q,i)=>(i?'L':'M')+X(q.m).toFixed(1)+' '+Y(q.p).toFixed(1)).join(' '),fill:'none',stroke:col,'stroke-width':k===key(st.c)?3.2:2.2,'stroke-dasharray':r.c.water?'4 4':null},crvG);
          a.forEach(q=>mk('circle',{cx:X(q.m),cy:Y(q.p),r:3.6,fill:'#FFFFFF',stroke:col,'stroke-width':1.6},crvG)); });
        txt(API,crvG,AX+AW-4,AY-AH+16+j*22,(r.c.water?'증류수':key(r.c)+' M'),{size:18,anchor:'end',fill:col,w:700}); });
      O('msg').textContent=message();
      const tb=O('log'); tb.innerHTML='';
      st.log.slice(-4).forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${r.add}</td><td>${f2(r.p)}</td><td>${(r.d>=0?'+':'')+f2(r.d)}</td>`; tb.appendChild(tr); });
      const tc=O('cap'); tc.innerHTML='';
      st.order.slice(-4).forEach(k=>{ const r=st.recs[k]; const tr=document.createElement('tr'); tr.innerHTML=`<td style="color:${r.col}">${r.c.water?'증류수':k}</td><td>${f2(r.p0)}</td><td>${capTxt(r,r.capA)}</td><td>${capTxt(r,r.capB)}</td>`; tc.appendChild(tr); });
    }
    function add(m){ st.msg=''; const R=cur(), side=m<0?-1:1;
      if(st.side!==0&&st.side!==side) st.msg='산과 염기는 다른 비커에 넣는다 — 같은 용액 50.0 mL를 새 비커에 담아 이어서 잰다.';
      st.side=side; const arr=side<0?R.acid:R.base, last=arr[arr.length-1], nm=Math.round((last.m+m)*100)/100;
      if(Math.abs(nm)>20+1e-9){ st.msg='20 mmol(20 mL)까지만 넣는다.'; paint(); return; }
      const p=meas(R.c,nm); arr.push({m:nm,p});
      if(!R.col){ R.col=COLS[st.nc%4]; st.nc++; st.order.push(R.k); }
      if(R.c.water){ if(side<0&&R.capA===null&&Math.abs(p-R.p0)>=1) R.capA=-nm; if(side>0&&R.capB===null&&Math.abs(p-R.p0)>=1) R.capB=nm; }
      else { if(side<0&&R.capA===null) R.capA=capOf(R.acid,R.p0); if(side>0&&R.capB===null) R.capB=capOf(R.base,R.p0); }
      st.log.push({k:R.c.water?'증류수':key(R.c),add:nm<0?`HCl ${f2(-nm)}`:`NaOH ${f2(nm)}`,p,d:p-R.p0});
      paint(); }
    root.querySelectorAll('[data-add]').forEach(b=>b.addEventListener('click',()=>add(+b.dataset.add)));
    root.querySelectorAll('[data-ha]').forEach(b=>b.addEventListener('click',()=>{ st.c={ha:+b.dataset.ha,a:st.c.water?0.10:st.c.a,water:false}; st.msg=''; ensure(); paint(); }));
    root.querySelectorAll('[data-ba]').forEach(b=>b.addEventListener('click',()=>{ st.c={ha:st.c.water?0.10:st.c.ha,a:+b.dataset.ba,water:false}; st.msg=''; ensure(); paint(); }));
    $('[data-act="water"]').addEventListener('click',()=>{ st.c={ha:0,a:0,water:true}; st.msg=''; ensure(); paint(); });
    $('[data-act="fresh"]').addEventListener('click',()=>{ st.side=0; st.msg='새 비커에 같은 용액 50.0 mL를 담았다.'; paint(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ init(); paint(); });
    init(); paint();
  },
