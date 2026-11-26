(()=>{const r=document.querySelector('[data-lab="em19dive"]');const o=k=>r.querySelector(`[data-o="${k}"]`).textContent;
const set=(k,v)=>{const i=r.querySelector(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
console.warn('LAB air40 '+o('p')+' | '+o('msg'));
r.querySelector('[data-act="rec"]').click();
r.querySelector('[data-gas="tri"]').click(); set('d',70); set('xo',17); set('xh',60);
console.warn('LAB tri70 '+o('p')+' xn '+o('xn')+' | '+o('msg'));
r.querySelector('[data-act="rec"]').click();
set('xh',90); console.warn('LAB clamp xh '+o('xh')+' xn '+o('xn'));
console.warn('LAB rows '+r.querySelectorAll('[data-o="log"] tr').length+' : '+r.querySelector('[data-o="log"]').textContent);
})()
