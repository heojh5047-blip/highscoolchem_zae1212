/* 고급화학 4-4-1 — 실험실 ac441diag : 교과서 247쪽 탐구 활동 「화학 반응에 관한 반응 에너지 도표 작성」(고화-탐37)
   반응 고르기 (가) NO2 + CO → NO + CO2 (Ea,f 132, ΔH −226, 그림 Ⅳ-30) / (나) O3 + O → 2O2 (Ea,f 19, ΔH −392, 연습 문제 2)
   / (다) (가)의 역반응 NO + CO2 → NO2 + CO (Ea,f 358, ΔH +226) / (라) 가상의 두 단계 반응(1단계 Ea 90, 중간체 +30, 2단계 Ea 30, ΔH −50).
   반응물 에너지 = 0(기준). 슬라이더로 활성화 착물·(중간체·둘째 활성화 착물)·생성물 에너지를 놓으면 곡선(코사인 보간)이 바뀌고
   Ea,f = (가장 높은 활성화 착물) − 반응물, Ea,r = (가장 높은 활성화 착물) − 생성물, ΔH = 생성물 − 반응물을 읽는다.
   「발열」·「흡열」 판정 → 자료와 비교해 기록 표에 쌓임. 아래: 온도 T, T+ΔT의 맥스웰–볼츠만 에너지 분포
   f(E) = 2/√π·(RT)^(-3/2)·√E·e^(-E/RT) 위에 Ea,f 선, Ea 이상 분율 F = erfc(√x) + 2√(x/π)e^(-x) (x = Ea/RT)와 그 비. */
