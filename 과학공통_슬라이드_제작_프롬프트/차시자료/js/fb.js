// Firebase(로그인 + Realtime Database) 연결. 주소 뒤에 ?local 을 붙이면 Firebase 없이 이 브라우저 안(localStorage)에서
// 시험 모드로 동작한다(로그인 단추 = 시험용 관리자). 시험 모드의 수정은 그 브라우저에만 남고 학생에게는 보이지 않는다.
const FB_VER = '10.12.2';
const LOCAL = new URLSearchParams(location.search).has('local');

function localDB() {
  const K = 'chemSlides:';
  const read = p => { try { const v = localStorage.getItem(K + p); return v == null ? null : JSON.parse(v); } catch (e) { return null; } };
  const write = (p, v) => { try { v == null ? localStorage.removeItem(K + p) : localStorage.setItem(K + p, JSON.stringify(v)); } catch (e) { } };
  let user = read('__user'); const subs = [];
  return {
    mode: 'local',
    onUser(cb) { subs.push(cb); cb(user); },
    async signIn() { user = { email: (window.SITE_CONFIG.ADMIN_EMAILS || ['admin@local'])[0], displayName: '시험용 관리자' }; write('__user', user); subs.forEach(f => f(user)); },
    async signOut() { user = null; write('__user', null); subs.forEach(f => f(user)); },
    async get(path) {
      if (path.split('/').length === 1) {   // 묶음 읽기(meta 등)
        const out = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k.startsWith(K + path + '/')) out[k.slice((K + path + '/').length)] = read(k.slice(K.length)); }
        return Object.keys(out).length ? out : null;
      }
      return read(path);
    },
    async set(path, val) { write(path, val); },
    async remove(path) { write(path, null); },
    async push(path, val) { write(path + '/' + Date.now(), val); },
    now() { return Date.now(); }
  };
}

async function firebaseDB() {
  const cfg = window.SITE_CONFIG.firebaseConfig;
  const app = await import(`https://www.gstatic.com/firebasejs/${FB_VER}/firebase-app.js`);
  const auth = await import(`https://www.gstatic.com/firebasejs/${FB_VER}/firebase-auth.js`);
  const db = await import(`https://www.gstatic.com/firebasejs/${FB_VER}/firebase-database.js`);
  const a = app.initializeApp(cfg);
  const A = auth.getAuth(a), D = db.getDatabase(a);
  return {
    mode: 'firebase',
    onUser(cb) { auth.onAuthStateChanged(A, u => cb(u ? { email: u.email, displayName: u.displayName, verified: u.emailVerified } : null)); },
    async signIn() { await auth.signInWithPopup(A, new auth.GoogleAuthProvider()); },
    async signOut() { await auth.signOut(A); },
    async get(path) { const s = await db.get(db.ref(D, path)); return s.exists() ? s.val() : null; },
    async set(path, val) { await db.set(db.ref(D, path), val); },
    async remove(path) { await db.remove(db.ref(D, path)); },
    async push(path, val) { await db.push(db.ref(D, path), val); },
    now() { return db.serverTimestamp(); }
  };
}

let _fb = null;
export async function getFB() {
  if (_fb) return _fb;
  const cfg = window.SITE_CONFIG || {};
  const unset = !cfg.firebaseConfig || /여기에|프로젝트ID/.test(JSON.stringify(cfg.firebaseConfig));
  if (LOCAL) return (_fb = localDB());
  if (unset) { const f = localDB(); f.mode = 'unset'; return (_fb = f); }
  try { return (_fb = await firebaseDB()); }
  catch (e) { console.error('[fb] Firebase를 불러오지 못함', e); const f = localDB(); f.mode = 'offline'; return (_fb = f); }
}
export function isAdmin(user) {
  if (!user || !user.email) return false;
  const list = (window.SITE_CONFIG.ADMIN_EMAILS || []).map(s => s.trim().toLowerCase());
  return list.includes(user.email.toLowerCase());
}
export const IS_LOCAL = LOCAL;
