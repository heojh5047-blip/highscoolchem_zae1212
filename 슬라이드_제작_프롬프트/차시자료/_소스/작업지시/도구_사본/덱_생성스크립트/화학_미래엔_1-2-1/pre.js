(()=>{const r=document.querySelector('[data-lab="cm121bal"]');
const O=k=>r.querySelector(`[data-o="${k}"]`).textContent; const act=a=>r.querySelector(`[data-act="${a}"]`).click();
const rx=k=>r.querySelector(`[data-r="${k}"]`).click();
const set=(i,v)=>{const e=r.querySelector(`[data-i="c${i}"]`); e.value=v; e.dispatchEvent(new Event('input'));};
const nat=()=>r.querySelectorAll('svg g g circle, svg circle').length;
const out=[];
const tryc=(k,cs)=>{rx(k); cs.forEach((v,i)=>set(i,v)); out.push(`${k} ${cs} atoms=${nat()} cnt=${r.querySelector('[data-o="cnt"]').textContent} msg=${O('msg').slice(0,60)} eq=${r.querySelector('[data-ov="eq"]').textContent.slice(0,40)}`); act('rec');};
tryc('w',[1,1,1]); tryc('w',[2,1,2]); tryc('w',[4,2,4]); tryc('co',[2,1,2]); tryc('nh',[1,3,2]); tryc('ch',[1,2,1,2]); tryc('wd',[2,2,1]);
out.push('ctl4 visible(ch)='+(()=>{rx('ch');return r.querySelector('[data-c="3"]').style.display;})()+' (w)='+(()=>{rx('w');return r.querySelector('[data-c="3"]').style.display;})());
out.push('rows='+r.querySelectorAll('tbody[data-o="log"] tr').length+' last='+r.querySelector('tbody[data-o="log"] tr:last-child').textContent);
act('reset'); out.push('after reset='+r.querySelector('tbody[data-o="log"]').textContent.slice(0,30));
out.forEach(x=>console.warn('LAB '+x));})()
