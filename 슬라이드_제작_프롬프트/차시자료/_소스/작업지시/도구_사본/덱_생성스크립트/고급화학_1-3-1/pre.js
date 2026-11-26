(()=>{const r=document.querySelector('[data-lab="ac131bond"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`);
const rep=t=>console.warn('LAB '+t+' | v2='+o('v2').textContent+' | v3='+o('v3').textContent+' | rows='+o('log').children.length+' | paths='+r.querySelectorAll('svg path').length+' | msg='+o('msg').textContent.slice(0,60));
rep('init');q('[data-h="sp2"]').click();rep('sp2');q('[data-h="sp"]').click();rep('sp');
q('[data-m="mol"]').click();q('[data-p="NH3"]').click();rep('NH3');q('[data-act="rec"]').click();rep('rec NH3');
q('[data-p="C2H4"]').click();q('[data-act="rec"]').click();q('[data-act="rec"]').click();rep('rec C2H4 x2');
q('[data-p="H2O"]').click();q('[data-act="rec"]').click();console.warn('LAB log: '+o('log').textContent);
q('[data-act="graph"]').click();rep('graph');})()
