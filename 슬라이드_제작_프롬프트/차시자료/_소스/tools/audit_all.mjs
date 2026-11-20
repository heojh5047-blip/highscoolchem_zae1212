// 차시자료 아래 모든 과목 폴더(화학_미래엔 등, _로 시작하는 폴더 제외)의 덱을 헤드리스 Chrome으로 열어 Harness.audit(false) 결과를 모은다.
// 사용: node audit_all.mjs [--json 출력.json] [--rule D8] [덱 이름 일부…]
// 열기 전에 *{transition:none!important}를 넣고, 모든 슬라이드를 Harness.show(i,'all')로 펼친 뒤 점검한다.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { launch } from './평가/cdp.mjs';

const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const argv = process.argv.slice(2);
const jsonOut = argv.includes('--json') ? argv[argv.indexOf('--json') + 1] : null;
const ruleF = argv.includes('--rule') ? argv[argv.indexOf('--rule') + 1] : null;
const pats = argv.filter((a, i) => !a.startsWith('--') && argv[i - 1] !== '--json' && argv[i - 1] !== '--rule');
const decks = [];
for (const subj of fs.readdirSync(SITE, { withFileTypes: true }).filter(d => d.isDirectory() && !/^(_|교실용$|vendor$|app$|thumbs$)/.test(d.name)).map(d => d.name).sort())
  for (const f of fs.readdirSync(path.join(SITE, subj)).filter(f => f.endsWith('.html')).sort())
    if (!pats.length || pats.some(p => (subj + '/' + f).includes(p))) decks.push(path.join(SITE, subj, f));

const c = await launch();
const all = [];
for (const f of decks) {
  c.consoleMsgs.length = 0;
  await c.send('Page.navigate', { url: pathToFileURL(f).href });
  let ready = false;
  for (let i = 0; i < 300 && !ready; i++) { await c.sleep(100); try { ready = await c.evaluate('window.__ready===true'); } catch {} }
  const r = await c.evaluate(`(async()=>{
    const st=document.createElement('style'); st.textContent='*{transition:none!important}'; document.head.appendChild(st);
    for(let i=0;i<Harness.N;i++) Harness.show(i,'all');
    await document.fonts.ready;
    const iss=(Harness.audit(false)||[]).map(x=>({slide:x.slide,rule:x.rule,msg:x.msg}));
    return {N:Harness.N, issues:iss};
  })()`, true);
  const name = path.relative(SITE, f).replace(/\\/g, '/');
  const iss = r.issues.filter(x => !ruleF || x.rule === ruleF);
  all.push({ deck: name, N: r.N, issues: iss, console: c.consoleMsgs.slice() });
  console.log(`${name.padEnd(44)} ${String(r.N).padStart(3)}장  점검 ${iss.length}건${c.consoleMsgs.length ? '  콘솔 ' + c.consoleMsgs.length : ''}`);
  for (const x of iss) console.log(`    ${x.slide}번 [${x.rule}] ${x.msg}`);
}
c.close();
if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(all, null, 1), 'utf8');
const tot = all.reduce((a, d) => a + d.issues.length, 0);
console.log(`\n덱 ${all.length}개, 점검 합계 ${tot}건, 콘솔 오류 덱 ${all.filter(d => d.console.length).length}개`);
process.exit(0);
