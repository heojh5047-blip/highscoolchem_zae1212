(()=>{const r=document.querySelector('[data-lab="em21heat"]');const o=k=>r.querySelector(`[data-o="${k}"]`).textContent;const t=r.querySelector('[data-i="t"]');
const set=v=>{t.value=v;t.dispatchEvent(new Event('input'))};const out=[];
['w','e','o'].forEach(s=>{r.querySelector(`[data-s="${s}"]`).click();[60,240].forEach(v=>{set(v);r.querySelector('[data-act="rec"]').click();out.push(s+v+':'+o('dt')+'/'+o('c'))})});
out.push('rows='+r.querySelectorAll('tbody[data-o="log"] tr').length+' msg='+o('msg'));
r.querySelector('[data-act="reset"]').click();out.push('after reset rows='+r.querySelectorAll('tbody[data-o="log"] tr').length);
r.querySelector('[data-s="e"]').click();set(240);r.querySelector('[data-act="rec"]').click();
console.warn('LAB '+out.join(' | '));})()
