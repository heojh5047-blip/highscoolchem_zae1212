/* 2-3 화학 전지의 원리 — 실험실
   rm23cell : 금속판과 전해질로 전지 만들기 (필수 탐구 반02-탐1)
     · 왼쪽·오른쪽 금속판(마그네슘·아연·철·구리·은), 전해질(각 금속 이온 1 M / 둘 다 묽은 황산 / 증류수), 염다리 있음·없음, 전극 사이 거리 1–5 cm
     · 표준 환원 전위(교과서 표 Ⅱ-1)가 작은 금속이 (−)극(산화 전극) → 그림의 극 라벨·전자 흐름 방향이 바뀜
     · 전압계 = 모형 기전력 + 작은 측정 오차(설정마다 고정), 5분 뒤 전압(묽은 황산은 분극으로 감소), 전류(저항 100 Ω 연결, 거리 → 내부 저항)
     · 「측정·기록」→ 기록 표에 행이 쌓이고(최근 6행) 전압 막대, 서로 다른 설정 3가지 이상이면 효율 조건 해석 · 「초기화」 */
window.DECK_LABS = {
  rm23cell(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const M={
      Mg:{nm:'마그네슘',e:-2.37,ion:'\\ce{MgSO4(aq)}',f:'#EEF1F4',s:'#9AA5B1',sc:'#DDEEF8',so:1},
      Zn:{nm:'아연',e:-0.76,ion:'\\ce{ZnSO4(aq)}',f:'#C9D3DD',s:'#7E8B98',sc:'#DDEEF8',so:1},
      Fe:{nm:'철',e:-0.45,ion:'\\ce{FeSO4(aq)}',f:'#8C8F94',s:'#5B6B7F',sc:'#9CCB8A',so:.4},
      Cu:{nm:'구리',e:0.34,ion:'\\ce{CuSO4(aq)}',f:'#E6C29C',s:'#B0835A',sc:'#3E8ED0',so:.3},
      Ag:{nm:'은',e:0.80,ion:'\\ce{AgNO3(aq)}',f:'#DDE1E6',s:'#8C99A6',sc:'#DDEEF8',so:1}
    };
    const EL={ion:'각 금속 이온 1 M',acid:'묽은 황산',water:'증류수'};
    let L='Zn', R='Cu', el='ion', br=1, log=[];
    const svg=$('svg'), gd=API.mk('g',{},svg), ge=API.mk('g',{},svg);
    const dots=[]; for(let i=0;i<10;i++) dots.push(API.mk('circle',{r:5,fill:API.COL.minus},ge));
    let path=null, LEN=1, dir=0, flowOn=false;
    const f2=x=>x.toFixed(2);
    function model(){
      const d=+$('[data-i="d"]').value, a=M[L], b=M[R];
      const neg = a.e<=b.e ? 'L':'R', mn = neg==='L'?L:R, mp = neg==='L'?R:L;
      const dE = Math.abs(a.e-b.e);
      let E=0, th=null;
      if(L===R) E=0;
      else if(el==='ion'){ E=dE; th=dE; }
      else if(el==='acid'){ E=Math.max(0.02,-M[mn].e); }
      else E=dE*0.5;
      if(!br) E=0;
      const h=[...(L+R+el+br+d)].reduce((s,c)=>(s*31+c.charCodeAt(0))%9973,7);
      const noise=E>0?((h%41)-20)/1000:0;
      const Vm=Math.max(0,E-0.02+noise);
      const v5 = el==='acid'? Vm*0.4 : el==='water'? Vm*0.9 : Math.max(0,Vm-0.01);
      const r = el==='ion'? 5*d : el==='acid'? 4*d : 4000;
      const I = Vm/(100+r)*1000;
      return {d,neg,mn,mp,E,th,Vm,v5,I};
    }
    function draw(){
      const m=model(), d=m.d;
      while(gd.firstChild) gd.firstChild.remove();
      const D=(t,a)=>API.mk(t,a,gd);
      const xR=230+(d-1)*25, cL=80, cR=xR+50;
      const sol=(x0,mt)=>{ const c= el==='ion'? M[mt].sc : el==='acid'? '#DDEEF8' : '#F4F9FC', o= el==='ion'? M[mt].so : 1;
        D('rect',{x:x0+2,y:140,width:146,height:98,fill:c,'fill-opacity':o}); };
      sol(30,L); sol(xR,R);
      [30,xR].forEach(x0=>D('path',{d:`M${x0-5} 110 H${x0} V232 Q${x0} 240 ${x0+8} 240 H${x0+142} Q${x0+150} 240 ${x0+150} 232 V110 H${x0+155}`,fill:'none',stroke:'#7E8B98','stroke-width':3,'stroke-linejoin':'round'}));
      if(br){ const p=`M150 214 V98 H${xR+30} V214`; D('path',{d:p,fill:'none',stroke:'#B9A98A','stroke-width':20}); D('path',{d:p,fill:'none',stroke:'#F6F0E0','stroke-width':15}); }
      D('rect',{x:cL-12,y:80,width:24,height:140,rx:3,fill:M[L].f,stroke:M[L].s,'stroke-width':2});
      D('rect',{x:cR-12,y:80,width:24,height:140,rx:3,fill:M[R].f,stroke:M[R].s,'stroke-width':2});
      D('path',{d:`M${cL} 80 V30 H226 M294 30 H${cR} V80`,fill:'none',stroke:API.COL.ink,'stroke-width':3});
      D('rect',{x:226,y:8,width:68,height:44,rx:8,fill:'#FFFFFF',stroke:API.COL.ink,'stroke-width':3});
      // 전자 경로: (−)극 → 도선 → (+)극
      flowOn = m.E>0 && el!=='water' && L!==R;
      const xn = m.neg==='L'?cL:cR, xp = m.neg==='L'?cR:cL;
      path={xn,xp}; LEN=50+Math.abs(xp-xn)+50;
      if(flowOn){ const sx = xn<xp?1:-1, ax=(xn+ (xn<xp?226:294))/2;
        API.arrow(gd, ax-26*sx, 18, ax+26*sx, 18, API.COL.minus, 3);
        API.place(V('e1'), ax-44*sx, 0); } else API.place(V('e1'),0,0,false);
      V('mL').innerHTML=API.tex('\\ce{'+L+'}'); V('mR').innerHTML=API.tex('\\ce{'+R+'}');
      API.place(V('mL'),cL-34,86); API.place(V('mR'),cR+34,86);
      const st=mt=> el==='ion'? API.tex(M[mt].ion) : el==='acid'? API.tex('\\ce{H2SO4(aq)}') : '증류수';
      V('sL').innerHTML=st(L); V('sR').innerHTML=st(R);
      API.place(V('sL'),105,212); API.place(V('sR'),xR+75,212);
      const neg='(−)극 · <span style="color:#C2410C">산화 전극</span>', pos='(+)극 · <span style="color:#0E7490">환원 전극</span>';
      if(L!==R){ V('pL').innerHTML= m.neg==='L'?neg:pos; V('pR').innerHTML= m.neg==='L'?pos:neg;
        API.place(V('pL'),105,244); API.place(V('pR'),xR+75,244); }
      else { API.place(V('pL'),0,0,false); API.place(V('pR'),0,0,false); }
      V('vm').textContent=f2(m.Vm)+' V'; API.place(V('vm'),260,18);
      O('d').textContent=d+' cm';
      O('v').textContent=f2(m.Vm)+' V'; O('v5').textContent=f2(m.v5)+' V';
      O('th').textContent= m.th===null? '해당 없음' : f2(m.th)+' V'; O('i').textContent=m.I.toFixed(1)+' mA';
      let msg;
      if(L===R) msg='두 금속판이 같으면 전위차가 없어 전압이 0 V이다. 서로 다른 금속을 골라 보자.';
      else if(!br) msg='염다리가 없어 회로가 끊겼다 — 이온이 이동할 길이 없어 전류가 흐르지 않는다.';
      else if(el==='water') msg='증류수에는 이온이 거의 없어 전류가 거의 흐르지 않는다 — 전해질이 필요하다.';
      else if(el==='acid') msg=`볼타 전지 꼴: (−)극 ${M[m.mn].nm}이 산화되고 (+)극 표면에서 수소 이온이 환원된다. 5분 뒤에는 분극으로 전압이 크게 떨어진다.`;
      else msg=`(−)극 ${M[m.mn].nm}(산화) → 도선의 전자 → (+)극 ${M[m.mp].nm}(환원). 이론값 ${f2(m.th)} V와 측정값 ${f2(m.Vm)} V를 비교해 보자.`;
      if(!O('msg').dataset.keep) O('msg').textContent=msg;
      ['l','r','e','s'].forEach(k=>root.querySelectorAll(`[data-${k}]`).forEach(x=>x.classList.toggle('on', x.dataset[k]===({l:L,r:R,e:el,s:String(br)})[k])));
      tick(window.__STILL?0:performance.now()/1000);
    }
    function tick(t){
      dots.forEach((c,i)=>{
        if(!flowOn||!path){ c.setAttribute('opacity',0); return; }
        let s=((i*(LEN/10)+t*40)%LEN); const {xn,xp}=path; let x,y;
        if(s<50){ x=xn; y=80-s; } else if(s<50+Math.abs(xp-xn)){ x=xn+(xp>xn?1:-1)*(s-50); y=30; } else { x=xp; y=30+(s-50-Math.abs(xp-xn)); }
        const hide=(y===30&&x>226&&x<294);
        c.setAttribute('cx',x); c.setAttribute('cy',y); c.setAttribute('opacity',hide?0:1); });
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-6).forEach(r=>{ const tr=document.createElement('tr');
        const w=Math.round(Math.min(1,r.v/2.8)*80);
        tr.innerHTML=`<td>${r.n}</td><td>${r.neg}</td><td>${r.pos}</td><td>${r.el}</td><td>${r.d} cm</td><td>${f2(r.v)}</td><td>${f2(r.v5)}</td><td class="l"><span class="rm23-bar" style="width:${w}px"></span></td>`; tb.appendChild(tr); }); }
    const on=(sel,fn)=>root.querySelectorAll(sel).forEach(x=>x.addEventListener('click',()=>{ fn(x); delete O('msg').dataset.keep; draw(); }));
    on('[data-l]',x=>L=x.dataset.l); on('[data-r]',x=>R=x.dataset.r); on('[data-e]',x=>el=x.dataset.e); on('[data-s]',x=>br=+x.dataset.s);
    $('[data-i="d"]').addEventListener('input',()=>{ delete O('msg').dataset.keep; draw(); });
    $('[data-act="rec"]').addEventListener('click',()=>{
      const m=model(); const same=L===R;
      log.push({n:log.length+1,neg:same?M[L].nm:M[m.mn].nm,pos:same?M[R].nm:M[m.mp].nm,el:br?EL[el]:EL[el]+'(염다리 없음)',d:m.d,v:m.Vm,v5:m.v5,key:L+R+el+br+m.d});
      renderLog();
      const n=new Set(log.map(r=>r.key)).size, best=log.reduce((a,b)=>b.v>a.v?b:a), msg=O('msg');
      msg.textContent = n>=3 ? `기록 ${n}가지: 전압이 가장 큰 것은 ${best.neg}–${best.pos}(${f2(best.v)} V). 효율적인 전지 = 표준 환원 전위 차이가 큰 금속 짝 + 전압을 유지하는 반쪽 전지·염다리 + 가까운 전극.`
                             : `기록 ${n}가지 — 금속 짝, 전해질, 거리를 바꾸어 더 측정해 보자 (${n}/3).`;
      msg.dataset.keep='1'; });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); L='Zn'; R='Cu'; el='ion'; br=1; $('[data-i="d"]').value=2; delete O('msg').dataset.keep; draw(); });
    API.onShow&&API.onShow(()=>draw());
    API.ready&&API.ready(()=>draw());
    draw();
    if(!window.__STILL) API.loop(root,()=>tick(performance.now()/1000));
  }
};
