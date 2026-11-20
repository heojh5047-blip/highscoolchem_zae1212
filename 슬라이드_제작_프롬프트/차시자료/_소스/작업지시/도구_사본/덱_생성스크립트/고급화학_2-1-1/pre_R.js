(()=>{const r=document.querySelector('[data-lab="ac211gasR"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
L('idle '+o('big')+' '+o('msg'));
q('[data-act="run"]').click();L('run1 '+o('big')+' | '+o('msg'));
q('[data-act="run"]').click();L('run2 '+o('big'));
set('m',1.00);set('t',20);set('pa',745);q('[data-act="run"]').click();L('run3 m1 20C 745 '+o('big')+' | '+o('msg'));
const c=q('[data-i="corr"]');c.checked=false;c.dispatchEvent(new Event('change'));q('[data-act="run"]').click();L('nocorr '+o('big')+' | '+o('msg'));
L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);})()
