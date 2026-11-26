// 덱 HTML 읽기 · 웹 수정본(슬라이드 부분) 끼워 넣기 · 편집 모드 준비
const SLB = '<!--SLIDES:BEGIN-->', SLE = '<!--SLIDES:END-->';

export function deckParam() {
  const d = new URLSearchParams(location.search).get('deck') || '';
  if (!/^[^/]+\/[^/]+$/.test(d) || d.includes('..')) return null;   // "<과목 키>/<파일 이름(.html 없이)>"
  return d;
}
export const deckPath = d => '/' + d.split('/').map(encodeURIComponent).join('/') + '.html';
export const dbKey = d => d.replace(/[.#$\[\]\/]/g, '_');            // Realtime Database 키로 쓸 수 없는 글자 바꿈

export async function loadDeck(d) {
  const r = await fetch(deckPath(d), { cache: 'no-cache' });
  if (!r.ok) throw new Error('덱 파일을 찾지 못함: ' + d + ' (' + r.status + ')');
  return r.text();
}
export function getSlides(html) {
  const i = html.indexOf(SLB), j = html.indexOf(SLE);
  if (i < 0 || j < i) throw new Error('덱에 SLIDES 표시가 없음(빌드한 덱이 아님)');
  return html.slice(i + SLB.length, j);
}
export function setSlides(html, slides) {
  const i = html.indexOf(SLB), j = html.indexOf(SLE);
  return html.slice(0, i + SLB.length) + slides + html.slice(j);
}
export function hash(s) {   // FNV-1a — 원본이 바뀌었는지 알아보는 용도
  let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193); }
  return (h >>> 0).toString(16);
}
export function withHead(html, extra) { return html.replace(/<head>/i, m => m + extra); }
export const editMode = html => withHead(html, '<script>window.__EDIT_MODE=true</script>');

// 엔진과 같은 규칙으로 요소 번호(data-eid)를 붙인 작업용 문서
export function parseSlides(slides) {
  const doc = new DOMParser().parseFromString('<!DOCTYPE html><html><head></head><body><div id="r">' + slides + '</div></body></html>', 'text/html');
  const root = doc.getElementById('r');
  const secs = [...root.children].filter(e => e.matches('section.slide'));
  const map = new Map();
  secs.forEach((s, i) => { map.set((i + 1) + '-0', s); [...s.querySelectorAll('*')].forEach((e, k) => map.set((i + 1) + '-' + (k + 1), e)); });
  return { doc, root, secs, map, html: () => root.innerHTML };
}

export function download(name, text) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([text], { type: 'text/html;charset=utf-8' }));
  a.download = name; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
}
