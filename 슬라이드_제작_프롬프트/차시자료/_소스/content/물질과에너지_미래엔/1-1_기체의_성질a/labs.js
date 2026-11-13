/* 1-1a 기체의 성질 (1) 기체 법칙 — 실험실
   em11gaslaw : 기체 법칙 모의실험 (성취기준 적용 시 고려 사항: 모의실험으로 압력–부피, 온도–부피, 몰수–부피 관계 파악)
     · 실험 Ⅰ 압력–부피(T 300 K, n 1.0 mol), Ⅱ 온도–부피(P 1.0 atm, n 1.0 mol), Ⅲ 양–부피(P 1.0 atm, T 300 K)
     · V = nRT/P, R = 0.082. 측정값 = 계산값 × (1 ± 0.6 % 고정 시드 오차)
     · 실린더: 피스톤 높이 ∝ V(6 px/L), 분자 수 24n, 속력 ∝ √T, 바탕 온도색, 추 개수 ∝ P
     · 「측정 기록」 → 표(최근 5행) + 그래프 점, 2점 이상이면 맞춤 곡선·직선과 해석 문장. 「초기화」 */
window.DECK_LABS = {
  em11gaslaw(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg'), fig=$('.lab-fig'), R=0.082;
    const gBg=API.mk('g',{},svg), gP=API.mk('g',{},svg), gCyl=API.mk('g',{},svg), gGr=API.mk('g',{},svg);
    const CX=40, CW=170, CB=370, PX=6;            // 실린더 왼쪽, 폭, 바닥, 1 L당 px
    const GX=310, GY=330, GW=340, GH=270;         // 그래프 원점·크기
    let mode=1, log=[], seed=7, parts=[], ticks=[];
    const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    const prng=(s=>()=>{ s=(s*48271)%2147483647; return s/2147483647; })(11);
    const st=()=>({P:mode===1?+I('P').value:1, T:mode===2?+I('t').value+273:300, n:mode===3?+I('n').value:1});
    const vol=s=>s.n*R*s.T/s.P;
    const AX={1:{x:[0,4.5],y:[0,55],xt:[0,1,2,3,4],yt:[0,10,20,30,40,50],xs:'P',xu:'[atm]',k:'PV'},
              2:{x:[-300,220],y:[0,45],xt:[-273,-200,-100,0,100,200],yt:[0,10,20,30,40],xs:'t',xu:'[°C]',k:'V/T'},
              3:{x:[0,2.2],y:[0,55],xt:[0,0.5,1,1.5,2],yt:[0,10,20,30,40,50],xs:'n',xu:'[mol]',k:'V/n'}};
    const X=v=>GX+(v-AX[mode].x[0])/(AX[mode].x[1]-AX[mode].x[0])*GW, Y=v=>GY-(v-AX[mode].y[0])/(AX[mode].y[1]-AX[mode].y[0])*GH;
    const x0px=()=>mode===2?X(0):GX;
    function tick(txt,x,y,anchor){ const d=document.createElement('div'); d.className='ov'+(anchor==='mid'?'':''); d.style.fontSize='18px'; d.textContent=txt; fig.appendChild(d); ticks.push(d);
      if(anchor==='end'){ d.style.transform='translate(-100%,-50%)'; } else d.style.transform='translate(-50%,0)'; API.place(d,x,y); }
    function axes(){
      ticks.forEach(d=>d.remove()); ticks=[]; gGr.innerHTML='';
      const a=AX[mode], yx=x0px();
      a.xt.forEach(v=>{ API.mk('line',{x1:X(v),y1:GY,x2:X(v),y2:GY-GH,stroke:'#E3E8EE','stroke-width':1.2},gGr); });
      a.yt.forEach(v=>{ API.mk('line',{x1:GX,y1:Y(v),x2:GX+GW,y2:Y(v),stroke:'#E3E8EE','stroke-width':1.2},gGr); });
      API.arrow(gGr,GX,GY,GX+GW+18,GY,'muted',2); API.arrow(gGr,yx,GY,yx,GY-GH-18,'muted',2);
      a.xt.forEach(v=>{ if(mode===2&&v===0) return; tick(String(v).replace('-','−'),X(v),GY+6); });
      a.yt.forEach(v=>{ if(v===0&&mode!==2) return; tick(String(v),yx-8,Y(v),'end'); });
      Ov('xl').innerHTML=API.tex(a.xs)+' '+a.xu; API.place(Ov('xl'),GX+GW-10,GY+30);
      Ov('yl').style.transform='none'; API.place(Ov('yl'),yx+10,GY-GH-26);
      O('kh').textContent=a.k;
    }
    function fmt(v,d){ return v.toFixed(d); }
    function graph(){
      [...gGr.querySelectorAll('.dyn')].forEach(e=>e.remove());
      const pts=log.map(r=>mode===1?[r.P,r.V]:mode===2?[r.T-273,r.V]:[r.n,r.V]);
      let msg='조작 변인을 바꾸며 「측정 기록」을 눌러 보자.';
      if(pts.length>=2){
        if(mode===1){ const k=log.reduce((s,r)=>s+r.P*r.V,0)/log.length; let d='';
          for(let p=0.45;p<=4.5;p+=0.05){ const v=k/p; if(v>55) continue; d+=(d?'L':'M')+X(p).toFixed(1)+' '+Y(v).toFixed(1); }
          API.mk('path',{d,fill:'none',stroke:'#2E9E6A','stroke-width':2.5,class:'dyn'},gGr);
          msg=`PV 값이 거의 일정하다(약 ${fmt(k,1)}) → 온도와 기체의 양이 일정할 때 부피는 압력에 반비례한다(보일 법칙).`; }
        if(mode===2){ const n=pts.length, sx=pts.reduce((s,p)=>s+p[0],0), sy=pts.reduce((s,p)=>s+p[1],0), sxx=pts.reduce((s,p)=>s+p[0]*p[0],0), sxy=pts.reduce((s,p)=>s+p[0]*p[1],0);
          const den=n*sxx-sx*sx;
          if(Math.abs(den)>1e-6){ const a=(n*sxy-sx*sy)/den, b=(sy-a*sx)/n, t0=-b/a, tmin=Math.min(...pts.map(p=>p[0]));
            API.mk('line',{x1:X(t0),y1:Y(0),x2:X(tmin),y2:Y(a*tmin+b),stroke:'#5B6B7F','stroke-width':2.5,'stroke-dasharray':'7 6',class:'dyn'},gGr);
            API.mk('line',{x1:X(tmin),y1:Y(a*tmin+b),x2:X(210),y2:Y(a*210+b),stroke:'#2E9E6A','stroke-width':2.5,class:'dyn'},gGr);
            API.mk('circle',{cx:X(t0),cy:Y(0),r:6,fill:'#fff',stroke:'#D7263D','stroke-width':3,class:'dyn'},gGr);
            msg=`직선을 연장하면 약 ${String(Math.round(t0)).replace('-','−')} °C에서 부피가 0이 된다 → 부피는 절대 온도에 비례한다(샤를 법칙). V/T ≈ ${fmt(log.reduce((s,r)=>s+r.V/r.T,0)/log.length,4)}`; }
          else msg='온도를 바꾸어 두 번 이상 측정하자.'; }
        if(mode===3){ const k=log.reduce((s,r)=>s+r.V/r.n,0)/log.length;
          API.mk('line',{x1:X(0),y1:Y(0),x2:X(2.15),y2:Y(k*2.15),stroke:'#2E9E6A','stroke-width':2.5,class:'dyn'},gGr);
          msg=`V/n 값이 거의 일정하다(약 ${fmt(k,1)}) → 온도와 압력이 일정할 때 부피는 기체의 양(몰수)에 비례한다(아보가드로 법칙).`; }
      }
      pts.forEach(p=>API.mk('circle',{cx:X(p[0]),cy:Y(p[1]),r:6,fill:'#16233D',class:'dyn'},gGr));
      O('msg').textContent=msg;
    }
    function table(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-5).forEach(r=>{ const tr=document.createElement('tr'); const kv=mode===1?fmt(r.P*r.V,1):mode===2?fmt(r.V/r.T,4):fmt(r.V/r.n,1);
        tr.innerHTML=`<td>${fmt(r.P,2)}</td><td>${r.T-273}</td><td>${fmt(r.n,2)}</td><td>${fmt(r.V,2)}</td><td>${kv}</td>`; tb.appendChild(tr); }); }
    function syncParts(n,top){ const want=Math.round(24*n), H=CB-top-18;
      if(window.__STILL) parts.forEach(p=>{ p.y=CB-9-prng()*H; });
      while(parts.length<want) parts.push({x:CX+12+prng()*(CW-24), y:CB-9-prng()*H, a:prng()*Math.PI*2, el:API.mk('circle',{r:7,fill:'#6C8EBF',stroke:'#3E5F8F','stroke-width':1.5},gP)});
      while(parts.length>want) parts.pop().el.remove(); }
    function cyl(){
      const s=st(), V=vol(s), h=Math.min(300,V*PX), top=CB-h;
      gBg.innerHTML=''; gCyl.innerHTML='';
      const f=API.clamp((s.T-223)/250,0,1), mix=(a,b)=>Math.round(a+(b-a)*f);
      API.mk('rect',{x:CX,y:top,width:CW,height:h,fill:`rgb(${mix(227,253)},${mix(238,226)},${mix(251,228)})`},gBg);
      API.mk('rect',{x:CX+2,y:top-12,width:CW-4,height:12,rx:2,fill:'#B7C2CE',stroke:'#7E8B98','stroke-width':2},gCyl);
      API.mk('rect',{x:CX+CW/2-6,y:top-40,width:12,height:28,fill:'#C9D3DD',stroke:'#7E8B98','stroke-width':2},gCyl);
      const nw=Math.round(s.P*2);
      for(let i=0;i<nw;i++){ const row=Math.floor(i/4), col=i%4; API.mk('rect',{x:CX+CW/2-58+col*29,y:top-40-16-row*16,width:26,height:14,rx:2,fill:'#5B6B7F'},gCyl); }
      API.mk('path',{d:`M${CX} 20 V${CB} H${CX+CW} V20`,fill:'none',stroke:'#7E8B98','stroke-width':3},gCyl);
      for(let L=10;L<=50;L+=10){ const y=CB-L*PX; API.mk('line',{x1:CX+CW,y1:y,x2:CX+CW+10,y2:y,stroke:'#5B6B7F','stroke-width':1.5},gCyl); }
      cyl.top=top; cyl.sp=60*Math.sqrt(s.T/300); syncParts(s.n,top);
      parts.forEach(p=>{ p.y=API.clamp(p.y,top+9,CB-9); p.el.setAttribute('cx',p.x.toFixed(1)); p.el.setAttribute('cy',p.y.toFixed(1)); });
      return {s,V};
    }
    function update(){
      const {s,V}=cyl();
      O('P').textContent=fmt(s.P,2)+' atm'; O('t').textContent=(s.T-273)+' °C ('+s.T+' K)'; O('n').textContent=fmt(s.n,2)+' mol';
      O('fix').textContent=mode===1?'통제 변인: T = 300 K, n = 1.00 mol':mode===2?'통제 변인: P = 1.00 atm, n = 1.00 mol':'통제 변인: P = 1.00 atm, T = 300 K';
      O('V').textContent=fmt(V,2)+' L';
    }
    function setMode(m){ mode=m; log=[];
      root.querySelectorAll('[data-x]').forEach(b=>b.classList.toggle('on',+b.dataset.x===m));
      root.querySelectorAll('[data-c]').forEach(c=>c.style.display=(+c.dataset.c===m)?'':'none');
      axes(); table(); graph(); update(); }
    root.querySelectorAll('[data-x]').forEach(b=>b.addEventListener('click',()=>setMode(+b.dataset.x)));
    ['P','t','n'].forEach(k=>I(k).addEventListener('input',update));
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const s=st(), V=vol(s)*(1+0.012*(rnd()-.5));
      log.push({P:s.P,T:s.T,n:s.n,V:Math.round(V*100)/100}); if(log.length>12) log.shift(); table(); graph(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ I('P').value=1; I('t').value=27; I('n').value=1; seed=7; setMode(1); });
    API.onShow&&API.onShow(()=>{ axes(); graph(); });
    setMode(1);
    if(!window.__STILL) API.loop(root,dt=>{ const top=cyl.top, sp=cyl.sp; dt=Math.min(dt,.05);
      parts.forEach(p=>{ p.x+=Math.cos(p.a)*sp*dt; p.y+=Math.sin(p.a)*sp*dt;
        if(p.x<CX+9){p.x=CX+9;p.a=Math.PI-p.a;} if(p.x>CX+CW-9){p.x=CX+CW-9;p.a=Math.PI-p.a;}
        if(p.y<top+9){p.y=top+9;p.a=-p.a;} if(p.y>CB-9){p.y=CB-9;p.a=-p.a;}
        p.el.setAttribute('cx',p.x.toFixed(1)); p.el.setAttribute('cy',p.y.toFixed(1)); }); });
  }
};
