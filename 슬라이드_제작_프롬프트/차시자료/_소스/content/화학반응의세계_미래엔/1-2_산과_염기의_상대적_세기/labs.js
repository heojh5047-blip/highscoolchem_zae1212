/* 1-2 산과 염기의 상대적 세기 — 실험실
   rm12ph : pH 측정값과 이론값 비교 (필수 탐구 반01-탐1)
     · 수용액(HCl, CH3COOH, NaOH, NH3)과 농도(0.1 M / 0.01 M)를 고른다.
     · 「이론값 계산」 → 이온화 상수로 계산한 pH(강산·강염기는 농도, 약산 √(CKa), 약염기 √(CKb)와 Kw).
     · 「pH 측정」 → 측정기 표시 창이 흔들리다 멈춘다(API.loop). 측정값 = 이론값 + 치우침 + 작은 잡음(고정 시드).
     · 측정·모둠 입력값은 표(최근 5행)에 쌓이고 그래프에 점으로 찍힌다. 「초기화」는 표·그래프를 비운다. */
window.DECK_LABS = {
  rm12ph(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), g=API.mk('g',{},svg);
    const ce=s=>API.tex('\\ce{'+s+'}');
    const KW=1.0e-14;
    const SOL=[
      {f:'HCl',  kind:'강산',   eq:'HCl(aq) + H2O(l) -> Cl-(aq) + H3O+(aq)', type:'sa', bias:0.06, why:'진한 강산 수용액에서는 이온끼리의 영향으로 측정값이 조금 크게 나올 수 있다.'},
      {f:'CH3COOH', kind:'약산', eq:'CH3COOH(aq) + H2O(l) <=> CH3COO-(aq) + H3O+(aq)', type:'wa', K:1.8e-5, bias:0.02, why:'계산의 근사와 온도 차이가 원인일 수 있다.'},
      {f:'NaOH', kind:'강염기', eq:'NaOH(aq) -> Na+(aq) + OH-(aq)', type:'sb', bias:-0.12, why:'수산화 나트륨 수용액이 공기 중 '+'CO2'+'를 흡수하면 [OH-]가 줄어 pH가 낮게 나온다.'},
      {f:'NH3',  kind:'약염기', eq:'NH3(aq) + H2O(l) <=> NH4+(aq) + OH-(aq)', type:'wb', K:1.8e-5, bias:-0.06, why:'암모니아가 공기 중으로 날아가 농도가 줄면 pH가 낮게 나온다.'}
    ];
    const CONC=[0.1,0.01];
    let st={s:0,c:0,calc:false,me:null,t:9,target:0}, log=[], seed=12;
    function rnd(){ seed=(seed*16807)%2147483647; return seed/2147483647; }
    const sct=v=>{ const e=Math.floor(Math.log10(v)+1e-9); const m=v/Math.pow(10,e); return m.toFixed(1)+'\\times10^{'+e+'}'; };
    function theory(i,C){
      const S=SOL[i]; let h,t;
      if(S.type==='sa'){ h=C; t='[\\ce{H3O+}]='+C+'\\ \\text{M}'; }
      else if(S.type==='wa'){ h=Math.sqrt(C*S.K); t='[\\ce{H3O+}]=\\sqrt{CK_\\mathrm{a}}='+sct(h)+'\\ \\text{M}'; }
      else { const oh=S.type==='sb'?C:Math.sqrt(C*S.K); h=KW/oh;
        t=(S.type==='sb'?'[\\ce{OH-}]='+C:'[\\ce{OH-}]=\\sqrt{CK_\\mathrm{b}}='+sct(oh))+'\\ \\text{M}\\to[\\ce{H3O+}]='+sct(h); }
      return {pH:-Math.log10(h), line:API.tex(t)};
    }
    const need=i=>API.tex(['\\text{농도}','K_\\mathrm{a}=1.8\\times10^{-5}','\\text{농도},\\ K_\\mathrm{w}=1.0\\times10^{-14}','K_\\mathrm{b}=1.8\\times10^{-5},\\ K_\\mathrm{w}'][i]);
    // 그래프 좌표
    const GX=[310,400,490,575], gy=p=>246-p*15.5, AX=270;
    function draw(){
      root.querySelectorAll('[data-s]').forEach(b=>{ const i=+b.dataset.s; b.innerHTML=ce(SOL[i].f); b.classList.toggle('on',i===st.s); });
      root.querySelectorAll('[data-c]').forEach(b=>b.classList.toggle('on',+b.dataset.c===st.c));
      const S=SOL[st.s], C=CONC[st.c], T=theory(st.s,C);
      O('eq').innerHTML='<b>'+S.kind+'</b> '+ce(S.eq);
      O('need').innerHTML=need(st.s);
      O('calc').innerHTML=st.calc?T.line:'—';
      O('th').textContent=st.calc?('pH '+T.pH.toFixed(2)+' (≈ '+T.pH.toFixed(1)+')'):'—';
      O('me').textContent=(st.me===null)?'—':(st.t<1.4?'측정 중…':'pH '+st.me.toFixed(2));
      g.innerHTML='';
      // 비커 + 측정기
      API.mk('path',{d:'M40 120 L40 250 Q40 262 52 262 L178 262 Q190 262 190 250 L190 120',fill:'none',stroke:'#7E8B98','stroke-width':3},g);
      API.mk('path',{d:'M42 160 L42 250 Q42 260 52 260 L178 260 Q188 260 188 250 L188 160 Z',fill:'#DDEEF8'},g);
      API.mk('rect',{x:18,y:14,width:132,height:54,rx:10,fill:'#16233D'},g);
      API.mk('rect',{x:26,y:22,width:116,height:38,rx:5,fill:'#CFE8D8'},g);
      const dip=st.me!==null, py=dip?100:44;
      API.mk('path',{d:`M150 40 Q166 40 166 ${py}`,fill:'none',stroke:'#3A3F47','stroke-width':2.5},g);
      API.mk('line',{x1:166,y1:py,x2:166,y2:py+132,stroke:'#3A3F47','stroke-width':8,'stroke-linecap':'round'},g);
      // 축
      API.mk('line',{x1:AX,y1:14,x2:AX,y2:246,stroke:'#5B6B7F','stroke-width':2},g);
      API.mk('line',{x1:AX,y1:246,x2:600,y2:246,stroke:'#5B6B7F','stroke-width':2},g);
      [0,7,14].forEach(p=>{ API.mk('line',{x1:AX-6,y1:gy(p),x2:AX,y2:gy(p),stroke:'#5B6B7F','stroke-width':2},g);
        API.mk('text',{x:AX-10,y:gy(p)+6,'text-anchor':'end','font-size':18,fill:'#5B6B7F'},g).textContent=p; });
      API.mk('line',{x1:AX,y1:gy(7),x2:600,y2:gy(7),stroke:'#8C99A6','stroke-width':1.5,'stroke-dasharray':'6 5'},g);
      API.mk('text',{x:AX+8,y:26,'font-size':18,fill:'#5B6B7F'},g).textContent='pH';
      // 이론값(빈 마름모) — 지금 고른 농도
      SOL.forEach((s,i)=>{ const p=theory(i,C).pH, x=GX[i]-9, y=gy(p);
        API.mk('path',{d:`M${x-8} ${y} L${x} ${y-9} L${x+8} ${y} L${x} ${y+9} Z`,fill:'#fff',stroke:'#16233D','stroke-width':2.5,opacity:(i===st.s||st.calc)?1:.45},g); });
      // 측정값(채운 원)
      log.forEach((r,k)=>{ const x=GX[r.i]+9+((k%3)-1)*3; API.mk('circle',{cx:x,cy:gy(r.m),r:6.5,fill:'#E08A2C',opacity:r.c===st.c?1:.35,stroke:r.src==='모둠'?'#16233D':'none','stroke-width':2},g); });
      const bw=SOL[st.s].f.length>4?96:64; API.mk('rect',{x:GX[st.s]-bw/2,y:252,width:bw,height:28,rx:6,fill:'none',stroke:'#16233D','stroke-width':1.5},g);
      SOL.forEach((s,i)=>{ const e=V('x'+i); e.innerHTML=ce(s.f); e.style.fontSize=(s.f.length>4?'17px':'19px'); API.place(e,GX[i],266); });
      API.place(V('bk'),100,212,true); V('bk').innerHTML=ce(S.f+'(aq)');
      // 표
      O('log').innerHTML=log.map(r=>`<tr><td>${ce(SOL[r.i].f)}</td><td>${CONC[r.c]} M</td><td>${r.th.toFixed(2)}</td><td>${r.m.toFixed(2)}</td><td>${(r.m-r.th>=0?'+':'−')+Math.abs(r.m-r.th).toFixed(2)}</td><td>${r.src}</td></tr>`).join('')||'<tr><td colspan="6" class="c-muted">측정하면 여기에 쌓인다.</td></tr>';
      showDisp();
    }
    function showDisp(){
      const e=V('disp'); let txt='pH --.--';
      if(st.me!==null){ const v=st.t<1.4?st.me+0.8*Math.exp(-st.t*2.5)*Math.sin(st.t*14):st.me; txt='pH '+API.clamp(v,0,14).toFixed(2); }
      e.textContent=txt; API.place(e,84,41,true);
    }
    function explain(r){
      const S=SOL[r.i], d=r.m-r.th;
      let s=ce(S.f)+' '+CONC[r.c]+' M: 계산 '+r.th.toFixed(2)+', 측정 '+r.m.toFixed(2)+' (차이 '+Math.abs(d).toFixed(2)+'). ';
      s+=Math.abs(d)<=0.1?'계산한 값과 잘 맞는다.':'차이의 원인: '+S.why.replace('CO2',ce('CO2')).replace('[OH-]','['+ce('OH-')+']');
      const done=[0,1,2,3].map(i=>log.find(x=>x.i===i&&x.c===0&&x.src==='모의'));
      if(done.every(Boolean)) s+=' — 0.1 M에서 강산·약산의 pH 차이 '+(done[1].th-done[0].th).toFixed(1)+', 강염기·약염기의 차이 '+(done[2].th-done[3].th).toFixed(1)+'이다.';
      return s;
    }
    function push(r){ log.push(r); if(log.length>5) log.shift(); }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ st.s=+b.dataset.s; st.calc=false; st.me=null; O('msg').textContent='먼저 이론값을 계산해 예측하고, pH를 측정해 비교하자.'; draw(); }));
    root.querySelectorAll('[data-c]').forEach(b=>b.addEventListener('click',()=>{ st.c=+b.dataset.c; st.calc=false; st.me=null; O('msg').textContent=st.c?'0.01 M: 10배 묽힌 수용액이다. pH가 얼마나 변할지 예측해 보자.':'0.1 M 수용액이다.'; draw(); }));
    $('[data-act="calc"]').addEventListener('click',()=>{ st.calc=true; const T=theory(st.s,CONC[st.c]);
      O('msg').innerHTML=(SOL[st.s].type==='sa'||SOL[st.s].type==='sb')?(SOL[st.s].type==='sa'?'강산은':'강염기는')+' 거의 모두 이온화하므로 농도만으로 pH를 구한다.':'약산·약염기는 이온화 상수로 구한다(근사 '+API.tex('C-x\\approx C')+').';
      draw(); });
    $('[data-act="meas"]').addEventListener('click',()=>{
      const S=SOL[st.s], th=theory(st.s,CONC[st.c]).pH;
      const m=Math.round((th+S.bias*(st.c?0.7:1)+(rnd()-0.5)*0.1)*100)/100;
      st.me=m; st.t=0; st.target=m;
      const r={i:st.s,c:st.c,th,m,src:'모의'}; push(r);
      O('msg').innerHTML=(st.calc?'':'(이론값을 먼저 계산하면 예측과 비교할 수 있다.) ')+explain(r);
      draw(); });
    $('[data-act="add"]').addEventListener('click',()=>{
      const v=parseFloat($('.rm12-in').value);
      if(!(v>=0&&v<=14)){ O('msg').textContent='0과 14 사이의 pH 값을 입력하자.'; return; }
      const th=theory(st.s,CONC[st.c]).pH, r={i:st.s,c:st.c,th,m:v,src:'모둠'}; push(r); st.me=v; st.t=9;
      O('msg').innerHTML='모둠 측정값을 기록했다. '+explain(r); draw(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; seed=12; st.me=null; st.calc=false; O('msg').textContent='초기화했다.'; draw(); });
    API.loop(root,(dt)=>{ if(st.me!==null&&st.t<1.4){ st.t+=dt; if(st.t>=1.4) draw(); else showDisp(); } });
    API.onShow(()=>draw());
    API.ready(()=>draw());
    O('msg').textContent='수용액을 고르고 「이론값 계산」으로 예측한 뒤 「pH 측정」으로 비교하자.';
    draw();
  }
};
