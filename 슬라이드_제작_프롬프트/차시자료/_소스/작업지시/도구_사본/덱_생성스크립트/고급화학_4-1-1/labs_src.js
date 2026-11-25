/* 고급화학 4-1-1 — 실험실
   ac411fescn : 지도서 디지털 탐구 Ⅳ-1 「분광 광도계로 FeSCN²⁺ 생성 반응의 평형 상수 구하기」(성취기준 04-01)
     · Fe³⁺ + SCN⁻ ⇌ FeSCN²⁺, K(25 °C) = 200, ΔH = −25 kJ/mol → K(40 °C) = 123 (반트호프)
     · 용액 n: 0.0020 M Fe(NO₃)₃ 5.00 mL + 0.0020 M KSCN n mL → 10.00 mL : [Fe³⁺]₀ = 1.00×10⁻³ M, [SCN⁻]₀ = 2.0×10⁻⁴·n M
     · 흡광도 A = ε·b·[FeSCN²⁺] (ε = 4700 M⁻¹cm⁻¹, b = 1.00 cm, 447 nm) + N(0, 0.003)
     · 검정선: Fe³⁺ 0.100 M 과량, SCN⁻ 3.0–15.0×10⁻⁵ M 표준 용액 (실제 전환율 95 % — 「모두 반응」 가정의 오차가 남음), 원점을 지나는 최소 제곱 직선
     · 측정 → [FeSCN²⁺] = A/기울기 → 평형 농도 → K = x/((F−x)(S−x)), 다른 비 = x/((F−x)+(S−x)) */
