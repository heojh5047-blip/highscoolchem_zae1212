/* 2-M 대단원 Ⅱ 마무리 — 실험실
   em29cool : 과학 글쓰기 11 — 부동액(에틸렌 글리콜) 양에 따른 냉각수의 어는점·끓는점
     · n = w/62 (mol), m = n / 1.00 kg, ΔTf = 1.86 m, ΔTb = 0.51 m (묽은 용액 식 — 어림값)
     · 판정: 어는점 < 최저 기온 → 얼지 않음, 아니면 얼 위험
     · 「기록」 → 표 최대 5행, 「초기화」 → 310 g, −15 °C */
window.DECK_LABS = {
  em29cool(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=$('svg'), iW=$('[data-i="w"]'), iT=$('[data-i="tm"]');
    const KB=0.51, KF=1.86, MM=62;
    let log=[], cur=null;
    const f1=v=>{ const r=Math.round(v*10+(v>=0?1e-6:-1e-6))/10; return (r===0?0:r).toFixed(1); };
    // ── 냉각수 상자 (왼쪽) ──
    const BX0=24, BX1=264, BY0=40, BY1=270;
    API.mk('rect',{x:BX0,y:BY0,width:BX1-BX0,height:BY1-BY0,rx:10,fill:'#DDEEF8',stroke:'#9FC3DD','stroke-width':3},svg);
    API.texText(svg,(BX0+BX1)/2,26,'냉각수 (물 1 kg + 부동액)',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    let seed=7; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    const pos=()=>({x:BX0+16+rnd()*(BX1-BX0-32), y:BY0+16+rnd()*(BY1-BY0-32), ph:rnd()*6.28});
    const gp=API.mk('g',{},svg);
    const water=Array.from({length:44},()=>{ const p=pos(); p.c=API.mk('circle',{r:6,fill:'#5DA9E9'},gp); return p; });
    const gly=Array.from({length:40},()=>{ const p=pos(); p.c=API.mk('circle',{r:9,fill:'#5FBF7F',stroke:'#2E9E6A','stroke-width':2},gp); return p; });
    API.mk('circle',{cx:40,cy:290,r:6,fill:'#5DA9E9'},svg); API.texText(svg,52,296,'물 분자',{size:18,mix:true});
    API.mk('circle',{cx:140,cy:290,r:8,fill:'#5FBF7F',stroke:'#2E9E6A','stroke-width':2},svg); API.texText(svg,154,296,'에틸렌 글리콜',{size:18,mix:true});
    // ── 온도 막대 (오른쪽) ──
    const AX=344, T0=-35, T1=110, YB=280, YT=34, ty=t=>YB-(t-T0)*(YB-YT)/(T1-T0);
    const ga=API.mk('g',{},svg);
    API.mk('line',{x1:AX,y1:YB,x2:AX,y2:YT-6,stroke:'#5B6B7F','stroke-width':2},ga);
    [-30,0,50,100].forEach(v=>{ API.mk('line',{x1:AX-6,y1:ty(v),x2:AX,y2:ty(v),stroke:'#5B6B7F','stroke-width':1.5},ga);
      API.mk('line',{x1:AX,y1:ty(v),x2:640,y2:ty(v),stroke:'#E2E7EC','stroke-width':1.5},ga);
      API.texText(svg,AX-10,ty(v)+6,String(v),{size:18,anchor:'end',mix:true}); });
    API.texText(svg,AX+8,22,'온도 [°C]',{size:18,anchor:'start',fill:'#5B6B7F',mix:true});
    API.mk('rect',{x:366,y:ty(100),width:80,height:ty(0)-ty(100),rx:5,fill:'#FFFFFF',stroke:'#1F6FD1','stroke-width':2.5,'stroke-dasharray':'7 5'},svg);
    API.texText(svg,406,ty(56),'순수한||물',{size:18,anchor:'middle',fill:'#1F6FD1',mix:true});
    const bar=API.mk('rect',{x:470,width:60,rx:5,fill:'#E3F4E8',stroke:'#2E9E6A','stroke-width':3},svg);
    const capB=API.mk('rect',{x:470,width:60,fill:'#F8C9CF'},svg), capF=API.mk('rect',{x:470,width:60,fill:'#C9DDF6'},svg);
    API.texText(svg,500,ty(40),'냉각수',{size:18,anchor:'middle',mix:true});
    const tmL=API.mk('line',{x1:AX,x2:640,stroke:'#1F6FD1','stroke-width':3,'stroke-dasharray':'9 6'},svg);
    const ovTb=$('[data-ov="tb"]'), ovTf=$('[data-ov="tf"]'), ovTm=$('[data-ov="tm"]');
    function draw(){
      const w=+iW.value, tm=+iT.value, n=w/MM, m=n/1.00, tf=-KF*m, tb=100+KB*m;
      O('w').textContent=w+' g'; O('tm').textContent=tm+' °C';
      O('m').textContent=m.toFixed(2)+' m'; O('tf').textContent=f1(tf)+' °C'; O('tb').textContent=f1(tb)+' °C';
      const yb=ty(Math.min(tb,T1)), yf=ty(Math.max(tf,T0));
      bar.setAttribute('y',yb.toFixed(1)); bar.setAttribute('height',(yf-yb).toFixed(1));
      capB.setAttribute('y',yb.toFixed(1)); capB.setAttribute('height',Math.max(0,ty(100)-yb).toFixed(1));
      capF.setAttribute('y',ty(0).toFixed(1)); capF.setAttribute('height',Math.max(0,yf-ty(0)).toFixed(1));
      tmL.setAttribute('y1',ty(tm)); tmL.setAttribute('y2',ty(tm));
      ovTb.textContent='끓는점 '+f1(tb); API.place(ovTb,590,yb-2,true);
      ovTf.textContent='어는점 '+f1(tf); API.place(ovTf,590,Math.min(yf+14,YB+4),true);
      ovTm.textContent='최저 기온 '+tm; API.place(ovTm,406,Math.min(ty(tm)+20,292),true);
      const k=Math.round(Math.min(40,w/20)); gly.forEach((p,i)=>p.c.setAttribute('opacity',i<k?1:0));
      const ok=tf<tm-1e-9;
      O('msg').textContent= ok ? `어는점 ${f1(tf)} °C < 최저 기온 ${tm} °C — 얼지 않음 (여유 ${f1(tm-tf)} °C)`
                               : `어는점 ${f1(tf)} °C ≥ 최저 기온 ${tm} °C — 얼 위험, 부동액을 더 넣자`;
      cur={w,m,tf,tb,tm,j:ok?'얼지 않음':'얼 위험'};
    }
    function drawLog(){ O('log').innerHTML=log.map(r=>`<tr><td>${r.w}</td><td>${r.m.toFixed(2)}</td><td>${f1(r.tf)}</td><td>${f1(r.tb)}</td><td>${r.tm}</td><td>${r.j}</td></tr>`).join(''); }
    function season(v){ iT.value=v; root.querySelectorAll('[data-season]').forEach(b=>b.classList.toggle('em29-act',+b.dataset.season===+v)); draw(); }
    root.querySelectorAll('[data-season]').forEach(b=>b.addEventListener('click',()=>season(b.dataset.season)));
    iW.addEventListener('input',draw);
    iT.addEventListener('input',()=>season(iT.value));
    $('[data-act="rec"]').addEventListener('click',()=>{ draw(); log.push(cur); if(log.length>5) log.shift(); drawLog(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; drawLog(); iW.value=310; season(-15); });
    API.onShow&&API.onShow(draw);
    draw(); drawLog();
    function place(t){ [...water,...gly].forEach((p,i)=>{ const a=t*2.2+p.ph; p.c.setAttribute('cx',(p.x+3*Math.sin(a)).toFixed(1)); p.c.setAttribute('cy',(p.y+3*Math.cos(a*1.3)).toFixed(1)); }); }
    place(0);
    API.loop(root,(dt,t)=>place(t));
  }
};
