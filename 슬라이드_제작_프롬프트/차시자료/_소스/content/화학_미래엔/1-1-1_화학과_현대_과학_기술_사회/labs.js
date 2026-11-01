/* 1-1-1 화학과 현대 과학·기술·사회 — 실험실
   cm111nh3 : 암모니아 합성 입자 모형 (덱이 더한 모의실험, 필수 탐구 아님)
     · 질소 분자 a(1–4)개, 수소 분자 b(1–12)개 → 반응 횟수 k = min(a, ⌊b/3⌋)
       생긴 NH3 = 2k, 남은 N2 = a − k, 남은 H2 = b − 3k  (N: 2a = 2k + 2(a−k), H: 2b = 6k + 2(b−3k))
     · 원자 하나하나(N 최대 8, H 최대 24)를 처음에 만들어 두고, 반응 전 자리 → 반응 후 자리로 옮긴다(원자 수 보존).
     · 「반응시키기」 → 1.6초 동안 이동(API.loop), 「기록」 → 표에 행이 쌓임(최근 5행), 「초기화」. */
window.DECK_LABS = {
  cm111nh3(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg');
    API.mk('rect',{x:8,y:36,width:584,height:256,rx:16,fill:'#F4F8FC',stroke:'#9FC3DD','stroke-width':2.5},svg);
    const g=API.mk('g',{},svg);
    const RN=24, RH=18, D2=37, DH=28, DX=33;
    const mkAtom=(el,r)=>{ const a=API.mk('g',{style:'display:none'},g); API.atom(a,0,0,r,el); return {el,g:a,s:[0,0],e:[0,0]}; };
    const Hs=[], Ns=[];
    for(let i=0;i<24;i++) Hs.push(mkAtom('H',RH));      // H를 먼저 만들어 N 뒤에 그려지게
    for(let i=0;i<8;i++) Ns.push(mkAtom('N',RN));
    let st={phase:0, t:0, a:1, b:3, res:null}, log=[];

    // 칸 배치: 5열 × 4행, 칸 112 × 62
    const cell=i=>[76+(i%5)*112, 80+Math.floor(i/5)*64];
    function layout(kind,x,y){
      if(kind==='N2') return {N:[[x-D2/2,y],[x+D2/2,y]],H:[]};
      if(kind==='H2') return {N:[],H:[[x-DH/2,y],[x+DH/2,y]]};
      const H=[90,210,330].map(d=>[x+DX*Math.cos(d*Math.PI/180), y+DX*Math.sin(d*Math.PI/180)]);
      return {N:[[x,y]],H};
    }
    function compute(){
      const a=+I('a').value, b=+I('b').value, k=Math.min(a,Math.floor(b/3));
      return {a,b,k,nh3:2*k,n2:a-k,h2:b-3*k};
    }
    function place(list,pts,key){ pts.forEach((p,i)=>{ list[i][key]=p; }); }
    function setup(){
      const r=compute(); st.res=r; st.a=r.a; st.b=r.b;
      O('a').textContent=r.a+'개'; O('b').textContent=r.b+'개';
      // 반응 전
      let nS=[], hS=[], c=0;
      for(let i=0;i<r.a;i++){ const L=layout('N2',...cell(c++)); nS.push(...L.N); }
      for(let i=0;i<r.b;i++){ const L=layout('H2',...cell(c++)); hS.push(...L.H); }
      // 반응 후
      let nE=[], hE=[]; c=0;
      for(let i=0;i<r.nh3;i++){ const L=layout('NH3',...cell(c++)); nE.push(...L.N); hE.push(...L.H); }
      for(let i=0;i<r.n2;i++){ const L=layout('N2',...cell(c++)); nE.push(...L.N); }
      for(let i=0;i<r.h2;i++){ const L=layout('H2',...cell(c++)); hE.push(...L.H); }
      if(nS.length!==nE.length||hS.length!==hE.length) console.error('[cm111nh3] 원자 수 불일치');
      Ns.forEach((A,i)=>{ A.on=i<nS.length; if(A.on){ A.s=nS[i]; A.e=nE[i]; } });
      Hs.forEach((A,i)=>{ A.on=i<hS.length; if(A.on){ A.s=hS[i]; A.e=hE[i]; } });
      st.phase=0; st.t=0; draw();
    }
    const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
    function draw(){
      const r=st.res, u=st.phase===2?1:st.phase===1?ease(st.t):0;
      Ns.concat(Hs).forEach(A=>{
        A.g.style.display=A.on?'':'none';
        if(!A.on) return;
        const x=A.s[0]+(A.e[0]-A.s[0])*u, y=A.s[1]+(A.e[1]-A.s[1])*u;
        A.g.setAttribute('transform',`translate(${x.toFixed(1)},${y.toFixed(1)})`);
      });
      const done=st.phase===2;
      Ov('st').textContent=done?'반응 후':st.phase===1?'반응하는 중…':'반응 전';
      API.place(Ov('st'),18,4);
      Ov('cnt').textContent=`N 원자 ${2*r.a}개 · H 원자 ${2*r.b}개`+(done?' (반응 전과 같다)':'');
      API.place(Ov('cnt'),330,6);
      O('nh3').textContent=done? r.nh3+'개' : '?';
      let left=[]; if(r.n2) left.push(`질소 분자 ${r.n2}개`); if(r.h2) left.push(`수소 분자 ${r.h2}개`);
      O('msg').textContent = !done ? '「반응시키기」를 눌러 원자가 어떻게 다시 결합하는지 보자.'
        : r.k===0 ? '수소 분자가 3개보다 적어 암모니아가 생기지 않았다. 질소 분자 1개에는 수소 분자 3개가 필요하다.'
        : left.length===0 ? `질소 분자 1개와 수소 분자 3개가 반응하는 비율에 딱 맞아, 남은 분자 없이 암모니아 ${r.nh3}개가 생겼다.`
        : `암모니아 ${r.nh3}개가 생기고 ${left.join(', ')}가 남았다. 원자는 없어지지 않고 남은 분자로 그대로 있다.`;
    }
    function renderLog(){
      O('log').innerHTML=log.slice(-5).map(r=>`<tr><td>${r.a}</td><td>${r.b}</td><td>${r.nh3}</td><td>${[r.n2?'질소 '+r.n2:'', r.h2?'수소 '+r.h2:''].filter(Boolean).join(', ')||'없음'}</td><td>N ${2*r.a} = ${2*r.a} · H ${2*r.b} = ${2*r.b}</td></tr>`).join('')
        || '<tr><td colspan="5" class="c-muted">반응시킨 뒤 「기록」을 누르면 여기에 쌓인다.</td></tr>';
    }
    root.querySelectorAll('input[type=range]').forEach(i=>i.addEventListener('input',setup));
    root.querySelector('[data-act="go"]').addEventListener('click',()=>{ if(st.phase===2) { st.phase=0; } st.phase=1; st.t=0; draw(); });
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{
      if(st.phase!==2){ O('msg').textContent='먼저 「반응시키기」를 눌러 반응을 끝낸 뒤 기록하자.'; return; }
      log.push(Object.assign({},st.res)); renderLog();
    });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ I('a').value=1; I('b').value=3; log=[]; renderLog(); setup(); });
    API.loop(root,dt=>{ if(st.phase!==1) return; st.t+=dt/1.6; if(st.t>=1){ st.t=1; st.phase=2; } draw(); });
    renderLog(); setup();
  }
};
