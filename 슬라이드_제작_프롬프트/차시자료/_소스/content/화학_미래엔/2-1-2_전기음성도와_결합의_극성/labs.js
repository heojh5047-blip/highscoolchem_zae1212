/* 2-1-2 전기음성도와 결합의 극성 — 실험실
   cm212graph : 해 보기 「전기음성도의 주기성 찾기」(스프레드시트 활동 대체)
     · 1–3주기 15원소의 교과서 전기음성도 값으로 그래프 종류(원자 번호 순 / 주기별 / 족별)와 모양(꺾은선 / 막대)을 바꿔 그림
     · 「그래프 공유」→ 공유 목록(최근 5행)에 쌓임, 「초기화」
   cm212bond : 해 보기 「공유 전자쌍의 치우침 확인하기」(모의실험 대체)
     · 원자 A, B 고르기 → 전기음성도 차이, 공유 전자쌍 위치(가운데 + 차이×22 px), 부분 전하, 쌍극자 모멘트 화살표(차이×60 px)
     · 같은 원소 → 무극성 공유 결합 / 금속(Li, Na) + 비금속 → 이온 결합 / C–S → 표시 값이 같음(창의력 키우기로 넘김)
     · 「기록」→ 표(최근 5행), 「초기화」 */
window.DECK_LABS = {
  cm212graph(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=$('svg'), fig=$('.lab-fig');
    const INK='#16233D', EQ='#E08A2C', MUTED='#5B6B7F', GRID='#E2E7EC';
    const D=[['H',1,1,1,2.2],['Li',3,2,1,1.0],['Be',4,2,2,1.6],['B',5,2,13,2.0],['C',6,2,14,2.6],['N',7,2,15,3.0],['O',8,2,16,3.4],['F',9,2,17,4.0],
             ['Na',11,3,1,0.9],['Mg',12,3,2,1.3],['Al',13,3,13,1.6],['Si',14,3,14,1.9],['P',15,3,15,2.2],['S',16,3,16,2.6],['Cl',17,3,17,3.2]]
      .map(([el,z,p,g,en])=>({el,z,p,g,en}));
    const GR=[1,2,13,14,15,16,17];
    const X0=78, Y0=360, W=530, H=300;
    const gA=API.mk('g',{},svg), gP=API.mk('g',{},svg);
    const pool={};
    function ov(k){ if(!pool[k]){ const d=document.createElement('div'); d.className='ov mid'; d.style.fontSize='18px'; fig.appendChild(d); pool[k]=d; } return pool[k]; }
    function hideAll(){ Object.values(pool).forEach(d=>API.place(d,0,0,false)); }
    let st={m:'z',s:'line'}, log=[], n=0;
    const yv=v=>Y0-H*v/4;
    function axes(){
      while(gA.firstChild) gA.removeChild(gA.firstChild);
      API.mk('line',{x1:X0,y1:Y0,x2:X0+W+10,y2:Y0,stroke:MUTED,'stroke-width':2},gA);
      API.mk('line',{x1:X0,y1:Y0,x2:X0,y2:Y0-H-14,stroke:MUTED,'stroke-width':2},gA);
      for(let k=1;k<=4;k++) API.mk('line',{x1:X0,y1:yv(k),x2:X0+W,y2:yv(k),stroke:GRID,'stroke-width':1},gA);
    }
    const msgs={
      z:'원자 번호가 커지면 2주기·3주기 안에서 각각 커지다가, 다음 주기 1족에서 다시 작아진다 — 같은 모양이 되풀이된다(주기성).',
      p:'같은 주기에서 족 번호(원자 번호)가 커질수록 전기음성도가 증가한다. 3주기 선이 2주기 선보다 아래에 있다.',
      g:'같은 족에서 주기(원자 번호)가 커질수록 전기음성도가 감소한다 — 모든 선이 오른쪽 아래로 내려간다.'};
    const trend={z:'주기마다 되풀이됨',p:'같은 주기에서 증가',g:'같은 족에서 감소'};
    const names={z:'원자 번호 순',p:'주기별',g:'족별'};
    function draw(){
      axes(); hideAll();
      while(gP.firstChild) gP.removeChild(gP.firstChild);
      for(let k=0;k<=4;k++) API.place(ov('y'+k),X0-22,yv(k),true), ov('y'+k).textContent=k;
      ov('yl').style.color=MUTED; ov('yl').textContent='전기음성도'; API.place(ov('yl'),X0+50,Y0-H-22,true);
      const xl=ov('xl'); xl.style.color=MUTED;
      let pts=[], series=[], xt=[];
      if(st.m==='z'){
        const xs=z=>X0+W*(z-0.4)/18.2;
        for(let z=1;z<=18;z++) xt.push([xs(z),z%2||z===18?String(z):'']);
        D.forEach(d=>pts.push({x:xs(d.z),d,c:INK}));
        series=[D.filter(d=>d.p===2),D.filter(d=>d.p===3)].map(a=>({pts:a.map(d=>[xs(d.z),yv(d.en)]),c:INK}));
        xl.textContent='원자 번호'; O('ax').textContent='원자 번호'; O('ser').textContent='주기마다 끊은 선';
      } else if(st.m==='p'){
        const xs=g=>X0+W*(GR.indexOf(g)+0.6)/7.4;
        GR.forEach(g=>xt.push([xs(g),g+'족']));
        D.forEach(d=>pts.push({x:xs(d.g)+(st.s==='bar'?(d.p===2?-14:d.p===3?14:-28):0),d,c:d.p===3?EQ:INK}));
        series=[2,3].map(p=>({pts:D.filter(d=>d.p===p).map(d=>[xs(d.g),yv(d.en)]),c:p===3?EQ:INK,lab:p+'주기'}));
        xl.textContent='족'; O('ax').textContent='족'; O('ser').textContent='2주기, 3주기';
      } else {
        const xs=p=>X0+W*(p-0.5)/3.2;
        [1,2,3].forEach(p=>xt.push([xs(p),p+'주기']));
        D.forEach(d=>pts.push({x:xs(d.p)+(st.s==='bar'?(GR.indexOf(d.g)-3)*20:0),d,c:INK}));
        series=GR.map(g=>({pts:D.filter(d=>d.g===g).map(d=>[xs(d.p),yv(d.en)]),c:INK,lab:g+'족'}));
        xl.textContent='주기'; O('ax').textContent='주기'; O('ser').textContent='1, 2, 13–17족';
      }
      API.place(xl,X0+W-24,Y0+40,true);
      xt.forEach(([x,t],i)=>{ if(!t) return; const e=ov('x'+i); e.textContent=t; e.style.color=MUTED; API.place(e,x,Y0+16,true); });
      if(st.s==='line'){
        series.forEach(s=>{ if(s.pts.length>1) API.mk('polyline',{points:s.pts.map(p=>p.join(',')).join(' '),fill:'none',stroke:s.c,'stroke-width':3,'stroke-linejoin':'round'},gP); });
        pts.forEach(p=>API.mk('circle',{cx:p.x,cy:yv(p.d.en),r:6,fill:'#fff',stroke:p.c,'stroke-width':3},gP));
      } else {
        const bw=st.m==='g'?16:st.m==='p'?24:20;
        pts.forEach(p=>API.mk('rect',{x:p.x-bw/2,y:yv(p.d.en),width:bw,height:Y0-yv(p.d.en),fill:p.c,'fill-opacity':p.c===EQ?.75:.55,stroke:p.c,'stroke-width':1.5},gP));
      }
      // 원소 기호: 꺾은선은 점 위, 막대는 막대 위. 족별 막대는 겹쳐서 생략
      pts.forEach((p,i)=>{ const e=ov('e'+i); if(st.m==='g'&&st.s==='bar'){ return; }
        e.innerHTML=API.tex('\\mathrm{'+p.d.el+'}'); e.style.color=p.c===EQ?'#9A5A12':INK;
        let dy=-20; if(st.m==='g'&&st.s==='line'&&p.d.p===2) dy=(p.d.g===1?-20:-20);
        API.place(e,p.x+(st.m==='g'&&st.s==='line'?(p.d.p===1?-18:p.d.p===3?18:0):0),yv(p.d.en)+dy,true); });
      if(st.m==='p'&&st.s==='line'){ const a=ov('L2'),b=ov('L3'); a.textContent='2주기'; b.textContent='3주기'; a.style.color=INK; b.style.color='#9A5A12';
        API.place(a,X0+W-30,yv(3.75)-28,true); API.place(b,X0+W-30,yv(2.6)+26,true); }
      let m=msgs[st.m]; if(st.m==='g'&&st.s==='bar') m='막대가 많아 같은 족끼리 비교하기 어렵다 — 족별 자료는 꺾은선이 낫다. '+msgs.g;
      O('msg').textContent=m;
      root.querySelectorAll('[data-m]').forEach(b=>b.classList.toggle('on',b.dataset.m===st.m));
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===st.s));
      const tb=O('log'); tb.innerHTML=log.slice(-5).map(r=>`<tr><td>${r.n}</td><td>${r.m}</td><td>${r.s}</td><td>${r.t}</td></tr>`).join('');
    }
    root.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>{st.m=b.dataset.m; draw();}));
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{st.s=b.dataset.s; draw();}));
    $('[data-act="rec"]').addEventListener('click',()=>{ n++; log.push({n,m:names[st.m],s:st.s==='line'?'꺾은선':'막대',t:(st.m==='g'&&st.s==='bar')?'보기 어려움':trend[st.m]}); draw(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ st={m:'z',s:'line'}; log=[]; n=0; draw(); });
    draw(); API.onShow&&API.onShow(draw);
  },

  cm212bond(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), V=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg');
    const INK='#16233D', PLUS='#D7263D', MINUS='#1F6FD1', MUTED='#5B6B7F', BOND='#9AA5B1', FIELD='#2E9E6A';
    const EN={H:2.2,Li:1.0,Na:0.9,C:2.6,N:3.0,O:3.4,F:4.0,S:2.6,Cl:3.2};
    const RA={H:18,Li:30,Na:32,C:24,N:24,O:24,F:24,S:29,Cl:29};
    const ION={Li:[15,'+'],Na:[19,'+'],H:[22,'-'],N:[28,'3-'],O:[26,'2-'],F:[25,'-'],S:[34,'2-'],Cl:[32,'-']};
    const METAL={Li:1,Na:1};
    const XA=190, XB=430, Y=105, SX0=80, SX1=540, SY=250;
    const gS=API.mk('g',{},svg), gF=API.mk('g',{},svg), gE=API.mk('g',{},svg);
    let st={a:'H',b:'H'}, log=[], cur={};
    const r1=v=>(Math.round(v*10)/10).toFixed(1);
    function lum(el){ const f=(API.ATOM&&API.ATOM[el]?API.ATOM[el][0]:'#C9D3DD').replace('#',''); return (0.299*parseInt(f.substr(0,2),16)+0.587*parseInt(f.substr(2,2),16)+0.114*parseInt(f.substr(4,2),16))/255; }
    function base(){
      API.mk('line',{x1:SX0,y1:SY,x2:SX1,y2:SY,stroke:MUTED,'stroke-width':2},gS);
      for(let k=0;k<=3;k++){ const x=SX0+(SX1-SX0)*k/3.1; API.mk('line',{x1:x,y1:SY-6,x2:x,y2:SY+6,stroke:MUTED,'stroke-width':2},gS); }
      API.place(V('s0'),SX0,SY+20); API.place(V('s3'),SX1,SY+20); API.place(V('sl'),(SX0+SX1)/2,SY+22);
    }
    function classify(a,b){
      const d=Math.abs(EN[a]-EN[b]);
      if(METAL[a]&&METAL[b]) return {t:'none',d};
      if(METAL[a]||METAL[b]){ const nm=METAL[a]?b:a; if(nm==='C') return {t:'skip',d}; return {t:'ion',d}; }
      if(a===b) return {t:'non',d:0};
      if(d<0.05) return {t:'same',d:0};
      return {t:'pol',d};
    }
    const KIND={non:'무극성 공유 결합',pol:'극성 공유 결합',ion:'이온 결합',same:'?',none:'—',skip:'—'};
    function lab(el,sup){ return API.tex('\\mathrm{'+el+'}'+(sup?'^{'+sup+'}':'')); }
    function draw(){
      [gF,gE].forEach(g=>{ while(g.firstChild) g.removeChild(g.firstChild); });
      const a=st.a, b=st.b, c=classify(a,b); cur=c;
      O('en').textContent=EN[a].toFixed(1)+' · '+EN[b].toFixed(1);
      O('d').textContent=r1(Math.abs(EN[a]-EN[b]));
      O('kind').textContent=KIND[c.t];
      ['dA','dB','tA','tB','cap'].forEach(k=>API.place(V(k),0,0,false));
      const big=EN[b]>EN[a]?1:-1;       // 공유 전자쌍이 가는 쪽: +1 = B 쪽
      let msg='';
      if(c.t==='none'){ msg='금속 원자끼리는 공유 결합을 만들지 않는다 — 다른 원자를 골라 보자.'; }
      else if(c.t==='skip'){ msg='금속과 탄소의 결합은 이 실험실에서 다루지 않는다 — 다른 원자를 골라 보자.'; }
      else if(c.t==='ion'){
        const m=METAL[a]?a:b, nm=METAL[a]?b:a, xm=METAL[a]?XA:XB, xn=METAL[a]?XB:XA;
        const [rm]=ION[m], [rn,qn]=ION[nm];
        API.atom(gF,xm,Y,rm,m,'-',false); API.atom(gF,xn,Y,rn,nm,'-',false);
        API.atom(gF,xm,Y,RA[m],m,'-',true);
        API.arrow(gF,xm+RA[m]-6,Y-RA[m]-6,xn-rn+4,Y-rn-10,MINUS,3);
        const tm=V(METAL[a]?'tA':'tB'), tn=V(METAL[a]?'tB':'tA');
        tm.innerHTML=lab(m,'+'); tm.style.color='#FFFFFF'; tn.innerHTML=lab(nm,qn); tn.style.color=lum(nm)<.55?'#FFFFFF':INK;
        API.place(tm,xm,Y); API.place(tn,xn,Y);
        const cap=V('cap'); cap.innerHTML='전자가 완전히 이동 '+API.tex('\\ce{e-}')+' → 양이온과 음이온 (이온 수의 비는 나타내지 않음)'; cap.style.color=MINUS; API.place(cap,310,185);
        msg='전기음성도 차이가 매우 크다. 전자가 '+m+'에서 '+nm+'(으)로 완전히 이동해 양이온과 음이온이 생긴다 → 이온 결합.';
      } else {
        const d=c.d, sh=big*d*22, mid=(XA+XB)/2;
        API.mk('ellipse',{cx:mid+sh*0.8,cy:Y,rx:(XB-XA)/2+40+Math.abs(sh)*0.3,ry:Math.max(RA[a],RA[b])+18,fill:'#8C99A6','fill-opacity':.16,stroke:'#8C99A6','stroke-width':1.5,'stroke-dasharray':'5 4'},gF);
        API.mk('line',{x1:XA,y1:Y,x2:XB,y2:Y,stroke:BOND,'stroke-width':7,'stroke-linecap':'round'},gF);
        API.atom(gF,XA,Y,RA[a],a,'-',false); API.atom(gF,XB,Y,RA[b],b,'-',false);
        const tA=V('tA'), tB=V('tB'); tA.innerHTML=lab(a); tB.innerHTML=lab(b);
        tA.style.color=lum(a)<.55?'#FFFFFF':INK; tB.style.color=lum(b)<.55?'#FFFFFF':INK; API.place(tA,XA,Y); API.place(tB,XB,Y);
        API.mk('circle',{cx:mid+sh,cy:Y,r:22,fill:FIELD,'fill-opacity':.18,stroke:FIELD,'stroke-width':1.5},gE);
        API.mk('circle',{cx:mid+sh,cy:Y-7,r:5,fill:INK},gE); API.mk('circle',{cx:mid+sh,cy:Y+7,r:5,fill:INK},gE);
        const cap=V('cap'); cap.style.color=MUTED;
        if(c.t==='pol'){
          const dp=V(big>0?'dA':'dB'), dm=V(big>0?'dB':'dA'); dp.innerHTML=API.tex('\\delta^+'); dp.style.color=PLUS; dm.innerHTML=API.tex('\\delta^-'); dm.style.color=MINUS;
          API.place(V('dA'),XA,Y-RA[a]-26); API.place(V('dB'),XB,Y-RA[b]-26);
          const L=d*60, x1=mid-big*L/2, x2=mid+big*L/2, y=190;
          API.arrow(gF,x1,y,x2,y,INK,3); const tx=x1+big*L*0.15; API.mk('line',{x1:tx,y1:y-7,x2:tx,y2:y+7,stroke:INK,'stroke-width':3},gF);
          const hi=big>0?b:a;
          msg='공유 전자쌍이 전기음성도가 큰 '+hi+' 쪽으로 치우친다. 차이 '+r1(d)+' → 극성 공유 결합, 쌍극자 모멘트 화살표는 '+(big>0?a:b)+'에서 '+hi+' 쪽.';
        } else if(c.t==='non'){
          cap.textContent='부분 전하 없음 · 쌍극자 모멘트 0'; API.place(cap,310,190);
          msg='같은 원자끼리 결합하면 공유 전자쌍이 가운데에 있다 → 무극성 공유 결합.';
        } else {
          cap.textContent='표시 값이 같다 — 정말 치우치지 않을까?'; API.place(cap,310,190);
          msg='두 원자의 전기음성도가 모두 2.6으로 표시된다. 그래도 서로 다른 원자이다 — 소단원 마무리 「창의력 키우기」에서 생각해 보자.';
        }
      }
      // 아래 띠: 전기음성도 차이 표시
      if(c.t!=='none'&&c.t!=='skip'){ const x=SX0+(SX1-SX0)*Math.min(3.1,Math.abs(EN[a]-EN[b]))/3.1;
        API.mk('path',{d:`M${x-9} ${SY-22} L${x+9} ${SY-22} L${x} ${SY-8} Z`,fill:INK},gF); }
      O('msg').textContent=msg;
      ['a','b'].forEach(s=>root.querySelectorAll(`[data-side="${s}"] [data-el]`).forEach(bt=>bt.classList.toggle('on',bt.dataset.el===st[s])));
      O('log').innerHTML=log.slice(-5).map(r=>`<tr><td>${r.k}</td><td>${r.e}</td><td>${r.d}</td><td>${r.w}</td><td>${r.t}</td></tr>`).join('');
    }
    root.querySelectorAll('[data-side]').forEach(seg=>seg.querySelectorAll('[data-el]').forEach(bt=>bt.addEventListener('click',()=>{ st[seg.dataset.side]=bt.dataset.el; draw(); })));
    $('[data-act="rec"]').addEventListener('click',()=>{ const c=cur, a=st.a, b=st.b; if(c.t==='none'||c.t==='skip') return;
      const hi=EN[b]>EN[a]?b:a, lo=hi===a?b:a;
      log.push({k:a+'–'+b,e:EN[a].toFixed(1)+' / '+EN[b].toFixed(1),d:r1(Math.abs(EN[a]-EN[b])),w:c.t==='ion'?lo+' → '+hi+' 전자 이동':c.t==='pol'?hi+' 쪽':c.t==='non'?'없음':'?',t:KIND[c.t]}); draw(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ st={a:'H',b:'H'}; log=[]; draw(); });
    base(); draw(); API.onShow&&API.onShow(draw);
    API.loop(root,(dt,t)=>{ gE.setAttribute('transform',`translate(${(Math.sin(t*3.1)*1.6).toFixed(2)},${(Math.cos(t*2.3)*1.2).toFixed(2)})`); });
  }
};
