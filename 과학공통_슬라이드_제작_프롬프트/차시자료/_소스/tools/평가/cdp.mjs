// 공용: 헤드리스 Chrome 시작 + CDP 연결 (render.mjs 와 같은 방식)
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

export async function launch(width = 1280, height = 720) {
  const CHROME = process.env.CHROME || ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find(p => fs.existsSync(p));
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const udd = fs.mkdtempSync(path.join(os.tmpdir(), 'pfcdp-'));
  const proc = spawn(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check',
    '--remote-debugging-port=0', `--user-data-dir=${udd}`, `--window-size=${width},${height}`, '--force-device-scale-factor=1', 'about:blank'], { stdio: ['ignore', 'ignore', 'ignore'] });
  let port;
  for (let i = 0; i < 150 && !port; i++) { try { port = fs.readFileSync(path.join(udd, 'DevToolsActivePort'), 'utf8').split('\n')[0].trim(); } catch {} if (!port) await sleep(100); }
  let target;
  for (let i = 0; i < 50 && !target; i++) { try { const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); target = list.find(t => t.type === 'page'); } catch {} if (!target) await sleep(100); }
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  let idc = 0; const pending = new Map(); const consoleMsgs = [];
  const listeners = [];
  ws.onmessage = ev => {
    const m = JSON.parse(ev.data);
    if (m.method) for (const fn of listeners) fn(m.method, m.params);
    if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.rej(new Error(p.method + ': ' + m.error.message)) : p.res(m.result); return; }
    if (m.method === 'Runtime.consoleAPICalled' && ['error', 'warning', 'assert'].includes(m.params.type)) consoleMsgs.push(`[${m.params.type}] ` + m.params.args.map(a => a.value ?? a.description ?? '').join(' ').slice(0, 300));
    if (m.method === 'Runtime.exceptionThrown') consoleMsgs.push('[exception] ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 300));
  };
  const send = (method, params = {}) => { const id = ++idc; ws.send(JSON.stringify({ id, method, params })); return new Promise((res, rej) => pending.set(id, { res, rej, method })); };
  const evaluate = async (expr, awaitPromise = false) => { const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise }); if (r.exceptionDetails) throw new Error('evaluate 실패: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text)); return r.result.value; };
  const close = () => { try { ws.close(); } catch {} try { proc.kill(); } catch {} setTimeout(() => { try { fs.rmSync(udd, { recursive: true, force: true }); } catch {} }, 400); };
  await send('Page.enable'); await send('Runtime.enable');
  await send('Page.addScriptToEvaluateOnNewDocument', { source: 'window.__STILL=true' });   // 움직임 끄기(캡처·점검이 늘 같은 모습)
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
  return { send, evaluate, close, sleep, consoleMsgs, on: fn => listeners.push(fn) };
}
