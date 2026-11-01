/* 3-1 화학 반응과 엔탈피 — 실험실 (필수 탐구 물03-탐1 「대체 연료와 화석 연료의 효율성을 비교하는 탐구하기」)
   em31fuel  : 연료(메탄올·에탄올·뷰테인)를 태워 캔 속 물을 가열 → 온도 변화·연료 감소 질량 측정 → q = c m Δt,
               1 g당·1 mol당 열. 열 전달 비율 f = 바람막이 0.42 / 없음 0.26 (× 1 ± 0.04 고정 시드), 연소 빠르기(g/min)
               메탄올 0.30, 에탄올 0.28, 뷰테인 0.35 (× 1 ± 0.03). 「기록」 → 표 누적(최근 5행), 통제 변인 검사.
   em31chart : em31fuel 기록(window.__em31log)의 연료별 평균과 자료값(수소·메테인·옥테인 포함)을 막대그래프로 비교.
               단위: 1 g당 열(kJ/g) / 1 mol당 열(kJ/mol) / 같은 열 1000 kJ을 얻을 때 이산화 탄소(g).
   자료값(연소 엔탈피, kJ/mol): H2 286, CH4 890, C4H10 2878, C8H18 5470, CH3OH 726, C2H5OH 1367. 물의 비열 4.18 J/(g·°C). */
(function(){
const FUEL={
  H2:{name:'수소',tex:'\\ce{H2}',M:2,H:286,nC:0,alt:true},
  CH3OH:{name:'메탄올',tex:'\\ce{CH3OH}',M:32,H:726,nC:1,alt:true,rate:.30},
  C2H5OH:{name:'에탄올',tex:'\\ce{C2H5OH}',M:46,H:1367,nC:2,alt:true,rate:.28},
  CH4:{name:'메테인',tex:'\\ce{CH4}',M:16,H:890,nC:1,alt:false},
  C4H10:{name:'뷰테인',tex:'\\ce{C4H10}',M:58,H:2878,nC:4,alt:false,rate:.35},
  C8H18:{name:'옥테인',tex:'\\ce{C8H18}',M:114,H:5470,nC:8,alt:false}
};
const ORDER=['H2','CH3OH','C2H5OH','CH4','C4H10','C8H18'];
const C_W=4.18;
if(!window.__em31log) window.__em31log=[];
const fmt=(v,d)=>v.toFixed(d);
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=a; t=Math.imul(t^(t>>>15),t|1); t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; }; }

