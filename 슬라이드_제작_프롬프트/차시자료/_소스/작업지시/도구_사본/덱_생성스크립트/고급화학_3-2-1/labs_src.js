/* 고급화학 3-2-1 — 실험실
   ac321micro : ◇ 덱 자체 「미시 상태 세기」 (선생님 지시 — 덱목록 labCandidate는 「없음」이었음)
     · 번호 붙은(구별되는) 입자 N개(1–8), 왼쪽 a칸(1–5) + 오른쪽 b칸(0–5). 입자 하나는 아무 칸에나, 한 칸에 여러 개도 됨(이상 기체)
     · W처음 = a^N(칸막이 닫힘: 모두 왼쪽), W나중 = (a+b)^N, 모두 왼쪽 확률 = (a/(a+b))^N, ΔS = k ln(W나중/W처음) = N ln((a+b)/a) · k
     · 왼쪽 입자 수 n의 이론 확률 P(n) = C(N,n) a^n b^(N−n) / (a+b)^N
     · 섞기: 고정 시드 난수로 입자마다 칸을 고름 → 왼쪽 입자 수 빈도 누적(막대) · 기록 표(최근 4행) */
(function(){
const M='−';
window.DECK_LABS = {
  ac321micro(root, API){
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), I=k=>$(`[data-i="${k}"]`);
    const svg=$('.lab-fig svg'), g=API.mk('g',{},svg);
    const GAS='#F2A65A', GAS_S='#B4561C', INK='#16233D', MUT='#5B6B7F', PLUS='#D7263D', CW=56, BY=34, BH=100;
    let N,a,b,pos,cnt,tot,log,auto,acc,seed;
    const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    const comb=(n,k)=>{ let r=1; for(let i=1;i<=k;i++) r=r*(n-k+i)/i; return r; };
    const fmtInt=v=>Math.round(v).toLocaleString('en-US');
    const mk=(t,at,p)=>API.mk(t,at,p||g);
    function txt(x,y,s,o){ const t=mk('text',Object.assign({x,y,'font-size':18,'text-anchor':'middle',fill:INK},o||{})); t.textContent=s; return t; }
    function readSet(){ N=+I('n').value; a=+I('a').value; b=+I('b').value; }
    function startPos(){ pos=[]; for(let i=0;i<N;i++) pos.push(i%a); }
    function clearCounts(){ cnt=new Array(9).fill(0); tot=0; }
    function init(){ I('n').value=4; I('a').value=2; I('b').value=2; seed=20261120; log=[]; auto=false; acc=0; readSet(); startPos(); clearCounts(); }
    function theory(){ const S=a+b, P=[]; for(let n=0;n<=N;n++) P.push(b===0?(n===N?1:0):comb(N,n)*Math.pow(a,n)*Math.pow(b,N-n)/Math.pow(S,N)); return P; }
    function shuffle(k){ if(b===0){ startPos(); } for(let r=0;r<k;r++){ for(let i=0;i<N;i++) pos[i]=Math.floor(rnd()*(a+b)); let nl=0; pos.forEach(c=>{ if(c<a) nl++; }); cnt[nl]++; tot++; } }
    function vals(){ const W1=Math.pow(a,N), W2=Math.pow(a+b,N), p=Math.pow(a/(a+b),N), ds=N*Math.log((a+b)/a); return {W1,W2,p,ds}; }
    function draw(){
      g.innerHTML=''; const v=vals(), S=a+b, X0=330-S*CW/2;
      // 상자와 칸
      mk('rect',{x:X0,y:BY,width:S*CW,height:BH,rx:4,fill:'#FFFFFF',stroke:INK,'stroke-width':3});
      for(let c=1;c<S;c++) if(c!==a) mk('line',{x1:X0+c*CW,y1:BY,x2:X0+c*CW,y2:BY+BH,stroke:'#C9D2DB','stroke-width':1.5});
      if(b>0) mk('line',{x1:X0+a*CW,y1:BY-8,x2:X0+a*CW,y2:BY+BH+8,stroke:PLUS,'stroke-width':3,'stroke-dasharray':'7 5'});
      txt(X0+a*CW/2,BY-10,`왼쪽 ${a}칸`,{fill:MUT}); if(b>0) txt(X0+a*CW+b*CW/2,BY-10,`오른쪽 ${b}칸`,{fill:MUT});
      // 입자 (한 칸 안 2열 × 4행)
      const occ=new Array(S).fill(0);
      pos.forEach((c,i)=>{ const k=occ[c]++; const x=X0+c*CW+CW/2+(k%2?11.5:-11.5), y=BY+14+Math.floor(k/2)*23;
        mk('circle',{cx:x,cy:y,r:11,fill:GAS,stroke:GAS_S,'stroke-width':1.5}); txt(x,y+6,String(i+1),{'font-size':16,'font-weight':700}); });
      // 확률 분포
      const P=theory(), HX0=78, HX1=640, HY0=250, HY1=166; const gw=(HX1-HX0)/(N+1);
      let ymax=Math.max(...P); for(let n=0;n<=N;n++) if(tot) ymax=Math.max(ymax,cnt[n]/tot); ymax=Math.min(1,Math.ceil(ymax*10+0.0001)/10);
      const yv=p=>HY0-(HY0-HY1)*p/ymax;
      mk('line',{x1:HX0,y1:HY0,x2:HX1,y2:HY0,stroke:MUT,'stroke-width':2}); mk('line',{x1:HX0,y1:HY0,x2:HX0,y2:HY1-8,stroke:MUT,'stroke-width':2});
      [0,ymax/2,ymax].forEach(t=>{ mk('line',{x1:HX0-5,y1:yv(t),x2:HX0,y2:yv(t),stroke:MUT,'stroke-width':1.5}); txt(HX0-8,yv(t)+6,t.toFixed(t===0?0:2),{'text-anchor':'end','font-size':16}); });
      txt(HX0+4,HY1-14,'확률',{'text-anchor':'start',fill:MUT});
      for(let n=0;n<=N;n++){ const cx=HX0+gw*(n+.5), bw=Math.min(22,gw*.36);
        if(tot){ const q=cnt[n]/tot; mk('rect',{x:cx+1,y:yv(q),width:bw,height:HY0-yv(q),fill:GAS,'fill-opacity':.75,stroke:GAS_S,'stroke-width':1}); }
        mk('rect',{x:cx-bw-1,y:yv(P[n]),width:bw,height:HY0-yv(P[n]),fill:'#FFFFFF',stroke:INK,'stroke-width':2});
        txt(cx,HY0+19,String(n),{'font-size':16}); }
      txt((HX0+HX1)/2,293,'왼쪽에 있는 입자 수',{fill:MUT});
      mk('rect',{x:400,y:150,width:14,height:14,fill:'#FFFFFF',stroke:INK,'stroke-width':2}); txt(420,163,'이론',{'text-anchor':'start','font-size':16});
      mk('rect',{x:470,y:150,width:14,height:14,fill:GAS,'fill-opacity':.75,stroke:GAS_S}); txt(490,163,`섞은 결과 ${tot}회`,{'text-anchor':'start','font-size':16});
      // 출력
      O('n').textContent=`${N}개`; O('a').textContent=`${a}칸`; O('b').textContent=b?`${b}칸`:'0칸 (닫힘)';
      O('w1').textContent=fmtInt(v.W1); O('w2').textContent=fmtInt(v.W2);
      O('p').textContent=b===0?'1':`${v.p<0.001?v.p.toExponential(2):v.p.toFixed(4)} (${fmtInt(1/v.p)}번에 1번)`;
      O('ds').textContent=`${v.ds.toFixed(2)} k`;
      const r=(a+b)/a, allL=tot?cnt[N]:0; let nmax=0; P.forEach((p,n)=>{ if(p>P[nmax]+1e-12) nmax=n; });
      O('msg').textContent= b===0 ? '오른쪽 칸이 없으면 칸막이를 열어도 W가 그대로이므로 ΔS = 0이다.'
        : `부피가 ${+(r.toFixed(2))}배 → 입자마다 자리가 ${+(r.toFixed(2))}배, W는 ${+(r.toFixed(2))}^${N} = ${fmtInt(Math.pow(r,N))}배. 확률이 가장 큰 것은 왼쪽 ${nmax}개(부피 비율대로 퍼진 분포).`
          + (tot?` 섞은 ${tot}회 중 모두 왼쪽 ${allL}회.`:'') + ` 1 mol이면 ΔS = R ln ${+(r.toFixed(2))} = ${(8.314*Math.log(r)).toFixed(2)} J/K.`;
    }
    function renderLog(){ const tb=O('log'); tb.innerHTML='';
      log.slice(-4).forEach(r=>{ const tr=document.createElement('tr');
        tr.innerHTML=`<td>${r.no}</td><td>${r.N}</td><td>${r.a}</td><td>${r.b}</td><td>${fmtInt(r.W1)}</td><td>${fmtInt(r.W2)}</td><td>${r.p<0.001?r.p.toExponential(2):r.p.toFixed(4)}</td><td>${r.ds.toFixed(2)} k</td><td>${r.tot}</td>`; tb.appendChild(tr); }); }
    function setAuto(on){ auto=on; const bt=$('[data-act="auto"]'); bt.classList.toggle('on',on); bt.textContent=on?'멈춤':'자동 섞기'; }
    root.querySelectorAll('input').forEach(i=>i.addEventListener('input',()=>{ readSet(); startPos(); clearCounts(); draw(); }));
    $('[data-act="one"]').addEventListener('click',()=>{ shuffle(1); draw(); });
    $('[data-act="many"]').addEventListener('click',()=>{ shuffle(100); draw(); });
    $('[data-act="auto"]').addEventListener('click',()=>{ setAuto(!auto); });
    $('[data-act="rec"]').addEventListener('click',()=>{ const v=vals(); log.push(Object.assign({no:log.length+1,N,a,b,tot},v)); renderLog(); });
    $('[data-act="reset"]').addEventListener('click',()=>{ init(); setAuto(false); renderLog(); draw(); });
    API.loop(root,dt=>{ if(!auto) return; acc+=dt; if(acc>=0.25){ acc=0; shuffle(1); draw(); } });
    init(); draw(); renderLog();
    API.ready(()=>draw()); API.onShow(s=>{ if(s===root.closest('.slide')) draw(); });
  }
};
})();
