/* 3-M 대단원 Ⅲ 마무리 — 실험실
   em39tank : 과학 글쓰기 12 — 같은 에너지를 얻는 데 필요한 연료의 질량·부피 (저장 상태 비교)
     · 단위 부피당(kJ/L) = 단위 질량당(kJ/g) × 밀도(g/L)
     · 필요한 질량 w = E / (kJ/g), 필요한 부피 V = E / (kJ/L)
     · 수소 142.9 kJ/g(285.8/2), 메테인 55.6 kJ/g(890/16), 옥테인 48.0 kJ/g(5470/114) — 01 덱 자료값
     · 밀도: 수소 기체 0.0813, 메테인 0.656, 옥테인 703 g/L(01 덱) / 압축 수소 약 40, 액체 수소 약 71 g/L(보충 어림값)
     · 「기록」 → 표 최대 5행, 「초기화」 → 수소 기체, 100,000 kJ */
window.DECK_LABS = {
  em39tank(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`);
    const svg=$('svg'), iE=$('[data-i="E"]');
    const ES=[1e4,2e4,5e4,1e5,2e5,5e5,1e6];
    const ST=[
      {sh:'수소 기체', cd:'25 °C, 1 기압', pg:285.8/2, d:0.0813, dots:6,  c:'#5DA9E9'},
      {sh:'압축 수소', cd:'약 700 기압', pg:285.8/2, d:40,     dots:22, c:'#5DA9E9'},
      {sh:'액체 수소', cd:'−253 °C 액체', pg:285.8/2, d:71,     dots:34, c:'#5DA9E9'},
      {sh:'메테인',    cd:'25 °C, 1 기압', pg:890/16,  d:0.656,  dots:7,  c:'#3A3F47'},
      {sh:'옥테인',    cd:'25 °C 액체', pg:5470/114,d:703,    dots:34, c:'#3A3F47'}];
    const fmt=v=>{ const r=Number(v.toPrecision(3)); return r>=1000? Math.round(r).toLocaleString('en-US') : String(r); };
    let si=0, log=[], cur=null;
    // ── 왼쪽: 탱크 (한 변 ∝ V^(1/3), 고정 배율 5 px) ──
    const AX=24, AY=262, K=5;
    API.texText(svg,135,22,'필요한 탱크 (같은 배율)',{size:18,anchor:'middle',fill:'#5B6B7F',mix:true});
    const ref=API.mk('rect',{x:AX,y:AY-10*K,width:10*K,height:10*K,fill:'none',stroke:'#5B6B7F','stroke-width':1.5,'stroke-dasharray':'5 4'},svg);
    const gt=API.mk('g',{},svg);
    const top=API.mk('path',{fill:'#CFE6F6',stroke:'#7E8B98','stroke-width':2},gt);
    const front=API.mk('rect',{x:AX,fill:'#E3F1FB',stroke:'#7E8B98','stroke-width':2.5},gt);
    let seed=11; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    const dots=Array.from({length:34},()=>({fx:.12+rnd()*.76, fy:.12+rnd()*.76, ph:rnd()*6.28, c:API.mk('circle',{r:4,fill:'#5DA9E9'},gt)}));
    svg.appendChild(ref);
    API.texText(svg,AX,290,'점선 상자: 1000 L',{size:18,anchor:'start',fill:'#5B6B7F',mix:true});
    // ── 오른쪽: 다섯 상태의 부피 막대 (로그 눈금 0.1 L – 100000 L) ──
    const BX=384, BW=170, RY=[52,96,140,184,228], lx=V=>BX+Math.max(2,Math.min(BW,(Math.log10(V)+1)/6*BW));
    API.texText(svg,BX,22,'필요한 부피 (로그 눈금)',{size:18,anchor:'start',fill:'#5B6B7F',mix:true});
    const hl=API.mk('rect',{x:282,width:362,height:38,rx:8,fill:'#FFF6C2'},svg);
    [[1,'1 L'],[100,'100 L'],[1e4,'1만 L']].forEach(([v,t])=>{ const x=lx(v); API.mk('line',{x1:x,y1:34,x2:x,y2:250,stroke:'#E2E7EC','stroke-width':1.5},svg); API.texText(svg,x,272,t,{size:18,anchor:'middle',fill:'#5B6B7F',mix:true}); });
    API.mk('line',{x1:BX,y1:34,x2:BX,y2:250,stroke:'#5B6B7F','stroke-width':2},svg);
    const bars=ST.map((s,i)=>{ API.texText(svg,BX-8,RY[i]+6,s.sh,{size:18,anchor:'end',mix:true}); return API.mk('rect',{x:BX,y:RY[i]-11,height:22,rx:3,fill:s.c},svg); });
    const ovs=ST.map((s,i)=>$(`[data-ov="v${i}"]`));
    function draw(){
      const E=ES[+iE.value], s=ST[si], pl=s.pg*s.d, w=E/s.pg, V=E/pl;
      O('E').textContent=E.toLocaleString('en-US')+' kJ';
      O('c').textContent=s.cd; O('d').textContent=fmt(s.d)+' g/L';
      O('pl').textContent=fmt(pl)+' kJ/L'; O('V').textContent=fmt(V)+' L';
      const a=K*Math.cbrt(V), dd=a*.32;
      front.setAttribute('y',(AY-a).toFixed(1)); front.setAttribute('width',a.toFixed(1)); front.setAttribute('height',a.toFixed(1));
      front.setAttribute('fill',si<3?'#E3F1FB':'#ECEEF1');
      top.setAttribute('d',`M${AX} ${(AY-a).toFixed(1)} l${dd.toFixed(1)} ${(-dd).toFixed(1)} h${a.toFixed(1)} v${a.toFixed(1)} l${(-dd).toFixed(1)} ${dd.toFixed(1)} v${(-a).toFixed(1)} Z`);
      dots.forEach((p,i)=>{ p.c.setAttribute('opacity',i<s.dots?1:0); p.c.setAttribute('fill',s.c); p.c.setAttribute('r',Math.max(1.5,Math.min(4,a/18)).toFixed(1)); });
      cur={s:s.sh,E,pl,w,V,a};
      ST.forEach((t,i)=>{ const v=E/(t.pg*t.d), x=lx(v); bars[i].setAttribute('width',(x-BX).toFixed(1)); bars[i].setAttribute('opacity',i===si?1:.45);
        ovs[i].textContent=fmt(v)+' L'; ovs[i].style.color=i===si?'#16233D':'#5B6B7F'; API.place(ovs[i],x+46,RY[i]-11,true); });
      hl.setAttribute('y',RY[si]-19);
      const Vg=E/(ST[0].pg*ST[0].d), Vo=E/(ST[4].pg*ST[4].d);
      O('msg').textContent= `${Number(s.pg.toPrecision(4))} kJ/g × ${fmt(s.d)} g/L = ${fmt(pl)} kJ/L · 질량 ${fmt(w)} g → `+(si===0 ? `옥테인 부피의 약 ${fmt(V/Vo)}배`
        : `수소 기체의 약 1/${Vg/V>=100?fmt(Vg/V):Number((Vg/V).toPrecision(2))}`+(si===4?'':`, 옥테인의 약 ${fmt(V/Vo)}배`));
    }
    function place(t){ if(!cur) return; const a=cur.a; dots.forEach(p=>{ const q=t*2.4+p.ph, j=Math.min(3,a/30);
      p.c.setAttribute('cx',(AX+p.fx*a+j*Math.sin(q)).toFixed(1)); p.c.setAttribute('cy',(AY-a+p.fy*a+j*Math.cos(q*1.3)).toFixed(1)); }); }
    function drawLog(){ O('log').innerHTML=log.map(r=>`<tr><td>${r.s}</td><td>${r.E.toLocaleString('en-US')}</td><td>${fmt(r.pl)}</td><td>${fmt(r.w)}</td><td>${fmt(r.V)}</td></tr>`).join(''); }
    function pick(i){ si=+i; root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('em39-act',+b.dataset.s===si)); draw(); place(0); }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>pick(b.dataset.s)));
    iE.addEventListener('input',()=>{ draw(); place(0); });
    $('[data-act="rec"]').addEventListener('click',()=>{ draw(); log.push(cur); if(log.length>5) log.shift(); drawLog(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; drawLog(); iE.value=3; pick(0); });
    API.onShow&&API.onShow(()=>{ draw(); place(0); });
    draw(); drawLog(); place(0);
    API.loop(root,(dt,t)=>place(t));
  }
};
