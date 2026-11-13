(()=>{ const S=[...document.querySelectorAll('.slide')]; const lab=document.querySelector('[data-lab="cm122mg"]');
const q=s=>lab.querySelector(s), out=k=>q(`[data-o="${k}"]`).textContent, rows=()=>q('[data-o="log"]').querySelectorAll('tr').length;
const set=v=>{const i=q('[data-i="m"]'); i.value=v; i.dispatchEvent(new Event('input'));};
const run=()=>q('[data-act="run"]').click(); const L=(t)=>console.warn('LAB '+t);
set(4); L('m='+out('m')+' n='+out('n')+' vp='+out('vp')); run(); L('r1 '+out('msg')+' rows='+rows());
set(8); run(); L('r2 '+out('msg')+' rows='+rows());
q('[data-h="lo"]').click(); L('lo vp='+out('vp')); run(); L('r3 '+out('msg'));
q('[data-h="hi"]').click(); set(10); const h=q('[data-e="hot"]'); h.checked=true; h.dispatchEvent(new Event('change')); run(); L('r4 '+out('msg'));
h.checked=false; const o=q('[data-e="ox"]'); o.checked=true; o.dispatchEvent(new Event('change')); set(6); run(); L('r5 '+out('msg'));
L('table: '+[...q('[data-o="log"]').querySelectorAll('tr')].map(r=>r.textContent.replace(/\s+/g,' ')).join(' | '));
L('points='+lab.querySelectorAll('svg circle[r="5.5"]').length);
q('[data-act="reset"]').click(); L('after reset rows='+rows()+' text='+q('[data-o="log"]').textContent.slice(0,20)+' pts='+lab.querySelectorAll('svg circle[r="5.5"]').length);
set(4); run(); })()
