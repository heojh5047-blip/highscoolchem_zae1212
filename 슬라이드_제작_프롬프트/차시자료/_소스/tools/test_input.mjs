// 넘기기(6.1)·펜(6.2) 입력 시험: 헤드리스 Chrome에 실제 마우스·터치·펜 입력(CDP Input)을 보내고 결과를 표로 낸다.
// 사용: node test_input.mjs <덱.html>
import { pathToFileURL } from 'node:url';
import { launch } from './평가/cdp.mjs';

const file = process.argv[2];
const c = await launch(1280, 720);
await c.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
async function open(q = '') {
  await c.send('Page.navigate', { url: pathToFileURL(file).href + q + '#2' });
  for (let i = 0; i < 300; i++) { await c.sleep(100); try { if (await c.evaluate('window.__ready===true')) break; } catch {} }
  await c.evaluate(`(()=>{ const s=document.createElement('style'); s.textContent='*{transition:none!important}'; document.head.appendChild(s);
    window.__pd=[]; addEventListener('pointerdown',e=>window.__pd.push([e.pointerType,e.buttons,e.button,+e.pressure.toFixed(2)]),true);
    window.__ctx=0; document.addEventListener('contextmenu',e=>{ window.__ctx++; window.__ctxPrevented=e.defaultPrevented; }); return 1; })()`);
}
const pos = () => c.evaluate(`(()=>{ const s=document.querySelectorAll('#deck > section.slide')[Harness.cur()]; return Harness.cur()*100 + s.querySelectorAll('.step.on').length; })()`);
const inkN = () => c.evaluate('Harness.inkStrokes().length');
const reset = () => c.evaluate("Harness.show(1,'reset'); (Harness.inkStrokes().length=0); 1");
// 빈 자리(제목 오른쪽 위 여백) — 무대 1280×720 이 창 1280×720 에 1:1
const X = 1100, Y = 105;
const M = (type, x, y, o = {}) => c.send('Input.dispatchMouseEvent', { type, x, y, button: o.button ?? 'left', buttons: o.buttons ?? (type === 'mouseReleased' ? 0 : 1), clickCount: 1, pointerType: o.pointerType || 'mouse', force: o.force, ...o.extra });
async function mouse(path, { hold = 0, pointerType = 'mouse', force, buttons } = {}) {
  const [x0, y0] = path[0];
  await M('mouseMoved', x0, y0, { buttons: 0, pointerType });
  await M('mousePressed', x0, y0, { pointerType, force, buttons });
  for (const [x, y, f] of path.slice(1)) { await c.sleep(16); await M('mouseMoved', x, y, { pointerType, force: f ?? force, buttons }); }
  if (hold) await c.sleep(hold);
  const [x1, y1] = path[path.length - 1];
  await M('mouseReleased', x1, y1, { pointerType, buttons: 0 });
  await c.sleep(80);
}
async function touch(path, id = 1) {
  await c.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: path[0][0], y: path[0][1], id }] });
  for (const [x, y] of path.slice(1)) { await c.sleep(16); await c.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y, id }] }); }
  await c.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await c.sleep(120);
}
const line = (x, y, dx, dy, n = 6) => Array.from({ length: n + 1 }, (_, k) => [x + dx * k / n, y + dy * k / n]);
const rows = [];
async function test(name, expect, fn) {
  await reset(); const p0 = await pos();
  const A1 = await c.evaluate('Harness.next(),1').then(pos), A2 = await c.evaluate('Harness.next(),1').then(pos);   // 한 번·두 번 넘겼을 때 자리
  await reset(); const k0 = await inkN();
  await fn();
  const p1 = await pos(), k1 = await inkN();
  const got = { move: p1 === p0 ? 0 : p1 === A1 ? 1 : p1 === A2 ? 2 : (p1 < p0 ? -1 : 9), ink: k1 - k0 };
  const ok = Object.entries(expect).every(([k, v]) => typeof v === 'function' ? v(got[k]) : got[k] === v);
  rows.push({ name, expect: JSON.stringify(expect, (k, v) => typeof v === 'function' ? String(v) : v), got: JSON.stringify(got), ok });
}

