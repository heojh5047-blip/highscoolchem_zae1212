(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="ac321micro"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const rd=()=>`N=${o('n')} a=${o('a')} b=${o('b')} | W1 ${o('w1')} W2 ${o('w2')} P ${o('p')} dS ${o('ds')}`;
L('init '+rd());
q('[data-act="many"]').click();L('after 100 bars '+r.querySelectorAll('svg rect').length+' msg '+o('msg'));
q('[data-act="rec"]').click();
set('n',8);L(rd());q('[data-act="many"]').click();q('[data-act="many"]').click();L('msg '+o('msg'));q('[data-act="rec"]').click();
set('n',4);set('a',3);set('b',3);L(rd());q('[data-act="rec"]').click();
set('a',2);set('b',4);L(rd());q('[data-act="one"]').click();L('one shuffle msg '+o('msg'));q('[data-act="rec"]').click();
set('b',0);L(rd()+' | '+o('msg'));q('[data-act="rec"]').click();
L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);
set('n',8);set('a',5);set('b',5);L(rd());
q('[data-act="auto"]').click();L('auto btn '+q('[data-act="auto"]').textContent);q('[data-act="auto"]').click();
q('[data-act="reset"]').click();L('reset rows '+q('[data-o="log"]').children.length+' '+rd());
})()
