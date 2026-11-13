(()=>{const r=document.querySelector('[data-lab="em29cool"]');const w=r.querySelector('[data-i="w"]'),T=r.querySelector('[data-i="tm"]');const o=k=>r.querySelector(`[data-o="${k}"]`).textContent;
const set=(el,v)=>{el.value=v;el.dispatchEvent(new Event('input'))};
const rec=()=>r.querySelector('[data-act="rec"]').click();
set(w,310);console.warn('LAB 310',o('m'),o('tf'),o('tb'),o('msg'));rec();
set(w,500);console.warn('LAB 500',o('m'),o('tf'),o('tb'),o('msg'));rec();
set(w,510);console.warn('LAB 510',o('tf'),o('msg'));
r.querySelector('[data-season="2"]').click();set(w,0);console.warn('LAB spring',o('tm'),o('tf'),o('msg'));rec();
console.warn('LAB rows',r.querySelectorAll('[data-o="log"] tr').length);
set(w,500); T.value=-15; T.dispatchEvent(new Event('input'));})()
