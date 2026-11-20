(async()=>{const r=document.querySelector('[data-lab="em43coll"]');const q=s=>r.querySelector(s);const w=ms=>new Promise(f=>setTimeout(f,ms));
const out=()=>['v','e','res'].map(k=>k+'='+q(`[data-o="${k}"]`).textContent).join(' | ');
const v=q('[data-i="v"]'); const set=x=>{v.value=x; v.dispatchEvent(new Event('input'));};
q('[data-act="go"]').click(); await w(900); console.warn('LAB mid atoms='+r.querySelector('svg[data-v="g"]').querySelectorAll('circle').length);
await w(3000); console.warn('LAB run1 '+out()+' msg='+q('[data-o="msg"]').textContent);
set(4); q('[data-act="go"]').click(); await w(5000); console.warn('LAB run2 '+out()+' msg='+q('[data-o="msg"]').textContent);
set(9); q('[data-d="b"]').click(); q('[data-act="go"]').click(); await w(4000); console.warn('LAB run3 '+out()+' msg='+q('[data-o="msg"]').textContent);
q('[data-d="c"]').click(); q('[data-act="go"]').click(); await w(4000);
console.warn('LAB run4 '+out()+' rows='+q('[data-o="log"]').children.length+' log='+q('[data-o="log"]').textContent);
q('[data-act="reset"]').click(); console.warn('LAB reset rows='+q('[data-o="log"]').children.length);
})()
