/* 1-4 고체의 종류와 구조 — 실험실
   em14sort : 해 보기(35쪽) 「화학 결합의 종류에 따라 고체 결정 분류하기」를 넓힌 모의실험
     · 고체 8종(구리, 설탕, 염화 나트륨 + 아이오딘, 염화 칼륨, 알루미늄, 흑연, 석영) 고르기
     · 시험 4가지(망치로 치기, 고체 전도성, 수용액 전도성, 녹는점 자료) → 입자 모형 움직임 + 결과 + 기록 표(고체마다 한 행)
     · 분류 단추(분자·공유·이온·금속 결정) → 시험 결과 2개 이상일 때 판정, 맞으면 까닭, 틀리면 실마리
   결정 구조(단위 세포)는 그리지 않는다 — 평면 배열 모형만. */
window.DECK_LABS = {
  em14sort(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=root.querySelector('svg');
    const KN=['분자 결정','공유 결정','이온 결정','금속 결정'];
    // 이름, 화학식, 결정(0 분자 1 공유 2 이온 3 금속), 모형, 망치, 고체 전도성, 수용액(null=녹지 않음), 녹는점, 틀렸을 때 실마리
    const S=[
      ['구리','Cu',3,'met','눌림(펴짐)',1,null,'1085 °C','망치로 치면 눌리고(펴지고) 고체에서 전류가 흐른다 — 이런 성질을 만드는 입자는?'],
      ['설탕','C12H22O11',0,'sug','깨짐',0,0,'약 186 °C','고체에서도 수용액에서도 전류가 흐르지 않고, 녹는점이 낮다.'],
      ['염화 나트륨','NaCl',2,'ion','깨짐(쪼개짐)',0,1,'801 °C','고체에서는 흐르지 않지만 수용액에서 전류가 흐른다 — 이동한 것은?'],
      ['아이오딘','I2',0,'i2','부서짐',0,null,'114 °C','전류가 흐르지 않고 녹는점이 낮다 — 약한 힘으로 모인 입자는?'],
      ['염화 칼륨','KCl',2,'ion','깨짐(쪼개짐)',0,1,'770 °C','고체에서는 흐르지 않고 수용액에서 흐르며, 힘을 주면 쪼개진다.'],
      ['알루미늄','Al',3,'met','눌림(펴짐)',1,null,'660 °C','고체에서 전류가 흐르고 얇게 펴진다(포일).'],
      ['흑연','C',1,'gra','층이 미끄러져 부서짐',1,null,'3600 °C 이상','전류는 흐르지만 펴지지 않고 부서지며, 녹는점이 매우 높다 — 탄소 원자끼리의 결합은?'],
      ['석영','SiO2',1,'qtz','매우 단단해 잘 깨지지 않음',0,null,'약 1700 °C','전류가 흐르지 않지만 녹는점이 매우 높고 아주 단단하다.']];
    const WHY=['고체·수용액에서 전류가 흐르지 않고 녹는점이 낮다 → 분자들이 약한 분자 간 인력으로 모인 분자 결정',
      '녹는점이 매우 높다(다이아몬드·석영은 매우 단단하고, 흑연은 전류가 흐르는 예외) → 원자들이 공유 결합 그물로 이어진 공유 결정',
      '고체에서는 흐르지 않고 수용액에서 흐르며, 힘을 주면 쪼개진다 → 이온 결합으로 배열된 이온 결정',
      '고체에서 전류가 흐르고 펴진다 → 금속 양이온과 자유 전자의 금속 결합으로 된 금속 결정'];
    const TN=['망치','고체 전도성','수용액 전도성','녹는점'];
    let cur=0, test=-1, t0=0, rows=[], msg='';
    const gB=API.mk('g',{},svg), gP=API.mk('g',{},svg), gR=API.mk('g',{},svg);
    // 바탕(처음 한 번)
    API.mk('rect',{x:6,y:6,width:330,height:288,rx:12,fill:'#FBFCFD',stroke:'#C9D3DD','stroke-width':1.5},gB);
    API.mk('rect',{x:350,y:6,width:304,height:288,rx:12,fill:'#F4F8FB',stroke:'#C9D3DD','stroke-width':1.5},gB);
    
    const lt=API.texText(gB,171,284,'입자 모형(평면, 크기 비례 아님)',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    const C=(g,x,y,r,s)=>API.charge(g,x,y,r,s);
    const E=(g,x,y)=>API.mk('circle',{cx:x,cy:y,r:5,fill:'#1F6FD1',stroke:'#fff','stroke-width':1.2},g);
    const ln=(g,x1,y1,x2,y2,c,w,da)=>API.mk('line',Object.assign({x1,y1,x2,y2,stroke:c,'stroke-width':w,'stroke-linecap':'round'},da?{'stroke-dasharray':da}:{}),g);
    function rnd(i){ const x=Math.sin(i*12.9898+cur*78.233)*43758.5453; return x-Math.floor(x); }
    // ── 입자 모형 (p: 망치 진행 0–1, fl: 전도 흐름 시간)
    function model(p,fl){
      gP.innerHTML=''; const s=S[cur], m=s[3], ham=test===0?p:0, cond=test===1&&s[5];
      if(m==='ion'){ const sp=40, x0=56, y0=70;
        const sh=sp*Math.min(1,ham*2), up=ham>0.5?36*(ham-0.5)*2:0;
        for(let j=0;j<5;j++) for(let i=0;i<7;i++){ const pos=(i+j)%2===0, top=j<2;
          C(gP,x0+i*sp+(top?sh:0),y0+j*sp-(top?up:0),pos?11:19,pos?'+':'-'); }
        if(ham>0.5) for(const i of [1,3,5]){ API.arrow(gP,x0+i*sp+20,y0+1.5*sp-up/2+6,x0+i*sp+20,y0+1.5*sp-up/2-14,'#16233D',2.5); API.arrow(gP,x0+i*sp+20,y0+1.5*sp-up/2+12,x0+i*sp+20,y0+1.5*sp-up/2+30,'#16233D',2.5); }
      } else if(m==='met'){ const sp=48, x0=50, y0=72;
        const sh=sp*Math.min(1,ham*1.4);
        for(let j=0;j<4;j++) for(let i=0;i<6;i++) C(gP,x0+i*sp+(j<2?sh:0),y0+j*sp,16,'+');
        for(let j=0;j<3;j++) for(let i=0;i<5;i++){ const k=j*5+i; let x=x0+(i+0.5)*sp+(rnd(k)-0.5)*12+(j<1?sh:j<2?sh/2:0), y=y0+(j+0.5)*sp+(rnd(k+40)-0.5)*12;
          if(cond) x=x0+((((i+0.5)*sp+fl*70+rnd(k)*20)%(5*sp))); E(gP,x,y); }
      } else if(m==='i2'||m==='sug'){ const sx=74, sy=58;
        for(let j=0;j<3;j++) for(let i=0;i<4;i++){ const k=j*4+i, dx=ham*(rnd(k)-0.5)*70, dy=ham*(rnd(k+20)-0.3)*50, x=60+i*sx+dx, y=80+j*sy+dy;
          if(m==='i2'){ const a=((i+j)%2?-35:35)*Math.PI/180, d=16; API.atom(gP,x-d*Math.cos(a),y-d*Math.sin(a),16,'I','-',false); API.atom(gP,x+d*Math.cos(a),y+d*Math.sin(a),16,'I','-',false); }
          else API.mk('ellipse',{cx:x,cy:y,rx:24,ry:14,fill:'#F3E7CC',stroke:'#B89A5E','stroke-width':2,transform:`rotate(${(i+j)%2?-20:20} ${x} ${y})`},gP); }
        if(!ham){ ln(gP,94,80,112,80,'#5B6B7F',2,'4 4'); ln(gP,168,138,186,138,'#5B6B7F',2,'4 4'); ln(gP,242,196,260,196,'#5B6B7F',2,'4 4'); }
      } else if(m==='gra'){ const sl=40*Math.min(1,ham*1.5);
        for(let L=0;L<4;L++){ const y=72+L*58, off=(L%2?18:0)+(L===0?sl:0)+(L===1?sl/2:0);
          for(let i=0;i<8;i++){ const x=40+i*36+off; if(i<7) ln(gP,x,y,x+36,y,'#6B7480',3.5); API.atom(gP,x,y,8,'C','-',false); }
          if(L<3) for(const i of [1,4,6]) ln(gP,40+i*36+off+9,y+12,40+i*36+off+9,y+50,'#5B6B7F',1.8,'4 4'); }
        if(cond) for(let k=0;k<6;k++){ const L=k%4, x=40+((k*53+fl*80)%250), y=72+L*58-14; E(gP,x,y); }
      } else if(m==='qtz'){ const a=30, w=Math.sqrt(3)*a, shake=ham>0&&ham<0.5?Math.sin(ham*60)*3:0;
        const pts=new Map(), ed=[];
        for(let j=0;j<3;j++) for(let i=0;i<4;i++){ const hx=60+i*w+(j%2)*w/2+shake, hy=90+j*1.5*a; const ring=[];
          for(let k=0;k<6;k++){ const an=(90+60*k)*Math.PI/180, q=[Math.round(hx+a*Math.cos(an)),Math.round(hy-a*Math.sin(an))]; ring.push(q); pts.set(q.join(','),q); }
          for(let k=0;k<6;k++) ed.push([ring[k],ring[(k+1)%6]]); }
        const seen=new Set();
        ed.forEach(([u,v])=>{ const key=[u.join(','),v.join(',')].sort().join('|'); if(seen.has(key)) return; seen.add(key); ln(gP,u[0],u[1],v[0],v[1],'#8E7A52',3); API.atom(gP,(u[0]+v[0])/2,(u[1]+v[1])/2,6,'O','-',false); });
        pts.forEach(q=>API.atom(gP,q[0],q[1],11,'Si','-',false));
      }
    }
    // ── 시험 장치(오른쪽 칸)
    function rig(p,fl){
      gR.innerHTML=''; const s=S[cur]; const showPM=(test===1||test===2);
      API.place(Ov('pm'),402,276,showPM); API.place(Ov('pp'),600,276,showPM); API.place(Ov('hint'),502,140,test<0);
      if(test<0) return;
      if(test===0){ // 망치
        API.mk('rect',{x:400,y:230,width:200,height:14,rx:4,fill:'#E9E4D8',stroke:'#B9B2A0','stroke-width':1.5},gR);
        const lump=s[2]===3?'M450 230 Q500 222 550 230 Z':'M470 230 L486 206 L512 200 L530 214 L536 230 Z';
        API.mk('path',{d:p>0.5&&s[2]===3?'M430 230 Q500 224 570 230 Z':lump,fill:s[2]===3?'#C8803A':'#E6EAF0',stroke:'#7E8B98','stroke-width':2},gR);
        if(p>0.5&&(s[2]===0||s[2]===2||s[3]==='gra')) for(let k=0;k<6;k++) API.mk('rect',{x:440+k*24+(rnd(k)*8),y:222-rnd(k+9)*16,width:9,height:7,fill:'#E6EAF0',stroke:'#7E8B98','stroke-width':1.2,transform:`rotate(${k*30} ${444+k*24} ${222})`},gR);
        const ang=-50+50*Math.min(1,p*2);
        const h=API.mk('g',{transform:`rotate(${ang} 610 190)`},gR);
        API.mk('rect',{x:500,y:184,width:110,height:12,rx:5,fill:'#B98A5A'},h); API.mk('rect',{x:476,y:160,width:34,height:62,rx:6,fill:'#7E8B98'},h);
        return; }
      // 전도성 측정 회로: 전원(위) — 전구 — 두 전극
      const on=(test===1&&s[5])||(test===2&&s[6]===1);
      ln(gR,390,60,390,200,'#5B6B7F',3); ln(gR,614,60,614,200,'#5B6B7F',3); ln(gR,390,60,470,60,'#5B6B7F',3); ln(gR,534,60,614,60,'#5B6B7F',3);
      API.mk('circle',{cx:502,cy:60,r:20,fill:on?'#FFE45C':'#fff',stroke:on?'#B59A1E':'#7E8B98','stroke-width':2.5},gR);
      if(on) for(let k=0;k<8;k++){ const a=k*Math.PI/4; ln(gR,502+27*Math.cos(a),60+27*Math.sin(a),502+36*Math.cos(a),60+36*Math.sin(a),'#E08A2C',2.5); }
      API.mk('rect',{x:381,y:150,width:18,height:110,rx:3,fill:'#7E8B98'},gR); API.mk('rect',{x:605,y:150,width:18,height:110,rx:3,fill:'#7E8B98'},gR);
      if(test===1){ API.mk('rect',{x:399,y:176,width:206,height:60,rx:6,fill:s[2]===3?'#C8803A':s[3]==='gra'?'#3A3F47':'#E6EAF0',stroke:'#7E8B98','stroke-width':2},gR);
        if(on) for(let k=0;k<5;k++) E(gR,410+((k*44+fl*90)%190),206+(k%2?-10:10)); }
      else { API.mk('path',{d:'M420 120 V256 Q420 264 428 264 H576 Q584 264 584 256 V120',fill:'#F8FBFD',stroke:'#7E8B98','stroke-width':3},gR);
        API.mk('rect',{x:423,y:160,width:158,height:101,rx:4,fill:'#DDEEF8'},gR);
        if(s[6]===null) API.mk('path',{d:'M470 260 L482 240 L506 236 L526 246 L532 260 Z',fill:s[2]===3?'#C8803A':s[3]==='gra'?'#3A3F47':s[3]==='i2'?'#5A2E78':'#E6EAF0',stroke:'#7E8B98','stroke-width':1.5},gR);
        else if(s[6]===1) for(let k=0;k<4;k++){ const y=178+k*20, d=(fl*40)%60; C(gR,540-((k*37+d)%100),y,8,'+'); C(gR,464+((k*29+d)%100),y+8,11,'-'); }
        else for(let k=0;k<6;k++) API.mk('ellipse',{cx:445+k*24,cy:185+(k%3)*24,rx:10,ry:6,fill:'#F3E7CC',stroke:'#B89A5E','stroke-width':1.5},gR);
      }
    }
    function result(){
      const s=S[cur];
      if(test<0) return '—';
      if(test===0) return s[4];
      if(test===1) return s[5]?'전류가 흐른다':'전류가 흐르지 않는다';
      if(test===2) return s[6]===null?'물에 녹지 않아 시험할 수 없다':s[6]?'전류가 흐른다':'전류가 흐르지 않는다';
      return `녹는점 ${s[7]}`;
    }
    function rowOf(i){ let r=rows.find(r=>r.i===i); if(r) rows.splice(rows.indexOf(r),1); else r={i,c:['','','','',''],k:''}; rows.push(r); return r; }
    function table(){ const tb=O('log'); tb.innerHTML='';
      rows.slice(-4).forEach(r=>{ const s=S[r.i], tr=document.createElement('tr');
        tr.innerHTML=`<td>${s[0]}</td>`+r.c.slice(0,4).map(v=>`<td>${v||'·'}</td>`).join('')+`<td>${r.k||'·'}</td>`; tb.appendChild(tr); }); }
    function draw(){
      const p=test>=0?Math.min(1,(performance.now()-t0)/1600):1, fl=(performance.now()-t0)/1000;
      model(window.__STILL?1:p,window.__STILL?0.5:fl); rig(window.__STILL?1:p,window.__STILL?0.5:fl);
    }
    function update(){
      const s=S[cur];
      Ov('nm').innerHTML=`${s[0]}(${API.tex('\\ce{'+s[1]+'}')})`;
      API.place(Ov('nm'),18,20,true);
      O('res').textContent=result();
      O('msg').textContent=msg||'고체를 고르고 시험 단추를 눌러 보자. 시험 결과가 두 가지 이상 모이면 분류 단추로 결정을 골라 보자.';
      table(); draw();
    }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{ cur=+b.dataset.s; test=-1; msg='';
      root.querySelectorAll('[data-s]').forEach(x=>x.classList.toggle('on',x===b)); update(); }));
    root.querySelectorAll('[data-t]').forEach(b=>b.addEventListener('click',()=>{ test=+b.dataset.t; t0=performance.now();
      const r=rowOf(cur); r.c[test]=test===0?S[cur][4]:test===1?(S[cur][5]?'흐름':'흐르지 않음'):test===2?(S[cur][6]===null?'녹지 않음':S[cur][6]?'흐름':'흐르지 않음'):S[cur][7];
      msg=`${S[cur][0]}: ${TN[test]} → ${result()}`; update(); }));
    root.querySelectorAll('[data-c]').forEach(b=>b.addEventListener('click',()=>{ const c=+b.dataset.c, s=S[cur], r=rows.find(r=>r.i===cur);
      const n=r?r.c.filter(v=>v).length:0;
      if(n<2){ msg=`먼저 ${s[0]}을(를) 두 가지 이상 시험해 보자.`; update(); return; }
      if(c===s[2]){ r.k='○ '+KN[c]; msg=`맞다! ${s[0]} = ${KN[c]}. ${WHY[c]}`; }
      else { r.k='✗ '+KN[c]; msg=`다시 생각해 보자. ${s[8]}`; }
      update(); }));
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ rows=[]; test=-1; msg=''; cur=0; root.querySelectorAll('[data-s]').forEach(x=>x.classList.toggle('on',x.dataset.s==='0')); update(); });
    update(); API.ready(update); API.onShow(update);
    if(!window.__STILL) API.loop(root,()=>{ if(test>=0) draw(); });
  }
};
