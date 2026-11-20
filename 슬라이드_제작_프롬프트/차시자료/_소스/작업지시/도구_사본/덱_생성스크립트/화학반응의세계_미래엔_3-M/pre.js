(()=>{const r=document.querySelector('[data-lab="rm39mirror"]');const q=s=>r.querySelector(s);const O=k=>q(`[data-o="${k}"]`).textContent;
const T=q('[data-i="T"]');const L=m=>console.warn('LAB '+m);
const run=(t)=>{T.value=t;T.dispatchEvent(new Event('input'));q('[data-act="heat"]').click();r._step(20);L(t+'C t20 '+O('t')+' A'+O('pA')+' B'+O('pB')+' C'+O('pC'));r._step(300);q('[data-act="rec"]').click();L('msg '+O('msg').slice(0,60));};
q('[data-act="rec"]').click();L('norec '+O('msg'));
run(60);run(80);run(40);run(30);
L('rows '+q('[data-o="log"]').children.length+' | '+[...q('[data-o="log"]').children].map(tr=>tr.textContent).join(' / '));
q('[data-act="reset"]').click();L('reset rows '+q('[data-o="log"]').children.length+' T '+O('T'));
})()
