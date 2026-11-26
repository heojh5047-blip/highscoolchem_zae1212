(()=>{const r=document.querySelector('[data-lab="em39tank"]');const o=k=>r.querySelector(`[data-o="${k}"]`).textContent;
const rep=t=>console.warn('LAB '+t+' | E='+o('E')+' pl='+o('pl')+' V='+o('V')+' msg='+o('msg')+' rows='+r.querySelectorAll('[data-o="log"] tr').length);
rep('기본');r.querySelector('[data-act="rec"]').click();
r.querySelector('[data-s="2"]').click();rep('액체');r.querySelector('[data-act="rec"]').click();
r.querySelector('[data-s="4"]').click();rep('옥테인');r.querySelector('[data-act="rec"]').click();rep('기록3');
const e=r.querySelector('[data-i="E"]');e.value=6;e.dispatchEvent(new Event('input'));rep('1e6');
r.querySelector('[data-s="1"]').click();rep('압축');r.querySelector('[data-s="3"]').click();rep('메테인');
r.querySelector('[data-act="reset"]').click();rep('초기화');})()
