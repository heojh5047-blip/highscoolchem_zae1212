/* ════════════════ SLIDE HARNESS ENGINE ════════════════ */
(function(){
'use strict';
const W=1280,H=720;
const deck=document.getElementById('deck');
const slides=[...deck.querySelectorAll(':scope > section.slide')];
const N=slides.length;
// 편집 모드(편집기 iframe 안, window.__EDIT_MODE): 부품 그리기·KaTeX 전에 원문 그대로의 요소에 번호를 붙인다.
// 규칙: 슬라이드 i(1부터) 자신 data-eid="i-0", 그 안의 모든 요소를 문서 순서로 "i-1", "i-2", … — 편집기는 같은 원문을 DOMParser로 읽어 같은 규칙으로 대응시킨다.
const EDIT=!!window.__EDIT_MODE;
function editPost(m){ try{ if(window.parent!==window) window.parent.postMessage(m,'*'); }catch(e){} }
if(EDIT) slides.forEach((s,i)=>{ s.setAttribute('data-eid',(i+1)+'-0'); s.querySelectorAll('*').forEach((e,k)=>e.setAttribute('data-eid',(i+1)+'-'+(k+1))); });
const SVGNS='http://www.w3.org/2000/svg', XHTML='http://www.w3.org/1999/xhtml';
const COL=window.HARNESS_COL||{ink:'#16233D',plus:'#D7263D',minus:'#1F6FD1',field:'#2E9E6A',equi:'#E08A2C',grav:'#8C99A6',muted:'#5B6B7F',white:'#FFFFFF',bfield:'#7B4FC8',ox:'#C2410C',rd:'#0E7490'};   // 색 표는 harness-ui.html(HARNESS_COL)
const colOf=v=>(v!=null&&COL[String(v).trim()])||v;                       // 'bfield' 같은 이름 → hex (hex는 그대로)
const params=new URLSearchParams(location.search);
const hud=document.getElementById('hud');
let cur=0, scale=1;
const shown=new Array(N).fill(0);
const showHooks=[];

/* ─────────── 1. CORE ─────────── */
function fit(){ scale=Math.min(innerWidth/W,innerHeight/H); deck.style.transform=`translate(-50%,-50%) scale(${scale})`; }
function groups(s){
  if(s._g) return s._g;
  const g=[],m=new Map();
  s.querySelectorAll('.step').forEach(e=>{ const k=e.dataset.g; if(k){ if(m.has(k)){ m.get(k).push(e); return; } const a=[e]; m.set(k,a); g.push(a); } else g.push([e]); });
  return (s._g=g);
}
function paint(i){ groups(slides[i]).forEach((a,k)=>a.forEach(e=>{ const was=e.classList.contains('on'), on=k<shown[i]; e.classList.toggle('on',on); if(on&&!was&&window.__fxReveal) window.__fxReveal(e); })); }
function show(i,mode){
  i=Math.max(0,Math.min(N-1,i|0));
  slides[cur].classList.remove('active');
  cur=i; const s=slides[i];
  if(mode==='all') shown[i]=groups(s).length; else if(mode==='reset') shown[i]=0;
  groups(s).forEach(a=>{ a._asked=false; a._asking=false; }); s.querySelectorAll('.ask').forEach(x=>x.classList.remove('ask'));
  s.classList.add('active'); paint(i);
  hud.style.width=((i+1)/N*100)+'%';
  try{ history.replaceState(null,'','#'+(i+1)); }catch(e){}
  redrawInk(); tocMark(); showHooks.forEach(f=>f(s,i));
}
function next(){ const g=groups(slides[cur]); if(shown[cur]<g.length){ const a=g[shown[cur]]; if(!a._asked&&askable(a)){ a._asked=true; askOn(a,true); return; } askOn(a,false); shown[cur]++; paint(cur); } else if(cur<N-1) show(cur+1,'reset'); }
function prev(){ const g=groups(slides[cur]), a=g[shown[cur]]; if(a&&a._asking){ askOn(a,false); a._asked=false; return; } if(shown[cur]>0){ shown[cur]--; paint(cur); const b=g[shown[cur]]; if(b) b._asked=false; } else if(cur>0) show(cur-1,'all'); }

// 머리띠(단원 · 쪽 번호)
slides.forEach((s,i)=>{ const b=document.createElement('div'); b.className='band'; const a=document.createElement('span'); a.className='sec'; a.textContent=s.dataset.sec||''; const p=document.createElement('span'); p.className='pg'; p.textContent=(i+1)+' / '+N; b.append(a,p); s.prepend(b); });

// 목차
const tocList=document.querySelector('#toc ol');
slides.forEach((s,i)=>{ const li=document.createElement('li'); const n=document.createElement('span'); n.className='n'; n.textContent=i+1; const t=document.createElement('span'); t.textContent=s.dataset.title||((s.querySelector('h2,h1')||{}).textContent||'').trim(); li.append(n,t); li.addEventListener('click',()=>{ closeOverlays(); show(i,'reset'); }); tocList.appendChild(li); });
function tocMark(){ [...tocList.children].forEach((li,i)=>li.classList.toggle('cur',i===cur)); }
function toggle(id){ const o=document.getElementById(id); const open=!o.classList.contains('open'); closeOverlays(); if(open) o.classList.add('open'); }
function closeOverlays(){ document.querySelectorAll('.ui-overlay.open').forEach(o=>o.classList.remove('open')); }
document.querySelectorAll('.ui-overlay').forEach(o=>o.addEventListener('click',e=>{ if(e.target===o) closeOverlays(); }));

function fullscreen(){ if(!document.fullscreenElement){ const r=document.documentElement.requestFullscreen; if(r) r.call(document.documentElement).catch(()=>{}); } else if(document.exitFullscreen) document.exitFullscreen(); }

// 키보드
document.addEventListener('keydown',e=>{
  if(EDIT) return;   // 편집 모드: 넘기기는 편집기가 Harness.show로
  const t=e.target, k=e.key;
  if(t.matches && t.matches('input[type=range]') && /^Arrow/.test(k)) return;
  if(t.matches && t.matches('input:not([type=range]),textarea,select')) return;
  if(t.closest && t.closest('button') && (k===' '||k==='Enter')) return;
  if(e.ctrlKey||e.metaKey||e.altKey) return;
  if(k==='Escape'){ closeOverlays(); setPen(false); document.body.classList.remove('black'); return; }
  switch(k){
    case 'ArrowRight': case 'ArrowDown': case 'PageDown': case ' ': case 'Enter': e.preventDefault(); next(); break;
    case 'ArrowLeft': case 'ArrowUp': case 'PageUp': case 'Backspace': e.preventDefault(); prev(); break;
    case 'Home': show(0,'reset'); break;
    case 'End': show(N-1,'all'); break;
    case 'o': case 'O': toggle('toc'); break;
    case 'f': case 'F': fullscreen(); break;
    case 'p': case 'P': setPen(!penOn); break;
    case 'x': case 'X': clearInk(); break;
    case 'b': case 'B': document.body.classList.toggle('black'); break;
    case 'd': case 'D': runAudit(true); break;
    case 'h': case 'H': case '?': toggle('help'); break;
  }
});

// 클릭 · 밀기 (가이드 6.1): 넘기기는 click이 아니라 pointerdown → pointerup 으로 판단한다.
//   넘기지 않는 경우: 6px(터치 10px) 넘게 움직임 · 500ms 넘게 누름 · 글자가 선택됨 · 펜 입력 · 조작 요소(INTERACTIVE) 위
//   스와이프(옆으로 60px 넘게)는 터치에만. click 넘기기는 없앴다(한 번 눌러 두 번 넘어가지 않게).
const viewport=document.getElementById('viewport');
const INTERACTIVE='a,button,input,select,textarea,label,output,svg,canvas,img,.lab,.chk';
const CHROME='#nav,#penbar,#hud,.ui-overlay,a,button,input,select,textarea,label';   // 펜으로도 눌러 쓰는 화면 조작부
const PEN_MOUSE=params.get('pen')==='mouse';                                          // 개발용: 마우스를 펜처럼(?pen=mouse)
const isPen=e=>e.pointerType==='pen'||(PEN_MOUSE&&e.pointerType==='mouse');
let tap=null, penDown=0;
viewport.addEventListener('pointerdown',e=>{
  if(EDIT||isPen(e)||(e.pointerType==='touch'&&penDown)) return;
  if(e.pointerType==='mouse'&&e.button!==0) return;
  tap={id:e.pointerId,type:e.pointerType,x:e.clientX,y:e.clientY,t:performance.now(),target:e.target,far:0};
});
viewport.addEventListener('pointermove',e=>{ if(tap&&e.pointerId===tap.id) tap.far=Math.max(tap.far,Math.hypot(e.clientX-tap.x,e.clientY-tap.y)); });
viewport.addEventListener('pointercancel',e=>{ if(tap&&e.pointerId===tap.id) tap=null; });
viewport.addEventListener('pointerup',e=>{
  if(!tap||e.pointerId!==tap.id) return; const t=tap; tap=null;
  if(EDIT||penOn||(t.type==='touch'&&penDown)) return;
  const dx=e.clientX-t.x, dy=e.clientY-t.y, dt=performance.now()-t.t;
  if(t.type==='touch'&&Math.abs(dx)>60&&Math.abs(dx)>1.5*Math.abs(dy)&&!(t.target.closest&&t.target.closest('input,.lab,svg,canvas'))){ if(dx<0) next(); else prev(); return; }
  if(Math.max(t.far,Math.hypot(dx,dy))>(t.type==='touch'?10:6)||dt>500) return;
  const sel=window.getSelection&&getSelection(); if(sel&&!sel.isCollapsed&&String(sel).trim()) return;
  if(t.target.closest&&t.target.closest(INTERACTIVE)){ const fig=t.target.closest('svg'); if(fig&&!fig.closest('.lab')&&window.__replayFig){ const top=fig.ownerSVGElement||fig; window.__replayFig(top); } return; }
  next();
});
document.addEventListener('click',e=>{ const c=e.target.closest('.chk'); if(c) c.classList.toggle('on'); const b=e.target.closest('button'); if(b) setTimeout(()=>b.blur(),0); });
deck.addEventListener('contextmenu',e=>e.preventDefault());   // 무대에서 길게 누름·펜 옆 단추로 메뉴가 뜨지 않게
let uiT; addEventListener('mousemove',()=>{ document.body.classList.add('ui'); clearTimeout(uiT); uiT=setTimeout(()=>document.body.classList.remove('ui'),2500); });

document.getElementById('nav').addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; const a=b.dataset.a; if(a==='prev') prev(); else if(a==='next') next(); else if(a==='toc') toggle('toc'); else if(a==='pen') setPen(!penOn); else if(a==='fs') fullscreen(); else if(a==='help') toggle('help'); });

