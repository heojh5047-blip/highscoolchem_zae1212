(()=>{const r=document.querySelector('[data-lab="ac341bridge"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const cl=s=>q(s).click(); const sl=(k,v)=>{const i=q(`[data-i="${k}"]`); i.value=v; i.dispatchEvent(new Event('input'));};
const out=[]; const rec=(t)=>{cl('[data-act="rec"]'); out.push(t+' | V '+o('v')+' I '+o('i')+' r '+o('r')+' VL '+o('vl'));};
out.push('init V '+o('v')+' I '+o('i')+' msg '+o('msg'));
cl('[data-s="0"]'); rec('없음'); cl('[data-s="1"]');
cl('[data-m="paper"]'); cl('[data-c="0"]'); rec('paper 증류수'); out.push('msg '+o('msg'));
cl('[data-c="1"]'); rec('paper 0.1'); cl('[data-c="2"]'); rec('paper 1.0');
cl('[data-m="thread"]'); rec('thread 1.0'); cl('[data-m="gel"]'); cl('[data-c="3"]'); rec('gel 포화');
out.push('msg '+o('msg')); out.push('rows '+q('[data-o="log"]').children.length);
cl('[data-m="paper"]'); cl('[data-c="2"]');
for(const c of [3,2,1,0]){ sl('cu',c); rec('Cu idx '+c+' '+o('cu')); }
out.push('msg '+o('msg'));
sl('cu',3); sl('zn',0); rec('Zn 0.0010'); 
cl('[data-act="reset"]'); out.push('reset rows '+q('[data-o="log"]').children.length+' V '+o('v'));
out.forEach(x=>console.warn('LAB '+x));})();
