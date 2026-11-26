/* 1-2-1 화학 반응식의 의미 — 실험실
   cm121bal : 계수 맞추기 (덱 추가 연습 도구, 가이드 5.11 "반응 전후 입자 상자")
     · 반응 5가지: 물 생성, 일산화 탄소 연소, 암모니아 생성, 메테인 연소, 물 분해
     · 물질마다 계수 슬라이더 1–6 → 반응 전·후 상자에 그 수만큼 분자 모형
     · 원소별 원자 수(반응 전·후) 표와 판정 문장: 안 맞음 / 맞지만 가장 간단한 정수비 아님 / 완성
     · 「확인 기록」 → 시도 표에 행이 쌓임(최근 5행), 「초기화」 */
window.DECK_LABS = {
  cm121bal(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const F={ H2:{H:2}, O2:{O:2}, N2:{N:2}, H2O:{H:2,O:1}, CO:{C:1,O:1}, CO2:{C:1,O:2}, CH4:{C:1,H:4}, NH3:{N:1,H:3} };
    const RX={
      w:{nm:'물 생성', L:['H2','O2'], Rr:['H2O']},
      co:{nm:'일산화 탄소 연소', L:['CO','O2'], Rr:['CO2']},
      nh:{nm:'암모니아 생성', L:['N2','H2'], Rr:['NH3']},
      ch:{nm:'메테인 연소', L:['CH4','O2'], Rr:['CO2','H2O']},
      wd:{nm:'물 분해', L:['H2O'], Rr:['H2','O2']}
    };
    const RA={H:18,C:24,N:24,O:24}, SC=0.6;
    function mol(k,x,y){ const r=e=>RA[e]*SC, P=(d,a)=>[x+d*Math.cos(a*Math.PI/180), y+d*Math.sin(a*Math.PI/180)], out=[];
      if(k==='H2'||k==='O2'||k==='N2'){ const e=k[0], d=0.78*r(e); out.push([e,...P(d,180)],[e,...P(d,0)]); }
      else if(k==='H2O'){ const d=0.78*(r('O')+r('H')); out.push(['H',...P(d,142.25)],['H',...P(d,37.75)],['O',x,y]); }
      else if(k==='CO2'){ const d=0.78*2*r('O'); out.push(['O',...P(d,180)],['O',...P(d,0)],['C',x,y]); }
      else if(k==='CO'){ const d=0.78*r('O'); out.push(['C',...P(d,180)],['O',...P(d,0)]); }
      else if(k==='CH4'){ const d=0.78*(r('C')+r('H')); [45,135,225,315].forEach(a=>out.push(['H',...P(d,a)])); out.push(['C',x,y]); }
      else if(k==='NH3'){ const d=0.78*(r('N')+r('H')); [90,210,330].forEach(a=>out.push(['H',...P(d,a)])); out.push(['N',x,y]); }
      return out.map(([e,px,py])=>[e,px,py,r(e)]);
    }
    const svg=$('svg');
    // 고정 그림: 상자 두 개, 화살표, 범례 (라벨은 처음에만 만든다)
    const back=API.mk('g',{},svg);
    API.mk('rect',{x:8,y:40,width:292,height:204,rx:12,fill:'#F4F8FC',stroke:'#9FC3DD','stroke-width':2.5},back);
    API.mk('rect',{x:340,y:40,width:292,height:204,rx:12,fill:'#F4F8FC',stroke:'#9FC3DD','stroke-width':2.5},back);
    API.arrow(back,304,142,336,142,'ink',3);
    API.texText(back,154,268,'반응 전',{size:19,anchor:'middle',fill:'#5B6B7F',mix:true});
    API.texText(back,486,268,'반응 후',{size:19,anchor:'middle',fill:'#5B6B7F',mix:true});
    const g=API.mk('g',{},svg);
    let st={k:'w'}, log=[];
    const ks=()=>{ const r=RX[st.k]; return r.L.concat(r.Rr); };
    const co=()=>ks().map((_,i)=>+I('c'+i).value);
    const gcd=(a,b)=>b?gcd(b,a%b):a;
    function count(list,c){ const n={}; list.forEach((k,i)=>{ for(const e in F[k]) n[e]=(n[e]||0)+F[k][e]*c[i]; }); return n; }
    const cf=n=>n===1?'':String(n);
    function eqTex(c){ const r=RX[st.k], nl=r.L.length;
      return '\\ce{'+r.L.map((k,i)=>cf(c[i])+k).join(' + ')+' -> '+r.Rr.map((k,i)=>cf(c[nl+i])+k).join(' + ')+'}'; }
    function place(list,c,x0){ // 3열 × 4행 칸, 물질마다 줄을 바꾸지 않고 이어서
      let slot=0;
      list.forEach((k,i)=>{ for(let j=0;j<c[i];j++){ const col=slot%3, row=Math.floor(slot/3);
        const x=x0+52+col*94, y=70+row*46;
        mol(k,x,y).forEach(([e,px,py,rr])=>API.atom(g,px,py,rr,e,'-',false)); slot++; } });
    }
    function judge(c){
      const r=RX[st.k], nl=r.L.length, L=count(r.L,c.slice(0,nl)), Rt=count(r.Rr,c.slice(nl));
      const els=Object.keys(Object.assign({},L,Rt)).sort((a,b)=>'CNHO'.indexOf(a)-'CNHO'.indexOf(b));
      const bad=els.filter(e=>(L[e]||0)!==(Rt[e]||0));
      const g0=c.reduce((a,b)=>gcd(a,b));
      return {L,Rt,els,bad,g0};
    }
    function draw(){
      const r=RX[st.k], list=ks(), c=co();
      root.querySelectorAll('[data-c]').forEach(el=>{ const i=+el.dataset.c; el.style.display=i<list.length?'':'none'; });
      list.forEach((k,i)=>{ O('n'+i).innerHTML=API.tex('\\ce{'+k+'}')+'의 계수'; O('c'+i).textContent=String(c[i]); });
      while(g.firstChild) g.removeChild(g.firstChild);
      place(r.L,c.slice(0,r.L.length),8); place(r.Rr,c.slice(r.L.length),340);
      const ov=root.querySelector('[data-ov="eq"]'); ov.innerHTML=API.tex(eqTex(c)); API.place(ov,320,20);
      const J=judge(c);
      O('cnt').innerHTML=J.els.map(e=>{ const a=J.L[e]||0, b=J.Rt[e]||0;
        return `<tr><td>${e}</td><td>${a}</td><td>${b}</td><td class="${a===b?'cm121-ok':'cm121-ng'}">${a===b?'✓':'✗'}</td></tr>`; }).join('');
      const m=O('msg');
      if(J.bad.length){ const e=J.bad[0]; m.textContent=`${e} 원자가 반응 전 ${J.L[e]||0}개, 반응 후 ${J.Rt[e]||0}개로 다르다. 계수를 바꿔 보자. (아래 첨자는 바꿀 수 없다)`; }
      else if(J.g0>1) m.textContent=`원자 수는 맞지만 가장 간단한 정수비가 아니다. 모든 계수를 ${J.g0}(으)로 나누자.`;
      else m.textContent=`완성! 원자의 종류와 수가 반응 전후에 같다. 계수비 ${c.join(' : ')} = 분자 수 비 = 몰비`;
    }
    function renderLog(){
      O('log').innerHTML=log.slice(-5).map(x=>`<tr><td>${x.nm}</td><td>${x.c}</td><td class="${x.ok?'cm121-ok':'cm121-ng'}">${x.res}</td></tr>`).join('')
        || '<tr><td colspan="3" class="c-muted">계수를 정하고 「확인 기록」을 누르면 여기에 쌓인다.</td></tr>';
    }
    function setRx(k){ st.k=k; for(let i=0;i<4;i++) I('c'+i).value=1;
      root.querySelectorAll('[data-r]').forEach(b=>b.classList.toggle('on',b.dataset.r===k)); draw(); }
    root.querySelectorAll('[data-r]').forEach(b=>b.addEventListener('click',()=>setRx(b.dataset.r)));
    root.querySelectorAll('input[type=range]').forEach(i=>i.addEventListener('input',draw));
    $('[data-act="rec"]').addEventListener('click',()=>{ const c=co(), J=judge(c);
      log.push({nm:RX[st.k].nm, c:c.join(', '), ok:!J.bad.length&&J.g0===1, res:J.bad.length?'✗ 원자 수 다름':J.g0>1?'△ 간단한 비 아님':'✓ 완성'}); renderLog(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ log=[]; renderLog(); setRx('w'); });
    API.ready(()=>{ renderLog(); draw(); });
    renderLog(); setRx('w');
  }
};
