(()=>{const r=document.querySelector('[data-lab="ac441diag"]'); const q=s=>r.querySelector(s); const c=s=>q(s).click();
const L=t=>console.warn('LAB '+t); const o=k=>q(`[data-o="${k}"]`).textContent;
const set=(k,v)=>{const e=q(`[data-i="${k}"]`); e.value=v; e.dispatchEvent(new Event('input',{bubbles:true}));};
const st=()=>`eaf=${o('eaf')} ear=${o('ear')} dh=${o('dh')} | ${o('fr')}`;
L('init '+st()+' || given '+o('given'));
c('[data-j="발열"]'); L('a wrong-diagram exo: '+o('msg'));
set('ts',132); set('p',-226); L('a set '+st()); c('[data-j="흡열"]'); L('a endo: '+o('msg')); c('[data-j="발열"]'); L('a exo: '+o('msg'));
set('T',400); L('T400 '+o('fr')); set('dT',50); L('dT50 '+o('fr')); set('T',300); set('dT',10);
c('[data-rx="b"]'); set('ts',19); set('p',-392); c('[data-j="발열"]'); L('b: '+st()+' || '+o('msg'));
c('[data-rx="c"]'); set('ts',358); set('p',226); c('[data-j="흡열"]'); L('c: '+st()+' || '+o('msg'));
c('[data-rx="d"]'); L('d two class '+q('[data-o="two"]').className); set('ts',90); set('im',30); set('ts2',60); set('p',-50); c('[data-j="발열"]'); L('d: '+st()+' || '+o('msg'));
L('log rows '+q('[data-o="log"]').children.length+' : '+[...q('[data-o="log"]').children].map(t=>t.textContent).join(' / '));
L('mag '+q('[data-ov="mag"]').textContent+' | r '+q('[data-ov="r"]').textContent);
})()
