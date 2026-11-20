(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="ac321micro"]');const q=s=>r.querySelector(s);
const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
q('[data-act="many"]').click();q('[data-act="rec"]').click();set('n',8);q('[data-act="many"]').click();q('[data-act="many"]').click();q('[data-act="rec"]').click();
set('a',2);set('b',4);q('[data-act="rec"]').click();set('n',8);set('a',5);set('b',5);q('[data-act="many"]').click();q('[data-act="rec"]').click();
console.warn('LAB msg '+q('[data-o="msg"]').textContent);})()
