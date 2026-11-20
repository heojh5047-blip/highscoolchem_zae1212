/* 3-4 탄소 화합물의 유용성 — 실험실
   rm34make : 새로운 물질 만들기 — 반응물 ①(카복실산·살리실산·염화 아디프산)과 ②(알코올·아세트산 무수물·헥사메틸렌다이아민)를 골라
              반응시키기 → 생성물 구조식(그림은 slides.html에 미리 그린 묶음을 켜고 끔), 떨어져 나간 분자, 쓰임,
              원자 수(반응물 합 = 생성물 + 떨어져 나간 분자), 분자량, 작용기·성질 변화 → 기록 표 (plan.md 2절) */
(function(){
const A={ aa:{t:'아세트산',c:{C:2,H:4,O:2},M:60,k:'acid'}, ba:{t:'뷰탄산',c:{C:4,H:8,O:2},M:88,k:'acid'},
          sa:{t:'살리실산',c:{C:7,H:6,O:3},M:138,k:'sal'}, ac:{t:'염화 아디프산',c:{C:6,H:8,O:2,Cl:2},M:183,k:'acl'} };
const B={ me:{t:'메탄올',c:{C:1,H:4,O:1},M:32,k:'alc'}, et:{t:'에탄올',c:{C:2,H:6,O:1},M:46,k:'alc'}, ia:{t:'아이소아밀 알코올',c:{C:5,H:12,O:1},M:88,k:'alc'},
          an:{t:'아세트산 무수물',c:{C:4,H:6,O:3},M:102,k:'anh'}, hd:{t:'헥사메틸렌다이아민',c:{C:6,H:16,N:2},M:116,k:'dia'} };
const BY={ w:{t:'물',tex:'\\ce{H2O}',c:{H:2,O:1},M:18}, ac:{t:'아세트산',tex:'\\ce{CH3COOH}',c:{C:2,H:4,O:2},M:60}, hcl:{t:'염화 수소',tex:'\\ce{2HCl}',c:{H:2,Cl:2},M:73} };
const P={
  aa_me:['메틸 아세테이트','달콤한 냄새 — 접착제 용매'], aa_et:['에틸 아세테이트','과일 향 — 매니큐어 제거제 용매'], aa_ia:['아이소아밀 아세테이트','바나나 향 — 향료'],
  ba_me:['메틸 뷰타노에이트','사과 향 — 향료'], ba_et:['에틸 뷰타노에이트','파인애플 향 — 향료'], ba_ia:['아이소아밀 뷰타노에이트','달콤한 과일 향 — 향료'],
  sa_me:['메틸 살리실레이트','파스 냄새 — 근육통 파스·연고'], sa_et:['에틸 살리실레이트','파스와 비슷한 향 — 향료'], sa_ia:['아이소아밀 살리실레이트','꽃 향 — 향수 원료'],
  sa_an:['아스피린','해열·진통제(의약품)'], ac_hd:['나일론','섬유, 칫솔모, 낙하산']
};
function pair(a,b){ // 반응 짝 → {key, by, role, kind}
  const ka=A[a].k, kb=B[b].k;
  if((ka==='acid'||ka==='sal')&&kb==='alc') return {key:a+'_'+b,by:'w',role:'e',kind:ka==='acid'?'ester':'sest'};
  if(ka==='sal'&&kb==='anh') return {key:'sa_an',by:'ac',role:'a',kind:'asp'};
  if(ka==='acl'&&kb==='dia') return {key:'ac_hd',by:'hcl',role:'n',kind:'nyl'};
  return null; }
const EL=['C','H','N','O','Cl'];
function add(x,y,s){ const r={}; EL.forEach(e=>{ r[e]=(x[e]||0)+s*(y[e]||0); }); return r; }
function fml(c){ let s=''; EL.forEach(e=>{ const k=c[e]||0; if(k>0) s+=e+(k>1?k:''); }); return '\\ce{'+s+'}'; }
const COND={ester:'진한 황산, 가열',sest:'진한 황산, 가열',asp:'인산, 가열',nyl:'두 용액의 경계면'};
const PROP={
  ester:'카복실산의 $-COOH$와 알코올의 $-OH$가 반응해 사라짐 → 산성이 없어지고, 물에 녹는 정도가 줄며, 과일 향이 난다.',
  sest:'살리실산의 $-COOH$가 알코올과 반응해 바뀜 → 산성이 크게 약해지고 향이 나는 물질이 된다.',
  asp:'고리의 $-OH$가 바뀌고 $-COOH$는 남음 → 여전히 산성이지만 위 자극이 줄어든 약이 된다.',
  nyl:'두 단위체가 번갈아 수없이 이어짐 → 물에 녹지 않고 질기며 잘 늘어나는 고분자가 된다.' };

window.DECK_LABS = {
  rm34make(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg');
    let a='aa', b='ia', reacted=true, p=1, log=[];
    const tx=s=>s.replace(/\$(.+?)\$/g,(m,t)=>API.tex('\\ce{'+t+'}'));
    const G=(sel)=>svg.querySelector(sel);
    function show(el,on){ if(el) el.style.display=on?'':'none'; }
    function apply(){
      const pr=pair(a,b);
      const rA=G(`[data-r="A${a}"]`), rB=G(`[data-r="B${b}"]`);
      svg.querySelectorAll('[data-r]').forEach(g=>show(g,g===rA||g===rB));
      [rA,rB].forEach(g=>{ g.style.opacity=reacted&&pr? String(1-.45*p) : '1';
        g.querySelectorAll('[data-hl]').forEach(h=>show(h,!!pr&&h.dataset.hl===pr.role)); });
      svg.querySelectorAll('[data-p]').forEach(g=>show(g,!!pr&&reacted&&g.dataset.p===pr.key));
      svg.querySelectorAll('[data-b]').forEach(g=>show(g,!!pr&&reacted&&g.dataset.b===pr.by));
      if(pr&&reacted){
        const gp=G(`[data-p="${pr.key}"]`), gb=G(`[data-b="${pr.by}"]`);
        gp.style.opacity=String(p);
        gb.style.opacity=String(Math.min(1,p*1.6));
        gb.setAttribute('transform',`translate(${((1-p)*-235).toFixed(1)},${((1-p)*-104).toFixed(1)})`);
      }
    }
    function update(){
      root.querySelectorAll('[data-a]').forEach(x=>x.classList.toggle('on',x.dataset.a===a));
      root.querySelectorAll('[data-b]').forEach(x=>{ if(x.tagName==='BUTTON') x.classList.toggle('on',x.dataset.b===b); });
      const pr=pair(a,b);
      const q=Ov('q'), cond=Ov('cond'), eq=Ov('eq'), mm=Ov('mm'), prop=Ov('prop');
      if(!pr){
        O('pname').textContent='—'; O('by').textContent='—'; O('use').textContent='—';
        O('msg').textContent='이 실험실에서 다루는 반응 짝이 아니다. 카복실산 + 알코올, 살리실산 + 아세트산 무수물, 염화 아디프산 + 헥사메틸렌다이아민 가운데에서 골라 보자.';
        q.innerHTML='이 실험실에서 다루지 않는 짝'; API.place(q,325,300);
        API.place(cond,0,0,false); API.place(eq,0,0,false); API.place(mm,0,0,false); API.place(prop,0,0,false);
        apply(); return;
      }
      cond.innerHTML=COND[pr.kind]; API.place(cond,205,208);
      if(!reacted){
        O('pname').textContent='?'; O('by').textContent='?'; O('use').textContent='?';
        O('msg').textContent='점선으로 표시한 부분이 떨어져 나간다. 어떤 물질이 생길지 예상한 뒤 ‘반응시키기’를 눌러 보자.';
        q.innerHTML='무엇이 생길까?'; API.place(q,325,300);
        API.place(eq,0,0,false); API.place(mm,0,0,false); API.place(prop,0,0,false);
        apply(); return;
      }
      API.place(q,0,0,false);
      const ra=A[a], rb=B[b], by=BY[pr.by];
      const sum=add(ra.c,rb.c,1), prod=add(sum,by.c,-1);
      const Mp=ra.M+rb.M-by.M;
      O('pname').textContent=P[pr.key][0]; O('by').textContent=by.t+(pr.by==='hcl'?' (반복 단위마다 2개)':'');
      O('use').textContent=P[pr.key][1];
      O('msg').textContent=pr.kind==='nyl'?'축합 중합: 염화 수소가 떨어져 나가며 두 단위체가 번갈아 이어진다. 원자 수는 반복 단위 하나로 비교한다.'
        :'두 분자의 작용기가 반응해 작은 분자가 떨어져 나가며 이어졌다. 반응물에 없던 새로운 성질을 가진 물질이다.';
      const lp=pr.kind==='nyl'?'반복 단위 ':'생성물 ';
      eq.innerHTML='원자 수&ensp;반응물 합 '+API.tex(fml(sum))+'&ensp;=&ensp;'+lp+API.tex(fml(prod))+'&ensp;+&ensp;'+API.tex(by.tex);
      mm.innerHTML='분자량&ensp;'+ra.M+' + '+rb.M+' = '+(ra.M+rb.M)+'&ensp;=&ensp;'+Mp+' + '+(pr.by==='hcl'?'2 × 36.5':by.M);
      prop.innerHTML=tx(PROP[pr.kind]);
      API.place(eq,325,394); API.place(mm,325,430); API.place(prop,325,478);
      apply();
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${r.r}</td><td>${r.p}</td><td>${r.by}</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('button[data-a]').forEach(x=>x.addEventListener('click',()=>{ a=x.dataset.a; reacted=false; p=0; update(); }));
    root.querySelectorAll('button[data-b]').forEach(x=>x.addEventListener('click',()=>{ b=x.dataset.b; reacted=false; p=0; update(); }));
    $('[data-act="react"]').addEventListener('click',()=>{ reacted=true; p=window.__STILL?1:0; update(); });
    $('[data-act="rec"]').addEventListener('click',()=>{ const pr=pair(a,b);
      log.push({r:A[a].t+' + '+B[b].t, p:(pr&&reacted)?P[pr.key][0]:'(다루지 않는 짝)', by:(pr&&reacted)?BY[pr.by].t:'—'});
      if(log.length>3) log.shift(); renderLog(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ a='aa'; b='ia'; reacted=false; p=0; log=[]; renderLog(); update(); });
    root._step=()=>{ p=1; update(); };
    if(!window.__STILL) API.loop(root,dt=>{ if(!reacted||p>=1) return; p=Math.min(1,p+dt*0.9); apply(); });
    API.ready(()=>update());
    update();
  }
};
})();
