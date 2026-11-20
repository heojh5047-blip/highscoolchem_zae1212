(()=>{const r=document.querySelector('[data-lab="cm313dir"]');const q=s=>r.querySelector(s);const st=()=>q('[data-o="q"]').textContent+' | '+q('[data-o="msg"]').textContent;
const set=(a,b)=>{const A=q('[data-i="a"]'),B=q('[data-i="b"]');A.value=a;A.dispatchEvent(new Event('input'));B.value=b;B.dispatchEvent(new Event('input'));};
console.warn('LAB def: '+st());q('[data-act="run"]').click();
set(0.02,0.10);console.warn('LAB 2: '+st());q('[data-act="run"]').click();
set(0.05,0.54);console.warn('LAB 3: '+st());q('[data-act="run"]').click();
set(0.2,0);console.warn('LAB 4: '+st());
console.warn('LAB rows '+[...q('[data-o="log"]').rows].map(t=>t.textContent.replace(/\s+/g,' ')).join(' / '));
for(let i=0;i<4;i++) q('[data-act="run"]').click(); console.warn('LAB rows7 '+q('[data-o="log"]').rows.length+' first '+q('[data-o="log"]').rows[0].cells[0].textContent);
})()
