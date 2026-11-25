(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="ac423buf"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const rows=k=>q(`[data-o="${k}"]`).children.length;
const add=(u,k)=>{for(let i=0;i<k;i++) q(`[data-add="${u}"]`).click();};
L('init '+o('comp')+' p0 '+o('p0')+' ph '+o('ph')+' | '+o('msg'));
add(-1,3);L('0.1 HCl3 '+o('ph')+' dp '+o('dp'));add(-1,2);L('HCl5 '+o('ph')+' dp '+o('dp')+' | '+o('msg'));
add(1,5);L('NaOH5 '+o('ph')+' dp '+o('dp')+' | '+o('msg'));
q('[data-ha="0.01"]').click();q('[data-ba="0.01"]').click();L('0.01 '+o('comp')+' p0 '+o('p0'));add(-0.1,6);add(0.1,6);L('0.01 msg '+o('msg'));
q('[data-ha="0.2"]').click();q('[data-ba="0.2"]').click();add(-1,9);add(1,9);L('0.2 msg '+o('msg'));
q('[data-ba="0.01"]').click(); q('[data-ha="0.1"]').click(); L('asym '+o('comp')+' p0 '+o('p0'));
q('[data-act="water"]').click();add(-0.1,1);L('water '+o('ph')+' | '+o('msg'));
L('log rows '+rows('log')+' cap rows '+rows('cap')+' cap: '+[...q('[data-o="cap"]').children].map(t=>t.textContent).join(' ; '));
L('curves '+r.querySelectorAll('.lab-fig svg path').length+' circles '+r.querySelectorAll('.lab-fig svg circle').length);

})()
