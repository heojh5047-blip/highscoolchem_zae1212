(()=>{const r=document.querySelector('[data-lab="rm24plate"]'); const q=s=>r.querySelector(s); const o=k=>q(`[data-o="${k}"]`).textContent;
const set=(k,v)=>{const i=q(`[data-i="${k}"]`); i.value=v; i.dispatchEvent(new Event('input'));};
const rep=t=>console.warn('LAB '+t+' | i='+o('i')+' ne='+o('ne')+' dm='+o('dm')+' da='+o('da')+' ions='+o('ions')+' rows='+q('[data-o="log"]').children.length+' pts='+q('svg.rm24-gr').querySelectorAll('g circle,g rect').length+' | '+o('msg').slice(0,90));
rep('init'); q('[data-act="rec"]').click(); rep('rec1 Ag k3 t10');
set('t',20); q('[data-act="rec"]').click(); rep('rec2 t20');
set('k',1); q('[data-act="rec"]').click(); rep('rec3 k1 t20');
q('[data-m="Cu"]').click(); set('k',3); set('t',20); q('[data-act="rec"]').click(); rep('rec4 Cu k3 t20');
set('t',10); q('[data-act="rec"]').click(); rep('rec5 Cu t10');
q('[data-b="Fe"]').click(); q('[data-m="Ag"]').click(); set('k',2); rep('Fe Ag k2 t10');
q('[data-c="p"]').click(); rep('reversed'); q('[data-act="rec"]').click(); rep('rec6 reversed');
set('t',0); rep('t0');
q('[data-act="reset"]').click(); rep('reset');})()
