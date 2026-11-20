(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="ac312hess"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const run=(e,l,c)=>{q(`[data-e="${e}"]`).click();q(`[data-l="${l}"]`).click();q(`[data-c="${c}"]`).click();q('[data-act="run"]').click();L(`${e} ${l} ${c}: ${o('tt')} | ${o('dt')} | ${o('q')} | ${o('h')}`);};
run('a','on','on');run('b','on','on');run('c','on','on');L('msg '+o('msg'));
q('[data-v="cmp"]').click();L('cmp bars '+r.querySelectorAll('svg rect').length);q('[data-v="tt"]').click();
run('a','on','off');run('b','on','off');run('c','on','off');L('msg '+o('msg'));
run('a','off','on');L('rows '+q('[data-o="log"]').children.length+' last '+q('[data-o="log"]').lastElementChild.textContent);
const i=q('[data-i="t0"]');i.value=25;i.dispatchEvent(new Event('input'));L('t0 '+o('t0')+' tt '+o('tt'));run('c','on','on');

})()
