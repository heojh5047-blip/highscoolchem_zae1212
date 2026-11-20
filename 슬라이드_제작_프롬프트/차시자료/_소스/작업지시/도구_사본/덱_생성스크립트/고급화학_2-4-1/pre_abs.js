(()=>{const r=document.querySelector('[data-lab="ac241abs"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
L('idle '+o('big')+' | '+o('msg'));
q('[data-act="scan"]').click();L('scan '+o('msg'));
set('lam',800);L('800 '+o('big'));
[0.1,0.2,0.3,0.4,0.5].forEach(c=>{q(`[data-c="${c}"]`).click();q('[data-act="rec"]').click();});L('cal800 '+o('msg'));
set('lam',600);[0.1,0.2,0.3,0.4,0.5].forEach(c=>{q(`[data-c="${c}"]`).click();q('[data-act="rec"]').click();});
q('[data-c="u"]').click();q('[data-act="rec"]').click();L('cal600 '+o('msg'));
L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);
L('circles '+r.querySelectorAll('.lab-fig svg circle').length);
})()
