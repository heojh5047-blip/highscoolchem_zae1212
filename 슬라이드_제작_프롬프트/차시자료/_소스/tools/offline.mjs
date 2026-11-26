// 덱 HTML → 교실용(오프라인) HTML. 변환 규칙은 편집기와 같은 app/offline.js 를 그대로 쓴다.
// 사용: node offline.mjs <덱.html> <출력_교실용.html>      (build.py --offline 이 부른다)
// KaTeX는 차시자료/vendor/katex-<버전>/ 사본을 읽고, 본문 글꼴은 Google Fonts(text=)에서 받는다(인터넷 필요).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SITE = path.resolve(HERE, '..', '..');                 // 차시자료
const { buildOffline } = await import(pathToFileURL(path.join(SITE, 'app', 'offline.js')).href);
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36';   // woff2를 받으려면 최신 브라우저로 보여야 함
const cache = new Map();
async function fetchBuf(url) {
  if (cache.has(url)) return cache.get(url);
  let buf;
  if (/^https?:/.test(url)) {
    const r = await fetch(url, { headers: { 'User-Agent': UA } });
    if (!r.ok) throw new Error(`${r.status} ${url}`);
    buf = Buffer.from(await r.arrayBuffer());
  } else buf = fs.readFileSync(path.join(SITE, url));
  cache.set(url, buf); return buf;
}
const get = { text: async u => (await fetchBuf(u)).toString('utf8'), b64: async u => (await fetchBuf(u)).toString('base64') };

const [inp, out] = process.argv.slice(2);
if (!inp || !out) { console.error('사용: node offline.mjs <덱.html> <출력.html>'); process.exit(2); }
const html = fs.readFileSync(inp, 'utf8');
const res = await buildOffline(html, get);
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, res, 'utf8');
console.log(`교실용 ${path.basename(out)} (${Math.round(res.length / 1024)} KB)`);
