(()=>{const r=document.querySelector('[data-lab="em23osmo"]');const o=k=>r.querySelector(`[data-o="${k}"]`).textContent;
const set=(k,v)=>{const i=r.querySelector(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'))};const c=s=>r.querySelector(s).click();const out=[];
c('[data-act="reset"]');
[[0.2,0.6],[0.4,1.0],[0,0.8]].forEach(([a,b])=>{set('a',a);set('b',b);c('[data-act="run"]');c('[data-act="rec"]');out.push(a+'/'+b+': '+o('msg'));});
out.push('rows='+r.querySelectorAll('tbody[data-o="log"] tr').length+' pts='+r.querySelectorAll('svg circle[r="6"]').length);
c('[data-v="co"]');set('a',0);set('b',0.8);c('[data-act="run"]');out.push('co: '+o('msg')+' | '+o('ctrl'));
c('[data-y="m"]');out.push('m: '+o('msg'));
c('[data-v="L"]');set('a',10);set('b',10);out.push('L same: '+o('msg'));set('b',20);out.push('L: '+o('msg'));
c('[data-v="ci"]');c('[data-y="h"]');set('a',0.2);set('b',0.6);
console.warn('LAB '+out.join(' || '));})()