(function(){
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=Math.imul(a^(a>>>15),1|a); t=(t+Math.imul(t^(t>>>7),61|t))^t; return ((t^(t>>>14))>>>0)/4294967296; }; }
function gauss(r){ let u=0,v=0; while(u===0)u=r(); v=r(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||18,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
const EPS=4700, KT=t=>200*Math.exp((-25000/8.314)*(1/298.15-1/(t+273.15)));
const xeq=(K,F,S)=>{ const a=K,b=-(K*(F+S)+1),c=K*F*S; return (-b-Math.sqrt(b*b-4*a*c))/(2*a); };
const red=A=>{ const a=Math.min(1,Math.max(0,A/0.75)); return `rgb(${Math.round(250-71*a)},${Math.round(238-220*a)},${Math.round(214-168*a)})`; };
const sci=(v,d)=>{ if(v===0) return '0'; const e=Math.floor(Math.log10(Math.abs(v))); return (v/Math.pow(10,e)).toFixed(d)+'×10'+String(e).replace('-','⁻').replace(/\d/g,c=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[c]); };
window.DECK_LABS = {
  ac411fescn(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=root.querySelector('.lab-fig svg'), app=root.querySelector('svg.ac411-app');
    let st, rnd;
    function init(){ st={n:3,t:25,slope:null,cal:[],log:[]}; rnd=rng(411); }
    init();
    // 장치
    const a0=API.mk('g',{},app);
    API.mk('rect',{x:6,y:36,width:52,height:40,rx:6,fill:'#FFF6D6',stroke:'#16233D','stroke-width':2},a0); txt(API,a0,32,100,'광원',{size:18});
    const b1=API.mk('line',{x1:58,y1:56,x2:180,y2:56,stroke:'#2F6FD6','stroke-width':7,'stroke-dasharray':'14 8'},a0);
    txt(API,a0,118,40,'447 nm',{size:18,fill:'#5B6B7F'});
    const cuv=API.mk('rect',{x:180,y:24,width:46,height:64,rx:3,stroke:'#7E8B98','stroke-width':2.5},a0); txt(API,a0,203,108,'큐벳',{size:18});
    const b2=API.mk('line',{x1:226,y1:56,x2:300,y2:56,stroke:'#2F6FD6','stroke-dasharray':'14 8'},a0);
    API.mk('rect',{x:300,y:30,width:92,height:52,rx:6,fill:'#E6EAEE',stroke:'#16233D','stroke-width':2},a0); const det=txt(API,a0,346,62,'',{size:18}); txt(API,a0,346,108,'검출기',{size:18});
    const g=API.mk('g',{},svg);
    const L1={x0:62,y0:206,w:230,h:170}, L2={x0:392,y0:206,w:230,h:170};
    function axes(P,xr,yr,xs,ys,fx,fy,xl,yl){
      const X=v=>P.x0+(v-xr[0])/(xr[1]-xr[0])*P.w, Y=v=>P.y0-(v-yr[0])/(yr[1]-yr[0])*P.h;
      xs.forEach(v=>{ API.mk('line',{x1:X(v),y1:P.y0,x2:X(v),y2:P.y0-P.h,stroke:'#E2E7EC','stroke-width':1},g); txt(API,g,X(v),P.y0+22,fx(v),{size:18}); });
      ys.forEach(v=>{ API.mk('line',{x1:P.x0,y1:Y(v),x2:P.x0+P.w,y2:Y(v),stroke:'#E2E7EC','stroke-width':1},g); txt(API,g,P.x0-7,Y(v)+6,fy(v),{size:18,anchor:'end'}); });
      API.mk('line',{x1:P.x0,y1:P.y0,x2:P.x0+P.w+6,y2:P.y0,stroke:'#5B6B7F','stroke-width':2},g); API.mk('line',{x1:P.x0,y1:P.y0,x2:P.x0,y2:P.y0-P.h-6,stroke:'#5B6B7F','stroke-width':2},g);
      txt(API,g,P.x0+P.w+4,P.y0+46,xl,{size:18,anchor:'end',fill:'#5B6B7F'}); txt(API,g,P.x0-4,P.y0-P.h-12,yl,{size:18,anchor:'start',fill:'#5B6B7F'});
      return {X,Y};
    }
    const F0=1e-3, S0=n=>2e-4*n;
    const trueA=(n,t)=>EPS*xeq(KT(t),F0,S0(n));
    const calc=(A,n)=>{ const x=A/st.slope, F=F0-x, S=S0(n)-x; return {x, K:(F>0&&S>0)?x/(F*S):NaN, r:x/(F+S)}; };
    function draw(){
      g.innerHTML='';
      root.querySelectorAll('[data-n]').forEach(b=>b.classList.toggle('on',+b.dataset.n===st.n));
      root.querySelectorAll('[data-t]').forEach(b=>b.classList.toggle('on',+b.dataset.t===st.t));
      const A=trueA(st.n,st.t), Tp=100*Math.pow(10,-A);
      cuv.setAttribute('fill',red(A)); b2.setAttribute('stroke-width',Math.max(1,7*Tp/100).toFixed(2)); det.textContent='A '+A.toFixed(3);
      O('a').textContent=A.toFixed(3);
      O('c0').textContent=`${(S0(st.n)*1e3).toFixed(2)} mM`;
      if(st.slope){ const c=calc(A,st.n); O('x').textContent=(c.x*1e6).toFixed(1)+' μM'; O('k').textContent=Math.round(c.K)+''; }
      else { O('x').textContent='검정선 필요'; O('k').textContent='—'; }
      // 왼쪽: 검정선
      const ax=axes(L1,[0,160],[0,0.8],[0,40,80,120,160],[0,0.4,0.8],v=>String(v),v=>v===0?'0':v.toFixed(1),'표준 용액 농도 (μM)','흡광도');
      if(st.slope){ API.mk('line',{x1:ax.X(0),y1:ax.Y(0),x2:ax.X(160),y2:ax.Y(Math.min(0.8,st.slope*16e-5)),stroke:'#2E9E6A','stroke-width':2.5},g);
        st.cal.forEach(p=>API.mk('circle',{cx:ax.X(p[0]*1e6),cy:ax.Y(p[1]),r:5,fill:'#FFFFFF',stroke:'#16233D','stroke-width':2},g));
        const cx=A/st.slope*1e6; API.mk('line',{x1:L1.x0,y1:ax.Y(A),x2:ax.X(cx),y2:ax.Y(A),stroke:'#D7263D','stroke-width':1.5,'stroke-dasharray':'4 4'},g);
        API.mk('line',{x1:ax.X(cx),y1:ax.Y(A),x2:ax.X(cx),y2:L1.y0,stroke:'#D7263D','stroke-width':1.5,'stroke-dasharray':'4 4'},g);
        API.mk('path',{d:`M${ax.X(cx)} ${ax.Y(A)-7} l7 7 l-7 7 l-7 -7 Z`,fill:'#D7263D'},g); }
      // 오른쪽: K
      const bx=axes(L2,[0.5,5.5],[0,300],[1,2,3,4,5],[0,100,200,300],v=>String(v),v=>String(v),'용액','K');
      [25,40].forEach(t=>{ const rs=st.log.filter(r=>r.t===t); if(!rs.length) return; const col=t===25?'#16233D':'#D7263D';
        const m=rs.reduce((a,r)=>a+r.K,0)/rs.length; API.mk('line',{x1:L2.x0,y1:bx.Y(m),x2:L2.x0+L2.w,y2:bx.Y(m),stroke:col,'stroke-width':1.5,'stroke-dasharray':'6 4'},g);
        rs.forEach(r=>API.mk('circle',{cx:bx.X(r.n),cy:bx.Y(Math.min(300,r.K)),r:6,fill:t===25?'#FFFFFF':col,stroke:col,'stroke-width':2},g));
        txt(API,g,L2.x0+L2.w,bx.Y(m)+(t===25?-8:20),`${t} °C 평균 ${Math.round(m)}`,{size:18,anchor:'end',fill:col}); });
      // 해석
      let msg;
      if(!st.slope) msg='먼저 「검정선 만들기」로 표준 용액 다섯 개의 흡광도를 재어 검정선을 그리자. 지금은 흡광도만 읽힌다.';
      else if(!st.log.length) msg=`검정선: 흡광도 = ${Math.round(st.slope)} × [FeSCN²⁺]. 용액을 고르고 「측정·기록」을 누르자. 용액 ${st.n}의 붉은색이 진할수록 흡광도가 크다.`;
      else { const rs=st.log.filter(r=>r.t===st.t);
        if(rs.length<2) msg=`${st.t} °C에서 용액을 하나 더 측정하자. 처음 농도가 다른 용액들의 K를 비교한다.`;
        else { const ks=rs.map(r=>r.K), m=ks.reduce((a,b)=>a+b,0)/ks.length, sd=Math.sqrt(ks.reduce((a,b)=>a+(b-m)*(b-m),0)/(ks.length-1)), rr=rs.map(r=>r.r);
          msg=`${st.t} °C ${rs.length}개: K 평균 ${Math.round(m)} (상대 표준편차 ${(100*sd/m).toFixed(1)} %) — 거의 일정. 다른 비는 ${Math.min(...rr).toFixed(3)}–${Math.max(...rr).toFixed(3)}로 ${(Math.max(...rr)/Math.min(...rr)).toFixed(1)}배 달라진다.`; }
        const k25=st.log.filter(r=>r.t===25), k40=st.log.filter(r=>r.t===40);
        if(k25.length&&k40.length){ const m25=k25.reduce((a,r)=>a+r.K,0)/k25.length, m40=k40.reduce((a,r)=>a+r.K,0)/k40.length; msg+=` 40 °C에서 K가 더 작다(${Math.round(m40)} < ${Math.round(m25)}) → 가열하면 역반응 쪽 → 정반응은 발열.`; } }
      O('msg').textContent=msg;
      const L=st.log; O('log').innerHTML=L.slice(-5).map((r,i)=>`<tr><td>${L.length-Math.min(5,L.length)+i+1}</td><td>${r.n}</td><td>${r.t} °C</td><td>${r.A.toFixed(3)}</td><td>${(r.x*1e6).toFixed(1)}</td><td>${Math.round(r.K)}</td><td>${r.r.toFixed(3)}</td></tr>`).join('');
    }
    root.querySelectorAll('[data-n]').forEach(b=>b.addEventListener('click',()=>{ st.n=+b.dataset.n; draw(); }));
    root.querySelectorAll('[data-t]').forEach(b=>b.addEventListener('click',()=>{ st.t=+b.dataset.t; draw(); }));
    root.querySelector('[data-act="cal"]').addEventListener('click',()=>{ const fr=xeq(200,0.100,1e-5)/1e-5; st.cal=[3,6,9,12,15].map(c=>[c*1e-5,Math.round((EPS*fr*c*1e-5+0.002*gauss(rnd))*1000)/1000]);
      let sxy=0,sxx=0; st.cal.forEach(p=>{ sxy+=p[0]*p[1]; sxx+=p[0]*p[0]; }); st.slope=sxy/sxx; draw(); });
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ if(!st.slope){ O('msg').textContent='검정선이 없으면 흡광도를 농도로 바꿀 수 없다. 「검정선 만들기」를 먼저 누르자.'; return; }
      const A=Math.round((trueA(st.n,st.t)+0.003*gauss(rnd))*1000)/1000, c=calc(A,st.n); st.log.push({n:st.n,t:st.t,A,x:c.x,K:c.K,r:c.r}); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ init(); draw(); });
    draw();
    let off=0; API.loop(root,(dt)=>{ off=(off-dt*40)%22; b1.setAttribute('stroke-dashoffset',off.toFixed(1)); b2.setAttribute('stroke-dashoffset',off.toFixed(1)); });
  }
};
})();
