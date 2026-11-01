/* 2-1-1 화학 결합의 전기적 성질 — 실험실
   cm211elec : 물의 전기 분해 실험실 (필수 탐구 화02-탐1 「물의 전기 분해 실험하기」)
     · 조작: 전해질(증류수만 / 황산 나트륨 수용액), 전압 3–9 V, 전류를 흘린 시간 0–10분
     · 모의 계산: 전류 I = (V − 1.8)/R (R: 황산 나트륨 20 Ω, 증류수 2000 Ω)
       수소 부피(mL) = I·t(s)/96485/2 × 24.5 L × 1000 (25 °C, 1 기압 가정 — 화면에는 식을 보이지 않음)
       산소 부피 = 수소 × 0.485 − 0.1 (산소가 물에 조금 더 녹음, 0 아래면 0), 측정값 = 계산값 + 고정 시드 오차(±0.1 mL)
     · 「측정 기록」→ 표(최근 4행)와 그래프(최근 12개)에 쌓인다. 「성냥불」「향불」로 기체 확인. 「초기화」. */
window.DECK_LABS = {
  cm211elec(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg');
    const MINUS='#1F6FD1', PLUS='#D7263D', MUTED='#5B6B7F', GLASS='#7E8B98', WATER='#DDEEF8', WE='#9FC3DD';
    const gS=API.mk('g',{},svg), gG=API.mk('g',{},svg), gB=API.mk('g',{},svg), gP=API.mk('g',{},svg);
    const XL=80, XR=200, W=22, TOP=30, BOT=210, BB=240, H0=TOP+W, HMAX=BOT-H0-12;   // 기체 30 mL = HMAX
    const GX=350, GY=250, GW=230, GH=210;
    let st={e:1}, log=[], bubbles=[], spawn=[0,0], flow=0, flowEls=[];

    const r1=v=>Math.round(v*10)/10;
    function noise(e,v,t,side){ let h=(e*131+Math.round(v*10)*17+t*29+side*7)%97; h=(h*h+11)%5; return [0,0.1,-0.1,0.1,-0.1][h]; }
    function calc(){
      const v=+I('v').value, t=+I('t').value, R=st.e?20:2000, cur=Math.max(0,(v-1.8)/R);
      let h=cur*t*60/96485/2*24.5*1000, o=Math.max(0,h*0.485-0.1);
      if(h>0.5) h+=noise(st.e,v,t,0); if(o>0.5) o+=noise(st.e,v,t,1);
      const full=h>30; h=Math.min(30,r1(h)); o=Math.min(30,r1(o));
      return {v,t,cur,h,o,full};
    }

    // 고정 그림: 장치·전원·도선·그래프 축
    function base(){
      const body=`M${XL-W} ${H0} A${W} ${W} 0 0 1 ${XL+W} ${H0} L${XL+W} ${BOT} L${XR-W} ${BOT} L${XR-W} ${H0} A${W} ${W} 0 0 1 ${XR+W} ${H0} L${XR+W} ${BB} L${XL-W} ${BB} Z`;
      API.mk('path',{d:body,fill:WATER},gS);
      st.body=body;
      // 도선·전원
      [[`M${XL} 262 L${XL} 280 L132 280`],[`M148 280 L${XR} 280 L${XR} 262`]].forEach(([d])=>API.mk('path',{d,fill:'none',stroke:'#16233D','stroke-width':3,'stroke-linejoin':'round'},gS));
      API.mk('line',{x1:132,y1:262,x2:132,y2:298,stroke:'#16233D','stroke-width':3},gS);
      API.mk('line',{x1:148,y1:271,x2:148,y2:289,stroke:'#16233D','stroke-width':6},gS);
      API.mk('line',{x1:116,y1:262,x2:126,y2:262,stroke:PLUS,'stroke-width':3},gS); API.mk('line',{x1:121,y1:257,x2:121,y2:267,stroke:PLUS,'stroke-width':3},gS);
      API.mk('line',{x1:154,y1:262,x2:164,y2:262,stroke:MINUS,'stroke-width':3},gS);
      flowEls=[`M${XL} 262 L${XL} 280 L132 280`,`M148 280 L${XR} 280 L${XR} 262`].map(d=>API.mk('path',{d,fill:'none',stroke:MINUS,'stroke-width':3,'stroke-dasharray':'4 10'},gS));
      // 그래프 축
      API.mk('line',{x1:GX,y1:GY,x2:GX+GW+12,y2:GY,stroke:MUTED,'stroke-width':2},gS);
      API.mk('line',{x1:GX,y1:GY,x2:GX,y2:GY-GH-12,stroke:MUTED,'stroke-width':2},gS);
      for(let k=1;k<=10;k++){ const x=GX+GW*k/10; API.mk('line',{x1:x,y1:GY,x2:x,y2:GY-GH,stroke:'#E2E7EC','stroke-width':1},gS); }
      for(let k=1;k<=4;k++){ const y=GY-GH*k/4; API.mk('line',{x1:GX,y1:y,x2:GX+GW,y2:y,stroke:'#E2E7EC','stroke-width':1},gS); }
      Ov('ax').innerHTML=API.tex('t')+' [분]'; Ov('ay').innerHTML=API.tex('V')+' [mL]';
    }
    function placeLabels(ymax){
      API.place(Ov('lp'),XL-16,BB+2); API.place(Ov('lm'),XR-16,BB+2);
      API.place(Ov('ax'),GX+GW-34,GY+20); API.place(Ov('ay'),GX+8,GY-GH-38);
      API.place(Ov('t0'),GX-6,GY+4); API.place(Ov('t10'),GX+GW-10,GY+4);
      Ov('y20').textContent=ymax; Ov('y10').textContent=ymax/2;
      API.place(Ov('y20'),GX-32,GY-GH-12); API.place(Ov('y10'),GX-32,GY-GH/2-12);
    }

    let cur={};
    function draw(){
      while(gG.firstChild) gG.removeChild(gG.firstChild);
      while(gP.firstChild) gP.removeChild(gP.firstChild);
      const c=cur;
      // 기체 기둥
      [[XL,c.o],[XR,c.h]].forEach(([x,vol])=>{ const hh=HMAX*vol/30;
        if(vol>0){ API.mk('path',{d:`M${x-W+2} ${H0} A${W-2} ${W-2} 0 0 1 ${x+W-2} ${H0} L${x+W-2} ${H0+hh} L${x-W+2} ${H0+hh} Z`,fill:'#FFFFFF'},gG);
          API.mk('line',{x1:x-W+2,y1:H0+hh,x2:x+W-2,y2:H0+hh,stroke:WE,'stroke-width':2},gG); } });
      API.mk('path',{d:st.body,fill:'none',stroke:GLASS,'stroke-width':3,'stroke-linejoin':'round'},gG);
      [XL,XR].forEach(x=>{ for(let k=0;k<10;k++){ const y=H0+8+k*HMAX/10; API.mk('line',{x1:x+W,y1:y,x2:x+W-(k%2?6:11),y2:y,stroke:MUTED,'stroke-width':1.4},gG); }
        API.mk('rect',{x:x-5,y:170,width:10,height:92,rx:2,fill:'#5B6B7F'},gG); });
      // 그래프 점
      const ymax=log.some(r=>r.h>20)||c.h>20?30:20; placeLabels(ymax);
      const px=t=>GX+GW*t/10, py=v=>GY-GH*v/ymax;
      log.slice(-12).forEach(r=>{ const fillM=r.e?MINUS:'#fff', fillP=r.e?PLUS:'#fff';
        API.mk('circle',{cx:px(r.t),cy:py(r.h),r:6,fill:fillM,stroke:MINUS,'stroke-width':2},gP);
        API.mk('rect',{x:px(r.t)-5.5,y:py(r.o)-5.5,width:11,height:11,fill:fillP,stroke:PLUS,'stroke-width':2},gP); });
      // 지금 값(고리)
      API.mk('circle',{cx:px(c.t),cy:py(c.h),r:9,fill:'none',stroke:MINUS,'stroke-width':1.5,'stroke-dasharray':'3 3'},gP);
      API.mk('circle',{cx:px(c.t),cy:py(c.o),r:9,fill:'none',stroke:PLUS,'stroke-width':1.5,'stroke-dasharray':'3 3'},gP);
      // 범례
      API.mk('circle',{cx:GX+20,cy:GY-GH+4,r:6,fill:MINUS},gP); API.mk('rect',{x:GX+14.5,y:GY-GH+20.5,width:11,height:11,fill:PLUS},gP);
      API.place(Ov('gm'),GX+32,GY-GH-8); API.place(Ov('gp'),GX+32,GY-GH+15);
    }

    function update(){
      cur=calc();
      O('v').textContent=cur.v.toFixed(1)+' V'; O('t').textContent=cur.t+'분';
      O('i').textContent=(cur.cur*1000).toFixed(cur.cur<0.01?1:0)+' mA';
      O('vm').textContent=cur.h.toFixed(1)+' mL'; O('vp').textContent=cur.o.toFixed(1)+' mL';
      O('r').textContent=cur.o>=0.5? (cur.h/cur.o).toFixed(1)+' : 1' : '—';
      root.querySelectorAll('[data-e]').forEach(b=>b.classList.toggle('on',+b.dataset.e===st.e));
      let m;
      if(!st.e) m='전류가 거의 흐르지 않아 기체가 거의 생기지 않는다 — 전해질이 필요하다.';
      else if(cur.t===0) m='시간을 늘려 전류를 흘려 보자. 기포는 어느 전극에서 더 많이 생길까?';
      else if(cur.full) m='(−)극 관이 가득 찼다. 전압이나 시간을 줄여 보자.';
      else m='(−)극 기체 부피가 (+)극의 약 2배이다 — 수소 : 산소 ≈ 2 : 1. 전압을 바꾸어도 부피비는 그대로이다.';
      O('msg').textContent=m;
      draw();
    }

    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-4).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${r.e?'황산 나트륨':'증류수'}</td><td>${r.v.toFixed(1)} V</td><td>${r.t}분</td><td>${r.h.toFixed(1)} mL</td><td>${r.o.toFixed(1)} mL</td><td>${r.o>=0.5?(r.h/r.o).toFixed(1)+' : 1':'—'}</td>`; tb.appendChild(tr); }); }

    root.querySelectorAll('[data-e]').forEach(b=>b.addEventListener('click',()=>{ st.e=+b.dataset.e; update(); }));
    ['v','t'].forEach(k=>I(k).addEventListener('input',update));
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ log.push({e:st.e,v:cur.v,t:cur.t,h:cur.h,o:cur.o}); if(log.length>30) log.shift(); renderLog(); draw(); });
    root.querySelector('[data-act="h2"]').addEventListener('click',()=>{ O('msg').textContent= cur.h>=2? "성냥불을 대니 '펑' 소리를 내며 탄다 → (−)극 기체는 수소이다." : '기체가 너무 적어 확인하기 어렵다. 시간을 늘려 보자.'; });
    root.querySelector('[data-act="o2"]').addEventListener('click',()=>{ O('msg').textContent= cur.o>=2? '꺼져 가던 향불이 다시 타오른다 → (+)극 기체는 산소이다.' : '기체가 너무 적어 확인하기 어렵다. 시간을 늘려 보자.'; });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; st.e=1; I('v').value=6; I('t').value=0; renderLog(); update(); });

    base(); update();
    // 기포·전자 흐름 (보일 때만)
    if(!window.__STILL) API.loop(root,dt=>{
      const rate=cur.t>0?cur.cur*40:0;             // 6 V·황산 나트륨: 초당 약 8개 (수소 쪽)
      flow=(flow+dt*Math.min(60,cur.cur*240))%14; flowEls.forEach(p=>p.setAttribute('stroke-dashoffset',(-flow).toFixed(1)));
      [[XL,0.5,cur.o],[XR,1,cur.h]].forEach(([x,k,vol],i)=>{ spawn[i]+=dt*rate*k;
        while(spawn[i]>=1){ spawn[i]-=1; if(bubbles.length<60) bubbles.push({x:x+(Math.random()*14-7),y:172,top:H0+HMAX*vol/30+6,r:2.5+Math.random()*2}); } });
      while(gB.firstChild) gB.removeChild(gB.firstChild);
      bubbles=bubbles.filter(b=>{ b.y-=dt*70; if(b.y<b.top) return false;
        API.mk('circle',{cx:b.x.toFixed(1),cy:b.y.toFixed(1),r:b.r.toFixed(1),fill:'#fff',stroke:WE,'stroke-width':1.3},gB); return true; });
    });
  }
};
