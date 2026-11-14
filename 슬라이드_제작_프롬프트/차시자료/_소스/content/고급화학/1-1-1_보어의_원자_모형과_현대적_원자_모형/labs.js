/* 고급화학 1-1-1 — 실험실
   ac111spec : 간이 분광기 실험실 (필수 탐구 고화-탐01)
     · 광원 관찰: 백열전구(연속)·H·He·Ne·Na·Hg 선 스펙트럼(문헌 주요 선, nm), 관찰 눈금 커서,
       「측정 기록」= 커서 ±6 nm 안 가장 가까운 선을 고정 시드 오차(±1.5 nm)로 읽어 표에 쌓음.
     · 수소 전이 계산: n_i(2–7) → n_f(1·2·3), ΔE = −2.178e-18 (1/nf² − 1/ni²) J, λ = hc/|ΔE| (h 6.626e-34, c 3.00e8).
   ac111rdf : 방사 분포 함수 (지도서 디지털 탐구 Ⅰ-1)
     · R1s = 2e^{-r}, R2s = (2−r)e^{-r/2}/(2√2), R3s = 2/(81√3)(27−18r+2r²)e^{-r/3}  (r: a0 단위)
     · P = r²R², 0–r 확률 = Σ P Δr (Δr = 0.01 사각형 합). 그래프 R / R² / P, 최댓값·마디 찾기, 기록 표. */
