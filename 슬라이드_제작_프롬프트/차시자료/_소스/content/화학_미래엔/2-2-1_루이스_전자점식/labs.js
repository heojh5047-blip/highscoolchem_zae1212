// 2-2-1 루이스 전자점식 — 실험실 (접두어 cm221)
window.DECK_LABS = {
  // 원자의 루이스 전자점식 그리기: 원소 고르기 → 원자가 전자를 하나씩 점으로 놓기
  cm221atom(root, API){
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), V=k=>$(`[data-ov="${k}"]`);
    const svg=$('svg'), g=API.mk('g',{},svg);
    const INK='#16233D', MUTED='#5B6B7F', PLUS='#D7263D', MINUS='#1F6FD1', GRAV='#8C99A6', EQUI='#E08A2C';
    const Z={H:1,He:2,Li:3,Be:4,B:5,C:6,N:7,O:8,F:9,Ne:10,Na:11,Mg:12,Al:13,Si:14,P:15,S:16,Cl:17,Ar:18};
    const NOBLE=['He','Ne','Ar'], METAL=['Li','Na','Mg','Al'], EXC=['Be','B'];
    const ORDER=['r','l','u','d','u','l','d','r'];             // 교과서 그림 Ⅱ-10 순서
    const BASE={r:0,u:90,l:180,d:270};
    const BX=140, BY=140, LX=440, LY=140, S=72;
    let st={el:'O',k:8}, log=[];

    const shells=z=> z<=2?[z]: z<=10?[2,z-2]:[2,8,z-10];
    const seq=el=> el==='He'?['r','r']:ORDER.slice(0,shells(Z[el]).slice(-1)[0]);
    function finalCount(sq){ const c={}; sq.forEach(s=>c[s]=(c[s]||0)+1); return c; }
    function circ(x,y,r,fill,stroke,w){ return API.mk('circle',{cx:x,cy:y,r,fill,stroke:stroke||'none','stroke-width':w||0},g); }

    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      const el=st.el, z=Z[el], sh=shells(z), sq=seq(el), n=sq.length; st.k=Math.min(st.k,n);
      root.querySelectorAll('[data-e]').forEach(b=>b.classList.toggle('on',b.dataset.e===el));
      // 전자 껍질 모형
      const R= sh.length===1?[50]: sh.length===2?[38,76]:[30,64,98];
      R.forEach(r=>circ(BX,BY,r,'none',MUTED,1.5));
      circ(BX,BY,16,PLUS);
      V('z').textContent=z+'+'; API.place(V('z'),BX,BY);
      sh.forEach((cnt,i)=>{ if(i===sh.length-1) return; const r=R[i];
        for(let j=0;j<cnt;j++){ const a=(cnt===2?45:90)+360*j/cnt, t=a*Math.PI/180; circ(BX+r*Math.cos(t),BY-r*Math.sin(t),5.5,GRAV); } });
      const fin=finalCount(sq), seen={}, rO=R[R.length-1];
      sq.forEach((s,i)=>{ seen[s]=(seen[s]||0)+1; const a=BASE[s]+(fin[s]===2?(seen[s]===1?-14:14):0), t=a*Math.PI/180;
        const x=BX+rO*Math.cos(t), y=BY-rO*Math.sin(t), on=i<st.k;
        if(i===st.k-1) circ(x,y,10,'none',EQUI,2.5);
        circ(x,y,5.5,on?MINUS:'#FFFFFF',MINUS,on?0:1.8); });
      API.arrow(g,268,BY,326,BY,GRAV,4);
      // 루이스 전자점식
      V('sym').innerHTML=API.tex('\\mathrm{'+el+'}'); API.place(V('sym'),LX,LY+2);
      const ox=(el.length>1?0.95:0.70)*S, oy=0.75*S, o=0.18*S, cur={};
      sq.slice(0,st.k).forEach(s=>cur[s]=(cur[s]||0)+1);
      const last=st.k?sq[st.k-1]:null;
      Object.keys(cur).forEach(s=>{
        const cx=LX+(s==='l'?-ox:s==='r'?ox:0), cy=LY+(s==='u'?-oy:s==='d'?oy:0), h=(s==='u'||s==='d');
        const pts= cur[s]===1?[[cx,cy]]: h?[[cx-o,cy],[cx+o,cy]]:[[cx,cy-o],[cx,cy+o]];
        pts.forEach((p,j)=>{ if(s===last && j===pts.length-1) circ(p[0],p[1],12,'none',EQUI,2.5); circ(p[0],p[1],6.5,INK); });
      });
      API.place(V('t1'),BX,2); API.place(V('t2'),LX,2);
      // 값
      const pairs=Object.values(cur).filter(c=>c===2).length, singles=Object.values(cur).filter(c=>c===1).length;
      O('val').textContent=n+'개'; O('put').textContent=st.k+'개';
      O('pairs').textContent=pairs+'쌍 · '+singles+'개';
      let msg;
      if(st.k===0) msg='「전자 하나 놓기」를 눌러 가장 바깥 껍질의 전자를 하나씩 점으로 옮겨 보자.';
      else if(st.k<n) msg= st.k===5 ? '다섯 번째 전자부터는 다시 위에 놓아 쌍을 이룬다.' : (st.k>4 ? '이미 점이 있는 자리에 놓아 쌍을 이룬다.' : '상하좌우에 하나씩 놓는다.')+` (${st.k}/${n})`;
      else if(NOBLE.includes(el)) msg=`가장 바깥 전자 껍질이 채워져(${el==='He'?'2개':'8개'}) 다른 원자와 결합을 잘 하지 않는다. 18족은 원자가 전자 수를 0으로 본다.`;
      else if(METAL.includes(el)) msg=`원자가 전자 ${n}개, 쌍을 이루지 않은 전자 ${singles}개. 금속 원소는 주로 전자를 잃어 양이온이 된다.`;
      else msg=`원자가 전자 ${n}개, 쌍을 이루지 않은 전자 ${singles}개 → 다른 원자와 공유 전자쌍을 ${singles}개 만들 수 있다.`+(EXC.includes(el)?' (옥텟 규칙의 예외)':'');
      O('msg').textContent=msg;
      st.pairs=pairs; st.singles=singles;
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${API.tex('\\mathrm{'+r.el+'}')}</td><td>${r.k}</td><td>${r.p}</td><td>${r.s}</td>`; tb.appendChild(tr); }); }

    root.querySelectorAll('[data-e]').forEach(b=>b.addEventListener('click',()=>{ st.el=b.dataset.e; st.k=0; draw(); }));
    root.querySelector('[data-act="one"]').addEventListener('click',()=>{ st.k++; draw(); });
    root.querySelector('[data-act="all"]').addEventListener('click',()=>{ st.k=99; draw(); });
    root.querySelector('[data-act="clear"]').addEventListener('click',()=>{ st.k=0; draw(); });
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{
      const row={el:st.el,k:st.k,p:st.pairs,s:st.singles}, i=log.findIndex(r=>r.el===st.el);
      if(i>=0) log[i]=row; else { log.push(row); if(log.length>5) log.shift(); } renderLog(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); st={el:'O',k:0}; draw(); });
    API.ready(()=>draw());
    draw();
  }
};
