/* 고급화학 2-4-1 — 실험실 (a·b 같은 파일)
   ac241abs : 흡광도 측정(필수 탐구 고화-탐16, a)
     · ε(λ) = 12.0·exp(−(10⁷/λ − 12500)²/(2·2400²)) M⁻¹cm⁻¹, b = 1.00 cm, 측정 흡광도 = −log(10^(−εbc) + 0.002) + N(0, 0.003), 미지 시료 0.26 M
   ac241col : 콜로이드 특성 관찰(필수 탐구 고화-탐17, b)
     · 입자 지름: 참용액 0.5 nm, 은 30 nm·(1+n)^1.4 (NaCl n 방울), 우유 400 nm. 지름 > 300 nm 덩어리는 10분 뒤 가라앉음
   ac241vpl : 증기 압력 내림·끓는점 오름(필수 탐구 고화-탐18, b)
     · P물 = 앙투안 식(kPa), X용질 = i·m/(i·m + 55.51), i: 설탕 1, NaCl 1.9, P = P물(1 − X) × (1 + N(0, 0.01 %)) 0.001 kPa
     · 끓는점 예측: 같은 시료·농도 3점 이상 ln P–1/T 최소 제곱 → P = 101.325 kPa인 T */
(function(){
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=Math.imul(a^(a>>>15),1|a); t=(t+Math.imul(t^(t>>>7),61|t))^t; return ((t^(t>>>14))>>>0)/4294967296; }; }
function gauss(r){ let u=0,v=0; while(u===0)u=r(); v=r(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||18,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
function fitL(pts){ const n=pts.length, mx=pts.reduce((a,p)=>a+p[0],0)/n, my=pts.reduce((a,p)=>a+p[1],0)/n;
  let sxx=0,sxy=0,syy=0; pts.forEach(p=>{ sxx+=(p[0]-mx)**2; sxy+=(p[0]-mx)*(p[1]-my); syy+=(p[1]-my)**2; });
  const b=sxy/sxx, a=my-b*mx, r2=syy>0?(sxy*sxy)/(sxx*syy):1; return {a,b,r2}; }
function axes(API,g,X0,Y0,W,H,xr,yr,xs,ys,fx,fy){
  const X=v=>X0+(v-xr[0])/(xr[1]-xr[0])*W, Y=v=>Y0-(v-yr[0])/(yr[1]-yr[0])*H;
  xs.forEach(v=>{ API.mk('line',{x1:X(v),y1:Y0,x2:X(v),y2:Y0-H,stroke:'#E2E7EC','stroke-width':1},g); txt(API,g,X(v),Y0+22,fx?fx(v):String(v),{size:18}); });
  ys.forEach(v=>{ API.mk('line',{x1:X0,y1:Y(v),x2:X0+W,y2:Y(v),stroke:'#E2E7EC','stroke-width':1},g); txt(API,g,X0-8,Y(v)+6,fy?fy(v):String(v),{size:18,anchor:'end'}); });
  API.mk('line',{x1:X0,y1:Y0,x2:X0+W+6,y2:Y0,stroke:'#5B6B7F','stroke-width':2},g); API.mk('line',{x1:X0,y1:Y0,x2:X0,y2:Y0-H-6,stroke:'#5B6B7F','stroke-width':2},g);
  return {X,Y};
}
const cuCol=c=>{ const a=Math.min(1,c/0.5); return `rgb(${Math.round(232-170*a)},${Math.round(242-100*a)},${Math.round(250-42*a)})`; };
function wl(l){ let r,g,b; if(l<440){r=(440-l)/60;g=0;b=1;} else if(l<490){r=0;g=(l-440)/50;b=1;} else if(l<510){r=0;g=1;b=(510-l)/20;} else if(l<580){r=(l-510)/70;g=1;b=0;} else if(l<645){r=1;g=(645-l)/65;b=0;} else {r=1;g=0;b=0;}
  const k=l<700?1:Math.max(.35,1-(l-700)/300); return `rgb(${Math.round(255*r*k)},${Math.round(255*g*k)},${Math.round(255*b*k)})`; }
const pw=t=>Math.pow(10,8.07131-1730.63/(233.426+t))*0.133322;

window.DECK_LABS = {
  /* ───────── 흡광도 ───────── */
  ac241abs(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('.lab-fig svg'), app=root.querySelector('svg.ac241-app');
    const UNK=0.26, eps=l=>12.0*Math.exp(-Math.pow(1e7/l-12500,2)/(2*2400*2400));
    let st={c:0.5,mode:'gs'}, log=[], spec={}, rnd=rng(110);
    const conc=()=>st.c==='u'?UNK:st.c, name=c=>c==='u'?'미지':(c===0?'증류수':c+' M');
    const meas=(c,l,noise)=>{ const A=-Math.log10(Math.pow(10,-eps(l)*c)+0.002)+(noise?0.003*gauss(rnd):0); return Math.max(0,c===0?0:A); };
    // 장치
    const a0=API.mk('g',{},app);
    API.mk('rect',{x:6,y:40,width:52,height:40,rx:6,fill:'#FFF6D6',stroke:'#16233D','stroke-width':2},a0); txt(API,a0,32,104,'광원',{size:18});
    API.mk('line',{x1:58,y1:60,x2:96,y2:60,stroke:'#C9B458','stroke-width':6},a0);
    API.mk('path',{d:'M96 36 L120 60 L96 84 Z',fill:'#E8EEF5',stroke:'#16233D','stroke-width':2},a0); txt(API,a0,108,104,'회절발',{size:18});
    const b1=API.mk('line',{x1:120,y1:60,x2:220,y2:60,'stroke-width':7},a0);
    const cuv=API.mk('rect',{x:220,y:30,width:44,height:60,rx:3,stroke:'#7E8B98','stroke-width':2.5},a0); txt(API,a0,242,108,'큐벳',{size:18});
    const b2=API.mk('line',{x1:264,y1:60,x2:340,y2:60},a0);
    API.mk('rect',{x:340,y:34,width:76,height:52,rx:6,fill:'#E6EAEE',stroke:'#16233D','stroke-width':2},a0); const det=txt(API,a0,378,66,'',{size:18}); txt(API,a0,378,108,'검출기',{size:18});
    const g=API.mk('g',{},svg); const X0=70,Y0=214,W=490,H=184;
    function draw(){
      g.innerHTML=''; const l=+I('lam').value, c=conc(), A=meas(c,l,false), Tp=100*Math.pow(10,-A);
      O('lam').textContent=l+' nm';
      root.querySelectorAll('[data-c]').forEach(b=>b.classList.toggle('on',String(b.dataset.c)===String(st.c)));
      root.querySelectorAll('[data-act="gs"],[data-act="gc"]').forEach(b=>b.classList.toggle('on',b.dataset.act===st.mode));
      b1.setAttribute('stroke',wl(l)); cuv.setAttribute('fill',c===0?'#F4F9FD':cuCol(c));
      b2.setAttribute('stroke',wl(l)); b2.setAttribute('stroke-width',Math.max(0.6,7*Tp/100).toFixed(2)); det.textContent=Tp.toFixed(1)+' %';
      O('big').textContent=A.toFixed(3);
      let m=`${name(st.c)}, ${l} nm: 투과율 ${Tp.toFixed(1)} %.`;
      if(A>2) m+=' 빛이 1 % 미만 통과 — 측정 한계에 가깝다.';
      if(st.mode==='gs'){
        const ax=axes(API,g,X0,Y0,W,H,[400,900],[0,3],[400,500,600,700,800,900],[0,1,2,3]);
        txt(API,g,X0+W,Y0+44,'파장 (nm)',{size:18,anchor:'end',fill:'#5B6B7F'}); txt(API,g,X0+4,16,'흡광도',{size:18,anchor:'start',fill:'#5B6B7F'});
        API.mk('line',{x1:X0,y1:ax.Y(2),x2:X0+W,y2:ax.Y(2),stroke:'#5B6B7F','stroke-width':1.5,'stroke-dasharray':'6 4'},g);
        API.mk('line',{x1:ax.X(l),y1:Y0,x2:ax.X(l),y2:Y0-H,stroke:wl(l),'stroke-width':2.5},g);
        Object.keys(spec).forEach(k=>{ const pts=spec[k]; const cc=k==='u'?UNK:+k;
          API.mk('polyline',{points:pts.map(p=>ax.X(p[0]).toFixed(1)+','+ax.Y(Math.min(3,p[1])).toFixed(1)).join(' '),fill:'none',stroke:k==='u'?'#D7263D':(cc===0?'#8C99A6':cuCol(Math.max(cc,0.15))),'stroke-width':2.5},g);
          const mx=pts.reduce((a,p)=>p[1]>a[1]?p:a,pts[0]); txt(API,g,ax.X(mx[0]),ax.Y(Math.min(3,mx[1]))-8,name(k==='u'?'u':cc),{size:18});
        });
        if(spec[String(st.c)]){ const pts=spec[String(st.c)], mx=Math.max(...pts.map(p=>p[1])), top=pts.filter(p=>p[1]>=0.97*mx), lc=Math.round(top.reduce((a,p)=>a+p[0],0)/top.length/10)*10; m+=` 스펙트럼: 흡광도가 가장 큰 파장 약 ${lc} nm(주황–빨강 영역)`+(mx>2?' — 봉우리가 측정 한계에 걸려 평평하다.':'.'); }
        else m+=' 「파장별 흡광도 측정」으로 스펙트럼을 그리자.';
      } else {
        const ax=axes(API,g,X0,Y0,W,H,[0,0.55],[0,3],[0,0.1,0.2,0.3,0.4,0.5],[0,1,2,3],v=>v===0?'0':v.toFixed(1));
        txt(API,g,X0+W,Y0+44,'농도 (M)',{size:18,anchor:'end',fill:'#5B6B7F'}); txt(API,g,X0+4,16,`흡광도 (${l} nm)`,{size:18,anchor:'start',fill:'#5B6B7F'});
        const rows=log.filter(r=>r.l===l), kn=rows.filter(r=>r.c!=='u');
        let k=null;
        if(kn.filter(r=>r.c>0).length>=2){ let sxy=0,sxx=0,syy=0,n=0,sy=0; kn.forEach(r=>{ sxy+=r.c*r.A; sxx+=r.c*r.c; syy+=r.A*r.A; }); k=sxy/sxx;
          const my=kn.reduce((a,r)=>a+r.A,0)/kn.length; let ssr=0,sst=0; kn.forEach(r=>{ ssr+=(r.A-k*r.c)**2; sst+=(r.A-my)**2; }); const r2=sst>0?1-ssr/sst:1;
          API.mk('line',{x1:ax.X(0),y1:ax.Y(0),x2:ax.X(0.55),y2:ax.Y(Math.min(3,0.55*k)),stroke:'#2E9E6A','stroke-width':2.5},g);
          m+=` 검량선 y = ${k.toFixed(2)}x (결정 계수 ${r2.toFixed(4)}).`; if(r2<0.99) m+=' 직선에서 벗어난다 — 흡광도가 너무 큰 파장인지 확인하자.'; }
        kn.forEach(r=>API.mk('circle',{cx:ax.X(r.c),cy:ax.Y(Math.min(3,r.A)),r:6,fill:'#FFFFFF',stroke:'#16233D','stroke-width':2.5},g));
        rows.filter(r=>r.c==='u').forEach(r=>{ if(!k) return; const x=r.A/k; const px=ax.X(Math.min(0.55,x)), py=ax.Y(r.A);
          API.mk('path',{d:`M${px} ${py-8} l8 8 l-8 8 l-8 -8 Z`,fill:'#D7263D'},g); API.mk('line',{x1:px,y1:py,x2:px,y2:Y0,stroke:'#D7263D','stroke-width':1.5,'stroke-dasharray':'4 4'},g);
          m+=` 미지 시료: 흡광도 ${r.A.toFixed(3)} → 농도 약 ${x.toFixed(2)} M.`; });
        if(!kn.length) m+=' 같은 파장에서 농도별로 「흡광도 측정·기록」을 하자.';
        if(new Set(log.map(r=>r.l)).size>1) m+=' (검량선은 지금 파장의 기록만 쓴다.)';
      }
      O('msg').textContent=m;
      O('log').innerHTML=log.slice(-4).map((r,i)=>`<tr><td>${log.length-Math.min(4,log.length)+i+1}</td><td>${name(r.c)}</td><td>${r.l}</td><td>${r.A.toFixed(3)}</td><td>${(100*Math.pow(10,-r.A)).toFixed(1)}</td></tr>`).join('');
    }
    root.querySelectorAll('[data-c]').forEach(b=>b.addEventListener('click',()=>{ st.c=b.dataset.c==='u'?'u':+b.dataset.c; draw(); }));
    I('lam').addEventListener('input',draw);
    root.querySelector('[data-act="gs"]').addEventListener('click',()=>{ st.mode='gs'; draw(); });
    root.querySelector('[data-act="gc"]').addEventListener('click',()=>{ st.mode='gc'; draw(); });
    root.querySelector('[data-act="scan"]').addEventListener('click',()=>{ const c=conc(), pts=[]; for(let l=400;l<=900;l+=10) pts.push([l,meas(c,l,true)]); spec[String(st.c)]=pts; st.mode='gs'; draw(); });
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const l=+I('lam').value, A=Math.round(meas(conc(),l,true)*1000)/1000;
      log=log.filter(r=>!(r.c===st.c&&r.l===l)); log.push({c:st.c,l,A}); st.mode='gc'; draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; spec={}; rnd=rng(110); st={c:0.5,mode:'gs'}; I('lam').value=600; draw(); });
    draw();
  },

  /* ───────── 콜로이드 ───────── */
  ac241col(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('.lab-fig svg');
    const S={water:{n:'증류수',d:0,col:'#EEF6FC'},cu:{n:'황산 구리 수용액',d:0.5,col:'#9CC4E8'},ag:{n:'은 나노 콜로이드',d:30,col:'#E3B23C'},milk:{n:'묽힌 우유',d:400,col:'#F1EFEA'}};
    let st={s:'ag'}, log=[], rnd=rng(113);
    const s0=API.mk('g',{},svg);
    API.mk('rect',{x:8,y:96,width:46,height:24,rx:4,fill:'#E6EAEE',stroke:'#16233D','stroke-width':2},s0); txt(API,s0,31,142,'레이저',{size:18});
    const liq=API.mk('rect',{x:82,y:56,width:196,height:150},s0);
    const sed=API.mk('rect',{x:82,y:194,width:196,height:12,fill:'#5E5648'},s0);
    API.mk('path',{d:'M76 34 L80 40 L80 210 L280 210 L280 40 L284 34',fill:'none',stroke:'#7E8B98','stroke-width':2.5},s0);
    const beamIn=API.mk('line',{x1:54,y1:108,x2:80,y2:108,stroke:'#E53935','stroke-width':3},s0);
    const beam=API.mk('line',{x1:80,y1:108,x2:280,y2:108,stroke:'#E53935','stroke-width':8,'stroke-linecap':'round'},s0);
    const beamOut=API.mk('line',{x1:280,y1:108,x2:300,y2:108,stroke:'#E53935','stroke-width':3},s0);
    txt(API,s0,180,236,'비커(옆에서 본 모습)',{size:18,fill:'#5B6B7F'});
    API.mk('circle',{cx:450,cy:118,r:100,fill:'#FFFBEA',stroke:'#16233D','stroke-width':2.5},s0);
    txt(API,s0,450,246,'한외 현미경 창',{size:18,fill:'#5B6B7F'});
    const note=txt(API,s0,450,124,'',{size:18,fill:'#5B6B7F'});
    const gp=API.mk('g',{},svg); const P=[];
    for(let i=0;i<20;i++) P.push({x:390+rnd()*120,y:60+rnd()*116,el:API.mk('circle',{r:4,fill:'#8A6A1E'},gp)});
    function state(){ const s=S[st.s], n=+I('n').value, later=I('later').checked; let d=s.d, col=s.col, light=0, agg=false;
      if(st.s==='ag'){ d=30*Math.pow(1+n,1.4); agg=n>=1; col=n===0?'#E3B23C':(n<=2?'#D49A45':'#8A8172'); }
      if(st.s==='ag'||st.s==='milk') light=Math.min(1,0.55+0.08*(st.s==='ag'?n:0)+(st.s==='milk'?0.35:0));
      const settled=later&&d>300&&st.s==='ag'; if(settled){ light*=0.15; col='#E9E5DA'; }
      return {s,n,later,d,col,light,agg,settled}; }
    function draw(){
      const c=state(), las=I('laser').checked;
      O('n').textContent=c.n+' 방울';
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===st.s));
      liq.setAttribute('fill',c.col); sed.setAttribute('visibility',c.settled?'visible':'hidden');
      [beamIn,beamOut].forEach(e=>e.setAttribute('visibility',las?'visible':'hidden'));
      beam.setAttribute('visibility',las&&c.light>0.05?'visible':'hidden'); beam.setAttribute('stroke-opacity',(0.2+0.75*c.light).toFixed(2));
      const vis=c.d>=10; P.forEach((p,i)=>{ p.el.setAttribute('visibility',vis&&i<(c.settled?3:20)?'visible':'hidden'); p.el.setAttribute('r',Math.min(9,3+Math.log10(Math.max(1,c.d))*1.6).toFixed(1)); });
      note.textContent=vis?'':(c.d===0?'입자 없음':'입자가 너무 작아 보이지 않음');
      const ty=!las?'—':(c.light>0.3?'보임':(c.light>0.05?'약하게 보임':'안 보임'));
      O('big').textContent=las?('빛의 길: '+ty):'레이저를 켜자';
      let m=`${c.s.n}: `;
      if(st.s==='water') m+='입자가 없어 빛이 산란되지 않는다.';
      else if(st.s==='cu') m+='이온(약 0.5 nm)이 너무 작아 빛을 거의 산란시키지 않는다 — 참용액.';
      else if(st.s==='milk') m+='지방 방울(약 0.4 μm)이 빛을 산란시킨다 — 에멀션(콜로이드).';
      else if(!c.agg) m+='은 입자(약 30 nm)가 빛을 산란시켜 빛의 길이 보이고, 브라운 운동을 한다.';
      else if(c.settled) m+=`엉긴 덩어리(약 ${Math.round(c.d)} nm)가 10분 뒤 가라앉아 위쪽은 맑아지고 빛의 길이 약해졌다.`;
      else m+=`NaCl ${c.n}방울: 입자 표면 전하가 가려져 엉긴다(약 ${Math.round(c.d)} nm) — 색이 ${c.n<=2?'주황색으로':'회색으로'} 변하고 틴들 현상은 더 뚜렷하다.`;
      if((st.s==='cu'||st.s==='water'||st.s==='milk')&&c.n>0) m+=' (NaCl을 넣어도 큰 변화가 없다.)';
      O('msg').textContent=m;
      O('log').innerHTML=log.slice(-4).map((r,i)=>`<tr><td>${log.length-Math.min(4,log.length)+i+1}</td><td>${r.s}</td><td>${r.n}</td><td>${r.ty}</td><td>${r.col}</td><td>${r.br}</td></tr>`).join('');
      return c;
    }
    const colName=c=>st.s==='ag'?(c.settled?'맑아짐+침전':(c.n===0?'노랑':(c.n<=2?'주황':'회색'))):({water:'무색',cu:'파랑',milk:'흰색'})[st.s];
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ st.s=b.dataset.s; draw(); }));
    I('n').addEventListener('input',draw); I('laser').addEventListener('change',draw); I('later').addEventListener('change',draw);
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const c=draw(), las=I('laser').checked;
      log.push({s:c.s.n,n:c.n+(c.later?' (10분 뒤)':''),ty:!las?'—':(c.light>0.3?'보임':(c.light>0.05?'약함':'안 보임')),col:colName(c),br:c.d<10?'안 보임':(c.d>300?'느림':'활발')}); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; st={s:'ag'}; I('n').value=0; I('laser').checked=true; I('later').checked=false; draw(); });
    draw();
    P.forEach(p=>{ p.el.setAttribute('cx',p.x.toFixed(1)); p.el.setAttribute('cy',p.y.toFixed(1)); });
    API.loop(root,(dt)=>{ const c=state(); const k=c.d>=10?60/Math.sqrt(c.d/30):0;
      P.forEach(p=>{ p.x+=gauss(rnd)*k*dt; p.y+=gauss(rnd)*k*dt; const dx=p.x-450, dy=p.y-118, r=Math.hypot(dx,dy); if(r>90){ p.x=450+dx*88/r; p.y=118+dy*88/r; } p.el.setAttribute('cx',p.x.toFixed(1)); p.el.setAttribute('cy',p.y.toFixed(1)); }); });
  },

  /* ───────── 증기 압력 내림 ───────── */
  ac241vpl(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('.lab-fig svg'), app=root.querySelector('svg.ac241-app');
    const SM={w:{n:'순수한 물',i:0,col:'#1F6FD1'},s:{n:'설탕',i:1,col:'#2E9E6A'},n:{n:'NaCl',i:1.9,col:'#D7263D'}};
    let st={s:'w',mode:'gp'}, log=[], rnd=rng(115);
    const a0=API.mk('g',{},app);
    const bath=API.mk('rect',{x:6,y:34,width:280,height:70,rx:6,stroke:'#7E8B98','stroke-width':2},a0);
    API.mk('rect',{x:36,y:54,width:180,height:30,rx:3,fill:'#FFFFFF',stroke:'#7E8B98','stroke-width':2},a0);
    API.mk('rect',{x:38,y:56,width:30,height:26,fill:'#DDEEF8'},a0);
    API.mk('rect',{x:212,y:50,width:9,height:38,fill:'#C9D2DB',stroke:'#16233D','stroke-width':1.5},a0);
    API.mk('line',{x1:221,y1:69,x2:284,y2:69,stroke:'#16233D','stroke-width':4},a0);
    API.mk('path',{d:'M36 69 L20 69 L20 10 L360 10 L360 18',fill:'none',stroke:'#5B6B7F','stroke-width':3},a0);
    API.mk('circle',{cx:360,cy:56,r:38,fill:'#FFFFFF',stroke:'#16233D','stroke-width':2.5},a0);
    const disp=txt(API,a0,360,62,'',{size:18}); txt(API,a0,360,84,'kPa',{size:18,fill:'#5B6B7F'});
    const sol=[]; for(let i=0;i<4;i++) sol.push(API.mk('circle',{cx:44+i*7,cy:62+(i%2)*10,r:3,fill:'#E08A2C'},a0));
    const gm=API.mk('g',{},app), mols=[];
    for(let i=0;i<24;i++) mols.push({x:74+rnd()*136,y:58+rnd()*22,vx:(rnd()-.5)*60,vy:(rnd()-.5)*60,el:API.mk('circle',{r:3,fill:'#E4E8EC',stroke:'#8C99A6','stroke-width':1},gm)});
    const g=API.mk('g',{},svg); const X0=72,Y0=210,W=490,H=180;
    const X=(s,m)=>s==='w'?0:SM[s].i*m/(SM[s].i*m+55.51);
    const cur=()=>{ const t=+I('t').value, m=+I('m').value; return {t,m,P:pw(t)*(1-X(st.s,m))}; };
    const key=r=>r.s==='w'?'w':r.s+'@'+r.m.toFixed(2);
    function series(){ const o={}; log.forEach(r=>{ (o[key(r)]=o[key(r)]||[]).push(r); }); Object.values(o).forEach(a=>a.sort((p,q)=>p.t-q.t)); return o; }
    const dP=r=>{ const w=log.find(q=>q.s==='w'&&q.t===r.t); return (r.s==='w'||!w)?null:w.P-r.P; };
    function tb(rows){ if(rows.length<3) return null; const F=fitL(rows.map(r=>[1/(r.t+273.15),Math.log(r.P)])); return 1/((Math.log(101.325)-F.a)/F.b)-273.15; }
    function draw(){
      g.innerHTML=''; const c=cur();
      O('t').textContent=c.t+' °C'; O('m').textContent=st.s==='w'?'— (물)':c.m.toFixed(2)+' m';
      I('m').disabled=st.s==='w';
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===st.s));
      root.querySelectorAll('[data-act^="g"]').forEach(b=>b.classList.toggle('on',b.dataset.act===st.mode));
      const w=(c.t-20)/60; bath.setAttribute('fill',`rgb(${Math.round(227+26*w)},${Math.round(238-12*w)},${Math.round(251-23*w)})`);
      sol.forEach(e=>e.setAttribute('visibility',st.s==='w'?'hidden':'visible'));
      disp.textContent=c.P.toFixed(3); O('big').textContent=c.P.toFixed(3)+' kPa';
      const nm=Math.max(2,Math.min(24,Math.round(c.P/47.3*22+2))); mols.forEach((m,i)=>m.el.setAttribute('visibility',i<nm?'visible':'hidden'));
      let msg=`${SM[st.s].n}${st.s==='w'?'':' '+c.m.toFixed(2)+' m'}, ${c.t} °C: 증기 압력 ${c.P.toFixed(3)} kPa`;
      if(st.s!=='w'){ const d=pw(c.t)-c.P; msg+=` — 같은 온도의 순수한 물보다 ${d.toFixed(3)} kPa 낮다(X용질 ${X(st.s,c.m).toFixed(4)}).`; } else msg+='.';
      const S=series();
      if(st.mode==='gp'){
        const ax=axes(API,g,X0,Y0,W,H,[15,85],[0,50],[20,30,40,50,60,70,80],[0,10,20,30,40,50]);
        txt(API,g,X0+W,Y0+40,'온도 (°C)',{size:18,anchor:'end',fill:'#5B6B7F'}); txt(API,g,X0+4,16,'증기 압력 (kPa)',{size:18,anchor:'start',fill:'#5B6B7F'});
        Object.keys(S).forEach(k=>{ const rows=S[k], col=SM[rows[0].s].col;
          if(rows.length>1) API.mk('polyline',{points:rows.map(r=>ax.X(r.t)+','+ax.Y(r.P)).join(' '),fill:'none',stroke:col,'stroke-width':2.5,'stroke-dasharray':rows[0].s==='n'?'7 4':''},g);
          rows.forEach(r=>API.mk('circle',{cx:ax.X(r.t),cy:ax.Y(r.P),r:5,fill:'#FFFFFF',stroke:col,'stroke-width':2.5},g)); });
        if(!log.length) msg+=' 「측정·기록」으로 20–80 °C를 재자.';
      } else if(st.mode==='gd'){
        const rows=log.filter(r=>dP(r)!==null), ym=Math.max(0.3,...rows.map(r=>dP(r)*1.15));
        const ax=axes(API,g,X0,Y0,W,H,[15,85],[0,ym],[20,30,40,50,60,70,80],[0,ym/3,2*ym/3,ym],null,v=>v===0?'0':v.toFixed(2));
        txt(API,g,X0+W,Y0+40,'온도 (°C)',{size:18,anchor:'end',fill:'#5B6B7F'}); txt(API,g,X0+4,16,'ΔP = P물 − P용액 (kPa)',{size:18,anchor:'start',fill:'#5B6B7F'});
        Object.keys(S).filter(k=>k!=='w').forEach(k=>{ const rr=S[k].filter(r=>dP(r)!==null), col=SM[S[k][0].s].col;
          if(rr.length>1) API.mk('polyline',{points:rr.map(r=>ax.X(r.t)+','+ax.Y(dP(r))).join(' '),fill:'none',stroke:col,'stroke-width':2.5},g);
          rr.forEach(r=>API.mk('circle',{cx:ax.X(r.t),cy:ax.Y(dP(r)),r:5,fill:'#FFFFFF',stroke:col,'stroke-width':2.5},g)); });
        msg+=rows.length?' 온도가 높을수록 ΔP가 커진다 — ΔP = X용질 × P물.':' 같은 온도에서 순수한 물과 용액을 모두 기록하면 ΔP가 그려진다.';
      } else {
        const ax=axes(API,g,X0,Y0,W,H,[2.8,3.45],[0.5,4.7],[2.8,2.9,3.0,3.1,3.2,3.3,3.4],[1,2,3,4],v=>v.toFixed(1));
        txt(API,g,X0+W,Y0+40,'1000/T (1/K)',{size:18,anchor:'end',fill:'#5B6B7F'}); txt(API,g,X0+4,16,'ln P (P: kPa)',{size:18,anchor:'start',fill:'#5B6B7F'});
        const yb=Math.log(101.325); API.mk('line',{x1:X0,y1:ax.Y(yb),x2:X0+W,y2:ax.Y(yb),stroke:'#5B6B7F','stroke-width':1.5,'stroke-dasharray':'6 4'},g); txt(API,g,X0+W-4,ax.Y(yb)+20,'101.325 kPa',{size:18,anchor:'end',fill:'#5B6B7F'});
        let tw=null; const res=[];
        Object.keys(S).forEach(k=>{ const rows=S[k], col=SM[rows[0].s].col;
          rows.forEach(r=>API.mk('circle',{cx:ax.X(1000/(r.t+273.15)),cy:ax.Y(Math.log(r.P)),r:5,fill:'#FFFFFF',stroke:col,'stroke-width':2.5},g));
          const T=tb(rows); if(T===null) return; const F=fitL(rows.map(r=>[1000/(r.t+273.15),Math.log(r.P)]));
          API.mk('line',{x1:ax.X(2.8),y1:ax.Y(F.a+F.b*2.8),x2:ax.X(3.45),y2:ax.Y(F.a+F.b*3.45),stroke:col,'stroke-width':2,'stroke-dasharray':'8 5'},g);
          if(k==='w') tw=T; res.push([k,T,rows[0]]); });
        if(!res.length) msg+=' 같은 시료를 3개 온도 이상 기록하면 직선을 연장해 끓는점을 예측한다.';
        res.forEach(([k,T,r])=>{ if(k==='w'){ msg+=` 물 예측 끓는점 ${T.toFixed(2)} °C(직선 연장은 증발 엔탈피가 일정하다고 가정해 약간 낮게 나온다 — 물과의 차 ΔTb로 비교).`; return; }
          const th=0.51*SM[r.s].i*r.m; msg+=` ${SM[r.s].n} ${r.m.toFixed(2)} m 예측 ${T.toFixed(2)} °C`+(tw!==null?` (ΔTb ${ (T-tw).toFixed(2)} °C, Kb·i·m = ${th.toFixed(3)} °C)`:'')+'.'; });
      }
      O('msg').textContent=msg;
      O('log').innerHTML=log.slice(-4).map((r,i)=>{ const d=dP(r); return `<tr><td>${log.length-Math.min(4,log.length)+i+1}</td><td>${SM[r.s].n}</td><td>${r.s==='w'?'—':r.m.toFixed(2)}</td><td>${r.t}</td><td>${r.P.toFixed(3)}</td><td>${d===null?'—':d.toFixed(3)}</td></tr>`; }).join('');
    }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ st.s=b.dataset.s; draw(); }));
    I('t').addEventListener('input',draw); I('m').addEventListener('input',draw);
    ['gp','gd','gb'].forEach(a=>root.querySelector(`[data-act="${a}"]`).addEventListener('click',()=>{ st.mode=a; draw(); }));
    root.querySelector('[data-act="rec"]').addEventListener('click',()=>{ const c=cur(), m=st.s==='w'?0:c.m;
      const P=Math.round(c.P*(1+0.0001*gauss(rnd))*1000)/1000;
      log=log.filter(r=>!(r.s===st.s&&r.t===c.t&&(st.s==='w'||Math.abs(r.m-m)<1e-9))); log.push({s:st.s,m,t:c.t,P}); draw(); });
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; rnd=rng(115); st={s:'w',mode:'gp'}; I('t').value=20; I('m').value=0.15; draw(); });
    draw();
    API.loop(root,(dt)=>{ const t=+I('t').value, sp=0.6+t/60;
      mols.forEach(m=>{ m.x+=m.vx*sp*dt; m.y+=m.vy*sp*dt; if(m.x<72){m.x=72;m.vx=Math.abs(m.vx);} if(m.x>208){m.x=208;m.vx=-Math.abs(m.vx);} if(m.y<58){m.y=58;m.vy=Math.abs(m.vy);} if(m.y>80){m.y=80;m.vy=-Math.abs(m.vy);} m.el.setAttribute('cx',m.x.toFixed(1)); m.el.setAttribute('cy',m.y.toFixed(1)); }); });
    mols.forEach(m=>{ m.el.setAttribute('cx',m.x.toFixed(1)); m.el.setAttribute('cy',m.y.toFixed(1)); });
  }
};
})();
