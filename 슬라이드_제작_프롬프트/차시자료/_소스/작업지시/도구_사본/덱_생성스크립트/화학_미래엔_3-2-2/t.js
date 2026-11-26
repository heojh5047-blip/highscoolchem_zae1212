(()=>{const r=document.querySelector('[data-lab="cm322temp"]');const q=s=>r.querySelector(s);
const st=()=>q('[data-o="q"]').textContent+' | '+q('[data-o="msg"]').textContent;
const rows=()=>[...q('[data-o="log"]').rows].map(t=>t.textContent.replace(/\s+/g,' ')).join(' / ');
const liq=()=>r.querySelectorAll('svg path')[1].getAttribute('fill');
const info=()=>[...r.querySelectorAll('svg text')].map(t=>t.textContent).filter(x=>x.includes('°C'))[0];
const pts=()=>r.querySelectorAll('svg circle[r="6"]').length;
console.warn('LAB co0: '+st()+' fill '+liq()+' info '+info());
for(let i=0;i<4;i++) q('[data-act="ca"]').click(); console.warn('LAB ca4: '+st()+' info '+info());
q('[data-t="0"]').click(); console.warn('LAB ice: '+st()+' info '+info());
q('[data-t="80"]').click(); console.warn('LAB hot: '+st()+' info '+info());
const sl=q('[data-i="t"]'); sl.value=40; sl.dispatchEvent(new Event('input')); q('[data-act="dip"]').click(); console.warn('LAB dip40: '+st()+' tv '+q('[data-o="tv"]').textContent);
console.warn('LAB corows: '+rows()+' pts '+pts());
q('[data-mode="no2"]').click(); console.warn('LAB n0: '+st()+' info '+info());
q('[data-t="80"]').click(); console.warn('LAB n80: '+st()+' info '+info());
q('[data-t="0"]').click(); console.warn('LAB n0C: '+st()+' info '+info());
console.warn('LAB nrows: '+rows()+' pts '+pts());
q('[data-act="reset"]').click(); console.warn('LAB reset rows='+q('[data-o="log"]').rows.length+' pts '+pts()+' '+st());
})()
