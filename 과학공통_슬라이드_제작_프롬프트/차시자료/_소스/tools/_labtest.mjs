// 헤드리스 Chrome으로 덱을 열어 자동 점검(?audit)을 돌리고, 모든 슬라이드를 "단계 모두 펼침" 상태로 캡처한다.
// 사용: node render.mjs <덱.html> <출력 폴더> [--slides=3,5-8] [--no-shots] [--steps]
//   --steps : 슬라이드마다 단계 0, 1, 2, … 상태를 각각 캡처 (단계 순서 확인용)
// 결과: <출력 폴더>/s03.png …, report.json { N, titles, audit, console }
// 표준 출력: 요약(점검 건수·콘솔 오류) — 에이전트가 읽기 좋게 짧게.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const flags = Object.fromEntries(args.filter(a => a.startsWith('--')).map(a => { const [k, v] = a.slice(2).split('='); return [k, v ?? true]; }));
const [fileArg, outArg] = args.filter(a => !a.startsWith('--'));
if (!fileArg) { console.error('사용: node render.mjs <덱.html> <출력 폴더> [--slides=3,5-8] [--no-shots] [--steps]'); process.exit(2); }
const file = path.resolve(fileArg);
const out = path.resolve(outArg || path.join(path.dirname(file), '_render', path.basename(file, '.html')));
fs.mkdirSync(out, { recursive: true });
for (const f of fs.readdirSync(out)) if (/^s\d+(-\d+)?\.png$/.test(f)) fs.unlinkSync(path.join(out, f));

const CHROME = process.env.CHROME || [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
].find(p => fs.existsSync(p));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const udd = fs.mkdtempSync(path.join(os.tmpdir(), 'hrender-'));
const proc = spawn(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check',
  '--remote-debugging-port=0', `--user-data-dir=${udd}`, '--window-size=1280,720', '--force-device-scale-factor=1', 'about:blank'],
  { stdio: ['ignore', 'ignore', 'ignore'] });

let ws, idc = 0;
const pending = new Map(), consoleMsgs = [];
function send(method, params = {}) {
  const id = ++idc;
  ws.send(JSON.stringify({ id, method, params }));
  return new Promise((res, rej) => pending.set(id, { res, rej, method }));
}
async function evaluate(expr, awaitPromise = false) {
  const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise });
  if (r.exceptionDetails) throw new Error('evaluate 실패: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
}
function cleanup(code) {
  try { ws && ws.close(); } catch {}
  try { proc.kill(); } catch {}
  setTimeout(() => { try { fs.rmSync(udd, { recursive: true, force: true }); } catch {} process.exit(code); }, 400);
}
const timer = setTimeout(() => { console.error('시간 초과(120초)'); cleanup(3); }, 120000);

try {
  let port;
  for (let i = 0; i < 150 && !port; i++) { try { port = fs.readFileSync(path.join(udd, 'DevToolsActivePort'), 'utf8').split('\n')[0].trim(); } catch {} if (!port) await sleep(100); }
  if (!port) throw new Error('Chrome 디버깅 포트를 찾지 못함');
  let target;
  for (let i = 0; i < 50 && !target; i++) { try { const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); target = list.find(t => t.type === 'page'); } catch {} if (!target) await sleep(100); }
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  ws.onmessage = ev => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.rej(new Error(p.method + ': ' + m.error.message)) : p.res(m.result); return; }
    if (m.method === 'Runtime.consoleAPICalled' && ['error', 'warning', 'assert'].includes(m.params.type)) {
      consoleMsgs.push(`[${m.params.type}] ` + m.params.args.map(a => a.value ?? a.description ?? '').join(' ').slice(0, 400));
    }
    if (m.method === 'Runtime.exceptionThrown') consoleMsgs.push('[exception] ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 400));
    if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error' && !/favicon/.test(m.params.entry.url || '')) consoleMsgs.push('[log] ' + m.params.entry.text.slice(0, 300) + (m.params.entry.url ? ' ' + m.params.entry.url : ''));
  };
  await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: pathToFileURL(file).href + '?audit' });
  let ready = false;
  for (let i = 0; i < 200 && !ready; i++) { await sleep(100); try { ready = await evaluate('window.__ready===true'); } catch {} }
  if (!ready) consoleMsgs.push('[harness] 파이프라인이 끝나지 않음(window.__ready 없음) — 스크립트 오류 가능성');
  let audit = null;
  for (let i = 0; i < 40 && audit === null; i++) { await sleep(100); try { audit = await evaluate('window.__audit||null'); } catch {} }
  const katex = await evaluate('!!window.katex');
  const N = await evaluate('window.Harness?window.Harness.N:document.querySelectorAll("#deck > section.slide").length');
  const titles = await evaluate('[...document.querySelectorAll("#deck > section.slide")].map(s=>s.dataset.title||"")');
  await evaluate(`(()=>{ const s=document.createElement('style'); s.textContent='*{transition:none!important} #nav,#hud{display:none!important}'; document.head.appendChild(s); document.querySelectorAll('.ui-overlay.open,.overlay.open').forEach(o=>o.classList.remove('open')); return 1; })()`);

  let want = [...Array(N).keys()];
  if (typeof flags.slides === 'string') {
    want = [];
    for (const part of flags.slides.split(',')) { const [a, b] = part.split('-').map(Number); for (let k = a; k <= (b || a); k++) if (k >= 1 && k <= N) want.push(k - 1); }
  }
  const shots = [];
  if (!flags['no-shots']) {
    for (const i of want) {
      const nsteps = await evaluate(`Harness.steps(${i})`);
      const states = flags.steps ? [...Array(nsteps + 1).keys()] : [null];
      for (const st of states) {
        if (st === null) await evaluate(`Harness.show(${i},'all'); 1`);
        else { await evaluate(`Harness.show(${i},'reset'); 1`); for (let k = 0; k < st; k++) await evaluate('Harness.next(); 1'); }
        if(process.env.PRE) await evaluate(process.env.PRE.replace('%I%',String(i))); await sleep(st === null ? 220 : 120);
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        const name = `s${String(i + 1).padStart(2, '0')}${st === null ? '' : '-' + st}.png`;
        fs.writeFileSync(path.join(out, name), Buffer.from(shot.data, 'base64'));
        shots.push(name);
      }
    }
  }
  const report = { file, N, katex, titles, audit, console: consoleMsgs, shots };
  fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 1), 'utf8');
  console.log(`슬라이드 ${N}장 · KaTeX ${katex ? '로드됨' : '로드 실패'} · 자동 점검 ${audit ? audit.length : '?'}건 · 콘솔 오류 ${consoleMsgs.length}건 · 캡처 ${shots.length}장 → ${out}`);
  (audit || []).forEach(a => console.log(`  [${a.rule}] ${a.slide > 0 ? a.slide + '번' : '전체'}: ${a.msg}`));
  consoleMsgs.forEach(m => console.log('  ' + m));
  clearTimeout(timer);
  cleanup(0);
} catch (e) {
  console.error('렌더 실패:', e.message);
  clearTimeout(timer);
  cleanup(1);
}
