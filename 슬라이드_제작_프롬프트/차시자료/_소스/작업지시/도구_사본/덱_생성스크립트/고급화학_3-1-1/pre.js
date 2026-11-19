(()=>{const r=document.querySelector('[data-lab="ac311piston"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const run=(p,v,qq)=>{set('p',p);set('v',v);set('q',qq);q('[data-act="rec"]').click();L(`P${p} V${v} q${qq}: ${o('big')} | ${o('msg')}`);};
run(1.2,8.5,0);run(2.0,6.0,0);run(1.0,10.0,0.5);run(0,16.0,0);run(1.2,20.0,1.46);
L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);
q('[data-m="rev"]').click();set('v',20);q('[data-act="rec"]').click();L('rev20 '+o('big')+' q:'+o('q')+' | '+o('msg'));
set('v',4);L('rev4 '+o('msg'));L('pdisabled '+q('[data-i="p"]').disabled);
q('[data-act="reset"]').click();L('reset rows '+q('[data-o="log"]').children.length+' '+o('big'));
})()
