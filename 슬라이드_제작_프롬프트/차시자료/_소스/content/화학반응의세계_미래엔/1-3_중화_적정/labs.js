/* 1-3 중화 적정 — 실험실
   rm13titr : 데이터로 중화 적정 곡선 그리기 (필수 탐구 반01-탐2, 교과서 16–17쪽 탐구)
     · 시료 20.0 mL: 0.1 M 염산 / 0.1 M 아세트산(Ka 1.8×10^-5) / 농도를 모르는 염산(참값 0.08 M). 표준 용액 0.1 M NaOH, 1방울 = 0.05 mL.
     · pH = 전하 균형으로 계산(강산: [H3O+] = (d+√(d²+4Kw))/2, 약산: 이분법) + 센서 잡음 ±0.02(고정 시드).
     · 넣을 때마다 (부피, pH)가 표에 쌓이고 그래프에 점이 찍힌다. 「곡선 잇기」로 점을 이어 시각화.
     · 시료를 바꾸면 지금까지의 점은 회색 점선 「이전 곡선」으로 남아 두 곡선을 비교할 수 있다.
     · 기록한 점 가운데 pH가 가장 크게 변한 구간의 가운데를 중화점으로 읽고, 산의 몰농도 = 0.1 × V중화점 / 20을 계산한다.
     · 뷰렛 50 mL, 위가 0 눈금, 처음 눈금 0.50 mL. */
