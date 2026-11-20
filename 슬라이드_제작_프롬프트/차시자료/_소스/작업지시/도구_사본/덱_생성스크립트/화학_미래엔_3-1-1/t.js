(()=>{const L=s=>console.warn('LAB '+s);
const e=document.querySelector('[data-lab="cm311eq"]'), O=k=>e.querySelector(`[data-o="${k}"]`).textContent;
const set=(k,v)=>{const i=e.querySelector(`[data-i="${k}"]`); i.value=v; i.dispatchEvent(new Event('input'));};
set('a0',40); set('b0',0); e.__test.step(30); L('eq NO2start cnt='+O('cnt')+' tot='+O('tot')+' msg='+O('msg'));
e.querySelector('[data-act="rec"]').click();
set('a0',0); set('b0',20); L('after reset cnt='+O('cnt')); e.__test.step(30); L('eq N2O4start cnt='+O('cnt')+' msg='+O('msg'));
e.querySelector('[data-act="rec"]').click(); L('log rows='+e.querySelectorAll('[data-o="log"] tr').length+' '+O('log'));
const w=document.querySelector('[data-lab="cm311water"]'), W=k=>w.querySelector(`[data-o="${k}"]`).textContent;
w.querySelector('[data-act="reset"]').click();
w.querySelector('[data-act="one"]').click(); L('w1 '+W('v')+' | '+W('mv')+' | '+W('msg'));
for(let i=0;i<4;i++) w.querySelector('[data-act="five"]').click(); L('w21 '+W('n')+' '+W('v')+' | '+W('mv')+' | '+W('msg')+' rows='+w.querySelectorAll('[data-o="log"] tr').length);
w.querySelector('[data-st="B"]').click(); for(let i=0;i<5;i++) w.querySelector('[data-act="five"]').click(); L('wB '+W('v'));
const i=w.querySelector('[data-i="db"]'); i.value=10; i.dispatchEvent(new Event('input')); for(let k=0;k<6;k++) w.querySelector('[data-act="five"]').click(); L('wEq10 '+W('v'));
})()
