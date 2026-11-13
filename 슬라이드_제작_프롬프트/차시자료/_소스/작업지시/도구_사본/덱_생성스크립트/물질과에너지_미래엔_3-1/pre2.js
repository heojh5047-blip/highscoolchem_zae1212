(()=>{const r=document.querySelector('[data-lab="em31conv"]');const c=s=>r.querySelector(s).click();
['C8H18','C2H5OH','H2'].forEach(f=>{c(`[data-f="${f}"]`);console.warn('LAB '+f+' g='+r.querySelector('[data-o="g"]').textContent+' L='+r.querySelector('[data-o="L"]').textContent);c('[data-act="rec"]');});
c('[data-u="L"]');console.warn('LAB rows='+r.querySelectorAll('[data-o="log"] tr').length+' | '+[...r.querySelectorAll('[data-o="log"] tr')].map(t=>t.textContent).join(' / '));
console.warn('LAB msg='+r.querySelector('[data-o="msg"]').textContent);})()
