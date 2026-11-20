(()=>{const r=document.querySelector('[data-lab="ac241col"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
L('ag0 '+o('big')+' | '+o('msg'));q('[data-act="rec"]').click();
q('[data-s="cu"]').click();L('cu '+o('big')+' | '+o('msg'));q('[data-act="rec"]').click();
q('[data-s="ag"]').click();set('n',2);L('ag2 '+o('msg'));q('[data-act="rec"]').click();
set('n',6);L('ag6 '+o('big')+' | '+o('msg'));
const c=q('[data-i="later"]');c.checked=true;c.dispatchEvent(new Event('change'));L('ag6later '+o('big')+' | '+o('msg'));q('[data-act="rec"]').click();
q('[data-s="milk"]').click();L('milk '+o('big'));
L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);
})()
