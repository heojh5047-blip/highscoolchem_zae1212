/* 2-5 우리 생활 속 산화·환원 반응 — 실험실
   rm25design : 지속가능한 발전을 위한 미래 전지 설계하기 (필수 탐구 반02-탐3)
     · 고르기: 용도(스마트폰 / 전기 자동차 / 전력 저장 장치), (−)극 물질(아연·마그네슘·철·수소),
       (+)극 물질(산소(공기)·구리 이온·은 이온), 전해질(수용액·유기 액체·고체), 재활용 설계(없음/있음)
     · 표준 전지 전위 E°전지 = E°(+)극 − E°(−)극 (교과서 표 Ⅱ-1 값만: O2 +1.23, Ag+ +0.80, Cu2+ +0.34, H+ 0.00, Fe2+ −0.45, Zn2+ −0.76, Mg2+ −2.37 V)
     · 시제품 전압 = E°전지 × (0.90–0.96, 설계마다 고정된 값: 내부 저항·실제 농도)
     · 평가표(덱이 만든 단순 모형, 1–5점): 전압(E°로), 에너지 밀도·안전성·자원·환경·재활용·수명·충전
       = 두 전극 점수의 평균 + 전해질 보정 (+ 재활용 설계면 환경 +1, 마그네슘 + 수용액이면 안전 −1)
     · 용도별 가중치로 용도 적합 총점(100점), 지속 가능성 지수 = (안전성 + 자원 + 환경·재활용) ÷ 3
     · 「평가표에 기록」→ 기록 표(최근 3행) + 해석, 「초기화」 */
