(()=>{let r=document.querySelector('[data-lab="em11pvnt"]');let q=s=>r.querySelector(s);
const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
q('[data-act="rec"]').click(); set('T',600); set('n',2); q('[data-act="rec"]').click();
console.warn('LAB pvnt P='+q('[data-o="P"]').textContent+' rows='+q('[data-o="log"]').children.length+' msg='+q('[data-o="msg"]').textContent);
r=document.querySelector('[data-lab="em11gasid"]');
q('[data-act="rec"]').click();
console.warn('LAB gasid nodesign msg='+q('[data-o="msg"]').textContent);
r.querySelectorAll('[data-m]').forEach(x=>x.checked=true);
q('[data-act="rec"]').click(); q('[data-act="rec"]').click();
console.warn('LAB gasid c1 msg='+q('[data-o="msg"]').textContent);
q('[data-c="2"]').click(); q('[data-act="rec"]').click(); q('[data-act="rec"]').click();
console.warn('LAB gasid c2 msg='+q('[data-o="msg"]').textContent+' rows='+q('[data-o="log"]').children.length);
r.querySelector('[data-m="pw"]').checked=false; q('[data-c="1"]').click(); q('[data-act="rec"]').click();
console.warn('LAB gasid nopw msg='+q('[data-o="msg"]').textContent+' last='+q('[data-o="log"]').lastChild.textContent);
})()
