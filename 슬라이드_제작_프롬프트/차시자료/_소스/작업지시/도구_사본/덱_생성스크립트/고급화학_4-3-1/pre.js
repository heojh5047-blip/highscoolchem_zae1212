(()=>{const r=document.querySelector('[data-lab="ac431ord"]'); const q=s=>r.querySelector(s); const c=s=>q(s).click();
const out=()=>['rx','np','slope','r2'].map(k=>k+'='+q(`[data-o="${k}"]`).textContent).join(' | ');
const msg=()=>q('[data-o="msg"]').textContent; const L=(t)=>console.warn('LAB '+t);
c('[data-act="measure"]'); L('cv0.05 '+out());
c('[data-gr="0"]'); L('A '+q('[data-o="r2"]').textContent); c('[data-gr="2"]'); L('1/A '+q('[data-o="r2"]').textContent);
c('[data-ord="2"]'); L('wrong: '+msg());
c('[data-gr="1"]'); L('lnA '+out()); c('[data-ord="1"]'); L('ok: '+msg());
c('[data-oh="0.1"]'); c('[data-act="measure"]'); c('[data-ord="1"]'); L('oh0.1: '+out()+' || '+msg());
c('[data-rx="no2"]'); c('[data-act="measure"]'); c('[data-gr="2"]'); c('[data-ord="2"]'); L('no2: '+out()+' || '+msg());
c('[data-rx="nh3"]'); c('[data-act="measure"]'); c('[data-gr="0"]'); c('[data-ord="0"]'); L('nh3: '+out()+' || '+msg());
L('log rows '+q('[data-o="log"]').children.length+' : '+[...q('[data-o="log"]').children].map(t=>t.textContent).join(' / '));
L('ohrow off '+q('[data-o="ohrow"]').className+' pts '+r.querySelectorAll('svg circle').length);
c('[data-act="reset"]'); L('reset rows '+q('[data-o="log"]').children.length+' '+out());
c('[data-act="measure"]');
})()
