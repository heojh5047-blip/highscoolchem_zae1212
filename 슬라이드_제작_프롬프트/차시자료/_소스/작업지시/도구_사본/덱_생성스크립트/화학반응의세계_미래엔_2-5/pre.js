(()=>{const r=document.querySelector('[data-lab="rm25design"]');const c=s=>r.querySelector(s).click();
const out=t=>{const g=k=>r.querySelector(`[data-o="${k}"]`).textContent;console.warn('LAB',t,'E',g('E'),'Vm',g('Vm'),'sc',[0,1,2,3,4,5].map(k=>g('s'+k)).join(','),'sus',g('sus'),'tot',g('tot'),'rows',r.querySelectorAll('[data-o="log"] tr').length,'|',g('msg'));};
out('init');c('[data-act="rec"]');out('rec1');
c('[data-u="ev"]');c('[data-n="Mg"]');c('[data-e="sol"]');c('[data-r="y"]');out('d2');c('[data-act="rec"]');out('rec2');
c('[data-u="ess"]');c('[data-n="Fe"]');c('[data-e="aq"]');out('d3');c('[data-act="rec"]');out('rec3');
c('[data-n="Mg"]');c('[data-r="n"]');out('d4');c('[data-act="rec"]');out('rec4');
c('[data-u="ph"]');c('[data-n="Zn"]');c('[data-p="Ag"]');c('[data-e="org"]');out('d5');c('[data-act="rec"]');out('rec5');
c('[data-n="H2"]');c('[data-p="O2"]');c('[data-e="sol"]');c('[data-u="ev"]');out('fuel');
c('[data-act="reset"]');out('reset');})()
