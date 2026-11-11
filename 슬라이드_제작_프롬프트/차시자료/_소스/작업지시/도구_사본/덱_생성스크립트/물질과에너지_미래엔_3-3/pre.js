(()=>{const r=document.querySelector('[data-lab="em33coin"]');const O=k=>r.querySelector(`[data-o="${k}"]`).textContent;const I=r.querySelector('[data-i="n"]');
const L=s=>console.warn('LAB '+s);
r.querySelector('[data-act="hund"]').click(); L('N4x100 tot='+O('tot')+' same='+O('same')+' th='+O('th'));
I.value=10; I.dispatchEvent(new Event('input')); r.querySelector('[data-act="hund"]').click(); L('N10x100 same='+O('same')+' th='+O('th')+' rows='+r.querySelectorAll('tbody tr').length);
r.querySelector('[data-act="one"]').click(); L('one tot='+O('tot')); L('msg='+O('msg'));
I.value=12; I.dispatchEvent(new Event('input')); r.querySelector('[data-act="hund"]').click(); L('N12 same='+O('same')+' rows='+r.querySelectorAll('tbody tr').length+' bars='+r.querySelectorAll('svg rect').length);
})()
