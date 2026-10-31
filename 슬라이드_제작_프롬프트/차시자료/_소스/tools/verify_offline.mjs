// 교실용 파일 점검: 네트워크를 끊은 헤드리스 Chrome으로 열어 외부 요청 수, KaTeX·글꼴 상태, 자동 점검 결과를 본다.
// 사용: node verify_offline.mjs <교실용.html> [더 많은 파일…]
import { pathToFileURL } from 'node:url';
import { launch } from './평가/cdp.mjs';

const files = process.argv.slice(2);
let bad = 0;
for (const f of files) {
  const c = await launch();
  const ext = [];
  c.on((m, p) => { if (m === 'Network.requestWillBeSent') { const u = p.request.url; if (!/^(file|data|blob|about):/.test(u)) ext.push(u); } });
  await c.send('Network.enable');
  await c.send('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0 });
  await c.send('Page.navigate', { url: pathToFileURL(f).href });
  let ready = false;
  for (let i = 0; i < 300 && !ready; i++) { await c.sleep(100); try { ready = await c.evaluate('window.__ready===true'); } catch {} }
  const r = await c.evaluate(`(async()=>{
    const N=Harness.N; for(let i=0;i<N;i++) Harness.show(i,'all'); Harness.show(0,'reset');
    await document.fonts.ready;
    const iss=Harness.audit(false)||[];
    const body=[...document.fonts].filter(x=>x.family.includes('IBM Plex')&&x.status==='loaded').length;
    const kx=[...document.fonts].filter(x=>x.family.includes('KaTeX')&&x.status==='loaded').length;
    return {katex:!!window.katex, kerr:document.querySelectorAll('.katex-error').length, nkatex:document.querySelectorAll('.katex').length,
            rawDollar:(document.querySelector('#deck').innerText.match(/\\$[^$\\n]{1,30}\\$/g)||[]).length, bodyFonts:body, katexFonts:kx,
            audit:iss.length, rules:iss.map(x=>x.rule+':'+(x.msg||'').slice(0,60))};
  })()`, true);
  const ok = ready && ext.length === 0 && r.katex && r.kerr === 0 && r.rawDollar === 0 && r.audit === 0;
  if (!ok) bad++;
  console.log(`${ok ? 'OK ' : '!! '} ${f.split(/[\\/]/).pop()} | 외부 요청 ${ext.length} | KaTeX ${r.katex ? '있음' : '없음'} 수식 ${r.nkatex} 오류 ${r.kerr} 원문$ ${r.rawDollar} | 글꼴 본문 ${r.bodyFonts} KaTeX ${r.katexFonts} | 점검 ${r.audit}건${r.audit ? ' ' + r.rules.slice(0, 4).join(' / ') : ''}${ext.length ? ' | ' + ext.slice(0, 3).join(' ') : ''}${c.consoleMsgs.length ? ' | 콘솔 ' + c.consoleMsgs.slice(0, 2).join(' / ') : ''}`);
  c.close();
}
process.exit(bad ? 1 : 0);
