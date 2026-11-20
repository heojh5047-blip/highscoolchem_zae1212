(()=>{const r=document.querySelector('[data-lab="em49dose"]');const O=k=>r.querySelector(`[data-o="${k}"]`).textContent;
const sl=r.querySelector('[data-i="tau"]');const rep=t=>console.warn('LAB '+t+' | '+O('tau')+' '+O('n')+' max '+O('mx')+' min '+O('mn')+' on '+O('on')+' | '+O('msg')+' | rows '+r.querySelectorAll('[data-o="log"] tr').length);
const rec=()=>r.querySelector('[data-act="rec"]').click();
rep('기본');rec();
sl.value=1;sl.dispatchEvent(new Event('input'));rep('4h');rec();
sl.value=4;sl.dispatchEvent(new Event('input'));rep('12h');rec();
sl.value=2;sl.dispatchEvent(new Event('input'));rep('6h');
r.querySelector('[data-s="1"]').click();rep('6h 가루');
sl.value=3;sl.dispatchEvent(new Event('input'));rep('8h 가루');rec();
r.querySelector('[data-act="reset"]').click();rep('초기화');})()
