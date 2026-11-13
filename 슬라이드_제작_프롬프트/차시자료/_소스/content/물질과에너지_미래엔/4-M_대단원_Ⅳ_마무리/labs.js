/* 4-M 대단원 Ⅳ 마무리 — 실험실
   em49dose : 과학 글쓰기 10 — 복용 간격·약의 형태에 따른 약물의 혈중 농도 (덱 모형)
     · 한 번 먹은 약의 혈중 농도 C(t) = D·ka/(ka−ke)·(e^(−ke·t) − e^(−ka·t)), 여러 번 먹으면 더함
     · ke = ln2 / 4 h (반감기 4시간, 일차 반응처럼 줄어듦), D = 80
     · 흡수 속도 ka: 알약 0.8 /h, 가루약 3.0 /h (가루약은 표면적이 커서 빨리 녹고 흡수됨)
     · 기준 농도 30, 독성 농도 100 (상대값), 판단은 둘째 날(24–48 h)
     · 「기록」 → 표 최대 6행, 「초기화」 → 알약, 8시간 */
window.DECK_LABS = {
  em49dose(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=$('svg'), iT=$('[data-i="tau"]');
    const TAUS=[3,4,6,8,12,24], FORM=[{nm:'알약',ka:0.8},{nm:'가루약',ka:3.0}];
    const ke=Math.LN2/4, D=80, LO=30, HI=100;
    const X0=60, Y0=250, W=580, H=222, TM=48, YM=140;
    const XX=t=>X0+W*t/TM, YY=c=>Y0-H*Math.min(c,YM)/YM;
    let fi=0, log=[], cur=null, pts=[];
    // 바탕: 둘째 날 음영, 약효 구간 띠, 눈금
    API.mk('rect',{x:XX(24),y:Y0-H,width:W/2,height:H,fill:'#F4F7FA'},svg);
    API.mk('rect',{x:X0,y:YY(HI),width:W,height:YY(LO)-YY(HI),fill:'#FFE45C',opacity:.2},svg);
    [0,12,24,36,48].forEach(t=>{ const tx=API.mk('text',{x:XX(t),y:Y0+22,'text-anchor':'middle','font-size':18,fill:API.COL.muted},svg); tx.textContent=t===48?'48 h':t; });
    [0,30,100].forEach(c=>{ const tx=API.mk('text',{x:X0-8,y:YY(c)+6,'text-anchor':'end','font-size':18,fill:API.COL.muted},svg); tx.textContent=c; });
    API.mk('line',{x1:X0,y1:YY(HI),x2:X0+W,y2:YY(HI),stroke:API.COL.plus,'stroke-width':2,'stroke-dasharray':'7 5'},svg);
    API.mk('line',{x1:X0,y1:YY(LO),x2:X0+W,y2:YY(LO),stroke:API.COL.field,'stroke-width':2,'stroke-dasharray':'7 5'},svg);
    API.mk('path',{d:`M${X0} ${Y0-H-6} V${Y0} H${X0+W+8}`,stroke:API.COL.muted,'stroke-width':2,fill:'none'},svg);
    API.texText(svg,X0+8,Y0-H+4,'혈중 농도',{size:18,anchor:'start',fill:'#5B6B7F',mix:true});
    API.texText(svg,X0+W-4,YY(HI)-8,'독성',{size:18,anchor:'end',fill:'#D7263D',mix:true});
    API.texText(svg,X0+W-4,YY(LO)+22,'기준 농도',{size:18,anchor:'end',fill:'#2E7D5B',mix:true});
    API.texText(svg,XX(36),Y0-H+4,'둘째 날로 판단',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    const gd=API.mk('g',{},svg);
    const curve=API.mk('path',{fill:'none',stroke:API.COL.ink,'stroke-width':3},svg);
    const dot=API.mk('circle',{r:7,fill:API.COL.plus,stroke:'#fff','stroke-width':2},svg);
    function conc(t,tau,ka){ let s=0; for(let k=0;k*tau<=t+1e-9;k++){ const p=t-k*tau; s+=D*ka/(ka-ke)*(Math.exp(-ke*p)-Math.exp(-ka*p)); } return s; }
    function draw(){
      const tau=TAUS[+iT.value], f=FORM[fi];
      pts=[]; let mx=0, mn=1e9, on=0, tox=0;
      for(let i=0;i<=480;i++){ const t=i*0.1, c=conc(t,tau,f.ka); pts.push([t,c]);
        if(t>=24 && i<480){ mx=Math.max(mx,c); mn=Math.min(mn,c); if(c>=LO) on+=0.1; if(c>HI) tox+=0.1; } }
      curve.setAttribute('d','M'+pts.map(p=>XX(p[0]).toFixed(1)+' '+YY(p[1]).toFixed(1)).join(' L'));
      gd.innerHTML='';
      for(let t=0;t<TM;t+=tau) API.mk('path',{d:`M${XX(t).toFixed(1)} ${Y0+1} l-6 10 h12 Z`,fill:API.COL.equi},gd);
      on=Math.round(on); tox=Math.round(tox*10)/10;
      const judge= tox>0 ? '독성 위험' : (on<24 ? '약효 끊김' : '알맞음');
      cur={f:f.nm,tau,mx,mn,on,judge};
      O('tau').textContent=tau+'시간마다';
      O('n').textContent=(24/tau)+'번';
      O('mx').textContent=mx.toFixed(0); O('mn').textContent=mn.toFixed(0);
      O('on').textContent=on+'시간 / 24시간';
      O('msg').textContent=`${tau}시간마다 ${f.nm}: 둘째 날 혈중 농도 ${mn.toFixed(0)}–${mx.toFixed(0)} → `+
        (tox>0 ? `독성 농도(100)를 넘는다`+(fi? ` — 가루약은 빨리 흡수되어 최고 농도가 높다.` : ` — 너무 자주 먹었다.`) : on<24 ? `기준 농도(30) 아래로 떨어져 약효가 ${24-on}시간 끊긴다`+(fi? ` — 가루약은 일찍 최고에 이른 뒤 빨리 줄어든다.` : `.`) : `기준 농도와 독성 농도 사이에 머문다 — 알맞은 간격.`);
    }
    function place(t){ if(!pts.length) return; const i=Math.min(480,Math.floor((t*8)%48*10)); dot.setAttribute('cx',XX(pts[i][0]).toFixed(1)); dot.setAttribute('cy',YY(pts[i][1]).toFixed(1)); }
    function drawLog(){ O('log').innerHTML=log.map(r=>`<tr><td>${r.f}</td><td>${r.tau}시간</td><td>${r.mx.toFixed(0)}</td><td>${r.mn.toFixed(0)}</td><td>${r.on}시간</td><td>${r.judge}</td></tr>`).join(''); }
    function pick(i){ fi=+i; root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('em49-act',+b.dataset.s===fi)); draw(); place(0); }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>pick(b.dataset.s)));
    iT.addEventListener('input',()=>{ draw(); place(0); });
    $('[data-act="rec"]').addEventListener('click',()=>{ draw(); log.push(cur); if(log.length>6) log.shift(); drawLog(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; drawLog(); iT.value=3; pick(0); });
    API.onShow&&API.onShow(()=>{ draw(); place(0); });
    draw(); drawLog(); place(0);
    API.loop(root,(dt,t)=>place(t));
  }
};
