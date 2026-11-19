/* 고급화학 1-4-S1 [심화] — 실험실
   ac14s1path : 반응 경로 고르기 (덱 자체 ◇ — 교과서 탐구 없음)
     기질(메틸·1차·2차·3차 브로민화 알킬) · 시약(I⁻, CN⁻, OH⁻, CH3CH2O⁻, (CH3)3CO⁻, H2O) · 용매(비양성자성/양성자성) · 온도(25 °C/가열)를 고르고
     경로를 예측한 뒤 「반응시키기」 → 우세한 경로(SN2·SN1·E2·E1·SN1+E1·거의 없음), 주생성물, 판단 근거, 에너지 도표(언덕 1개/2개),
     기록 표에 한 행씩 쌓임. 규칙은 자체 교과서 표 1-24–1-27, 그림 1-105, 90쪽 예제(plan.md 2절). */
window.DECK_LABS = {
  ac14s1path(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=root.querySelector('.lab-fig svg'), g=API.mk('g',{},svg), dotG=API.mk('g',{},svg);
    const SUB={me:{n:'메틸',f:'CH3Br',R:'CH3'},p1:{n:'1차',f:'CH3CH2CH2CH2Br',R:'CH3CH2CH2CH2'},p2:{n:'2차',f:'CH3CH2CHBrCH3',R:'CH3CH2CH(CH3)'},p3:{n:'3차',f:'(CH3)3CBr',R:'(CH3)3C'}};
    const RG={I:{t:'I-',txt:'I⁻',k:'wb'},CN:{t:'CN-',txt:'CN⁻',k:'wb'},OH:{t:'OH-',txt:'OH⁻',k:'sb'},EtO:{t:'CH3CH2O-',txt:'에탄올산 이온',k:'sb'},tBuO:{t:'(CH3)3CO-',txt:'부피 큰 염기',k:'bulky'},H2O:{t:'H2O',txt:'물',k:'neu'}};
    const NUP={I:['I','아이오도'],CN:['CN','나이트릴'],OH:['OH','알코올'],EtO:['OCH2CH3','에테르'],tBuO:['OC(CH3)3','에테르'],H2O:['OH','알코올']};
    const PN={me:{I:'아이오도메테인',CN:'아세토나이트릴',OH:'메탄올',EtO:'에틸 메틸 에테르',tBuO:'삼차-뷰틸 메틸 에테르'},
      p1:{I:'1-아이오도뷰테인',CN:'펜테인나이트릴',OH:'1-뷰탄올',EtO:'뷰틸 에틸 에테르'},
      p2:{I:'2-아이오도뷰테인(반전)',CN:'2-메틸뷰테인나이트릴(반전)'}};
    let st={s:'p1',r:'CN',v:'apr',t:'rt',p:null}, log=[], n=0, hit=0, cur=null, tt=0;
    const segs=(attr,key)=>root.querySelectorAll(`[data-${attr}]`).forEach(b=>b.addEventListener('click',e=>{ e.stopPropagation(); st[key]=b.dataset[attr]; if(key==='r'&&st.r==='H2O') st.v='pro'; if(key==='v'&&st.v==='apr'&&st.r==='H2O') st.r='OH'; cur=null; sync(); }));
    segs('s','s'); segs('r','r'); segs('v','v'); segs('t','t');
    root.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',e=>{ e.stopPropagation(); st.p=b.dataset.p; sync(); }));
    function sync(){
      root.querySelectorAll('[data-s]').forEach(b=>b.classList.toggle('on',b.dataset.s===st.s));
      root.querySelectorAll('[data-r]').forEach(b=>b.classList.toggle('on',b.dataset.r===st.r));
      root.querySelectorAll('[data-v]').forEach(b=>b.classList.toggle('on',b.dataset.v===st.v));
      root.querySelectorAll('[data-t]').forEach(b=>b.classList.toggle('on',b.dataset.t===st.t));
      root.querySelectorAll('[data-p]').forEach(b=>b.classList.toggle('ac14s1-pk',b.dataset.p===st.p));
      O('cond').textContent=`${SUB[st.s].n} + ${RG[st.r].txt}, ${st.v==='apr'?'DMSO':'물·에탄올'}, ${st.t==='rt'?'25 °C':'가열'}`;
      if(!cur){ O('path').textContent='?'; O('msg').textContent=st.p?'「반응시키기」를 눌러 예측을 확인하자.':'먼저 우세한 경로를 예측하여 고르자.'; draw(null); }
      O('score').textContent=n?`맞힘 ${hit} / ${n}`:'';
    }
    // ── 규칙 (교과서 표 1-24–1-27, 그림 1-105)
    function decide(){
      const s=st.s, r=st.r, k=RG[r].k, apr=st.v==='apr', hot=st.t==='hot';
      const R=SUB[s].R; let path, why, prod, pname, minor='';
      const sub=()=>{ const [nu,kind]=NUP[r]; return {prod:R+nu, pname:(PN[s]&&PN[s][r])||kind}; };
      if(s==='me'){
        if(k==='neu'){ path='none'; why='메틸: 탄소 양이온이 생기지 않고, 물은 약한 친핵체라 SN2도 매우 느리다.'; }
        else { path='SN2'; why='메틸: β 수소가 없어 제거가 불가능하고 입체 장애가 가장 작다 → SN2'+(k==='bulky'?' (부피 큰 알코올산 이온도 친핵체로 작용 — 윌리엄슨 에테르 합성)':'')+(apr?'':' · 양성자성 용매라 조금 느리다'); ({prod,pname}=sub()); }
      } else if(s==='p1'){
        if(k==='neu'){ path='none'; why='1차: 1차 탄소 양이온은 불안정(SN1·E1 ×), 물은 약한 친핵체(SN2 매우 느림).'; }
        else if(k==='bulky'){ path='E2'; why='1차 + 부피 큰 강한 염기 → 탄소에 다가가기 어렵고 β 수소를 떼어 낸다 → E2'; prod='CH3CH2CH=CH2'; pname='1-뷰텐'; }
        else { path='SN2'; why='1차 + 좋은 친핵체 → 입체 장애가 작아 SN2'+(apr?' (비양성자성 용매: 빠름)':' (양성자성 용매: 친핵체가 수소 결합으로 둘러싸여 느림)'); ({prod,pname}=sub()); if(k==='sb'&&hot) minor='가열하면 E2 생성물(1-뷰텐)이 조금 늘어난다.'; }
      } else if(s==='p2'){
        if(k==='wb'){ path='SN2'; why='2차 + 염기성이 약한 친핵체'+(apr?' + 비양성자성 용매 → SN2, 입체 배열 반전':' → SN2 (양성자성 용매라 느리다)'); ({prod,pname}=sub()); }
        else if(k==='sb'||k==='bulky'){ path='E2'; why='2차 + 강한 염기 → E2, 자이체프 생성물이 주생성물'; prod='CH3CH=CHCH3'; pname='2-뷰텐(주) + 1-뷰텐'; if(r==='EtO') minor='교과서: 2-뷰텐 약 81 %, 1-뷰텐 약 19 %'; }
        else { path='SN1E1'; why='2차 + 물(약한 친핵체·약한 염기, 양성자성) → SN1과 E1이 함께, 그러나 느리다.'; prod='CH3CH2CH(OH)CH3'; pname='2-뷰탄올 + 2-뷰텐'; minor=hot?'가열하면 E1(2-뷰텐) 비율이 늘어난다.':''; }
      } else {
        if(k==='sb'||k==='bulky'||r==='CN'){ path='E2'; why='3차: SN2 불가(입체 장애) + '+(r==='CN'?'염기로 작용하는 CN⁻':'강한 염기')+' → E2'; prod='(CH3)2C=CH2'; pname='2-메틸프로펜'; }
        else if(k==='neu'||!apr){ path='SN1E1'; why='3차 + 중성·양성자성 용매 → 안정한 3차 탄소 양이온 → SN1과 E1이 함께'; prod=r==='I'?'(CH3)3CI':'(CH3)3COH'; pname=(r==='I'?'2-아이오도-2-메틸프로페인':'2-메틸-2-프로판올')+' + 2-메틸프로펜'; minor=hot?'가열하면 제거(2-메틸프로펜) 비율이 늘어난다 (교과서: 65 °C, 80 % 에탄올 수용액에서 치환 : 제거 ≈ 64 : 36).':'25 °C에서는 치환 생성물이 더 많다.'; }
        else { path='none'; why='3차 + I⁻ + 비양성자성 용매: SN2는 입체 장애로 불가, 양이온을 안정화하는 양성자성 용매가 없어 SN1도 어렵다.'; }
      }
      return {path,why,prod,pname,minor};
    }
    const PL={SN2:'SN2',SN1:'SN1',E2:'E2',E1:'E1',SN1E1:'SN1 + E1',none:'거의 반응 안 함'};
    function correct(p,path){ return p===path || (path==='SN1E1'&&(p==='SN1'||p==='E1')); }
    function draw(res){
      while(g.firstChild) g.removeChild(g.firstChild);
      const x0=40,y0=226,W=540;
      API.arrow(g,x0,y0,x0,18,'muted',2); API.arrow(g,x0,y0,W-8,y0,'muted',2);
      const t1=API.mk('text',{x:x0+8,y:30,'font-size':17,fill:'#5B6B7F'},g); t1.textContent='에너지';
      const t2=API.mk('text',{x:W-12,y:y0+20,'font-size':17,fill:'#5B6B7F','text-anchor':'end'},g); t2.textContent='반응 경로';
      Ov('prod').innerHTML=''; Ov('pname').textContent='';
      if(!res){ API.place(Ov('prod'),0,0,false); API.place(Ov('pname'),0,0,false); cur=null; return; }
      const two=(res.path==='SN1E1'||res.path==='SN1'||res.path==='E1'), none=res.path==='none';
      let pts;
      if(none) pts=[[70,150],[290,34],[500,170]];
      else if(two) pts=[[70,150],[180,60],[260,120],[330,92],[500,182]];
      else pts=[[70,150],[280,70],[500,180]];
      let d=`M${pts[0][0]} ${pts[0][1]}`;
      for(let i=1;i<pts.length;i++){ const [a,b]=pts[i-1],[c,e]=pts[i],h=(c-a)/2; d+=` C${a+h} ${b} ${c-h} ${e} ${c} ${e}`; }
      API.mk('path',{d,fill:'none',stroke:'#16233D','stroke-width':3,'data-path':'1'},g);
      API.mk('line',{x1:52,y1:150,x2:110,y2:150,stroke:'#16233D','stroke-width':3},g);
      const lab=(x,y,t,c,anchor)=>{ const e=API.mk('text',{x,y,'font-size':17,fill:c||'#16233D','text-anchor':anchor||'middle'},g); e.textContent=t; };
      lab(80,172,'반응물');
      if(none){ lab(290,26,'Eₐ 매우 큼','#E08A2C'); }
      else if(two){ API.mk('circle',{cx:260,cy:120,r:6,fill:'#E08A2C'},g); lab(260,146,'탄소 양이온(중간체)','#E08A2C'); lab(180,52,'속도 결정 단계','#D7263D'); }
      else { lab(280,62,'전이 상태 ‡'); lab(280,100,'중간체 없음','#5B6B7F'); }
      if(!none){ API.mk('line',{x1:460,y1:pts[pts.length-1][1],x2:530,y2:pts[pts.length-1][1],stroke:'#16233D','stroke-width':3},g);
        Ov('prod').innerHTML=API.tex('\\ce{'+res.prod+'}'); Ov('pname').textContent=res.pname;
        API.place(Ov('prod'),440,pts[pts.length-1][1]-34,true); API.place(Ov('pname'),400,pts[pts.length-1][1]+14,true); }
      else { API.place(Ov('prod'),0,0,false); API.place(Ov('pname'),0,0,false); }
      cur={pts,path:g.querySelector('[data-path]')}; tt=0;
    }
    root.querySelector('[data-act="run"]').addEventListener('click',e=>{
      e.stopPropagation();
      const res=decide(); draw(res);
      O('path').textContent=PL[res.path];
      const ok=st.p?correct(st.p,res.path):null;
      n++; if(ok) hit++;
      O('msg').textContent=(ok===null?'(예측 없음) ':ok?'예측이 맞았다! ':'예측과 다르다. ')+res.why+(res.minor?' '+res.minor:'');
      log.unshift([n,SUB[st.s].n,`${RG[st.r].txt}·${st.v==='apr'?'DMSO':'양성자성'}·${st.t==='rt'?'25 °C':'가열'}`,st.p?PL[st.p]:'–',PL[res.path]+(ok?' ○':ok===false?' ✕':'')]);
      if(log.length>5) log.pop();
      const tb=O('log'); tb.innerHTML=log.map(r=>'<tr>'+r.map(c=>`<td>${c}</td>`).join('')+'</tr>').join('');
      O('score').textContent=`맞힘 ${hit} / ${n}`;
      st.p=null; root.querySelectorAll('[data-p]').forEach(b=>b.classList.remove('ac14s1-pk'));
    });
    root.querySelector('[data-act="reset"]').addEventListener('click',e=>{ e.stopPropagation(); st={s:'p1',r:'CN',v:'apr',t:'rt',p:null}; log=[]; n=0; hit=0; O('log').innerHTML=''; cur=null; sync(); });
    // 경로 위를 지나가는 점(보일 때만)
    const dot=API.mk('circle',{r:7,fill:'#E08A2C',stroke:'#fff','stroke-width':2,opacity:0},dotG);
    API.loop(root,(dt)=>{
      if(!cur||!cur.path){ dot.setAttribute('opacity',0); return; }
      tt=(tt+dt*0.35)%1.25; const L=cur.path.getTotalLength(), q=Math.min(tt,1)*L, P=cur.path.getPointAtLength(q);
      dot.setAttribute('cx',P.x); dot.setAttribute('cy',P.y); dot.setAttribute('opacity',1);
    });
    sync();
  }
};
