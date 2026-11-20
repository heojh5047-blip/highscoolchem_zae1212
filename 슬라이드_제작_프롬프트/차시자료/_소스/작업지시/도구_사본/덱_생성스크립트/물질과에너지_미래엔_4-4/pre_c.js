(async()=>{const w=ms=>new Promise(f=>setTimeout(f,ms));
let r=document.querySelector('[data-lab="em44cat"]');let q=s=>r.querySelector(s);
const o=k=>q(`[data-o="${k}"]`).textContent;
for(const c of ['none','ki','h3po4']){ q(`[data-c="${c}"]`).click(); q('[data-act="run"]').click(); if(c==='ki'){ await w(3000); console.warn('LAB mid v='+o('v')); await w(8000);} else await w(11000);
 console.warn(`LAB cat ${c} ea=${o('ea')} fr=${o('fr')} v=${o('v')} m=${o('m')}`); }
q('[data-c="ki"]').click();
console.warn('LAB cat rows='+q('[data-o="log"]').children.length+' log='+o('log')+' msg='+o('msg').replace(/\n/g,' / '));
})()
