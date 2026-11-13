(()=>{ const r=document.querySelector('[data-lab="rm32bre"]'); const q=s=>r.querySelector(s); const o=k=>q(`[data-o="${k}"]`).textContent;
 const c=s=>q(s).click(); const N=q('[data-i="n"]'); const setN=v=>{N.value=v; N.dispatchEvent(new Event('input'));};
 const snap=t=>console.warn('LAB '+t+' | t='+o('t')+' L='+o('L')+' | '+o('msg').slice(0,60));
 const run=(s,n)=>{ c(`[data-s="${s}"]`); setN(n); c('[data-act="rec"]'); snap(s+n+' 기록전'); c('[data-act="go"]'); r._step(20); snap(s+n+' 20s'); r._step(200); snap(s+n+' 끝'); c('[data-act="rec"]'); };
 run('eth',2); run('eth',4); run('eth',6); run('ald',4); run('ace',4); run('wat',4);
 console.warn('LAB 기록행 '+q('[data-o="log"]').children.length+' : '+[...q('[data-o="log"]').children].map(tr=>tr.textContent.replace(/\s+/g,' ')).join(' / '));
 return 1; })()
