(()=>{const r=document.querySelector('[data-lab="ac241vpl"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const T=[20,30,40,50,60,70,80];
['w','s','n'].forEach(s=>{q(`[data-s="${s}"]`).click();T.forEach(t=>{set('t',t);q('[data-act="rec"]').click();});});
L('after80 '+o('big')+' | '+o('msg'));
L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);
q('[data-act="gd"]').click();L('gd '+o('msg'));
q('[data-act="gb"]').click();L('gb '+o('msg'));
q('[data-s="s"]').click();set('m',1.0);[20,50,80].forEach(t=>{set('t',t);q('[data-act="rec"]').click();});L('s1.0 '+o('msg'));
L('circles '+r.querySelectorAll('.lab-fig svg circle').length);
})()
