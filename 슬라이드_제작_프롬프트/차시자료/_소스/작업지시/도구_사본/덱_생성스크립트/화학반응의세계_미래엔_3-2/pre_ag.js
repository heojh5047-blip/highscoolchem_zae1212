(()=>{ const r=document.querySelector('[data-lab="rm32ag"]'); const q=s=>r.querySelector(s); const o=k=>q(`[data-o="${k}"]`).textContent;
 const c=s=>q(s).click(); const T=q('[data-i="T"]'); const setT=v=>{T.value=v; T.dispatchEvent(new Event('input'));};
 const snap=t=>console.warn('LAB '+t+' | t='+o('t')+' p='+o('p')+' | '+q('[data-ov="vial"]').textContent+' | '+o('msg').slice(0,70));
 const run=(s,temp,koh)=>{ c(`[data-s="${s}"]`); if(temp) setT(temp); if(koh===false) c('[data-act="koh"]'); c('[data-act="add"]'); snap(s+' 방울0 add'); for(let i=0;i<2;i++) c('[data-act="nh3"]'); snap(s+' 2방울'); c('[data-act="add"]'); snap(s+' add막힘');
   for(let i=0;i<3;i++) c('[data-act="nh3"]'); c('[data-act="add"]'); c('[data-act="heat"]'); r._step(30); snap(s+' 30s'); r._step(300); snap(s+' 300s'); c('[data-act="rec"]'); };
 run('glu',60); run('glu',80); run('ald',60); run('eth',60); run('ace',60); run('glu',60,false);
 console.warn('LAB 기록행 '+q('[data-o="log"]').children.length+' : '+[...q('[data-o="log"]').children].map(tr=>tr.textContent.replace(/\s+/g,' ')).join(' / '));
 return 1; })()
