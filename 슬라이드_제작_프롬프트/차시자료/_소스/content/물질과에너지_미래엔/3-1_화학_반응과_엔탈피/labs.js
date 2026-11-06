/* 3-1 화학 반응과 엔탈피 — 실험실 (필수 탐구 물03-탐1 「대체 연료와 화석 연료의 효율성을 비교하는 탐구하기」,
   교과서 74–75쪽 탐구 「대체 연료와 화석 연료의 효율성 비교하기」)
   em31conv : 연료 고르기 → 몰당 연소 엔탈피를 단위 질량당(÷ 몰질량)·단위 부피당(× 밀도)으로 변환,
              같은 열 1000 kJ을 얻을 때 이산화 탄소 질량(연료 1 mol당 CO2 mol × 44 ÷ 몰당 열 × 1000).
              「계산 기록」→ 표에 행이 쌓이고, 기록한 연료가 막대그래프(단위 질량당 / 단위 부피당 / 이산화 탄소)에 그려진다.
   자료(교과서 74쪽, 25 °C·1 기압): 옥테인 −5470 kJ/mol, 703 g/L, 114 g/mol · 에탄올 −1367, 785, 46 · 수소 −285.8, 0.0813, 2.
   더 해 보기(덱 보충 자료): 메테인 −890, 0.656 g/L, 16 · 메탄올 −726, 787 g/L, 32. */
