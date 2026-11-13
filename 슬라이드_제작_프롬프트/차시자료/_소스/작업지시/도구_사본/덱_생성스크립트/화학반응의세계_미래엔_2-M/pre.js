(()=>{const r=document.querySelector('[data-lab="rm29range"]');const O=k=>r.querySelector(`[data-o="${k}"]`).textContent;const c=s=>r.querySelector(s).click();
const L=[];const rd=t=>L.push(t+': '+O('km')+' | '+O('safe'));
rd('init');c('[data-act="rec"]');
c('[data-ch="fast"]');c('[data-se="win"]');rd('fast+win');c('[data-act="rec"]');
c('[data-el="sol"]');const i=r.querySelector('[data-i="d"]');i.value=400;i.dispatchEvent(new Event('input'));rd('sol400 fast win');
c('[data-act="shock"]');rd('sol shock');c('[data-act="rec"]');
c('[data-el="liq"]');c('[data-act="shock"]');rd('liq shock');
console.warn('LAB '+L.join(' || ')+' || rows='+r.querySelectorAll('[data-o="log"] tr').length+' || msg='+O('msg'));
})()
