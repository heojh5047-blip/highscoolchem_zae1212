(()=>{const out=[];
const g=document.querySelector('[data-lab="cm212graph"]'); const q=s=>g.querySelector(s); const O=k=>q(`[data-o="${k}"]`).textContent;
const pts=()=>g.querySelectorAll('svg circle').length+'c/'+g.querySelectorAll('svg rect').length+'r';
out.push('G0 ax='+O('ax')+' '+pts());
q('[data-act="rec"]').click(); q('[data-m="p"]').click(); out.push('Gp ax='+O('ax')+' ser='+O('ser')+' '+pts()+' msg='+O('msg').slice(0,20));
q('[data-act="rec"]').click(); q('[data-s="bar"]').click(); out.push('Gpbar '+pts()); q('[data-m="g"]').click(); out.push('Ggbar msg='+O('msg').slice(0,25)); q('[data-act="rec"]').click();
out.push('Grows='+q('[data-o="log"]').children.length+' last='+q('[data-o="log"]').lastElementChild.textContent);
q('[data-act="reset"]').click(); out.push('Greset rows='+q('[data-o="log"]').children.length+' ax='+O('ax'));
const b=document.querySelector('[data-lab="cm212bond"]'); const Q=s=>b.querySelector(s); const P=k=>Q(`[data-o="${k}"]`).textContent;
const pick=(s,e)=>Q(`[data-side="${s}"] [data-el="${e}"]`).click();
const snap=l=>out.push(l+': en='+P('en')+' d='+P('d')+' k='+P('kind')+' | '+P('msg').slice(0,30));
snap('HH'); Q('[data-act="rec"]').click(); pick('b','F'); snap('HF'); Q('[data-act="rec"]').click(); pick('b','Cl'); snap('HCl'); Q('[data-act="rec"]').click();
pick('a','Na'); snap('NaCl'); Q('[data-act="rec"]').click(); pick('b','Li'); snap('NaLi'); pick('a','C'); pick('b','S'); snap('CS'); pick('b','O'); snap('CO');
out.push('Brows='+Q('[data-o="log"]').children.length+' last='+Q('[data-o="log"]').lastElementChild.textContent);
Q('[data-act="reset"]').click(); out.push('Breset rows='+Q('[data-o="log"]').children.length+' en='+P('en'));
out.forEach(l=>console.warn('LAB '+l));})()
