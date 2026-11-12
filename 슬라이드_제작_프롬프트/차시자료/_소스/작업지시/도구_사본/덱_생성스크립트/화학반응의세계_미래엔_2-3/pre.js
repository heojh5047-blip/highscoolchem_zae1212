(()=>{const r=document.querySelector('[data-lab="rm23cell"]'); const q=s=>r.querySelector(s); const o=k=>q(`[data-o="${k}"]`).textContent;
const rep=t=>console.warn('LAB '+t+' | v='+o('v')+' v5='+o('v5')+' th='+o('th')+' i='+o('i')+' rows='+q('[data-o="log"]').children.length+' pL='+q('[data-ov="pL"]').textContent+' | '+o('msg').slice(0,60));
rep('init'); q('[data-act="rec"]').click(); rep('rec1');
q('[data-l="Mg"]').click(); rep('Mg-Cu'); q('[data-act="rec"]').click();
q('[data-r="Zn"]').click(); q('[data-l="Cu"]').click(); rep('Cu-Zn(swap)');
q('[data-e="acid"]').click(); rep('acid'); q('[data-act="rec"]').click(); rep('rec3');
q('[data-e="water"]').click(); rep('water');
q('[data-e="ion"]').click(); q('[data-s="0"]').click(); rep('nobridge'); q('[data-s="1"]').click();
const d=q('[data-i="d"]'); d.value=5; d.dispatchEvent(new Event('input')); rep('d5');
q('[data-act="reset"]').click(); rep('reset');})()
