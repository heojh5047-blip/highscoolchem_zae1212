(()=>{ const r=document.querySelector('[data-lab="rm33poly"]'); const q=s=>r.querySelector(s), O=k=>q(`[data-o="${k}"]`).textContent;
const out=[];
['pe','gly','pet'].forEach(s=>{ q(`[data-s="${s}"]`).click(); q('[data-act="rec"]').click(); out.push(s+' n1 M'+O('M'));
 for(let i=0;i<3;i++) q('[data-act="add"]').click(); q('[data-act="rec"]').click(); out.push('n4 w'+O('w')+' M'+O('M'));
 for(let i=0;i<5;i++) q('[data-act="add"]').click(); q('[data-act="rec"]').click(); out.push('n'+O('n')+' w'+O('w')+' M'+O('M')+' dis'+q('[data-act="add"]').disabled); });
out.push('rows '+q('[data-o="log"]').children.length+' pts '+r.querySelectorAll('svg g')[3].children.length);
out.push('atoms '+q('[data-ov="atoms"]').textContent.replace(/\s+/g,' ').slice(0,160));
console.warn('LAB '+out.join(' | ')); })()