(function(){
function wlColor(w){
  const fix={656:'#E8322B',486:'#21B5C9',434:'#3D4FE0',410:'#7B3FC4'};
  for(const k in fix) if(Math.abs(w-k)<2.5) return fix[k];
  if(w<380||w>750) return null;
  let r,g,b;
  if(w<440){r=-(w-440)/60;g=0;b=1;} else if(w<490){r=0;g=(w-440)/50;b=1;} else if(w<510){r=0;g=1;b=-(w-510)/20;}
  else if(w<580){r=(w-510)/70;g=1;b=0;} else if(w<645){r=1;g=-(w-645)/65;b=0;} else {r=1;g=0;b=0;}
  const fac=w<420?.3+.7*(w-380)/40:(w<=700?1:.3+.7*(750-w)/50);
  const h=c=>Math.round(255*Math.pow(c*fac,.8)).toString(16).padStart(2,'0');
  return '#'+h(r)+h(g)+h(b);
}
function colName(w){ if(w<380) return '자외선'; if(w>750) return '적외선'; if(w<450) return '보라'; if(w<480) return '파랑'; if(w<500) return '청록'; if(w<565) return '초록'; if(w<590) return '노랑'; if(w<625) return '주황'; return '빨강'; }
function sci(x){ const e=Math.floor(Math.log10(Math.abs(x))), m=x/Math.pow(10,e), sup={'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}; return m.toFixed(3)+'×10'+String(e).split('').map(c=>sup[c]).join(''); }
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=Math.imul(a^(a>>>15),1|a); t=(t+Math.imul(t^(t>>>7),61|t))^t; return ((t^(t>>>14))>>>0)/4294967296; }; }

window.DECK_LABS = {
  ac111spec(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg');
    const LINES={
      H:[[656.3,1],[486.1,.6],[434.0,.35],[410.2,.25]],
      He:[[706.5,.5],[667.8,.6],[587.6,1],[501.6,.4],[492.2,.25],[471.3,.3],[447.1,.6]],
      Ne:[[585.2,.8],[588.2,.4],[594.5,.6],[603.0,.4],[607.4,.5],[609.6,.6],[614.3,.8],[616.4,.4],[621.7,.5],[626.6,.6],[633.4,.7],[638.3,.6],[640.2,1],[650.7,.7],[659.9,.4],[703.2,.6]],
      Na:[[589.0,1],[589.6,.8]],
      Hg:[[404.7,.5],[435.8,1],[546.1,1],[577.0,.6],[579.1,.6]] };
    const NAME={lamp:'백열전구',H:'수소',He:'헬륨',Ne:'네온',Na:'나트륨',Hg:'수은'};
    const W0=380,W1=740,X0=30,X1=570, X=w=>X0+(w-W0)/(W1-W0)*(X1-X0);
    const YL=n=>n===0?145:145+140/(n*n);
    let st={mode:'src',src:'H',nf:2}, log=[], rand=rng(20261113);
    // 정적 부품
    const stat=API.mk('g',{},svg);
    const defs=API.mk('defs',{},stat), gr=API.mk('linearGradient',{id:'grad-ac111-12',x1:0,x2:1,y1:0,y2:0},defs);
    for(let w=W0;w<=W1;w+=10){ const c=wlColor(w); if(c) API.mk('stop',{offset:((w-W0)/(W1-W0)).toFixed(3),'stop-color':c},gr); }
    API.mk('rect',{x:X0,y:20,width:X1-X0,height:70,fill:'#111',rx:4},stat);
    [400,500,600,700].forEach(w=>{ API.mk('line',{x1:X(w),y1:90,x2:X(w),y2:97,stroke:'#5B6B7F','stroke-width':1.5},stat); API.texText(stat,X(w),118,`${w}\\ \\text{nm}`,{size:18,anchor:'middle'}); });
    const gSrc=API.mk('g',{},stat), gH=API.mk('g',{},stat);
    API.mk('line',{x1:X0,y1:280,x2:X1,y2:280,stroke:'#5B6B7F','stroke-width':1.5},gSrc);
    API.texText(gSrc,X0,148,'상대 세기',{size:18,anchor:'start',mix:true,fill:'#5B6B7F'});
    [1,2,3,4,5,6,7,0].forEach(n=>API.mk('line',{x1:90,y1:YL(n),x2:520,y2:YL(n),stroke:'#16233D','stroke-width':n&&n<4?2:1.2,...(n===0?{'stroke-dasharray':'5 4'}:{})},gH));
    [1,2,3].forEach(n=>API.texText(gH,528,YL(n)+6,`n=${n}`,{size:18,anchor:'start'}));
    API.texText(gH,82,YL(0)+6,'n=\\infty',{size:18,anchor:'end'});
    const g=API.mk('g',{},svg);

    function hLam(ni,nf){ const dE=-2.178e-18*(1/(nf*nf)-1/(ni*ni)); return {dE, lam:6.626e-34*3.00e8/Math.abs(dE)*1e9}; }
    function series(nf){ return nf===1?'라이먼 계열 (자외선)':nf===2?'발머 계열 (가시광선)':'파센 계열 (적외선)'; }
    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      gSrc.style.display=st.mode==='src'?'':'none'; gH.style.display=st.mode==='h'?'':'none';
      root.querySelector('[data-set="src"]').style.display=st.mode==='src'?'':'none';
      root.querySelector('[data-set="h"]').style.display=st.mode==='h'?'':'none';
      root.querySelectorAll('[data-m]').forEach(b=>b.classList.toggle('on',b.dataset.m===st.mode));
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===st.src));
      root.querySelectorAll('[data-f]').forEach(b=>b.classList.toggle('on',+b.dataset.f===st.nf));
      API.place(Ov('t1'),0,0,false);
      if(st.mode==='src'){
        const cur=+I('cur').value; O('cur').textContent=cur+' nm';
        if(st.src==='lamp'){
          API.mk('rect',{x:X(400),y:20,width:X(700)-X(400),height:70,fill:'url(#grad-ac111-12)'},g);
          const pts=[]; for(let w=400;w<=700;w+=5) pts.push(`${X(w).toFixed(1)} ${(280-90*Math.exp(-Math.pow((w-640)/160,2))).toFixed(1)}`);
          API.mk('path',{d:'M'+pts.join(' L'),fill:'none',stroke:'#E08A2C','stroke-width':2.5},g);
        } else LINES[st.src].forEach(([w,a])=>{
          const c=wlColor(w)||'#888';
          API.mk('rect',{x:X(w)-2,y:20,width:4,height:70,fill:c,opacity:(.45+.55*a).toFixed(2)},g);
          API.mk('line',{x1:X(w),y1:280,x2:X(w),y2:280-110*a,stroke:c,'stroke-width':4},g);
        });
        API.mk('line',{x1:X(cur),y1:12,x2:X(cur),y2:286,stroke:'#16233D','stroke-width':1.5,'stroke-dasharray':'4 3'},g);
        API.mk('polygon',{points:`${X(cur)-7},6 ${X(cur)+7},6 ${X(cur)},16`,fill:'#16233D'},g);
        const near=nearest(cur);
        O('rlab').textContent='관찰 눈금 근처의 선';
        if(st.src==='lamp'){ O('big').textContent='연속'; O('msg').textContent='백열전구: 모든 파장의 빛이 이어진 연속 스펙트럼 — 선이 없다.'; }
        else if(near){ O('big').textContent='약 '+Math.round(near[0])+' nm'; O('msg').textContent=`${NAME[st.src]}: 선 ${LINES[st.src].length}개가 보인다. 눈금 근처 선은 ${colName(near[0])}빛. 「측정 기록」으로 읽은 값을 표에 남기자.`; }
        else { O('big').textContent='—'; O('msg').textContent=`${NAME[st.src]}: 눈금 근처(±6 nm)에 선이 없다. 눈금을 밝은 선에 맞추자.`; }
      } else {
        const ni=+I('ni').value, nf=st.nf; O('ni').textContent=ni;
        O('rlab').textContent='계산한 파장';
        if(ni<=nf){ O('big').textContent='—'; O('msg').textContent=`처음 준위가 나중 준위(n = ${nf})보다 높아야 빛을 방출한다. 처음 준위를 올리자.`; return; }
        const {dE,lam}=hLam(ni,nf), c=wlColor(lam);
        const x=150+ (ni-2)*55;
        API.arrow(g,x,YL(ni),x,YL(nf),c||'#16233D',3.5);
        if(c){ API.mk('rect',{x:X(lam)-2.5,y:20,width:5,height:70,fill:c},g); }
        else { API.place(Ov('t1'),300,48,true); Ov('t1').style.color='#fff'; Ov('t1').textContent=(lam<380?'자외선':'적외선')+' — 눈에 보이지 않는다 (화면 밖)'; }
        O('big').textContent=(lam<1000?lam.toFixed(1):Math.round(lam))+' nm';
        O('msg').textContent=`n = ${ni} → ${nf}: ΔE = ${sci(dE)} J (방출). ${series(nf)}${c?' — '+colName(lam)+'빛':''}.`;
      }
    }
    function nearest(cur){ if(st.src==='lamp') return null; let b=null; LINES[st.src].forEach(l=>{ if(Math.abs(l[0]-cur)<=6&&(!b||Math.abs(l[0]-cur)<Math.abs(b[0]-cur))) b=l; }); return b; }
    function rec(){
      let row;
      if(st.mode==='src'){
        const n=nearest(+I('cur').value);
        if(!n){ O('msg').textContent=st.src==='lamp'?'연속 스펙트럼에는 읽을 선이 없다.':'눈금 근처에 선이 없어 기록하지 않았다.'; return; }
        const read=n[0]+(rand()*3-1.5);
        row=[NAME[st.src], read.toFixed(1)+' nm', n[0].toFixed(1)+' nm', colName(n[0])];
      } else {
        const ni=+I('ni').value, nf=st.nf; if(ni<=nf) return;
        const {dE,lam}=hLam(ni,nf);
        row=[`수소 ${ni} → ${nf}`, (lam<1000?lam.toFixed(1):Math.round(lam))+' nm', sci(dE)+' J', series(nf).replace(/.*\((.*)\)/,'$1')];
      }
      log.push(row); if(log.length>5) log.shift();
      O('log').innerHTML=log.map(r=>'<tr>'+r.map(c=>`<td>${c}</td>`).join('')+'</tr>').join('');
      O('msg').textContent='기록했다 ('+log.length+'행). 문헌값·계산값과 비교해 보자.';
    }
    root.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>{st.mode=b.dataset.m; draw();}));
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{st.src=b.dataset.s; draw();}));
    root.querySelectorAll('[data-f]').forEach(b=>b.addEventListener('click',()=>{st.nf=+b.dataset.f; draw();}));
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',draw));
    $('[data-act="rec"]').addEventListener('click',rec);
    $('[data-act="reset"]').addEventListener('click',()=>{ st={mode:'src',src:'H',nf:2}; log=[]; rand=rng(20261113); I('cur').value=656; I('ni').value=3; O('log').innerHTML=''; draw(); });
    draw(); API.onShow&&API.onShow(draw);
  },

  ac111rdf(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), fig=$('.lab-fig');
    const X0=70,X1=590,Y0=286,Y1=22, X=r=>X0+r/20*(X1-X0);
    const ORB=[
      {k:'1s',R:r=>2*Math.exp(-r),col:'#16233D',max:1.0,nodes:[]},
      {k:'2s',R:r=>(2-r)*Math.exp(-r/2)/(2*Math.SQRT2),col:'#2E9E6A',max:5.236,nodes:[2.0]},
      {k:'3s',R:r=>2/(81*Math.sqrt(3))*(27-18*r+2*r*r)*Math.exp(-r/3),col:'#7B4FC8',max:13.074,nodes:[1.902,7.098]}];
    const DR=0.01, N=2001;
    ORB.forEach(o=>{ o.cum=new Float64Array(N); let s=0; for(let i=0;i<N;i++){ const r=i*DR, p=r*r*o.R(r)**2; o.cum[i]=s; s+=p*DR; } });
    let st={view:'P',node:-1}, log=[];
    const stat=API.mk('g',{},svg);
    API.mk('line',{x1:X0,y1:Y0,x2:X1+8,y2:Y0,stroke:'#5B6B7F','stroke-width':1.6},stat);
    API.mk('line',{x1:X0,y1:Y0+4,x2:X0,y2:Y1-6,stroke:'#5B6B7F','stroke-width':1.6},stat);
    [0,5,10,15,20].forEach(r=>{ API.mk('line',{x1:X(r),y1:Y0,x2:X(r),y2:Y0+6,stroke:'#5B6B7F','stroke-width':1.5},stat); API.texText(stat,X(r),Y0+26,String(r),{size:18,anchor:'middle'}); });
    API.texText(stat,X1+6,Y0-10,'r\\ (a_0)',{size:18,anchor:'end'});
    const g=API.mk('g',{},svg);
    const yt=[]; for(let i=0;i<6;i++){ const d=document.createElement('div'); d.className='ov'; d.style.cssText='font-size:18px;transform:translate(-100%,-50%)'; fig.appendChild(d); yt.push(d); }
    const sel=()=>ORB.filter((o,i)=>I('o'+(i+1)).checked);
    const val=(o,r)=>{ const R=o.R(r); return st.view==='R'?R:st.view==='R2'?R*R:r*r*R*R; };
    function range(){
      let lo=0,hi=0; sel().forEach(o=>{ for(let i=0;i<=400;i++){ const v=val(o,i*0.05); lo=Math.min(lo,v); hi=Math.max(hi,v); } });
      const nice=v=>{ if(v<=0) return 0; const e=Math.pow(10,Math.floor(Math.log10(v))), m=v/e; return (m<=1?1:m<=2?2:m<=2.5?2.5:m<=5?5:10)*e; };
      hi=nice(hi*1.05)||0.6; lo=lo<0?-nice(-lo*1.1):0; return [lo,hi];
    }
    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      const r=+I('r').value; O('r').textContent=r.toFixed(2);
      root.querySelectorAll('[data-v]').forEach(b=>b.classList.toggle('on',b.dataset.v===st.view));
      const [lo,hi]=range(), Y=v=>Y0-(v-lo)/(hi-lo)*(Y0-Y1);
      if(lo<0) API.mk('line',{x1:X0,y1:Y(0),x2:X1,y2:Y(0),stroke:'#5B6B7F','stroke-width':1.2},g);
      const step=(hi-lo)/5;
      yt.forEach((d,i)=>{ const v=lo+step*i; if(i===0&&lo===0){API.place(d,0,0,false);return;} d.textContent=Math.abs(v)<1e-9?'0':(+v.toPrecision(3)).toString(); API.place(d,X0-6,Y(v),true);
        API.mk('line',{x1:X0,y1:Y(v),x2:X1,y2:Y(v),stroke:'#E2E7EC','stroke-width':1},g); });
      Ov('yl').innerHTML=API.tex(st.view==='R'?'R(r)':st.view==='R2'?'R^2(r)\\ \\text{확률 밀도}':'P(r)=r^2R^2(r)'); API.place(Ov('yl'),X0+120,0,true);
      const rows=[];
      sel().forEach(o=>{
        const pts=[]; for(let i=0;i<=800;i++){ const rr=i*0.025; pts.push(X(rr).toFixed(1)+' '+Y(val(o,rr)).toFixed(1)); }
        API.mk('path',{d:'M'+pts.join(' L'),fill:'none',stroke:o.col,'stroke-width':2.6},g);
        o.nodes.forEach(n=>API.mk('line',{x1:X(n),y1:Y1,x2:X(n),y2:Y0,stroke:'#5B6B7F','stroke-width':1.3,'stroke-dasharray':'4 4'},g));
        if(st.view==='P') API.mk('circle',{cx:X(o.max),cy:Y(val(o,o.max)),r:5,fill:'#E08A2C'},g);
        const R=o.R(r), P=r*r*R*R, cum=o.cum[Math.min(N-1,Math.round(r/DR))];
        API.mk('circle',{cx:X(r),cy:Y(val(o,r)),r:5,fill:'#fff',stroke:o.col,'stroke-width':2.5},g);
        rows.push([o.k,R,P,cum]);
      });
      API.mk('line',{x1:X(r),y1:Y1,x2:X(r),y2:Y0,stroke:'#D7263D','stroke-width':1.5},g);
      O('rd').innerHTML=rows.map(([k,R,P,c])=>`<tr><td>${k}</td><td>${R.toFixed(4)}</td><td>${P.toFixed(4)}</td><td>${c.toFixed(3)}</td></tr>`).join('');
      if(!rows.length){ O('msg').textContent='오비탈을 하나 이상 고르자.'; return; }
      const o=sel()[0], R=o.R(r), c=o.cum[Math.min(N-1,Math.round(r/DR))];
      let m;
      if(o.nodes.some(n=>Math.abs(n-r)<0.03)) m=`${o.k}: 마디 — R = 0이므로 이 거리에서 전자를 발견할 확률은 0이다.`;
      else if(Math.abs(r-o.max)<0.06) m=`${o.k}: 방사 방향 확률 분포의 가장 큰 봉우리 (r ≈ ${o.max.toFixed(2)} a₀).`;
      else if(c>=0.9) m=`${o.k}: 0–r 확률이 ${c.toFixed(3)} — 90 % 경계면 바깥이다.`;
      else m=`${o.k}: R ${R>=0?'> 0 (양)':'< 0 (음)'}, 0–r 확률 ${c.toFixed(3)}. 최댓값·마디를 찾아보자.`;
      O('msg').textContent=m;
    }
    function go(r){ I('r').value=r.toFixed(2); draw(); }
    $('[data-act="max"]').addEventListener('click',()=>{ const o=sel()[0]; if(o) go(o.max); });
    $('[data-act="node"]').addEventListener('click',()=>{ const o=sel()[0]; if(!o) return;
      if(!o.nodes.length){ O('msg').textContent=`${o.k}에는 마디가 없다.`; return; }
      st.node=(st.node+1)%o.nodes.length; go(o.nodes[st.node]); });
    $('[data-act="rec"]').addEventListener('click',()=>{ const r=+I('r').value; const o=sel()[0]; if(!o) return;
      const R=o.R(r); log.push([o.k,r.toFixed(2),R.toFixed(4),(r*r*R*R).toFixed(4),o.cum[Math.min(N-1,Math.round(r/DR))].toFixed(3)]); if(log.length>5) log.shift();
      O('log').innerHTML=log.map(x=>'<tr>'+x.map(c=>`<td>${c}</td>`).join('')+'</tr>').join(''); });
    $('[data-act="reset"]').addEventListener('click',()=>{ st={view:'P',node:-1}; log=[]; O('log').innerHTML=''; I('o1').checked=true; I('o2').checked=false; I('o3').checked=false; go(1.5); });
    root.querySelectorAll('[data-v]').forEach(b=>b.addEventListener('click',()=>{ st.view=b.dataset.v; draw(); }));
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',()=>{ st.node=-1; draw(); }));
    draw(); API.onShow&&API.onShow(draw);
  }
};
})();