window.DECK_LABS = {
  em31fuel(root, API){
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), Ov=k=>$(`[data-ov="${k}"]`), I=k=>$(`[data-i="${k}"]`);
    const svg=$('svg'), g=API.mk('g',{},svg);
    let st={f:'CH3OH', trial:0, res:null, anim:1};
    const log=window.__em31log;

    function settings(){ return {w:+I('w').value, t:+I('t').value, ws:I('ws').checked}; }
    function run(){
      const s=settings(), F=FUEL[st.f], r=rng(1000+st.trial*7919+ORDER.indexOf(st.f)*131); st.trial++;
      const T0=Math.round((19.6+0.8*r())*10)/10;
      const dm=Math.round(F.rate*s.t*(1+0.06*(r()-.5))*100)/100;
      const f=(s.ws?.42:.26)*(1+0.08*(r()-.5));
      const qTrue=dm*F.H/F.M*f;                    // kJ, 물이 실제로 얻은 열
      const dt=Math.round(qTrue*1000/(C_W*s.w)*10)/10;
      const m0=Math.round((150+40*r())*100)/100;
      const q=C_W*s.w*dt/1000, perG=q/dm, perMol=perG*F.M;
      st.res={...s,f:st.f,T0,T1:Math.round((T0+dt)*10)/10,dt,dm,m0,m1:Math.round((m0-dm)*100)/100,q,perG,perMol,boil:T0+dt>95};
      st.anim=window.__STILL?1:0; show(); draw();
    }
    function show(){
      const s=settings(); O('w').textContent=s.w+' g'; O('t').textContent=s.t+'분';
      root.querySelectorAll('[data-f]').forEach(b=>b.classList.toggle('on',b.dataset.f===st.f));
      const F=FUEL[st.f]; Ov('f').innerHTML=API.tex(F.tex)+' <span style="font-size:19px;font-weight:400;color:#5B6B7F">'+F.name+(F.alt?' · 대체 연료':' · 화석 연료')+'</span>'; API.place(Ov('f'),300,6);
      const R=st.res;
      if(!R){ O('T').textContent='—'; O('dm').textContent='—'; O('q').textContent='—'; O('per').textContent='—';
        O('msg').textContent='연료와 조건을 정하고 「실험하기」를 누르자.'; return; }
      if(R.boil){ O('T').textContent=fmt(R.T0,1)+' → 95 °C 넘음'; O('dm').textContent='—'; O('q').textContent='—'; O('per').textContent='—';
        O('msg').textContent='물이 끓기 전에 멈추자 — 가열 시간을 줄이거나 물을 늘리자. (기록되지 않음)'; return; }
      O('T').textContent=`${fmt(R.T0,1)} → ${fmt(R.T1,1)} °C (Δt ${fmt(R.dt,1)})`;
      O('dm').textContent=`${fmt(R.m0,2)} → ${fmt(R.m1,2)} g (${fmt(R.dm,2)} g)`;
      O('q').textContent=`${fmt(R.q,2)} kJ`;
      O('per').textContent=`${fmt(R.perG,1)} kJ/g · ${Math.round(R.perMol)} kJ/mol`;
      const lit=F.H/F.M, pc=Math.round(R.perG/lit*100);
      O('msg').textContent=`자료값은 ${fmt(lit,1)} kJ/g — 측정값은 자료값의 약 ${pc} %이다. `+(R.ws?'열의 일부가 공기·캔으로 빠져나갔다.':'바람막이가 없어 열 손실이 더 크다.');
    }
    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      const R=st.res, k=R&&!R.boil? st.anim:0, burning=R&&!R.boil&&st.anim<1;
      const T=R? (R.boil? R.T0 : R.T0+R.dt*k) : 20, s=settings();
      const mk=(t,a)=>API.mk(t,a,g);
      // 스탠드
      mk('line',{x1:40,y1:30,x2:40,y2:236,stroke:'#7E8B98','stroke-width':6}); mk('rect',{x:16,y:236,width:150,height:10,rx:3,fill:'#7E8B98'});
      mk('line',{x1:40,y1:72,x2:110,y2:72,stroke:'#7E8B98','stroke-width':5});
      // 캔과 물 (물 높이 ∝ 질량)
      mk('rect',{x:110,y:50,width:110,height:90,rx:8,fill:'#D5DCE3',stroke:'#7E8B98','stroke-width':2.5});
      const wh=20+50*(s.w-100)/200; mk('rect',{x:114,y:136-wh,width:102,height:wh,rx:4,fill:'#DDEEF8'});
      // 온도계
      const tx=196; mk('rect',{x:tx-6,y:14,width:12,height:118,rx:6,fill:'#fff',stroke:'#7E8B98','stroke-width':2});
      const lv=Math.max(0,Math.min(1,T/100)); mk('rect',{x:tx-3,y:128-104*lv,width:6,height:104*lv+4,fill:'#E0664F'}); mk('circle',{cx:tx,cy:134,r:8,fill:'#E0664F'});
      // 바람막이
      if(s.ws){ mk('rect',{x:92,y:150,width:9,height:86,fill:'#C9D3DD',stroke:'#9FB0C2'}); mk('rect',{x:229,y:150,width:9,height:86,fill:'#C9D3DD',stroke:'#9FB0C2'}); }
      // 연료 (램프 또는 버너)
      const cx=165;
      if(st.f==='C4H10'){ mk('rect',{x:cx-24,y:196,width:48,height:40,rx:6,fill:'#E9EEF3',stroke:'#7E8B98','stroke-width':2.5}); mk('rect',{x:cx-6,y:180,width:12,height:16,fill:'#7E8B98'}); }
      else { mk('path',{d:`M${cx-22} 198 L${cx+22} 198 L${cx+32} 236 L${cx-32} 236 Z`,fill:'#EEF5FB',stroke:'#7E8B98','stroke-width':2.5});
        mk('path',{d:`M${cx-27} 218 L${cx+27} 218 L${cx+32} 236 L${cx-32} 236 Z`,fill:'#DDEEF8'}); mk('line',{x1:cx,y1:184,x2:cx,y2:198,stroke:'#5B6B7F','stroke-width':3}); }
      if(burning){ const fl=1+0.08*Math.sin(Date.now()/90);
        mk('path',{d:`M${cx} ${182} C${cx-14} ${172} ${cx-12} ${160-10*fl} ${cx} ${146-6*fl} C${cx+12} ${160-10*fl} ${cx+14} ${172} ${cx} ${182} Z`,fill:'#F6A623'});
        mk('path',{d:`M${cx} ${180} C${cx-7} ${174} ${cx-6} ${166} ${cx} ${158} C${cx+6} ${166} ${cx+7} ${174} ${cx} ${180} Z`,fill:'#FFD45C'}); }
      // 표시판
      mk('rect',{x:300,y:70,width:220,height:60,rx:10,fill:'#16233D'}); mk('rect',{x:300,y:166,width:220,height:60,rx:10,fill:'#16233D'});
      const mass=R&&!R.boil? R.m0-R.dm*k : (R? R.m0:null);
      Ov('th').textContent=fmt(T,1)+' °C'; Ov('bal').textContent= mass==null?'— g':fmt(mass,2)+' g';
      Ov('th').style.color='#FFE45C'; Ov('bal').style.color='#9BE3B8';
      API.place(Ov('th'),410,100); API.place(Ov('bal'),410,196); API.place(Ov('thl'),410,56); API.place(Ov('ball'),410,152);
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML=''; const rows=log.slice(-5);
      rows.forEach(r=>{ const tr=document.createElement('tr'); if(!r.fair) tr.className='em31-bad';
        tr.innerHTML=`<td>${FUEL[r.f].name}</td><td>${r.w} g</td><td>${r.t}분</td><td>${r.ws?'있음':'없음'}</td><td>${fmt(r.dt,1)}</td><td>${fmt(r.dm,2)}</td><td>${fmt(r.perG,1)}${r.fair?'':' ⚠'}</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-f]').forEach(b=>b.addEventListener('click',()=>{ st.f=b.dataset.f; st.res=null; show(); draw(); }));
    ['w','t'].forEach(k=>I(k).addEventListener('input',()=>{ st.res=null; show(); draw(); }));
    I('ws').addEventListener('change',()=>{ st.res=null; show(); draw(); });
    $('[data-act="run"]').addEventListener('click',run);
    $('[data-act="rec"]').addEventListener('click',()=>{ const R=st.res; if(!R||R.boil){ O('msg').textContent='먼저 「실험하기」로 측정하자.'; return; }
      if(R.recorded) { O('msg').textContent='이미 기록한 측정이다. 다시 「실험하기」를 누르자.'; return; }
      const first=log[0]; const fair=!first||(first.w===R.w&&first.t===R.t&&first.ws===R.ws);
      log.push({f:R.f,w:R.w,t:R.t,ws:R.ws,dt:R.dt,dm:R.dm,perG:R.perG,perMol:R.perMol,fair}); R.recorded=true; renderLog();
      O('msg').textContent= fair? `기록했다(${log.length}번째). 다른 연료로 같은 조건에서 되풀이하자.` : '통제 변인(물의 질량·가열 시간·바람막이)이 첫 기록과 다르다 — 공정한 비교가 아니다(⚠).'; });
    $('[data-act="reset"]').addEventListener('click',()=>{ log.length=0; renderLog(); st={f:'CH3OH',trial:0,res:null,anim:1};
      I('w').value=200; I('t').value=3; I('ws').checked=true; show(); draw(); });
    API.ready(()=>{ show(); draw(); });
    show(); draw(); renderLog();
    if(!window.__STILL) API.loop(root,dt=>{ if(st.res&&!st.res.boil&&st.anim<1){ st.anim=Math.min(1,st.anim+dt/2.2); show(); draw(); } });
  },

  em31chart(root, API){
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), Ov=k=>$(`[data-ov="${k}"]`), I=k=>$(`[data-i="${k}"]`);
    const svg=$('svg'), fig=$('.lab-fig'), g=API.mk('g',{},svg), W=650, X0=78, Y0=330, YT=40;
    let unit='g';
    const names={}; ORDER.forEach(k=>{ const d=document.createElement('div'); d.className='ov mid'; d.style.cssText='font-size:19px;line-height:1.25;text-align:center';
      d.innerHTML=API.tex(FUEL[k].tex)+'<br>'+FUEL[k].name; fig.appendChild(d); names[k]=d; });
    const litVal=k=>{ const F=FUEL[k]; return unit==='g'? F.H/F.M : unit==='mol'? F.H : F.nC*44/F.H*1000; };
    const UN={g:['1 g당 방출한 열 [kJ/g]',160,40,1],mol:['1 mol당 방출한 열 [kJ/mol]',6000,1000,0],co2:['열 1000 kJ당 이산화 탄소 [g]',80,20,1]};
    function meas(){ const m={}; window.__em31log.forEach(r=>{ (m[r.f]=m[r.f]||[]).push(r); });
      const out={}; for(const k in m){ const a=m[k]; out[k]={n:a.length, g:a.reduce((s,r)=>s+r.perG,0)/a.length, mol:a.reduce((s,r)=>s+r.perMol,0)/a.length}; } return out; }
    function draw(){
      root.querySelectorAll('[data-u]').forEach(b=>b.classList.toggle('on',b.dataset.u===unit));
      while(g.firstChild) g.removeChild(g.firstChild);
      const mk=(t,a)=>API.mk(t,a,g), [lab,ymax,tick,dec]=UN[unit], showLit=I('lit').checked, M=meas();
      const keys=ORDER.filter(k=>showLit||FUEL[k].rate);
      const y=v=>Y0-(Y0-YT)*Math.min(v,ymax)/ymax;
      for(let v=0;v<=ymax+1e-9;v+=tick){ mk('line',{x1:X0,y1:y(v),x2:W-14,y2:y(v),stroke:'#E2E7EC','stroke-width':1});
        const t=mk('text',{x:X0-8,y:y(v)+6,'text-anchor':'end','font-size':18,fill:'#5B6B7F'}); t.textContent=v; }
      API.arrow(g,X0,Y0+4,X0,YT-22,'#5B6B7F',2.5); mk('line',{x1:X0-4,y1:Y0,x2:W-10,y2:Y0,stroke:'#5B6B7F','stroke-width':2.5});
      Ov('ax').textContent=lab; API.place(Ov('ax'),X0+10,4);
      const slot=(W-14-X0)/keys.length, bw=Math.min(34,slot*.32);
      ORDER.forEach(k=>{ names[k].innerHTML=API.tex(FUEL[k].tex)+'<br>'+FUEL[k].name; API.place(names[k],0,0,false); });
      keys.forEach((k,i)=>{ const F=FUEL[k], cx=X0+slot*(i+.5), col=F.alt?'#2E9E6A':'#3A3F47';
        const lv=litVal(k), hasM=M[k]&&unit!=='co2';
        const lx=hasM? cx+2 : cx-bw/2;
        mk('rect',{x:lx,y:y(lv),width:bw,height:Y0-y(lv),fill:'#fff','fill-opacity':.6,stroke:col,'stroke-width':2.5,'stroke-dasharray':'6 4'});
        const t=mk('text',{x:lx+bw/2,y:y(lv)-6,'text-anchor':'middle','font-size':18,fill:col,'font-weight':700}); t.textContent=lv.toFixed(dec);
        if(hasM){ const mv=M[k][unit]; mk('rect',{x:cx-bw-2,y:y(mv),width:bw,height:Y0-y(mv),fill:col,'fill-opacity':.85});
          const t2=mk('text',{x:cx-bw/2-2,y:y(mv)-6,'text-anchor':'middle','font-size':18,fill:col}); t2.textContent=mv.toFixed(dec); }
        API.place(names[k],cx,Y0+36,true); });
      // 읽기
      const n=window.__em31log.length; O('n').textContent=n+'개';
      const best=keys.reduce((a,b)=> (unit==='co2'? litVal(b)>litVal(a) : litVal(b)>litVal(a))? b:a);
      O('top').textContent= unit==='co2'? `${FUEL[best].name} (가장 많이 배출)` : FUEL[best].name;
      const rank=[...keys].sort((a,b)=>litVal(b)-litVal(a)).map(k=>FUEL[k].name).join(' > ');
      let msg = unit==='g'? `1 g당 열(자료값): ${rank}. `+(showLit?'대체 연료 가운데 수소만 화석 연료보다 크다.':'알코올은 뷰테인보다 1 g당 열이 작다.')
        : unit==='mol'? `1 mol당 열: ${rank}. 분자가 클수록 1 mol당 열이 크지만, 연료는 질량으로 싣고 판다.`
        : `같은 열을 얻을 때 이산화 탄소: ${rank}. 수소는 0 g — 메테인이 화석 연료 중 가장 적다.`;
      if(!n) msg='실험실 ①에서 측정하고 「기록」하면 측정값 막대가 생긴다. '+msg;
      else if(unit!=='co2') msg+=' 측정값은 열 손실 때문에 자료값보다 작다.';
      O('msg').textContent=msg;
    }
    root.querySelectorAll('[data-u]').forEach(b=>b.addEventListener('click',()=>{ unit=b.dataset.u; draw(); }));
    I('lit').addEventListener('change',draw);
    API.onShow(draw); API.ready(draw); draw();
  }
};
})();
