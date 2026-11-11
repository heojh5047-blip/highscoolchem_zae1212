/* 3-3 화학 변화의 자발성 — 실험실 (덱 보충, 교과서 81쪽 「무질서도와 확률」 그림 Ⅲ-5 확장)
   em33coin : 동전 수 N(2–12)을 고르고 1번/100번 던지기 → 마지막 결과 동전 그림, 앞면 수별 실험 비율 막대와
              이론 확률 C(N,k)/2^N 점, "모두 같은 면" 횟수·비율과 이론 확률 2/2^N, 결과 표(동전 수마다 한 행).
   난수: mulberry32(시드 33) — 초기화하면 처음 수열로 돌아간다(재현 가능). 엔트로피 값은 계산하지 않는다(정성). */
window.DECK_LABS = {
  em33coin(root, API){
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), Ov=k=>$(`[data-ov="${k}"]`), I=k=>$(`[data-i="${k}"]`);
    const svg=$('svg'), g=API.mk('g',{},svg), W=660;
    const X0=78, X1=560, Y0=256, Y1=104;
    let rnd, data, last, order, spin;
    function mulberry(a){ return ()=>{ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
    function init(){ rnd=mulberry(33); data={}; last=null; order=[]; spin=0; I('n').value=4; }
    const N=()=>+I('n').value;
    const comb=(n,k)=>{ let r=1; for(let i=1;i<=k;i++) r=r*(n-k+i)/i; return r; };
    const pct=v=>{ const p=v*100; return (p>=1? p.toFixed(1) : p.toPrecision(2))+' %'; };
    const D=n=>data[n]||(data[n]={tot:0,same:0,hist:new Array(n+1).fill(0)});
    function throwOnce(n){ const c=[]; for(let i=0;i<n;i++) c.push(rnd()<0.5?1:0); const h=c.reduce((a,b)=>a+b,0), d=D(n);
      d.tot++; d.hist[h]++; if(h===0||h===n) d.same++; return c; }
    function doThrow(times){
      const n=N(); let c; for(let i=0;i<times;i++) c=throwOnce(n);
      last={n,c}; order=order.filter(x=>x!==n); order.push(n);
      spin=window.__STILL?0:0.6; update();
    }
    function controls(){ O('n').textContent=`${N()}개`; }
    function readout(){
      const n=N(), d=data[n], th=2/Math.pow(2,n);
      O('th').textContent=`2/${Math.pow(2,n)} = ${pct(th)}`;
      if(!d||!d.tot){ O('tot').textContent='0번'; O('same').textContent='–'; O('msg').textContent=`동전 ${n}개를 던져 보자. 모두 같은 면(모두 앞면 또는 모두 뒷면)이 나올 이론 확률은 ${pct(th)}이다.`; return; }
      O('tot').textContent=`${d.tot}번`; O('same').textContent=`${d.same}번 (${pct(d.same/d.tot)})`;
      let m=`동전 ${n}개를 ${d.tot}번 던져 모두 같은 면이 ${d.same}번(${pct(d.same/d.tot)}) 나왔다. 이론 확률은 ${pct(th)}이다.`;
      if(n>=8) m+=' 동전이 많을수록 모두 같은 면은 거의 나오지 않고, 앞면과 뒷면이 섞인 결과가 대부분이다 → 섞인(무질서한) 상태가 될 확률이 압도적으로 크다.';
      else if(n<=3) m+=' 동전이 적으면 모두 같은 면도 자주 나온다. 동전 수를 늘려 보자.';
      else m+=' 가운데(앞면과 뒷면이 반씩 섞인) 막대가 가장 높다. 동전 수를 늘리면 어떻게 될까?';
      O('msg').textContent=m;
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      order.slice(-4).forEach(n=>{ const d=data[n], tr=document.createElement('tr');
        tr.innerHTML=`<td>${n}</td><td>${d.tot}</td><td>${d.same}</td><td>${pct(d.same/d.tot)}</td><td>${pct(2/Math.pow(2,n))}</td>`; tb.appendChild(tr); }); }
    function drawCoins(){
      const mk=(t,a)=>API.mk(t,a,g);
      if(!last||last.n!==N()){ const t=mk('text',{x:W/2,y:42,'text-anchor':'middle','font-size':20,fill:'#5B6B7F'}); t.textContent=`동전 ${N()}개 — 「던지기」를 누르자`; return; }
      const n=last.n, sp=Math.min(52,(W-40)/n), x0=W/2-sp*(n-1)/2;
      const sx=spin>0? Math.abs(Math.cos(spin*18)) : 1;
      last.c.forEach((v,i)=>{ const x=x0+i*sp, face=spin>0?(Math.cos(spin*18)>0?v:1-v):v;
        mk('ellipse',{cx:x,cy:36,rx:Math.max(2,20*sx),ry:20,fill:face?'#E8C547':'#B9C2CC',stroke:face?'#A88A1E':'#7E8B98','stroke-width':2});
        if(sx>0.6){ const t=mk('text',{x,y:43,'text-anchor':'middle','font-size':19,'font-weight':700,fill:'#16233D'}); t.textContent=face?'앞':'뒤'; } });
      if(spin<=0){ const h=last.c.reduce((a,b)=>a+b,0), t=mk('text',{x:W-10,y:84,'text-anchor':'end','font-size':19,fill:(h===0||h===n)?'#B35F0F':'#2457A6','font-weight':700});
        t.textContent=(h===0||h===n)?'이번 결과: 모두 같은 면!':`이번 결과: 앞면 ${h}개, 뒷면 ${n-h}개`; }
    }
    function drawChart(){
      const mk=(t,a)=>API.mk(t,a,g), n=N(), d=data[n];
      const th=[...Array(n+1)].map((_,k)=>comb(n,k)/Math.pow(2,n));
      const ex=d&&d.tot? d.hist.map(c=>c/d.tot) : null;
      let ymax=Math.max(...th,...(ex||[0])); ymax=Math.max(0.2,Math.ceil(ymax*10)/10);
      const y=v=>Y0-(Y0-Y1)*v/ymax, step=(X1-X0)/(n+1), bw=step*0.62, xc=k=>X0+step*(k+0.5);
      [0,ymax/2,ymax].forEach(v=>{ mk('line',{x1:X0,y1:y(v),x2:X1,y2:y(v),stroke:'#E2E7EC','stroke-width':1});
        const t=mk('text',{x:X0-8,y:y(v)+6,'text-anchor':'end','font-size':18,fill:'#5B6B7F'}); t.textContent=v.toFixed(2); });
      API.arrow(g,X0,Y0+4,X0,Y1-18,'#5B6B7F',2.5); mk('line',{x1:X0,y1:Y0,x2:X1,y2:Y0,stroke:'#5B6B7F','stroke-width':2.5});
      for(let k=0;k<=n;k++){
        const end=(k===0||k===n);
        if(ex) mk('rect',{x:xc(k)-bw/2,y:y(ex[k]),width:bw,height:Y0-y(ex[k]),fill:end?'#FCE6CF':'#CFE0F5',stroke:end?'#E08A2C':'#3F7FD6','stroke-width':2});
        const t=mk('text',{x:xc(k),y:Y0+22,'text-anchor':'middle','font-size':18,fill:end?'#B35F0F':'#5B6B7F','font-weight':end?700:400}); t.textContent=k;
      }
      let dpath=''; th.forEach((v,k)=>{ dpath+=(k?'L':'M')+xc(k).toFixed(1)+' '+y(v).toFixed(1)+' '; });
      mk('path',{d:dpath,fill:'none',stroke:'#16233D','stroke-width':2,'stroke-dasharray':'6 4'});
      th.forEach((v,k)=>mk('circle',{cx:xc(k),cy:y(v),r:5,fill:'#16233D'}));
      mk('rect',{x:X1-170,y:Y1-12,width:16,height:14,fill:'#CFE0F5',stroke:'#3F7FD6','stroke-width':2});
      let t=mk('text',{x:X1-148,y:Y1,'font-size':18,fill:'#16233D'}); t.textContent='실험 비율';
      mk('circle',{cx:X1-48,cy:Y1-5,r:5,fill:'#16233D'});
      t=mk('text',{x:X1-36,y:Y1,'font-size':18,fill:'#16233D'}); t.textContent='이론 확률';
      Ov('ya').innerHTML='비율'; API.place(Ov('ya'),X0+8,Y1-34,true);
      Ov('xa').innerHTML='앞면의 수'; API.place(Ov('xa'),X1+10,Y0-14,true);
    }
    function draw(){ while(g.firstChild) g.removeChild(g.firstChild); drawCoins(); drawChart(); }
    function update(){ controls(); readout(); renderLog(); draw(); }
    $('[data-act="one"]').addEventListener('click',()=>doThrow(1));
    $('[data-act="hund"]').addEventListener('click',()=>doThrow(100));
    $('[data-act="reset"]').addEventListener('click',()=>{ init(); update(); });
    I('n').addEventListener('input',()=>{ spin=0; update(); });
    API.loop(root,dt=>{ if(spin<=0) return; spin=Math.max(0,spin-dt); draw(); });
    init(); API.ready(()=>update()); API.onShow(s=>{ if(s===root.closest('.slide')) draw(); });
    update();
  }
};
