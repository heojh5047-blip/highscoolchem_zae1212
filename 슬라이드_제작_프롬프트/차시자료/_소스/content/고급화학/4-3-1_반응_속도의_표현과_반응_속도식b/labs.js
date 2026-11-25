/* 고급화학 4-3-1b — 실험실 ac431ord : ◆ 지도서 디지털 탐구 Ⅳ-4 「색 센서로 크리스털 바이올렛의 탈색 반응 차수 구하기」 + 교과서 적분 속도식 자료 비교
   자료 (가) CV+ + OH- → CVOH, 25 °C: 흡광도 A ∝ [CV+], A0 = 0.80, k = 0.20 L/(mol·s), 유사 1차 k' = k[OH-] ([OH-] 0.025·0.050·0.10 M 고름),
         15 s 간격 10 min 측정, A < 0.02이면 멈춤(검출 한계). 측정 잡음 σ = 0.6 % + 0.0008 (고정 시드).
   자료 (나) 2NO2 → 2NO + O2, 300 °C: 2차, k = 0.541 L/(mol·s), [NO2]0 = 8.00×10⁻³ M, 50 s 간격 500 s (잡음 0.5 %).
   자료 (다) 2NH3 → N2 + 3H2 (W 표면): 0차, k = 1.0×10⁻⁵ M/s, [NH3]0 = 4.00×10⁻³ M, 25 s 간격 375 s (잡음 0.5 % + 5×10⁻⁶ M).
   그래프 고르기([A]·ln[A]·1/[A]–t) → 최소 제곱 직선과 결정 계수 R² → 판정(0·1·2차) → 기록 표(직선 그래프, R², k, t½)에 쌓임.
   (가)를 두 [OH-]에서 1차로 판정하면 k'/[OH-]를 비교해 OH-에 대한 차수를 알려 준다. */
