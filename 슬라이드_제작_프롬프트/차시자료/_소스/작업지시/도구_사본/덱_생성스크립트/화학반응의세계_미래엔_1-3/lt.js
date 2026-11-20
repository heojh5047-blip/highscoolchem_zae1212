(()=>{const s=[...document.querySelectorAll('section.slide')][9];const L=s.querySelector('.lab');
const o=k=>L.querySelector(`[data-o="${k}"]`).textContent;const c=sel=>L.querySelector(sel).click();
const rep=t=>console.warn('LAB '+t+' | v='+o('v')+' ph='+o('ph')+' n='+o('n')+' rows='+L.querySelectorAll('tbody tr').length+' msg='+o('msg'));
rep('init');
c('[data-add="100"]');c('[data-add="100"]');c('[data-add="100"]');rep('15mL');
for(let i=0;i<4;i++)c('[data-add="20"]');rep('19mL');
c('[data-add="20"]');c('[data-add="20"]');c('[data-add="20"]');rep('22mL');
c('[data-a="1"]');rep('acetic start');console.warn('LAB prevpaths='+L.querySelectorAll('svg g path[stroke-dasharray="6 4"]').length);
for(let i=0;i<4;i++)c('[data-add="100"]');for(let i=0;i<2;i++)c('[data-add="20"]');rep('acetic 22');
c('[data-a="2"]');for(let i=0;i<3;i++)c('[data-add="100"]');c('[data-add="20"]');c('[data-add="20"]');rep('unknown 17');
c('[data-act="line"]');console.warn('LAB line d len='+(L.querySelector('svg > path[stroke-linejoin]')||{getAttribute:()=>''}).getAttribute('d').length);
for(let i=0;i<12;i++)c('[data-add="100"]');rep('overflow');
c('[data-act="reset"]');rep('reset');
})()
