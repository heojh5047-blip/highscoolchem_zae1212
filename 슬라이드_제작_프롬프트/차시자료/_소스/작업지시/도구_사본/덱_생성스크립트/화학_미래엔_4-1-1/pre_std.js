(()=>{const r=document.querySelector('[data-lab="cm411std"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const nx=()=>q('[data-act="next"]').click();
const run=(lab)=>{for(let i=0;i<7;i++)nx();q('[data-act="measure"]').click();const m=o('meas');q('[data-act="rec"]').click();console.warn('LAB',lab,'meas',m,'calc',o('calc'),'msg',o('msg').slice(0,60));};
run('바름');
q('[data-e="wash"]').checked=true;q('[data-e="wash"]').dispatchEvent(new Event('change'));q('[data-u="NaCl"]').click();run('헹군물X');
q('[data-e="wash"]').checked=false;q('[data-e="over"]').checked=true;q('[data-u="Glc"]').click();run('넘김 포도당');
q('[data-e="over"]').checked=false;q('[data-e="above"]').checked=true;q('[data-u="NaOH"]').click();run('위에서 NaOH');
const M=q('[data-i="M"]');M.value=0.25;M.dispatchEvent(new Event('input'));q('[data-v="250"]').click();q('[data-e="above"]').checked=false;q('[data-e="mix"]').checked=true;run('안흔듦 0.25M 250');
q('[data-act="measure"]').click();console.warn('LAB 재측정',o('meas'));
console.warn('LAB rows',q('[data-o="log"]').children.length, q('[data-o="log"]').innerText.replace(/\s+/g,' ').slice(0,400));
})()
