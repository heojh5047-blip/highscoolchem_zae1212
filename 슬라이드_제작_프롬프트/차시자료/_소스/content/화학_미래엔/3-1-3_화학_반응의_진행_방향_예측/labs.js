/* 3-1-3 화학 반응의 진행 방향 예측 — 실험실
   cm313dir : 반응 지수로 진행 방향 예측하기. 2NO2(g) ⇌ N2O4(g), 25 °C, K = 212(3-1-2 탐구 값).
              슬라이더 = 지금(처음) 농도 → Q = [N2O4]/[NO2]^2 를 K와 비교해 방향 문장.
              [반응 진행시키기] → 평형 계산(N 보존 c = a + 2b, 2Kx² + x − c = 0) 후 표에 한 행 추가(최대 5행),
              2초 동안 농도·플라스크 색·Q 점이 평형으로 움직임(API.loop). |Q/K − 1| < 0.05 이면 "이미 평형". */
window.DECK_LABS = {
  cm313dir(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('svg');
    const K=212, MAXR=5, NO2C='#B5562A', EQ='#E08A2C';
    const NL={x0:230,x1:670,y:64}, BAR={x0:330,w:300,max:1.1};
    const XL=q=>NL.x0+API.clamp(Math.log10(Math.max(q,1)),0,4)/4*(NL.x1-NL.x0);
    let a,b,anim=null,rows=[],nexp=0;
    // 고정 그림(texText는 처음 한 번만)
    const bg=API.mk('g',{},svg);
    const flaskD='M78 30 V74 A60 60 0 1 0 122 74 V30';
    const fill=API.mk('path',{d:flaskD+' Z',fill:NO2C,'fill-opacity':0.3},bg);
    API.mk('path',{d:flaskD,fill:'none',stroke:'#7E8B98','stroke-width':4},bg);
    API.mk('rect',{x:71,y:16,width:58,height:20,rx:5,fill:'#C9B79C',stroke:'#8C7A5E','stroke-width':2.5},bg);
    API.texText(bg,100,222,'25 °C, 밀폐 용기',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    API.arrow(bg,NL.x0-8,NL.y,NL.x1+14,NL.y,'ink',2);
    [0,1,2,3,4].forEach(e=>{ const x=NL.x0+e/4*(NL.x1-NL.x0);
      API.mk('path',{d:`M${x} ${NL.y-7} V${NL.y+7}`,stroke:'#16233D','stroke-width':2},bg);
      API.texText(bg,x,NL.y+28,e===0?'1':e===1?'10':`$10^{${e}}$`,{size:18,anchor:'middle',fill:'#16233D',mix:true}); });
    API.texText(bg,NL.x0-10,20,'반응 지수 $Q$ (로그 눈금)',{size:18,anchor:'start',fill:'#16233D',mix:true});
    const xk=XL(K);
    API.mk('path',{d:`M${xk} 28 V${NL.y+10}`,stroke:'#16233D','stroke-width':3,'stroke-dasharray':'7 5'},bg);
    API.texText(bg,xk+8,38,'$K=212$',{size:20,anchor:'start',fill:'#16233D',mix:true});
    API.texText(bg,BAR.x0-12,147,'$[\\ce{NO2}]$',{size:20,anchor:'end',fill:'#16233D',mix:true});
    API.texText(bg,BAR.x0-12,182,'$[\\ce{N2O4}]$',{size:20,anchor:'end',fill:'#16233D',mix:true});
    API.mk('path',{d:`M${BAR.x0} 124 V196`,stroke:'#16233D','stroke-width':2},bg);
    [0,0.5,1.0].forEach(v=>{ const x=BAR.x0+v/BAR.max*BAR.w; API.mk('path',{d:`M${x} 196 V202`,stroke:'#5B6B7F','stroke-width':2},bg);
      API.texText(bg,x,222,v===1?'1.0 mol/L':v.toFixed(1),{size:18,anchor:v===1?'start':'middle',fill:'#5B6B7F',mix:true}); });
    // 움직이는 Q 점(라벨 묶음을 통째로 옮김)
    const qg=API.mk('g',{},svg);
    API.mk('circle',{cx:0,cy:NL.y,r:9,fill:EQ,stroke:'#fff','stroke-width':2},qg);
    API.texText(qg,0,NL.y-18,'$Q$',{size:20,anchor:'middle',fill:'#B45F06',mix:true});
    const dyn=API.mk('g',{},svg);
    const fmtQ=q=>q>=100?q.toFixed(0):q>=10?q.toFixed(1):q.toFixed(2);
    const Qof=(x,y)=>y/(x*x);
    function cmp(q){ if(Math.abs(q/K-1)<0.05) return 0; return q<K?-1:1; }
    function draw(x,y,done){
      const q=Qof(x,y), s=cmp(q);
      fill.setAttribute('fill-opacity',(0.75*x/0.2).toFixed(3));
      qg.setAttribute('transform',`translate(${XL(q).toFixed(1)},0)`);
      dyn.innerHTML='';
      if(!done && s!==0){ const xq=XL(q); API.arrow(dyn,xq+(s<0?14:-14),NL.y+46,xk+(s<0?-6:6),NL.y+46,s<0?'field':'bfield',3); }
      [[x,NO2C,NO2C,128],[y,'#fff','#16233D',163]].forEach(([v,fc,sc,yy])=>{
        API.mk('rect',{x:BAR.x0,y:yy,width:Math.max(1,v/BAR.max*BAR.w),height:24,rx:3,fill:fc,'fill-opacity':fc==='#fff'?1:0.8,stroke:sc,'stroke-width':2},dyn);
        const t=API.mk('text',{x:BAR.x0+v/BAR.max*BAR.w+8,y:yy+19,'font-size':19,fill:'#16233D'},dyn); t.textContent=v.toFixed(3); });
      O('q').textContent='Q = '+(q===0?'0':fmtQ(q));
      let m;
      if(done) m=`평형에 도달했다: Q = K = 212. 정반응과 역반응은 같은 속도로 계속 일어난다.`;
      else if(s<0) m=`Q(${fmtQ(q)}) < K(212) → 정반응이 우세하게 진행한다. NO2는 줄고 N2O4는 늘어 색이 옅어진다.`;
      else if(s>0) m=`Q(${fmtQ(q)}) > K(212) → 역반응이 우세하게 진행한다. N2O4가 분해되어 NO2가 늘고 색이 진해진다.`;
      else m=`Q(${fmtQ(q)}) ≈ K(212) → 이미 평형 상태이다. 농도가 변하지 않는다.`;
      O('msg').textContent=m;
    }
    function fromSliders(){ a=+I('a').value; b=+I('b').value; O('a').textContent=a.toFixed(2)+' mol/L'; O('b').textContent=b.toFixed(2)+' mol/L'; anim=null; draw(a,b,false); }
    function eqOf(a0,b0){ const c=a0+2*b0, x=(-1+Math.sqrt(1+8*K*c))/(4*K); return [x,(c-x)/2]; }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      rows.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=r.map(v=>`<td>${v}</td>`).join(''); tb.appendChild(tr); }); }
    function run(){
      const q=Qof(a,b), s=cmp(q), [xe,ye]=eqOf(a,b);
      nexp++; rows.push([nexp,a.toFixed(2),b.toFixed(2),fmtQ(q),s<0?'Q < K':s>0?'Q > K':'Q ≈ K',s<0?'정반응 우세':s>0?'역반응 우세':'평형 유지',xe.toFixed(3),ye.toFixed(3)]);
      if(rows.length>MAXR) rows.shift(); renderLog();
      if(s===0){ draw(a,b,false); return; }
      anim={t:0,a0:a,xe,c:a+2*b};
    }
    function reset(){ rows=[]; nexp=0; renderLog(); I('a').value=0.1; I('b').value=0.5; fromSliders(); }
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',fromSliders));
    root.querySelector('[data-act="run"]').addEventListener('click',run);
    root.querySelector('[data-act="reset"]').addEventListener('click',reset);
    reset();
    API.loop(root,(dt)=>{ if(!anim) return; anim.t=Math.min(1,anim.t+dt/2); const e=1-Math.pow(1-anim.t,3);
      const x=anim.a0+(anim.xe-anim.a0)*e, y=(anim.c-x)/2; draw(x,y,anim.t>=1); if(anim.t>=1) anim=null; });
  }
};
