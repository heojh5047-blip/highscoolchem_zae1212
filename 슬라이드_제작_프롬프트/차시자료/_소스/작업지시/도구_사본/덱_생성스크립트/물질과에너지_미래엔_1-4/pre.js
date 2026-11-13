(()=>{const r=document.querySelector('[data-lab="em14sort"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const log=t=>console.warn('LAB '+t);
const rows=()=>[...q('[data-o="log"]').querySelectorAll('tr')].map(tr=>tr.textContent.replace(/\s+/g,' ')).join(' | ');
q('[data-s="2"]').click(); q('[data-c="2"]').click(); log('early: '+o('msg'));
for(const t of [0,1,2,3]){ q(`[data-t="${t}"]`).click(); log('NaCl t'+t+': '+o('res')); }
q('[data-c="3"]').click(); log('wrong: '+o('msg')); q('[data-c="2"]').click(); log('right: '+o('msg'));
q('[data-s="6"]').click(); q('[data-t="1"]').click(); log('graphite cond: '+o('res')); q('[data-t="0"]').click(); log('graphite ham: '+o('res'));
q('[data-c="3"]').click(); log('gra wrong: '+o('msg')); q('[data-c="1"]').click(); log('gra right: '+o('msg'));
q('[data-s="1"]').click(); q('[data-t="2"]').click(); log('sugar aq: '+o('res')); q('[data-s="0"]').click(); q('[data-t="2"]').click(); log('Cu aq: '+o('res'));
q('[data-s="7"]').click(); q('[data-t="0"]').click(); log('quartz ham: '+o('res'));
log('rows: '+rows()); log('nm: '+q('[data-ov="nm"]').textContent);
q('[data-s="2"]').click(); q('[data-t="2"]').click();
})()
