(()=>{const r=document.querySelector('[data-lab="ac111rdf"]');const q=s=>r.querySelector(s);const O=k=>q(`[data-o="${k}"]`).innerText.replace(/\n/g,' / ');
const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const ck=(k,v)=>{const i=q(`[data-i="${k}"]`);i.checked=v;i.dispatchEvent(new Event('input'));};
q('[data-act="max"]').click();console.warn('LAB 1smax',O('r'),O('rd'),O('msg'));q('[data-act="rec"]').click();
q('[data-act="node"]').click();console.warn('LAB 1snode',O('msg'));
ck('o1',false);ck('o2',true);q('[data-act="node"]').click();console.warn('LAB 2snode',O('r'),O('rd'),O('msg'));q('[data-act="rec"]').click();
q('[data-act="max"]').click();console.warn('LAB 2smax',O('r'),O('rd'));q('[data-act="rec"]').click();
set('r',9.13);console.warn('LAB 2s90',O('rd'),O('msg'));
ck('o3',true);ck('o1',true);q('[data-v="R"]').click();set('r',15);console.warn('LAB R view',O('rd'));q('[data-act="rec"]').click();
q('[data-v="P"]').click();set('r',20);console.warn('LAB 20',O('rd'));
console.warn('LAB rows',q('[data-o="log"]').children.length,O('log'));})()
