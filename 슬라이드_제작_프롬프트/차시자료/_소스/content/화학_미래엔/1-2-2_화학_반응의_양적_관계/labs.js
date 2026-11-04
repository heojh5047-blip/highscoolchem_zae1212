/* 1-2-2 화학 반응의 양적 관계 — 실험실
   cm122mg : 마그네슘과 염산 — 마그네슘의 양을 바꾸며 수소 부피 재기 (필수 탐구 화01-탐2)
     · 염산 50 mL: 충분(1 M, HCl 50 mmol) / 적게(0.1 M, HCl 5 mmol)
     · 마그네슘 질량 0.01–0.10 g → 양(mmol), 예상 수소 부피(실험실 기체 1 몰 = 24 L)
     · 오차 요인(계획서 보완 토의): 산화막(반응하는 Mg ×0.93), 마개 늦게(기체 −6 %), 식기 전에 읽음(×1.05)
     · 「반응시키고 측정」 → 고정 시드 잡음(±1.5 %)을 넣은 측정값을 표에 쌓고 그래프에 점을 찍음, 피스톤이 밀려 나가는 움직임
     · 100 mL를 넘으면 측정 실패 행, 「초기화」 */
window.DECK_LABS = {
  cm122mg(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=$('svg'), S=0.66, TX=0, TY=14;           // 장치 축척(그림 좌표 → 화면)
    const VM=24;                                       // mL/mmol (실험실 기체 1 몰 = 24 L)
    const HCL={hi:{nm:'충분', n:50}, lo:{nm:'적게', n:5}};
    let st={h:'hi'}, log=[], seed=122, anim=null, shown=0;
    const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    // ── 고정 그림 ──
    const back=API.mk('g',{transform:`translate(${TX},${TY}) scale(${S})`},svg);
    const P=(d,a)=>API.mk('path',Object.assign({d},a),back);
    P('M196 80 C 236 72, 246 120, 302 120',{fill:'none',stroke:'#B9824F','stroke-width':8,'stroke-linecap':'round'});
    P('M116 62 V110 L50 236 Q46 250 62 250 H198 Q214 250 210 236 L144 110 V62',{fill:'#F7FAFC',stroke:'#7E8B98','stroke-width':3.5,'stroke-linejoin':'round'});
    P('M78.6 186 H181.4 L208 238 Q211 248 198 248 H62 Q49 248 52 238 Z',{fill:'#E6F1F8'});
    P('M144 82 L196 76 V86 L144 92 Z',{fill:'#F7FAFC',stroke:'#7E8B98','stroke-width':3,'stroke-linejoin':'round'});
    P('M110 44 H150 L146 72 H114 Z',{fill:'#6FA8C8',stroke:'#16233D','stroke-width':2.5,'stroke-linejoin':'round'});
    API.mk('rect',{x:300,y:114,width:22,height:12,rx:3,fill:'#F7FAFC',stroke:'#7E8B98','stroke-width':2.5},back);
    API.mk('rect',{x:322,y:104,width:216,height:32,rx:4,fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':3},back);
    const gas=API.mk('rect',{x:330,y:107,width:0,height:26,fill:'#DCEFFB'},back);
    for(let v=0;v<=100;v+=10) API.mk('line',{x1:330+2*v,y1:104,x2:330+2*v,y2:v%50?112:116,stroke:'#5B6B7F','stroke-width':1.6},back);
    API.mk('rect',{x:538,y:98,width:8,height:44,rx:2,fill:'#C9D3DD',stroke:'#7E8B98','stroke-width':2},back);
    const pist=API.mk('g',{},back);
    API.mk('rect',{x:324,y:106,width:10,height:28,rx:2,fill:'#3A3F47'},pist);
    API.mk('rect',{x:334,y:116,width:150,height:8,fill:'#C9D3DD',stroke:'#7E8B98','stroke-width':1.5},pist);
    API.mk('rect',{x:484,y:100,width:8,height:40,rx:2,fill:'#9AA5B1',stroke:'#7E8B98','stroke-width':1.5},pist);
    const rib=API.mk('path',{d:'M98 238 l8 -8 l8 8 l8 -8 l8 8 l8 -8 l8 8 l8 -8',fill:'none',stroke:'#8E959E','stroke-width':5,'stroke-linecap':'round','stroke-linejoin':'round'},back);
    const bub=API.mk('g',{},back);
    const BB=[[106,0,5],[122,.3,6],[138,.6,4.5],[150,.15,5.5],[116,.8,4]].map(([x,ph,r])=>({x,ph,c:API.mk('circle',{cx:x,cy:230,r,fill:'#FFFFFF','fill-opacity':.75,stroke:'#7FB6D9','stroke-width':1.8,opacity:0},bub)}));
    const sx=x=>TX+S*x, sy=y=>TY+S*y;
    API.texText(svg,sx(330),sy(160),'0',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    API.texText(svg,sx(430),sy(160),'50',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    API.texText(svg,sx(522),sy(160),'100',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    API.texText(svg,sx(434),sy(196),'주사기(mL)',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    API.texText(svg,sx(130),sy(282),'염산 50 mL + Mg 리본',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    // ── 그래프 ──
    const GX0=478, GX1=630, GY0=200, GYT=34, NX=4.5, VY=110;
    const gx=n=>GX0+(GX1-GX0)*n/NX, gy=v=>GY0-(GY0-GYT)*v/VY;
    const ga=API.mk('g',{},svg);
    [50,100].forEach(v=>{ API.mk('line',{x1:GX0,y1:gy(v),x2:GX1,y2:gy(v),stroke:'#E2E7EC','stroke-width':1.5},ga);
      API.texText(svg,GX0-6,gy(v)+6,String(v),{size:18,anchor:'end',fill:'#5B6B7F',mix:true}); });
    [0,2,4].forEach(n=>{ API.mk('line',{x1:gx(n),y1:GY0,x2:gx(n),y2:GY0+5,stroke:'#5B6B7F','stroke-width':1.6},ga);
      API.texText(svg,gx(n),GY0+24,String(n),{size:18,anchor:'middle',fill:'#5B6B7F',mix:true}); });
    API.arrow(ga,GX0,GY0,GX1+12,GY0,'muted',2); API.arrow(ga,GX0,GY0,GX0,GYT-16,'muted',2);
    API.texText(svg,GX0+6,GYT-10,'$V$ [mL]',{size:18,anchor:'start',mix:true});
    API.texText(svg,GX1+8,GY0+46,'Mg의 양 [mmol]',{size:18,anchor:'end',mix:true});
    const gl=API.mk('g',{},svg), gp=API.mk('g',{},svg);
    // ── 계산 ──
    const mass=()=>+$('[data-i="m"]').value/100;                    // g
    const err=k=>$(`[data-e="${k}"]`).checked;
    const nMg=m=>m/24*1000;                                         // mmol
    const ideal=m=>Math.min(nMg(m),HCL[st.h].n/2)*VM;               // 오차 없는 예상 부피 (mL)
    function measure(m){
      let react=nMg(m)*(err('ox')?0.93:1);
      react=Math.min(react,HCL[st.h].n/2);
      let V=react*VM*(err('late')?0.94:1)*(err('hot')?1.05:1);
      V*=1+(rnd()*2-1)*0.015;
      return V;
    }
    function setPiston(V){ const v=Math.max(0,Math.min(100,V)); gas.setAttribute('width',(2*v).toFixed(1)); pist.setAttribute('transform',`translate(${(2*v).toFixed(1)},0)`);
      const ov=$('[data-ov="rd"]'); ov.textContent=`${v.toFixed(1)} mL`; API.place(ov,sx(430),sy(64)); }
    function drawLines(){
      while(gl.firstChild) gl.removeChild(gl.firstChild);
      const pts=st.h==='hi'?[[0,0],[4.5,108]]:[[0,0],[2.5,60],[4.5,60]];
      API.mk('path',{d:'M'+pts.map(([n,v])=>`${gx(n).toFixed(1)} ${gy(v).toFixed(1)}`).join(' L'),fill:'none',stroke:'#5B6B7F','stroke-width':2,'stroke-dasharray':'6 5'},gl);
      while(gp.firstChild) gp.removeChild(gp.firstChild);
      log.filter(x=>!x.over).forEach(x=>API.mk('circle',{cx:gx(x.n).toFixed(1),cy:gy(x.V).toFixed(1),r:5.5,
        fill:x.h==='hi'?'#16233D':'#FFFFFF',stroke:x.h==='hi'?'#16233D':'#E08A2C','stroke-width':2.5},gp));
    }
    function draw(){
      const m=mass(), n=nMg(m);
      O('m').textContent=`${m.toFixed(2)} g`;
      O('n').textContent=`${n.toFixed(2)} mmol`;
      const vi=ideal(m);
      O('vp').textContent=nMg(m)*VM>100?`${(n*VM).toFixed(1)} mL (주사기 넘침)`:`${vi.toFixed(1)} mL`;
      root.querySelectorAll('[data-h]').forEach(b=>b.classList.toggle('on',b.dataset.h===st.h));
      drawLines();
    }
    function renderLog(){
      O('log').innerHTML=log.slice(-5).map(x=>x.over
        ? `<tr><td>${x.i}</td><td>${HCL[x.h].nm}</td><td>${x.m.toFixed(2)}</td><td>${x.n.toFixed(2)}</td><td class="cm122-ng">100 넘음</td><td>—</td><td class="cm122-ng">측정 실패</td></tr>`
        : `<tr><td>${x.i}</td><td>${HCL[x.h].nm}</td><td>${x.m.toFixed(2)}</td><td>${x.n.toFixed(2)}</td><td>${x.V.toFixed(1)}</td><td>${(x.V/VM).toFixed(2)}</td><td class="${Math.abs(x.V/VM/x.n-1)<0.04?'cm122-ok':''}">1 : ${(x.V/VM/x.n).toFixed(2)}</td></tr>`).join('')
        || '<tr><td colspan="7" class="c-muted">질량을 정하고 「반응시키고 측정」을 누르면 여기에 쌓인다.</td></tr>';
    }
    function msgFor(x){
      const ex=[]; if(err('ox')) ex.push('산화막 때문에 일부 마그네슘이 반응하지 않았다'); if(err('late')) ex.push('마개를 닫기 전에 기체가 빠져나갔다'); if(err('hot')) ex.push('기체가 식기 전이라 팽창해 있다');
      if(x.over) return '생긴 기체가 100 mL를 넘어 피스톤이 빠졌다 — 측정 실패. 마그네슘을 줄여 다시 계획하자.';
      const left=x.n-HCL[x.h].n/2;
      if(x.h==='lo'&&left>0.05) return `HCl 5 mmol이 모두 소모되어 Mg ${left.toFixed(2)} mmol이 남았다 — 수소는 2.5 mmol(60 mL)보다 늘지 않는다.`;
      const vi=ideal(x.m), d=(x.V-vi)/vi*100;
      if(ex.length&&Math.abs(d)>2.5) return `예상값 ${vi.toFixed(1)} mL보다 ${Math.abs(d).toFixed(0)} % ${d<0?'작다':'크다'} — 까닭: ${ex.join(', ')}.`;
      return `Mg ${x.n.toFixed(2)} mmol → 수소 ${(x.V/VM).toFixed(2)} mmol: 몰비 1 : ${(x.V/VM/x.n).toFixed(2)} — 화학 반응식의 계수비(1 : 1)와 거의 같다.`;
    }
    function run(){
      const m=mass(), n=nMg(m), V=measure(m), over=V>100;
      const x={i:log.length+1,h:st.h,m,n,V,over}; log.push(x);
      O('msg').textContent=msgFor(x); renderLog(); drawLines();
      anim={t:0,from:0,to:over?100:V,ribbon:Math.min(1,(HCL[st.h].n/2)/n)};
      if(!API.isActive(root)) finish();
    }
    function finish(){ if(!anim) return; setPiston(anim.to); rib.setAttribute('opacity',(1-anim.ribbon*0.85).toFixed(2)); BB.forEach(b=>b.c.setAttribute('opacity',0)); anim=null; }
    root.querySelectorAll('[data-h]').forEach(b=>b.addEventListener('click',()=>{ st.h=b.dataset.h; draw(); }));
    $('[data-i="m"]').addEventListener('input',draw);
    root.querySelectorAll('[data-e]').forEach(c=>c.addEventListener('change',draw));
    $('[data-act="run"]').addEventListener('click',run);
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; seed=122; anim=null; st.h='hi'; $('[data-i="m"]').value=4;
      root.querySelectorAll('[data-e]').forEach(c=>c.checked=false); setPiston(0); rib.setAttribute('opacity',1);
      O('msg').textContent='질량을 정하고 「반응시키고 측정」을 누르자. 먼저 예상 부피를 계산해 보자.'; renderLog(); draw(); });
    API.loop(root,(dt)=>{
      if(!anim) return;
      anim.t+=dt/1.8; const p=Math.min(1,anim.t), e=1-Math.pow(1-p,2);
      setPiston(anim.from+(anim.to-anim.from)*e);
      rib.setAttribute('opacity',(1-anim.ribbon*0.85*e).toFixed(2));
      BB.forEach(b=>{ const q=(anim.t*1.6+b.ph)%1; b.c.setAttribute('cy',(232-46*q).toFixed(1)); b.c.setAttribute('opacity',p<1?(0.9*(1-q*0.6)).toFixed(2):0); });
      if(p>=1) finish();
    });
    API.ready(()=>{ setPiston(0); });
    O('msg').textContent='질량을 정하고 「반응시키고 측정」을 누르자. 먼저 예상 부피를 계산해 보자.';
    setPiston(0); renderLog(); draw();
  }
};
