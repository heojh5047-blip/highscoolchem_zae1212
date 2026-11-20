/* 1-M 대단원 Ⅰ 마무리 — 실험실
   cm19caco3 : 과학 역량 키우기 12 실험 설계하기 — 탄산 칼슘의 질량을 바꾸며 반응 전후 질량 감소(= CO2 질량) 재기
     · 탄산 칼슘 0.5–5.0 g (몰질량 100 g/mol), 묽은 염산 100 mL는 0.1 몰까지 충분 (덱 범위 0.05 몰)
     · m1 = 플라스크+염산 152.30 g + 시약포지 0.45 g + w, 질량 감소 = 44 n (1 ± 1.5 % 고정 시드), 「기포가 멈추기 전」 ×0.85
     · 「반응시키고 측정」 → 저울 숫자가 m1에서 m2로 줄고 기포가 오름, 표(최대 6행) 누적, 그래프 n(CaCO3)–n(CO2) 점 · 이론선 기울기 1
     · 「초기화」 */
window.DECK_LABS = {
  cm19caco3(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=$('svg'), BASE=152.30+0.45;
    let log=[], seed=19, run=null, last=null;
    const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    // ── 저울과 플라스크 ──
    const g=API.mk('g',{},svg);
    API.mk('rect',{x:20,y:200,width:220,height:36,rx:8,fill:'#C9D3DD',stroke:'#7E8B98','stroke-width':2.5},g);
    API.mk("rect",{x:66,y:202,width:128,height:30,rx:4,fill:"#16233D"},g);
    API.mk('rect',{x:40,y:192,width:180,height:8,rx:3,fill:'#9AA5B1'},g);
    API.mk('path',{d:'M112 60 V96 L58 186 Q54 192 62 192 H198 Q206 192 202 186 L148 96 V60',fill:'#F7FAFC',stroke:'#7E8B98','stroke-width':3.5,'stroke-linejoin':'round'},g);
    API.mk('path',{d:'M84 146 H176 L201 186 Q204 191 197 191 H63 Q56 191 59 186 Z',fill:'#EEF6FB'},g);
    API.mk('line',{x1:84,y1:146,x2:176,y2:146,stroke:'#9FC3DD','stroke-width':2},g);
    const powder=API.mk('ellipse',{cx:130,cy:186,rx:20,ry:4,fill:'#F4F1EA',stroke:'#B9AD8E','stroke-width':2},g);
    const bub=API.mk('g',{},g);
    const BB=[[104,0,4],[122,.25,5],[140,.5,4],[156,.75,5],[130,.4,3.5]].map(([x,ph,r])=>({x,ph,c:API.mk('circle',{cx:x,cy:180,r,fill:'#FFFFFF','fill-opacity':.8,stroke:'#7FB6D9','stroke-width':1.8,opacity:0},bub)}));
    API.texText(svg,130,52,'묽은 염산 100 mL',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    // ── 그래프 ──
    const GX0=360, GX1=630, GY0=200, GYT=30, NX=0.05;
    const gx=n=>GX0+(GX1-GX0)*n/NX, gy=n=>GY0-(GY0-GYT)*n/NX;
    const ga=API.mk('g',{},svg);
    [0.025,0.05].forEach(v=>{ API.mk('line',{x1:GX0,y1:gy(v),x2:GX1,y2:gy(v),stroke:'#E2E7EC','stroke-width':1.5},ga);
      API.texText(svg,GX0-6,gy(v)+6,String(v),{size:18,anchor:'end',fill:'#5B6B7F',mix:true});
      API.mk('line',{x1:gx(v),y1:GY0,x2:gx(v),y2:GY0+5,stroke:'#5B6B7F','stroke-width':1.6},ga);
      API.texText(svg,gx(v),GY0+24,String(v),{size:18,anchor:'middle',fill:'#5B6B7F',mix:true}); });
    API.arrow(ga,GX0,GY0,GX1+14,GY0,'muted',2); API.arrow(ga,GX0,GY0,GX0,GYT-14,'muted',2);
    API.mk('path',{d:`M${GX0} ${GY0} L${gx(0.05)} ${gy(0.05)}`,stroke:'#5B6B7F','stroke-width':2,'stroke-dasharray':'6 5',fill:'none'},ga);
    API.texText(svg,GX0+8,GYT-6,'$\\ce{CO2}$의 양 [mol]',{size:18,anchor:'start',mix:true});
    API.texText(svg,GX1+14,GY0+46,'$\\ce{CaCO3}$의 양 [mol]',{size:18,anchor:'end',mix:true});
    API.texText(svg,gx(0.05)-4,gy(0.05)+30,'1 : 1',{size:18,anchor:'end',fill:'#5B6B7F',mix:true});
    const gp=API.mk('g',{},svg);
    // ── 계산 ──
    const w=()=>+$('[data-i="w"]').value/10;
    const early=()=>$('[data-e="early"]').checked;
    const bal=$('[data-ov="bal"]');
    function setBal(v){ bal.textContent=v.toFixed(2)+' g'; API.place(bal,130,204); }
    function info(){
      const m=w(), n=m/100;
      O('w').textContent=m.toFixed(1)+' g';
      O('n').textContent=n.toFixed(3)+' mol';
      if(!run) { O('m').textContent=(BASE+m).toFixed(2)+' g → ?'; setBal(BASE+m); }
    }
    function drawLog(){
      O('log').innerHTML=log.map((r,i)=>`<tr><td>${i+1}</td><td>${r.w.toFixed(1)}</td><td>${r.n.toFixed(3)}</td><td>${r.d.toFixed(2)}</td><td>${(r.d/44).toFixed(4)}</td><td>1 : ${(r.d/44/r.n).toFixed(2)}</td></tr>`).join('');
      while(gp.firstChild) gp.removeChild(gp.firstChild);
      log.forEach(r=>{ const e=r.early;
        API.mk('circle',{cx:gx(r.n),cy:gy(r.d/44),r:6,fill:e?'#FFFFFF':'#16233D',stroke:e?'#E08A2C':'#16233D','stroke-width':2.5},gp); });
    }
    function doRun(){
      if(run) return;
      const m=w(), n=m/100, e=early();
      const d=44*n*(1+(rnd()*2-1)*0.015)*(e?0.85:1);
      run={t:0,m1:BASE+m,m2:BASE+m-d}; last={w:m,n,d,early:e};
      O('msg').textContent='반응 중… 기포가 생긴다.';
    }
    function finish(){
      const r=last; log.push(r); if(log.length>6) log.shift(); drawLog();
      O('m').textContent=`${(BASE+r.w).toFixed(2)} → ${(BASE+r.w-r.d).toFixed(2)} g`;
      const ratio=r.d/44/r.n;
      O('msg').textContent=r.early?`몰비 1 : ${ratio.toFixed(2)} — 질량 감소가 작게 측정됨. 기포가 다 빠진 뒤에 재야 한다.`
        : (Math.abs(ratio-1)<=0.03?`몰비 1 : ${ratio.toFixed(2)} ≈ 1 : 1 — 계수비와 같다(가설과 일치).`:`몰비 1 : ${ratio.toFixed(2)} — 반복 측정해 평균을 내 보자.`);
      run=null;
    }
    root.querySelector('[data-act="run"]').addEventListener('click',doRun);
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; run=null; seed=19; drawLog(); O('msg').textContent='탄산 칼슘의 질량을 고르고 측정해 보자.'; BB.forEach(b=>b.c.setAttribute('opacity',0)); info(); });
    $('[data-i="w"]').addEventListener('input',()=>{ if(!run) info(); });
    O('msg').textContent='탄산 칼슘의 질량을 고르고 측정해 보자.';
    API.onShow&&API.onShow(info);
    info(); drawLog();
    API.loop(root,(dt)=>{
      if(!run) return;
      run.t+=dt; const k=Math.min(1,run.t/1.6);
      setBal(run.m1+(run.m2-run.m1)*k);
      powder.setAttribute('rx',(20*(1-k)+2).toFixed(1));
      BB.forEach(b=>{ const p=(run.t*1.2+b.ph)%1; b.c.setAttribute('cy',(186-40*p).toFixed(1)); b.c.setAttribute('opacity',k<1?(1-p).toFixed(2):0); });
      if(k>=1){ BB.forEach(b=>b.c.setAttribute('opacity',0)); powder.setAttribute('rx',20); finish(); }
    });
  }
};
