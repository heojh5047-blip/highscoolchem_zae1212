(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="ac411fescn"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const rd=()=>`A ${o('a')} | c0 ${o('c0')} | x ${o('x')} | K ${o('k')}`;
L('init '+rd());L('msg '+o('msg'));
q('[data-act="rec"]').click();L('rec-before-cal '+o('msg')+' rows '+q('[data-o="log"]').children.length);
q('[data-act="cal"]').click();L('cal '+rd());L('msg '+o('msg'));
L('cal circles '+r.querySelectorAll('.lab-fig svg circle').length);
[1,2,3,4,5].forEach(n=>{q(`[data-n="${n}"]`).click();L('n'+n+' '+rd());q('[data-act="rec"]').click();});
L('msg25 '+o('msg'));
q('[data-t="40"]').click();[1,3,5].forEach(n=>{q(`[data-n="${n}"]`).click();L('40C n'+n+' '+rd());q('[data-act="rec"]').click();});
L('msg40 '+o('msg'));
L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);
L('K pts '+r.querySelectorAll('.lab-fig svg circle').length+' cuv '+r.querySelector('svg.ac411-app rect:nth-of-type(2)').getAttribute('fill'));

})()
