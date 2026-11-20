(()=>{const run=(name,fn)=>{const r=document.querySelector(`[data-lab="${name}"]`);const q=s=>r.querySelector(s);const st=()=>q('[data-o="q"]').textContent+' | '+q('[data-o="msg"]').textContent;
const rows=()=>[...q('[data-o="log"]').rows].map(t=>t.textContent.replace(/\s+/g,' ')).join(' / ');fn(r,q,st,rows);};
run('cm321conc',(r,q,st,rows)=>{console.warn('LAB c0: '+st()+' fill '+r.querySelector('svg path').getAttribute('fill'));
for(let i=0;i<4;i++) q('[data-act="oh"]').click(); console.warn('LAB c4: '+st());
q('[data-act="h"]').click(); console.warn('LAB c5: '+st()); console.warn('LAB crows: '+rows());
q('[data-sol="1"]').click(); q('[data-act="h"]').click(); console.warn('LAB chromate+H: '+st());});
run('cm321press',(r,q,st,rows)=>{console.warn('LAB p0: '+st());
const v=q('[data-i="v"]'); v.value=25; v.dispatchEvent(new Event('input')); q('[data-act="vol"]').click(); console.warn('LAB p25: '+st());
q('[data-act="hefix"]').click(); console.warn('LAB hefix: '+st());
q('[data-act="hefree"]').click(); console.warn('LAB hefree: '+st());
q('[data-mode="temp"]').click(); q('[data-t="80"]').click(); console.warn('LAB t80: '+st());
console.warn('LAB prows: '+rows()); console.warn('LAB reset rows='+q('[data-o="log"]').rows.length+' '+st());});
})()
