(async()=>{const r=document.querySelector('[data-lab="em41rate"]');const q=s=>r.querySelector(s);const w=ms=>new Promise(f=>setTimeout(f,ms));
const out=()=>['val','avg','ins','v0'].map(k=>k+'='+q(`[data-o="${k}"]`).textContent).join(' | ');
q('[data-act="run"]').click(); await w(7000); console.warn('LAB run1 '+out());
q('[data-act="rec"]').click();
const c=q('[data-i="c"]'); c.value=0.4; c.dispatchEvent(new Event('input')); q('[data-act="run"]').click(); await w(7000);
console.warn('LAB run2 '+out()); q('[data-act="rec"]').click();
const t=q('[data-i="t"]'); t.value=1500; t.dispatchEvent(new Event("input")); console.warn('LAB t1500 '+out());
q('[data-s="C"]').click(); q('[data-act="run"]').click(); await w(7000); q('[data-act="rec"]').click(); console.warn('LAB conc '+out());
console.warn('LAB rows='+q('[data-o="log"]').children.length+' pts='+r.querySelectorAll('svg')[1].querySelectorAll('circle').length+' msg='+q('[data-o="msg"]').textContent);
})()
