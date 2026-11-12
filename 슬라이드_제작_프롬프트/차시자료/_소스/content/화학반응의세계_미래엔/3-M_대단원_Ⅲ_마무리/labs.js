/* 3-M 대단원 Ⅲ 마무리 — 실험실
   rm39mirror : 과학 글쓰기 13 — 자일로스·자일리톨·포도당의 은거울 반응 (덱 추가, 3-2 rm32ag 모형 값을 이어 씀)
     · 은 석출 정도 p = 1 − e^(−t/τ), τ(60 °C) 자일로스 50 s · 포도당 60 s, τ × 2^((60−T)/10)
     · 자일리톨(포밀기 없음) p = 0
     · 50 % 시간 t50 = τ ln2 → 표에 반올림 정수 s, 300 s보다 길면 "300 s 안에 안 생김"
     · 「중탕」 → 시간 흐름(화면 30배속, 최대 300 s), 「기록」 → 표 최대 5행 + 그 온도 곡선 흐리게, 「초기화」 → 60 °C */
(function(){
const INK='#16233D', MUT='#5B6B7F', EQ='#E08A2C', BF='#7B4FC8', GR='#8C99A6', OX='#C2410C', RD='#0E7490';
const S=[{k:'A',name:'자일로스',fg:'포밀기 ○',base:50,c:EQ},{k:'B',name:'자일리톨',fg:'포밀기 ✕',base:0,c:GR},{k:'C',name:'포도당',fg:'포밀기 ○',base:60,c:BF}];
const clear=g=>{ while(g.firstChild) g.removeChild(g.firstChild); };

window.DECK_LABS = {
  rm39mirror(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=$('svg'), iT=$('[data-i="T"]');
    const TM=300;
    let heat=false, t=0, done=false, runs=[];
    const T=()=>+iT.value;
    const tau=(s,TT)=>s.base? s.base*Math.pow(2,(60-(TT===undefined?T():TT))/10) : Infinity;
    const pOf=(tt,ta)=>isFinite(ta)? 1-Math.exp(-tt/ta) : 0;
    const t50=(s,TT)=>{ const ta=tau(s,TT); if(!isFinite(ta)) return '안 생김'; const v=ta*Math.LN2; return v<=TM? Math.round(v)+' s' : '300 s 안에 안 생김'; };
    // ── 고정 그림: 중탕 비커·시험관 라벨·그래프 축 ──
    const gBath=API.mk('g',{},svg), gTube=API.mk('g',{},svg), gAx=API.mk('g',{},svg), gCur=API.mk('g',{},svg);
    const TX=[70,160,250], TY0=50, TY1=200, TW=44;
    API.mk('path',{d:'M20 110 V232 q0 8 8 8 H292 q8 0 8 -8 V110',fill:'none',stroke:'#7E8B98','stroke-width':3},gBath);
    const water=API.mk('rect',{x:23,y:130,width:274,height:107,fill:'#DDEEF8'},gBath);
    S.forEach((s,i)=>{ API.texText(svg,TX[i],266,s.name,{size:19,anchor:'middle',fill:INK,mix:true});
      API.texText(svg,TX[i],290,s.fg,{size:18,anchor:'middle',fill:s.base?EQ:MUT,mix:true}); });
    const GX=370, GY=34, GW=250, GH=190;
    const gx=v=>GX+v/TM*GW, gy=p=>GY+(1-p)*GH;
    [0,.5,1].forEach(p=>{ API.mk('line',{x1:GX,y1:gy(p),x2:GX+GW,y2:gy(p),stroke:'#E2E7EC','stroke-width':1.5},gAx); API.texText(gAx,GX-8,gy(p)+6,'$'+(p*100)+'$',{size:18,anchor:'end',fill:MUT,mix:true}); });
    [0,100,200,300].forEach(v=>API.texText(gAx,gx(v),GY+GH+24,'$'+v+'$',{size:18,anchor:'middle',fill:MUT,mix:true}));
    API.mk('line',{x1:GX,y1:GY-6,x2:GX,y2:GY+GH,stroke:MUT,'stroke-width':2},gAx);
    API.mk('line',{x1:GX,y1:GY+GH,x2:GX+GW,y2:GY+GH,stroke:MUT,'stroke-width':2},gAx);
    API.mk('line',{x1:GX,y1:gy(.5),x2:GX+GW,y2:gy(.5),stroke:EQ,'stroke-width':1.6,'stroke-dasharray':'6 5'},gAx);
    API.texText(gAx,GX+4,GY-14,'은 석출 정도 [%]',{size:18,anchor:'start',fill:MUT,mix:true});
    API.texText(gAx,GX+GW,GY+GH+50,'시간 [s]',{size:18,anchor:'end',fill:MUT,mix:true});

    function drawTubes(){
      clear(gTube);
      water.setAttribute('fill',heat?'#FDE2E4':'#DDEEF8');
      S.forEach((s,i)=>{ const x=TX[i]-TW/2, p=heat? pOf(t,tau(s)) : 0, top=TY0+50;
        const tint=`rgb(${Math.round(238-120*p)},${Math.round(243-120*p)},${Math.round(248-118*p)})`;
        API.mk('rect',{x:x+3,y:top,width:TW-6,height:TY1-top-3,rx:6,fill:tint},gTube);
        if(p>0.01){ const op=Math.min(1,p*1.05);
          [[x+3,top,7,TY1-top-2],[x+TW-10,top,7,TY1-top-2],[x+3,TY1-11,TW-6,8]].forEach(([X,Y,w,h])=>API.mk('rect',{x:X,y:Y,width:w,height:h,rx:3,fill:'#AEB4BD','fill-opacity':op,stroke:'#8A919C','stroke-width':1,'stroke-opacity':op},gTube)); }
        API.mk('path',{d:`M${x} ${TY0} V${TY1-10} q0 10 10 10 h${TW-20} q10 0 10 -10 V${TY0}`,fill:'none',stroke:'#7E8B98','stroke-width':3},gTube);
        API.mk('circle',{cx:TX[i],cy:TY0-12,r:7,fill:s.c},gTube); });
      clear(gCur);
      runs.forEach(r=>S.forEach(s=>{ if(!s.base) return; const pts=[]; for(let v=0;v<=TM;v+=10) pts.push(gx(v)+','+gy(pOf(v,tau(s,r.T))));
        API.mk('polyline',{points:pts.join(' '),fill:'none',stroke:s.c,'stroke-width':2,'stroke-opacity':.35},gCur); }));
      if(heat) S.forEach(s=>{ const ta=tau(s), pts=[]; for(let v=0;v<t;v+=5) pts.push(gx(v)+','+gy(pOf(v,ta))); pts.push(gx(t)+','+gy(pOf(t,ta)));
        API.mk('polyline',{points:pts.join(' '),fill:'none',stroke:s.c,'stroke-width':3.5,'stroke-dasharray':s.base?'':'7 5'},gCur);
        API.mk('circle',{cx:gx(t),cy:gy(pOf(t,ta)),r:5.5,fill:s.c},gCur); });
    }
    function update(){
      O('T').textContent=T()+' °C';
      O('t').textContent=heat? Math.round(t)+' s' : '—';
      S.forEach(s=>{ O('p'+s.k).textContent=heat? Math.round(pOf(t,tau(s))*100)+' %' : '—'; });
      $('[data-act="heat"]').disabled=heat&&!done;
      const pA=pOf(t,tau(S[0]));
      let m;
      if(!heat) m='세 시험관을 '+T()+' °C 물에 넣고 중탕해 보자. 어느 시험관에 은거울이 생길까?';
      else if(pA<.05) m='중탕하는 중… 시험관 벽을 살펴보자.';
      else if(!done && pA<.5) m='자일로스·포도당 시험관 벽이 점점 은빛으로 흐려진다. 자일리톨 시험관은 그대로다.';
      else m='자일로스와 포도당은 포밀기가 산화되며 은 이온을 환원시켜 은거울을 만들었다. 자일리톨은 포밀기가 하이드록시기로 바뀌었으므로 은거울이 생기지 않는다.';
      if(heat && T()<=40) m+=' 온도가 낮아 느리다.';
      O('msg').textContent=m;
      drawTubes();
    }
    function renderLog(){ O('log').innerHTML=runs.map(r=>`<tr><td>${r.T} °C</td><td>${r.A}</td><td>${r.B}</td><td>${r.C}</td></tr>`).join(''); }
    iT.addEventListener('input',()=>{ heat=false; t=0; done=false; update(); });
    $('[data-act="heat"]').addEventListener('click',()=>{ heat=true; t=0; done=false; update(); });
    $('[data-act="rec"]').addEventListener('click',()=>{
      if(!heat){ O('msg').textContent='먼저 시험관을 넣고 중탕한 뒤 기록하자.'; return; }
      if(!done && pOf(t,tau(S[0]))<.5){ O('msg').textContent='아직 관찰 중이다. 자일로스 시험관이 50 %를 넘거나 300 s가 지난 뒤 기록하자.'; return; }
      runs.push({T:T(),A:t50(S[0]),B:t50(S[1]),C:t50(S[2])}); if(runs.length>5) runs.shift(); renderLog(); update(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ runs=[]; iT.value=60; heat=false; t=0; done=false; renderLog(); update(); });
    root._step=(sec)=>{ if(heat&&!done){ t=Math.min(TM,t+sec); if(t>=TM) done=true; update(); } };
    if(!window.__STILL) API.loop(root,dt=>{ if(heat&&!done){ t=Math.min(TM,t+dt*30); if(t>=TM) done=true; update(); } });
    update(); renderLog();
  }
};
})();
