(async()=>{const w=ms=>new Promise(f=>setTimeout(f,ms));
let r=document.querySelector('[data-lab="em44conc"]');let q=s=>r.querySelector(s);
const o=k=>q(`[data-o="${k}"]`).textContent;
for(const k of [1,2,3,4]){ q(`[data-w="${k}"]`).click(); q('[data-act="run"]').click(); await w([0,3.66,1.7,0.85,0.5][k]*1000+1500);
 console.warn(`LAB conc w${k} vol=${o('vol')} rc=${o('rc')} clk=${o('clk')} rate=${o('rate')}`); }
console.warn('LAB conc rows='+q('[data-o="log"]').children.length+' log='+o('log')+' msg='+o('msg')+' pts='+r.querySelectorAll('svg')[1].querySelectorAll('circle').length);
})()
