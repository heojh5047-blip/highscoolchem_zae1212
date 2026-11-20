/* 고급화학 3-1-1 — 실험실
   ac311piston : 피스톤 팽창·압축(덱 자체 ◇) — w, q, ΔU의 부호와 크기, P–V 그래프 넓이
     · 일정한 외부 압력: V처음 = 8.00 L, w = −P외부 × ΔV (L·atm) × 101.325 J/(L·atm), q는 입력(kJ), ΔU = q + w
     · 등온 가역(심화): n = 1.00 mol, T = 292 K, w = −nRT ln(V나중/V처음) (R = 8.314 J/(mol·K)), ΔU = 0, q = −w
       비교: 같은 처음·나중 상태를 외부 압력 P나중 = nRT/V나중 (R = 0.08206)으로 한 번에 바꿀 때 w = −P나중 ΔV */
(function(){
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||18,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
const M='−';
function sg(v,d){ const a=Math.abs(v); const s=a.toFixed(d); if(+s===0) return (0).toFixed(d); return (v<0?M:'+')+s; }
function fm(v,d){ return (v<0?M:'')+Math.abs(v).toFixed(d); }
window.DECK_LABS = {
  ac311piston(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('.lab-fig svg');
    const V1=8.00, LA=101.325, nR=8.314, Ta=292, Ra=0.08206;
    const CX=80, CW=150, BOT=284, K=9.5, PT=14;
    let st={m:'ext'}, log=[], anim=null;
    const gBack=API.mk('g',{},svg), gGas=API.mk('g',{},svg), gTop=API.mk('g',{},svg), gGr=API.mk('g',{},svg);
    const gasRect=API.mk('rect',{x:CX+3,width:CW-6,fill:'#FFFFFF'},gBack);
    const mols=[]; let s0=311; const rnd=()=>{ s0=(s0*16807)%2147483647; return s0/2147483647; };
    for(let i=0;i<16;i++) mols.push({x:CX+12+rnd()*(CW-24),f:rnd(),vx:(rnd()-.5)*90,vy:(rnd()-.5)*90,el:API.mk('circle',{r:7,fill:'#F2A65A',stroke:'#B4561C','stroke-width':1.5},gGas)});
    const yOf=V=>BOT-V*K-PT;
    let pyNow=yOf(8.5);
    function cur(){
      const V2=+I('v').value;
      if(st.m==='ext'){
        const P=+I('p').value, q=+I('q').value*1000, dV=V2-V1, wL=-P*dV, w=wL*LA;
        return {m:'ext',P,V2,dV,wL,w,q,dU:q+w};
      }
      const w=-1*nR*Ta*Math.log(V2/V1), P2=Ra*Ta/V2, wi=-P2*(V2-V1)*LA;
      return {m:'rev',V2,dV:V2-V1,w,q:-w,dU:0,P2,wi};
    }
    function pname(c){
      if(c.m==='rev') return c.dV>0?'등온 가역 팽창':(c.dV<0?'등온 가역 압축':'변화 없음');
      let b=Math.abs(c.dV)<0.05?'부피 일정':(c.dV>0?(c.P===0?'진공 팽창':'팽창'):'압축');
      const h=c.q>0?'가열하며 ':(c.q<0?'냉각하며 ':(Math.abs(c.dV)<0.05?'':'단열 '));
      return h+b;
    }
    function drawPiston(py,c){
      gTop.innerHTML='';
      gasRect.setAttribute('y',py+PT); gasRect.setAttribute('height',Math.max(0,BOT-py-PT));
      const tcol=c.dU>1?'#FDE2E4':(c.dU<-1?'#E3EEFB':'#FFFFFF'); gasRect.setAttribute('fill',tcol);
      API.mk('line',{x1:CX-6,y1:yOf(V1)+PT,x2:CX+CW+6,y2:yOf(V1)+PT,stroke:'#5B6B7F','stroke-width':1.5,'stroke-dasharray':'6 4'},gTop);
      txt(API,gTop,CX-6,yOf(V1)+PT+6,'처음',{size:18,anchor:'end',fill:'#5B6B7F'});
      API.mk('rect',{x:CX+3,y:py,width:CW-6,height:PT,rx:2,fill:'#C9D2DB',stroke:'#16233D','stroke-width':2},gTop);
      API.mk('path',{d:`M${CX} 20 L${CX} ${BOT} L${CX+CW} ${BOT} L${CX+CW} 20`,fill:'none',stroke:'#16233D','stroke-width':3},gTop);
      // 외부 압력 화살표
      const na=c.m==='rev'?3:Math.round(c.P*2), top=Math.max(4,py-36);
      for(let i=0;i<na;i++){ const x=CX+CW*(i+1)/(na+1); API.arrow(gTop,x,top,x,py-3,'ink',2.5); }
      txt(API,gTop,38,40,'P외부',{size:18}); txt(API,gTop,38,62,c.m==='rev'?'= P':c.P.toFixed(2)+' atm',{size:18});
      // 열
      if(c.m==='ext'&&Math.abs(c.q)>0.5){ const inn=c.q>0, w=2+Math.min(5,Math.abs(c.q)/600);
        [240,264].forEach(y=>inn?API.arrow(gTop,6,y,CX-6,y,'equi',w):API.arrow(gTop,CX-6,y,6,y,'equi',w));
        txt(API,gTop,38,292,inn?'열 흡수':'열 방출',{size:18,fill:'#E08A2C',w:700}); }
      if(c.m==='rev'&&Math.abs(c.q)>0.5){ const inn=c.q>0; [240,264].forEach(y=>inn?API.arrow(gTop,6,y,CX-6,y,'equi',4):API.arrow(gTop,CX-6,y,6,y,'equi',4));
        txt(API,gTop,38,292,inn?'열 흡수':'열 방출',{size:18,fill:'#E08A2C',w:700}); }
      // 일
      if(Math.abs(c.dV)>=0.05&&Math.abs(c.w)>0.05){ const up=c.dV>0, x=CX+CW+30, y0=py+PT/2;
        up?API.arrow(gTop,x,y0+26,x,y0-26,'ink',4):API.arrow(gTop,x,y0-26,x,y0+26,'ink',4);
        txt(API,gTop,x+6,y0+52,up?'일 함':'일 받음',{size:18,anchor:'middle'}); }
    }
    function graph(c){
      gGr.innerHTML='';
      const X0=340,Y0=250,W=260,H=214, pmax=c.m==='rev'?6.5:3.5;
      const X=v=>X0+v/24*W, Y=p=>Y0-p/pmax*H;
      const yt=c.m==='rev'?[0,2,4,6]:[0,1,2,3];
      [4,8,12,16,20,24].forEach(v=>API.mk('line',{x1:X(v),y1:Y0,x2:X(v),y2:Y0-H,stroke:'#E2E7EC','stroke-width':1},gGr));
      yt.slice(1).forEach(p=>API.mk('line',{x1:X0,y1:Y(p),x2:X0+W,y2:Y(p),stroke:'#E2E7EC','stroke-width':1},gGr));
      API.mk('line',{x1:X0,y1:Y0,x2:X0+W+6,y2:Y0,stroke:'#5B6B7F','stroke-width':2},gGr); API.mk('line',{x1:X0,y1:Y0,x2:X0,y2:Y0-H-6,stroke:'#5B6B7F','stroke-width':2},gGr);
      [0,8,16,24].forEach(v=>txt(API,gGr,X(v),Y0+22,String(v),{size:18}));
      yt.forEach(p=>txt(API,gGr,X0-8,Y(p)+6,String(p),{size:18,anchor:'end'}));
      txt(API,gGr,X0+W,Y0+44,'V [L]',{size:18,anchor:'end',fill:'#5B6B7F'}); txt(API,gGr,X0+6,22,'P [atm]',{size:18,anchor:'start',fill:'#5B6B7F'});
      const a=Math.min(V1,c.V2), b=Math.max(V1,c.V2);
      if(c.m==='ext'){
        if(b-a>=0.05&&c.P>0) API.mk('rect',{x:X(a),y:Y(c.P),width:X(b)-X(a),height:Y0-Y(c.P),fill:'#7B4FC8','fill-opacity':.15},gGr);
        API.mk('line',{x1:X(V1),y1:Y(c.P),x2:X(c.V2),y2:Y(c.P),stroke:'#7B4FC8','stroke-width':3},gGr);
        if(b-a>=0.5) API.arrow(gGr,X(V1)+(c.dV>0?2:-2),Y(c.P)-12,X(c.V2),Y(c.P)-12,'bfield',2.5);
        txt(API,gGr,X0+W-4,40,'넓이 = |w| = '+Math.abs(c.wL).toFixed(2)+' L·atm',{size:18,anchor:'end'});
      } else {
        const pts=[]; for(let i=0;i<=80;i++){ const v=a+(b-a)*i/80; pts.push(X(v)+','+Y(Ra*Ta/v)); }
        if(b-a>=0.05) API.mk('polygon',{points:X(a)+','+Y0+' '+pts.join(' ')+' '+X(b)+','+Y0,fill:'#2E9E6A','fill-opacity':.2},gGr);
        const cv=[]; for(let i=0;i<=120;i++){ const v=3.8+20.2*i/120; cv.push(X(v)+','+Y(Ra*Ta/v)); }
        API.mk('polyline',{points:cv.join(' '),fill:'none',stroke:'#16233D','stroke-width':3},gGr);
        if(b-a>=0.05) API.mk('rect',{x:X(a),y:Y(c.P2),width:X(b)-X(a),height:Y0-Y(c.P2),fill:'none',stroke:'#7B4FC8','stroke-width':2.5,'stroke-dasharray':'7 4'},gGr);
        API.mk('circle',{cx:X(V1),cy:Y(Ra*Ta/V1),r:5,fill:'#D7263D',stroke:'#16233D','stroke-width':1.5},gGr);
        API.mk('circle',{cx:X(c.V2),cy:Y(c.P2),r:5,fill:'#D7263D',stroke:'#16233D','stroke-width':1.5},gGr);
        txt(API,gGr,X0+W-4,40,'가역 |w| '+(Math.abs(c.w)/1000).toFixed(2)+' kJ',{size:18,anchor:'end',fill:'#2E9E6A',w:700});
        txt(API,gGr,X0+W-4,62,'한 번에 |w| '+(Math.abs(c.wi)/1000).toFixed(2)+' kJ',{size:18,anchor:'end',fill:'#7B4FC8',w:700});
      }
    }
    function draw(){
      const c=cur(), ext=c.m==='ext';
      root.querySelectorAll('[data-m]').forEach(b=>b.classList.toggle('on',b.dataset.m===st.m));
      ['p','q'].forEach(k=>{ root.querySelector(`[data-c="${k}"]`).classList.toggle('ac311-off',!ext); I(k).disabled=!ext; });
      O('p').textContent=ext?c.P.toFixed(2)+' atm':'= 기체 압력 P';
      O('v').textContent=c.V2.toFixed(2)+' L (ΔV '+sg(c.dV,2)+' L)';
      O('q').textContent=ext?sg(c.q/1000,2)+' kJ':sg(c.q/1000,2)+' kJ (자동)';
      O('big').textContent='ΔU = '+(Math.abs(c.dU)<0.05?'0':sg(c.dU,1))+' J';
      let msg;
      if(ext){
        const ws=Math.abs(c.w)<0.05?'일 없음':(c.w<0?'계가 주위에 일을 했다':'계가 주위로부터 일을 받았다');
        const qs=Math.abs(c.q)<0.5?'열 출입 없음':(c.q>0?'계가 열을 흡수':'계가 열을 방출');
        const us=Math.abs(c.dU)<0.05?'내부 에너지·온도 그대로':(c.dU>0?'내부 에너지 증가, 온도 올라감':'내부 에너지 감소, 온도 내려감');
        msg=`w = −P외부ΔV = ${sg(c.wL,3)} L·atm = ${sg(c.w,1)} J (${ws}), q = ${sg(c.q,0)} J (${qs}) → ΔU = q + w: ${us}.`;
        if(c.P===0&&c.dV>0) msg+=' 진공 팽창: 거스르는 힘이 없어 일 0.';
      } else {
        msg=`등온 가역: w = −nRT ln(V나중/V처음) = ${sg(c.w/1000,2)} kJ, ΔU = 0, q = ${sg(c.q/1000,2)} kJ. `;
        if(c.dV>0.05) msg+=`한 번에(${c.P2.toFixed(2)} atm) 팽창하면 w = ${sg(c.wi/1000,2)} kJ — 가역 팽창의 일이 더 크다(초록 넓이 > 보라 넓이).`;
        else if(c.dV<-0.05) msg+=`한 번에(${c.P2.toFixed(2)} atm) 압축하면 받는 일 ${sg(c.wi/1000,2)} kJ — 가역 압축은 가장 적은 일로 압축한다.`;
      }
      O('msg').textContent=msg;
      if(!anim){ pyNow=yOf(c.V2); drawPiston(pyNow,c); }
      graph(c);
      O('log').innerHTML=log.slice(-4).map((r,i)=>`<tr><td>${log.length-Math.min(4,log.length)+i+1}</td><td>${r.n}</td><td>${r.P}</td><td>${sg(r.dV,2)}</td><td>${sg(r.w,1)}</td><td>${sg(r.q,0)}</td><td>${Math.abs(r.dU)<0.05?'0':sg(r.dU,1)}</td></tr>`).join('');
    }
    root.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>{ st.m=b.dataset.m; const v=I('v');
      if(st.m==='rev'){ v.min=4; v.max=24; if(+v.value<4) v.value=4; } else { v.min=2; v.max=20; if(+v.value>20) v.value=20; } anim=null; draw(); }));
    ['p','v','q'].forEach(k=>I(k).addEventListener('input',()=>{ anim=null; draw(); }));
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const c=cur();
      log.push({n:pname(c),P:c.m==='ext'?c.P.toFixed(2):'= P',dV:c.dV,w:c.w,q:c.q,dU:c.dU}); anim={t:0,c}; draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; anim=null; st.m='ext'; const v=I('v'); v.min=2; v.max=20; v.value=8.5; I('p').value=1.2; I('q').value=0; draw(); });
    draw();
    API.loop(root,(dt)=>{
      if(anim){ anim.t+=dt/1.2; const k=Math.min(1,anim.t), e=1-Math.pow(1-k,3);
        pyNow=yOf(V1)+(yOf(anim.c.V2)-yOf(V1))*e; drawPiston(pyNow,anim.c); if(k>=1) anim=null; }
      const c=cur(), sp=Math.max(.4,Math.min(2,1+c.dU/1500)), y0=pyNow+PT+9, y1=BOT-9;
      mols.forEach(m=>{ m.x+=m.vx*sp*dt; if(m.x<CX+12){m.x=CX+12;m.vx=Math.abs(m.vx);} if(m.x>CX+CW-12){m.x=CX+CW-12;m.vx=-Math.abs(m.vx);}
        m.f+=m.vy*sp*dt/Math.max(20,y1-y0); if(m.f<0){m.f=-m.f;m.vy=Math.abs(m.vy);} if(m.f>1){m.f=2-m.f;m.vy=-Math.abs(m.vy);}
        m.el.setAttribute('cx',m.x.toFixed(1)); m.el.setAttribute('cy',(y0+m.f*(y1-y0)).toFixed(1)); });
    });
    { const y0=pyNow+PT+9, y1=BOT-9; mols.forEach(m=>{ m.el.setAttribute('cx',m.x.toFixed(1)); m.el.setAttribute('cy',(y0+m.f*(y1-y0)).toFixed(1)); }); }
  }
};
})();
