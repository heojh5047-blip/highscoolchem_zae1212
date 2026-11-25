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
window.DECK_LABS = {

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
};
})();