// 판서 펜 (가이드 6.2): 펜(pointerType 'pen')은 P 키 없이 바로 쓴다. 마우스·터치는 P(펜 켜기)일 때만.
//   압력 → 굵기, 펜 지우개 끝(buttons & 32) → 지우개, 펜이 닿아 있는 동안 터치 무시, getCoalescedEvents로 촘촘하게.
//   획은 무대 좌표(1280×720)로 저장하므로 창 크기·확대와 무관하다.
const ink=document.getElementById('ink'), ictx=ink.getContext('2d'), DPR=2;
ink.width=W*DPR; ink.height=H*DPR; ictx.setTransform(DPR,0,0,DPR,0,0);
let penOn=false, penColor=COL.plus, drawing=null, drawId=null;
const strokes=slides.map(()=>[]);
function setPen(v){ penOn=!!v; document.body.classList.toggle('pen',penOn); }
function pt(e){ const r=deck.getBoundingClientRect(), pr=e.pointerType==='mouse'||!e.pressure?.5:e.pressure; return [(e.clientX-r.left)*W/r.width,(e.clientY-r.top)*H/r.height,pr]; }
const widthOf=(s,p)=>s.c==='erase'?30:4*(0.45+1.1*(p[2]==null?.5:p[2]));   // 압력 0.5 ≈ 4px
function penStyle(s){ if(s.c==='erase'){ ictx.globalCompositeOperation='destination-out'; } else { ictx.globalCompositeOperation='source-over'; ictx.strokeStyle=s.c; } ictx.lineCap='round'; ictx.lineJoin='round'; }
function seg(s,a,b){ ictx.lineWidth=widthOf(s,b); ictx.beginPath(); ictx.moveTo(a[0],a[1]); ictx.lineTo(b[0]+(a===b?.01:0),b[1]); ictx.stroke(); }
function drawStroke(s){ penStyle(s); const p=s.p; seg(s,p[0],p[0]); for(let i=1;i<p.length;i++) seg(s,p[i-1],p[i]); ictx.globalCompositeOperation='source-over'; }
function redrawInk(){ ictx.globalCompositeOperation='source-over'; ictx.clearRect(0,0,W,H); strokes[cur].forEach(drawStroke); ictx.globalCompositeOperation='source-over'; }
function clearInk(){ strokes[cur]=[]; redrawInk(); }
function endStroke(e){ if(drawId!==e.pointerId) return; if(isPen(e)) penDown=Math.max(0,penDown-1); drawing=null; drawId=null; ictx.globalCompositeOperation='source-over'; }
// 캡처 단계에서 먼저 받는다: 펜은 슬라이드 요소(그림·실험실) 위에서도 바로 필기
viewport.addEventListener('pointerdown',e=>{
  if(EDIT) return;
  if(e.pointerType==='touch'&&penDown){ e.preventDefault(); e.stopPropagation(); return; }   // 손바닥 무시
  const pen=isPen(e);
  if(!pen&&!(penOn&&e.target===ink)) return;
  if(e.target.closest&&e.target.closest(CHROME)) return;                                    // 단추·슬라이더는 펜으로도 누른다
  if(!deck.contains(e.target)) return;
  e.preventDefault(); e.stopPropagation();
  if(pen) penDown++;
  try{ viewport.setPointerCapture(e.pointerId); }catch(_){}   // 이미 끝난 포인터 등
  const erase=(e.buttons&32)||penColor==='erase';
  drawing={c:erase?'erase':penColor,p:[pt(e)]}; drawId=e.pointerId; strokes[cur].push(drawing); drawStroke(drawing);
},true);
viewport.addEventListener('pointermove',e=>{
  if(e.pointerType==='touch'&&penDown&&drawId!==e.pointerId){ e.stopPropagation(); return; }
  if(!drawing||e.pointerId!==drawId) return;
  e.preventDefault();
  const evs=e.getCoalescedEvents?e.getCoalescedEvents():[e];
  penStyle(drawing);
  (evs.length?evs:[e]).forEach(ev=>{ const p=pt(ev), l=drawing.p[drawing.p.length-1]; drawing.p.push(p); seg(drawing,l,p); });
  ictx.globalCompositeOperation='source-over';
},true);
['pointerup','pointercancel','lostpointercapture'].forEach(ev=>viewport.addEventListener(ev,endStroke,true));
document.getElementById('penbar').addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; if(b.dataset.c){ penColor=b.dataset.c; document.querySelectorAll('#penbar [data-c]').forEach(x=>x.classList.toggle('on',x===b)); } else if(b.dataset.a==='clear') clearInk(); else if(b.dataset.a==='penoff') setPen(false); });

addEventListener('resize',fit);
fit();
const h0=parseInt(location.hash.slice(1),10);
show(isNaN(h0)?0:h0-1,'reset');

/* ─────────── 2. COMPONENTS ─────────── */
function mk(tag,attrs,parent){ const e=document.createElementNS(SVGNS,tag); for(const k in attrs) e.setAttribute(k,/^(fill|stroke|stop-color|color)$/.test(k)?colOf(attrs[k]):attrs[k]); if(parent) parent.appendChild(e); return e; }
function head(g,x,y,ux,uy,hs,color){ const L=hs*1.6, Wd=hs*.78, bx=x-ux*L, by=y-uy*L, px=-uy, py=ux; return mk('polygon',{points:`${(x).toFixed(1)},${(y).toFixed(1)} ${(bx+px*Wd).toFixed(1)},${(by+py*Wd).toFixed(1)} ${(bx-px*Wd).toFixed(1)},${(by-py*Wd).toFixed(1)}`,fill:color},g); }
function arrow(g,x1,y1,x2,y2,color,w,dash){ w=w||3; const dx=x2-x1, dy=y2-y1, len=Math.hypot(dx,dy)||1, ux=dx/len, uy=dy/len, hs=3+w*1.6, cut=hs*1.6*.8; const a={x1,y1,x2:x2-ux*cut,y2:y2-uy*cut,stroke:color,'stroke-width':w,'stroke-linecap':dash?'butt':'round'}; if(dash) a['stroke-dasharray']='7 5'; mk('line',a,g).classList.add('arw-l'); head(g,x2,y2,ux,uy,hs,color).classList.add('arw-h'); }
const CH={'+':[COL.plus,'#A51B2E'],'-':[COL.minus,'#16539E'],P:[COL.plus,'#A51B2E'],M:[COL.minus,'#16539E'],N:['#A7B3BF','#7E8B98']};
function charge(g,x,y,r,sign,dashed){
  const [f,s]=CH[sign]||CH.N;
  const c=mk('circle',{cx:x,cy:y,r,fill:f,stroke:s,'stroke-width':Math.max(1.5,r*.07)},g);
  if(dashed){ c.setAttribute('fill-opacity','.22'); c.setAttribute('stroke-dasharray','5 4'); }
  else if(sign==='+'||sign==='-') mk('circle',{cx:x-r*.32,cy:y-r*.36,r:r*.3,fill:'#fff','fill-opacity':.25},g);   // P·M·N은 라벨이 들어가므로 광택 생략
  const a=r*.48, t=Math.max(2.4,r*.14), sc=dashed?s:'#fff';
  if(sign==='+'||sign==='-') mk('rect',{x:x-a,y:y-t/2,width:2*a,height:t,rx:t/3,fill:sc},g);
  if(sign==='+') mk('rect',{x:x-t/2,y:y-a,width:t,height:2*a,rx:t/3,fill:sc},g);
}
// 원자 모형 (화학, 가이드 5.0·D21): <g data-atom="x,y,r,원소[,라벨|-][,d]"> — 원소별 고정 색(HARNESS_ATOM), 원소 기호 LaTeX 라벨
//  라벨 생략 시 원소 기호(\mathrm{O}), "-"면 라벨 없음, 그 밖의 값은 LaTeX(예: \mathrm{O}^{\delta-}). d면 점선(이전 위치·빈자리)
const ATOM=Object.assign({H:['#F4F6F8','#8C99A6'],C:['#3A3F47','#1C1F24'],N:['#4F6BD8','#2F4AA8'],O:['#E5533D','#A8321F'],F:['#9BD86F','#5E9B37'],Cl:['#4CAF50','#2E7D32'],Br:['#A5452B','#6E2A18'],I:['#7E3FA3','#552870'],S:['#E8C547','#A88A1E'],P:['#F09A3E','#B0661A'],Na:['#8E5BD0','#5E3A96'],K:['#A06CD5','#6C4596'],Li:['#C08BE6','#8456A8'],Mg:['#3FA36B','#256B44'],Ca:['#7FA08C','#4E6B5A'],Al:['#B9A8A0','#7D6E66'],Be:['#B8A9D9','#7B6BA6'],B:['#E7A15E','#A86A2C'],Si:['#C9B48A','#8E7A52'],Fe:['#C7743D','#874A20'],Cu:['#C8803A','#8A5221'],Zn:['#8FA3B8','#5C6F82'],Ag:['#C9CED6','#8A919C'],He:['#D9F2F2','#7FB3B3'],Ne:['#C7E3F7','#6F9FC4'],Ar:['#BFD9E6','#6E95A8'],X:['#C9D3DD','#7E8B98']},window.HARNESS_ATOM||{});
function atom(g,x,y,r,el,label,dashed){
  const [f,s]=ATOM[el]||ATOM.X;
  const c=mk('circle',{cx:x,cy:y,r,fill:f,stroke:s,'stroke-width':Math.max(1.2,r*.06)},g);
  if(dashed){ c.setAttribute('fill-opacity','.25'); c.setAttribute('stroke-dasharray','5 4'); }
  else mk('ellipse',{cx:x-r*.33,cy:y-r*.38,rx:r*.34,ry:r*.24,fill:'#fff','fill-opacity':.32},g);
  if(label==='-') return c;
  const hex=f.replace('#',''), lum=(0.299*parseInt(hex.substr(0,2),16)+0.587*parseInt(hex.substr(2,2),16)+0.114*parseInt(hex.substr(4,2),16))/255;
  const size=Math.round(Math.min(r*(label?0.7:el&&el.length>1?0.78:0.92),36));
  texText(g,x,y+size*.36,label||('\\mathrm{'+el+'}'),{size,anchor:'middle',fill:dashed?COL.muted:lum<.55?'#FFFFFF':COL.ink,weight:700});
  return c;
}
function vfield(g,c){ const color=COL[c.color]||c.color||COL.field, w=c.w||2.6; c.rings.forEach(([r,L,n,rot])=>{ for(let j=0;j<n;j++){ const a=2*Math.PI*j/n+(rot||0)*Math.PI/180, ux=Math.cos(a), uy=Math.sin(a); if(c.s>0) arrow(g,c.x+ux*r,c.y+uy*r,c.x+ux*(r+L),c.y+uy*(r+L),color,w); else arrow(g,c.x+ux*(r+L),c.y+uy*(r+L),c.x+ux*r,c.y+uy*r,color,w); } }); }

