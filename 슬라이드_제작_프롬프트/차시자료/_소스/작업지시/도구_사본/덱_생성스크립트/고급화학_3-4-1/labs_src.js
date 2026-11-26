/* 고급화학 3-4-1a 화학 전지의 개요 — 실험실
   ac341bridge : 다니엘 전지 조립하기 — 염다리의 작용 실험 설계와 실험 (필수 탐구 고화-탐25, 교과서 168쪽)
     · 염다리 있음/없음, 재질(거름종이·면실·한천 젤 U자관), 염다리 속 KNO3 농도(증류수·0.1 M·1.0 M·포화 약 3 M),
       [Zn2+]·[Cu2+] 1.0–0.0010 M(10배씩)
     · 기전력 E = 1.10 − (0.0592/2)·log([Zn2+]/[Cu2+]) V (염다리 없으면 회로가 끊겨 0) — 농도 효과의 까닭은 (2)의 심화(네른스트 식)
     · 내부 저항 r = 염다리 저항(재질 상수 k / KNO3 농도) + 용액 저항(2/[Zn2+] + 2/[Cu2+]) + 2 Ω
       k: 거름종이 60, 면실 400, 한천 젤 U자관 20 (Ω·M) — 모형 값
     · 전압계(입력 저항 10 MΩ) 값 = E·10 MΩ/(10 MΩ + r) + 작은 측정 오차(설정마다 고정)
       부하 100 Ω: 전류 I = E/(100 + r), 부하 전압 = 100·I
     · 그림: 전자(도선, Zn → Cu)와 염다리 이온(음이온 → Zn 쪽, 양이온 → Cu 쪽)이 전류에 비례한 빠르기로 움직임
     · 「측정·기록」→ 표에 행이 쌓이고(최근 5행) 전류 막대, 서로 다른 설정 3가지 이상이면 결론 문장 · 「초기화」 */