window.DECK_LABS = {
  rm25design(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    // [에너지 밀도, 안전성, 자원, 환경·재활용, 수명·충전]
    const NEG={Zn:{nm:'아연',E:-0.76,s:[3,4,4,4,2],f:'#C9D3DD',st:'#7E8B98'},
               Mg:{nm:'마그네슘',E:-2.37,s:[4,3,4,4,1],f:'#EEF1F4',st:'#8C99A6'},
               Fe:{nm:'철',E:-0.45,s:[2,5,5,5,4],f:'#8C8F94',st:'#5B6B7F'},
               H2:{nm:'수소',E:0.00,s:[4,2,3,5,4],f:'#F3F6FA',st:'#8C99A6',gas:1}};
    const POS={O2:{nm:'산소(공기)',E:1.23,s:[5,4,5,5,3],f:'#F3F6FA',st:'#8C99A6',gas:1},
               Cu:{nm:'구리 이온',E:0.34,s:[2,4,3,3,3],f:'#E6C29C',st:'#B0835A'},
               Ag:{nm:'은 이온',E:0.80,s:[2,4,1,3,3],f:'#DDE1E6',st:'#8C99A6'}};
    const ELY={aq:{nm:'수용액',m:[-1,1,1,1,0],c:'#DDEEF8',o:1},
               org:{nm:'유기 액체',m:[0,-2,0,-1,0],c:'#F6EBC4',o:1},
               sol:{nm:'고체',m:[1,2,-1,0,1],c:'#E7E1F2',o:1}};
    const USE={ph:{nm:'스마트폰',w:[2,2,3,1,1,2]}, ev:{nm:'전기 자동차',w:[2,3,3,1,1,2]}, ess:{nm:'전력 저장 장치',w:[1,1,3,3,2,2]}};
    const CRIT=['전압','에너지 밀도','안전성','자원','환경·재활용','수명·충전'];
    const REF=[5,4,2,2,2,4];   // 현재 리튬 이온 전지(자료: 약 3.7 V, 액체 전해질) — 비교용
    let u='ph', ng='Zn', ps='O2', el='aq', rc='n', log=[];
    const ap=$('svg.rm25-ap'), rd=$('svg.rm25-rad'), gd=API.mk('g',{},ap), ge=API.mk('g',{},ap), gr=API.mk('g',{},rd);
    const eds=[]; for(let i=0;i<8;i++) eds.push(API.mk('circle',{r:4.5,fill:API.COL.minus},ge));
    const cats=[], ans=[];
    for(let i=0;i<3;i++){ cats.push(API.mk('circle',{r:6,fill:'#FDE2E4',stroke:API.COL.plus,'stroke-width':2},ge));
                          ans.push(API.mk('circle',{r:6,fill:'#E3EEFB',stroke:API.COL.minus,'stroke-width':2},ge)); }
    const hash=s=>[...s].reduce((a,c)=>(a*31+c.charCodeAt(0))%9973,7);
    const cl=x=>Math.max(1,Math.min(5,Math.round(x)));
    const vs=E=>E>=3?5:E>=2?4:E>=1.5?3:E>=1?2:1;
    function model(){
      const N=NEG[ng], P=POS[ps], L=ELY[el];
      const E=P.E-N.E, h=hash(u+ng+ps+el+rc), Vm=E*(0.90+(h%61)/1000);
      const s=[0,1,2,3,4].map(k=>(N.s[k]+P.s[k])/2+L.m[k]);
      if(rc==='y') s[3]+=1;
      if(ng==='Mg'&&el==='aq') s[1]-=1;
      const sc=[vs(E)].concat(s.map(cl));
      const w=USE[u].w, tot=Math.round(w.reduce((a,x,i)=>a+x*sc[i],0)/(5*w.reduce((a,x)=>a+x,0))*100);
      const sus=(sc[2]+sc[3]+sc[4])/3;
      return {E,Vm,sc,tot,sus};
    }
    const PX=170, PY=135, R=90, ang=k=>(-90+60*k)*Math.PI/180;
    const pt=(k,v)=>[PX+Math.cos(ang(k))*R*v/5, PY+Math.sin(ang(k))*R*v/5];
    const poly=a=>a.map((v,k)=>pt(k,v).map(z=>z.toFixed(1)).join(',')).join(' ');
    function radar(sc){
      while(gr.firstChild) gr.firstChild.remove();
      for(let v=1;v<=5;v++) API.mk('polygon',{points:poly([v,v,v,v,v,v]),fill:'none',stroke:'#C9D3DD','stroke-width':v===5?2:1},gr);
      for(let k=0;k<6;k++){ const [x,y]=pt(k,5); API.mk('line',{x1:PX,y1:PY,x2:x,y2:y,stroke:'#C9D3DD','stroke-width':1},gr); }
      API.mk('polygon',{points:poly(REF),fill:'none',stroke:API.COL.muted,'stroke-width':2.5,'stroke-dasharray':'6 5'},gr);
      API.mk('polygon',{points:poly(sc),fill:API.COL.equi,'fill-opacity':.22,stroke:API.COL.equi,'stroke-width':3},gr);
      sc.forEach((v,k)=>{ const [x,y]=pt(k,v); API.mk('circle',{cx:x,cy:y,r:5,fill:API.COL.equi},gr); });
    }
    function draw(){
      const q=model(), N=NEG[ng], P=POS[ps], L=ELY[el];
      while(gd.firstChild) gd.firstChild.remove();
      const D=(t,a)=>API.mk(t,a,gd);
      // 바깥 회로: 도선 + 부하(전구)
      D('path',{d:'M145 66 V30 H262 M298 30 H415 V66',fill:'none',stroke:API.COL.ink,'stroke-width':3});
      D('circle',{cx:280,cy:30,r:18,fill:'#FFF4C2',stroke:API.COL.ink,'stroke-width':3});
      D('path',{d:'M268 30 q6 -10 12 0 q6 10 12 0',fill:'none',stroke:API.COL.ink,'stroke-width':2});
      // 전지 몸통
      D('rect',{x:110,y:66,width:340,height:100,rx:10,fill:'#FFFFFF',stroke:'#5B6B7F','stroke-width':2.5});
      D('rect',{x:180,y:70,width:200,height:92,fill:L.c,'fill-opacity':L.o});
      if(el==='sol') for(let x=188;x<380;x+=16) D('line',{x1:x,y1:72,x2:x+12,y2:160,stroke:'#B9A8D6','stroke-width':1.5});
      else D('line',{x1:280,y1:72,x2:280,y2:160,stroke:'#8C99A6','stroke-width':2,'stroke-dasharray':'5 5'});
      const blk=(x,M)=>{ D('rect',{x,y:70,width:50,height:92,rx:4,fill:M.f,stroke:M.st,'stroke-width':2});
        if(M.gas) for(let i=0;i<6;i++) D('circle',{cx:x+14+(i%2)*22,cy:86+Math.floor(i/2)*28,r:5,fill:'#FFFFFF',stroke:M.st,'stroke-width':1.5}); };
      blk(130,N); blk(380,P);
      V('mL').textContent=N.nm; API.place(V('mL'),155,184);
      V('mR').textContent=P.nm; API.place(V('mR'),405,184);
      V('ely').textContent=L.nm+' 전해질'+(el==='sol'?'':' + 분리막'); API.place(V('ely'),280,150);
      V('vm').textContent=q.Vm.toFixed(2)+' V'; API.place(V('vm'),280,58);
      // 출력
      O('E').textContent=q.E.toFixed(2)+' V'; O('Vm').textContent=q.Vm.toFixed(2)+' V';
      q.sc.forEach((v,k)=>O('s'+k).textContent=v);
      O('sus').textContent=q.sus.toFixed(1)+' / 5'; O('tot').textContent=q.tot+'점';
      const lo=q.sc.indexOf(Math.min(...q.sc)), tip=[
        '전압이 낮다 — 표준 환원 전위 차가 큰 전극 쌍을 골라 보자.',
        '에너지 밀도가 낮다 — 가벼운 전극 물질이나 공기 중 산소를 쓰는 극을 생각해 보자.',
        '안전성이 낮다 — 불에 타지 않는 수용액이나 고체 전해질로 바꿔 보자.',
        '자원 점수가 낮다 — 희귀하고 비싼 물질 대신 풍부한 물질을 써 보자.',
        '환경·재활용 점수가 낮다 — 유해 물질을 줄이고 재활용 설계를 넣어 보자.',
        '수명·충전 점수가 낮다 — 충전해 오래 쓸 수 있는 전극 물질을 생각해 보자.'][lo];
      let msg=`${USE[u].nm}용 ${N.nm}–${P.nm} 전지: 표준 전지 전위 ${q.E.toFixed(2)} V, 지속 가능성 ${q.sus.toFixed(1)}. 가장 약한 기준: ${CRIT[lo]} — ${tip.split(' — ')[1]}`;
      if(ng==='Mg'&&el==='aq') msg+=' (마그네슘은 물과 반응해 수소 기체가 생길 수 있다.)';
      if(!O('msg').dataset.keep) O('msg').textContent=msg;
      ['u','n','p','e','r'].forEach(kk=>root.querySelectorAll(`[data-${kk}]`).forEach(x=>x.classList.toggle('on', x.dataset[kk]===({u,n:ng,p:ps,e:el,r:rc})[kk])));
      radar(q.sc); tick(window.__STILL?0:performance.now()/1000);
    }
    function tick(t){
      // 전자: (−)극(왼쪽) → 도선 → 부하 → (+)극(오른쪽)
      const Lp=36+270+36;
      eds.forEach((c,i)=>{ const s=(i*Lp/8+t*50)%Lp; let x,y;
        if(s<36){ x=145; y=66-s; } else if(s<306){ x=145+(s-36); y=30; } else { x=415; y=30+(s-306); }
        c.setAttribute('cx',x); c.setAttribute('cy',y); c.setAttribute('opacity',(y===30&&x>258&&x<302)?0:1); });
      cats.forEach((c,i)=>{ const s=(i*190/3+t*28)%190; c.setAttribute('cx',188+s); c.setAttribute('cy',92+i*26); });
      ans.forEach((c,i)=>{ const s=(i*190/3+t*28+60)%190; c.setAttribute('cx',372-s); c.setAttribute('cy',105+i*26); });
    }
    const SH={ph:'스마트폰',ev:'자동차',ess:'저장 장치'}, PS={O2:'공기',Cu:'구리 이온',Ag:'은 이온'};
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-3).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${r.n}</td><td>${SH[r.u]}</td><td class="l">${NEG[r.ng].nm}–${PS[r.ps]} · ${ELY[r.el].nm}${r.rc==='y'?' · 재활용':''}</td><td>${r.Vm.toFixed(2)}</td><td>${r.sus.toFixed(1)}</td><td>${r.tot}</td>`; tb.appendChild(tr); }); }
    const bind=(sel,fn)=>root.querySelectorAll(sel).forEach(x=>x.addEventListener('click',()=>{ fn(x); delete O('msg').dataset.keep; draw(); }));
    bind('[data-u]',x=>u=x.dataset.u); bind('[data-n]',x=>ng=x.dataset.n); bind('[data-p]',x=>ps=x.dataset.p);
    bind('[data-e]',x=>el=x.dataset.e); bind('[data-r]',x=>rc=x.dataset.r);
    $('[data-act="rec"]').addEventListener('click',()=>{
      const q=model(); log.push({n:log.length+1,u,ng,ps,el,rc,Vm:q.Vm,sus:q.sus,tot:q.tot,E:q.E});
      renderLog(); draw();
      const msg=O('msg');
      const same=log.filter(r=>r.u===u);
      if(log.length>=3 && same.length>=2){
        const best=same.reduce((a,b)=>b.tot>a.tot?b:a), hv=same.reduce((a,b)=>b.E>a.E?b:a);
        msg.textContent=`${USE[u].nm}용 기록 ${same.length}개 중 총점 최고 #${best.n}(${best.tot}점), 전압 최고 #${hv.n}(${hv.Vm.toFixed(2)} V). `+
          (best.n===hv.n?'이 용도에서는 전압이 높은 설계가 총점도 높았다. 다른 용도로도 비교해 보자.':'전압이 가장 높은 설계가 가장 좋은 전지는 아니다 — 안전성·자원·환경·수명과 용도를 함께 따져야 한다.');
      } else if(log.length>=3) msg.textContent=`기록 ${log.length}개 — 총점은 같은 용도끼리 비교한다. 지금 용도(${USE[u].nm})로 설계를 하나 더 기록해 보자.`;
      else msg.textContent=`기록 ${log.length}개 — 용도나 재료를 바꾸어 설계를 더 기록하고 비교해 보자 (${log.length}/3).`;
      msg.dataset.keep='1'; });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); u='ph'; ng='Zn'; ps='O2'; el='aq'; rc='n'; delete O('msg').dataset.keep; draw(); });
    API.onShow&&API.onShow(()=>draw());
    API.ready&&API.ready(()=>draw());
    draw();
    if(!window.__STILL) API.loop(root,()=>tick(performance.now()/1000));
  }
};
