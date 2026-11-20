/* 고급화학 3-2-2 — 실험실
   ac322gibbs : 교과서 155쪽 탐구 활동(ΔG° 그래프 작성과 자발적 과정 온도 범위 토의, 고화-탐23) + 지도서 Ⅲ-2 디지털 탐구(스프레드시트로 자발성이 바뀌는 온도 예측)를 합친 실험실
     · 반응 고르기(탐구 활동 직선, 석회석 분해, 암모니아 합성, 과산화 수소 분해, 오존 생성, 브로민 증발) 또는 ΔH°·ΔS° 슬라이더로 직접 입력
     · ΔG°(T) = ΔH° − T·ΔS°/1000 [kJ] (ΔS°는 J/K → kJ/K로 바꿈), 0–1500 K 직선, 자발 구간(ΔG° < 0) 음영
     · 자발성이 바뀌는 온도 T* = ΔH°/ΔS° (부호가 같을 때만), 경우 (가)–(라)
     · 점 찍기: 지금 온도의 (T, ΔG°)를 그래프에 찍고 기록 표에 한 행 · 비교로 남기기: 지금 직선을 회색으로 남김(최대 3개) */
(function(){
const M='−';
const PRE={inq:['탐구 활동',40.0,100.0],caco3:['석회석 분해',178.3,160.6],nh3:['암모니아 합성',-92.0,-198.9],h2o2:['과산화 수소 분해',-196.1,125.8],o3:['오존 생성',285.4,-137.6],br2:['브로민 증발',31.0,93.0]};
const DASH={'가':'','나':'12 7','다':'3 6','라':'14 6 3 6'};
window.DECK_LABS = {
  ac322gibbs(root, API){
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), I=k=>$(`[data-i="${k}"]`);
    const svg=$('.lab-fig svg'), g=API.mk('g',{},svg);
    const INK='#16233D', MUT='#5B6B7F', PLUS='#D7263D', FIELD='#2E9E6A', RD='#0E7490', BF='#7B4FC8', GRAV='#8C99A6';
    const X0=70, X1=616, Y0=262, Y1=26, TMAX=1500;
    let H,S,T,name,pid,pts,kept,log;
    const sgn=v=>(v>0?'+':v<0?M:'')+Math.abs(v).toFixed(1);
    const fmt=(v,d)=>(v<0?M:'')+Math.abs(v).toFixed(d);
    const mk=(t,at,p)=>API.mk(t,at,p||g);
    function txt(x,y,s,o){ const t=mk('text',Object.assign({x,y,'font-size':18,'text-anchor':'middle',fill:INK},o||{})); t.textContent=s; return t; }
    const G=(h,s,t)=>h-t*s/1000;
    function kase(h,s){ if(h<0&&s>0) return '나'; if(h<0&&s<=0) return '가'; if(h>=0&&s>0) return '라'; return '다'; }
    function tstar(h,s){ return (s!==0 && h*s>0) ? h/s*1000 : null; }
    function niceRange(lines){
      let lo=0, hi=0; lines.forEach(([h,s])=>{ [0,TMAX].forEach(t=>{ const v=G(h,s,t); lo=Math.min(lo,v); hi=Math.max(hi,v); }); });
      const span=Math.max(hi-lo,20); const steps=[5,10,20,25,50,100,200,250,500]; let st=steps.find(x=>span/x<=7)||1000;
      return {lo:Math.floor(lo/st)*st, hi:Math.ceil(hi/st)*st, st};
    }
    function read(){ H=+I('h').value; S=+I('s').value; T=+I('t').value; }
    function setPreset(k){ pid=k; const p=PRE[k]; name=p[0]; I('h').value=p[1]; I('s').value=p[2]; pts=[]; markSeg(); read(); }
    function markSeg(){ root.querySelectorAll('[data-p]').forEach(b=>b.classList.toggle('on',b.dataset.p===pid)); }
    function init(){ kept=[]; log=[]; I('t').value=300; setPreset('inq'); }
    function draw(){
      g.innerHTML='';
      const R=niceRange([[H,S]].concat(kept.map(k=>[k.H,k.S])));
      const X=t=>X0+(X1-X0)*t/TMAX, Y=v=>Y0-(Y0-Y1)*(v-R.lo)/(R.hi-R.lo);
      for(let t=0;t<=TMAX;t+=300){ mk('line',{x1:X(t),y1:Y0,x2:X(t),y2:Y1,stroke:'#E2E7EC','stroke-width':1}); txt(X(t),Y0+22,String(t),{'font-size':16}); }
      for(let v=R.lo;v<=R.hi+1e-9;v+=R.st){ mk('line',{x1:X0,y1:Y(v),x2:X1,y2:Y(v),stroke:'#E2E7EC','stroke-width':1}); txt(X0-8,Y(v)+6,(v<0?M:'')+Math.abs(v),{'font-size':16,'text-anchor':'end'}); }
      mk('line',{x1:X0,y1:Y0,x2:X1+6,y2:Y0,stroke:MUT,'stroke-width':2}); mk('line',{x1:X0,y1:Y0,x2:X0,y2:Y1-6,stroke:MUT,'stroke-width':2});
      txt(X1,Y0+44,'온도 T [K]',{'text-anchor':'end',fill:MUT}); txt(X0+6,Y1-8,'ΔG° [kJ]',{'text-anchor':'start',fill:MUT});
      // 자발 구간
      let a=null,b=null; for(let t=0;t<=TMAX;t+=2){ if(G(H,S,t)<0){ if(a===null) a=t; b=t; } }
      if(a!==null){ mk('rect',{x:X(a),y:Y(0),width:X(b)-X(a),height:Y(R.lo)-Y(0),fill:FIELD,'fill-opacity':.15});
        if(X(b)-X(a)>70) txt((X(a)+X(b))/2,Y(R.lo)-10,'자발적',{fill:FIELD,'font-weight':700}); }
      mk('line',{x1:X0,y1:Y(0),x2:X1,y2:Y(0),stroke:MUT,'stroke-width':2,'stroke-dasharray':'7 5'});
      // 남긴 직선
      kept.forEach(k=>{ mk('line',{x1:X(0),y1:Y(G(k.H,k.S,0)),x2:X(TMAX),y2:Y(G(k.H,k.S,TMAX)),stroke:GRAV,'stroke-width':2.5,'stroke-dasharray':DASH[kase(k.H,k.S)]||null});
        k.pts.forEach(p=>mk('circle',{cx:X(p[0]),cy:Y(p[1]),r:4.5,fill:GRAV}));
        const ty=Y(G(k.H,k.S,TMAX)); txt(X1-4,ty+(ty<Y1+30?22:-8),k.name,{'text-anchor':'end','font-size':16,fill:GRAV}); });
      // ΔH° 선과 지금 직선
      mk('line',{x1:X0,y1:Y(H),x2:X1,y2:Y(H),stroke:RD,'stroke-width':2,'stroke-dasharray':'7 5'});
      txt(X1-4,Y(H)+(Y(H)<Y1+24?20:-8),'ΔH°',{'text-anchor':'end',fill:RD,'font-weight':700});
      const k=kase(H,S);
      mk('line',{x1:X(0),y1:Y(G(H,S,0)),x2:X(TMAX),y2:Y(G(H,S,TMAX)),stroke:INK,'stroke-width':3.5,'stroke-dasharray':DASH[k]||null,'stroke-linecap':'round'});
      const ts=tstar(H,S);
      if(ts!==null && ts<=TMAX){ mk('circle',{cx:X(ts),cy:Y(0),r:7,fill:'#FFFFFF',stroke:INK,'stroke-width':2.5}); txt(X(ts)+(S>0?-10:10),Y(0)+26,`${ts.toFixed(0)} K`,{'font-weight':700,'text-anchor':S>0?'end':'start'}); }
      // 지금 온도
      const gv=G(H,S,T);
      mk('line',{x1:X(T),y1:Y0,x2:X(T),y2:Y1,stroke:MUT,'stroke-width':1.5,'stroke-dasharray':'4 4'});
      if(Math.abs(Y(gv)-Y(H))>14) API.arrow(g,X(T),Y(H),X(T),Y(gv),'bfield',2.5);
      pts.forEach(p=>mk('circle',{cx:X(p[0]),cy:Y(p[1]),r:5.5,fill:PLUS,stroke:'#FFFFFF','stroke-width':1.5}));
      mk('circle',{cx:X(T),cy:Y(gv),r:6.5,fill:'#FFFFFF',stroke:INK,'stroke-width':2.5});
      // 출력
      O('h').textContent=`${sgn(H)} kJ`; O('s').textContent=`${sgn(S)} J/K`; O('t').textContent=`${T} K (${T-273} °C)`;
      O('g').textContent=`${sgn(gv)} kJ`;
      O('ts').textContent= ts===null ? '없음 (부호가 다름)' : `${ts.toFixed(0)} K`;
      const lab={'가':'(가) 저온에서 자발적','나':'(나) 항상 자발적','다':'(다) 항상 비자발적','라':'(라) 고온에서 자발적'}[k];
      O('case').textContent=lab;
      const now = gv<-1e-9 ? '자발적' : gv>1e-9 ? '비자발적(역반응이 자발적)' : '평형';
      let range='';
      if(k==='가') range=`T < ${ts.toFixed(0)} K에서 자발적`; else if(k==='라') range=`T > ${ts.toFixed(0)} K에서 자발적`;
      else if(k==='나') range='모든 온도에서 ΔG° < 0'; else range='모든 온도에서 ΔG° > 0';
      O('msg').textContent=`${name}: 절편 ΔH° = ${sgn(H)} kJ, 기울기 −ΔS° = ${fmt(-S/1000,4)} kJ/K → ${range}. 지금 ${T} K에서 ΔG° = ${sgn(gv)} kJ → ${now}.`;
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-4).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${r.no}</td><td>${r.name}</td><td>${sgn(r.H)}</td><td>${sgn(r.S)}</td><td>${r.T}</td><td>${sgn(r.g)}</td><td>${r.g<-1e-9?'자발적':r.g>1e-9?'비자발적':'평형'}</td>`; tb.appendChild(tr); }); }
    root.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{ setPreset(b.dataset.p); draw(); }));
    ['h','s'].forEach(k=>I(k).addEventListener('input',()=>{ pid=null; name='직접 입력'; pts=[]; markSeg(); read(); draw(); }));
    I('t').addEventListener('input',()=>{ read(); draw(); });
    $('[data-act="pt"]').addEventListener('click',()=>{ const gv=G(H,S,T); if(!pts.some(p=>p[0]===T)) pts.push([T,gv]); log.push({no:log.length+1,name,H,S,T,g:gv}); renderLog(); draw(); });
    $('[data-act="keep"]').addEventListener('click',()=>{ kept.push({name,H,S,pts:pts.slice()}); if(kept.length>3) kept.shift(); pts=[]; draw(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ init(); renderLog(); draw(); });
    init(); draw(); renderLog();
    API.ready(()=>draw()); API.onShow(s=>{ if(s===root.closest('.slide')) draw(); });
  }
};
})();
