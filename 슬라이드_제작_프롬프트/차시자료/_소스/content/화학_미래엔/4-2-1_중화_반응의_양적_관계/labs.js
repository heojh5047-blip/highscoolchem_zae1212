/* 4-2-1 중화 반응의 양적 관계 — 실험실
   cm421mix : 중화 반응 가상 실험 (교과서 157쪽 디지털 소양 키우기·153/155쪽 모의실험 대체)
     · 산: 0.1 M 염산(가수 1) / 0.1 M 황산(가수 2), 산 부피 10·20 mL, 넣은 0.1 M NaOH 수용액 0–40 mL(5 mL 간격)
     · 넣은 H+ = 가수 × 0.1 × V산(L), 넣은 OH- = 0.1 × V염기(L), 생성된 물 = 둘 중 작은 값 (H+ : OH- = 1 : 1)
     · 입자 1개 = 0.0005 mol. 반응 칸 j에서 H+ j와 OH- j가 만나 물 분자 j가 된다(원자 보존).
     · 액체 색 = BTB(산성 노랑, 중성 초록, 염기성 파랑). 막대 = 입자 수. 「기록」 → 표 누적(최근 3행). 적정 곡선은 그리지 않는다. */
window.DECK_LABS = {
  cm421mix(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), C=API.COL;
    const BX=20, BW=320, BASE=330, TIP=[290,74];
    const COLS={a:'#F6E58A',n:'#BFE3B4',b:'#AFCDF2'}, EDGE={a:'#D8C25A',n:'#8DC48A',b:'#7FA6D8'};
    // ── 칸(슬롯): 7열 × 3행, 고정 순서로 섞어 음이온 4 · 반응 8 · Na+ 8
    const SL=[]; for(let r=0;r<4;r++) for(let c=0;c<6;c++) SL.push([BX+BW*(c+.5)/6, BASE-24-r*45]);
    let seed=11; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    const order=SL.map((_,i)=>i); for(let i=order.length-1;i>0;i--){ const j=Math.floor(rnd()*(i+1)); [order[i],order[j]]=[order[j],order[i]]; }
    const SA=order.slice(0,4).map(i=>SL[i]), SR=order.slice(4,12).map(i=>SL[i]), SN=order.slice(12,20).map(i=>SL[i]);
    // ── 정적 틀
    const base=API.mk('g',{},svg);
    const liq=API.mk('rect',{x:BX+1.5,width:BW-3,fill:COLS.a},base);
    const surf=API.mk('line',{x1:BX+1.5,x2:BX+BW-1.5,stroke:EDGE.a,'stroke-width':2},base);
    API.mk('path',{d:`M${BX-6},${BASE-252} L${BX},${BASE-244} L${BX},${BASE} L${BX+BW},${BASE} L${BX+BW},${BASE-244} L${BX+BW+6},${BASE-252}`,fill:'none',stroke:'#7E8B98','stroke-width':2.6,'stroke-linejoin':'round'},base);
    API.mk('rect',{x:TIP[0]-11,y:0,width:22,height:58,rx:3,fill:COLS.b,stroke:'#7E8B98','stroke-width':2},base);
    API.mk('rect',{x:TIP[0]-11,y:0,width:22,height:20,rx:3,fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':2},base);
    API.mk('path',{d:`M${TIP[0]-6},58 L${TIP[0]},${TIP[1]} L${TIP[0]+6},58`,fill:'#7E8B98'},base);
    API.texText(base,TIP[0]-20,30,'0.1\\ \\text{M}\\ \\ce{NaOH(aq)}',{size:19,anchor:'end',fill:C.muted});
    // 막대그래프 틀
    const GX=[400,442,484,526,568], GB=BASE, U=24;
    for(let v=2;v<=8;v+=2){ const y=GB-v*U; API.mk('line',{x1:382,y1:y,x2:592,y2:y,stroke:'#E1E6EC','stroke-width':1.2},base); API.texText(base,376,y+6,String(v),{size:18,anchor:'end',fill:C.muted}); }
    API.texText(base,376,GB+6,'0',{size:18,anchor:'end',fill:C.muted});
    API.mk('line',{x1:382,y1:GB,x2:594,y2:GB,stroke:C.ink,'stroke-width':2},base);
    API.mk('line',{x1:382,y1:GB,x2:382,y2:106,stroke:C.ink,'stroke-width':2},base);
    API.texText(base,388,112,'\\text{입자 수}',{size:19,anchor:'start',fill:C.ink});
    [['\\ce{H+}',0],['\\ce{Na+}',2],['\\ce{OH-}',3],['\\text{물}',4]].forEach(([t,i])=>API.texText(base,GX[i],GB+26,t,{size:18,anchor:'middle',fill:C.ink}));
    const BF=[[C.plus,C.plus],['#D5DCE3',C.grav],[C.grav,'#6F7C89'],[C.minus,C.minus],['#FFFFFF',C.grav]];
    const bars=BF.map(([f,s])=>API.mk('rect',{width:30,fill:f,stroke:s,'stroke-width':1.6},base));
    API.texText(base,BX+BW/2,384,'\\text{입자 1개}=0.0005\\ \\text{mol}',{size:19,anchor:'middle',fill:C.muted});
    // 범례: 물 분자
    const lg=API.mk('g',{transform:'translate(420,400)'},base); water(lg);
    API.texText(base,454,406,'\\text{물 분자}',{size:19,anchor:'start',fill:C.muted});
    // ── 입자 풀 (처음에 만들어 라벨이 KaTeX로 바뀌게 함)
    function water(g){ API.atom(g,0,-4,14,'O','-'); [35,145].forEach(a=>{ const r=a*Math.PI/180; API.atom(g,18*Math.cos(r),-4+18*Math.sin(r),10,'H','-'); }); }
    const layer=API.mk('g',{},svg);
    function mkIon(kind){ const g=API.mk('g',{},layer);
      const sp={H:['P','\\ce{H+}','#FFFFFF',19],OH:['M','\\ce{OH-}','#FFFFFF',19],Na:['N','\\ce{Na+}',C.ink,19],Cl:['N','\\ce{Cl-}',C.ink,19],SO4:['N','\\ce{SO4^2-}',C.ink,23]}[kind];
      if(kind==='W') water(g); else { API.charge(g,0,0,sp[3],sp[0]); API.texText(g,0,6.5,sp[1],{size:18,anchor:'middle',fill:sp[2],weight:700}); }
      const it={g,x:0,y:0,vis:false,anim:null,pop:1,ph:rnd()*6.28}; g.style.display='none'; return it; }
    const P={H:[],OH:[],Na:[],W:[],Cl:[],SO4:[]};
    for(let i=0;i<8;i++){ P.H.push(mkIon('H')); P.OH.push(mkIon('OH')); P.Na.push(mkIon('Na')); P.W.push(mkIon('W')); }
    for(let i=0;i<4;i++){ P.Cl.push(mkIon('Cl')); P.SO4.push(mkIon('SO4')); }
    const vis=(it,v)=>{ it.vis=v; it.g.style.display=v?'':'none'; };
    const put=(it,x,y)=>{ it.x=x; it.y=y; };
    // ── 상태
    let st={a:1,va:20,vb:0}, rec=[];
    const cnt=()=>{ const H=st.a*st.va/5, A=st.va/5, OH=st.vb/5, W=Math.min(H,OH); return {H,A,OH,Na:OH,W,rH:H-W,rOH:OH-W}; };
    const fmt=v=>v.toFixed(4)+' mol';
    function apply(prev){
      const k=cnt(), anim=prev!=null && !window.__STILL && st.vb>prev;
      const pOH=prev!=null? prev/5 : 0;
      ['Cl','SO4'].forEach(t=>P[t].forEach((it,i)=>{ vis(it, t===(st.a===1?'Cl':'SO4') && i<k.A); it.anim=null; put(it,...SA[i]); }));
      P.Na.forEach((it,i)=>{ const on=i<k.Na; if(on && anim && i>=pOH){ it.anim={t:-(i-pOH)*.35,x0:TIP[0],y0:TIP[1]+16,x1:SN[i][0],y1:SN[i][1]}; } else it.anim=null; vis(it,on); put(it,...(it.anim?[TIP[0],TIP[1]+16]:SN[i])); });
      for(let j=0;j<8;j++){ const [x,y]=SR[j], h=P.H[j], o=P.OH[j], w=P.W[j];
        [h,o,w].forEach(it=>{ it.anim=null; put(it,x,y); });
        const isW=j<k.W, isH=!isW && j<k.H, isO=!isW && !isH && j<k.OH;
        if(anim && j>=pOH && j<k.OH){   // 새로 넣은 OH-가 떨어져 들어온다
          o.anim={t:-(j-pOH)*.35-.15,x0:TIP[0],y0:TIP[1]+16,x1:x,y1:y,land:isW?j:-1}; put(o,TIP[0],TIP[1]+16); vis(o,true);
          vis(h,isW); vis(w,false);
        } else { vis(h,isH); vis(o,isO); vis(w,isW); w.pop=1; }
      }
      paint(k); }
    function kindOf(k){ return k.rH>0?'a':k.rOH>0?'b':(k.H>0?'n':'n'); }
    function paint(k){
      const top=BASE-(186+54*(st.va+st.vb-10)/50), kd=kindOf(k);
      liq.setAttribute('y',top); liq.setAttribute('height',BASE-top-1.5); liq.setAttribute('fill',COLS[kd]);
      surf.setAttribute('y1',top); surf.setAttribute('y2',top); surf.setAttribute('stroke',EDGE[kd]);
      const vals=[k.rH,k.A,k.Na,k.rOH,k.W];
      vals.forEach((v,i)=>{ bars[i].setAttribute('x',GX[i]-15); bars[i].setAttribute('y',GB-v*U); bars[i].setAttribute('height',v*U);
        const e=Ov('c'+i); e.textContent=String(v); API.place(e,GX[i],GB-v*U-26,true); });
      const an=Ov('anion'); an.innerHTML=API.tex(st.a===1?'\\ce{Cl-}':'\\ce{SO4^2-}'); API.place(an,GX[1],GB+30,true);
      O('vb').textContent=st.vb+' mL';
      O('nh').textContent=fmt(st.a*0.1*st.va/1000); O('noh').textContent=fmt(0.1*st.vb/1000); O('nw').textContent=fmt(k.W*0.0005);
      O('kind').textContent={a:'산성 (노란색)',n:'중성 (초록색)',b:'염기성 (파란색)'}[kd];
      root.querySelectorAll('[data-a]').forEach(b=>b.classList.toggle('on',+b.dataset.a===st.a));
      root.querySelectorAll('[data-va]').forEach(b=>b.classList.toggle('on',+b.dataset.va===st.va));
      O('msg').textContent=message(k,kd); }
    function message(k,kd){
      const an=st.a===1?'염화 이온':'황산 이온', need=(k.H-k.OH)*5;
      if(st.vb===0) return `산 수용액만 있다(수소 이온 ${k.H}개, ${an} ${k.A}개). 수산화 나트륨 수용액을 5 mL씩 넣어 보자.`;
      if(kd==='a') return `수산화 이온이 모두 물이 되고 수소 이온 ${k.rH}개가 남아 산성. 완전히 중화하려면 ${need} mL 더. 나트륨 이온·${an}(구경꾼 이온)은 줄지 않는다.`;
      if(kd==='n') return `완전히 중화! 가수×몰농도×부피: 산 ${st.a}×0.1×${(st.va/1000).toFixed(3)} = 염기 1×0.1×${(st.vb/1000).toFixed(3)} = ${(k.W*0.0005).toFixed(4)} mol → 중성.`;
      return `수소 이온이 모두 반응해 더 넣은 수산화 이온 ${k.rOH}개가 남는다 → 염기성. 물 분자는 ${k.W}개에서 더 늘지 않는다.`; }
    function record(){ const k=cnt(), kd=kindOf(k);
      const left=k.rH? `${API.tex('\\ce{H+}')} ${k.rH}` : k.rOH? `${API.tex('\\ce{OH-}')} ${k.rOH}` : '없음';
      rec.push(`<td>${st.a===1?'염산':'황산'}</td><td>${st.va}</td><td>${st.vb}</td><td>${left}</td><td>${(k.W*0.0005).toFixed(4)}</td><td>${{a:'산성',n:'중성',b:'염기성'}[kd]}</td>`);
      const tb=O('log'); tb.innerHTML=''; rec.slice(-3).forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=r; tb.appendChild(tr); }); }
    const sl=$('[data-i="vb"]');
    sl.addEventListener('input',()=>{ const prev=st.vb; st.vb=+sl.value; apply(prev); });
    root.querySelectorAll('[data-a]').forEach(b=>b.addEventListener('click',()=>{ st.a=+b.dataset.a; apply(null); }));
    root.querySelectorAll('[data-va]').forEach(b=>b.addEventListener('click',()=>{ st.va=+b.dataset.va; apply(null); }));
    $('[data-act="rec"]').addEventListener('click',record);
    $('[data-act="reset"]').addEventListener('click',()=>{ st={a:1,va:20,vb:0}; sl.value=0; rec=[]; O('log').innerHTML=''; apply(null); });
    function draw(t){
      ['H','OH','Na','W','Cl','SO4'].forEach(k=>P[k].forEach(it=>{ if(!it.vis) return;
        let x=it.x, y=it.y, s=it.pop;
        if(!it.anim && !window.__STILL){ x+=1.5*Math.sin(t*1.7+it.ph); y+=1.5*Math.cos(t*1.3+it.ph*1.7); }
        it.g.setAttribute('transform',`translate(${x.toFixed(1)},${y.toFixed(1)})`+(s<1?` scale(${s.toFixed(3)})`:'')); })); }
    API.loop(root,(dt,t)=>{
      ['OH','Na'].forEach(k=>P[k].forEach((it,j)=>{ const a=it.anim; if(!a) return;
        a.t+=dt; const p=Math.max(0,Math.min(1,a.t/.7)), e=1-(1-p)*(1-p);
        it.x=a.x0+(a.x1-a.x0)*e; it.y=a.y0+(a.y1-a.y0)*e;
        if(p>=1){ it.anim=null; it.x=a.x1; it.y=a.y1;
          if(a.land!=null && a.land>=0){ vis(it,false); vis(P.H[j],false); const w=P.W[j]; w.pop=0; vis(w,true); } } }));
      P.W.forEach(w=>{ if(w.vis && w.pop<1) w.pop=Math.min(1,w.pop+dt*3); });
      draw(t); });
    apply(null); draw(0);
    API.ready(()=>{ apply(null); draw(0); });
  }
};