window.DECK_LABS = {
  em31conv(root, API){
    const FUEL={
      C8H18:{name:'옥테인',tex:'\\ce{C8H18}',M:114,H:5470,d:703,nC:8,alt:false},
      C2H5OH:{name:'에탄올',tex:'\\ce{C2H5OH}',M:46,H:1367,d:785,nC:2,alt:true},
      H2:{name:'수소',tex:'\\ce{H2}',M:2,H:285.8,d:0.0813,nC:0,alt:true},
      CH4:{name:'메테인',tex:'\\ce{CH4}',M:16,H:890,d:0.656,nC:1,alt:false},
      CH3OH:{name:'메탄올',tex:'\\ce{CH3OH}',M:32,H:726,d:787,nC:1,alt:true}
    };
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), Ov=k=>$(`[data-ov="${k}"]`);
    const svg=$('svg'), fig=$('.lab-fig'), g=API.mk('g',{},svg), W=620, X0=84, Y0=226, YT=34;
    let st={f:'C8H18', unit:'g'}, log=[];
    const val=k=>{ const F=FUEL[k], pg=F.H/F.M; return {g:pg, L:pg*F.d, co2:F.nC*44/F.H*1000}; };
    const sci=v=> v>=1000? Math.round(v).toLocaleString('en-US') : v>=100? v.toFixed(0) : v.toFixed(1);
    const names={};
    function label(k){ if(!names[k]){ const d=document.createElement('div'); d.className='ov mid'; d.style.cssText='font-size:19px;line-height:1.25;text-align:center'; fig.appendChild(d); names[k]=d; }
      names[k].innerHTML=API.tex(FUEL[k].tex)+'<br>'+FUEL[k].name; return names[k]; }
    function show(){
      root.querySelectorAll('[data-f]').forEach(b=>b.classList.toggle('on',b.dataset.f===st.f));
      root.querySelectorAll('[data-u]').forEach(b=>b.classList.toggle('on',b.dataset.u===st.unit));
      const F=FUEL[st.f], v=val(st.f);
      O('H').textContent=`−${F.H} kJ/mol`;
      O('M').textContent=`${F.M} g/mol · ${F.d} g/L`;
      O('g').textContent=`${F.H} ÷ ${F.M} = ${v.g.toFixed(1)}`;
      O('L').textContent=`${v.g.toFixed(1)} × ${F.d} = ${sci(v.L)}`;
      O('c').textContent=`${v.co2.toFixed(1)} g`;
      let m=`${F.name}(${F.alt?'대체 연료':'화석 연료'}): `;
      if(st.f==='H2') m+='단위 질량당 열은 가장 크지만, 기체라 단위 부피당 열은 매우 작다. 연소 생성물은 물뿐이다.';
      else if(st.f==='CH4') m+='기체 연료라 단위 부피당 열이 작다. 화석 연료 가운데 이산화 탄소가 가장 적다.';
      else m+= `액체라 단위 부피당 열이 크다. 열 1000 kJ을 얻을 때 이산화 탄소 ${v.co2.toFixed(1)} g이 생긴다.`;
      O('msg').textContent=m;
    }
    const UN={g:['단위 질량당 연소 엔탈피 [kJ/g]',160,40],L:['단위 부피당 연소 엔탈피 [kJ/L]',40000,10000],co2:['열 1000 kJ당 이산화 탄소 [g]',80,20]};
    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      const mk=(t,a)=>API.mk(t,a,g), [lab,ymax,tick]=UN[st.unit], y=v=>Y0-(Y0-YT)*Math.min(v,ymax)/ymax;
      for(let v=0;v<=ymax+1e-9;v+=tick){ mk('line',{x1:X0,y1:y(v),x2:W-12,y2:y(v),stroke:'#E2E7EC','stroke-width':1});
        const t=mk('text',{x:X0-8,y:y(v)+6,'text-anchor':'end','font-size':18,fill:'#5B6B7F'}); t.textContent=v; }
      API.arrow(g,X0,Y0+4,X0,YT-20,'#5B6B7F',2.5); mk('line',{x1:X0-4,y1:Y0,x2:W-8,y2:Y0,stroke:'#5B6B7F','stroke-width':2.5});
      Ov('ax').textContent=lab; API.place(Ov('ax'),X0+10,2);
      Object.values(names).forEach(d=>API.place(d,0,0,false));
      const keys=log.map(r=>r.f), slot=(W-12-X0)/Math.max(keys.length,3), bw=Math.min(56,slot*.5);
      if(!keys.length){ const t=mk('text',{x:(X0+W)/2,y:130,'text-anchor':'middle','font-size':20,fill:'#5B6B7F'}); t.textContent='「계산 기록」을 누르면 막대가 생긴다'; }
      keys.forEach((k,i)=>{ const F=FUEL[k], v=val(k)[st.unit], cx=X0+slot*(i+.5), col=F.alt?'#2E9E6A':'#3A3F47';
        mk('rect',{x:cx-bw/2,y:y(v),width:bw,height:Math.max(Y0-y(v),0),fill:col,'fill-opacity':.85});
        const t=mk('text',{x:cx,y:Math.min(y(v),Y0)-6,'text-anchor':'middle','font-size':18,fill:col,'font-weight':700}); t.textContent=st.unit==='L'? sci(v) : v.toFixed(1);
        API.place(label(k),cx,Y0+32,true); });
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const v=val(r.f), tr=document.createElement('tr');
        tr.innerHTML=`<td>${FUEL[r.f].name}</td><td>${v.g.toFixed(1)}</td><td>${sci(v.L)}</td><td>${v.co2.toFixed(1)}</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-f]').forEach(b=>b.addEventListener('click',()=>{ st.f=b.dataset.f; show(); }));
    root.querySelectorAll('[data-u]').forEach(b=>b.addEventListener('click',()=>{ st.unit=b.dataset.u; show(); draw(); }));
    $('[data-act="rec"]').addEventListener('click',()=>{ if(log.some(r=>r.f===st.f)){ O('msg').textContent=`${FUEL[st.f].name}은(는) 이미 기록했다. 다른 연료를 골라 보자.`; return; }
      log.push({f:st.f}); renderLog(); draw();
      if(log.length>=3){ const best=u=>log.reduce((a,b)=>val(b.f)[u]>val(a.f)[u]?b:a).f;
        O('msg').textContent=`기록 ${log.length}개 — 단위 질량당은 ${FUEL[best('g')].name}, 단위 부피당은 ${FUEL[best('L')].name}이(가) 가장 크다. 기준에 따라 '가장 효율적인 연료'가 달라진다.`; } });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; st={f:'C8H18',unit:'g'}; renderLog(); show(); draw(); });
    API.ready(()=>{ show(); draw(); });
    show(); draw();
  }
};
