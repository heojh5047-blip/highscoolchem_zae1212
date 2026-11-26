/* 고급화학 4-5-1 — 실험실 ac451cat : 교과서 257쪽 탐구 활동 「촉매의 사용 분야와 용도 조사 및 촉매 반응 실험」(고화-탐39)
   과산화 수소수(1·2·3 %, 5 mL)의 분해 2H2O2 → 2H2O + O2 를 촉매(없음·KI·MnO2·카탈레이스)·온도(15–55 °C)를 바꾸어 측정한다.
   계산 모형(calc.py와 같음): H2O2에 대해 1차 반응, V(t) = Vmax(1 − e^(−kt)), Vmax = (p×10/34.01 M)×0.005 L ÷ 2 × 24.5 L/mol (25 °C, 1 atm 환산)
   k(T) = k25·exp(−Ea/R·(1/T − 1/298.15)) — Ea: 없음 76(교과서), KI 57, MnO2 50, 카탈레이스 23 kJ/mol(모형 값),
   k25: 2.0×10⁻⁷, 0.010, 0.025, 0.050 s⁻¹. 카탈레이스는 단백질 변성 인자 1/(1+e^((t−45)/3)) (25 °C를 1로)를 곱한다.
   「측정 시작」 → 180 s를 약 5 s에 보여 주며 곡선이 그려지고(API.loop), 끝나면 기록 표에 30 s·180 s 부피(고정 시드 ±1.5 % 오차)와 반감기가 쌓인다.
   직전 기록과 한 조건만 다르면 해석 문장에서 비교한다. 오른쪽: 촉매 없음(ink) / 고른 촉매(field 점선) 반응 에너지 도표. */
