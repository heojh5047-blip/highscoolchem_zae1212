(()=>{const r=document.querySelector('[data-lab="cm223dipole"]');const o=k=>r.querySelector(`[data-o="${k}"]`).textContent;
const out=[];['NH3','CH4','CO2','H2O','BCl3','CH3Cl','HCN','CH2O','H2','HF'].forEach(m=>{r.querySelector(`[data-m="${m}"]`).click();const pre=o('pol');r.querySelector('[data-act="add"]').click();r.querySelector('[data-act="rec"]').click();out.push(m+':'+pre+'>'+o('sum')+'/'+o('pol'));});
console.warn('LAB '+out.join(' | ')+' rows='+r.querySelectorAll('[data-o="log"] tr').length);
const f=document.querySelector('[data-lab="cm223field"]');const q=k=>f.querySelector(`[data-o="${k}"]`).textContent;const res=[];
f.querySelector('[data-m="HF"]').click();res.push(q('arr'));f.querySelector('[data-i="on"]').click();res.push(q('arr')+' '+q('deg'));f.querySelector('[data-act="rec"]').click();f.querySelector('[data-act="flip"]').click();res.push(q('fld')+' '+q('deg'));f.querySelector('[data-act="rec"]').click();f.querySelector('[data-m="F2"]').click();res.push(q('arr')+' '+q('deg'));f.querySelector('[data-act="rec"]').click();
console.warn('LAB field '+res.join(' | ')+' rows='+f.querySelectorAll('[data-o="log"] tr').length);})()
