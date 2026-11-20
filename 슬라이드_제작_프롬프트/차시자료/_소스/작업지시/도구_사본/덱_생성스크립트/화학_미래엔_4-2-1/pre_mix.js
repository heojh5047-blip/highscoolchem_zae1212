(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="cm421mix"]');const q=s=>r.querySelector(s);
const sl=q('[data-i="vb"]');const setV=v=>{sl.value=v;sl.dispatchEvent(new Event('input'));};
const vis=k=>[...r.querySelectorAll('svg g')].length;
const show=t=>console.warn('LAB',t,'| vb',q('[data-o="vb"]').textContent,'| nh',q('[data-o="nh"]').textContent,'| noh',q('[data-o="noh"]').textContent,'| nw',q('[data-o="nw"]').textContent,'| kind',q('[data-o="kind"]').textContent,'| counts',[0,1,2,3,4].map(i=>q(`[data-ov="c${i}"]`).textContent).join(','),'| rows',q('[data-o="log"]').children.length,'| msg',q('[data-o="msg"]').textContent.slice(0,70));
show('init');setV(10);show('10');q('[data-act="rec"]').click();setV(20);show('20');q('[data-act="rec"]').click();setV(40);show('40');q('[data-act="rec"]').click();
q('[data-a="2"]').click();show('H2SO4 40');setV(20);show('H2SO4 20');q('[data-va="10"]').click();show('H2SO4 10mL vb20');q('[data-act="rec"]').click();
console.warn('LAB row',q('[data-o="log"] tr:last-child').innerText.replace(/\s+/g,' '));
q('[data-act="reset"]').click();show('reset');q(`[data-a="2"]`).click();setV(40);q(`[data-act="rec"]`).click();q(`[data-act="rec"]`).click();q(`[data-act="rec"]`).click();q(`[data-act="rec"]`).click();show("final");})()
