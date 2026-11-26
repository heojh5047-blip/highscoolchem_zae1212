(async()=>{const W=ms=>new Promise(r=>setTimeout(r,ms));
Harness.show(23,'all'); await W(400);
const R=document.querySelectorAll('.slide')[23].querySelector('.lab'), q=s=>R.querySelector(s), o=k=>q(`[data-o="${k}"]`).textContent.replace(/\s+/g,' ').trim();
const rows=()=>q('[data-o="log"]').querySelectorAll('tr').length;
q('[data-s="1"]').click(); console.warn('LAB th before calc', o('th'));
q('[data-act="calc"]').click(); console.warn('LAB th after calc', o('th'), '|', o('calc').slice(0,60));
q('[data-act="meas"]').click(); await W(1700); console.warn('LAB me', o('me'), 'rows', rows(), '|', o('msg').slice(0,120));
for(const i of [0,2,3]){ q(`[data-s="${i}"]`).click(); q('[data-act="calc"]').click(); q('[data-act="meas"]').click(); await W(300); console.warn('LAB', i, o('th'), o('me'));}
await W(1500); console.warn('LAB rows', rows(), '|', o('msg'));
q('[data-c="1"]').click(); q('[data-s="1"]').click(); q('[data-act="calc"]').click(); console.warn('LAB 0.01', o('th'));
q('.rm12-in').value='3.42'; q('[data-act="add"]').click(); console.warn('LAB add rows', rows(), '|', o('msg').slice(0,80));
q('[data-c="0"]').click(); q('[data-s="2"]').click(); q('[data-act="meas"]').click(); await W(1600);
console.warn('LAB final rows', rows(), q('svg').querySelectorAll('circle').length);
})()
