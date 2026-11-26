(()=>{const r=document.querySelector('[data-lab="cm312ratio"]');const q=s=>r.querySelector(s);const col=i=>[...q('[data-o="log"]').rows].map(t=>t.cells[i].textContent).join(',');
q('[data-k="a"]').click();q('[data-act="calc"]').click();console.warn('LAB a: '+col(3)+' | '+q('[data-o="msg"]').textContent);
q('[data-k="b"]').click();q('[data-act="calc"]').click();console.warn('LAB b: '+col(4)+' | '+q('[data-o="spread"]').textContent+' | '+q('[data-o="msg"]').textContent);
const a=q('[data-i="a0"]');a.value=0.2;a.dispatchEvent(new Event('input'));q('[data-act="meas"]').click();a.value=0.05;a.dispatchEvent(new Event('input'));q('[data-act="meas"]').click();
console.warn('LAB rows '+q('[data-o="log"]').rows.length+' new: '+[...q('[data-o="log"]').rows].slice(5).map(t=>t.textContent).join(' / ')+' | a0 '+q('[data-o="a0"]').textContent);
q('[data-k="c"]').click();q('[data-act="calc"]').click();q('[data-k="d"]').click();q('[data-act="calc"]').click();console.warn('LAB all: '+q('[data-o="msg"]').textContent);q('[data-k="b"]').click();console.warn('LAB b7: '+col(4)+' '+q('[data-o="spread"]').textContent+' '+q('[data-o="msg"]').textContent);
for(let i=0;i<5;i++) q('[data-act="meas"]').click(); console.warn('LAB rows after 7 meas '+q('[data-o="log"]').rows.length+' first6 '+q('[data-o="log"]').rows[5].cells[0].textContent);
})()