window.DECK_LABS = {
  ac341bridge(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const CONC=[0.0010,0.010,0.10,1.0], CS=['0.0010 M','0.010 M','0.10 M','1.0 M'];
    const BC=[1e-5,0.1,1.0,3.0], BN=['증류수','0.1 M','1.0 M','포화'];
    const MK={paper:60,thread:400,gel:20}, MN={paper:'거름종이',thread:'면실',gel:'한천 젤'};
    let br=1, mat='paper', bc=2, log=[];
    const svg=$('svg'), gd=API.mk('g',{},svg), ge=API.mk('g',{},svg);
    const edots=[], adots=[], cdots=[];
    for(let i=0;i<10;i++) edots.push(API.mk('circle',{r:5,fill:API.COL.minus},ge));
    for(let i=0;i<4;i++){ adots.push(API.mk('circle',{r:6,fill:'#DCE9FA',stroke:API.COL.minus,'stroke-width':2},ge)); cdots.push(API.mk('circle',{r:6,fill:'#FFE4E7',stroke:API.COL.plus,'stroke-width':2},ge)); }
    const cL=90, cR=450, bx1=150, bx2=390, btop=96, bbot=214;
    const BLEN=(bbot-btop)*2+(bx2-bx1), WLEN=50+(cR-cL)+50;
    let st={I:0,flow:false};
    const f2=x=>x.toFixed(2);
    const fr=r=> r>=1e6? (r/1e6).toFixed(1)+' MΩ' : r>=1e3? (r/1e3).toFixed(1)+' kΩ' : Math.round(r)+' Ω';
    function model(){
      const iz=+$('[data-i="zn"]').value, ic=+$('[data-i="cu"]').value, cz=CONC[iz], cc=CONC[ic];
      const E0=1.10-0.0296*Math.log10(cz/cc);
      const rb= br? MK[mat]/BC[bc] : Infinity;
      const r = rb + 2/cz + 2/cc + 2;
      const E = br? E0 : 0;
      const h=[...(String(br)+mat+bc+iz+ic)].reduce((s,c)=>(s*31+c.charCodeAt(0))%9973,7);
      const noise=E>0?((h%9)-4)/1000:0;
      const Vm = br? Math.max(0,E*1e7/(1e7+r)+noise) : 0;
      const I = br? E/(100+r)*1000*(1+((h%7)-3)/100) : 0;   // mA
      const VL = I/1000*100;
      return {iz,ic,cz,cc,E0,E,r,Vm,I,VL};
    }
    function bpath(D){
      if(!br) return;
      const p=`M${bx1} ${bbot} V${btop} H${bx2} V${bbot}`;
      if(mat==='gel'){ D('path',{d:p,fill:'none',stroke:'#7E8B98','stroke-width':26}); D('path',{d:p,fill:'none',stroke:'#F6F0E0','stroke-width':20}); }
      else if(mat==='paper'){ D('path',{d:p,fill:'none',stroke:'#C8B98F','stroke-width':11}); D('path',{d:p,fill:'none',stroke:bc? '#F3EBD3':'#FBF8EF','stroke-width':6}); }
      else { D('path',{d:p,fill:'none',stroke:'#B9A98A','stroke-width':4}); D('path',{d:p,fill:'none',stroke:'#FFFFFF','stroke-width':1.5}); }
    }
    function draw(){
      const m=model();
      while(gd.firstChild) gd.firstChild.remove();
      const D=(t,a)=>API.mk(t,a,gd);
      D('rect',{x:32,y:140,width:146,height:98,fill:'#DDEEF8'});
      D('rect',{x:362,y:140,width:146,height:98,fill:'#3E8ED0','fill-opacity':0.06+0.09*m.ic});
      [30,360].forEach(x0=>D('path',{d:`M${x0-5} 110 H${x0} V232 Q${x0} 240 ${x0+8} 240 H${x0+142} Q${x0+150} 240 ${x0+150} 232 V110 H${x0+155}`,fill:'none',stroke:'#7E8B98','stroke-width':3,'stroke-linejoin':'round'}));
      bpath(D);
      D('rect',{x:cL-12,y:80,width:24,height:140,rx:3,fill:'#C9D3DD',stroke:'#7E8B98','stroke-width':2});
      D('rect',{x:cR-12,y:80,width:24,height:140,rx:3,fill:'#E6C29C',stroke:'#B0835A','stroke-width':2});
      D('path',{d:`M${cL} 80 V30 H236 M304 30 H${cR} V80`,fill:'none',stroke:API.COL.ink,'stroke-width':3});
      D('rect',{x:236,y:8,width:68,height:44,rx:8,fill:'#FFFFFF',stroke:API.COL.ink,'stroke-width':3});
      st={I:m.I,flow:m.I>0.05};
      if(st.flow){ API.arrow(gd,140,16,200,16,API.COL.minus,3); API.arrow(gd,340,16,400,16,API.COL.minus,3); API.place(V('e1'),120,16); } else API.place(V('e1'),0,0,false);
      V('sL').innerHTML=API.tex(CS[m.iz].replace(' M','\\ \\text{M}\\ ')+'\\ce{ZnSO4}');
      V('sR').innerHTML=API.tex(CS[m.ic].replace(' M','\\ \\text{M}\\ ')+'\\ce{CuSO4}');
      API.place(V('mL'),cL-34,92); API.place(V('mR'),cR+34,92);
      API.place(V('sL'),105,224); API.place(V('sR'),435,224);
      API.place(V('pL'),105,262); API.place(V('pR'),435,262);
      API.place(V('ia'),270,136,!!br); API.place(V('ic'),270,166,!!br);
      V('vm').textContent=f2(m.Vm)+' V'; API.place(V('vm'),270,30);
      O('zn').textContent=CS[m.iz]; O('cu').textContent=CS[m.ic];
      O('v').textContent=f2(m.Vm)+' V'; O('i').textContent=m.I.toFixed(1)+' mA';
      O('r').textContent= br? fr(m.r) : '∞ (끊김)'; O('vl').textContent=f2(m.VL)+' V';
      let msg;
      if(!br) msg='염다리가 없어 이온이 지나갈 길이 없다 — 회로가 끊겨 전압계 0 V, 전류 0이다.';
      else if(bc===0) msg=`증류수만 적신 염다리는 이온이 거의 없어 내부 저항이 매우 크다(${fr(m.r)}). 전압계 값도 작고, 부하에는 전류가 거의 흐르지 않는다.`;
      else {
        msg=`내부 저항 ${fr(m.r)} → 전류 ${m.I.toFixed(1)} mA. 염다리 이온이 진하고 통로가 넓을수록 저항이 작아 전류가 크다. 전압계 값은 기전력 ${f2(m.E)} V와 거의 같다.`;
        if(m.iz!==3||m.ic!==3) msg+=' 이온 농도를 바꾸면 전압계 값이 조금 달라진다 — 까닭은 (2) 전지 전위의 심화(네른스트 식).';
      }
      if(!O('msg').dataset.keep) O('msg').textContent=msg;
      root.querySelectorAll('[data-s]').forEach(x=>x.classList.toggle('on',x.dataset.s===String(br)));
      root.querySelectorAll('[data-m]').forEach(x=>x.classList.toggle('on',x.dataset.m===mat));
      root.querySelectorAll('[data-c]').forEach(x=>x.classList.toggle('on',+x.dataset.c===bc));
      tick(window.__STILL?0:performance.now()/1000);
    }
    function bpt(s){ // 염다리 경로 위 점: s=0 왼쪽 아래 → BLEN 오른쪽 아래
      const h=bbot-btop;
      if(s<h) return [bx1,bbot-s];
      if(s<h+(bx2-bx1)) return [bx1+(s-h),btop];
      return [bx2,btop+(s-h-(bx2-bx1))];
    }
    function tick(t){
      const sp=Math.min(60,6+st.I*6);
      edots.forEach((c,i)=>{
        if(!st.flow){ c.setAttribute('opacity',0); return; }
        let s=((i*(WLEN/10)+t*sp)%WLEN), x,y;
        if(s<50){ x=cL; y=80-s; } else if(s<50+(cR-cL)){ x=cL+(s-50); y=30; } else { x=cR; y=30+(s-50-(cR-cL)); }
        c.setAttribute('cx',x); c.setAttribute('cy',y); c.setAttribute('opacity',(y===30&&x>236&&x<304)?0:1); });
      const show=br&&st.flow;
      adots.forEach((c,i)=>{ if(!show){ c.setAttribute('opacity',0); return; }
        const s=BLEN-((i*BLEN/4+t*sp*0.6)%BLEN), [x,y]=bpt(s); c.setAttribute('cx',x); c.setAttribute('cy',y); c.setAttribute('opacity',1); });
      cdots.forEach((c,i)=>{ if(!show){ c.setAttribute('opacity',0); return; }
        const s=((i*BLEN/4+BLEN/8+t*sp*0.6)%BLEN), [x,y]=bpt(s); c.setAttribute('cx',x); c.setAttribute('cy',y); c.setAttribute('opacity',1); });
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-5).forEach(r=>{ const tr=document.createElement('tr');
        const w=Math.round(Math.min(1,r.I/12)*80);
        tr.innerHTML=`<td>${r.n}</td><td>${r.b}</td><td>${r.c}</td><td>${r.zn}</td><td>${r.cu}</td><td>${f2(r.v)}</td><td>${r.I.toFixed(1)}</td><td class="l"><span class="ac341-bar" style="width:${w}px"></span></td>`; tb.appendChild(tr); }); }
    const on=(sel,fn)=>root.querySelectorAll(sel).forEach(x=>x.addEventListener('click',()=>{ fn(x); delete O('msg').dataset.keep; draw(); }));
    on('[data-s]',x=>br=+x.dataset.s); on('[data-m]',x=>mat=x.dataset.m); on('[data-c]',x=>bc=+x.dataset.c);
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',()=>{ delete O('msg').dataset.keep; draw(); }));
    $('[data-act="rec"]').addEventListener('click',()=>{
      const m=model();
      log.push({n:log.length+1,b:br?MN[mat]:'없음',c:br?BN[bc]:'—',zn:CS[m.iz],cu:CS[m.ic],v:m.Vm,I:m.I,key:br?(mat+bc+m.iz+m.ic):('x'+m.iz+m.ic)});
      renderLog();
      const n=new Set(log.map(r=>r.key)).size, best=log.reduce((a,b)=>b.I>a.I?b:a), msg=O('msg');
      msg.textContent = n>=3 ? `기록 ${n}가지: 전류가 가장 큰 것은 ${best.b}·${best.c}(${best.I.toFixed(1)} mA). 결론 — 염다리가 있어야 작동하고, 이온 농도가 높고 이온이 잘 지나는 염다리일수록 전지 성능(전류)이 크다.`
                           : `기록 ${n}가지 — 한 번에 한 변인만 바꾸어 더 측정해 보자 (${n}/3).`;
      msg.dataset.keep='1'; });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); br=1; mat='paper'; bc=2; $('[data-i="zn"]').value=3; $('[data-i="cu"]').value=3; delete O('msg').dataset.keep; draw(); });
    API.onShow&&API.onShow(()=>draw());
    API.ready&&API.ready(()=>draw());
    draw();
    if(!window.__STILL) API.loop(root,()=>tick(performance.now()/1000));
  }
};