(function(){
const R=8.314e-3; // kJ/(mol·K)
function erfc(x){ const t=1/(1+0.5*x); const y=t*Math.exp(-x*x-1.26551223+t*(1.00002368+t*(0.37409196+t*(0.09678418+t*(-0.18628806+t*(0.27886807+t*(-1.13520398+t*(1.48851587+t*(-0.82215223+t*0.17087277))))))))); return y; }
function frac(Ea,T){ if(Ea<=0) return 1; const x=Ea/(R*T); return erfc(Math.sqrt(x))+2*Math.sqrt(x/Math.PI)*Math.exp(-x); }
function lfrac(Ea,T){ const x=Ea/(R*T); if(x<600) return Math.log10(frac(Ea,T)); // 아주 작을 때: 로그로 근사(점근식)
  return (-x+Math.log(2*Math.sqrt(x/Math.PI)*(1+1/(2*x))))/Math.LN10; }
function fE(E,T){ const RT=R*T; return 2/Math.sqrt(Math.PI)*Math.pow(RT,-1.5)*Math.sqrt(Math.max(E,0))*Math.exp(-E/RT); }
function sciL(l){ // log10 값 → 지수 표기 HTML
  if(l>-2) return Math.pow(10,l).toPrecision(2); const e=Math.floor(l); const m=Math.pow(10,l-e); return m.toFixed(1)+'×10<sup>'+String(e).replace('-','−')+'</sup>'; }
const sgn=v=>(v>0?'+':v<0?'−':'')+Math.abs(v);
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||18,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
const RX={
  a:{nm:'(가)',lo:-300,hi:200,two:false,ts:132,p:-226,r:'\\ce{NO2 + CO}',q:'\\ce{NO + CO2}',start:{ts:60,p:0},
     eq:'\\ce{NO2 + CO -> NO + CO2}',given:'E<sub>a,f</sub> 132, ΔH −226 kJ/mol (그림 Ⅳ-30)'},
  b:{nm:'(나)',lo:-450,hi:100,two:false,ts:19,p:-392,r:'\\ce{O3 + O}',q:'\\ce{2O2}',start:{ts:60,p:-100},
     eq:'\\ce{O3 + O -> 2O2}',given:'E<sub>a,f</sub> 19, ΔH −392 kJ/mol (연습 문제 2)'},
  c:{nm:'(다)',lo:-80,hi:420,two:false,ts:358,p:226,r:'\\ce{NO + CO2}',q:'\\ce{NO2 + CO}',start:{ts:150,p:0},
     eq:'\\ce{NO + CO2 -> NO2 + CO}',given:'(가)의 역반응: E<sub>a,f</sub> 358, ΔH +226 kJ/mol'},
  d:{nm:'(라)',lo:-120,hi:160,two:true,ts:90,im:30,ts2:60,p:-50,r:'\\mathrm{A}',q:'\\mathrm{C}',start:{ts:40,im:0,ts2:40,p:0},
     eq:'\\mathrm{A} \\ce{->} \\mathrm{C}',given:'두 단계(가상): 1단계 E<sub>a</sub> 90, 중간체 +30, 2단계 E<sub>a</sub> 30, ΔH −50 kJ/mol'}
};
window.DECK_LABS = {
  ac441diag(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('.lab-fig svg'), C=API.COL, mk=(t,a,p)=>API.mk(t,a,p);
    const g=mk('g',{},svg);
    const DX=70, DY=222, DW=300, DH=180;      // 반응 에너지 도표
    const MX=455, MY=222, MW=190, MH=170;     // 에너지 분포
    let st;
    function init(){ st={rx:'a',run:0,log:[],msg:'반응을 고르고, 자료에 맞게 활성화 착물과 생성물의 에너지를 놓은 뒤 「발열」 또는 「흡열」로 판정하세요.'}; setRx('a'); }
    function setRx(k){ st.rx=k; const R_=RX[k];
      ['ts','p','im','ts2'].forEach(n=>{ const e=I(n); e.min=R_.lo+10; e.max=R_.hi-10; });
      I('ts').min=0; Object.entries(R_.start).forEach(([n,v])=>I(n).value=v);
      if(!R_.two){ I('im').value=0; I('ts2').value=0; }
      root.querySelectorAll('[data-rx]').forEach(b=>b.classList.toggle('on',b.dataset.rx===k));
      O('two').classList.toggle('ac441-off',!R_.two);
      draw(); }
    function lv(){ const R_=RX[st.rx]; const v={ts:+I('ts').value,p:+I('p').value,im:+I('im').value,ts2:+I('ts2').value};
      if(R_.two){ v.im=Math.min(v.im,v.ts-5,v.ts2-5); }
      const top=R_.two?Math.max(v.ts,v.ts2):v.ts; v.top=Math.max(top,0,v.p);
      v.eaf=v.top; v.ear=v.top-v.p; v.dh=v.p; return v; }
    function nodes(v){ const R_=RX[st.rx];
      return R_.two? [[0,0],[.08,0],[.28,v.ts],[.5,v.im],[.7,v.ts2],[.9,v.p],[1,v.p]] : [[0,0],[.16,0],[.47,Math.max(v.ts,0,v.p)],[.8,v.p],[1,v.p]]; }
    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      const R_=RX[st.rx], v=lv(); O('given').innerHTML=API.tex(R_.eq)+' — '+R_.given;
      ['ts','p','im','ts2'].forEach(n=>O(n).textContent=sgn(+I(n).value));
      const X=t=>DX+t*DW, Y=E=>DY-(E-R_.lo)/(R_.hi-R_.lo)*DH;
      // 축
      API.arrow(g,DX,DY,DX,DY-DH-18,C.muted,2); API.arrow(g,DX,DY,DX+DW+16,DY,C.muted,2);
      const step=(R_.hi-R_.lo)>400?100:50;
      for(let E=Math.ceil(R_.lo/step)*step;E<=R_.hi;E+=step){ mk('line',{x1:DX-5,y1:Y(E),x2:DX,y2:Y(E),stroke:C.muted,'stroke-width':1.5},g); txt(API,g,DX-8,Y(E)+6,String(E).replace('-','−'),{size:17,anchor:'end',fill:C.muted}); }
      txt(API,g,DX+4,DY-DH-24,'에너지 [kJ/mol]',{size:17,anchor:'start'}); txt(API,g,DX+DW+14,DY+26,'반응 진행 경로',{size:17,anchor:'end'});
      // 곡선
      const N=nodes(v); let d='';
      for(let i=0;i<N.length-1;i++){ const [t1,e1]=N[i],[t2,e2]=N[i+1]; for(let j=0;j<=30;j++){ const u=j/30; d+=(d?' L':'M')+X(t1+(t2-t1)*u).toFixed(1)+' '+Y(e1+(e2-e1)*(1-Math.cos(Math.PI*u))/2).toFixed(1); } }
      mk('path',{d,fill:'none',stroke:C.ink,'stroke-width':3.5,'stroke-linejoin':'round'},g);
      // 기준선·치수선
      const tTop=R_.two?(v.ts>=v.ts2?.28:.7):.47;
      mk('line',{x1:X(0),y1:Y(0),x2:X(.98),y2:Y(0),stroke:C.muted,'stroke-width':1.4,'stroke-dasharray':'5 4'},g);
      mk('line',{x1:X(.1),y1:Y(v.top),x2:X(.95),y2:Y(v.top),stroke:C.muted,'stroke-width':1.4,'stroke-dasharray':'5 4'},g);
      const xa=R_.two?.16:.3, xr=R_.two?.82:.66;
      if(v.eaf>2) API.arrow(g,X(xa),Y(0),X(xa),Y(v.top),C.equi,2.5);
      if(v.ear>2) API.arrow(g,X(xr),Y(v.p),X(xr),Y(v.top),C.equi,2.5);
      if(Math.abs(v.dh)>2) API.arrow(g,X(.96),Y(0),X(.96),Y(v.p),C.ink,2.5);
      API.place(Ov('ea'),X(xa)-34,(Y(0)+Y(v.top))/2,v.eaf>12); API.place(Ov('er'),X(xr)+34,(Y(v.p)+Y(v.top))/2,v.ear>12); API.place(Ov('dh'),X(.96)-28,(Y(0)+Y(v.p))/2,Math.abs(v.dh)>12);
      Ov('r').innerHTML=API.tex(R_.r); Ov('q').innerHTML=API.tex(R_.q);
      API.place(Ov('r'),X(.15),Y(0)+16,true); API.place(Ov('q'),X(.9),Y(v.p)+(v.p>0?-16:16),true);
      if(R_.two){ mk('circle',{cx:X(.5),cy:Y(v.im),r:5,fill:C.equi},g); txt(API,g,X(.5),Y(v.im)+28,'중간체',{size:17,fill:C.equi}); }
      txt(API,g,X(tTop),Y(v.top)-10,'‡',{size:20,fill:C.muted});
      // 읽은 값
      O('eaf').textContent=v.eaf; O('ear').textContent=v.ear; O('dh').textContent=sgn(v.dh);
      // 에너지 분포
      const T1=+I('T').value, T2=T1+(+I('dT').value); O('T').textContent=T1+' K'; O('dT').textContent='+'+I('dT').value+' K → '+T2+' K';
      const Ea=Math.max(v.eaf,1); const xmax=Math.max(Ea*1.2,14*R*T2); const ymax=fE(R*T1/2,T1)*1.15;
      const PX=E=>MX+E/xmax*MW, PY=y=>MY-Math.min(y/ymax,1.05)*MH;
      API.arrow(g,MX,MY,MX+MW+12,MY,C.muted,2); API.arrow(g,MX,MY,MX,MY-MH-10,C.muted,2);
      txt(API,g,MX-8,MY-MH+16,'분자',{size:17,anchor:'end'}); txt(API,g,MX-8,MY-MH+38,'분율',{size:17,anchor:'end'}); txt(API,g,MX+MW+10,MY+26,'에너지 [kJ/mol]',{size:17,anchor:'end'});
      const l1=lfrac(Ea,T1), l2=lfrac(Ea,T2); const f2=fE(Ea,T2); let n=0;
      if(f2<0.12*ymax){ n=Math.ceil(Math.log10(0.45*ymax/Math.max(f2,1e-300))); if(!isFinite(n)) n=0; }
      const fl2=Math.log10(Math.max(f2,1e-300));
      // 꼬리 확대(10^n배) — 아주 작은 값은 로그로 계산
      const tail=(T,col,op)=>{ let dd=`M${PX(Ea).toFixed(1)} ${MY}`; const RT=R*T; for(let j=0;j<=40;j++){ const E=Ea+(xmax-Ea)*j/40; const lf=Math.log10(2/Math.sqrt(Math.PI))-1.5*Math.log10(RT)+0.5*Math.log10(E)-E/RT/Math.LN10+n; const y=Math.pow(10,Math.min(lf,5)); dd+=` L${PX(E).toFixed(1)} ${PY(y).toFixed(1)}`; } dd+=` L${PX(xmax).toFixed(1)} ${MY} Z`; mk('path',{d:dd,fill:col,'fill-opacity':op,stroke:'none'},g); };
      tail(T2,'#FFE45C',.6); tail(T1,C.minus,.25);
      const curve=(T,col)=>{ let dd=''; for(let j=0;j<=120;j++){ const E=xmax*j/120; dd+=(dd?' L':'M')+PX(E).toFixed(1)+' '+PY(fE(E,T)).toFixed(1); } mk('path',{d:dd,fill:'none',stroke:col,'stroke-width':3},g); };
      curve(T1,C.minus); curve(T2,C.plus);
      mk('line',{x1:PX(Ea),y1:MY,x2:PX(Ea),y2:MY-MH,stroke:C.equi,'stroke-width':2.5},g);
      API.place(Ov('eam'),PX(Ea),MY-MH-2,true);
      Ov('mag').innerHTML=n>0?`음영: E<sub>a</sub> 이상 ×10<sup>${n}</sup> 확대`:'음영: E<sub>a</sub> 이상 부분';
      API.place(Ov('mag'),MX+MW/2+6,14,true);
      O('fr').innerHTML=`E<sub>a</sub> 이상 분율 — ${T1} K: ${sciL(l1)}, ${T2} K: ${sciL(l2)} → <b>${Math.pow(10,l2-l1).toFixed(2)}배</b>`;
      O('msg').innerHTML=st.msg;
      const tb=O('log'); tb.innerHTML='';
      st.log.slice(-3).forEach(r=>{ const e=document.createElement('tr'); e.innerHTML=`<td>${r.run}</td><td>${r.nm}</td><td>${r.eaf}</td><td>${r.ear}</td><td>${sgn(r.dh)}</td><td style="color:${r.ok?C.field:C.plus}">${r.j} ${r.ok?'○':'×'}</td><td style="color:${r.mt?C.field:C.plus}">${r.mt?'일치':'다름'}</td><td>${r.ratio}</td>`; tb.appendChild(e); });
    }
    function judge(j){ const R_=RX[st.rx], v=lv(); st.run++;
      const truth=v.dh<0?'발열':(v.dh>0?'흡열':'—'); const ok=(j===truth);
      const diff=[]; const near=(a,b)=>Math.abs(a-b)<=3;
      if(!near(+I('ts').value,R_.ts)) diff.push(`${R_.two?'첫째 ':''}활성화 착물 → ${R_.ts}`);
      if(R_.two){ if(!near(v.im,R_.im)) diff.push(`중간체 → +${R_.im}`); if(!near(+I('ts2').value,R_.ts2)) diff.push(`둘째 활성화 착물 → ${R_.ts2}`); }
      if(!near(v.p,R_.p)) diff.push(`생성물 → ${sgn(R_.p)}`);
      const mt=diff.length===0; const T1=+I('T').value, T2=T1+(+I('dT').value);
      const ratio=Math.pow(10,lfrac(Math.max(v.eaf,1),T2)-lfrac(Math.max(v.eaf,1),T1)).toFixed(2)+'배';
      st.log.push({run:st.run,nm:R_.nm,eaf:v.eaf,ear:v.ear,dh:v.dh,j,ok,mt,ratio});
      let m='';
      if(v.dh===0) m='ΔH = 0이면 흡열도 발열도 아닙니다 — 생성물의 에너지를 먼저 옮기세요. ';
      else if(!ok) m=`ΔH = 생성물 − 반응물 = ${sgn(v.dh)} kJ/mol이므로 이 도표는 <b>${truth} 반응</b>입니다. `;
      else m=`판정 맞음: ΔH = ${sgn(v.dh)} kJ/mol → ${truth} 반응. `;
      if(mt){ m+=`자료와 일치 — E<sub>a,r</sub> = E<sub>a,f</sub> − ΔH = ${v.eaf} − (${sgn(v.dh)}) = ${v.ear} kJ/mol.`;
        if(R_.two) m+=' 골짜기(중간체)가 하나 → 두 단계 반응, 전체 E<sub>a</sub>는 가장 높은 활성화 착물까지.'; }
      else m+=`자료와 다름: ${diff.join(', ')} (kJ/mol)으로 옮겨 보세요.`;
      st.msg=m; draw(); }
    root.querySelectorAll('[data-rx]').forEach(b=>b.addEventListener('click',()=>{ setRx(b.dataset.rx); }));
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',draw));
    root.querySelectorAll('[data-j]').forEach(b=>b.addEventListener('click',()=>judge(b.dataset.j)));
    $('[data-act="reset"]').addEventListener('click',init);
    init(); API.ready(()=>draw());
  }
};
})();
