(()=>{const r=document.querySelector('[data-lab="em22sensor"]');const o=k=>r.querySelector(`[data-o="${k}"]`).textContent;const m=r.querySelector('[data-i="m"]');
const set=v=>{m.value=v;m.dispatchEvent(new Event('input'))};const c=s=>r.querySelector(s).click();const out=[];
c('[data-act="reset"]');
['b','f'].forEach(x=>{c(`[data-x="${x}"]`);[0,0.5,1,1.5].forEach(v=>{set(v);c('[data-act="run"]');c('[data-act="rec"]');out.push(x+v+':'+o('T')+'/'+o('dT'))});out.push('msg='+o('msg'));});
out.push('rows='+r.querySelectorAll('tbody[data-o="log"] tr').length+' pts='+r.querySelectorAll('svg circle[r="6"], svg rect[width="12"]').length+' kb='+r.querySelector('[data-ov="kb"]').textContent+' kf='+r.querySelector('[data-ov="kf"]').textContent);
console.warn('LAB '+out.join(' | '));})()
