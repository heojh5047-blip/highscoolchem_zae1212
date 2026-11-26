(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="ac322gibbs"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const P=k=>q(`[data-p="${k}"]`).click();const rd=()=>`H ${o('h')} S ${o('s')} T ${o('t')} | G ${o('g')} | T* ${o('ts')} | ${o('case')}`;
L('init '+rd());L('msg '+o('msg'));
q('[data-act="pt"]').click();set('t',600);L(rd());q('[data-act="pt"]').click();
L('pts(red) '+[...r.querySelectorAll('svg circle')].filter(c=>c.getAttribute('fill')==='#D7263D').length);
q('[data-act="keep"]').click();
P('caco3');set('t',1200);L(rd());q('[data-act="pt"]').click();
P('nh3');set('t',300);L(rd());q('[data-act="pt"]').click();
P('h2o2');L(rd());P('o3');L(rd());P('br2');set('t',400);L(rd());q('[data-act="pt"]').click();
set('h',-50);set('s',50);L(rd()+' | '+o('msg'));
L('kept grey lines '+[...r.querySelectorAll('svg line')].filter(c=>c.getAttribute('stroke')==='#8C99A6').length);
L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);
q('[data-act="reset"]').click();L('reset rows '+q('[data-o="log"]').children.length+' '+rd());
})()
