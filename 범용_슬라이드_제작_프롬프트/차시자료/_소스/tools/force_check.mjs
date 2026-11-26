// 힘 화살표 작용점 점검: 움직이는 물체(data-anim: move·rot·scale·pop·spin)에 꼬리(작용점)나 머리가 닿아 있는데
//   그 움직임 묶음 밖에 있는 화살표(data-arw)를 찾는다 — 움직이는 동안 화살표가 물체에서 떨어져 보이는 곳.
//   꼬리가 닿으면 '꼬리', 머리만 닿으면 '머리'(미는 힘 등 — 그림에 따라 판단).
// 사용: node force_check.mjs [덱 이름 일부…]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { launch } from './평가/cdp.mjs';
const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const pats = process.argv.slice(2);
const PAD = +(process.env.PAD || 16);   // 물체 경계에서 몇 px까지 '닿음'으로 볼지
const decks = [];
for (const subj of fs.readdirSync(SITE, { withFileTypes: true }).filter(d => d.isDirectory() && !/^(_|완성본$|교실용$|vendor$|app$|thumbs$)/.test(d.name)).map(d => d.name).sort())
  for (const f of fs.readdirSync(path.join(SITE, subj)).filter(f => f.endsWith('.html')).sort())
    if (!pats.length || pats.some(p => (subj + '/' + f).includes(p))) decks.push(path.join(SITE, subj, f));
const c = await launch();
let total = 0;
for (const f of decks) {
  await c.send('Page.navigate', { url: pathToFileURL(f).href + '?still' });
  let ready = false;
  for (let i = 0; i < 300 && !ready; i++) { await c.sleep(100); try { ready = await c.evaluate('window.__ready===true'); } catch {} }
  const r = await c.evaluate(`(()=>{ const out=[]; const MOV=['move','rot','scale','pop','spin'];
    for(let i=0;i<Harness.N;i++){ Harness.show(i,'all'); const s=document.querySelectorAll('#deck > section.slide')[i];
      const movs=[...s.querySelectorAll('[data-anim]')].filter(e=>MOV.includes(e.dataset.anim)&&!e.closest('[data-flow]'));
      if(!movs.length) continue;
      // 단계 순서: 단계 묶음(data-g 또는 단계 자신)의 문서 순서. -1 = 처음부터 보임/슬라이드가 보일 때 시작
      const keys=[]; s.querySelectorAll('.step').forEach(st=>{ const k=st.dataset.g||st; if(!keys.includes(k)) keys.push(k); });
      const ord=el=>{ const st=el.closest('.step'); if(!st) return -1; return keys.indexOf(st.dataset.g||st); };
      const startOrd=e=>{ const on=e.dataset.on||''; if(on.startsWith('g:')) return keys.indexOf(on.slice(2)); if(on==='step'&&e.closest('.step')) return ord(e); return ord(e); };
      const LOOP=e=>e.dataset.anim==='spin'||['loop','alt','swing','damp'].includes(e.dataset.rep||'');
      s.querySelectorAll('[data-arw]').forEach(g=>{ if(g.closest('[data-flow]')) return;
        const a=g.dataset.arw.split(',').map(Number), m=g.getScreenCTM(); if(!m) return;
        const P=(x,y)=>new DOMPoint(x,y).matrixTransform(m), t=P(a[0],a[1]), h=P(a[2],a[3]);
        for(const e of movs){ if(e.contains(g)||g.contains(e)) continue; if(e.ownerSVGElement!==g.ownerSVGElement&&e!==g.ownerSVGElement) continue;
          // 화살표를 품은 다른 움직임 묶음이 같은 움직임이면(같이 움직임) 통과
          const b=e.getBoundingClientRect(); if(!b.width&&!b.height) continue; const pad=${PAD};
          const inB=p=>p.x>=b.left-pad&&p.x<=b.right+pad&&p.y>=b.top-pad&&p.y<=b.bottom+pad;
          const D=s.getBoundingClientRect(), big=b.width*b.height>D.width*D.height*.25; if(big) continue;   // 그림 전체를 움직이는 큰 묶음은 제외
          const k=inB(t)?'꼬리':inB(h)?'머리':null; if(!k) continue;
          if(!LOOP(e)&&ord(g)>startOrd(e)) continue;   // 물체 움직임이 끝난 뒤 단계에서 나타나는 화살표는 문제 없음
          const num=(v,d)=>v==null||v===''?d:+v;
          if(!LOOP(e)&&ord(g)===startOrd(e)&&g.dataset.delay!=null&&num(g.dataset.delay,0)>=num(e.dataset.delay,0)+num(e.dataset.dur,1.2)-.05) continue;   // 화살표 data-delay로 움직임이 끝난 뒤 나타남
          const mine=g.closest('[data-anim]'); if(mine&&MOV.includes(mine.dataset.anim)&&(mine.dataset.dur||'')===(e.dataset.dur||'')&&(mine.dataset.delay||'')===(e.dataset.delay||'')&&(mine.dataset.on||'')===(e.dataset.on||'')&&(mine.dataset.rep||'')===(e.dataset.rep||'')) continue;   // 화살표가 같은 시간표로 움직이는 자기 묶음 안에 있음(물체와 함께 감)
          out.push({s:i+1,t:s.dataset.title||'',k,anim:e.dataset.anim+(e.dataset.from?'('+e.dataset.from+')':''),arw:g.dataset.arw}); break; }
      }); }
    return out; })()`, true);
  const name = path.relative(SITE, f).replace(/\\/g, '/');
  total += r.length;
  if (r.length) { console.log(`${name}  ${r.length}곳`); for (const x of r) console.log(`    ${x.s}번 ${x.t}: ${x.k} — ${x.anim} · arw ${x.arw}`); }
}
c.close();
console.log(`\n덱 ${decks.length}개 · 떨어져 보일 수 있는 화살표 ${total}곳`);
process.exit(0);
