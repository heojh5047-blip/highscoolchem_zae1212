(()=>{const r=document.querySelector('[data-lab="em11gaslaw"]');const q=s=>r.querySelector(s);
const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const rec=()=>q('[data-act="rec"]').click();
[1,2,3,4].forEach(p=>{set('P',p);rec();});
console.warn('LAB I V='+q('[data-o="V"]').textContent+' rows='+q('[data-o="log"]').children.length+' msg='+q('[data-o="msg"]').textContent);
q('[data-x="2"]').click();
[-50,27,100,200].forEach(t=>{set('t',t);rec();});
console.warn('LAB II rows='+q('[data-o="log"]').children.length+' msg='+q('[data-o="msg"]').textContent+' pts='+r.querySelectorAll('svg circle.dyn').length);
q('[data-x="3"]').click();
[0.5,1,2].forEach(n=>{set('n',n);rec();});
console.warn('LAB III V='+q('[data-o="V"]').textContent+' rows='+q('[data-o="log"]').children.length+' msg='+q('[data-o="msg"]').textContent);
q('[data-x="2"]').click();[-50,200].forEach(t=>{set('t',t);rec();});
})()
