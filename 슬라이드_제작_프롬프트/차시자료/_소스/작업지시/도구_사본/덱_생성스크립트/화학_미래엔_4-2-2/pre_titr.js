(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="cm422titr"]');const q=s=>r.querySelector(s);
const add=(u,k)=>{for(let i=0;i<(k||1);i++) q(`[data-add="${u}"]`).click();};
const o=k=>q(`[data-o="${k}"]`).textContent;
const show=t=>console.warn('LAB',t,'| v0',o('v0'),'| v1',o('v1'),'| dv',o('dv'),'| col',o('col'),'| rows',q('[data-o="log"]').children.length,'| msg',o('msg').slice(0,50),'| calc',o('calc'));
show('init');
add(100,3);add(20,4);show('19mL');
add(2,5);show('19.5');
while(!/연붉은/.test(o('col'))) add(1);show('end1');q('[data-act="rec"]').click();show('rec1');q('[data-act="rec"]').click();show('dup');
q('[data-act="next"]').click();show('next');add(100,4);while(!/연붉은/.test(o('col'))) add(1);q('[data-act="rec"]').click();show('rec2');
q('[data-act="next"]').click();add(100,4);while(!/연붉은/.test(o('col'))) add(1);add(1,4);show('over');q('[data-act="rec"]').click();show('rec3 over');
q('[data-act="next"]').click();add(100,4);while(!/연붉은/.test(o('col'))) add(1);q('[data-act="rec"]').click();show('rec4');
console.warn('LAB rowtxt',q('[data-o="log"]').innerText.replace(/\s+/g,' '));
q('[data-d="1"]').click();add(100,11);show('raw');
q('[data-d="10"]').click();q('[data-v="B"]').click();add(100,2);add(20,4);while(!/연붉은/.test(o('col'))) add(1);q('[data-act="rec"]').click();show('B');
q('[data-act="reset"]').click();show('reset');})()
