(()=>{const sl=[...document.querySelectorAll('.slide')]; const r=sl.find(s=>s.querySelector('[data-lab="rm21metal"]')).querySelector('.lab');
const o=k=>r.querySelector(`[data-o="${k}"]`).textContent;
const c=(a,v)=>r.querySelector(`[data-${a}="${v}"]`).click();
const out=[];
[['Zn','Cu'],['Cu','Zn'],['Mg','Ag'],['Cu','Ag'],['Ag','Ag']].forEach(([m,s])=>{c('m',m);c('s',s);out.push(`${m}/${s}: ${o('rx')} | ${o('ox')} | ${o('rd')} | ${o('msg')} | eq=${r.querySelector('[data-ov="eq"]').textContent.slice(0,40)}`); r.querySelector('[data-act="rec"]').click();});
out.push('rows='+r.querySelectorAll('[data-o="log"] tr').length);
r.querySelector('[data-act="reset"]').click(); out.push('after reset rows='+r.querySelectorAll('[data-o="log"] tr').length+' m='+o('ox'));
out.forEach(x=>console.warn('LAB '+x));})()
