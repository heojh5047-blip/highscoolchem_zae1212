(async()=>{const r=document.querySelector('[data-lab="em42half"]');const q=s=>r.querySelector(s);const w=ms=>new Promise(f=>setTimeout(f,ms));
const out=()=>['c','t','now','h1','h2'].map(k=>k+'='+q(`[data-o="${k}"]`).textContent).join(' | ');
q('[data-act="run"]').click(); await w(2500); console.warn('LAB mid '+out()+' box='+r.querySelector('svg[data-v="box"]').textContent);
await w(5000); console.warn('LAB run1 '+out()); q('[data-act="rec"]').click();
const c=q('[data-i="c"]'); c.value=0.05; c.dispatchEvent(new Event('input')); q('[data-act="run"]').click(); await w(7000);
console.warn('LAB run2 '+out()); q('[data-act="rec"]').click(); console.warn('LAB msg2 '+q('[data-o="msg"]').textContent);
q('[data-r="A"]').click(); q('[data-act="run"]').click(); await w(7000); q('[data-act="rec"]').click();
console.warn('LAB runA '+out()+' rows='+q('[data-o="log"]').children.length+' pts='+r.querySelector('svg[data-v="g"]').querySelectorAll('circle').length+' msg='+q('[data-o="msg"]').textContent);
})()
