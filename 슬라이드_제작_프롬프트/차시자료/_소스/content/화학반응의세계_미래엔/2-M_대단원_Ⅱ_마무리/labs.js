/* 2-M 대단원 Ⅱ 마무리 — 실험실
   rm29range : 과학 글쓰기 12 — 전해질과 에너지 밀도에 따른 주행 거리 (교과서 73쪽 자료로 만든 단순 모형)
     · 기준: 에너지 밀도 250 Wh/kg → 1회 충전 550 km (교과서 500–600 km의 가운데), 전지 질량 일정
     · 주행 거리 = 550 × (d/250) × 충전(완속 1, 급속 0.8) × 계절(봄·가을 1, 겨울 0.65 = 30–40 % 감소의 가운데)
     · 충격 주기: 액체 전해질 → 분리막 손상·화재 위험, 고체 전해질 → 화재 위험 적음
     · 「기록」 → 표 최대 5행, 「초기화」 → 액체·250·완속·봄가을 */
window.DECK_LABS = {
  rm29range(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=$('svg'), iD=$('[data-i="d"]');
    const OX='#C2410C', RD='#0E7490';
    let el='liq', ch='full', se='mild', shocked=false, log=[], cur=null;
    const show=(g,on)=>g.setAttribute('display',on?'inline':'none');
    // ── 전지 단면 ──
    API.mk('path',{d:'M70 56 V36 H330 V56',fill:'none',stroke:'#16233D','stroke-width':3},svg);
    API.arrow(svg,170,20,230,20,'#1F6FD1',3);
    API.texText(svg,242,27,'$e^-$',{size:20,anchor:'start',fill:'#1F6FD1',mix:true});
    const elec=API.mk('rect',{x:100,y:56,width:200,height:120,fill:'#DDEEF8',stroke:'#9FC3DD','stroke-width':2},svg);
    API.mk('rect',{x:40,y:56,width:60,height:120,rx:4,fill:'#4A4F57'},svg);
    API.mk('rect',{x:300,y:56,width:60,height:120,rx:4,fill:'#B8BEC6',stroke:'#7E8B98','stroke-width':2},svg);
    const sep=API.mk('line',{x1:200,y1:56,x2:200,y2:176,stroke:'#5B6B7F','stroke-width':3,'stroke-dasharray':'7 5'},svg);
    const ions=[0,1,2,3,4].map(k=>API.mk('circle',{cx:120,cy:74+k*22,r:6,fill:'#D7263D'},svg));
    const gCrack=API.mk('g',{},svg);
    API.mk('path',{d:'M200 56 V96 L186 110 L214 124 L200 138 V176',fill:'none',stroke:'#C2410C','stroke-width':3},gCrack);
    API.mk('path',{d:'M200 80 C184 102 180 120 194 138 C188 120 202 116 200 104 C212 116 214 130 208 140 C226 124 218 100 200 80 Z',fill:'#F59E0B',stroke:'#C2410C','stroke-width':2},gCrack);
    const gSafe=API.mk('g',{},svg);
    API.mk('rect',{x:128,y:98,width:144,height:36,rx:8,fill:'#FFFFFF',stroke:'#2E9E6A','stroke-width':2},gSafe);
    API.texText(gSafe,200,123,'안전',{size:20,anchor:'middle',fill:'#2E9E6A',mix:true});
    API.texText(svg,70,198,'(−)극',{size:18,anchor:'middle',mix:true});
    API.texText(svg,70,220,'산화 전극',{size:18,anchor:'middle',fill:OX,mix:true});
    API.texText(svg,330,198,'(+)극',{size:18,anchor:'middle',mix:true});
    API.texText(svg,330,220,'환원 전극',{size:18,anchor:'middle',fill:RD,mix:true});
    const gLiq=API.mk('g',{},svg), gSol=API.mk('g',{},svg);
    API.texText(gLiq,200,198,'액체 전해질',{size:18,anchor:'middle',fill:'#3E73A8',mix:true});
    API.texText(gLiq,200,220,'+ 분리막',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    API.texText(gSol,200,198,'고체 전해질',{size:18,anchor:'middle',fill:'#7A6540',mix:true});
    // ── 충전량 · 계절 ──
    API.texText(svg,495,52,'충전량',{size:19,anchor:'middle',mix:true});
    API.mk('rect',{x:420,y:64,width:150,height:54,rx:8,fill:'#FFFFFF',stroke:'#5B6B7F','stroke-width':3},svg);
    API.mk('rect',{x:570,y:80,width:10,height:22,rx:2,fill:'#5B6B7F'},svg);
    const fill=API.mk('rect',{x:423,y:67,width:144,height:48,rx:6,fill:'#2E9E6A'},svg);
    const g100=API.mk('g',{},svg), g80=API.mk('g',{},svg);
    API.texText(g100,495,98,'100 %',{size:20,anchor:'middle',fill:'#FFFFFF',mix:true});
    API.texText(g80,480,98,'80 %',{size:20,anchor:'middle',fill:'#FFFFFF',mix:true});
    const gMild=API.mk('g',{},svg), gWin=API.mk('g',{},svg);
    API.texText(gMild,495,166,'봄·가을',{size:20,anchor:'middle',fill:'#2E9E6A',mix:true});
    API.mk('rect',{x:420,y:140,width:150,height:40,rx:8,fill:'#E3EEFB'},gWin);
    API.texText(gWin,495,166,'겨울: 약 35 % 감소',{size:18,anchor:'middle',fill:'#1F6FD1',mix:true});
    // ── 주행 거리 막대 ──
    const B0=40, B1=600, bx=k=>B0+Math.min(1000,k)/1000*(B1-B0), BY=248;
    API.texText(svg,B0,240,'예상 주행 거리 [km]',{size:18,anchor:'start',mix:true});
    API.mk('rect',{x:B0,y:BY,width:B1-B0,height:16,rx:8,fill:'#E4E9EE'},svg);
    const bar=API.mk('rect',{x:B0,y:BY,width:10,height:16,rx:8,fill:'#1F6FD1'},svg);
    [0,250,500,750,1000].forEach(v=>{ API.mk('line',{x1:bx(v),y1:BY+16,x2:bx(v),y2:BY+21,stroke:'#5B6B7F','stroke-width':1.5},svg);
      API.texText(svg,bx(v),BY+38,String(v),{size:18,anchor:'middle',mix:true}); });
    const car=API.mk('path',{d:'',fill:'#16233D'},svg);
    function calc(){ const d=+iD.value, c=ch==='fast'?0.8:1, s=se==='win'?0.65:1;
      return {d, km:Math.round(550*(d/250)*c*s)}; }
    function draw(){ const v=calc();
      O('d').textContent=v.d+' Wh/kg'; O('km').textContent='약 '+v.km+' km';
      const sf=!shocked?'아직 하지 않음':el==='liq'?'분리막 손상 → 화재 위험 큼':'고체 전해질 → 화재 위험 적음';
      O('safe').textContent=sf;
      let m=ch==='fast'&&se==='win'?'급속 충전(80 %)과 겨울(약 35 % 감소)이 겹쳐 주행 거리가 크게 줄었다.'
        :ch==='fast'?'급속 충전으로는 80 %만 충전되어 주행 거리가 줄었다.'
        :se==='win'?'겨울에는 주행 거리가 약 35 % 줄어든다.'
        :'에너지 밀도가 클수록 같은 무게의 전지로 더 멀리 간다.';
      if(shocked) m=(el==='liq'?'충격으로 분리막이 손상되어 화재가 날 수 있다! ':'고체 전해질은 충격에도 안전하다. ')+m;
      O('msg').textContent=m;
      elec.setAttribute('fill',el==='liq'?'#DDEEF8':'#E7DDC8'); elec.setAttribute('stroke',el==='liq'?'#9FC3DD':'#B9A98A');
      show(sep,el==='liq'&&!shocked); show(gLiq,el==='liq'); show(gSol,el==='sol');
      show(gCrack,shocked&&el==='liq'); show(gSafe,shocked&&el==='sol');
      fill.setAttribute('width',(144*(ch==='fast'?0.8:1)).toFixed(1)); show(g100,ch!=='fast'); show(g80,ch==='fast');
      show(gMild,se!=='win'); show(gWin,se==='win');
      const x=bx(v.km); bar.setAttribute('width',Math.max(16,x-B0).toFixed(1));
      car.setAttribute('d',`M${x-14} ${BY-4} L${x+14} ${BY-4} L${x} ${BY+2} Z`);
      cur={el:el==='liq'?'액체':'고체',d:v.d,ch:ch==='fast'?'급속':'완속',se:se==='win'?'겨울':'봄·가을',km:v.km,sh:!shocked?'—':el==='liq'?'화재 위험':'안전'};
    }
    function drawLog(){ O('log').innerHTML=log.map(r=>`<tr><td>${r.el}</td><td>${r.d}</td><td>${r.ch}</td><td>${r.se}</td><td>${r.km} km</td><td>${r.sh}</td></tr>`).join(''); }
    function seg(attr,val){ root.querySelectorAll(`[data-${attr}]`).forEach(b=>b.classList.toggle('rm29-act',b.dataset[attr]===val)); }
    root.querySelectorAll('[data-el]').forEach(b=>b.addEventListener('click',()=>{ el=b.dataset.el; shocked=false; seg('el',el); draw(); }));
    root.querySelectorAll('[data-ch]').forEach(b=>b.addEventListener('click',()=>{ ch=b.dataset.ch; seg('ch',ch); draw(); }));
    root.querySelectorAll('[data-se]').forEach(b=>b.addEventListener('click',()=>{ se=b.dataset.se; seg('se',se); draw(); }));
    iD.addEventListener('input',draw);
    $('[data-act="shock"]').addEventListener('click',()=>{ shocked=true; draw(); });
    $('[data-act="rec"]').addEventListener('click',()=>{ draw(); log.push(cur); if(log.length>5) log.shift(); drawLog(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; drawLog(); iD.value=250; el='liq'; ch='full'; se='mild'; shocked=false; seg('el',el); seg('ch',ch); seg('se',se); draw(); });
    API.onShow&&API.onShow(draw);
    draw(); drawLog();
    API.loop(root,(dt,t)=>{ const sp=el==='liq'&&shocked?0:0.25;
      ions.forEach((c,k)=>{ const p=(((t||0)*sp)+k/5)%1; c.setAttribute('cx',(112+p*176).toFixed(1)); c.setAttribute('opacity',(p<0.08||p>0.92)?0.3:1); });
    });
  }
};
