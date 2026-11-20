/* 1-2 혼합 기체의 부분 압력과 몰분율 — 실험실
   em12mix : 해 보기(18쪽) 「혼합 기체의 압력과 성분 기체의 압력 사이 관계 알아보기」를 넓힌 모의실험
     · 27 °C(300 K), 부피 24.6 L 고정 → RT/V = 0.082×300/24.6 = 1 (1 mol당 1 기압)
     · 산소·질소의 양(0–2 mol) → P_O2 = n_O2·RT/V, P_N2 = n_N2·RT/V, P = P_O2 + P_N2, X_O2 = n_O2/(n_O2+n_N2)
     · 「산소만」「질소만」「혼합」: 용기에 남길 기체 — 압력계는 남은 기체의 압력(= 그 기체의 부분 압력)
     · 분자 1 mol당 5개, 무작위 운동(API.loop). 오른쪽 쌓은 막대 = 부분 압력. 「측정 기록」→ 표(최근 4행) */
window.DECK_LABS = {
  em12mix(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=root.querySelector('svg'), R=0.082, T=300, V=24.6, K=R*T/V;
    const box={x:20,y:28,w:300,h:214}, gx=420, gy=140, gr=66, bx=560, bw=60, base=236, u=46;
    const gBox=API.mk('g',{},svg), gP=API.mk('g',{},svg), gG=API.mk('g',{},svg), gB=API.mk('g',{},svg);
    let mode='M', log=[], parts={O:[],N:[]};
    let seed=7; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    // 고정 그림: 용기, 관, 막대 축
    API.mk('rect',{x:box.x,y:box.y,width:box.w,height:box.h,rx:14,fill:'#F4F8FB',stroke:'#7E8B98','stroke-width':3},gBox);
    API.mk('path',{d:`M${box.x+box.w} ${gy} H${gx-gr}`,stroke:'#7E8B98','stroke-width':6},gBox);
    API.mk('line',{x1:bx-20,y1:base,x2:bx+bw+20,y2:base,stroke:'#5B6B7F','stroke-width':2},gBox);
    API.mk('line',{x1:bx-20,y1:base,x2:bx-20,y2:base-4*u-6,stroke:'#5B6B7F','stroke-width':2},gBox);
    for(let k=0;k<=4;k++){ API.mk('line',{x1:bx-26,y1:base-k*u,x2:bx-20,y2:base-k*u,stroke:'#5B6B7F','stroke-width':2},gBox); API.texText(gBox,bx-32,base-k*u+6,String(k),{size:18,anchor:'end'}); }
    API.texText(gBox,bx+bw/2,22,'\\text{부분 압력 [atm]}',{size:19,anchor:'middle'});
    API.texText(gBox,gx,gy+gr+30,'\\text{압력계 [atm]}',{size:19,anchor:'middle'});
    function mkMol(el){ const g=API.mk('g',{},gP); API.atom(g,-8,0,11,el,'-',false); API.atom(g,8,0,11,el,'-',false);
      return {g, x:box.x+24+rnd()*(box.w-48), y:box.y+24+rnd()*(box.h-48), a:rnd()*6.283, rot:rnd()*180}; }
    function setPos(p){ p.g.setAttribute('transform',`translate(${p.x.toFixed(1)} ${p.y.toFixed(1)}) rotate(${p.rot.toFixed(0)})`); }
    const st=()=>({nO:+I('nO').value, nN:+I('nN').value});
    function draw(){
      const s=st(), PO=s.nO*K, PN=s.nN*K, P=PO+PN, nt=s.nO+s.nN;
      ['O','N'].forEach(el=>{ const want=Math.round(5*(el==='O'?s.nO:s.nN)), L=parts[el];
        while(L.length<want){ const p=mkMol(el); setPos(p); L.push(p); }
        while(L.length>want) L.pop().g.remove();
        const show=mode==='M'||mode===el; L.forEach(p=>p.g.style.display=show?'':'none'); });
      const Pg=mode==='O'?PO:mode==='N'?PN:P;
      // 압력계
      gG.innerHTML=''; const a0=Math.PI*0.8, a1=Math.PI*2.2;
      API.mk('circle',{cx:gx,cy:gy,r:gr,fill:'#fff',stroke:'#7E8B98','stroke-width':3},gG);
      for(let k=0;k<=8;k++){ const a=a0+(a1-a0)*k/8; API.mk('line',{x1:gx+(gr-(k%2?8:14))*Math.cos(a),y1:gy+(gr-(k%2?8:14))*Math.sin(a),x2:gx+gr*Math.cos(a),y2:gy+gr*Math.sin(a),stroke:'#5B6B7F','stroke-width':2},gG); }
      const ang=a0+(a1-a0)*API.clamp(Pg/4,0,1);
      API.mk('line',{x1:gx,y1:gy,x2:gx+(gr-18)*Math.cos(ang),y2:gy+(gr-18)*Math.sin(ang),stroke:'#D7263D','stroke-width':4,'stroke-linecap':'round'},gG);
      API.mk('circle',{cx:gx,cy:gy,r:6,fill:'#16233D'},gG);
      // 부분 압력 막대 (아래 산소, 위 질소)
      gB.innerHTML='';
      const hO=PO*u, hN=PN*u, dimO=mode==='N', dimN=mode==='O';
      if(hO>0) API.mk('rect',{x:bx,y:base-hO,width:bw,height:hO,fill:'#F7C9C1',stroke:'#E5533D','stroke-width':2,opacity:dimO?.3:1},gB);
      if(hN>0) API.mk('rect',{x:bx,y:base-hO-hN,width:bw,height:hN,fill:'#C9D3F3',stroke:'#4F6BD8','stroke-width':2,opacity:dimN?.3:1},gB);
      API.place(Ov('lo'),bx+bw+8,base-hO/2,hO>=20);
      API.place(Ov('ln'),bx+bw+8,base-hO-hN/2,hN>=20);
      O('nO').textContent=s.nO.toFixed(2)+' mol'; O('nN').textContent=s.nN.toFixed(2)+' mol';
      O('P').textContent=Pg.toFixed(2)+' atm';
      const what=mode==='O'?'산소만 남김 → 산소의 부분 압력':mode==='N'?'질소만 남김 → 질소의 부분 압력':'혼합 기체의 전체 압력';
      if(!log.length) O('msg').textContent=`${what}. 「산소만」「질소만」「혼합」을 눌러 압력계를 비교하고 「측정 기록」을 눌러 보자.`;
      else O('msg').textContent=`${what}. 표에서 (산소의 부분 압력) + (질소의 부분 압력) = (전체 압력), (산소의 몰분율) × (전체 압력) = (산소의 부분 압력)인지 확인하자.`;
      draw.sp=70;
    }
    function table(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-4).forEach((r,i)=>{ const nt=r.nO+r.nN, X=nt?r.nO/nt:NaN, PO=r.nO*K, PN=r.nN*K, P=PO+PN;
        const tr=document.createElement('tr');
        tr.innerHTML=`<td>${log.length-Math.min(log.length,4)+i+1}</td><td>${r.nO.toFixed(2)}</td><td>${r.nN.toFixed(2)}</td><td>${nt?X.toFixed(2):'–'}</td><td>${PO.toFixed(2)}</td><td>${PN.toFixed(2)}</td><td>${P.toFixed(2)}</td><td>${nt?(X*P).toFixed(2):'–'}</td>`;
        tb.appendChild(tr); }); }
    root.querySelectorAll('[data-v]').forEach(b=>b.addEventListener('click',()=>{ mode=b.dataset.v; root.querySelectorAll('[data-v]').forEach(x=>x.classList.toggle('on',x===b)); draw(); }));
    ['nO','nN'].forEach(k=>I(k).addEventListener('input',draw));
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ log.push(st()); if(log.length>8) log.shift(); table(); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ I('nO').value=0.75; I('nN').value=1.25; mode='M'; root.querySelectorAll('[data-v]').forEach(x=>x.classList.toggle('on',x.dataset.v==='M')); log=[]; table(); draw(); });
    draw(); table();
    if(!window.__STILL) API.loop(root,dt=>{ dt=Math.min(dt,.05); const sp=draw.sp||70;
      ['O','N'].forEach(el=>parts[el].forEach(p=>{ p.x+=Math.cos(p.a)*sp*dt; p.y+=Math.sin(p.a)*sp*dt; p.rot+=60*dt;
        if(p.x<box.x+20){p.x=box.x+20;p.a=Math.PI-p.a;} if(p.x>box.x+box.w-20){p.x=box.x+box.w-20;p.a=Math.PI-p.a;}
        if(p.y<box.y+20){p.y=box.y+20;p.a=-p.a;} if(p.y>box.y+box.h-20){p.y=box.y+box.h-20;p.a=-p.a;}
        setPos(p); })); });
  }
};
