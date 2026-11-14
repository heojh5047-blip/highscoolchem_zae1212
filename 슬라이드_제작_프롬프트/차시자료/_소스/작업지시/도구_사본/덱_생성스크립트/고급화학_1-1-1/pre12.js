(()=>{const r=document.querySelector('[data-lab="ac111spec"]');const q=s=>r.querySelector(s);const O=k=>q(`[data-o="${k}"]`).textContent;
const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const rec=()=>q('[data-act="rec"]').click();
q('[data-s="H"]').click();set('cur',656);console.warn('LAB H656',O('big'),'|',O('msg'));rec();
set('cur',486);rec();set('cur',600);console.warn('LAB H600',O('big'),'|',O('msg'));
q('[data-s="Ne"]').click();set('cur',640);rec();console.warn('LAB Ne',O('big'));
q('[data-s="lamp"]').click();console.warn('LAB lamp',O('big'),O('msg'));
q('[data-m="h"]').click();[3,4,5,6].forEach(n=>{set('ni',n);console.warn('LAB h',n,'->2',O('big'));});
set('ni',6);rec();q('[data-f="1"]').click();set('ni',2);console.warn('LAB 2->1',O('big'),O('msg'));rec();
q('[data-f="3"]').click();set('ni',3);console.warn('LAB 3->3',O('big'),O('msg'));set('ni',4);console.warn('LAB 4->3',O('big'));rec();
console.warn('LAB rows',q('[data-o="log"]').children.length, q('[data-o="log"]').innerText.replace(/\n/g,' / '));})()
