(()=>{const r=document.querySelector('[data-lab="em12mix"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const click=s=>q(s).click();
let out=[];out.push('init P='+o('P'));
set('nO',1);set('nN',1.5);out.push('mix P='+o('P'));
click('[data-v="O"]');out.push('Oonly P='+o('P'));click('[data-v="N"]');out.push('Nonly P='+o('P'));click('[data-v="M"]');
click('[data-act="rec"]');set('nO',0.5);set('nN',1.5);click('[data-act="rec"]');set('nO',0);set('nN',2);click('[data-act="rec"]');
out.push('rows='+q('[data-o="log"]').children.length);
[...q('[data-o="log"]').children].forEach(tr=>out.push('row '+tr.textContent.replace(/\s+/g,'|')));
out.push('msg='+o('msg'));click('[data-act="reset"]');out.push('reset rows='+q('[data-o="log"]').children.length+' P='+o('P'));
console.warn('LAB '+out.join(' ; '));})()
