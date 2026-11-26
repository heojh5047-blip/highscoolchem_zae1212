(()=>{const r=document.querySelector('[data-lab="ac451cat"]'); const q=s=>r.querySelector(s); const c=s=>q(s).click();
const L=t=>console.warn('LAB '+t); const o=k=>q(`[data-o="${k}"]`).textContent;
const set=(k,v)=>{const e=q(`[data-i="${k}"]`); e.value=v; e.dispatchEvent(new Event('input',{bubbles:true}));};
const rows=()=>[...q('[data-o="log"]').children].map(t=>t.textContent.replace(/\s+/g,' ')).join(' / ');
L('init now='+o('now')+' | rows='+q('[data-o="log"]').children.length);
c('[data-act="skip"]'); L('none25 '+o('msg'));
c('[data-c="KI"]'); L('ea1='+q('[data-ov="ea1"]').textContent); c('[data-act="skip"]'); L('KI25 '+o('msg'));
set('t',35); c('[data-act="skip"]'); L('KI35 '+o('msg'));
c('[data-p="1"]'); c('[data-act="skip"]'); L('KI35 1% '+o('msg'));
c('[data-p="3"]'); set('t',25); c('[data-c="MnO2"]'); c('[data-act="skip"]'); L('MnO2 25 '+o('msg'));
c('[data-c="cat"]'); c('[data-act="skip"]'); L('cat25 '+o('msg'));
set('t',35); c('[data-act="skip"]'); L('cat35 '+o('msg'));
set('t',55); c('[data-act="skip"]'); L('cat55 '+o('msg'));
L('rows '+q('[data-o="log"]').children.length+': '+rows());
c('[data-act="run"]'); L('running now='+o('now'));
c('[data-c="KI"]'); L('cancel msg='+o('msg'));
})()
