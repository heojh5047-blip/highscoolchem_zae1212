(async()=>{const sl=document.querySelectorAll('.slide')[20];const L=sl.querySelector('.lab');const q=s=>L.querySelector(s);const T=e=>e.textContent.replace(/\s+/g,' ').trim();
const click=e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}));
const rep=t=>console.warn('LAB '+t+' | msg='+T(q('[data-o="msg"]')).slice(0,60)+' | ab='+T(q('[data-o="ab"]')).slice(0,40)+' | rows='+q('[data-o="log"]').children.length+' | score='+T(q('[data-o="score"]')));
click(q('[data-r="0"]'));click(q('[data-p="1"]'));rep('r1 wrong');click(q('[data-p="0"]'));rep('r1 right');click(q('[data-act="rec"]'));rep('rec');
for(const [r,p] of [[1,1],[4,0],[6,0]]){click(q(`[data-r="${r}"]`));click(q(`[data-p="${p}"]`));click(q('[data-act="rec"]'));}rep('after4');
click(q('[data-r="5"]'));click(q('[data-p="1"]'));rep('r6');click(q('[data-act="rec"]'));rep('5 recs');
console.warn('LAB pairs='+T(q('[data-o="pairs"]'))+' water='+T(q('[data-o="water"]')));
click(q('[data-act="reset"]'));rep('reset');})();
