(()=>{const s=[...document.querySelectorAll('section.slide')][17];const L=s.querySelector('.lab');
const o=k=>L.querySelector(`[data-o="${k}"]`).textContent;const c=sel=>L.querySelector(sel).click();
const rep=t=>console.warn('LAB '+t+' | cp='+o('cp')+' mp='+o('mp')+' rows='+L.querySelectorAll('tbody tr').length+' marks='+L.querySelectorAll('svg > g:last-child > *').length+' msg='+o('msg')+' | eq='+L.querySelector('[data-ov="eq"]').textContent.slice(0,40)+' | k='+L.querySelector('[data-ov="k"]').textContent.slice(0,60));
rep('init');
c('[data-act="paper"]');rep('nopred');
c('[data-s="1"]');c('[data-p="2"]');c('[data-act="calc"]');rep('ac calc');
c('[data-act="paper"]');rep('ac paper');
c('[data-s="2"]');c('[data-p="2"]');c('[data-act="meter"]');rep('nh4 wrong meter');
c('[data-s="3"]');c('[data-c="1"]');c('[data-p="2"]');c('[data-act="calc"]');c('[data-act="meter"]');rep('hcoo 0.01 meter');
c('[data-s="4"]');c('[data-c="0"]');c('[data-p="2"]');c('[data-act="calc"]');c('[data-act="paper"]');rep('clo paper');
const r=L.querySelector('[data-i="my"]');r.value=9;r.dispatchEvent(new Event('input'));c('[data-act="mine"]');rep('mine 9');
c('[data-s="0"]');c('[data-p="1"]');c('[data-act="calc"]');c('[data-act="meter"]');rep('nacl');
console.warn('LAB rowtext '+[...L.querySelectorAll('tbody tr')].map(t=>t.textContent).join(' / '));
c('[data-act="reset"]');rep('reset');
})()
