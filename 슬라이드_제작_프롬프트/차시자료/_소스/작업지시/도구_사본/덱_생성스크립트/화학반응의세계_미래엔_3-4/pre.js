(()=>{ const r=document.querySelector('[data-lab="rm34make"]'); const q=s=>r.querySelector(s), O=k=>q(`[data-o="${k}"]`).textContent;
const ov=k=>(q(`[data-ov="${k}"]`).textContent.match(/\\ce\{[^}]*\}/g)||[q(`[data-ov="${k}"]`).textContent.replace(/\s+/g,' ')]).join(' ');
const vis=()=>[...r.querySelectorAll('svg [data-p],svg [data-r],svg [data-b]')].filter(g=>g.style.display!=='none').map(g=>g.dataset.p||g.dataset.r||g.dataset.b).join(',');
const out=[];
q('[data-act="reset"]').click(); out.push('reset: '+O('pname')+' vis='+vis());
[['aa','ia'],['ba','et'],['sa','me'],['sa','an'],['ac','hd'],['aa','hd']].forEach(([a,b])=>{
 q(`button[data-a="${a}"]`).click(); q(`button[data-b="${b}"]`).click(); const pre=O('pname');
 q('[data-act="react"]').click(); r._step(); q('[data-act="rec"]').click();
 out.push(`${a}+${b}: pre=${pre} P=${O('pname')} by=${O('by')} use=${O('use')} vis=${vis()} eq=[${ov('eq')}] mm=[${ov('mm')}]`); });
out.push('rows '+q('[data-o="log"]').children.length+' last='+q('[data-o="log"]').lastElementChild.textContent);
out.forEach(x=>console.warn('LAB '+x)); })()