await open();
await test('마우스 짧게 클릭', { move: 1 }, () => mouse([[X, Y]]));
await test('마우스 5px 움직임(6px 이하)', { move: 1 }, () => mouse(line(X, Y, 5, 0, 2)));
await test('마우스 20px 끌기', { move: 0 }, () => mouse(line(X, Y, 20, 0)));
await test('마우스 가로 120px 끌기(스와이프 아님)', { move: 0 }, () => mouse(line(X - 200, Y, 120, 0)));
await test('마우스 700ms 길게 누름', { move: 0 }, () => mouse([[X, Y]], { hold: 700 }));
await test('글자 선택 중 놓기', { move: 0 }, async () => {
  await M('mouseMoved', X, Y, { buttons: 0 }); await M('mousePressed', X, Y);
  await c.evaluate(`(()=>{ const h=document.querySelectorAll('#deck > section.slide')[Harness.cur()].querySelector('h2'); const r=document.createRange(); r.selectNodeContents(h); getSelection().removeAllRanges(); getSelection().addRange(r); return 1; })()`);
  await M('mouseReleased', X, Y, { buttons: 0 }); await c.sleep(80); await c.evaluate('getSelection().removeAllRanges(),1');
});
await test('오른쪽 단추 클릭', { move: 0 }, async () => {
  await c.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: X, y: Y, button: 'right', buttons: 2, clickCount: 1 });
  await c.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: X, y: Y, button: 'right', buttons: 0, clickCount: 1 });
  await c.sleep(80);
});
await test('터치 짧게 탭(한 번만 넘어감)', { move: 1 }, () => touch([[X, Y]]));
await test('터치 8px 움직임(10px 이하)', { move: 1 }, () => touch(line(X, Y, 8, 0, 2)));
await test('터치 15px 움직임', { move: 0 }, () => touch(line(X, Y, 15, 0, 3)));
await test('터치 왼쪽 스와이프 120px', { move: 1 }, () => touch(line(X, Y, -120, 0)));
await test('펜 탭: 넘기지 않고 점 하나', { move: 0, ink: 1 }, () => mouse([[X, Y]], { pointerType: 'pen', force: .5 }));
await test('펜 획(압력 변화)', { move: 0, ink: 1 }, () => mouse(line(300, 600, 300, 20, 10).map(([x, y], k) => [x, y, .1 + .08 * k]), { pointerType: 'pen', force: .1 }));
const pr = await c.evaluate("(()=>{ const s=Harness.inkStrokes()[0]; if(!s) return null; return {n:s.p.length, first:s.p[0].map(v=>+(+v).toFixed(2)), last:s.p[s.p.length-1].map(v=>+(+v).toFixed(2)), c:s.c}; })()");
// CDP Input은 펜 지우개 비트(buttons 32)를 보내지 못하므로, 같은 모양의 PointerEvent를 페이지에서 직접 보낸다
await test('펜 지우개 끝(buttons 32, 합성 이벤트)', { move: 0, ink: 1 }, () => c.evaluate(`(()=>{ const el=document.querySelectorAll('#deck > section.slide')[Harness.cur()];
  const ev=(t,x,b)=>el.dispatchEvent(new PointerEvent(t,{bubbles:true,cancelable:true,composed:true,pointerId:9,pointerType:'pen',clientX:x,clientY:600,pressure:b?.5:0,buttons:b,button:t==='pointerdown'?5:-1}));
  ev('pointerdown',300,32); ev('pointermove',340,32); ev('pointermove',380,32); ev('pointerup',380,0); return 1; })()`));
const er = await c.evaluate("(()=>{ const s=Harness.inkStrokes()[0]; return s&&s.c; })()");
await test('펜이 닿은 동안 터치', { move: 0, ink: 1 }, async () => {
  await M('mouseMoved', 300, 500, { buttons: 0, pointerType: 'pen' }); await M('mousePressed', 300, 500, { pointerType: 'pen', force: .5 });
  await M('mouseMoved', 340, 500, { pointerType: 'pen', force: .5 });
  await touch([[X, Y]], 7);
  await M('mouseReleased', 340, 500, { pointerType: 'pen', buttons: 0 }); await c.sleep(80);
});
await test('펜으로 오른쪽 아래 ▶ 단추', { move: 1, ink: 0 }, async () => {
  const r = await c.evaluate("(()=>{ document.body.classList.add('ui'); const b=document.querySelector('#nav [data-a=next]').getBoundingClientRect(); return [b.left+b.width/2,b.top+b.height/2]; })()");
  await mouse([r], { pointerType: 'pen', force: .5 }); await c.sleep(50);
});
const ctx = await c.evaluate('({n:window.__ctx, prevented:window.__ctxPrevented})');
await test('P 키(펜 켬) + 마우스 끌기 = 필기', { move: 0, ink: 1 }, async () => {
  await c.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'p', text: 'p' }); await c.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'p' });
  await mouse(line(300, 600, 200, 0));
  await c.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape' }); await c.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape' });
});
// 창을 절반(640×360)으로 줄여도 획은 무대 좌표(1280×720)로 저장되는지
await c.send('Emulation.setDeviceMetricsOverride', { width: 640, height: 360, deviceScaleFactor: 1, mobile: false }); await c.sleep(300);
await test('창 640×360에서 펜 획 → 무대 좌표', { move: 0, ink: 1 }, () => mouse(line(150, 300, 100, 0), { pointerType: 'pen', force: .5 }));
const half = await c.evaluate("(()=>{ const s=Harness.inkStrokes()[0]; return s?[s.p[0].map(v=>Math.round(v)), s.p[s.p.length-1].map(v=>Math.round(v))]:null; })()");
await c.send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
await open('?pen=mouse');
await test('?pen=mouse: 마우스 끌기 = 필기', { move: 0, ink: 1 }, () => mouse(line(300, 600, 200, 0)));
await test('?pen=mouse: 마우스 클릭도 넘기지 않음', { move: 0, ink: 1 }, () => mouse([[X, Y]]));

console.log('| 시험 | 기대 | 결과 | 판정 |\n|---|---|---|---|');
for (const r of rows) console.log(`| ${r.name} | ${r.expect} | ${r.got} | ${r.ok ? '통과' : '**실패**'} |`);
console.log('\n펜 획 저장(무대 좌표·압력):', JSON.stringify(pr));
console.log('창 절반에서 (150,300)→(250,300) 펜 획의 무대 좌표:', JSON.stringify(half));
console.log('지우개 획 종류:', er, '| contextmenu:', JSON.stringify(ctx), '| 콘솔:', c.consoleMsgs.length ? c.consoleMsgs.join(' / ') : '없음');
c.close(); process.exit(rows.every(r => r.ok) ? 0 : 1);
