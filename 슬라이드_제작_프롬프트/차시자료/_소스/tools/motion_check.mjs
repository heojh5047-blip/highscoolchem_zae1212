// 움직임 켠 상태(?motion)로 모든 덱을 열어 슬라이드·단계를 끝까지 넘기며 콘솔 오류를 모은다.
// 사용: node motion_check.mjs [덱 이름 일부…]
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
let bad = 0;
for (const f of decks) {
  c.consoleMsgs.length = 0;
  await c.send('Page.navigate', { url: pathToFileURL(f).href + '?motion' });
  let ready = false;
  for (let i = 0; i < 300 && !ready; i++) { await c.sleep(100); try { ready = await c.evaluate('window.__ready===true'); } catch {} }
  const r = await c.evaluate(`(async()=>{ const still=document.documentElement.classList.contains('still'); let n=0;
    for(let i=0;i<Harness.N;i++){ Harness.show(i,'reset'); const k=Harness.steps(i); for(let j=0;j<k;j++){ Harness.next(); n++; } await new Promise(r=>setTimeout(r,30)); }
    await new Promise(r=>setTimeout(r,400)); return {still,n,anims:document.querySelectorAll('[data-anim]').length}; })()`, true);
  const name = path.relative(SITE, f).replace(/\\/g, '/');
  if (c.consoleMsgs.length || r.still) bad++;
  console.log(`${name.padEnd(46)} 움직임 ${r.still ? '꺼짐!' : '켜짐'} · 단계 ${r.n} · data-anim ${r.anims}${c.consoleMsgs.length ? ' · 콘솔 ' + c.consoleMsgs.length + ': ' + c.consoleMsgs[0].slice(0, 160) : ''}`);
}
c.close();
console.log(`\n덱 ${decks.length}개, 문제 덱 ${bad}개`);
process.exit(0);
