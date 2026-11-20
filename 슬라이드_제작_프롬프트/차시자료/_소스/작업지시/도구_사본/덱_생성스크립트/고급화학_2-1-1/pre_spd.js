(()=>{const r=document.querySelector('[data-lab="ac211spd"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const setT=v=>{const i=q('[data-i="T"]');i.value=v;i.dispatchEvent(new Event('input'));};
const L=s=>console.warn('LAB '+s);
setT(200);L('N2 200 '+o('big'));q('[data-act="pin"]').click();q('[data-act="rec"]').click();
setT(300);L('N2 300 '+o('big'));q('[data-act="rec"]').click();
setT(600);L('N2 600 '+o('big')+' | '+o('msg'));q('[data-act="rec"]').click();
q('[data-gas="He"]').click();setT(300);L('He 300 '+o('big'));q('[data-act="rec"]').click();
q('[data-gas="CO2"]').click();L('CO2 300 '+o('big'));
L('rows '+q('[data-o="log"]').children.length+' paths '+r.querySelectorAll('.lab-fig path').length);
L('row1 '+q('[data-o="log"]').children[0].textContent);})()
