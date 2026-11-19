(()=>{const r=document.querySelector('[data-lab="ac221vp"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
L('mode '+q('[data-act="cc"]').classList.contains('on')+' '+o('msg'));
[20,30,40,50,60,70,80].forEach(t=>{set('t',t);q('[data-act="rec"]').click();});L('fit '+o('msg'));
q('[data-act="reset"]').click();L('reset rows '+q('[data-o="log"]').children.length+' cc '+q('[data-act="cc"]').classList.contains('on'));
const c=q('[data-i="air"]');c.checked=true;c.dispatchEvent(new Event('change'));[20,40,60,80].forEach(t=>{set('t',t);q('[data-act="rec"]').click();});L('air '+o('msg'));
[20,40,60,80].forEach(t=>{set('t',t);q('[data-act="rec"]').click();});
})()
