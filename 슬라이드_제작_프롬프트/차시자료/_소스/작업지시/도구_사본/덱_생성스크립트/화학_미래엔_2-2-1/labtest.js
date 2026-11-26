(()=>{const r=document.querySelector('[data-lab="cm221atom"]');const O=k=>r.querySelector(`[data-o="${k}"]`).textContent;
const c=s=>r.querySelector(s).click();const out=[];
const snap=t=>out.push(t+' | '+O('val')+' / '+O('put')+' / '+O('pairs')+' | '+O('msg').slice(0,40)+' | dots='+r.querySelectorAll('svg circle[fill="#16233D"]').length+' log='+r.querySelectorAll('[data-o="log"] tr').length);
snap('init O');c('[data-e="N"]');snap('N');for(let i=0;i<5;i++){c('[data-act="one"]');snap('N one '+(i+1));}
c('[data-act="rec"]');c('[data-e="Cl"]');c('[data-act="all"]');snap('Cl all');c('[data-act="rec"]');
c('[data-e="He"]');c('[data-act="all"]');snap('He');c('[data-act="rec"]');c('[data-e="Na"]');c('[data-act="all"]');snap('Na');
c('[data-e="B"]');c('[data-act="all"]');snap('B');c('[data-act="rec"]');snap('after rec');c('[data-act="reset"]');snap('reset');
out.forEach(l=>console.warn('LAB '+l));})()
