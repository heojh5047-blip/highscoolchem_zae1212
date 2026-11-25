(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="ac423titr"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const rows=()=>q('[data-o="log"]').children.length;const pts=()=>r.querySelectorAll('.lab-fig svg circle').length;
L('init v '+o('v')+' ph '+o('ph')+' n '+o('n')+' | '+o('msg'));
const add=(u,k)=>{for(let i=0;i<k;i++) q(`[data-add="${u}"]`).click();};
// HCl
add(5,4);L('HCl 20 '+o('ph')+' n '+o('n'));add(1,4);L('HCl 24 '+o('ph'));add(0.2,10);L('HCl 26 '+o('ph')+' rows '+rows()+' pts '+pts());add(5,2);L('HCl msg '+o('msg'));
// 아세트산
q('[data-a="1"]').click();L('AcOH init '+o('ph')+' prevpath '+(r.querySelectorAll('.lab-fig svg path[stroke-dasharray="6 4"]').length));
add(1,24);add(0.2,10);add(5,2);L('AcOH msg '+o('msg'));
q('[data-ind="1"]').click();L('MO '+o('msg').slice(-60)+' beaker '+r.querySelector('.lab-fig svg rect[fill^="rgb"]')?.getAttribute('fill'));
q('[data-ind="3"]').click();L('PP '+o('msg').slice(-40));
// 식초
q('[data-a="2"]').click();add(1,19);add(0.2,10);add(5,3);L('vin msg '+o('msg'));L('vin rows '+rows()+' n '+o('n')+' last '+q('[data-o="log"]').lastElementChild.textContent);


})()
