// 덱 HTML → 오프라인 단일 HTML(완성본). 인터넷이 없는 교실·연수실에서도 두 번 눌러 바로 열린다.
// 사용: node offline.mjs <덱.html> <출력.html>      (python build.py --offline 이 부른다)
//  - KaTeX(수식·화학식): _소스/vendor/katex/ 사본(CSS·JS·mhchem·auto-render·woff2 글꼴)을 파일 안에 넣는다. 인터넷 필요 없음.
//  - 본문 글꼴(IBM Plex Sans KR): 덱에 쓰인 글자만 Google Fonts에서 받아 넣는다(이때만 인터넷 필요).
//    받지 못하면 경고만 하고 컴퓨터 기본 글꼴(맑은 고딕·Apple SD 고딕 Neo 등)로 보이게 둔다.
// (범용 묶음 사본: 원본 묶음의 app/offline.js 없이 혼자 동작하도록 새로 쓴 파일)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const VENDOR = path.resolve(HERE, '..', 'vendor', 'katex');
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36';   // woff2를 받으려면 최신 브라우저로 보여야 함

const [inp, out] = process.argv.slice(2);
if (!inp || !out) { console.error('사용: node offline.mjs <덱.html> <출력.html>'); process.exit(2); }
let html = fs.readFileSync(inp, 'utf8');
const rdV = f => fs.readFileSync(path.join(VENDOR, f));
const inlineJS = s => s.replace(/<\/script/gi, '<\\/script');

// 1) KaTeX CSS: 글꼴은 woff2만 남기고 data URI로
let css = rdV('katex.min.css').toString('utf8');
css = css.replace(/src:([^;}]*)/g, (m, list) => {
  const w2 = list.match(/url\((fonts\/[^)]+\.woff2)\)/);
  if (!w2) return m;
  return `src:url(data:font/woff2;base64,${rdV(w2[1]).toString('base64')}) format("woff2")`;
});
const KX = 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/';
let nRep = 0;
html = html.replace(new RegExp(`<link rel="stylesheet" href="${KX.replace(/\./g, '\\.')}katex\\.min\\.css">`), () => (nRep++, `<style>/* KaTeX 0.16.11 (MIT) */\n${css}\n</style>`));
for (const f of ['katex.min.js', 'contrib/mhchem.min.js', 'contrib/auto-render.min.js']) {
  // defer 스크립트를 head 안의 일반 스크립트로: 순서(katex → mhchem → auto-render → 엔진)는 그대로 지켜진다
  html = html.replace(`<script defer src="${KX}${f}"></script>`, () => (nRep++, `<script>${inlineJS(rdV(f).toString('utf8'))}</script>`));
}
if (nRep !== 4) { console.error(`KaTeX 태그를 ${nRep}/4개만 찾음 — build.py로 만든 덱인지 확인`); process.exit(1); }

// 2) 본문 글꼴: 덱에 쓰인 글자만(unicode-range로 나눠 받음)
html = html.replace(/<link rel="preconnect"[^>]*>\n?/g, '');
const FONT_LINK = /<link href="https:\/\/fonts\.googleapis\.com\/css2\?family=IBM\+Plex\+Sans\+KR[^"]*" rel="stylesheet">/;
let fontNote = '';
if (FONT_LINK.test(html)) {
  const chars = [...new Set([...html].filter(ch => ch.codePointAt(0) >= 32 && ch.codePointAt(0) !== 0x2060))].sort();
  const chunks = []; for (let i = 0; i < chars.length; i += 250) chunks.push(chars.slice(i, i + 250));
  try {
    let fcss = '';
    for (const weight of [400, 500, 700]) for (const ch of chunks) {
      const url = `https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@${weight}&text=${encodeURIComponent(ch.join(''))}`;
      const r = await fetch(url, { headers: { 'User-Agent': UA } });
      if (!r.ok) throw new Error(`글꼴 CSS ${r.status}`);
      const t = await r.text();
      const m = t.match(/url\(([^)]+)\)\s*format\('([^']+)'\)/);
      if (!m) continue;
      const fr = await fetch(m[1], { headers: { 'User-Agent': UA } });
      if (!fr.ok) throw new Error(`글꼴 파일 ${fr.status}`);
      const b64 = Buffer.from(await fr.arrayBuffer()).toString('base64');
      const mime = m[2] === 'woff2' ? 'font/woff2' : m[2] === 'woff' ? 'font/woff' : 'font/ttf';
      const range = ch.map(c => 'U+' + c.codePointAt(0).toString(16).toUpperCase()).join(',');
      fcss += `@font-face{font-family:'IBM Plex Sans KR';font-style:normal;font-weight:${weight};font-display:block;src:url(data:${mime};base64,${b64}) format('${m[2]}');unicode-range:${range}}\n`;
    }
    html = html.replace(FONT_LINK, () => `<style>/* IBM Plex Sans KR (SIL OFL) — 이 덱에 쓰인 글자만 */\n${fcss}</style>`);
    fontNote = `본문 글꼴 넣음(글자 ${chars.length}개)`;
  } catch (e) {
    html = html.replace(FONT_LINK, '<!-- 본문 글꼴을 받지 못해 컴퓨터 기본 글꼴로 보임 -->');
    fontNote = `경고: 본문 글꼴을 받지 못함(${e.message}) — 컴퓨터 기본 글꼴(맑은 고딕 등)로 보입니다. 인터넷이 될 때 다시 만드세요`;
  }
}
// 3) 머리 주석의 '인터넷이 없는 교실' 안내를 완성본 안내로
html = html.replace(/  인터넷이 없는 교실:[^\n]*\n/, '  완성본(오프라인 단일 파일): 수식 글꼴·본문 글꼴이 파일 안에 들어 있어 인터넷 없이 열립니다.\n');
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, html, 'utf8');
console.log(`완성본 ${path.basename(out)} (${Math.round(html.length / 1024)} KB) · ${fontNote}`);
