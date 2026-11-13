(async()=>{const r=document.querySelectorAll('.slide')[19];const q=s=>r.querySelector(s);const sl=q('[data-i="w"]');const W=ms=>new Promise(f=>setTimeout(f,ms));
const run=async(v,e)=>{sl.value=v;sl.dispatchEvent(new Event('input'));q('[data-e="early"]').checked=e;q('[data-act="run"]').click();await W(2300);console.warn('LAB',v/10,e,q('[data-o="m"]').textContent,'|',q('[data-o="msg"]').textContent,'| rows',q('[data-o="log"]').children.length);};
await run(10,false);await run(30,false);await run(50,false);await run(20,true);
q('[data-act="reset"]').click();console.warn('LAB reset rows',q('[data-o="log"]').children.length);})()
