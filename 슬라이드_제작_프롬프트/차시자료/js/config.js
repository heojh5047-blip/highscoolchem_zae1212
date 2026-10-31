// 웹사이트 설정 — 배포할 때 이 파일만 고친다 (firebase deploy 전에)
// 1) Firebase 콘솔 → 프로젝트 설정 → 내 앱(웹 </>) → SDK 설정 및 구성의 firebaseConfig 값을 그대로 붙여 넣는다.
//    databaseURL이 없으면 Realtime Database를 먼저 만든다(콘솔 → 빌드 → Realtime Database → 데이터베이스 만들기).
// 2) ADMIN_EMAILS에 관리자 구글 이메일을 넣는다(database.rules.json의 이메일과 같아야 저장된다).
window.SITE_CONFIG = {
  firebaseConfig: {
    apiKey: "AIzaSyCP2tlfmB7cIc9DEaPrPXGfHycSQIZniNY",
    authDomain: "chem-high1.firebaseapp.com",
    databaseURL: "https://chem-high1-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "chem-high1",
    storageBucket: "chem-high1.firebasestorage.app",
    messagingSenderId: "900903379775",
    appId: "1:900903379775:web:902ff87ce014c77678a98a"
  },
  ADMIN_EMAILS: ["heojh5047@gmail.com"],
  SITE_TITLE: "화학 수업 슬라이드",
  SCHOOL: ""          // 첫 화면 부제(학교 이름 등, 비워도 됨)
};