window.DECK_LABS = {
  rm13titr(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), C=API.COL, mk=(t,a,p)=>API.mk(t,a,p);
    const WATER='#DDEEF8', WATER_S='#9FC3DD', GLASS='#7E8B98', STAND='#5B6B7F', KW=1e-14;
    const ACID=[{n:'0.1 M 염산',C:0.1,Ka:0,col:C.ink},{n:'0.1 M 아세트산',C:0.1,Ka:1.8e-5,col:C.equi},{n:'농도 모르는 염산',C:0.08,Ka:0,col:C.ink}];
    const VA=20, CB=0.1, R0=0.50;
    function pHcalc(a,V){
      const A=ACID[a], Vt=(VA+V)/1000, na=A.C*VA/1000, nb=CB*V/1000;
      if(!A.Ka){ const d=(na-nb)/Vt, h=(d+Math.sqrt(d*d+4*KW))/2; return -Math.log10(h); }
      const Ct=na/Vt, Na=nb/Vt; let lo=-14.5, hi=0.5, m=0;
      for(let i=0;i<70;i++){ m=(lo+hi)/2; const h=Math.pow(10,m); const f=h+Na-Ct*A.Ka/(A.Ka+h)-KW/h; if(f>0) hi=m; else lo=m; }
      return -m; }
    // ── 기하
    const BX=112, BW=16, YT=10, Y0=22, PPM=4, STOP=Y0+50*PPM+18, TIP=STOP+14;   // 뷰렛 (0 위)
    const KX=62, KW2=100, KY=262, KB=314;                                    // 비커
    const AX=300, AY=286, AW=330, AH=250, VMAX=30;                           // 그래프
    const X=v=>AX+v/VMAX*AW, Y=p=>AY-Math.max(0,Math.min(14,p))/14*AH;
    const base=mk('g',{},svg);
    // 스탠드
    mk('rect',{x:10,y:KB+6,width:180,height:8,rx:2,fill:STAND},base);
    mk('rect',{x:24.5,y:4,width:7,height:KB+2,fill:'#8C99A6',stroke:STAND,'stroke-width':1.2},base);
    mk('line',{x1:28,y1:162,x2:BX-12,y2:162,stroke:STAND,'stroke-width':5,'stroke-linecap':'round'},base);
    mk('path',{d:`M${BX-13},153 L${BX-9},162 L${BX-13},171 M${BX+13},153 L${BX+9},162 L${BX+13},171`,fill:'none',stroke:STAND,'stroke-width':3,'stroke-linecap':'round'},base);
    // 뷰렛
    const bLiq=mk('rect',{x:BX-BW/2+1.5,width:BW-3,fill:WATER},base);
    const bMen=mk('path',{fill:'none',stroke:WATER_S,'stroke-width':2},base);
    mk('rect',{x:BX-2,y:STOP+6,width:4,height:TIP-STOP-10,fill:WATER},base);
    mk('path',{d:`M${BX-BW/2},${YT} L${BX-BW/2},${STOP-8} M${BX+BW/2},${YT} L${BX+BW/2},${STOP-8}`,fill:'none',stroke:GLASS,'stroke-width':2.4},base);
    for(let v=0;v<=50;v+=5){ const y=Y0+v*PPM, L=v%10===0?9:6;
      mk('line',{x1:BX-BW/2,y1:y,x2:BX-BW/2+L,y2:y,stroke:v===0?C.ink:C.muted,'stroke-width':v%10===0?1.6:1.1},base);
      if(v%10===0) API.texText(base,BX-BW/2-6,y+6,String(v),{size:18,anchor:'end',fill:v===0?C.ink:C.muted}); }
    mk('path',{d:`M${BX-BW/2},${STOP-8} L${BX-4},${STOP-4} L${BX-4},${STOP+6} L${BX-2.5},${TIP} L${BX+2.5},${TIP} L${BX+4},${STOP+6} L${BX+4},${STOP-4} L${BX+BW/2},${STOP-8}`,fill:'none',stroke:GLASS,'stroke-width':2.2,'stroke-linejoin':'round'},base);
    mk('rect',{x:BX-9,y:STOP-5,width:18,height:10,rx:3,fill:'#E9EEF3',stroke:GLASS,'stroke-width':2},base);
    mk('rect',{x:BX+9,y:STOP-3.5,width:14,height:7,rx:2,fill:C.minus},base);
    API.texText(base,BX+16,40,'\\ce{NaOH(aq)}',{size:18,anchor:'start',fill:C.minus});
    // 비커 액체(움직임) + 비커 + 센서 + 젓개
    const kLiq=mk('rect',{x:KX+2,width:KW2-4,fill:WATER},base), kSurf=mk('line',{x1:KX+2,x2:KX+KW2-2,stroke:WATER_S,'stroke-width':2},base);
    mk('rect',{x:KX+40,y:KB-11,width:26,height:7,rx:3,fill:'#FFFFFF',stroke:STAND,'stroke-width':1.6},base);
    mk('path',{d:`M${KX-8},${KY} L${KX-1},${KY+6} L${KX-1},${KB-8} Q${KX-1},${KB} ${KX+8},${KB} L${KX+KW2-8},${KB} Q${KX+KW2+1},${KB} ${KX+KW2+1},${KB-8} L${KX+KW2+1},${KY}`,fill:'none',stroke:GLASS,'stroke-width':3,'stroke-linejoin':'round'},base);
    mk('line',{x1:KX+22,y1:KY-36,x2:KX+22,y2:KB-20,stroke:'#3A3F47','stroke-width':7,'stroke-linecap':'round'},base);
    mk('ellipse',{cx:KX+22,cy:KB-18,rx:6,ry:8,fill:'#9AA5B1'},base);
    mk('path',{d:`M${KX+22},${KY-36} Q${KX+40},${KY-80} 190,${KY-70}`,fill:'none',stroke:'#3A3F47','stroke-width':2.5},base);
    mk('rect',{x:KX-10,y:KB+0.5,width:KW2+20,height:5,rx:2,fill:'#C9D3DD'},base);
    mk('rect',{x:186,y:KY-96,width:106,height:46,rx:7,fill:C.ink},base);
    mk('rect',{x:192,y:KY-90,width:94,height:34,rx:4,fill:'#CFE8D8'},base);
    API.texText(base,239,KY-104,'\\text{pH 센서}',{size:18,anchor:'middle',fill:C.muted});
    // 방울
    const drops=[]; for(let i=0;i<5;i++){ drops.push({el:mk('ellipse',{cx:BX,rx:3.2,ry:4.2,fill:WATER_S,opacity:0},base),t:-9}); }
    // 그래프
    const gx=mk('g',{},svg);
    mk('line',{x1:AX,y1:AY,x2:AX+AW+10,y2:AY,stroke:C.muted,'stroke-width':2},gx);
    mk('line',{x1:AX,y1:AY,x2:AX,y2:AY-AH-10,stroke:C.muted,'stroke-width':2},gx);
    mk('line',{x1:AX,y1:Y(7),x2:AX+AW,y2:Y(7),stroke:C.grav,'stroke-width':1.5,'stroke-dasharray':'6 5'},gx);
    [0,10,20,30].forEach(v=>{ mk('line',{x1:X(v),y1:AY,x2:X(v),y2:AY+6,stroke:C.muted,'stroke-width':2},gx); API.texText(gx,X(v),AY+25,String(v),{size:18,anchor:'middle',fill:C.muted}); });
    [0,7,14].forEach(p=>{ mk('line',{x1:AX-6,y1:Y(p),x2:AX,y2:Y(p),stroke:C.muted,'stroke-width':2},gx); API.texText(gx,AX-10,Y(p)+6,String(p),{size:18,anchor:'end',fill:C.muted}); });
    API.texText(gx,AX+10,AY-AH-6,'\\text{pH}',{size:18,anchor:'start',fill:C.muted});
    API.texText(gx,AX+AW+10,AY-10,'V\\ [\\text{mL}]',{size:18,anchor:'end',fill:C.muted});
    const prevG=mk('g',{},svg), lineP=mk('path',{fill:'none','stroke-width':2.5,'stroke-linejoin':'round'},svg), ptsG=mk('g',{},svg), eqG=mk('g',{},svg);
    // ── 상태
    let seed=7; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    let st, shown=R0, prev=null;
    const f2=v=>v.toFixed(2);
    function meas(V){ return pHcalc(st.a,V)+(rnd()-0.5)*0.04; }
    function init(keepPrev){ st={a:st?st.a:0,n:0,rows:[],line:true,msg:''}; seed=7; st.rows.push({v:0,p:meas(0)}); shown=R0; if(!keepPrev) prev=null; }
    const V=()=>st.n*0.05;
    function analyse(){
      const rs=st.rows.slice().sort((a,b)=>a.v-b.v); let best=null;
      for(let i=1;i<rs.length;i++){ const d=rs[i].p-rs[i-1].p; if(!best||d>best.d+1e-9) best={d,i,a:rs[i-1],b:rs[i]}; }
      if(!best||best.d<=2.5) return null;
      // 이웃 구간도 크게 변했으면 두 구간이 만나는 점이 중화점(급변 구간의 가운데 점)
      const i=best.i, dn=i+1<rs.length?rs[i+1].p-rs[i].p:0, dp=i>=2?rs[i-1].p-rs[i-2].p:0;
      best.ve= dn>0.5*best.d&&dn>=dp ? rs[i].v : dp>0.5*best.d ? rs[i-1].v : (best.a.v+best.b.v)/2;
      best.w= dn>0.5*best.d ? rs[i+1].v-rs[i-1].v : dp>0.5*best.d ? rs[i].v-rs[i-2].v : best.b.v-best.a.v;
      return best; }
    function message(){
      if(st.msg) return st.msg;
      const A=ACID[st.a], p=pHcalc(st.a,V()), eq=analyse();
      if(st.n===0) return `${A.n} 20.0 mL의 초기 pH를 기록했다. 표준 용액을 넣으며 데이터를 모으자.`;
      if(!eq) return p<6? `중화점 이전 — pH가 천천히 증가한다. 급격히 변하기 시작하면 0.1 mL·1방울씩 넣자.` : `pH가 크게 변하기 시작했다. 2 mL–3 mL를 더 넣어 곡선의 뒷부분까지 얻자.`;
      const ve=eq.ve, w=eq.w, pe=pHcalc(st.a,ve);
      let s=`pH가 가장 크게 변한 곳(${f2(eq.a.v)}–${f2(eq.b.v)} mL) → 중화점 ≈ ${f2(ve)} mL, 산의 몰농도 = 0.1 M × ${f2(ve)} mL ÷ 20.0 mL = ${(0.1*ve/20).toFixed(3)} M.`;
      s+= ACID[st.a].Ka? ` 중화점의 pH는 약 ${pe.toFixed(1)}이다(7보다 크다).` : ` 중화점의 pH는 약 7이다.`;
      if(w>2.1) s+=' (점 사이가 넓다 — 다시 할 때 중화점 근처를 1방울씩 넣으면 더 정확하다.)';
      return s; }
    function paint(){
      const A=ACID[st.a], p=st.rows[st.rows.length-1];
      O('rd').textContent=f2(R0+V())+' mL'; O('v').textContent=f2(V())+' mL'; O('ph').textContent=p.p.toFixed(2); O('n').textContent=st.rows.length+'개';
      Ov('disp').textContent='pH '+p.p.toFixed(2); API.place(Ov('disp'),239,KY-73,true);
      O('msg').textContent=message();
      root.querySelectorAll('[data-a]').forEach(b=>b.classList.toggle('on',+b.dataset.a===st.a));
      const lb=$('[data-act="line"]'); lb.classList.toggle('off',!st.line);
      // 비커 액면
      const lv=KB-6-(VA+V())*0.6;
      kLiq.setAttribute('y',lv); kLiq.setAttribute('height',KB-2-lv); kSurf.setAttribute('y1',lv); kSurf.setAttribute('y2',lv);
      // 점
      while(ptsG.firstChild) ptsG.removeChild(ptsG.firstChild);
      const rs=st.rows.slice().sort((a,b)=>a.v-b.v);
      rs.forEach(r=>{ if(r.v<=VMAX) mk('circle',{cx:X(r.v),cy:Y(r.p),r:4.5,fill:A.col,stroke:'#fff','stroke-width':1},ptsG); });
      const pd=rs.filter(r=>r.v<=VMAX).map((r,i)=>(i?'L':'M')+X(r.v).toFixed(1)+' '+Y(r.p).toFixed(1)).join(' ');
      lineP.setAttribute('d',st.line&&rs.length>1?pd:''); lineP.setAttribute('stroke',A.col);
      while(prevG.firstChild) prevG.removeChild(prevG.firstChild);
      if(prev&&prev.length>1) mk('path',{d:prev.filter(r=>r.v<=VMAX).map((r,i)=>(i?'L':'M')+X(r.v).toFixed(1)+' '+Y(r.p).toFixed(1)).join(' '),fill:'none',stroke:C.grav,'stroke-width':2.5,'stroke-dasharray':'6 4'},prevG);
      while(eqG.firstChild) eqG.removeChild(eqG.firstChild);
      const eq=analyse(); if(eq){ const ve=eq.ve; mk('line',{x1:X(ve),y1:AY,x2:X(ve),y2:AY-AH,stroke:C.field,'stroke-width':2,'stroke-dasharray':'5 4'},eqG); }
      // 표
      const tb=O('log'); tb.innerHTML='';
      st.rows.slice(-5).forEach((r,i,arr)=>{ const k=st.rows.length-arr.length+i, d=k>0?r.p-st.rows[k-1].p:null;
        const tr=document.createElement('tr'); tr.innerHTML=`<td>${A.n}</td><td>${f2(r.v)}</td><td>${r.p.toFixed(2)}</td><td>${d===null?'—':(d>=0?'+':'')+d.toFixed(2)}</td>`; tb.appendChild(tr); });
      if(window.__STILL) shown=R0+V();
      level(shown); }
    function level(rd){ const yl=Y0+rd*PPM; bLiq.setAttribute('y',yl); bLiq.setAttribute('height',STOP-8-yl);
      bMen.setAttribute('d',`M${BX-BW/2+3},${yl+1.5} Q${BX},${yl+5} ${BX+BW/2-3},${yl+1.5}`); }
    function add(u){
      st.msg='';
      if(R0+(st.n+u)*0.05>50+1e-9){ st.msg='뷰렛 눈금이 50 mL를 넘는다 — 더 넣을 수 없다. 「초기화」 하자.'; paint(); return; }
      st.n+=u; st.rows.push({v:V(),p:meas(V())});
      if(!window.__STILL){ const nd=Math.min(5,Math.max(1,Math.round(u/4))); drops.forEach((d,i)=>{ if(i<nd) d.t=-i*.12; }); }
      paint(); }
    root.querySelectorAll('[data-add]').forEach(b=>b.addEventListener('click',()=>add(+b.dataset.add)));
    root.querySelectorAll('[data-a]').forEach(b=>b.addEventListener('click',()=>{ const a=+b.dataset.a; if(a===st.a&&st.n===0) return;
      prev=st.rows.length>1? st.rows.slice().sort((x,y)=>x.v-y.v): prev; st.a=a; init(true);
      st.msg=`${ACID[a].n} 20.0 mL로 새로 적정한다. 앞의 데이터는 회색 점선(이전 곡선)으로 남겨 비교한다.`; paint(); }));
    $('[data-act="line"]').addEventListener('click',()=>{ st.line=!st.line; st.msg=''; paint(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ st.a=0; init(false); paint(); });
    API.loop(root,(dt)=>{
      const target=R0+V();
      if(Math.abs(shown-target)>1e-4){ shown+=(target-shown)*Math.min(1,dt*6); if(Math.abs(shown-target)<0.005) shown=target; level(shown); }
      const lv=+kSurf.getAttribute('y1');
      drops.forEach(d=>{ if(d.t<=-9) return; d.t+=dt; if(d.t<0){ d.el.setAttribute('opacity',0); return; }
        const q=d.t/.3; if(q>=1){ d.t=-9; d.el.setAttribute('opacity',0); return; }
        d.el.setAttribute('cy',TIP+6+(lv-TIP-6)*q*q); d.el.setAttribute('opacity',1); });
    });
    st=null; init(false); paint();
    API.ready(()=>{ paint(); });
  }
};
