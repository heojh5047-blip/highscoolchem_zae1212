(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="ac322gibbs"]');const q=s=>r.querySelector(s);
const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
set('t',200);q('[data-act="pt"]').click();set('t',600);q('[data-act="pt"]').click();q('[data-act="keep"]').click();
q('[data-p="caco3"]').click();set('t',800);q('[data-act="pt"]').click();set('t',1300);q('[data-act="pt"]').click();
console.warn('LAB rows '+q('[data-o="log"]').children.length);})()