(function(){
const R=8.314e-3;
const CAT={none:{nm:'없음',html:'없음',Ea:76,k25:2.0e-7},KI:{nm:'KI',html:'KI',Ea:57,k25:0.010},MnO2:{nm:'MnO2',html:'MnO<sub>2</sub>',Ea:50,k25:0.025},cat:{nm:'카탈레이스',html:'카탈레이스',Ea:23,k25:0.050}};
const den=t=>1/(1+Math.exp((t-45)/3));
function kOf(c,t){ const T=t+273.15; let k=CAT[c].k25*Math.exp(-CAT[c].Ea/R*(1/T-1/298.15)); if(c==='cat') k*=den(t)/den(25); return k; }
const Vmax=p=>p*10/34.01*0.005/2*24.5*1000;
const fx=(v,d=1)=>v.toFixed(d);
function xr(v){ if(v>=1000||v<0.01){ const e=Math.floor(Math.log10(v)); return (v/Math.pow(10,e)).toFixed(1)+'×10<sup>'+String(e).replace('-','−')+'</sup>'; } return v<1?v.toFixed(2):v.toPrecision(3); }
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||17,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
window.DECK_LABS = {
  ac451cat(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('.lab-fig svg'), app=$('svg.ac451-app'), C=API.COL, mk=(t,a,p)=>API.mk(t,a,p);
    const g=mk('g',{},svg), ga=mk('g',{},app);
    const GX=62, GY=250, GW=330, GH=205, TMAX=180, VMAX=60;
    const EX=455, EY=250, EW=175, EH=190, ELO=-110, EHI=90;
    const X=t=>GX+t/TMAX*GW, Y=v=>GY-Math.min(v,VMAX)/VMAX*GH;
    const RUNCOL=['#1F6FD1','#7B4FC8','#C2410C','#0E7490'];
    let st, bubbles=[];
    function init(){ st={c:'none',p:3,run:false,t:0,cur:null,runs:[],log:[],n:0,
      msg:'촉매·농도·온도를 고르고 「측정 시작」을 누르세요. 한 번에 <b>한 조건만</b> 바꾸어 기록을 쌓으면 해석 문장이 직전 기록과 비교해 줍니다.'};
      I('t').value=25; sel(); draw(); }
    function sel(){ root.querySelectorAll('[data-c]').forEach(b=>b.classList.toggle('on',b.dataset.c===st.c));
      root.querySelectorAll('[data-p]').forEach(b=>b.classList.toggle('on',+b.dataset.p===st.p)); }
    const noise=(n,s)=>1+0.015*Math.sin((n*7+s/30)*12.9898+1.7);
    function V(run,t){ return run.Vm*(1-Math.exp(-run.k*t)); }
    function start(){ const t=+I('t').value; st.n++; st.cur={n:st.n,c:st.c,p:st.p,T:t,k:kOf(st.c,t),Vm:Vmax(st.p),col:RUNCOL[(st.n-1)%4]}; st.t=0; st.run=true; st.msg='측정 중… 30 s마다 부피를 읽어 점을 찍습니다.'; draw(); }
    function finish(){ const r=st.cur; if(!r) return; st.run=false; st.t=TMAX;
      r.v30=V(r,30)*noise(r.n,30); r.v180=V(r,180)*noise(r.n,180); r.half=Math.log(2)/r.k;
      st.runs.push(r); if(st.runs.length>4) st.runs.shift(); st.log.push(r);
      st.msg=interp(r); st.cur=null; draw(); }
    function hs(h){ return h>1e4?'매우 긺':fx(h,0)+' s'; }
    function interp(r){ const nm=CAT[r.c].html; let m='';
      if(r.c==='none') m=`촉매가 없으면 180 s 동안 산소가 거의 생기지 않는다(E<sub>a</sub> ${CAT.none.Ea} kJ/mol). `;
      else m=`${nm}: 처음 30 s 평균 ${fx(r.v30/30,2)} mL/s, 반감기 ${hs(r.half)}, 180 s에 ${fx(r.v180)} mL (최대 ${fx(r.Vm)} mL). `;
      const q=st.log[st.log.length-2];
      if(q){ const sc=q.c===r.c, sp=q.p===r.p, sT=q.T===r.T;
        if(!sc&&sp&&sT) m+=`촉매 ${CAT[q.c].html} → ${nm}: 속도 상수 ${xr(r.k/q.k)}배. 최종 부피(${fx(r.Vm)} mL)는 촉매와 관계없이 같다.`;
        else if(sc&&sp&&!sT){ m+=`${q.T} → ${r.T} °C: 속도 상수 ${xr(r.k/q.k)}배.`; if(r.c==='cat'&&r.T>q.T&&r.k<q.k) m+=' 효소(단백질)가 높은 온도에서 변해 오히려 느려졌다.'; else if(r.k>q.k) m+=' 온도가 높을수록 E<sub>a</sub> 이상의 분자가 많아 빨라진다.'; }
        else if(sc&&!sp&&sT) m+=`농도 ${q.p} → ${r.p} %: 처음 속도 ${(r.v30/q.v30).toFixed(2)}배, 최종 부피 ${(r.Vm/q.Vm).toFixed(1)}배, 반감기는 같다(1차 반응).`;
        else if(sc&&sp&&sT) m+='직전과 같은 조건 — 되풀이 측정값이 거의 같다.';
        else m+='직전과 두 가지 이상 조건이 다르다 — 한 조건만 바꾸어 비교하자.'; }
      return m; }
    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      const t=+I('t').value; O('t').textContent=t+' °C';
      // 그래프 축
      for(let v=0;v<=60;v+=20){ mk('line',{x1:GX,y1:Y(v),x2:GX+GW,y2:Y(v),stroke:'#E2E7EC','stroke-width':1},g); txt(API,g,GX-8,Y(v)+6,String(v),{anchor:'end',fill:C.muted}); }
      for(let s=0;s<=180;s+=30){ mk('line',{x1:X(s),y1:GY,x2:X(s),y2:GY+5,stroke:C.muted,'stroke-width':1.5},g); txt(API,g,X(s),GY+24,String(s),{fill:C.muted}); }
      API.arrow(g,GX,GY,GX+GW+14,GY,C.muted,2); API.arrow(g,GX,GY,GX,GY-GH-14,C.muted,2);
      API.place(Ov('vy'),GX+46,GY-GH-26,true); API.place(Ov('tx'),GX+GW+4,GY+38,true);
      const curve=(r,tEnd,col,dash,w)=>{ let d=''; for(let j=0;j<=90;j++){ const s=tEnd*j/90; d+=(d?' L':'M')+X(s).toFixed(1)+' '+Y(V(r,s)).toFixed(1); } mk('path',{d,fill:'none',stroke:col,'stroke-width':w||3,'stroke-dasharray':dash||'none','stroke-linejoin':'round'},g); };
      const pts=(r,tEnd,col)=>{ for(let s=30;s<=tEnd+0.01;s+=30) mk('circle',{cx:X(s),cy:Y(V(r,s)*noise(r.n,s)),r:5,fill:col,stroke:'#fff','stroke-width':1.5},g); };
      st.runs.forEach((r,i)=>{ const last=(i===st.runs.length-1)&&!st.cur; curve(r,TMAX,r.col,null,last?3.5:2.2); pts(r,TMAX,r.col); if(last) txt(API,g,X(TMAX)+4,Y(V(r,TMAX))+6,r.n+'회',{anchor:'start',size:17,fill:r.col}); });
      if(st.cur){ curve(st.cur,st.t,st.cur.col,null,3.5); pts(st.cur,Math.floor(st.t/30)*30,st.cur.col); }
      // 에너지 도표
      const ex=s=>EX+s*EW, ey=E=>EY-(E-ELO)/(EHI-ELO)*EH;
      API.arrow(g,EX,EY,EX,EY-EH-10,C.muted,2); API.arrow(g,EX,EY,EX+EW+10,EY,C.muted,2);
      txt(API,g,EX+6,EY-EH-14,'에너지',{anchor:'start'}); txt(API,g,EX+EW+8,EY+24,'반응 진행 경로',{anchor:'end'});
      const path=(N,col,dash)=>{ let d=''; for(let i=0;i<N.length-1;i++){ const [t1,e1]=N[i],[t2,e2]=N[i+1]; for(let j=0;j<=24;j++){ const u=j/24; d+=(d?' L':'M')+ex(t1+(t2-t1)*u).toFixed(1)+' '+ey(e1+(e2-e1)*(1-Math.cos(Math.PI*u))/2).toFixed(1); } } mk('path',{d,fill:'none',stroke:col,'stroke-width':3,'stroke-dasharray':dash||'none'},g); };
      path([[0,0],[.14,0],[.45,76],[.8,-95],[1,-95]],C.ink);
      const E1=CAT[st.c].Ea;
      if(st.c!=='none'){ const im=Math.round(E1*.35), t2=Math.round(E1*.75); path([[0,0],[.1,0],[.3,E1],[.46,im],[.6,t2],[.84,-95],[1,-95]],C.field,'6 5');
        mk('circle',{cx:ex(.46),cy:ey(im),r:4.5,fill:C.equi},g); }
      mk('line',{x1:ex(.05),y1:ey(0),x2:ex(.5),y2:ey(0),stroke:C.muted,'stroke-width':1.3,'stroke-dasharray':'4 4'},g);
      API.arrow(g,ex(.14),ey(0),ex(.14),ey(76),C.equi,2.2);
      API.place(Ov('ea0'),ex(.14)-26,ey(40),true); Ov('ea0').innerHTML='E<sub>a</sub> 76';
      if(st.c!=='none'){ API.arrow(g,ex(.3),ey(0),ex(.3),ey(E1),C.field,2.2); API.place(Ov('ea1'),ex(.3)+30,ey(E1/2)+12,true); Ov('ea1').innerHTML=`${E1}`; }
      else API.place(Ov('ea1'),0,0,false);
      txt(API,g,ex(.03),ey(-80),'ΔH 같음',{anchor:'start',size:17,fill:C.muted});
      // 장치 그림 (주사기 피스톤 = 현재 부피)
      while(ga.firstChild) ga.removeChild(ga.firstChild);
      const vnow=st.cur?V(st.cur,st.t):(st.runs.length?V(st.runs[st.runs.length-1],TMAX):0);
      mk('path',{d:'M40 14 L40 40 L14 92 L96 92 L70 40 L70 14',fill:'none',stroke:'#7E8B98','stroke-width':3},ga);
      mk('path',{d:'M26 68 L84 68 L95 90 L15 90 Z',fill:'#DDEEF8',stroke:'none'},ga);
      if(st.c!=='none') mk('rect',{x:40,y:84,width:30,height:6,rx:2,fill:st.c==='cat'?'#E8D9A8':'#3A2E25'},ga);
      mk('path',{d:'M55 14 L55 6 L170 6 L170 30',fill:'none',stroke:'#16233D','stroke-width':3},ga);
      mk('rect',{x:160,y:30,width:250,height:40,rx:6,fill:'#F7F8FA',stroke:'#7E8B98','stroke-width':3},ga);
      const px=172+Math.min(vnow,60)/60*220;
      mk('rect',{x:172,y:34,width:px-172,height:32,fill:'#E6F2EA'},ga);
      mk('rect',{x:px,y:33,width:8,height:34,fill:'#7E8B98'},ga); mk('line',{x1:px+8,y1:50,x2:418,y2:50,stroke:'#16233D','stroke-width':4},ga);
      for(let v=0;v<=60;v+=20){ mk('line',{x1:172+v/60*220,y1:70,x2:172+v/60*220,y2:78,stroke:C.muted,'stroke-width':1.5},ga); txt(API,ga,172+v/60*220,96,String(v),{size:17,fill:C.muted}); }
      bubbles.forEach(b=>mk('circle',{cx:b.x,cy:b.y,r:b.r,fill:'#fff',stroke:'#9FC3DD','stroke-width':1.5},ga));
      O('now').innerHTML=st.cur?`측정 중 ${st.cur.n}회: t = ${fx(st.t,0)} s, V = ${fx(V(st.cur,st.t))} mL`:(st.runs.length?`마지막 측정(${st.runs[st.runs.length-1].n}회): 180 s에 ${fx(st.runs[st.runs.length-1].v180)} mL`:'아직 측정하지 않았습니다.');
      O('msg').innerHTML=st.msg;
      const tb=O('log'); tb.innerHTML='';
      st.log.slice(-4).forEach(r=>{ const e=document.createElement('tr'); e.innerHTML=`<td style="color:${r.col}">${r.n}</td><td>${CAT[r.c].html}</td><td>${r.T} °C</td><td>${r.p} %</td><td>${fx(r.v30)} mL</td><td>${fx(r.v180)} mL</td><td>${hs(r.half)}</td>`; tb.appendChild(e); });
    }
    function cancel(){ if(st.run){ st.run=false; st.cur=null; st.msg='조건을 바꾸어 측정을 멈췄습니다. 다시 「측정 시작」을 누르세요.'; } }
    root.querySelectorAll('[data-c]').forEach(b=>b.addEventListener('click',()=>{ cancel(); st.c=b.dataset.c; sel(); draw(); }));
    root.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{ cancel(); st.p=+b.dataset.p; sel(); draw(); }));
    I('t').addEventListener('input',()=>{ cancel(); draw(); });
    $('[data-act="run"]').addEventListener('click',start);
    $('[data-act="skip"]').addEventListener('click',()=>{ if(!st.run) start(); finish(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ bubbles=[]; init(); });
    API.loop(root,(dt)=>{
      if(st.run){ st.t=Math.min(TMAX,st.t+dt*36); const rate=st.cur.k*st.cur.Vm*Math.exp(-st.cur.k*st.t);
        if(Math.random()<Math.min(.9,rate*0.6)) bubbles.push({x:26+Math.random()*58,y:88,r:2+Math.random()*3});
        if(st.t>=TMAX) finish(); }
      if(bubbles.length||st.run){ bubbles.forEach(b=>b.y-=dt*60); bubbles=bubbles.filter(b=>b.y>66); draw(); }
    });
    init(); API.ready(()=>draw());
  }
};
})();
