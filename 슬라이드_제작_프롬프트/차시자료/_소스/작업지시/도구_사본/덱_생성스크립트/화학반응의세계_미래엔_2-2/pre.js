(()=>{const r=document.querySelector('[data-lab="rm22cell"]');const o=k=>r.querySelector(`[data-o="${k}"]`).textContent;
const log=t=>console.warn('LAB '+t);
const clk=b=>r.querySelector(`[data-b="${b}"]`).click(); const rec=()=>r.querySelector('[data-act="rec"]').click();
['volta','lead','li','fuel'].forEach(b=>{clk(b);log(b+' | '+o('cls')+' | '+o('neg')+' | '+o('pos')+' | mn='+r.querySelector('[data-ov="mn"]').textContent.slice(0,20)); rec(); log('rows='+r.querySelectorAll('tbody[data-o="log"] tr').length+' msg='+o('msg'));});
clk('mn'); rec(); clk('nimh'); rec(); log('rows(max5)='+r.querySelectorAll('tbody[data-o="log"] tr').length);
log('g1 display='+r.querySelector('[data-ov="g1"]').style.display);
r.querySelector('[data-act="reset"]').click(); log('after reset rows='+r.querySelectorAll('tbody[data-o="log"] tr').length+' cls='+o('cls'));
clk('fuel'); log('fuel g1='+r.querySelector('[data-ov="g1"]').style.display+' cations shown='+[...r.querySelectorAll('svg g g')].filter(g=>g.getAttribute('display')!=='none'&&g.getAttribute('transform')).length);
})()
