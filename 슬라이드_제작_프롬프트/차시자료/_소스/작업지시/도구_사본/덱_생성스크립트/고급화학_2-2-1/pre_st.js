(()=>{const r=document.querySelector('[data-lab="ac221st"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
L('idle '+o('msg'));
q('[data-act="pull"]').click();L('water '+o('big')+' | '+o('msg'));
q('[data-liq="ethanol"]').click();q('[data-act="pull"]').click();L('eth '+o('big')+' | '+o('msg'));
q('[data-liq="glycerol"]').click();q('[data-act="pull"]').click();L('gly '+o('big'));
q('[data-liq="water"]').click();set('t',50);q('[data-act="pull"]').click();L('w50 '+o('big')+' | '+o('msg'));
set('r',0.4);L('r0.4 '+o('msg'));set('d',4.0);q('[data-act="pull"]').click();L('d4 '+o('big'));
L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);
})()