// 전기력선 (5.3: (+)는 앞으로, (−)는 뒤로 추적 → 대칭 보장)
function fieldAt(ch,x,y){ let ex=0,ey=0; for(const c of ch){ const dx=x-c.x, dy=y-c.y, r2=dx*dx+dy*dy, r=Math.sqrt(r2), f=c.q/(r2*r); ex+=f*dx; ey+=f*dy; } return [ex,ey]; }
function trace(ch,x,y,dir,B,hR,self){
  const pts=[[x,y]]; let pdx=0,pdy=0,end={type:'out'};
  for(let k=0;k<8000;k++){
    let dmin=1e9,imin=-1; for(let i=0;i<ch.length;i++){ const d=Math.hypot(x-ch[i].x,y-ch[i].y); if(d<dmin){ dmin=d; imin=i; } }
    if(imin!==self && dmin<hR){ end={type:'hit',idx:imin}; pts.push([ch[imin].x,ch[imin].y]); break; }
    if(x<B.x0||x>B.x1||y<B.y0||y>B.y1) break;
    const ds=Math.min(10,Math.max(.8,dmin*.06));
    let [ax,ay]=fieldAt(ch,x,y), m=Math.hypot(ax,ay); if(!m){ end={type:'stall'}; break; } ax=ax/m*dir; ay=ay/m*dir;
    let [bx,by]=fieldAt(ch,x+ax*ds*.5,y+ay*ds*.5); m=Math.hypot(bx,by); if(!m){ end={type:'stall'}; break; } bx=bx/m*dir; by=by/m*dir;
    if(k>0 && bx*pdx+by*pdy<-.3){ end={type:'stall'}; break; }
    x+=bx*ds; y+=by*ds; pdx=bx; pdy=by; pts.push([x,y]);
  }
  return {pts,end};
}
function fieldLines(svg,cfg){
  const vb=svg.viewBox.baseVal, ch=cfg.charges, per=cfg.perUnit||16, sR=cfg.startR||30, hR=cfg.hitR||28, M=200;
  const B={x0:vb.x-M,y0:vb.y-M,x1:vb.x+vb.width+M,y1:vb.y+vb.height+M};
  const lines=[];
  ch.forEach((c,ci)=>{ const n=Math.round(per*Math.abs(c.q)), dir=c.q>0?1:-1;
    for(let j=0;j<n;j++){ const th=2*Math.PI*j/n+Math.PI/n; const tr=trace(ch,c.x+sR*Math.cos(th),c.y+sR*Math.sin(th),dir,B,hR,ci);
      if(dir<0 && tr.end.type==='hit' && ch[tr.end.idx].q>0) continue;   // 이미 (+)에서 그린 선
      tr.pts.unshift([c.x,c.y]); lines.push(tr); } });
  const g=mk('g',{class:'fieldlines'}); svg.insertBefore(g,svg.firstChild);
  const FC=COL[cfg.color]||cfg.color||COL.field;   // 선 색(기본 전기장 초록, 자기력선은 "color":"#7B4FC8" 등)
  lines.forEach(L=>mk('path',{d:'M'+L.pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L'),fill:'none',stroke:FC,'stroke-width':cfg.w||2.2,'stroke-linejoin':'round'},g));
  lines.forEach(L=>{
    const cum=[0]; for(let i=1;i<L.pts.length;i++) cum.push(cum[i-1]+Math.hypot(L.pts[i][0]-L.pts[i-1][0],L.pts[i][1]-L.pts[i-1][1]));
    const tot=cum[cum.length-1];
    const at=L.end.type==='hit' ? (tot<260?[tot/2]:[60,tot-60]) : [60];
    at.forEach(s=>{ let i=1; while(i<cum.length-1 && cum[i]<s) i++; const f=(s-cum[i-1])/((cum[i]-cum[i-1])||1); const x=L.pts[i-1][0]+(L.pts[i][0]-L.pts[i-1][0])*f, y=L.pts[i-1][1]+(L.pts[i][1]-L.pts[i-1][1])*f;
      if(x<vb.x+8||x>vb.x+vb.width-8||y<vb.y+8||y>vb.y+vb.height-8) return;
      let [ex,ey]=fieldAt(ch,x,y); const m=Math.hypot(ex,ey); if(!m) return; ex/=m; ey/=m; head(g,x+ex*7,y+ey*7,ex,ey,7,FC); });
  });
  if(cfg.draw){ const cg=mk('g',{},svg); ch.forEach(c=>charge(cg,c.x,c.y,cfg.r||22,c.q>0?'+':'-')); }
  return g;   // 실험실에서 다시 그릴 때 g.remove() 후 API.fieldLines(svg,cfg)
}

// SVG 속 LaTeX 라벨을 만드는 도우미 (texSVG 단계에서 foreignObject + KaTeX로 바뀜)
function texText(parent,x,y,tex,o){
  o=o||{};
  const t=mk('text',{class:'tex',x:(+x).toFixed(1),y:(+y).toFixed(1),'data-size':o.size||22,'data-anchor':o.anchor||'start'},parent);
  t.setAttribute(o.mix?'data-mix':'data-tex',tex);
  if(o.fill) t.setAttribute('fill',COL[o.fill]||o.fill);
  if(o.weight) t.setAttribute('data-weight',o.weight);
  if(o.halo) t.setAttribute('data-halo','1');
  return t;
}

// 회로도 (5.2): <svg viewBox data-circuit='{"parts":[…],"stroke":3}'>
//  ["wire",[[x,y],…]]                      꺾은선
//  ["R",[x1,y1],[x2,y2],"R_1",{side,L,A,peaks,color,labelColor,size}]   지그재그 저항. 라벨: 가로면 위, 세로면 왼쪽 (D1)
//  ["C",[x1,y1],[x2,y2],"C",{side,gap,plate,…}]                        축전기(평행한 두 판). 라벨 규칙은 R과 같음
//  ["bat",[x,y],{"dir":"h"|"v","pos":"right"|"left"|"up"|"down","label":"V","signs":true,"signSize":14}]
//        긴 판(+)이 pos 쪽. 라벨은 항상 오른쪽 아래 (D1). 도선은 x±8(가로) 또는 y±8(세로)까지 그린다
//  ["node",[x,y]]  접합점 ●      ["term",[x,y],"a",{"side":"left"}]  단자 ○ + 라벨
//  ["sw",[x1,y1],[x2,y2],true|false]  스위치(닫힘/열림)
//  ["bulb",[x,y],{"r":14,"on":true,"label":"L_1"}]  전구 기호 ⊗ (도선은 x±r 또는 y±r까지)
//  ["meter",[x,y],"A"|"V"|"G",{"r":16}]  전류계·전압계·검류계 (도선은 원 둘레까지)
//  ["ac",[x,y],{"r":18,"label":"V"}]  교류 전원 ○ 안에 사인 곡선 (도선은 원 둘레까지). 라벨은 오른쪽 아래 (D1)
//  ["L",[x1,y1],[x2,y2],"L",{loops:4,side,color,…}]  코일(인덕터): 반원 고리. 라벨 규칙은 R과 같음(가로면 위, 세로면 왼쪽)
//  ["D",[x1,y1],[x2,y2],"D",{led:true,fill:true}]  다이오드: p1 = (+)쪽(애노드) → p2 = 막대 쪽(캐소드). led면 빛 화살표 2개. 라벨 규칙은 R과 같음
//  ["npn",[x,y],{"r":26,"type":"npn"|"pnp","labels":true}]  트랜지스터(베이스 왼쪽, 컬렉터 위, 이미터 아래).
//        단자: B (x−r−18, y), C (x+0.45r, y−r−18), E (x+0.45r, y+r+18) — 도선을 이 점까지 잇는다
//  ["arrow",[x1,y1],[x2,y2],{"color":"plus","w":3,"label":"I","lx":…,"ly":…}]  전류 등 화살표
//  ["label",[x,y],"I",{size,anchor,fill,mix,weight,halo}]  임의 LaTeX(mix:true면 글+$수식$)
function renderCircuit(svg,cfg){
  const sw=cfg.stroke||3, ink=COL[cfg.color]||cfg.color||COL.ink, LS=cfg.labelSize||22;
  const g=mk('g',{class:'circuit',fill:'none',stroke:ink,'stroke-width':sw,'stroke-linecap':'round','stroke-linejoin':'round'});
  svg.insertBefore(g,svg.firstChild);
  const line=(x1,y1,x2,y2,w,col)=>mk('line',{x1:(+x1).toFixed(1),y1:(+y1).toFixed(1),x2:(+x2).toFixed(1),y2:(+y2).toFixed(1),'stroke-width':w||sw,stroke:col||ink},g);
  const lab=(x,y,t,o,anchor)=>texText(svg,x,y,t,{size:o.size||LS,anchor,fill:o.labelColor});
  (cfg.parts||[]).forEach(p=>{ try{
    const kind=p[0];
    if(kind==='wire'){ mk('path',{d:'M'+p[1].map(q=>q[0]+' '+q[1]).join(' L')},g); }
    else if(kind==='R'||kind==='C'||kind==='L'||kind==='D'){
      const [x1,y1]=p[1],[x2,y2]=p[2],t=p[3],o=p[4]||{};
      const dx=x2-x1,dy=y2-y1,len=Math.hypot(dx,dy)||1,ux=dx/len,uy=dy/len,nx=-uy,ny=ux,mx=(x1+x2)/2,my=(y1+y2)/2,horiz=Math.abs(dx)>=Math.abs(dy);
      const col=COL[o.color]||o.color||ink; let ext;
      if(kind==='R'){
        const L=o.L||Math.min(64,len*.62), A=o.A||9, n=o.peaks||6, s0=len/2-L/2;
        let d=`M${x1} ${y1} L${(x1+ux*s0).toFixed(1)} ${(y1+uy*s0).toFixed(1)}`;
        for(let i=0;i<n;i++){ const s=s0+L*(i+.5)/n, a=(i%2?-A:A); d+=` L${(x1+ux*s+nx*a).toFixed(1)} ${(y1+uy*s+ny*a).toFixed(1)}`; }
        d+=` L${(x1+ux*(s0+L)).toFixed(1)} ${(y1+uy*(s0+L)).toFixed(1)} L${x2} ${y2}`;
        mk('path',{d,stroke:col},g); ext=A;
      } else if(kind==='L'){   // 코일: 바깥쪽(nx,ny 반대쪽)으로 볼록한 반원 n개
        const n=o.loops||4, L=o.L||Math.min(n*18,len*.7), s0=len/2-L/2, rr=L/n/2, side=o.bulge==='in'?1:-1;
        let d=`M${x1} ${y1} L${(x1+ux*s0).toFixed(1)} ${(y1+uy*s0).toFixed(1)}`;
        for(let i=0;i<n;i++){ const s=s0+L*(i+1)/n; d+=` A${rr.toFixed(1)} ${rr.toFixed(1)} 0 0 ${side>0?0:1} ${(x1+ux*s).toFixed(1)} ${(y1+uy*s).toFixed(1)}`; }
        d+=` L${x2} ${y2}`;
        mk('path',{d,stroke:col},g); ext=rr+2;
      } else if(kind==='D'){   // 다이오드: 삼각형(애노드→캐소드 방향) + 캐소드 막대
        const T=o.T||24, H=o.H||14, bxs=len/2-T/2, txs=len/2+T/2, P=(s,k)=>[(x1+ux*s+nx*k).toFixed(1),(y1+uy*s+ny*k).toFixed(1)].join(',');
        line(x1,y1,x1+ux*bxs,y1+uy*bxs); line(x1+ux*txs,y1+uy*txs,x2,y2);
        mk('polygon',{points:[P(bxs,H),P(bxs,-H),P(txs,0)].join(' '),fill:o.fill===false?'#fff':col,stroke:col},g);
        line(x1+ux*txs+nx*H,y1+uy*txs+ny*H,x1+ux*txs-nx*H,y1+uy*txs-ny*H,sw,col);
        if(o.led){ const ag=mk('g',{},svg), sgn=o.ledSide==='in'?1:-1;   // 빛 화살표: 막대 반대쪽(바깥)으로 비스듬히
          [-6,8].forEach(dd=>{ const sx=x1+ux*(len/2+dd)+nx*sgn*(H+3), sy=y1+uy*(len/2+dd)+ny*sgn*(H+3), vx=(ux+nx*sgn)*.7071, vy=(uy+ny*sgn)*.7071; arrow(ag,sx,sy,sx+vx*26,sy+vy*26,COL[o.ledColor]||o.ledColor||'#E08A2C',2.6); }); }
        ext=H+(o.led?26:0);
      } else {
        const gap=o.gap||12, hp=o.plate||18, s1=len/2-gap/2, s2=len/2+gap/2;
        line(x1,y1,x1+ux*s1,y1+uy*s1); line(x1+ux*s2,y1+uy*s2,x2,y2);
        [s1,s2].forEach(s=>{ const cx=x1+ux*s, cy=y1+uy*s; line(cx+nx*hp,cy+ny*hp,cx-nx*hp,cy-ny*hp,sw*1.3,col); });
        ext=hp;
      }
      if(t!=null && t!==''){
        const side=o.side||(horiz?'above':'left'), s=o.size||LS, gp=8;
        if(side==='above') lab(mx,my-ext-gp,t,o,'middle');
        else if(side==='below') lab(mx,my+ext+gp+s*.85,t,o,'middle');
        else if(side==='left') lab(mx-ext-gp-2,my+s*.35,t,o,'end');
        else lab(mx+ext+gp+2,my+s*.35,t,o,'start');
      }
    }
    else if(kind==='bat'){
      const [x,y]=p[1], o=p[2]||{}, v=(o.dir||'h')==='v', pos=o.pos||(v?'up':'right'), LL=o.long||20, SS=o.short||11, col=COL[o.color]||o.color||ink;
      let lx,ly;
      if(!v){ lx=pos==='left'?x-8:x+8; const sx=pos==='left'?x+8:x-8; line(lx,y-LL,lx,y+LL,sw,col); line(sx,y-SS,sx,y+SS,sw*2,col); }
      else { ly=pos==='down'?y+8:y-8; const sy=pos==='down'?y-8:y+8; line(x-LL,ly,x+LL,ly,sw,col); line(x-SS,sy,x+SS,sy,sw*2,col); }
      if(o.signs){   // 극 표시: 글꼴 대신 굵은 선(축전기 패널과 같은 방식). 크기 o.signSize(기본 14)
        const S=(o.signSize||14)/2, plus=(cx,cy)=>{ line(cx-S,cy,cx+S,cy,3,COL.plus); line(cx,cy-S,cx,cy+S,3,COL.plus); }, minus=(cx,cy)=>line(cx-S,cy,cx+S,cy,3,COL.minus);
        if(!v){ const sx=pos==='left'?x+8:x-8, d=pos==='left'?-1:1; plus(lx+d*(8+S),y-LL+S); minus(sx-d*(8+S),y-LL+S); }
        else { const sy=pos==='down'?y-8:y+8; plus(x-LL-8-S,ly); minus(x-SS-8-S,sy); }
      }
      if(o.label!=null && o.label!==''){ const s=o.size||LS; if(!v) lab(x+12,y+LL+s*.95,o.label,o,'start'); else lab(x+LL+8,y+8+s*.95,o.label,o,'start'); }
    }
    else if(kind==='node'){ const [x,y]=p[1]; mk('circle',{cx:x,cy:y,r:(p[2]&&p[2].r)||5,fill:ink,stroke:'none'},g); }
    else if(kind==='term'){
      const [x,y]=p[1], t=p[2], o=p[3]||{}, s=o.size||LS, side=o.side||'left';
      mk('circle',{cx:x,cy:y,r:6,fill:'#fff'},g);
      if(t){ if(side==='left') lab(x-12,y+s*.35,t,o,'end'); else if(side==='right') lab(x+12,y+s*.35,t,o,'start'); else if(side==='top'||side==='above') lab(x,y-12,t,o,'middle'); else lab(x,y+12+s*.8,t,o,'middle'); }
    }
    else if(kind==='sw'){
      const [x1,y1]=p[1],[x2,y2]=p[2], closed=!!p[3], o=p[4]||{}, dx=x2-x1, dy=y2-y1, len=Math.hypot(dx,dy);
      let ex=x2, ey=y2;
      if(!closed){ const a=Math.atan2(dy,dx)-(o.angle||30)*Math.PI/180; ex=x1+Math.cos(a)*len; ey=y1+Math.sin(a)*len; }
      line(x1,y1,ex,ey);
      [[x1,y1],[x2,y2]].forEach(q=>mk('circle',{cx:q[0],cy:q[1],r:4,fill:'#fff'},g));
    }
    else if(kind==='bulb'){
      const [x,y]=p[1], o=p[2]||{}, r=o.r||14, k=r*.7071;
      if(o.on) mk('circle',{cx:x,cy:y,r:r*1.9,fill:'#FFE45C',opacity:.6,stroke:'none'},g);
      mk('circle',{cx:x,cy:y,r,fill:'#fff'},g); line(x-k,y-k,x+k,y+k,sw*.8); line(x-k,y+k,x+k,y-k,sw*.8);
      if(o.label) lab(x,y-r*(o.on?1.9:1)-6,o.label,o,'middle');
    }
    else if(kind==='meter'){
      const [x,y]=p[1], o=p[3]||{}, r=o.r||16;
      mk('circle',{cx:x,cy:y,r,fill:'#fff'},g);
      texText(svg,x,y+r*.42,'\\mathrm{'+(p[2]||'A')+'}',{size:o.size||Math.round(r*1.15),anchor:'middle'});
    }
    else if(kind==='npn'){
      const [x,y]=p[1], o=p[2]||{}, r=o.r||26, bx=x-r*.3, cx=x+r*.45, pnp=o.type==='pnp';
      mk('circle',{cx:x,cy:y,r,fill:'#fff'},g);
      line(x-r-18,y,bx,y); line(bx,y-r*.5,bx,y+r*.5,sw*1.4);
      line(bx,y-r*.22,cx,y-r*.72); line(cx,y-r*.72,cx,y-r-18);
      line(bx,y+r*.22,cx,y+r*.72); line(cx,y+r*.72,cx,y+r+18);
      const ex=cx-bx, ey=r*.5, el=Math.hypot(ex,ey), ux=ex/el, uy=ey/el;   // 이미터 화살: npn은 바깥으로, pnp는 안으로
      if(!pnp) head(g,bx+ex*.78,y+r*.22+ey*.78,ux,uy,5.5,ink); else head(g,bx+ex*.3,y+r*.22+ey*.3,-ux,-uy,5.5,ink);
      if(o.labels){ const s=o.size||Math.round(LS*.9); lab(x-r-14,y-8,'\\mathrm{B}',o,'end'); lab(cx+8,y-r-4,'\\mathrm{C}',o,'start'); lab(cx+8,y+r+s*.8,'\\mathrm{E}',o,'start'); }   // 단자 이름은 로마체
    }
    else if(kind==='ac'){
      const [x,y]=p[1], o=p[2]||{}, r=o.r||18, a=r*.62;
      mk('circle',{cx:x,cy:y,r,fill:'#fff'},g);
      mk('path',{d:`M${x-a} ${y} C${x-a*.6} ${y-a*1.1} ${x-a*.1} ${y-a*1.1} ${x} ${y} S${x+a*.6} ${y+a*1.1} ${x+a} ${y}`,'stroke-width':sw*.8},g);
      if(o.label!=null && o.label!==''){ const s=o.size||LS; lab(x+r*.75+4,y+r+s*.8,o.label,o,'start'); }
    }
    else if(kind==='arrow'){
      const [x1,y1]=p[1],[x2,y2]=p[2], o=p[3]||{}, col=COL[o.color]||o.color||COL.ink;
      const ag=mk('g',{},svg); arrow(ag,x1,y1,x2,y2,col,o.w||3,o.dash);
      if(o.label){ const s=o.size||LS, hz=Math.abs(x2-x1)>=Math.abs(y2-y1);
        const lx=o.lx!=null?o.lx:(x1+x2)/2+(hz?0:10), ly=o.ly!=null?o.ly:(y1+y2)/2+(hz?-10:s*.35);
        texText(svg,lx,ly,o.label,{size:s,anchor:o.anchor||(hz?'middle':'start'),fill:o.labelColor||o.color,mix:o.mix}); }
    }
    else if(kind==='label'){ const [x,y]=p[1], o=p[3]||{}; texText(svg,x,y,p[2],{size:o.size||LS,anchor:o.anchor,fill:o.fill,mix:o.mix,weight:o.weight,halo:o.halo}); }
    else console.error('[circuit] 알 수 없는 부품: '+kind);
  }catch(e){ console.error('[circuit] 부품 오류',p,e); } });
}

// 축전기 단계 패널 (5.4): <div class="cappanel" data-cfg='{"bat":1,"sw":1,"q":0.5,"cur":"up","bulb":1,"v":0,"zero":0}'>
//  bat 전지 있음(충전 회로)/없음(방전 회로) · sw 스위치 닫힘 1/열림 0 · q 충전 정도 0–1 (판의 ± 개수, 판 사이 전기장 화살표 수)
//  cur "up"(충전)/"down"(방전) 전류 화살표 · bulb 키가 있으면 전구, 1이면 켜짐 · v 판 사이 V 표시 · zero "0 V" 표시
function capPanel(div,c){
  const svg=mk('svg',{viewBox:'0 0 300 250',role:'img','aria-label':(c.bat?'전지와 연결된':'전지 없이 전구와 연결된')+' 축전기 회로'}); div.appendChild(svg);
  const g=mk('g',{fill:'none',stroke:COL.ink,'stroke-width':3,'stroke-linecap':'round','stroke-linejoin':'round'},svg);
  const ln=(x1,y1,x2,y2,w,col)=>mk('line',{x1,y1,x2,y2,'stroke-width':w||3,stroke:col||COL.ink},g);
  const L=62,R=226,T=34,B=216,PT=94,PB=156,HW=42;
  ln(L,T,L,PT); ln(L,PB,L,B); ln(L-HW,PT,L+HW,PT,4.5); ln(L-HW,PB,L+HW,PB,4.5);
  ln(L,T,122,T); ln(170,T,R,T);
  const open=!c.sw, a=-30*Math.PI/180; ln(122,T,open?122+Math.cos(a)*48:170,open?T+Math.sin(a)*48:T);
  [[122,T],[170,T]].forEach(q=>mk('circle',{cx:q[0],cy:q[1],r:4,fill:'#fff'},g));
  ln(L,B,R,B);
  const hasBulb=('bulb' in c), comps=[]; if(c.bat) comps.push('bat'); if(hasBulb) comps.push('bulb');
  const ys=comps.length===2?[92,162]:[125];
  let yPrev=T;
  comps.forEach((k,i)=>{ const y=ys[i];
    if(k==='bat'){ ln(R,yPrev,R,y-8); ln(R-20,y-8,R+20,y-8,3); ln(R-11,y+8,R+11,y+8,6); yPrev=y+8; }
    else { const r=14, k2=r*.7071; ln(R,yPrev,R,y-r); if(c.bulb==1) mk('circle',{cx:R,cy:y,r:r*1.9,fill:'#FFE45C',opacity:.6,stroke:'none'},g); mk('circle',{cx:R,cy:y,r,fill:'#fff'},g); ln(R-k2,y-k2,R+k2,y+k2,2.4); ln(R-k2,y+k2,R+k2,y-k2,2.4); yPrev=y+r; }
  });
  ln(R,yPrev,R,B);
  const q=clamp(+c.q||0,0,1), n=Math.round(q*5), m=Math.round(q*3), sz=12, t=3;
  for(let i=0;i<n;i++){ const x=L-HW+8+(2*HW-16)*(n===1?.5:i/(n-1));
    mk('rect',{x:x-sz/2,y:PT+11-t/2,width:sz,height:t,rx:1,fill:COL.plus,stroke:'none'},g); mk('rect',{x:x-t/2,y:PT+11-sz/2,width:t,height:sz,rx:1,fill:COL.plus,stroke:'none'},g);
    mk('rect',{x:x-sz/2,y:PB-11-t/2,width:sz,height:t,rx:1,fill:COL.minus,stroke:'none'},g); }
  for(let j=0;j<m;j++){ const x=L-HW+18+(2*HW-36)*(m===1?.5:j/(m-1)); arrow(g,x,PT+21,x,PB-19,COL.field,2.4); }
  if(c.v) texText(svg,L+HW+10,(PT+PB)/2+9,'V',{size:26});
  else if(c.zero) texText(svg,L+HW+10,(PT+PB)/2+9,'0\\ \\text{V}',{size:24});
  if(c.cur && c.sw){ const up=c.cur==='up', x=R+32; arrow(g,x,up?176:78,x,up?78:176,COL.ink,3); texText(svg,x+9,135,'I',{size:26}); }
}

// 지면에 수직인 자기장 표시: <g data-bgrid="x,y,w,h,간격,in|out[,색,크기]">  in = ×(들어가는 방향), out = ⊙(나오는 방향)
function bgrid(g,a){
  const x0=+a[0], y0=+a[1], w=+a[2], h=+a[3], gap=+a[4]||32, dir=(a[5]||'in').trim(), col=(a[6]&&a[6].trim())?(COL[a[6].trim()]||a[6].trim()):COL.muted, s=+(a[7]||gap*.22);
  const nx=Math.max(1,Math.floor(w/gap)), ny=Math.max(1,Math.floor(h/gap)), ox=x0+(w-(nx-1)*gap)/2, oy=y0+(h-(ny-1)*gap)/2;
  for(let i=0;i<nx;i++) for(let j=0;j<ny;j++){ const cx=ox+i*gap, cy=oy+j*gap;
    if(dir==='out'){ mk('circle',{cx,cy,r:s*1.15,fill:'none',stroke:col,'stroke-width':1.6},g); mk('circle',{cx,cy,r:s*.32,fill:col},g); }
    else { mk('line',{x1:cx-s,y1:cy-s,x2:cx+s,y2:cy+s,stroke:col,'stroke-width':2,'stroke-linecap':'round'},g); mk('line',{x1:cx-s,y1:cy+s,x2:cx+s,y2:cy-s,stroke:col,'stroke-width':2,'stroke-linecap':'round'},g); } }
}
deck.querySelectorAll('[fill],[stroke],[stop-color]').forEach(e=>['fill','stroke','stop-color'].forEach(k=>{ const v=e.getAttribute(k); if(v&&COL[v]) e.setAttribute(k,COL[v]); }));   // fill="bfield" 등(D7)
deck.querySelectorAll('[data-bgrid]').forEach(g=>{ try{ bgrid(g,g.dataset.bgrid.split(',')); }catch(e){ console.error('[bgrid] 오류',g,e); } });
// <g class="step" data-circuit='…'>로 단계 공개 회로도 가능
deck.querySelectorAll('svg[data-circuit], g[data-circuit]').forEach(svg=>{ try{ renderCircuit(svg,JSON.parse(svg.dataset.circuit)); }catch(e){ console.error('[circuit] JSON 오류',svg,e); } });
deck.querySelectorAll('svg[data-field]').forEach(svg=>fieldLines(svg,JSON.parse(svg.dataset.field)));
deck.querySelectorAll('.cappanel[data-cfg]').forEach(d=>{ try{ capPanel(d,JSON.parse(d.dataset.cfg)); }catch(e){ console.error('[cappanel] 오류',d,e); } });
deck.querySelectorAll('[data-vfield]').forEach(g=>vfield(g,JSON.parse(g.dataset.vfield)));
deck.querySelectorAll('[data-arw]').forEach(g=>{ const a=g.dataset.arw.split(',').map(s=>s.trim()); arrow(g,+a[0],+a[1],+a[2],+a[3],COL[a[4]]||a[4],a[5]?+a[5]:3,a[6]==='d'); });
deck.querySelectorAll('[data-chg]').forEach(g=>{ const a=g.dataset.chg.split(',').map(s=>s.trim()); charge(g,+a[0],+a[1],+a[2],a[3],a[4]==='d'); });
deck.querySelectorAll('[data-atom]').forEach(g=>{ try{ const a=g.dataset.atom.split(',').map(s=>s.trim()); const d=a[4]==='d'||a[5]==='d'; atom(g,+a[0],+a[1],+a[2],a[3],a[4]==='d'?'':(a[4]||''),d); }catch(e){ console.error('[atom] 오류',g,e); } });
deck.querySelectorAll('[data-pm]').forEach(g=>{ const a=g.dataset.pm.split(','); const sign=a[0].trim(), sz=+a[1], col=colOf(a[3]&&a[3].trim())||(sign==='+'?COL.plus:COL.minus), t=Math.max(2.2,sz*.24);
  a[2].trim().split(/\s+/).forEach(p=>{ const [x,y]=p.split(':').map(Number); mk('rect',{x:x-sz/2,y:y-t/2,width:sz,height:t,rx:t/3,fill:col},g); if(sign==='+') mk('rect',{x:x-t/2,y:y-sz/2,width:t,height:sz,rx:t/3,fill:col},g); }); });

// 실험실
function signed(v){ return v>0?'+'+v:v<0?'−'+(-v):'0'; }
function fmtN(v){ if(v===0) return '0'; if(v>=100) return v.toFixed(0); if(v>=10) return v.toFixed(1); if(v>=1) return v.toFixed(2); return v.toFixed(3); }
function gcd(a,b){ return b?gcd(b,a%b):a; }
function niceRatio(x){ if(!isFinite(x)) return '—'; for(let d=1;d<=36;d++){ const n=Math.round(x*d); if(n>0 && Math.abs(n/d-x)<1e-9){ const g=gcd(n,d); return d/g===1?(n/g)+'배':(n/g)+'/'+(d/g)+'배'; } } return x.toFixed(2)+'배'; }
function clamp(v,a,b){ return Math.max(a,Math.min(b,v)); }
function place(e,x,y,vis){ e.style.left=x+'px'; e.style.top=y+'px'; e.style.display=vis===false?'none':''; }
const LABS={
  coulomb(root){
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), V=k=>$(`[data-ov="${k}"]`);
    const iq1=$('[data-i="q1"]'), iq2=$('[data-i="q2"]'), ir=$('[data-i="r"]'), g=mk('g',{},$('svg'));
    let ref=null;
    const Fof=()=>90*Math.abs(iq1.value*iq2.value)/(ir.value*ir.value);   // k·(μC)²/(cm)² = 90 N
    function draw(){
      const q1=+iq1.value, q2=+iq2.value, r=+ir.value, F=Fof();
      O('q1').textContent=signed(q1)+' μC'; O('q2').textContent=signed(q2)+' μC'; O('r').textContent=r+' cm';
      O('F').textContent=fmtN(F)+' N';
      const kd=O('kind'); kd.className='kind '+(F===0?'':q1*q2>0?'rep':'att');
      kd.textContent=F===0?'전하량이 0이면 전기력이 없다':q1*q2>0?'척력: 서로 밀어낸다':'인력: 서로 끌어당긴다';
      O('ratio').textContent=ref===null?'':ref===0?'기준이 0 N':'기준의 '+niceRatio(F/ref);
      while(g.firstChild) g.removeChild(g.firstChild);
      const cx=340, y=150, x1=cx-r*8, x2=cx+r*8, R=24;
      mk('line',{x1:12,y1:y,x2:668,y2:y,stroke:'#D5DDE5','stroke-width':2,'stroke-dasharray':'6 6'},g);
      mk('line',{x1,y1:272,x2,y2:272,stroke:COL.muted,'stroke-width':1.5},g);
      [x1,x2].forEach(x=>mk('line',{x1:x,y1:263,x2:x,y2:281,stroke:COL.muted,'stroke-width':1.5},g));
      charge(g,x1,y,R,q1>0?'P':q1<0?'M':'N'); charge(g,x2,y,R,q2>0?'P':q2<0?'M':'N');
      place(V('b1'),x1,y); place(V('b2'),x2,y); place(V('r'),cx,272);
      if(F>0){
        const d=q1*q2>0?-1:1, L=clamp(16+22*Math.log10(F/.05),20,92);
        mk('line',{x1,y1:104,x2:x1,y2:y-R,stroke:COL.ink,'stroke-width':1.2,'stroke-dasharray':'2 3'},g);
        mk('line',{x1:x2,y1:y+R,x2:x2,y2:196,stroke:COL.ink,'stroke-width':1.2,'stroke-dasharray':'2 3'},g);
        arrow(g,x1,96,x1+d*L,96,COL.ink,3.5); arrow(g,x2,204,x2-d*L,204,COL.ink,3.5);
        place(V('l1'),clamp(x1+d*L/2,105,575),60); place(V('l2'),clamp(x2-d*L/2,105,575),216);
      } else { place(V('l1'),0,0,false); place(V('l2'),0,0,false); }
    }
    [iq1,iq2,ir].forEach(i=>i.addEventListener('input',draw));
    $('[data-b="ref"]').addEventListener('click',()=>{ ref=Fof(); draw(); });
    draw();
  },
  potential(root){
    const $=s=>root.querySelector(s), O=k=>$(`[data-o="${k}"]`), V=k=>$(`[data-ov="${k}"]`);
    const ih=$('[data-i="h"]'), iq=$('[data-i="q"]'), g=mk('g',{},$('svg'));
    const f=v=>Number.isInteger(v)?String(v):v.toFixed(1);
    function draw(){
      const h=+ih.value, q=+iq.value, Vv=2*h, Wv=q*Vv;           // 12 V / 6 cm = 2 V/cm
      O('h').textContent=h.toFixed(1)+' cm'; O('q').textContent='+'+q+' C';
      O('W').textContent=f(Wv)+' J'; O('U').textContent=f(Wv)+' J'; O('V').textContent=f(Vv)+' V'; O('Vt').textContent=f(Vv)+' V';
      while(g.firstChild) g.removeChild(g.firstChild);
      const cx=230, cy=340-50*h, R=12+4*q;
      mk('line',{x1:cx+R+4,y1:cy,x2:440,y2:cy,stroke:COL.muted,'stroke-width':1.5,'stroke-dasharray':'5 5'},g);
      mk('polygon',{points:`452,${cy} 440,${cy-7} 440,${cy+7}`,fill:COL.ink},g);
      charge(g,cx,cy,R,'+');
      const ya=clamp(cy-20,50,292), xa=cx-R-18;
      arrow(g,xa,ya,xa,ya+40,COL.ink,3.5);
      place(V('F'),xa-8,ya+20); place(V('Vt'),412,cy-6);
    }
    [ih,iq].forEach(i=>i.addEventListener('input',draw));
    draw();
  }
};
// 차시별 실험실: 내용 파일의 window.DECK_LABS = { 이름(root, API){…} } 를 함께 등록한다.
const readyHooks=[];
const API={mk,arrow,head,charge,atom,ATOM,vfield,fieldAt,trace,fieldLines,texText,bgrid:(g,x,y,w,h,gap,dir,col,size)=>bgrid(g,[x,y,w,h,gap,dir,col||'',size||'']),signed,fmtN,niceRatio,clamp,place,COL,SVGNS,
  // 슬라이드가 보일 때만 도는 애니메이션 반복. fn(dt초, t초). 멈추는 함수를 돌려준다.
  loop(root,fn){ const slide=root.closest('.slide'); let last=0, raf=0, stop=false;
    const tick=ts=>{ if(stop) return; raf=requestAnimationFrame(tick); if(!slide||!slide.classList.contains('active')){ last=0; return; } const dt=last?Math.min(.05,(ts-last)/1000):0; last=ts; try{ fn(dt,ts/1000); }catch(e){ console.error(e); stop=true; } };
    raf=requestAnimationFrame(tick); return ()=>{ stop=true; cancelAnimationFrame(raf); }; },
  onShow(fn){ showHooks.push(fn); },          // fn(slide, index) — 슬라이드가 보일 때마다
  ready(fn){ readyHooks.push(fn); },          // KaTeX·texSVG·keepWords가 끝난 뒤 한 번
  tex(t){ return tex2html(t); },               // LaTeX 문자열 → HTML (KaTeX가 아직 없으면 간이 표시)
  isActive(root){ const s=root.closest('.slide'); return !!(s&&s.classList.contains('active')); }
};
Object.assign(LABS, window.DECK_LABS||{});
deck.querySelectorAll('.lab[data-lab]').forEach(r=>{ const fn=LABS[r.dataset.lab]; if(!fn){ console.error('[lab] 등록되지 않은 실험실: '+r.dataset.lab); return; } try{ fn(r,API); }catch(e){ console.error('[lab '+r.dataset.lab+']',e); } });
// 첫 show()는 실험실 등록 전에 불렸으므로, 지금 보이는 슬라이드에 대해 표시 훅을 한 번 불러 준다.
showHooks.forEach(f=>{ try{ f(slides[cur],cur); }catch(e){ console.error(e); } });


/* ─────────── 움직임 (가이드 6.4) ─────────── */
// 정지 모드: 캡처·점검(도구가 window.__STILL을 넣음)·?still·?audit·편집기·'동작 줄이기' 설정 → 움직임 없이 그린 그대로.
//   그림은 언제나 '그린 모습 = 마지막 모습'이다. 움직임은 그 모습에서 출발값(data-from)을 거꾸로 거슬러 와서 끝난다.
// 자동(모든 덱): ① 슬라이드가 보일 때 본문 덩어리가 차례로 떠오름(h2는 왼쪽에서) ② 형광펜(mark)이 그어짐
//   ③ 그림 속 화살표(data-arw)가 꼬리에서 머리로 자라남 ④ 단계 공개: 글은 떠오르고, 그림(SVG) 단계는 선이 그려지고, 정답(.ans)은 한 번 튐
// 내용이 정하는 그림 움직임: SVG 요소에 data-anim
//   rot  data-from="각(°)" data-o="cx,cy"  — 각만큼 돌려 놓은 데서 그린 모습으로 (시계 방향 +)
//   move data-from="dx,dy"                 — 그만큼 옮긴 데서
//   scale data-from="배율" 또는 "가로배율,세로배율"(예 "1,0" = 세로로 자라남) data-o="cx,cy"
//   fade · draw(선 그리기) · pop(작게서 튀어나옴, data-o)
//   spin data-o="cx,cy" data-speed="°/s"   — 계속 돎 · dash data-speed="px/s" — 점선이 흐름(전류·흐름 표시)
//   공통: data-dur(초, 기본 1.2) data-delay(초) data-rep="once|alt|loop|damp|swing"(기본 once; swing = 그린 모습을 가운데로 ±출발값 사이를 계속 흔들림(dur = 반 주기); alt = 그린 모습↔출발값 왕복, damp = 양쪽으로 흔들리며 줄어 그린 모습에 섬 — dur는 반 번 흔들리는 시간)
//         data-ease="io|out|lin|in|soft|back|bounce"(기본 io; in = 정지에서 등가속, out = 등감속해 정지, soft = 부드럽게 멈춤) data-on="step"(가까운 .step이 켜질 때 시작; 기본은 슬라이드가 보일 때)
const STILL=(!!window.__STILL&&!params.has('motion'))||params.has('still')||params.has('audit')||EDIT||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
document.documentElement.classList.toggle('still',STILL);
const EASE={lin:t=>t,io:t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2,out:t=>1-(1-t)*(1-t),in:t=>t*t,   // in = 정지에서 등가속(낙하), out = 등감속해 정지(제동)
  soft:t=>1-Math.pow(1-t,3), sine:t=>(1-Math.cos(Math.PI*t))/2,   // sine = 단진동 모양(alt와 함께 진동·정상파)
  back:t=>{ const c=1.70158; return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2); },
  bounce:t=>{ const n=7.5625,d=2.75; if(t<1/d) return n*t*t; if(t<2/d) return n*(t-=1.5/d)*t+.75; if(t<2.5/d) return n*(t-=2.25/d)*t+.9375; return n*(t-=2.625/d)*t+.984375; }};
// 본문 덩어리에 차례 번호(떠오르는 순서)
slides.forEach(s=>{ let k=0; [...s.children].forEach(c=>{ if(!c.classList.contains('band')) c.style.setProperty('--i',k++); }); });
function strokeLen(e){ try{ return e.getTotalLength(); }catch(_){ return 0; } }
function drawStroke(e,delay,dur){
  if(STILL||!e.animate) return; const L=strokeLen(e); if(!L||e.getAttribute('stroke-dasharray')) return fadeIn(e,delay,dur);
  e.animate([{strokeDasharray:L+' '+L,strokeDashoffset:L},{strokeDasharray:L+' '+L,strokeDashoffset:0}],{duration:dur*1000,delay:delay*1000,easing:'cubic-bezier(.3,.6,.3,1)',fill:'backwards'});
}
function fadeIn(e,delay,dur){ if(!STILL&&e.animate) e.animate([{opacity:0},{opacity:parseFloat(getComputedStyle(e).opacity)||1}],{duration:dur*1000,delay:delay*1000,fill:'backwards'}); }
function growArrows(root,delay){
  root.querySelectorAll('[data-arw]').forEach((g,k)=>{ const st=g.closest('.step'); if(st&&!st.classList.contains('on')&&!root.matches('.step')) return;
    if(g.closest('[data-anim]')&&!root.matches('[data-anim]')) return;   // 움직이는 묶음 안의 화살표는 그 움직임을 따름
    const own=g.dataset.delay!=null&&g.dataset.delay!==''?+g.dataset.delay:null;   // 화살표 자체의 data-delay(초) — 광선 draw 끝에 맞출 때
    const d=own!=null?delay+own:delay+Math.min(k,8)*.08; g.querySelectorAll('.arw-l').forEach(l=>drawStroke(l,d,.55)); g.querySelectorAll('.arw-h').forEach(h=>fadeIn(h,d+.4,.2)); });
}
window.__fxReveal=e=>{
  if(STILL) return;
  const inSvg=e.ownerSVGElement&&e.tagName.toLowerCase()!=='svg';
  if(inSvg){ const parts=[...e.querySelectorAll('path,line,polyline,circle,ellipse,rect')].filter(x=>!x.closest('[data-arw]')&&x.getAttribute('stroke')&&x.getAttribute('stroke')!=='none');
    if(['path','line','polyline'].includes(e.tagName)) parts.push(e);
    parts.slice(0,30).forEach(x=>drawStroke(x,0,.6)); growArrows(e,0); }
  else growArrows(e,.1);
  const ans=e.matches('.ans')?[e]:[...e.querySelectorAll('.ans')];
  ans.forEach(a=>a.animate&&a.animate([{backgroundColor:'rgba(255,228,92,0)'},{backgroundColor:'rgba(255,228,92,.95)'},{backgroundColor:'rgba(255,228,92,0)'}],{duration:900,delay:250,easing:'ease-out'}));
  ANIMS.forEach(a=>{ if((a.onStep&&a.e.closest('.step')===e)||(a.onG&&e.dataset.g===a.onG&&a.slide===e.closest('.slide'))) a._t0=null; });   // 단계가 막 켜짐 → 그 단계의 그림 움직임 시작
};
const ANIMS=[...deck.querySelectorAll('[data-anim]')].map(e=>{ const d=e.dataset, num=(v,def)=>v==null||v===''?def:+v, pair=v=>(v||'0,0').split(',').map(Number);
  return {e,type:d.anim,from:d.from,o:pair(d.o),dur:num(d.dur,1.2),delay:num(d.delay,0),rep:d.rep||'once',ease:EASE[d.ease]||EASE.io,speed:num(d.speed,d.anim==='spin'?40:30),
    onStep:d.on==='step'&&!!e.closest('.step'),onG:(d.on||'').startsWith('g:')?d.on.slice(2):null,base:e.getAttribute('transform')||'',slide:e.closest('.slide'),len:0,op:parseFloat(getComputedStyle(e).opacity)||1}; });   // op = 그린 모습의 불투명도(opacity 속성 유지)
const nz=v=>Math.abs(v)<.001?(v<0?-.001:.001):v;   // 0 배율만 피함(음수 = 뒤집힘 허용: 정상파 "1,-1")
function applyAnim(a,p){   // p: 0 = 출발값, 1 = 그린 모습 · spin/dash는 경과 시간
  const e=a.e, q=1-p, [cx,cy]=a.o;
  let tf='';
  switch(a.type){
    case 'rot': tf=`rotate(${(+a.from||0)*q} ${cx} ${cy})`; break;
    case 'move': { const [dx,dy]=(a.from||'0,0').split(',').map(Number); tf=`translate(${dx*q} ${dy*q})`; break; }
    case 'scale': { const f=String(a.from||'1').split(',').map(Number), fx=f[0], fy=f.length>1?f[1]:f[0], sx=1+(fx-1)*q, sy=1+(fy-1)*q; tf=`translate(${cx} ${cy}) scale(${nz(sx)} ${nz(sy)}) translate(${-cx} ${-cy})`; break; }
    case 'pop': { const s=Math.max(.001,p); tf=`translate(${cx} ${cy}) scale(${s}) translate(${-cx} ${-cy})`; break; }
    case 'fade': e.style.opacity=p*a.op; break;
    case 'draw': { if(!a.parts){ const tg=e.tagName.toLowerCase(); a.parts=(tg==='g'||tg==='a')?[...e.querySelectorAll('path,line,polyline,polygon,circle,ellipse,rect')].filter(x=>{ const cs=getComputedStyle(x); return cs.stroke&&cs.stroke!=='none'; }):[e];   // <g>에 걸면 안의 선들을 함께 그림
        a.parts=a.parts.map(x=>({x,dashed:!!(x.getAttribute('stroke-dasharray')||getComputedStyle(x).strokeDasharray!=='none'&&getComputedStyle(x).strokeDasharray),len:strokeLen(x)||1,op:parseFloat(getComputedStyle(x).opacity)||1}));
        a.dashed=a.parts.some(r=>r.dashed); }
      for(const r of a.parts){ if(r.dashed){ r.x.style.opacity=p*r.op; continue; }   // 점선은 그리기 대신 나타남(점선 모양 유지)
        r.x.style.strokeDasharray=r.len+' '+r.len; r.x.style.strokeDashoffset=r.len*q; }
      break; }
  }
  if(a.type!=='fade'&&a.type!=='draw') e.setAttribute('transform',(tf+' '+a.base).trim());
}
function resetAnim(a){ if(a.type==='fade') a.e.style.opacity=''; if(a.type==='draw') (a.parts||[]).forEach(r=>{ r.x.style.opacity=''; r.x.style.strokeDasharray=''; r.x.style.strokeDashoffset=''; }); if(a.type!=='dash') a.e.setAttribute('transform',a.base); if(!a.base) a.e.removeAttribute('transform'); if(a.type==='dash') a.e.style.strokeDashoffset=''; }
if(!STILL&&ANIMS.length){
  showHooks.push(s=>{ const now=performance.now()/1000; ANIMS.forEach(a=>{ if(a.slide===s){ a._t0=a.onG?(a.slide.querySelector('.step.on[data-g="'+a.onG+'"]')?now:undefined):a.onStep?(a.e.closest('.step')&&a.e.closest('.step').classList.contains('on')?now:undefined):now; if(a._t0!==undefined&&a.type!=='spin'&&a.type!=='dash') applyAnim(a,0); } }); });
  const tick=()=>{ requestAnimationFrame(tick); const now=performance.now()/1000;
    for(const a of ANIMS){ if(!a.slide.classList.contains('active')) continue;
      if(a._t0===null) a._t0=now;                       // 단계가 막 켜짐
      if(a._t0===undefined){ continue; }
      const t=now-a._t0-a.delay;
      if(a.type==='spin'){ if(t>=0) a.e.setAttribute('transform',`rotate(${(t*a.speed)%360} ${a.o[0]} ${a.o[1]}) ${a.base}`.trim()); continue; }
      if(a.type==='dash'){ a.e.style.strokeDashoffset=-(Math.max(0,t)*a.speed); continue; }
      if(t<0){ applyAnim(a,0); continue; }
      if(a.rep==='swing'){ applyAnim(a,1-Math.cos(Math.PI*t/a.dur)); continue; }   // 그린 모습을 가운데로 양쪽 끝(±출발값)까지 계속 흔들림(진자·용수철)
      if(a.rep==='damp'){ const u=t/a.dur, q=Math.cos(Math.PI*u)*Math.exp(-u/2.2); applyAnim(a,u>2&&Math.abs(q)<.004?1:1-q); continue; }   // 감쇠 왕복: 양쪽으로 흔들리며 줄어 그린 모습에 섬
      let u=t/a.dur;
      if(a.rep==='once') u=Math.min(1,u);
      else if(a.rep==='loop') u=u%1;
      else { u=u%2; u=u>1?2-u:u; }                       // alt: 왕복
      applyAnim(a,a.ease(u));
    } };
  requestAnimationFrame(tick);
  // 단계로 숨겨 둔 그림 움직임은 처음엔 출발값(보이지 않으니 상관없음) — 켜질 때 시작
  ANIMS.forEach(a=>{ if(a.onStep||a.onG) a._t0=undefined; });
}
if(!STILL) showHooks.push(s=>growArrows(s,.35));
if(!STILL){ try{ growArrows(slides[cur],.35); ANIMS.forEach(a=>{ if(a.slide===slides[cur]&&!a.onStep&&!a.onG) a._t0=performance.now()/1000; }); }catch(e){ console.error(e); } }

/* ─────────── 질문 먼저, 답은 다음 누름에 (가이드 6.5) ─────────── */
// 다음 단계가 '답'이면 한 번 누를 때 질문(빈칸·질문 문장·개념 지도 빈칸 상자)을 강조만 하고, 다음 누름에 답을 연다.
// 답으로 보는 단계: .blank 안의 단계 · .ans/.answer(를 품은) 단계 · '→'로 시작하는 단계 · SVG에서 점선 빈칸 상자 위의 글 단계 · data-ask가 있는 단계.
// 빼기: 단계에 data-ask="no". 평가 문항(.pf-key 안 — 풀이 공간 단계가 이미 있음)과 도구·편집 모드는 하지 않는다.
var ASK_OFF=(!!window.__STILL&&!params.has('motion'))||params.has('audit')||EDIT;
function svgBlankBox(e){
  const svg=e.ownerSVGElement; if(!svg) return null;
  let bb; try{ bb=e.getBBox(); }catch(_){ return null; } if(!bb||(!bb.width&&!bb.height)) return null;
  const cx=bb.x+bb.width/2, cy=bb.y+bb.height/2;
  for(const r of svg.querySelectorAll('rect')){ if(r===e||e.contains(r)) continue;
    const d=r.getAttribute('stroke-dasharray')||(r.style&&r.style.strokeDasharray); if(!d&&!r.classList.contains('blank')) continue;
    const x=+r.getAttribute('x'), y=+r.getAttribute('y'), w=+r.getAttribute('width'), h=+r.getAttribute('height');
    if(cx>=x-4&&cx<=x+w+4&&cy>=y-4&&cy<=y+h+4) return r; }
  return null;
}
function isAnswerEl(e){
  if(e.dataset&&e.dataset.ask==='no') return false;
  if(e.closest&&e.closest('.pf-key')) return false;
  if(e.dataset&&e.dataset.ask!==undefined) return true;
  if(e.ownerSVGElement) return !!svgBlankBox(e);
  if(e.closest('.blank')) return true;
  if(e.matches('.ans,.answer')||e.querySelector('.ans,.answer')) return true;
  const tx=e.textContent||''; return /^\s*→/.test(tx)&&!/[?？]\s*$/.test(tx.trim());   // '→ …?'는 질문
}
function askArea(x){ const b=x.getBoundingClientRect(), D=deck.getBoundingClientRect(); return D.width&&D.height?b.width*b.height/(D.width*D.height):0; }
function askHidden(x){ return !!(x.closest('.step:not(.on)')||getComputedStyle(x).visibility==='hidden'); }
function askIsQ(x){ return x.hasAttribute('data-q')||/[?？]|^\s*Q/.test(x.textContent||''); }   // 질문 문장: '?'·'Q…' 또는 data-q
function askQuestionIn(c){ const qs=[...c.querySelectorAll('p,li,h3,td,.card,.note,[data-q]')].filter(q=>!askHidden(q)&&askIsQ(q)&&askArea(q)<=.3); return qs.length?qs[qs.length-1]:null; }
function askQ(x){ if(!x||askHidden(x)||x.classList.contains('band')) return null; if((x.matches('p,li,h2,h3,.card,.note')||x.hasAttribute('data-q'))&&askIsQ(x)&&askArea(x)<=.3) return x; return askQuestionIn(x); }   // 질문 문장만(그림·빈 칸 제외)
function askMarked(e){   // 답 앞쪽에서 가장 가까운 data-q — 그 사이에 '?' 질문이 먼저 있으면 그 질문이 우선(null → 보통 찾기)
  const own=e.closest('[data-q]'); if(own&&own!==e&&!askHidden(own)) return own;
  for(let anc=e; anc&&!anc.classList.contains('slide'); anc=anc.parentElement)
    for(let q=anc.previousElementSibling; q; q=q.previousElementSibling){
      if(askHidden(q)) continue;
      const m=q.hasAttribute('data-q')?q:[...q.querySelectorAll('[data-q]')].filter(x=>!askHidden(x)).pop();
      if(m) return m;
      if(/[?？]/.test(q.textContent||'')) return null; }
  return null;
}
function askFit(c){ if(!c||c.classList.contains('slide')||askHidden(c)) return null; return askArea(c)<=.3?c:askQuestionIn(c); }   // 너무 크면 그 안의 질문 줄만
function askTargets(a){
  const out=new Set();
  a.forEach(e=>{ if(!isAnswerEl(e)) return;
    if(e.ownerSVGElement){ const r=svgBlankBox(e); if(r&&!askHidden(r)) out.add(r); return; }
    const bl=e.closest('.blank'); if(bl){ if(!askHidden(bl)) out.add(bl); return; }
    let c=askMarked(e);
    if(c) ; else if(/^inline/.test(getComputedStyle(e).display)) c=askFit(e.parentElement&&e.parentElement.closest('p,li,td,th,dd,h3,.card,.note,div'));
    else { let p=e.previousElementSibling;
      while(p&&!c){ if(!p.classList.contains('step')&&!p.classList.contains('band')) c=askFit(p); p=c?p:p.previousElementSibling; }
      if(!c) c=askFit(e.parentElement&&e.parentElement.closest('.card,.note,.stage'));
      for(let anc=e.parentElement; !c&&anc&&!anc.classList.contains('slide'); anc=anc.parentElement)   // 답 묶음 첫 답: 바깥 앞쪽의 질문 문장
        for(let q=anc.previousElementSibling; q&&!c; q=q.previousElementSibling) c=askQ(q); }
    if(c) out.add(c);
  });
  return [...out];
}
function askable(a){ return !ASK_OFF&&a.some(isAnswerEl)&&askTargets(a).length>0; }   // 강조할 질문을 못 찾으면 바로 답(헛누름 없음)
function askOn(a,on){
  if(on){ a._asking=true; a._askEls=askTargets(a); a._askEls.forEach(x=>{ x.classList.remove('ask'); void x.getBoundingClientRect(); x.classList.add('ask'); }); }
  else { a._asking=false; (a._askEls||[]).forEach(x=>x.classList.remove('ask')); a._askEls=null; }
}

/* ─────────── 움직이는 그림을 누르면 다시 움직임 ─────────── */
window.__replayFig=svg=>{
  if(STILL) return false;
  const now=performance.now()/1000; let any=false;
  ANIMS.forEach(a=>{ if(!svg.contains(a.e)) return; const st=a.e.closest('.step'); if(a.onStep&&!(st&&st.classList.contains('on'))) return;
    if(a.type==='spin'||a.type==='dash') return; a._t0=now; applyAnim(a,0); any=true; });
  if(svg.querySelector('[data-arw]')){ growArrows(svg,0); any=true; }
  return any;
};
ANIMS.forEach(a=>{ const s=a.e.ownerSVGElement; if(s) s.setAttribute('data-replay',''); });
/* ─────────── 편집 모드: 클릭 = 요소 고르기 (window.__EDIT_MODE일 때만) ─────────── */
// 부모 창으로: {type:'ready',N} · {type:'pick',slide(0부터),eid} · {type:'show',slide(0부터)}
// 부모 창에서: {type:'show',slide,mode('all'|'reset')} · {type:'select',eid} · {type:'audit'} → 답 {type:'audit',issues:[{slide(1부터),rule,msg,eid}]}
//   (같은 출처 iframe이면 Harness.show·Harness.audit를 직접 불러도 된다)
if(EDIT){
  const st=document.createElement('style');
  st.textContent='#nav,#hud{display:none!important} #deck [data-eid]{cursor:pointer} .eid-pick{outline:3px solid #FFB000!important;outline-offset:2px}';
  document.head.appendChild(st);
  let picked=null;
  const mark=el=>{ if(picked) picked.classList.remove('eid-pick'); picked=el||null; if(picked) picked.classList.add('eid-pick'); };
  addEventListener('click',e=>{
    const el=e.target&&e.target.closest&&e.target.closest('#deck [data-eid]');
    if(!el) return;
    e.preventDefault(); e.stopPropagation();
    mark(el); editPost({type:'pick',slide:slides.indexOf(el.closest('#deck > section.slide')),eid:el.getAttribute('data-eid')});
  },true);
  showHooks.push((s,i)=>{ if(picked && !s.contains(picked)) mark(null); editPost({type:'show',slide:i}); });
  addEventListener('message',e=>{
    const m=e.data; if(e.source!==window.parent || !m || typeof m!=='object') return;
    if(m.type==='show') show(m.slide|0, m.mode==='reset'?'reset':'all');
    else if(m.type==='select'){ const el=/^\d+-\d+$/.test(m.eid||'')?deck.querySelector('[data-eid="'+m.eid+'"]'):null; if(el){ const i=slides.indexOf(el.closest('#deck > section.slide')); if(i>=0 && i!==cur) show(i,'all'); } mark(el); }
    else if(m.type==='audit'){ const r=runAudit(false)||[]; editPost({type:'audit',issues:r.map(x=>{ const h=x.el&&x.el.closest?x.el.closest('[data-eid]'):null; return {slide:x.slide,rule:x.rule,msg:x.msg,eid:h?h.getAttribute('data-eid'):null}; })}); }
  });
}

/* ─────────── 4. texSVG: SVG <text class="tex"> → foreignObject + KaTeX ─────────── */
function esc(s){ return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function tex2html(t){ if(window.katex){ try{ return katex.renderToString(t,{throwOnError:false}); }catch(e){} } return '<i>'+esc(t)+'</i>'; }
function mix2html(s){ return s.split(/(\$[^$]+\$)/).map(p=>(p.length>1&&p[0]==='$'&&p[p.length-1]==='$')?tex2html(p.slice(1,-1)):esc(p)).join(''); }
let texItems=[];
function fontsReady(){
  if(!document.fonts) return Promise.resolve();
  const loads=['22px KaTeX_Main','italic 22px KaTeX_Math','700 22px KaTeX_Main'].map(f=>document.fonts.load(f).catch(()=>{}));
  return Promise.race([Promise.all(loads).then(()=>document.fonts.ready),new Promise(r=>setTimeout(r,3000))]);
}
async function texSVG(){
  const ts=[...deck.querySelectorAll('svg text.tex')]; if(!ts.length) return;
  const box=document.createElement('div'); box.className='texmeasure'; document.body.appendChild(box);
  texItems=ts.map(t=>{
    const size=+(t.dataset.size||20), anchor=t.dataset.anchor||'start';
    const cls='texlab'+(anchor==='middle'?' c':anchor==='end'?' r':'')+(t.dataset.halo!=null?' halo':'');
    const lines=t.dataset.tex!=null?[tex2html(t.dataset.tex)]:(t.dataset.mix||'').split('||').map(mix2html);
    const inner=lines.map((h,i)=>'<span class="ln">'+h+(i===0?'<span class="probe"></span>':'')+'</span>').join('');
    const m=document.createElement('span'); m.className=cls; m.style.fontSize=size+'px'; if(t.dataset.weight) m.style.fontWeight=t.dataset.weight; m.innerHTML=inner;
    box.appendChild(m); box.appendChild(document.createElement('br'));
    const fo=document.createElementNS(SVGNS,'foreignObject'); fo.setAttribute('class','texfo'+(t.classList.contains('step')?' step':'')); if(t.dataset.g) fo.dataset.g=t.dataset.g; if(t.dataset.overlap) fo.dataset.overlap=t.dataset.overlap; if(t.dataset.eid) fo.dataset.eid=t.dataset.eid;
    const d=document.createElementNS(XHTML,'div'); d.className=cls; d.style.fontSize=size+'px'; if(t.dataset.weight) d.style.fontWeight=t.dataset.weight; d.style.color=t.getAttribute('fill')||COL.ink;
    d.innerHTML=inner.replace('<span class="probe"></span>',''); fo.appendChild(d);
    t.replaceWith(fo);
    return {fo,m,x:+t.getAttribute('x'),y:+t.getAttribute('y'),anchor};
  });
  void box.offsetHeight;
  await fontsReady();
  layoutTex();
  if(document.fonts && document.fonts.addEventListener) document.fonts.addEventListener('loadingdone',()=>{ clearTimeout(layoutTex.t); layoutTex.t=setTimeout(layoutTex,60); });
  slides.forEach(s=>{ delete s._g; }); paint(cur);
}
function layoutTex(){
  texItems.forEach(it=>{ const r=it.m.getBoundingClientRect(), p=it.m.querySelector('.probe').getBoundingClientRect();
    const w=r.width, h=r.height, b=p.top-r.top, x0=it.anchor==='middle'?it.x-w/2:it.anchor==='end'?it.x-w:it.x;
    it.fo.setAttribute('x',(x0-1).toFixed(1)); it.fo.setAttribute('y',(it.y-b-1).toFixed(1)); it.fo.setAttribute('width',(w+2).toFixed(1)); it.fo.setAttribute('height',(h+2).toFixed(1)); });
}

/* ─────────── 5. keepWords: 어절 단위 보정 (T1, T2) ─────────── */
function keepWords(root){
  const SKIP='svg,.katex,button,output,canvas,script,style,textarea,select,.w,.band .pg';
  const tw=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode(n){ if(!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT; const p=n.parentElement; return (!p||p.closest(SKIP))?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT; }});
  const nodes=[]; while(tw.nextNode()) nodes.push(tw.currentNode);
  const WJ='⁠';
  // WORD JOINER는 inline-block(수식 .katex 안의 .base, 빈칸 .blank) 경계에서는 줄바꿈을 막지 못한다 → 그 요소와 붙은 낱말을 span.w(nowrap)로 함께 감싼다
  const ATOM='.katex,.blank';
  const atom=e=>!!(e && e.nodeType===1 && !e.closest('.lab') && (e.matches(ATOM) || (e.tagName==='SPAN' && e.children.length===1 && e.firstElementChild.classList.contains('katex'))));   // 자동 렌더는 <span><span class="katex">…</span></span>
  const glued=e=>!!(e && e.nodeType===1 && e.classList.contains('w') && e.dataset.glue==='1');
  nodes.forEach(n=>{
    let v=n.nodeValue; const pv=n.previousSibling, nx=n.nextSibling;
    const glueL=/^\S/.test(v) && (atom(pv)||glued(pv)), glueR=/\S$/.test(v) && atom(nx);
    if(/^\S/.test(v) && pv && pv.nodeType===1 && pv.tagName!=='BR') v=WJ+v;
    if(/\S$/.test(v) && nx && nx.nodeType===1 && nx.tagName!=='BR') v=v+WJ;
    const toks=v.split(/(\s+)/).filter(Boolean), frag=document.createDocumentFragment();
    let host=null;
    toks.forEach((tok,k)=>{
      if(/^\s+$/.test(tok)){ frag.appendChild(document.createTextNode(tok)); return; }
      if(k===0 && glueL && glued(pv)){ pv.appendChild(document.createTextNode(tok)); host=pv; }
      else { const s=document.createElement('span'); s.className='w'; if(k===0 && glueL){ s.dataset.glue='1'; s.appendChild(pv); } s.appendChild(document.createTextNode(tok)); frag.appendChild(s); host=s; }
      if(k===toks.length-1 && glueR){ host.dataset.glue='1'; host.appendChild(nx); }
    });
    n.replaceWith(frag);
  });
}

/* ─────────── 6. AUDIT ─────────── */
function desc(e){ const t=(e.textContent||'').replace(/⁠/g,'').replace(/\s+/g,' ').trim().slice(0,28); return '<'+e.tagName.toLowerCase()+(e.classList&&e.classList.length?'.'+[...e.classList].filter(c=>c!=='on').join('.'):'')+'> '+t; }
function runAudit(open){
  const issues=[], add=(i,rule,msg,el)=>issues.push({slide:i+1,rule,msg,el});
  const ids={}; document.querySelectorAll('[id]').forEach(e=>{ ids[e.id]=(ids[e.id]||0)+1; });
  Object.keys(ids).forEach(k=>{ if(ids[k]>1) add(-1,'D5',`id "${k}" 중복 ${ids[k]}개`); });
  if(!window.katex) add(-1,'M1','KaTeX를 불러오지 못함 (인터넷 연결 확인) — 수식이 원문으로 보입니다');
  slides.forEach((s,i)=>{
    const act=s.classList.contains('active'); if(!act) s.classList.add('measure');
    const steps=groups(s).flat(), was=steps.map(e=>e.classList.contains('on')); steps.forEach(e=>e.classList.add('on'));
    const sr=s.getBoundingClientRect(), k=sr.width/W, safe={l:sr.left+24*k,r:sr.right-24*k,t:sr.top+56*k,b:sr.bottom-40*k};
    const flagged=[];
    s.querySelectorAll('*').forEach(e=>{
      if(e.closest('.band')||e.closest('[data-audit="skip"]')) return;
      if(e instanceof SVGElement && !(e instanceof SVGSVGElement)) return;
      if(e.closest('foreignObject')) return;
      if(e.closest('.katex') && !e.classList.contains('katex')) return;
      if(flagged.some(f=>f.contains(e))) return;
      const r=e.getBoundingClientRect(); if(r.width<1&&r.height<1) return;
      if(r.left<safe.l-1||r.right>safe.r+1||r.top<safe.t-1||r.bottom>safe.b+1){ flagged.push(e); add(i,'D8','영역 밖으로 넘침: '+desc(e),e); }
    });
    s.querySelectorAll('.formula,td,th,.answer,.note,.card,.stage,.chk').forEach(e=>{ if(e.scrollWidth>e.clientWidth+2) add(i,'T4','칸 안 넘침: '+desc(e),e); });
    s.querySelectorAll('.katex').forEach(e=>{ if(!e.closest('svg') && e.getClientRects().length>1) add(i,'T2','수식 줄바꿈: '+desc(e),e); });
    s.querySelectorAll('.katex-error').forEach(e=>add(i,'M1','KaTeX 오류: '+(e.getAttribute('title')||e.textContent),e));
    s.querySelectorAll('svg').forEach(svg=>{ const R=svg.getBoundingClientRect(); svg.querySelectorAll('foreignObject.texfo > div').forEach(d=>{ const r=d.getBoundingClientRect(); if(r.width<1&&r.height<1) return; if(r.left<R.left-1||r.right>R.right+1||r.top<R.top-1||r.bottom>R.bottom+1) add(i,'D8','그림 라벨 잘림: '+desc(d),d); }); });
    // D8 그림 라벨끼리 겹침(일부러 겹친 라벨 — 단계에서 덮어쓰는 라벨, 자석 N/S처럼 붙인 글자 — 은 data-overlap="ok"로 뺀다): 같은 SVG 안 라벨 사각형이 가로·세로 모두 3px(무대 기준) 넘게 겹치면 경고 (KaTeX 상자는 위아래가 넉넉해 3px까지는 봐줌)
    s.querySelectorAll('svg').forEach(svg=>{ if(svg.closest('[data-audit="skip"]')) return;
      const labs=[...svg.querySelectorAll('foreignObject.texfo > div')].filter(d=>d.closest('svg')===svg && !d.closest('[data-overlap="ok"]')).map(d=>({d,r:d.getBoundingClientRect()})).filter(x=>x.r.width>=1&&x.r.height>=1&&getComputedStyle(x.d).visibility!=='hidden');
      const txt=d=>{ const c=d.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(z=>z.remove()); return (c.textContent||'').replace(/⁠/g,'').replace(/\s+/g,' ').trim().slice(0,14); };
      for(let a=0;a<labs.length;a++) for(let b=a+1;b<labs.length;b++){ const A=labs[a].r,B=labs[b].r;
        const ox=(Math.min(A.right,B.right)-Math.max(A.left,B.left))/k, oy=(Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top))/k;
        if(ox>3&&oy>3) add(i,'D8',`그림 라벨 겹침: "${txt(labs[a].d)}" ↔ "${txt(labs[b].d)}" (${ox.toFixed(0)}×${oy.toFixed(0)}px)`,labs[a].d); } });
    // 3.2 글자 크기: 그림 라벨이 화면(무대 1280×720 기준)에서 실제로 보이는 크기 — 16px 미만이면 경고(권장 18px 이상)
    { const small=[]; s.querySelectorAll('svg text, svg foreignObject.texfo > div').forEach(t=>{
        if(t.closest('.katex')||t.closest('[data-audit="skip"]')) return;
        const fo=t.tagName.toLowerCase()==='div'; if(!fo&&t.closest('foreignObject')) return;
        if(!(t.textContent||'').replace(/⁠/g,'').trim()) return;
        const r=t.getBoundingClientRect(); if(r.width<1&&r.height<1) return;
        const m=(fo?t.parentNode:t).getScreenCTM(); if(!m) return;
        const px=parseFloat(getComputedStyle(t).fontSize)*Math.hypot(m.a,m.b)/k; if(px<15.95) small.push({t,px}); });
      if(small.length){ small.sort((a,b)=>a.px-b.px); add(i,'3.2',`그림 라벨 ${small.length}개가 화면에서 16px 미만(가장 작은 것 ${small[0].px.toFixed(1)}px — 16px 이상, 권장 18px): `+small.slice(0,3).map(x=>{ const c=x.t.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(z=>z.remove()); return '"'+(c.textContent||'').replace(/⁠/g,'').replace(/\s+/g,' ').trim().slice(0,14)+'"'; }).join(', '),small[0].t); } }
    const tw=document.createTreeWalker(s,NodeFilter.SHOW_TEXT); while(tw.nextNode()){ const n=tw.currentNode; if(n.parentElement.closest('.katex-mathml')) continue; if(/[₀-₉⁰-⁹]/.test(n.nodeValue)) add(i,'M1','유니코드 첨자: '+n.nodeValue.trim().slice(0,24),n.parentElement); }
    { const tw2=document.createTreeWalker(s,NodeFilter.SHOW_TEXT), FORM=/(?<![A-Za-z])(?:[A-Z][a-z]?\d*){1,8}(?:\((?:aq|s|l|g)\))?[+\-−]?(?![A-Za-z0-9])/g;   // C1 화학식·이온을 \ce{} 밖 본문 글자로 씀(H2O, Na+, CO2(g))
      while(tw2.nextNode()){ const n=tw2.currentNode, pe=n.parentElement; if(!pe||pe.closest('.katex,.katex-mathml,script,style,output,textarea,[data-audit="skip"],.band')) continue;
        const v=n.nodeValue.replace(/⁠/g,''), hit=(v.match(FORM)||[]).find(t=>/[A-Za-z]\d/.test(t)||/[A-Za-z)][+\-−]$/.test(t)); if(hit) add(i,'C1',`화학식·이온을 \\ce{} 밖 글자로 씀("${hit}"): `+v.trim().slice(0,24),pe); } }
    s.querySelectorAll('annotation').forEach(a=>{ if(a.textContent.indexOf('·')>=0) add(i,'M2','수식 안 가운뎃점(·): '+a.textContent,a.closest('.katex')); });
    s.querySelectorAll('*').forEach(e=>{ if(e instanceof SVGElement||e.closest('.katex')||e.closest('foreignObject')) return; const d=getComputedStyle(e).display; if(!/flex|grid/.test(d)) return;
      for(const c of e.childNodes){ if((c.nodeType===3&&c.nodeValue.replace(/⁠/g,'').trim())||(c.nodeType===1&&c.classList.contains('w'))){ add(i,'T5','flex·grid 요소에 텍스트 직접 포함: '+desc(e),e); break; } } });
    // S9 정답 강조 누락: "→"로 시작하고 바로 뒤가 굵은 글씨나 수식인 정답 단계에 .ans가 없음 (tools/ans_mark.py로 변환)
    s.querySelectorAll('.step').forEach(e=>{ if(e.matches('.answer')||e.closest('.answer')||e.querySelector('.ans')) return;
      const norm=x=>(x||'').replace(/[\s⁠ ]/g,''), plain=x=>{ const c=x.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(z=>z.remove()); return c.textContent; };
      const t=norm(plain(e)); if(t[0]!=='→') return;
      const cand=[...e.querySelectorAll('b,strong,.katex')].find(x=>!x.closest('.katex-mathml')&&!(x.matches('b,strong')&&x.closest('.katex'))); if(!cand||(cand.matches('b,strong')&&cand.className)) return;   // 색 클래스 굵은 글씨(O/X 색 구분)는 이미 강조됨
      const ct=norm(plain(cand)); if(ct && t.slice(1).startsWith(ct.slice(0,Math.min(4,ct.length)))) add(i,'S9','정답 강조 누락(→ 뒤 답에 .ans 없음): '+desc(e),e); });
    if(s.querySelectorAll('.answer').length>1 && !s.querySelector('.board') && s.dataset.tpl!=='check') add(i,'S2','정답이 2개 이상인데 판서 공간이 없음 (제안)');
    steps.forEach((e,j)=>e.classList.toggle('on',was[j])); if(!act) s.classList.remove('measure');
  });
  window.__audit=issues.map(x=>({slide:x.slide,rule:x.rule,msg:x.msg}));
  console.log('[AUDIT] '+issues.length+'건 '+JSON.stringify(window.__audit));
  const list=document.querySelector('#audit .list'); list.innerHTML='';
  if(!issues.length){ const ok=document.createElement('div'); ok.className='ok'; ok.textContent='점검 0건 — 문제가 발견되지 않았습니다.'; list.appendChild(ok); }
  issues.forEach(x=>{ const d=document.createElement('div'); d.className='it'; const r=document.createElement('span'); r.className='rule'; r.textContent=x.rule; d.append(r,document.createTextNode((x.slide>0?x.slide+'번: ':'전체: ')+x.msg));
    d.addEventListener('click',()=>{ if(x.slide>0){ closeOverlays(); show(x.slide-1,'all'); if(x.el){ x.el.classList.add('flash'); setTimeout(()=>x.el.classList.remove('flash'),2200); } } }); list.appendChild(d); });
  if(open){ closeOverlays(); document.getElementById('audit').classList.add('open'); }
  return issues;
}

/* ─────────── 파이프라인: KaTeX → texSVG → keepWords → (audit) ─────────── */
async function pipeline(){
  if(window.renderMathInElement){ try{ renderMathInElement(deck,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false,ignoredTags:['script','noscript','style','textarea','pre','code','option','output']}); }catch(e){ console.error(e); } }
  await texSVG();
  keepWords(deck);
  readyHooks.forEach(f=>{ try{ f(); }catch(e){ console.error(e); } });
  // 본문 웹 글꼴까지 다 불러온 뒤 준비 완료(점검·캡처가 글꼴 바뀌기 전 줄바꿈으로 재지 않게, 최대 3초)
  if(document.fonts) await Promise.race([document.fonts.ready,new Promise(r=>setTimeout(r,3000))]);
  window.__ready=true;
  if(EDIT) editPost({type:'ready',N});
  if(params.has('audit')) setTimeout(()=>runAudit(true),300);
}
if(document.readyState==='complete') pipeline(); else addEventListener('load',pipeline);

window.Harness={show,next,prev,audit:runAudit,inkStrokes:i=>strokes[i==null?cur:i],onShow:f=>showHooks.push(f),N,cur:()=>cur,steps:i=>groups(slides[i]).length};
})();
