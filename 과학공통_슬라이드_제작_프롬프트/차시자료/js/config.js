// 웹사이트 설정 — 배포할 때 이 파일만 고친다 (firebase deploy 전에)
// 1) Firebase 콘솔 → 프로젝트 설정 → 내 앱(웹 </>) → SDK 설정 및 구성의 firebaseConfig 값을 그대로 붙여 넣는다.
//    databaseURL이 없으면 Realtime Database를 먼저 만든다(콘솔 → 빌드 → Realtime Database → 데이터베이스 만들기).
// 2) ADMIN_EMAILS에 관리자 구글 이메일을 넣는다(database.rules.json의 이메일과 같아야 저장된다).
// 3) 묶음 폴더의 .firebaserc에 projectId를 적는다("your-project-id" 자리).
window.SITE_CONFIG = {
  firebaseConfig: {
    // 아래 값을 모두 Firebase 콘솔의 값으로 바꾼다. "여기에"가 남아 있으면 사이트는 시험 모드(이 브라우저에만 저장)로 열린다.
    apiKey: "여기에_apiKey",
    authDomain: "your-project-id.firebaseapp.com",
    databaseURL: "여기에_databaseURL",
    projectId: "your-project-id",
    storageBucket: "your-project-id.firebasestorage.app",
    messagingSenderId: "여기에_messagingSenderId",
    appId: "여기에_appId"
  },
  ADMIN_EMAILS: ["you@example.com"],
  SITE_TITLE: "과학 수업 슬라이드",
  SCHOOL: ""          // 첫 화면 부제(학교 이름 등, 비워도 됨)
};

// 첫 화면(덱 목록) 아래쪽 출처 표시 — 수업 화면(view.html)·수정 화면(edit.html)에는 넣지 않는다.
window.SITE_CONFIG.CREDIT = ["제작: 여수고등학교 허재형"];
document.addEventListener('DOMContentLoaded', () => {
  const wrap = document.querySelector('.wrap');
  if (!wrap || !document.getElementById('tabs')) return;
  const f = document.createElement('footer');
  window.SITE_CONFIG.CREDIT.forEach(t => { const d = document.createElement('div'); d.textContent = t; f.appendChild(d); });
  f.style.cssText = 'max-width:inherit;margin:40px auto 24px;padding:14px 16px 0;border-top:1px solid #DDE3E8;text-align:center;font-size:14px;line-height:1.6;color:#5B6B7F';
  wrap.after(f);
});
