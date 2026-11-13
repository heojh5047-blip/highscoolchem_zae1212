/* 4-3 유효 충돌과 활성화 에너지 — 실험실
   em43coll : 방향과 빠르기를 바꾸어 NO + O3 충돌시키기 (덱 보충 모의실험, 교과서 106쪽 해 보기 · 107쪽 그림 IV-4의 Ea = 10.5 kJ/mol)
     · 방향 a: NO의 N → O3의 끝 O (적합) / b: N → O3의 가운데 O / c: NO의 O → O3의 끝 O
     · 충돌 에너지(1몰당으로 나타낸 값, 모형) E = 0.25·v² kJ/mol (v = 상대 빠르기 1–10) → v ≥ 7 이면 E ≥ 10.5
     · 반응 조건: 방향 a 이고 E ≥ Ea(10.5 kJ/mol) → 끝 O 하나가 N 으로 옮겨 가 NO2 + O2 (원자 보존: N 1, O 4)
     · 그렇지 않으면 그대로 튕겨 나감. 「충돌시키기」마다 표에 한 줄(최대 6줄). 세 경우를 모두 해 보면 정리 문장 */
window.DECK_LABS = {
  em43coll(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=$('svg[data-v="g"]'), bar=$('svg[data-v="bar"]');
    const g0=API.mk('g',{},svg), g=API.mk('g',{},svg), gb=API.mk('g',{},bar);
    const R=20, EA=10.5, CX=262, CY=128;
    const DIR={a:'N → 끝 O', b:'N → 가운데 O', c:'O → 끝 O'};
    let st={d:'a', ph:'idle', t:0, react:false}, log=[], lab1='', lab2='';
    const E=()=>0.25*Math.pow(+I('v').value,2);
    const P=(x,y,a,d)=>[x+d*Math.cos(a*Math.PI/180), y+d*Math.sin(a*Math.PI/180)];
    // 접촉 순간의 배치 (O3 는 가운데 O 를 기준)
    function contact(d){
      const ap=d==='b'?180:-20, c=[CX+40,CY];
      const t1=P(c[0],c[1],ap+180-58.5,1.25*R), t2=P(c[0],c[1],ap+180+58.5,1.25*R);
      const tgt=d==='b'?c:(t1[0]<t2[0]?t1:t2), oth=d==='b'?null:(tgt===t1?t2:t1);
      const front=[tgt[0]-1.9*R, tgt[1]], back=[front[0]-1.25*R, front[1]];
      return {c, t1, t2, tgt, oth, nPos:d==='c'?back:front, oPos:d==='c'?front:back};
    }
    function frame(){
      g.innerHTML='';
      const K=contact(st.d), v=+I('v').value, sp=40+18*v;
      let dl=0, dr=0, q=0;           // dl: NO 쪽 왼쪽 이동, dr: O3 쪽 오른쪽 이동
      if(st.ph==='idle'){ dl=150; dr=110; }
      else if(st.ph==='in'){ const s=Math.max(0,1-st.t); dl=150*s; dr=110*s; }
      else if(st.ph==='out'||st.ph==='done'){ q=Math.min(1,st.t); dl=q*120; dr=q*100; }
      const at=(x,y,el)=>API.atom(g,x,y,R,el,'-',false);
      if(st.react && (st.ph==='out'||st.ph==='done')){
        // NO2: N 은 그대로, 옮겨 온 O 는 N 에서 -46° 자리로 (O–N–O 134°)
        const dest=P(K.nPos[0],K.nPos[1],-46,1.25*R), s=Math.min(1,q*2.2);
        const ox=K.tgt[0]+(dest[0]-K.tgt[0])*s, oy=K.tgt[1]+(dest[1]-K.tgt[1])*s;
        at(K.c[0]+dr,K.c[1],'O'); at(K.oth[0]+dr,K.oth[1],'O');
        at(K.oPos[0]-dl,K.oPos[1],'O'); at(ox-dl*s,oy,'O'); at(K.nPos[0]-dl,K.nPos[1],'N');
        setLab('\\ce{NO2}','\\ce{O2}'); place(K.nPos[0]-dl, K.c[0]+dr);
      } else {
        const pts=[K.c,K.t1,K.t2]; pts.forEach(p=>at(p[0]+dr,p[1],'O'));
        if(st.d==='c'){ at(K.nPos[0]-dl,K.nPos[1],'N'); at(K.oPos[0]-dl,K.oPos[1],'O'); }
        else { at(K.oPos[0]-dl,K.oPos[1],'O'); at(K.nPos[0]-dl,K.nPos[1],'N'); }
        setLab('\\ce{NO}','\\ce{O3}'); place(K.nPos[0]-dl, K.c[0]+dr);
      }
      // 충돌 섬광
      if((st.ph==='out'&&st.t<0.35)||(st.ph==='in'&&st.t>0.97)){
        const fx=(K.tgt[0]+(st.d==='c'?K.oPos[0]:K.nPos[0]))/2, Rr=st.react?38:(E()>=EA?32:18), pts=[];
        for(let i=0;i<24;i++){ const rr=i%2?Rr*.45:Rr; pts.push(P(fx,K.tgt[1],i*15,rr).map(v=>v.toFixed(1)).join(',')); }
        API.mk('polygon',{points:pts.join(' '),fill:'#FFD34D',opacity:.85},g);
      }
      // 빠르기 줄 (들어올 때)
      if(st.ph==='in'||st.ph==='idle'){
        const L=6+5*v, x0=Math.min(K.nPos[0],K.oPos[0])-dl-R-6;
        for(let i=-1;i<=1;i++) API.mk('line',{x1:x0,y1:CY+i*9,x2:x0-L*(1-.25*Math.abs(i)),y2:CY+i*9,stroke:'#C9D3DD','stroke-width':3,'stroke-linecap':'round'},g);
        const x1=K.c[0]+dr+R*1.3;
        for(let i=-1;i<=1;i++) API.mk('line',{x1:x1,y1:CY+i*9,x2:x1+L*(1-.25*Math.abs(i)),y2:CY+i*9,stroke:'#C9D3DD','stroke-width':3,'stroke-linecap':'round'},g);
      }
    }
    function setLab(a,b){ if(a!==lab1){ lab1=a; Ov('l1').innerHTML=API.tex(a); } if(b!==lab2){ lab2=b; Ov('l2').innerHTML=API.tex(b); } }
    function place(x1,x2){ API.place(Ov('l1'),API.clamp(x1-30,10,440),CY+42); API.place(Ov('l2'),API.clamp(x2-16,10,460),CY+42); }
    function drawBar(){
      gb.innerHTML='';
      const y0=210, H=170, MAX=25, e=E(), ye=y0-Math.min(e,MAX)/MAX*H, ya=y0-EA/MAX*H;
      API.mk('line',{x1:30,y1:y0,x2:110,y2:y0,stroke:API.COL.muted,'stroke-width':2},gb);
      API.mk('rect',{x:50,y:ye,width:40,height:y0-ye,rx:4,fill:e>=EA?'#9FB0C2':'#D5DCE4',stroke:API.COL.ink,'stroke-width':1.5},gb);
      API.mk('line',{x1:24,y1:ya,x2:116,y2:ya,stroke:API.COL.equi,'stroke-width':2.5,'stroke-dasharray':'6 4'},gb);
      API.place(Ov('ea'),24,ya-34);
    }
    function msgFor(x){
      if(x.ok) return `반응함 — 방향이 적합하고 충돌 에너지(${x.e.toFixed(1)} kJ/mol)가 활성화 에너지 이상이다. → 유효 충돌`;
      if(x.d!=='a') return '반응 안 함 — 에너지는 '+(x.e>=EA?'충분하지만':'부족하고')+' 충돌 방향이 반응에 적합하지 않다.';
      return `반응 안 함 — 방향은 적합하지만 충돌 에너지(${x.e.toFixed(1)} kJ/mol)가 활성화 에너지보다 작다.`;
    }
    function summary(){
      const ok=log.some(x=>x.ok), lowE=log.some(x=>x.d==='a'&&!x.ok), badD=log.some(x=>x.d!=='a'&&x.e>=EA);
      if(ok&&lowE&&badD) return '정리: 방향이 적합하고 충돌 에너지가 활성화 에너지(10.5 kJ/mol) 이상일 때만 반응했다. → 이런 충돌이 유효 충돌이다.';
      const need=[]; if(!ok) need.push('반응이 일어나는 충돌'); if(!lowE) need.push('방향은 맞고 느린 충돌'); if(!badD) need.push('빠르지만 방향이 다른 충돌');
      return '더 해 볼 것: '+need.join(', ');
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach((x,i)=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${x.n}</td><td>${DIR[x.d]}</td><td>${x.e.toFixed(1)}</td><td>${x.ok?'반응함':'반응 안 함'}</td>`; if(x.ok) tr.className='hl'; tb.appendChild(tr); }); }
    let runNo=0;
    function draw(){
      const v=+I('v').value; O('v').textContent=v+' (상대값)'; O('e').textContent=E().toFixed(1)+' kJ/mol';
      root.querySelectorAll('[data-d]').forEach(b=>b.classList.toggle('on',b.dataset.d===st.d));
      O('res').textContent=st.ph==='done'?(st.react?'반응함':'반응 안 함'):'–';
      frame(); drawBar();
    }
    root.querySelectorAll('[data-d]').forEach(b=>b.addEventListener('click',()=>{ st={d:b.dataset.d,ph:'idle',t:0,react:false}; O('msg').textContent='「충돌시키기」를 눌러 보자.'; draw(); }));
    I('v').addEventListener('input',()=>{ if(st.ph!=='in'&&st.ph!=='out') st={d:st.d,ph:'idle',t:0,react:false}; draw(); });
    $('[data-act="go"]').addEventListener('click',()=>{ st={d:st.d,ph:'in',t:0,react:st.d==='a'&&E()>=EA}; O('msg').textContent='충돌하는 중 …'; draw(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; runNo=0; renderLog(); I('v').value=8; st={d:'a',ph:'idle',t:0,react:false}; O('msg').textContent='방향과 빠르기를 고르고 「충돌시키기」를 눌러 보자.'; draw(); });
    function finish(){
      const x={n:++runNo,d:st.d,e:E(),ok:st.react}; log.push(x); if(log.length>6) log.shift();
      renderLog(); O('msg').textContent=msgFor(x)+'\n'+summary();
    }
    API.loop(root,dt=>{
      if(st.ph==='in'){ const v=+I('v').value; st.t+=dt*(0.35+0.09*v); if(st.t>=1){ st.ph='out'; st.t=0; } draw(); }
      else if(st.ph==='out'){ st.t+=dt*0.8; if(st.t>=1){ st.t=1; st.ph='done'; finish(); } draw(); }
    });
    // 범례(처음 한 번)
    API.mk('rect',{x:404,y:8,width:108,height:44,rx:6,fill:'#fff',stroke:'#C9D3DD','stroke-width':1.5},g0);
    API.atom(g0,424,30,10,'N','-',false); API.texText(g0,440,37,'\\mathrm{N}',{size:19,anchor:'start'});
    API.atom(g0,472,30,10,'O','-',false); API.texText(g0,488,37,'\\mathrm{O}',{size:19,anchor:'start'});
    const gl=API.mk('g',{},bar); API.texText(gl,70,240,'\\text{충돌 에너지}',{size:18,anchor:'middle',fill:API.COL.muted});
    Ov('ea').innerHTML=API.tex('E_\\mathrm{a}');
    O('msg').textContent='방향과 빠르기를 고르고 「충돌시키기」를 눌러 보자.';
    draw(); API.ready(()=>{ lab1=lab2=''; Ov('ea').innerHTML=API.tex('E_\\mathrm{a}'); draw(); });
  }
};
