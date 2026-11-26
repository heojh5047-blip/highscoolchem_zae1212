(()=>{const r=document.querySelector('[data-lab="ac221vp"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
L('idle '+o('big')+' | '+o('msg'));
[20,30,40,50,60,70,80].forEach(t=>{set('t',t);q('[data-act="rec"]').click();});
L('rows '+q('[data-o="log"]').children.length+' big '+o('big')+' last '+q('[data-o="log"]').lastElementChild.textContent);
set('t',100);L('t100 '+o('big')+' | '+o('msg'));q('[data-act="rec"]').click();L('after100 rows '+q('[data-o="log"]').children.length);
q('[data-act="cc"]').click();L('cc '+o('msg'));
q('[data-liq="ethanol"]').click();[20,40,60].forEach(t=>{set('t',t);q('[data-act="rec"]').click();});L('eth '+o('msg'));
q('[data-liq="ether"]').click();[10,20,30,40].forEach(t=>{set('t',t);q('[data-act="rec"]').click();});L('ether '+o('msg'));
q('[data-liq="water"]').click();const c=q('[data-i="air"]');c.checked=true;c.dispatchEvent(new Event('change'));set('t',50);L('air50 '+o('big')+' | '+o('msg'));
L('circles '+r.querySelectorAll('.lab-fig svg circle').length);
})()
