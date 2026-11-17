(()=>{const r=document.querySelector('[data-lab="ac113fill"]');const q=s=>r.querySelector(s);const O=k=>q(`[data-o="${k}"]`).innerText.replace(/\n/g,'');
const set=(v)=>{const i=q('[data-i="z"]');i.value=v;i.dispatchEvent(new Event('input'));};
const act=a=>q(`[data-act="${a}"]`).click(); const chg=v=>q(`[data-q="${v}"]`).click();
const box=k=>q(`rect[data-k="${k}"]`).dispatchEvent(new MouseEvent('click',{bubbles:true}));
const W=t=>console.warn('LAB '+t,'|',O('cnt'),'|',O('info'),'|',O('msg'));
set(7);act('fill');box(3);W('N 2p 2nd box u->d');act('check');W('N hund');act('rec');
set(8);act('fill');act('clear');for(let i=0;i<8;i++)act('add');box(3);box(3);box(3);box(4);act('check');W('O pair wrong');
set(11);for(let i=0;i<10;i++)act('add');box(6);act('check');W('Na 3p excited');act('rec');
set(26);act('fill');act('check');W('Fe');chg(2);act('fill');W('Fe2+ val');act('rec');
console.warn('LAB rows',q('[data-o="log"]').children.length);})()
