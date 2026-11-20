(()=>{ const r=document.querySelector('[data-lab="rm31fg"]'); const q=s=>r.querySelector(s); const o=k=>q(`[data-o="${k}"]`).textContent;
 const snap=t=>console.warn('LAB '+t+' | '+o('name')+' | '+q('[data-x="mf"]').textContent.replace(/\s+/g,'').slice(0,60)+' | '+o('bp')+' | '+q('[data-ov="tube"]').textContent+' | '+o('msg'));
 const c=s=>q(s).click(); const n=q('[data-i="n"]'); const setn=v=>{n.value=v; n.dispatchEvent(new Event('input'));};
 snap('초기 에탄올'); c('[data-act="rec"]'); snap('기록 전 확인');
 c('[data-act="water"]'); c('[data-act="btb"]'); snap('에탄올 물+BTB'); c('[data-act="rec"]');
 c('[data-f="COOH"]'); c('[data-act="water"]'); c('[data-act="btb"]'); c('[data-act="soda"]'); snap('아세트산'); c('[data-act="rec"]');
 c('[data-f="CHO"]'); c('[data-act="water"]'); c('[data-act="btb"]'); snap('아세트알데하이드'); c('[data-act="rec"]');
 c('[data-f="none"]'); c('[data-act="water"]'); c('[data-act="btb"]'); snap('에테인'); c('[data-act="rec"]');
 c('[data-f="OH"]'); setn(6); c('[data-act="water"]'); c('[data-act="btb"]'); snap('헥산올'); c('[data-act="rec"]');
 setn(1); c('[data-f="COOH"]'); snap('폼산(물 전)');
 console.warn('LAB 기록행 '+q('[data-o="log"]').children.length+' : '+[...q('[data-o="log"]').children].map(tr=>tr.textContent.replace(/\s+/g,' ')).join(' / '));
 console.warn('LAB 그래프 점 '+q('svg').querySelectorAll('g:nth-of-type(4) > *').length);
 return 1; })()
