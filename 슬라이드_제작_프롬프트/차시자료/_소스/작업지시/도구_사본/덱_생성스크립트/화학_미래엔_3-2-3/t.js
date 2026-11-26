(()=>{const r=document.querySelector('[data-lab="cm323nh3"]');const q=s=>r.querySelector(s);
const st=()=>q('[data-o="y"]').textContent+' | '+q('[data-o="sub"]').textContent+' | '+q('[data-o="msg"]').textContent+' | mol '+r.querySelectorAll('svg g g g').length;
const rows=()=>[...q('[data-o="log"]').rows].map(t=>t.textContent.replace(/\s+/g,' ')).join(' / ');
const set=(k,v)=>{const s=q(`[data-i="${k}"]`);s.value=v;s.dispatchEvent(new Event('input'));};
console.warn('LAB init: '+st()); q('[data-act="rec"]').click();
set('t',200);set('p',400);console.warn('LAB 200/400: '+st()); q('[data-act="rec"]').click();
set('t',300);set('p',200);console.warn('LAB 300/200: '+st()); q('[data-act="rec"]').click();
set('t',600);set('p',30);console.warn('LAB 600/30: '+st());
set('t',450);set('p',200);q('[data-act="cat"]').click();console.warn('LAB nocat: '+st()); q('[data-act="rec"]').click(); q('[data-act="rec"]').click();
console.warn('LAB rows: '+rows()+' pts '+r.querySelectorAll('svg circle[r="5"]').length);
q('[data-act="reset"]').click();console.warn('LAB reset rows='+q('[data-o="log"]').rows.length+' '+st());})()
