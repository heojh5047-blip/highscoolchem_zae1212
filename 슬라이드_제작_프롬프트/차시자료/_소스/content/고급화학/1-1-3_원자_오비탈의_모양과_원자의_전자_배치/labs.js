/* 고급화학 1-1-3 — 실험실
   ac113fill : 전자 배치 상자 실험실 (덱 자체 ◇, 성취기준 01-02)
     · 원자 번호 Z(1–36)와 전하(−2…+3) → 필요한 전자 수 = Z − 전하
     · 상자 1s 2s 2p 3s 3p 4s 3d 4p(18칸)를 에너지 계단으로. 상자 누르기: 빈칸 → ↑ → ↓ → ↑↓ → 빈칸
     · 「전자 1개 넣기」= 쌓음 순서(1s→2s→2p→3s→3p→4s→3d→4p)대로 훈트 규칙을 지켜 하나씩
     · 「모두 채우기」= 실제 바닥상태(Cr·Cu 예외, 양이온은 n이 큰 오비탈(4s)부터 뺌)
     · 「규칙 검사」= 전자 수 → 부껍질별 전자 수(쌓음 원리·Cr/Cu 예외·4s 먼저) → 훈트 규칙 */
(function(){
const SUB=[{k:'1s',n:1,l:0,m:1,y:214},{k:'2s',n:2,l:0,m:1,y:180},{k:'2p',n:2,l:1,m:3,y:154},{k:'3s',n:3,l:0,m:1,y:118},
           {k:'3p',n:3,l:1,m:3,y:94},{k:'4s',n:4,l:0,m:1,y:58},{k:'3d',n:3,l:2,m:5,y:44},{k:'4p',n:4,l:1,m:3,y:10}];
const SYM=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr'];
const NAME=['수소','헬륨','리튬','베릴륨','붕소','탄소','질소','산소','플루오린','네온','나트륨','마그네슘','알루미늄','규소','인','황','염소','아르곤','칼륨','칼슘','스칸듐','타이타늄','바나듐','크로뮴','망가니즈','철','코발트','니켈','구리','아연','갈륨','저마늄','비소','셀레늄','브로민','크립톤'];
const BW=30, GAP=12, X0=44;
let xx=X0; SUB.forEach(s=>{ s.x=xx; xx+=s.m*BW+GAP; });
const NB=SUB.reduce((a,s)=>a+s.m,0);
function aufbau(ne){ const c=SUB.map(()=>0); let r=ne; SUB.forEach((s,i)=>{ const t=Math.min(r,2*s.m); c[i]=t; r-=t; }); return c; }
function neutral(Z){ const c=aufbau(Z); if(Z===24||Z===29){ c[5]=1; c[6]=(Z===24?5:10); } return c; }
const REMOVE=[7,5,6,4,3,2,1,0]; // 4p,4s,3d,3p,3s,2p,2s,1s (n 큰 것부터)
function target(Z,q){
  const c=neutral(Z);
  if(q>0){ let r=q; for(const i of REMOVE){ const t=Math.min(r,c[i]); c[i]-=t; r-=t; } }
  if(q<0){ let r=-q; for(let i=0;i<SUB.length&&r>0;i++){ const t=Math.min(r,2*SUB[i].m-c[i]); c[i]+=t; r-=t; } }
  return c;
}
function boxesFor(c){ // 부껍질 전자 수 → 칸(훈트 규칙)
  const o=[]; SUB.forEach((s,i)=>{ const e=c[i]; for(let j=0;j<s.m;j++){ o.push(e>j+s.m?'ud':(e>j?'u':'')); } }); return o;
}
window.DECK_LABS = {
  ac113fill(root, API){
    const $=s=>root.querySelector(s), O=k=>root.querySelector(`[data-o="${k}"]`), I=k=>root.querySelector(`[data-i="${k}"]`), Ov=k=>root.querySelector(`[data-ov="${k}"]`);
    const svg=$('svg');
    let st={q:0,occ:Array(NB).fill(''),last:-1}, log=[];
    const stat=API.mk('g',{},svg);
    API.mk('line',{x1:18,y1:286,x2:18,y2:10,stroke:'#5B6B7F','stroke-width':2},stat);
    API.mk('path',{d:'M11 20 L18 8 L25 20',fill:'none',stroke:'#5B6B7F','stroke-width':2},stat);
    API.texText(stat,30,22,'\\text{에너지}',{size:18,anchor:'start'});
    SUB.forEach(s=>API.texText(stat,s.x+s.m*BW/2,s.y+BW+20,s.k,{size:19,anchor:'middle'}));
    const g=API.mk('g',{},svg);
    const off=[]; { let k=0; SUB.forEach((s,i)=>{ for(let j=0;j<s.m;j++) off.push({i,j,x:s.x+j*BW,y:s.y}); }); }
    const Z=()=>+I('z').value, need=()=>Z()-st.q;
    const counts=o=>SUB.map((s,i)=>off.reduce((a,b,k)=>a+(b.i===i?o[k].length:0),0));
    function harp(x,y,up,col){ const p=up?`M${x} ${y+24} L${x} ${y+6} L${x-5} ${y+13}`:`M${x} ${y+6} L${x} ${y+24} L${x+5} ${y+17}`;
      API.mk('path',{d:p,fill:'none',stroke:col,'stroke-width':2.4,'stroke-linecap':'round','stroke-linejoin':'round'},g); }
    function label(){ const z=Z(), q=st.q; return '\\mathrm{'+SYM[z-1]+'}'+(q===0?'':'^{'+(Math.abs(q)>1?Math.abs(q):'')+(q>0?'+':'-')+'}'); }
    function cfg(c){ const parts=SUB.map((s,i)=>c[i]?s.k+'^{'+c[i]+'}':'').filter(Boolean); return parts.length?parts.join('\\,'):'\\text{(전자 없음)}'; }
    function abbr(c){
      const full=i=>c[i]===2*SUB[i].m;
      let core='',from=0;
      if([0,1,2,3,4].every(full)){ core='[\\mathrm{Ar}]'; from=5; } else if([0,1,2].every(full)){ core='[\\mathrm{Ne}]'; from=3; } else if(full(0)){ core='[\\mathrm{He}]'; from=1; }
      const rest=SUB.map((s,i)=>({s,i})).filter(o=>o.i>=from&&c[o.i]).sort((a,b)=>a.s.n-b.s.n||a.s.l-b.s.l).map(o=>o.s.k+'^{'+c[o.i]+'}');
      return (core+rest.join('\\,'))||'\\text{—}';
    }
    const unpaired=o=>o.filter(v=>v.length===1).length;
    function valence(c){ let nmax=0; SUB.forEach((s,i)=>{ if(c[i]) nmax=Math.max(nmax,s.n); }); return SUB.reduce((a,s,i)=>a+(s.n===nmax&&s.l<2?c[i]:0),0); }
    function draw(){
      while(g.firstChild) g.removeChild(g.firstChild);
      const z=Z(); O('z').textContent=`${z} ${SYM[z-1]} (${NAME[z-1]})`;
      root.querySelectorAll('[data-q]').forEach(b=>b.classList.toggle('on',+b.dataset.q===st.q));
      off.forEach((b,k)=>{
        const v=st.occ[k];
        const r=API.mk('rect',{x:b.x,y:b.y,width:BW,height:BW,fill:v.length===1?'rgba(224,138,44,.18)':'#fff',stroke:'#16233D','stroke-width':1.5,class:'ac113-box','data-k':k},g);
        r.addEventListener('click',()=>tap(k));
        const cx=b.x+BW/2, col=k===st.last?'#2E9E6A':'#16233D';
        if(v==='u') harp(cx,b.y,true,col); else if(v==='d') harp(cx,b.y,false,col);
        else if(v==='ud'){ harp(cx-6,b.y,true,'#16233D'); harp(cx+6,b.y,false,col); }
      });
      const c=counts(st.occ), tot=c.reduce((a,b)=>a+b,0);
      O('cnt').textContent=`${tot} / ${need()}`;
      Ov('cfg').innerHTML=API.tex(cfg(c)+(tot?'\\ =\\ '+abbr(c):'')); API.place(Ov('cfg'),360,288,true);
      O('info').innerHTML=`${API.tex(label())} ${NAME[z-1]}${st.q?' 이온':''} · 홀전자 <b>${unpaired(st.occ)}개</b> · 원자가 전자 <b>${valence(c)}개</b>`;
    }
    function check(){
      const ne=need(), c=counts(st.occ), tot=c.reduce((a,b)=>a+b,0), t=target(Z(),st.q), z=Z(), q=st.q;
      if(tot!==ne) return {ok:false,m:tot<ne?`전자가 ${ne-tot}개 더 필요하다.`:`전자가 ${tot-ne}개 많다.`,s:'전자 수'};
      const same=c.every((v,i)=>v===t[i]);
      const ans='바닥상태: '+abbr(t).replace(/\\mathrm\{(\w+)\}/g,'$1').replace(/[\\{}]/g,'').replace(/\^/g,'');
      if(!same){
        const nv=aufbau(ne);
        if(q===0&&(z===24||z===29)&&c.every((v,i)=>v===nv[i])) return {ok:false,m:`쌓음 순서대로는 맞지만 실제 바닥상태는 ${z===24?'[Ar]3d⁵4s¹ — 반쯤 채워진 d⁵':'[Ar]3d¹⁰4s¹ — 모두 채워진 d¹⁰'} 배치가 더 안정하다(4s와 3d의 에너지 차가 작다).`,s:'Cr·Cu 예외'};
        if(q>0&&c[5]>t[5]) return {ok:false,m:'전이 원소가 양이온이 될 때는 4s 전자를 먼저 잃는다. 3d가 채워지면 3d의 에너지가 4s보다 낮아지기 때문이다.',s:'4s 먼저'};
        for(let i=0;i<SUB.length;i++){ if(c[i]<2*SUB[i].m&&c.slice(i+1).some(v=>v>0)&&c[i]<t[i]) return {ok:false,m:`쌓음 원리 위반 — ${SUB[i].k}가 다 차지 않았는데 더 높은 오비탈에 전자가 있다(들뜬상태).`,s:'쌓음 원리'}; }
        return {ok:false,m:'바닥상태와 다르다. '+ans,s:'다름'};
      }
      let bad=false, i0=0;
      SUB.forEach((s,i)=>{ const b=st.occ.slice(i0,i0+s.m); i0+=s.m;
        const pairs=b.filter(v=>v==='ud').length, sing=b.filter(v=>v.length===1);
        if(pairs!==Math.max(0,c[i]-s.m)) bad=true;
        if(sing.length&&!sing.every(v=>v===sing[0])) bad=true; });
      if(bad) return {ok:false,m:'훈트 규칙 위반 — 에너지가 같은 오비탈에는 빈 칸부터 같은 스핀으로 하나씩 넣어 홀전자 수를 최대로 한다.',s:'훈트 규칙'};
      let extra=''; if(q===0&&(z===24||z===29)) extra=' (쌓음 순서와 다른 예외 배치)'; if(q>0&&z>=21&&z<=30) extra=' (4s 전자를 먼저 잃었다)';
      return {ok:true,m:'바닥상태 전자 배치이다 ✔'+extra,s:'바닥상태 ✔'};
    }
    function tap(k){ const cyc={'':'u','u':'d','d':'ud','ud':''}; st.occ[k]=cyc[st.occ[k]]; st.last=st.occ[k]?k:-1;
      O('msg').textContent=st.occ[k]==='ud'?'한 칸에는 스핀이 반대인 전자 2개까지만 들어간다(파울리 배타 원리).':'칸을 다시 누르면 전자의 스핀이나 개수가 바뀐다.'; draw(); }
    function add(){
      const ne=need(), c=counts(st.occ), tot=c.reduce((a,b)=>a+b,0);
      if(tot>=ne){ O('msg').textContent='필요한 전자를 모두 넣었다. 「규칙 검사」를 눌러 보자.'; return; }
      const nv=aufbau(tot+1); let i=SUB.findIndex((s,j)=>c[j]<nv[j]); if(i<0) i=SUB.findIndex((s,j)=>c[j]<2*s.m);
      let k0=off.findIndex(b=>b.i===i), m=SUB[i].m, k=-1;
      for(let j=0;j<m;j++) if(st.occ[k0+j]===''){ k=k0+j; st.occ[k]='u'; break; }
      if(k<0) for(let j=0;j<m;j++) if(st.occ[k0+j].length===1){ k=k0+j; st.occ[k]='ud'; break; }
      st.last=k; O('msg').textContent=`${SUB[i].k}에 전자를 넣었다(쌓음 순서, 훈트 규칙).`; draw();
    }
    function fill(){ st.occ=boxesFor(target(Z(),st.q)); st.last=-1; O('msg').textContent='실제 바닥상태로 채웠다.'; draw(); }
    function clear(msg){ st.occ=Array(NB).fill(''); st.last=-1; O('msg').textContent=msg||'상자를 비웠다.'; draw(); }
    I('z').addEventListener('input',()=>{ if(Z()-st.q<0||Z()-st.q>36) st.q=0; clear('새 원소 — 필요한 전자 수만큼 채워 보자.'); });
    root.querySelectorAll('[data-q]').forEach(b=>b.addEventListener('click',()=>{ const q=+b.dataset.q, ne=Z()-q;
      if(ne<0||ne>36){ O('msg').textContent='이 전하는 만들 수 없다(전자 수 0–36).'; return; } st.q=q; clear(`전하 ${q>0?'+':''}${q} — 전자 ${ne}개가 필요하다.`); }));
    $('[data-act="add"]').addEventListener('click',add);
    $('[data-act="fill"]').addEventListener('click',fill);
    $('[data-act="clear"]').addEventListener('click',()=>clear());
    $('[data-act="check"]').addEventListener('click',()=>{ const r=check(); O('msg').textContent=r.m; });
    $('[data-act="rec"]').addEventListener('click',()=>{ const c=counts(st.occ), r=check();
      log.push([API.tex(label()),API.tex(abbr(c)),unpaired(st.occ),valence(c),r.s]); if(log.length>5) log.shift();
      O('log').innerHTML=log.map(x=>'<tr>'+x.map(v=>`<td>${v}</td>`).join('')+'</tr>').join(''); O('msg').textContent=`기록했다 (${log.length}행).`; });
    $('[data-act="reset"]').addEventListener('click',()=>{ I('z').value=6; st.q=0; log=[]; O('log').innerHTML=''; clear('초기화했다. 탄소부터 채워 보자.'); });
    clear('원소를 고르고 전자를 채워 보자. 「전자 1개 넣기」는 쌓음 순서를 따른다.');
    API.onShow&&API.onShow(draw);
  }
};
})();
