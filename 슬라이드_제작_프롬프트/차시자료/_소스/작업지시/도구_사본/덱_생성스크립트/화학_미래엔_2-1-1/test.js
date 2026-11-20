(()=>{const r=document.querySelector('[data-lab="cm211elec"]'); const q=s=>r.querySelector(s); const O=k=>q(`[data-o="${k}"]`).textContent;
const set=(k,v)=>{const i=q(`[data-i="${k}"]`); i.value=v; i.dispatchEvent(new Event('input'));};
const out=[]; const snap=l=>out.push(l+': I='+O('i')+' +='+O('vp')+' -='+O('vm')+' r='+O('r'));
snap('t0'); set('t',6); snap('t6'); q('[data-act="rec"]').click(); set('v',4.5); snap('4.5V'); q('[data-act="rec"]').click();
q('[data-act="h2"]').click(); out.push('h2:'+O('msg'));
q('[data-e="0"]').click(); set('t',10); snap('dist'); q('[data-act="rec"]').click(); q('[data-act="o2"]').click(); out.push('o2:'+O('msg'));
out.push('rows='+q('[data-o="log"]').children.length+' pts='+r.querySelectorAll('svg circle[r="6"]').length);
q('[data-act="reset"]').click(); out.push('after reset rows='+q('[data-o="log"]').children.length+' v='+O('v'));
console.warn('LAB '+out.join(' | '));})()
