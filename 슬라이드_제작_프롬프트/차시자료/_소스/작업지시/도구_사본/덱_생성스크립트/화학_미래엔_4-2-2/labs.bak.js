/* 4-2-2 중화 적정 — 실험실
   cm422titr : 식초 중화 적정 (필수 탐구 화04-탐3, 교과서 159–161쪽 탐구 · 실험 영상 대체)
     · 식초 A 1.00 M(6.0 %) / 식초 B 0.75 M(4.5 %) — 덱이 정한 참값. 희석 원액 / 1/10, 시료(피펫) 10.0 / 20.0 mL
     · 표준 용액 0.1 M NaOH, 한 방울 = 0.05 mL. 중화점 부피 V* = (식초 몰농도 / 희석) × 시료 / 0.1 + 시료마다 작은 오차(고정 시드)
     · 뷰렛 50 mL, 위가 0 눈금. 처음 눈금은 시료마다 다름. 50 mL를 넘게 넣을 수 없음(원액이면 넘침 → 희석 필요)
     · 색: V < V*−0.5 무색(떨어진 자리만 잠깐 붉음) · V* 바로 앞 무색(붉은색이 천천히 사라짐) · V* ≤ V < V*+0.1 연붉은색(중화점) · 그 뒤 붉은색(지나침)
     · 「기록」 → 표 누적, 중화점 행만 평균 → 묽힌 식초 몰농도 → 식초 몰농도 → 함량(%) = 몰농도 × 60 g/mol ÷ 1000 g × 100
     · 적정 곡선(pH–부피)은 그리지 않는다. */
