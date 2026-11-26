/* 고급화학 2-1-1b — 실험실
   ac211mm : 기체 분자량 측정 (필수 탐구 고화-탐10, 아이소프로필 알코올 기화 — 뒤마 방법)
     · 실제 증기 몰수 n = PV/(RT) (P = 대기압/760 atm, T = t+273.15, R 0.082057)
     · 측정 질량 m = nM ×(1+N(0,0.4 %)) + (바깥 물기 0.025–0.045 g) + (액체 남음 0.08–0.15 g) — 고정 시드
     · 계산 M = mRT/(PV) (R 0.08206, T = t + 273) → 문헌값과 오차 %, 미지 시료는 후보와 비교 */
(function(){
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=Math.imul(a^(a>>>15),1|a); t=(t+Math.imul(t^(t>>>7),61|t))^t; return ((t^(t>>>14))>>>0)/4294967296; }; }
function gauss(r){ let u=0,v=0; while(u===0)u=r(); v=r(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
function txt(API,g,x,y,s,o={}){ const e=API.mk('text',{x,y,'font-size':o.size||18,'text-anchor':o.anchor||'middle',fill:o.fill||'#16233D','font-weight':o.w||400},g); e.textContent=s; return e; }
const SUB={ipa:{n:'아이소프로필 알코올',M:60.10,bp:82},etoh:{n:'에탄올',M:46.07,bp:78},ace:{n:'아세톤',M:58.08,bp:56},unk:{n:'미지 시료',M:88.11,bp:77}};
const CAND=[['메탄올',32.04],['에탄올',46.07],['아세톤',58.08],['아이소프로필 알코올',60.10],['아세트산 에틸',88.11]];
window.DECK_LABS = {
  ac211mm(root, API){
    const O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`);
    const svg=root.querySelector('.lab-fig svg');
    let st={s:'ipa'}, log=[], rnd=rng(83);
    const s0=API.mk('g',{},svg);
    API.mk('rect',{x:30,y:110,width:250,height:120,rx:8,fill:'#DDEEF8',stroke:'#7E8B98','stroke-width':2},s0);
    API.mk('line',{x1:32,y1:128,x2:278,y2:128,stroke:'#9FC3DD','stroke-width':2},s0);
    API.mk('path',{d:'M141 30 L141 100 A50 50 0 1 0 169 100 L169 30 Z',fill:'#FFFFFF','fill-opacity':.85,stroke:'#7E8B98','stroke-width':2.5},s0);
    API.mk('path',{d:'M135 30 L175 30 L173 20 L137 20 Z',fill:'#C9D3DD',stroke:'#5B6B7F','stroke-width':1.5},s0);
    API.mk('rect',{x:20,y:230,width:270,height:14,rx:3,fill:'#C9D3DD',stroke:'#16233D','stroke-width':1.5},s0);
    const g=API.mk('g',{},svg), vap=API.mk('g',{},g), liq=API.mk('path',{d:'M128 190 Q155 198 182 190 L182 196 Q155 206 128 196 Z',fill:'#7B4FC8','fill-opacity':.5},g);
    const dots=[]; for(let i=0;i<9;i++){ dots.push(API.mk('circle',{r:5,fill:'#7B4FC8','fill-opacity':.35,stroke:'#7B4FC8','stroke-width':1},vap)); }
    const tx=[0,1,2,3,4].map(i=>txt(API,g,320,40+i*30,'',{anchor:'start',size:19}));
    const wet=API.mk('g',{},g); [[118,150],[192,170],[126,186]].forEach(([x,y])=>API.mk('ellipse',{cx:x,cy:y,rx:4,ry:6,fill:'#9FC3DD'},wet));
    function show(){
      O('v').textContent=I('v').value+' mL'; O('t').textContent=(+I('t').value).toFixed(1)+' °C'; O('pa').textContent=I('pa').value+' mmHg';
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===st.s));
      O('log').innerHTML=log.map((r,i)=>`<tr><td>${i+1}</td><td>${r.n}</td><td>${r.m.toFixed(3)}</td><td>${r.V.toFixed(3)}</td><td>${r.T.toFixed(1)}</td><td>${r.P.toFixed(3)}</td><td>${r.M.toFixed(1)}</td></tr>`).join('');
      wet.style.display=I('wet').checked?'':'none'; liq.style.display=I('early').checked?'':'none';
    }
    function idle(){ tx.forEach(e=>e.textContent=''); dots.forEach((d,i)=>{ d.setAttribute('cx',140+(i%3)*15); d.setAttribute('cy',130+Math.floor(i/3)*20); }); O('big').textContent='—'; O('msg').textContent='시료와 조건을 정하고 「실험하기」를 누르자. 오차 원인을 하나씩 켜 보며 결과를 비교하자.'; show(); }
    function run(){
      const S=SUB[st.s], V=+I('v').value/1000, t=+I('t').value, pa=+I('pa').value, P=pa/760;
      const n=P*V/(0.082057*(t+273.15));
      let m=n*S.M*(1+0.004*gauss(rnd));
      if(I('wet').checked) m+=0.025+0.02*rnd();
      if(I('early').checked) m+=0.08+0.07*rnd();
      m=Math.round(m*1000)/1000;
      const T=t+273, M=m*0.08206*T/(P*V);
      log.push({n:S.n,m,V,T,P,M}); if(log.length>6) log.shift();
      tx[0].textContent=`응축한 액체 m = ${m.toFixed(3)} g`; tx[1].textContent=`부피 V = ${V.toFixed(3)} L`;
      tx[2].textContent=`온도 T = ${T.toFixed(1)} K`; tx[3].textContent=`압력 P = ${P.toFixed(3)} atm`;
      tx[4].textContent=`M = mRT/(PV) = ${M.toFixed(1)} g/mol`;
      O('big').textContent=M.toFixed(1)+' g/mol';
      let msg;
      if(st.s==='unk'){ const b=CAND.reduce((a,c)=>Math.abs(c[1]-M)<Math.abs(a[1]-M)?c:a); msg=`후보 가운데 가장 가까운 것: ${b[0]} (${b[1]} g/mol).`; }
      else { let er=(M-S.M)/S.M*100; if(Math.abs(er)<0.05) er=0; msg=`문헌값 ${S.M} g/mol과의 오차 ${er>=0?'+':''}${er.toFixed(1)} %.`; }
      if(I('wet').checked||I('early').checked) msg+=' 켜 둔 오차 원인은 측정 질량을 크게 하여 몰질량이 커진다.';
      else msg+=' 액체가 모두 기화했고 물기를 닦았다.';
      O('msg').textContent=msg; show();
    }
    root.querySelectorAll('[data-s]').forEach(b=>b.addEventListener('click',()=>{st.s=b.dataset.s;idle();}));
    ['v','t','pa'].forEach(k=>I(k).addEventListener('input',idle)); ['wet','early'].forEach(k=>I(k).addEventListener('change',idle));
    root.querySelector('[data-act="run"]').addEventListener('click',run);
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{ log=[]; rnd=rng(83); st.s='ipa'; I('v').value=256; I('t').value=99; I('pa').value=760; I('wet').checked=false; I('early').checked=false; idle(); });
    idle();
    API.loop(root,(dt,tt)=>{ dots.forEach((d,i)=>{ const a=tt*(1.3+i*0.17)+i*2.1; d.setAttribute('cx',(155+38*Math.sin(a)).toFixed(1)); d.setAttribute('cy',(148+34*Math.cos(a*0.8+i)).toFixed(1)); }); });
  }
};
})();
