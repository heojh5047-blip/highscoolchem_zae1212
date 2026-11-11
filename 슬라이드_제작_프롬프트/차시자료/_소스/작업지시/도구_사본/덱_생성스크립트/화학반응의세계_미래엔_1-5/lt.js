(()=>{const s=[...document.querySelectorAll('section.slide')][8];const L=s.querySelector('.lab');
const o=k=>L.querySelector(`[data-o="${k}"]`).textContent;const c=sel=>L.querySelector(sel).click();
const rep=t=>console.warn('LAB '+t+' | add='+o('add')+' mp='+o('mp')+' rows='+L.querySelectorAll('tbody tr').length+' pts='+L.querySelectorAll('svg > g:last-child circle').length+' parts='+L.querySelectorAll('svg > g:nth-child(2) > g').length+' msg='+o('msg'));
rep('init');
c('[data-act="meas"]');rep('water0');
c('[data-p="0"]');c('[data-add="b5"]');rep('water +5b');c('[data-act="meas"]');rep('water meas');
c('[data-s="3"]');c('[data-act="meas"]');rep('buf0');c('[data-add="b5"]');c('[data-act="meas"]');rep('buf +5b');
c('[data-add="a1"]');rep('buf a1 fresh');c('[data-act="meas"]');rep('buf a1 meas');
c('[data-act="fresh"]');c('[data-add="b5"]');c('[data-add="b5"]');c('[data-add="b5"]');c('[data-add="b5"]');c('[data-add="b5"]');c('[data-add="b5"]');c('[data-act="meas"]');rep('buf +30b');
c('[data-add="b1"]');rep('cap');
c('[data-s="2"]');c('[data-act="meas"]');c('[data-add="a5"]');c('[data-act="meas"]');rep('NaAc a5');
c('[data-s="1"]');c('[data-act="meas"]');c('[data-add="b5"]');c('[data-act="meas"]');rep('HAc b5');
const r=L.querySelector('[data-i="my"]');r.value=3.9;r.dispatchEvent(new Event('input'));c('[data-act="mine"]');rep('mine');
console.warn('LAB rowtext '+[...L.querySelectorAll('tbody tr')].map(t=>t.textContent).join(' / '));
c('[data-act="reset"]');rep('reset');
})()
