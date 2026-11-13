(()=>{const r=document.querySelector('[data-lab="em13bp"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const per=q('[data-i="per"]');const rec=q('[data-act="rec"]');
const W=(m)=>console.warn('LAB '+m);
q('[data-g="16"]').click(); per.value=2; per.dispatchEvent(new Event('input')); W('16족2주기 bp='+o('bp')+' mw='+o('mw')+' kind='+o('kind'));
rec.click(); per.value=3; per.dispatchEvent(new Event('input')); W('16족3주기 bp='+o('bp')); rec.click();
per.value=4; per.dispatchEvent(new Event('input')); rec.click(); per.value=5; per.dispatchEvent(new Event('input')); rec.click();
W('rows='+q('[data-o="log"]').children.length+' msg='+o('msg'));
q('[data-act="ext"]').click(); W('ext msg='+o('msg'));
q('[data-g="14"]').click(); per.value=2; per.dispatchEvent(new Event('input')); W('14족2 bp='+o('bp')+' kind='+o('kind'));
q('[data-act="all"]').click(); W('all rows='+q('[data-o="log"]').children.length+' msg='+o('msg'));
q('[data-act="ext"]').click(); q('[data-act="ext"]').click();
const v=document.querySelector('[data-lab="em13vp"]');const vo=k=>v.querySelector(`[data-o="${k}"]`).textContent;
const t=v.querySelector('[data-i="t"]'),P=v.querySelector('[data-i="P"]');
t.value=50; t.dispatchEvent(new Event('input')); W('vp t50 P1 nb='+vo('nb')+' tb='+vo('tb'));
v.querySelector('[data-pp="2"]').click(); t.value=110; t.dispatchEvent(new Event('input')); W('vp t110 P2 nb='+vo('nb')+' msg='+vo('msg'));
v.querySelector('[data-pp="0.7"]').click(); t.value=95; t.dispatchEvent(new Event('input')); W('vp t95 P0.7 nb='+vo('nb')+' msg='+vo('msg'));
})()
