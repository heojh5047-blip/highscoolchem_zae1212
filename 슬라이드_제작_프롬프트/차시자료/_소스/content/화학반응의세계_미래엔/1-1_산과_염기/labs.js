/* 1-1 산과 염기 — 실험실
   rm11proton : 양성자 이동 추적 (연습용, 필수 탐구 아님)
     · 반응 7개 중 하나를 고르고, 두 반응물 가운데 H+을 내놓는 쪽(산)을 고른다.
     · 맞히면 H+ 공이 산 → 염기로 계속 옮겨 가고(API.loop), 역할·짝산·짝염기 쌍·물의 역할이 나타난다.
     · 「기록」→ 표에 행이 쌓인다(최근 4행). 「초기화」는 표·점수·단계를 비운다. */
window.DECK_LABS = {
  rm11proton(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), g=API.mk('g',{},svg), gh=API.mk('g',{},svg);
    const RX=[
      {eq:'\\ce{HCl(g) + H2O(l) -> Cl-(aq) + H3O+(aq)}', s:['HCl','H2O','Cl-','H3O+'], ar:'->', acid:0, water:'염기 (H+을 받음)'},
      {eq:'\\ce{NH3(aq) + H2O(l) <=> NH4+(aq) + OH-(aq)}', s:['NH3','H2O','NH4+','OH-'], ar:'<=>', acid:1, water:'산 (H+을 내놓음)'},
      {eq:'\\ce{HCl(g) + NH3(g) -> NH4Cl(s)}', s:['HCl','NH3','Cl-','NH4+'], ar:'->', acid:0, water:'없음 (물이 없는 반응)'},
      {eq:'\\ce{CH3COOH(aq) + H2O(l) <=> CH3COO-(aq) + H3O+(aq)}', s:['CH3COOH','H2O','CH3COO-','H3O+'], ar:'<=>', acid:0, water:'염기 (H+을 받음)'},
      {eq:'\\ce{HF(aq) + NH3(aq) <=> F-(aq) + NH4+(aq)}', s:['HF','NH3','F-','NH4+'], ar:'<=>', acid:0, water:'없음 (물이 없는 반응)'},
      {eq:'\\ce{H2O(l) + H2O(l) <=> H3O+(aq) + OH-(aq)}', s:['H2O','H2O','OH-','H3O+'], ar:'<=>', acid:-1, water:'산이면서 염기 (양쪽성)'},
      {eq:'\\ce{HCO3-(aq) + OH-(aq) <=> CO3^2-(aq) + H2O(l)}', s:['HCO3-','OH-','CO3^2-','H2O'], ar:'<=>', acid:0, water:'생성물 (OH-의 짝산)'}
    ];
    // 화면 배치: 생성물은 [산의 짝염기, 염기의 짝산] 순서로 둔다(반응 3·6은 반응식 꼴과 순서가 달라도 같은 이온)
    const X=[78,222,392,532], Y=104, BW=124, BH=58, PLUS='#D7263D', MINUS='#1F6FD1', FIELD='#2E9E6A', BF='#7B4FC8';
    let st={r:0, solved:false, acid:0, tries:0, ok:0, t:0}, log=[];
    const ce=s=>API.tex('\\ce{'+s+'}');

    function box(x,y,col,dim){ API.mk('rect',{x:x-BW/2,y:y-BH/2,width:BW,height:BH,rx:12,fill:'#fff',stroke:col,'stroke-width':2.5,opacity:dim?.4:1},g); }
    function bracket(x1,x2,yy,col){ API.mk('path',{d:`M${x1} 176 L${x1} ${yy} L${x2} ${yy} L${x2} 176`,fill:'none',stroke:col,'stroke-width':3,'stroke-linejoin':'round'},g); }

    function draw(){
      const R=RX[st.r];
      root.querySelectorAll('[data-r]').forEach(b=>b.classList.toggle('on',+b.dataset.r===st.r));
      O('eq').innerHTML=API.tex(R.eq);
      root.querySelectorAll('[data-p]').forEach(b=>{ const i=+b.dataset.p; b.innerHTML=ce(R.s[i]); b.classList.toggle('on',st.solved&&st.acid===i); });
      g.innerHTML=''; gh.innerHTML='';
      const ai=st.acid, bi=1-ai;
      const cols=st.solved?[0,1,2,3].map(k=>k===ai||k===3?PLUS:MINUS):['#7E8B98','#7E8B98','#9AA5B1','#9AA5B1'];
      for(let k=0;k<4;k++) box(X[k],Y,cols[k],k>=2&&!st.solved);
      // 반응물·생성물 화학식: 생성물 2 = 산의 짝염기, 3 = 염기의 짝산
      const sp=[R.s[0],R.s[1],R.s[2],R.s[3]];
      const prodCB=R.s[2], prodCA=R.s[3];
      sp.forEach((s,k)=>{ const e=V('s'+k); e.innerHTML=ce(k===2?prodCB:k===3?prodCA:s); e.style.opacity=(k>=2&&!st.solved)?.4:1; API.place(e,X[k],Y); });
      V('arr').innerHTML=API.tex('\\ce{'+R.ar+'}'); API.place(V('arr'),307,Y);
      API.place(V('pl1'),150,Y); API.place(V('pl2'),462,Y);
      const roles=st.solved?[[ai,'산',PLUS],[bi,'염기',MINUS],[2,'짝염기',MINUS],[3,'짝산',PLUS]]:[[0,'?','#5B6B7F'],[1,'?','#5B6B7F'],[2,'',''],[3,'','']];
      roles.forEach(([k,t,c],j)=>{ const e=V('r'+j); e.textContent=t; e.style.color=c; API.place(e,X[k],160,!!t); });
      if(st.solved){
        bracket(X[ai],X[2],204,FIELD); bracket(X[bi],X[3],234,BF);
        API.mk('text',{x:X[2]-6,y:200,'text-anchor':'end','font-size':19,fill:FIELD},g).textContent='쌍 1';
        API.mk('text',{x:X[3]-6,y:230,'text-anchor':'end','font-size':19,fill:BF},g).textContent='쌍 2';
      }
      API.place(V('hp'),(X[ai]+X[bi])/2,22,st.solved); V('hp').innerHTML=ce('H+')+' 이동';
      O('ab').innerHTML=st.solved?ce(R.s[ai])+' · '+ce(R.s[bi]):'—';
      O('pairs').innerHTML=st.solved?ce(R.s[ai])+'–'+ce(prodCB)+', '+ce(prodCA)+'–'+ce(R.s[bi]):'—';
      O('water').innerHTML=st.solved?R.water.replace('H+',ce('H+')).replace('OH-',ce('OH-')):'—';
      O('score').textContent=` 맞힘 ${st.ok} / 시도 ${st.tries}`;
      O('log').innerHTML=log.map(r=>`<tr><td>${r[0]}</td><td>${ce(r[1])}</td><td>${ce(r[2])}</td><td>${ce(r[1])}–${ce(r[3])}, ${ce(r[4])}–${ce(r[2])}</td></tr>`).join('');
    }

    root.querySelectorAll('[data-r]').forEach(b=>b.addEventListener('click',()=>{ st.r=+b.dataset.r; st.solved=false; O('msg').innerHTML=ce('H+')+'을 내놓는 쪽을 골라 보자. 생성물에서 H가 하나 줄어든 물질을 찾는다.'; draw(); }));
    root.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{
      if(st.solved) return;
      const i=+b.dataset.p, R=RX[st.r]; st.tries++;
      if(R.acid===-1||R.acid===i){ st.ok++; st.solved=true; st.acid=i; st.t=0;
        O('msg').innerHTML=R.acid===-1?'맞다. 같은 물 분자 둘 중 하나는 산, 다른 하나는 염기로 작용한다.':'맞다. '+ce(R.s[i])+'이(가) '+ce('H+')+'을 내놓아 짝염기 '+ce(R.s[2])+'이(가) 된다.';
      } else O('msg').innerHTML='다시 골라 보자. '+ce(R.s[i])+'은(는) 생성물에서 H가 하나 늘어났다 → '+ce('H+')+'을 받는 쪽(염기)이다.';
      draw(); }));
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{
      if(!st.solved){ O('msg').textContent='먼저 산을 골라 양성자 이동을 확인하자.'; return; }
      const R=RX[st.r], ai=st.acid; log.push([st.r+1,R.s[ai],R.s[1-ai],R.s[2],R.s[3]]); if(log.length>4) log.shift();
      O('msg').textContent='기록했다. 다른 반응도 골라 보자.'; draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; st.tries=0; st.ok=0; st.solved=false; O('msg').textContent='초기화했다.'; draw(); });

    API.loop(root,(dt)=>{
      if(!st.solved){ gh.innerHTML=''; return; }
      st.t=(st.t+dt*0.55)%1;
      const a=X[st.acid], b=X[1-st.acid], u=st.t, x=a+(b-a)*u, y=Y-BH/2-6-70*Math.sin(Math.PI*u);
      gh.innerHTML=''; API.charge(gh,x,y,10,'+');
    });
    API.onShow(()=>draw());
    API.ready(()=>{ O('msg').innerHTML='반응을 고르고, '+ce('H+')+'을 내놓는 쪽(산)을 골라 보자.'; draw(); });
    O('msg').innerHTML='반응을 고르고, '+ce('H+')+'을 내놓는 쪽(산)을 골라 보자.';
    draw();
  }
};
