(async()=>{const r=document.querySelector('[data-lab="cm111nh3"]'); const sl=ms=>new Promise(f=>setTimeout(f,ms));
const set=(k,v)=>{const i=r.querySelector(`[data-i="${k}"]`); i.value=v; i.dispatchEvent(new Event('input'));};
const O=k=>r.querySelector(`[data-o="${k}"]`).textContent; const act=a=>r.querySelector(`[data-act="${a}"]`).click();
const out=[];
for(const [a,b] of [[1,3],[2,5],[4,12],[3,2]]){ set('a',a); set('b',b); out.push(`before ${a},${b}: nh3=${O('nh3')}`); act('go'); await sl(2200); act('rec');
  const vis=[...r.querySelectorAll('svg g[transform]')].filter(g=>g.style.display!=='none').length;
  out.push(`after ${a},${b}: nh3=${O('nh3')} atoms=${vis} msg=${O('msg')}`); }
out.push('rows='+r.querySelectorAll('tbody[data-o="log"] tr').length+' last='+r.querySelector('tbody[data-o="log"] tr:last-child').textContent);
act('reset'); out.push('reset rows='+r.querySelectorAll('tbody[data-o="log"] tr td[colspan]').length+' a='+O('a'));
set('a',2); set('b',7); act('go'); await sl(2200);
out.forEach(x=>console.warn('LAB '+x.slice(0,150))); return 1;})()
