(async()=>{const w=ms=>new Promise(f=>setTimeout(f,ms));
let r=document.querySelector('[data-lab="em44temp"]');let q=s=>r.querySelector(s);
const o=k=>q(`[data-o="${k}"]`).textContent;
for(const T of ['1.8','18','40']){ q(`[data-p="${T}"]`).click(); q('[data-act="run"]').click(); await w(9000);
 console.warn(`LAB temp T=${o('T')} clk=${o('clk')} rate=${o('rate')} on=${q('[data-p].on')&&q('[data-p].on').dataset.p}`); }
const sl=q('[data-i="T"]'); sl.value=30; sl.dispatchEvent(new Event('input')); q('[data-act="run"]').click(); await w(9000);
console.warn('LAB temp rows='+q('[data-o="log"]').children.length+' log='+o('log')+' msg='+o('msg'));
})()
