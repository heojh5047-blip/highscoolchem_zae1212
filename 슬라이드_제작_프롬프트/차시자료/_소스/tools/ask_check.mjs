// '질문 강조' 점검: 모든 덱의 모든 슬라이드를 next()로 넘기며, 강조 단계마다
//   ① 강조된 것이 없음(헛누름) ② 강조 영역이 너무 큼(무대 넓이의 35% 넘음) ③ 강조 영역이 화면에 안 보임(숨은 단계 안) 을 찾는다.
// 사용: node ask_check.mjs [덱 이름 일부…]  (?motion으로 열어 도구용 정지 모드를 끔)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { launch } from './평가/cdp.mjs';
const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const pats = process.argv.slice(2);
const decks = [];
for (const subj of fs.readdirSync(SITE, { withFileTypes: true }).filter(d => d.isDirectory() && !/^(_|교실용$|vendor$|app$|thumbs$)/.test(d.name)).map(d => d.name).sort())
  for (const f of fs.readdirSync(path.join(SITE, subj)).filter(f => f.endsWith('.html')).sort())
    if (!pats.length || pats.some(p => (subj + '/' + f).includes(p))) decks.push(path.join(SITE, subj, f));
const c = await launch();
let total = 0, probs = 0;
for (const f of decks) {
  c.consoleMsgs.length = 0;
  await c.send('Page.navigate', { url: pathToFileURL(f).href + '?motion' });
  let ready = false;
  for (let i = 0; i < 300 && !ready; i++) { await c.sleep(100); try { ready = await c.evaluate('window.__ready===true'); } catch {} }
  const r = await c.evaluate(`(async()=>{ const out=[]; let asks=0; const deck=document.getElementById('deck'), D=deck.getBoundingClientRect();
    for(let i=0;i<Harness.N;i++){ Harness.show(i,'reset'); let guard=0;
      while(Harness.cur()===i && guard++<200){
        const before=document.querySelectorAll('.slide.active .step.on').length;
        if(i===Harness.N-1 && before>=document.querySelectorAll('.slide.active .step').length) break;   // 마지막 장 끝
        Harness.next(); if(Harness.cur()!==i) break;
        const asked=[...document.querySelectorAll('.slide.active .ask')];
        const after=document.querySelectorAll('.slide.active .step.on').length;
        if(after===before){   // 이번 누름은 질문 강조였음
          asks++;
          const title=(document.querySelector('.slide.active').dataset.title||'');
          if(!asked.length) out.push({s:i+1,t:title,k:'헛누름(강조 없음)'});
          for(const a of asked){ const b=a.getBoundingClientRect(); const area=b.width*b.height/(D.width*D.height);
            const vis=getComputedStyle(a).visibility!=='hidden' && !a.closest('.step:not(.on)');
            if(area>.35) out.push({s:i+1,t:title,k:'강조 영역 큼 '+Math.round(area*100)+'%',e:a.tagName+'.'+a.className});
            if(!vis) out.push({s:i+1,t:title,k:'숨은 요소를 강조',e:a.tagName+'.'+a.className}); }
        }
      } }
    return {asks,out}; })()`, true);
  const name = path.relative(SITE, f).replace(/\\/g, '/');
  total += r.asks; probs += r.out.length;
  console.log(`${name.padEnd(46)} 질문 강조 ${String(r.asks).padStart(3)}회 · 문제 ${r.out.length}${c.consoleMsgs.length ? ' · 콘솔 ' + c.consoleMsgs.length : ''}`);
  for (const x of r.out) console.log(`    ${x.s}번 ${x.t}: ${x.k}${x.e ? ' (' + x.e + ')' : ''}`);
}
c.close();
console.log(`\n덱 ${decks.length}개 · 질문 강조 ${total}회 · 문제 ${probs}건`);
process.exit(0);
