(()=>{const r=document.querySelector('[data-lab="ac211mm"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const ck=(k,v)=>{const i=q(`[data-i="${k}"]`);i.checked=v;i.dispatchEvent(new Event('change'));};
q('[data-act="run"]').click();L('ipa '+o('big')+' | '+o('msg'));
ck('wet',true);q('[data-act="run"]').click();L('ipa wet '+o('big')+' | '+o('msg'));
ck('wet',false);ck('early',true);q('[data-act="run"]').click();L('ipa early '+o('big'));ck('early',false);
q('[data-s="etoh"]').click();set('v',150);q('[data-act="run"]').click();L('etoh 150 '+o('big')+' | '+o('msg'));
q('[data-s="unk"]').click();q('[data-act="run"]').click();L('unk '+o('big')+' | '+o('msg'));
L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);})()