window.DECK_LABS = {
  cm422titr(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), C=API.COL;
    const WATER='#DDEEF8', WATER_S='#9FC3DD', GLASS='#7E8B98', PINK_L='#F6C3D9', PINK_LS='#E79BBE', PINK='#E04A8B', PINK_S='#B8326C', STAND='#5B6B7F';
    const TRUE={A:1.00,B:0.75}, DELTA=[0.03,-0.08,0.02,-0.03,0.06], R0=[0.50,0.20,1.00,0.35,0.80];
    // ── 기하
    const BX=190, BW=16, Y0=24, PPM=3, STOP=190, TIP=210;           // 뷰렛
    const FX=190, FB=284, FH=72, FW=130, FNW=24, FNH=16;              // 삼각 플라스크
    const ZX=390, ZY=34, ZW=170, ZH=236, ZP=60, ZT=60;                // 확대 창 (1 mL = 60 px)
    const mk=(t,a,p)=>API.mk(t,a,p);
    const base=mk('g',{},svg);
    // 스탠드·흰 종이
    mk('rect',{x:40,y:FB+4,width:300,height:9,rx:2,fill:STAND},base);
    mk('rect',{x:56.5,y:6,width:7,height:FB-2,fill:'#8C99A6',stroke:STAND,'stroke-width':1.2},base);
    mk('line',{x1:60,y1:62,x2:BX-12,y2:62,stroke:STAND,'stroke-width':5,'stroke-linecap':'round'},base);
    mk('rect',{x:52,y:53,width:16,height:18,rx:3,fill:'#C9D3DD',stroke:STAND,'stroke-width':1.5},base);
    mk('path',{d:`M${BX-13},53 L${BX-9},62 L${BX-13},71 M${BX+13},53 L${BX+9},62 L${BX+13},71`,fill:'none',stroke:STAND,'stroke-width':3,'stroke-linecap':'round'},base);
    mk('path',{d:`M${FX-95},${FB+3} L${FX-80},${FB-4} L${FX+110},${FB-4} L${FX+95},${FB+3} Z`,fill:'#FFFFFF',stroke:C.grav,'stroke-width':1.5},base);
    // 뷰렛 액체(움직임)
    const bLiq=mk('rect',{x:BX-BW/2+1.5,width:BW-3,fill:WATER},base);
    const bMen=mk('path',{fill:'none',stroke:WATER_S,'stroke-width':2},base);
    mk('rect',{x:BX-2,y:STOP+6,width:4,height:TIP-STOP-12,fill:WATER},base);
    mk('path',{d:`M${BX-BW/2},8 L${BX-BW/2},${STOP-8} M${BX+BW/2},8 L${BX+BW/2},${STOP-8}`,fill:'none',stroke:GLASS,'stroke-width':2.4},base);
    for(let v=0;v<=50;v++){ const y=Y0+v*PPM, L=v%10===0?9:(v%5===0?6:0); if(!L) continue;
      mk('line',{x1:BX-BW/2,y1:y,x2:BX-BW/2+L,y2:y,stroke:v===0?C.ink:C.muted,'stroke-width':v%10===0?1.6:1.1},base);
      if(v%10===0) API.texText(base,BX-BW/2-6,y+6,String(v),{size:18,anchor:'end',fill:v===0?C.ink:C.muted}); }
    mk('path',{d:`M${BX-BW/2},${STOP-8} L${BX-4},${STOP-4} L${BX-4},${STOP+6} L${BX-2.5},${TIP} L${BX+2.5},${TIP} L${BX+4},${STOP+6} L${BX+4},${STOP-4} L${BX+BW/2},${STOP-8}`,fill:'none',stroke:GLASS,'stroke-width':2.2,'stroke-linejoin':'round'},base);
    mk('rect',{x:BX-9,y:STOP-5,width:18,height:10,rx:3,fill:'#E9EEF3',stroke:GLASS,'stroke-width':2},base);
    mk('rect',{x:BX+9,y:STOP-3.5,width:14,height:7,rx:2,fill:C.minus},base);
    API.texText(base,BX+34,196,'\\text{뷰렛}',{size:19,anchor:'start',fill:C.ink});
    API.texText(base,BX+34,220,'0.1\\ \\text{M}\\ \\ce{NaOH}',{size:19,anchor:'start',fill:C.minus});
    // 삼각 플라스크
    const ftop=FB-FH, fsh=ftop+FNH, hw=y=>y<=fsh?FNW/2:FNW/2+(FW/2-FNW/2)*(y-fsh)/(FB-8-fsh);
    const fLiq=mk('path',{fill:WATER},base), fSurf=mk('line',{'stroke-width':2,stroke:WATER_S},base);
    const spot=mk('ellipse',{cx:FX,rx:26,ry:6,fill:PINK,opacity:0},base);
    mk('path',{d:`M${FX-FNW/2-3},${ftop} L${FX-FNW/2},${ftop+4} L${FX-FNW/2},${fsh} L${FX-FW/2},${FB-8} Q${FX-FW/2},${FB} ${FX-FW/2+8},${FB} L${FX+FW/2-8},${FB} Q${FX+FW/2},${FB} ${FX+FW/2},${FB-8} L${FX+FNW/2},${fsh} L${FX+FNW/2},${ftop+4} L${FX+FNW/2+3},${ftop}`,fill:'none',stroke:GLASS,'stroke-width':2.6,'stroke-linejoin':'round'},base);
    // 떨어지는 방울
    const drops=[]; for(let i=0;i<6;i++){ const d=mk('ellipse',{cx:BX,rx:3.5,ry:4.5,fill:WATER_S,opacity:0},base); drops.push({el:d,t:-1}); }
    // 확대 창
    const defs=mk('defs',{},svg), cp=mk('clipPath',{id:'clip-cm422-17'},defs); mk('rect',{x:ZX,y:ZY,width:ZW,height:ZH,rx:10},cp);
    mk('rect',{x:ZX,y:ZY,width:ZW,height:ZH,rx:10,fill:'#FFFFFF'},svg);
    const zg=mk('g',{'clip-path':'url(#clip-cm422-17)'},svg);
    const zLiq=mk('rect',{x:ZX+ZW/2-ZT/2,width:ZT,fill:WATER},zg), zMen=mk('path',{fill:WATER,stroke:WATER_S,'stroke-width':2.4},zg);
    mk('path',{d:`M${ZX+ZW/2-ZT/2},${ZY} L${ZX+ZW/2-ZT/2},${ZY+ZH} M${ZX+ZW/2+ZT/2},${ZY} L${ZX+ZW/2+ZT/2},${ZY+ZH}`,stroke:GLASS,'stroke-width':2.6},zg);
    const zTicks=mk('g',{},zg);
    mk('rect',{x:ZX,y:ZY,width:ZW,height:ZH,rx:10,fill:'none',stroke:C.ink,'stroke-width':2},svg);
    const zRead=mk('line',{x1:ZX+ZW/2-ZT/2-4,x2:ZX+ZW+14,stroke:C.plus,'stroke-width':2,'stroke-dasharray':'5 4'},svg);
    const zLink=mk('line',{stroke:C.muted,'stroke-width':1.4,'stroke-dasharray':'3 4'},svg);
    API.texText(svg,ZX+ZW/2,ZY-10,'\\text{눈금 확대}',{size:19,anchor:'middle',fill:C.muted});
    // ── 상태
    let st, shown=0;
    const init=()=>{ st={vin:'A',dil:10,samp:20,k:0,n:0,rec:false,rows:[],msg:''}; shown=R0[0]; };
    const r0=()=>R0[st.k%5], vStar=()=>TRUE[st.vin]/st.dil*st.samp/0.1+DELTA[st.k%5], V=()=>st.n*0.05;
    const f2=v=>v.toFixed(2);
    function state(){ const v=V(), s=vStar(); if(st.n===0) return 'zero'; if(v<s-0.5) return 'none'; if(v<s-1e-9) return 'near'; if(v<s+0.1-1e-9) return 'end'; return 'over'; }
    const COLN={zero:'무색',none:'무색',near:'무색',end:'연붉은색',over:'붉은색'};
    function message(sx){
      if(st.msg) return st.msg;
      if(sx==='zero') return `묽힌 정도와 시료 부피를 정하고 페놀프탈레인을 넣었다(무색). 필요한 표준 용액의 부피를 예측한 뒤 넣어 보자.`;
      if(sx==='none') return `떨어진 자리만 잠깐 붉어졌다 사라진다 — 아직 아세트산이 남아 있다.`;
      if(sx==='near') return `붉은색이 천천히 사라진다 — 중화점이 가깝다. 한 방울씩 넣자.`;
      if(sx==='end') return `흔들어도 연붉은색이 남는다 — 중화점! 나중 눈금 ${f2(r0()+V())} mL를 읽고 「기록」.`;
      return `진한 붉은색 — 중화점을 지났다. 이 부피는 실제보다 크다. 「다음 시료」로 다시 하자.`; }
    function calc(){
      const ok=st.rows.filter(r=>r.s==='end');
      if(!st.rows.length) return '중화점에서 기록한 부피의 평균으로 식초 속 아세트산의 함량을 구한다.';
      if(!ok.length) return '중화점(연붉은색)에서 기록한 값이 없다 — 평균에 넣을 값이 없다.';
      const avg=ok.reduce((a,r)=>a+r.v,0)/ok.length, md=0.1*avg/st.samp, mv=md*st.dil;
      return `중화점 ${ok.length}회 평균 ${f2(avg)} mL → 묽힌 식초 ${md.toFixed(3)} M → 식초 ${mv.toFixed(2)} M → 함량 ${(mv*6).toFixed(1)} %`; }
    function paint(){
      const sx=state();
      O('v0').textContent=f2(r0())+' mL'; O('v1').textContent=f2(r0()+V())+' mL'; O('dv').textContent=f2(V())+' mL';
      O('col').textContent=COLN[sx]+(sx==='end'?' (중화점)':sx==='over'?' (지나침)':'');
      O('msg').textContent=message(sx); O('calc').textContent=calc();
      root.querySelectorAll('[data-v]').forEach(b=>b.classList.toggle('on',b.dataset.v===st.vin));
      root.querySelectorAll('[data-d]').forEach(b=>b.classList.toggle('on',+b.dataset.d===st.dil));
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',+b.dataset.s===st.samp));
      // 플라스크 액체
      const lv=FB-10-(st.samp+V())*0.42, a=hw(lv);
      fLiq.setAttribute('d',`M${FX-a+1.5},${lv} L${FX-FW/2+3},${FB-8} Q${FX-FW/2+3},${FB-1.5} ${FX-FW/2+10},${FB-1.5} L${FX+FW/2-10},${FB-1.5} Q${FX+FW/2-3},${FB-1.5} ${FX+FW/2-3},${FB-8} L${FX+a-1.5},${lv} Z`);
      fSurf.setAttribute('x1',FX-a+1.5); fSurf.setAttribute('x2',FX+a-1.5); fSurf.setAttribute('y1',lv); fSurf.setAttribute('y2',lv);
      const fc=sx==='end'?[PINK_L,PINK_LS]:sx==='over'?[PINK,PINK_S]:[WATER,WATER_S];
      fLiq.setAttribute('fill',fc[0]); fSurf.setAttribute('stroke',fc[1]);
      spot.setAttribute('cy',lv+16);
      const tb=O('log'); tb.innerHTML='';
      st.rows.slice(-3).forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${r.k}</td><td>${f2(r.a)}</td><td>${f2(r.b)}</td><td>${f2(r.v)}</td><td>${COLN[r.s]}</td>`; tb.appendChild(tr); });
      if(window.__STILL) shown=r0()+V();
      level(shown); }
    function level(rd){
      const yl=Y0+rd*PPM;
      bLiq.setAttribute('y',yl); bLiq.setAttribute('height',STOP-8-yl);
      bMen.setAttribute('d',`M${BX-BW/2+4},${yl+2} Q${BX},${yl+6} ${BX+BW/2-4},${yl+2}`);
      // 확대 창: 가운데 = 지금 눈금
      const cy=ZY+ZH/2, cx=ZX+ZW/2;
      zLiq.setAttribute('y',cy); zLiq.setAttribute('height',ZH);
      zMen.setAttribute('d',`M${cx-ZT/2},${cy-10} Q${cx-ZT/2+9},${cy} ${cx},${cy} Q${cx+ZT/2-9},${cy} ${cx+ZT/2},${cy-10} L${cx+ZT/2},${cy+4} L${cx-ZT/2},${cy+4} Z`);
      zRead.setAttribute('y1',cy); zRead.setAttribute('y2',cy);
      zLink.setAttribute('x1',BX+BW/2+2); zLink.setAttribute('y1',yl); zLink.setAttribute('x2',ZX-2); zLink.setAttribute('y2',cy);
      while(zTicks.firstChild) zTicks.removeChild(zTicks.firstChild);
      let li=0;
      for(let t=Math.ceil((rd-2.2)*10);t<=Math.floor((rd+2.2)*10);t++){
        if(t<0||t>500) continue;
        const y=cy+(t/10-rd)*ZP; if(y<ZY+3||y>ZY+ZH-3) continue;
        const L=t%10===0?30:(t%5===0?20:11);
        mk('line',{x1:cx-ZT/2,y1:y,x2:cx-ZT/2+L,y2:y,stroke:t%10===0?C.ink:C.muted,'stroke-width':t%10===0?2:1.2},zTicks);
        if(t%10===0 && y>ZY+12 && y<ZY+ZH-12 && li<4){ const e=Ov('z'+li); e.textContent=String(t/10); API.place(e,ZX+24,y,true); li++; } }
      for(;li<4;li++) API.place(Ov('z'+li),0,0,false); }
    function add(u){
      st.msg='';
      if(r0()+(st.n+u)*0.05>50+1e-9){ st.msg=`뷰렛 눈금이 50 mL를 넘는다 — 표준 용액이 모자란다. 식초를 묽히거나 시료를 줄여 다시 설계하자.`; paint(); return; }
      const before=state(); st.n+=u; const sx=state();
      // 방울 떨어뜨리기 + 붉은 자국
      if(!window.__STILL){ const nd=Math.min(6,Math.max(1,Math.round(u/3))); drops.forEach((d,i)=>{ if(i<nd) d.t=-i*.12; });
        spotLife=(sx==='near')?2.4:(sx==='none'?.7:0); spotDelay=nd*.12+.25; }
      paint(); }
    let spotLife=0, spotDelay=0, spotT=-1;
    $('[data-act="rec"]').addEventListener('click',()=>{ st.msg='';
      if(st.n===0){ st.msg='아직 표준 용액을 넣지 않았다.'; paint(); return; }
      if(st.rec){ st.msg='이 시료는 이미 기록했다 — 「다음 시료」.'; paint(); return; }
      st.rows.push({k:st.k+1,a:r0(),b:r0()+V(),v:V(),s:state()}); st.rec=true; st.msg=`실험 ${st.k+1}의 부피 ${f2(V())} mL를 기록했다. 「다음 시료」로 3회 이상 반복하자.`; paint(); });
    $('[data-act="next"]').addEventListener('click',()=>{ st.k++; st.n=0; st.rec=false; st.msg=`새 시료 ${st.k+1}: 뷰렛을 다시 채우고 처음 눈금 ${f2(r0())} mL를 읽었다.`; shown=r0(); paint(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ init(); paint(); });
    const newExp=()=>{ st.k=0; st.n=0; st.rec=false; st.rows=[]; st.msg=''; shown=r0(); paint(); };
    root.querySelectorAll('[data-v]').forEach(b=>b.addEventListener('click',()=>{ st.vin=b.dataset.v; newExp(); }));
    root.querySelectorAll('[data-d]').forEach(b=>b.addEventListener('click',()=>{ st.dil=+b.dataset.d; newExp(); }));
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ st.samp=+b.dataset.s; newExp(); }));
    root.querySelectorAll('[data-add]').forEach(b=>b.addEventListener('click',()=>add(+b.dataset.add)));
    API.loop(root,(dt)=>{
      const target=r0()+V();
      if(Math.abs(shown-target)>1e-4){ shown+=(target-shown)*Math.min(1,dt*6); if(Math.abs(shown-target)<0.005) shown=target; level(shown); }
      const lv=+fSurf.getAttribute('y1');
      drops.forEach(d=>{ if(d.t<0){ if(d.t>-1){ d.t+=dt; } d.el.setAttribute('opacity',0); if(d.t>=0) d.t=0.0001; return; }
        d.t+=dt; const p=d.t/.35, y=TIP+6+(lv-TIP-6)*p*p;
        if(p>=1){ d.t=-1; d.el.setAttribute('opacity',0); return; }
        d.el.setAttribute('cy',y); d.el.setAttribute('opacity',1); });
      if(spotDelay>0){ spotDelay-=dt; if(spotDelay<=0 && spotLife>0) spotT=0; }
      if(spotT>=0){ spotT+=dt; const o=Math.max(0,.6*(1-spotT/spotLife)); spot.setAttribute('opacity',o.toFixed(3)); if(o<=0) spotT=-1; }
    });
    init(); paint();
    API.ready(()=>{ paint(); });
  }
};