(function(){
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=Math.imul(a^(a>>>15),1|a); t=(t+Math.imul(t^(t>>>7),61|t))^t; return ((t^(t>>>14))>>>0)/4294967296; }; }
function gauss(r){ let u=0,v=0; while(u===0)u=r(); v=r(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||18,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
function lsq(xs,ys){ const n=xs.length, mx=xs.reduce((a,b)=>a+b,0)/n, my=ys.reduce((a,b)=>a+b,0)/n; let sxx=0,sxy=0,syy=0;
  for(let i=0;i<n;i++){ sxx+=(xs[i]-mx)**2; sxy+=(xs[i]-mx)*(ys[i]-my); syy+=(ys[i]-my)**2; } const b=sxy/sxx; return {b,a:my-b*mx,r2:sxy*sxy/(sxx*syy)}; }
function sci(v,d=2){ if(v===0) return '0'; const a=Math.abs(v); if(a>=0.01&&a<1000) return v.toPrecision(d+1).replace(/\.?0+$/,m=>m.includes('.')?'':m); const e=Math.floor(Math.log10(a)); const m=v/Math.pow(10,e); return m.toFixed(d)+'×10^'+e; }
function sup(s){ return s.replace(/\^(-?\d+)/,(m,e)=>'<sup>'+e.replace('-','−')+'</sup>'); }
const S=(v,d)=>sup(sci(v,d));
function tick(v){ const a=Math.abs(v); if(a===0) return '0'; if(a>=10) return v.toFixed(0); if(a>=0.1) return v.toFixed(2); return v.toExponential(1).replace('e','E'); }
window.DECK_LABS = {
  ac431ord(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('.lab-fig svg'), C=API.COL, mk=(t,a,p)=>API.mk(t,a,p);
    const AX=78, AY=258, AW=400, AH=220;
    const RX={
      cv:{nm:'(가) 크리스털 바이올렛',ord:1,dt:15,tmax:600,c0:0.80,yn:['A','\\ln A','1/A'],un:['흡광도/s','s<sup>−1</sup>','1/(흡광도·s)'],
          f:(t,oh)=>0.80*Math.exp(-0.20*oh*t),noise:(v,r)=>v*(1+0.006*gauss(r))+0.0008*gauss(r),stop:0.02},
      no2:{nm:'(나) 이산화 질소',ord:2,dt:50,tmax:500,c0:8.00e-3,yn:['[\\ce{NO2}]','\\ln[\\ce{NO2}]','1/[\\ce{NO2}]'],un:['M/s','s<sup>−1</sup>','L/(mol·s)'],
          f:t=>1/(0.541*t+125),noise:(v,r)=>v*(1+0.005*gauss(r)),stop:0},
      nh3:{nm:'(다) 암모니아',ord:0,dt:25,tmax:375,c0:4.00e-3,yn:['[\\ce{NH3}]','\\ln[\\ce{NH3}]','1/[\\ce{NH3}]'],un:['M/s','s<sup>−1</sup>','L/(mol·s)'],
          f:t=>Math.max(4.00e-3-1.0e-5*t,0),noise:(v,r)=>v*(1+0.005*gauss(r))+5e-6*gauss(r),stop:0}
    };
    const tr=[v=>v,v=>Math.log(v),v=>1/v];
    const gx=mk('g',{},svg), gd=mk('g',{},svg), gc=mk('g',{},svg);
    // 시료 칸(색은 측정 재생에 따라 바뀜)
    mk('rect',{x:540,y:40,width:60,height:110,rx:4,fill:'#fff',stroke:C.ink,'stroke-width':2.5},gc);
    const cell=mk('rect',{x:543,y:60,width:54,height:87,fill:'#6A2C91','fill-opacity':.8},gc);
    const cur=txt(API,gc,570,178,'',{size:18}); txt(API,gc,570,30,'시료',{size:18,fill:C.muted});
    let st, rnd, play=0;
    function init(){ st={rx:'cv',oh:0.05,gr:0,data:null,run:0,log:[],msg:'자료와 조건을 고른 뒤 「측정하기」를 누르세요.'}; rnd=rng(4311); play=0; sync(); draw(); }
    function measure(){ const R=RX[st.rx]; st.run++; const ts=[],cs=[];
      for(let t=0;t<=R.tmax+1e-9;t+=R.dt){ const v=R.f(t,st.oh); let m=R.noise(v,rnd); if(R.stop&&m<R.stop) break; if(m<=0) break; ts.push(t); cs.push(m); }
      st.data={rx:st.rx,oh:st.oh,ts,cs,run:st.run}; play=0;
      st.msg=`${R.nm}: ${ts.length}개 측정${R.stop&&ts[ts.length-1]<R.tmax?' (흡광도가 0.02 아래로 내려가 '+ts[ts.length-1]+' s에서 멈춤)':''}. 세 그래프 가운데 직선인 것을 찾으세요.`; draw(); }
    function fit(){ const d=st.data; if(!d) return null; return lsq(d.ts,d.cs.map(tr[st.gr])); }
    function judge(o){ const d=st.data; if(!d){ st.msg='먼저 측정하세요.'; draw(); return; } const R=RX[d.rx];
      const fits=[0,1,2].map(g=>lsq(d.ts,d.cs.map(tr[g]))); const F=fits[o]; const ok=(o===R.ord);
      let k=null,h=null;
      if(ok){ k=(o===2?F.b:-F.b); const c0=d.cs[0]; h=o===0?c0/(2*k):(o===1?Math.LN2/k:1/(k*c0)); }
      const cond=d.rx==='cv'?` ${d.oh.toFixed(3)} M`:'';
      st.log.push({run:d.run,rx:R.nm.slice(0,3)+cond,gr:['[A]–t','ln[A]–t','1/[A]–t'][o],r2:F.r2,ok,o,k,h,un:R.un[o],rxk:d.rx,oh:d.oh});
      if(!ok){ st.msg=`${o}차라면 ${['[A]','ln[A]','1/[A]'][o]}–t가 직선이어야 하는데 R<sup>2</sup> = ${F.r2.toFixed(3)}로 휘어 있습니다. R<sup>2</sup>가 1에 가장 가까운 그래프를 다시 찾아보세요.`; }
      else { st.msg=`맞습니다: ${['[A]','ln[A]','1/[A]'][o]}–t가 직선(R<sup>2</sup> = ${F.r2.toFixed(4)}) → ${o}차 반응. k = ${o===2?'기울기':'−기울기'} = ${S(k,2)} ${R.un[o]}, t<sub>1/2</sub> = ${h.toFixed(0)} s.`;
        if(d.rx==='cv'){ const cvs=st.log.filter(r=>r.ok&&r.rxk==='cv'); const ohs=[...new Set(cvs.map(r=>r.oh))];
          if(ohs.length>=2){ const a=cvs.find(r=>r.oh===Math.min(...ohs)), b=cvs.find(r=>r.oh===Math.max(...ohs)); const rk=b.k/a.k, ro=b.oh/a.oh;
            st.msg+=` 수산화 이온 농도가 ${ro.toFixed(1)}배일 때 k′는 ${rk.toFixed(2)}배 → 수산화 이온에도 1차, k = k′ ÷ (수산화 이온 농도) ≈ ${(b.k/b.oh).toFixed(2)} L/(mol·s).`; }
          else st.msg+=' 이것은 유사 1차 속도 상수 k′이다. 수산화 이온 농도를 바꾸어 다시 재 보세요.'; } }
      draw(); }
    function sync(){
      root.querySelectorAll('[data-rx]').forEach(b=>b.classList.toggle('on',b.dataset.rx===st.rx));
      root.querySelectorAll('[data-oh]').forEach(b=>b.classList.toggle('on',Math.abs(+b.dataset.oh-st.oh)<1e-9));
      O('ohrow').classList.toggle('ac431-off',st.rx!=='cv');
      root.querySelectorAll('[data-gr]').forEach(b=>b.classList.toggle('on',+b.dataset.gr===st.gr));
    }
    function draw(){
      while(gx.firstChild) gx.removeChild(gx.firstChild); while(gd.firstChild) gd.removeChild(gd.firstChild);
      const d=st.data, R=RX[d?d.rx:st.rx];
      mk('line',{x1:AX,y1:AY,x2:AX+AW+6,y2:AY,stroke:C.muted,'stroke-width':2},gx); mk('line',{x1:AX,y1:AY,x2:AX,y2:AY-AH-6,stroke:C.muted,'stroke-width':2},gx);
      const tmax=R.tmax; const X=t=>AX+t/tmax*AW;
      for(let i=0;i<=5;i++){ const t=tmax*i/5; mk('line',{x1:X(t),y1:AY,x2:X(t),y2:AY+5,stroke:C.muted,'stroke-width':1.5},gx); txt(API,gx,X(t),AY+24,String(Math.round(t)),{size:18,fill:C.muted}); }
      Ov('ylab').innerHTML=API.tex(R.yn[st.gr]); API.place(Ov('ylab'),AX-8,AY-AH-22,true); API.place(Ov('xlab'),AX+AW-10,AY+46,true);
      O('rx').textContent=d?RX[d.rx].nm+(d.rx==='cv'?` · 수산화 이온 ${d.oh.toFixed(3)} M`:''):'—';
      O('np').textContent=d?d.ts.length+'개':'—';
      if(d){ const ys=d.cs.map(tr[st.gr]); let lo=Math.min(...ys), hi=Math.max(...ys); const pad=(hi-lo)*0.08||1; lo-=pad; hi+=pad;
        const Y=v=>AY-(v-lo)/(hi-lo)*AH;
        for(let i=0;i<=4;i++){ const v=lo+(hi-lo)*i/4; mk('line',{x1:AX,y1:Y(v),x2:AX+AW,y2:Y(v),stroke:'#E2E7EC','stroke-width':1},gx); txt(API,gx,AX-6,Y(v)+6,tick(v),{size:17,anchor:'end',fill:C.muted}); }
        const F=fit(), good=F.r2>=0.995;
        mk('line',{x1:X(0),y1:Y(F.a),x2:X(d.ts[d.ts.length-1]),y2:Y(F.a+F.b*d.ts[d.ts.length-1]),stroke:good?C.field:C.muted,'stroke-width':good?4:2,'stroke-dasharray':good?'':'8 6'},gd);
        d.ts.forEach((t,i)=>mk('circle',{cx:X(t),cy:Y(ys[i]),r:4.5,fill:i<=play*d.ts.length?C.ink:'#C9D2DB'},gd));
        txt(API,gd,AX+AW-4,AY-AH+14,good?'직선!':'곡선',{size:19,anchor:'end',fill:good?C.field:C.muted,w:700});
        O('slope').innerHTML=S(F.b,2)+' '+R.un[st.gr]; O('r2').textContent=F.r2.toFixed(4);
      } else { O('slope').textContent='—'; O('r2').textContent='—'; }
      O('msg').innerHTML=st.msg;
      const tb=O('log'); tb.innerHTML='';
      st.log.slice(-4).forEach(r=>{ const e=document.createElement('tr'); e.innerHTML=`<td>${r.run}</td><td>${r.rx}</td><td>${r.gr}</td><td>${r.r2.toFixed(3)}</td><td style="color:${r.ok?C.field:C.plus}">${r.o}차 ${r.ok?'○':'×'}</td><td>${r.ok?S(r.k,2):'—'}</td><td>${r.ok?r.h.toFixed(0)+' s':'—'}</td>`; tb.appendChild(e); });
      paint();
    }
    function paint(){ const d=st.data; if(!d){ cell.setAttribute('fill-opacity',.0); cur.textContent=''; return; }
      const i=Math.min(d.ts.length-1,Math.floor(play*d.ts.length)); const R=RX[d.rx];
      const frac=Math.max(0,Math.min(1,d.cs[i]/R.c0));
      cell.setAttribute('fill',d.rx==='cv'?'#6A2C91':(d.rx==='no2'?'#A4421A':'#D8DEE4'));
      cell.setAttribute('fill-opacity',(d.rx==='nh3'?0.5:0.85*frac).toFixed(3)); cur.textContent=d.ts[i]+' s'; }
    root.querySelectorAll('[data-rx]').forEach(b=>b.addEventListener('click',()=>{ st.rx=b.dataset.rx; sync(); draw(); }));
    root.querySelectorAll('[data-oh]').forEach(b=>b.addEventListener('click',()=>{ st.oh=+b.dataset.oh; sync(); draw(); }));
    root.querySelectorAll('[data-gr]').forEach(b=>b.addEventListener('click',()=>{ st.gr=+b.dataset.gr; sync(); draw(); }));
    root.querySelectorAll('[data-ord]').forEach(b=>b.addEventListener('click',()=>judge(+b.dataset.ord)));
    $('[data-act="measure"]').addEventListener('click',measure);
    $('[data-act="reset"]').addEventListener('click',init);
    API.loop(root,(dt)=>{ if(!st.data||play>=1) return; play=Math.min(1,play+dt/3.0); draw(); });
    init();
  }
};
})();
