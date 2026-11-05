(()=>{window.__STILL=true;const r=document.querySelector('[data-lab="cm412dil"]');const q=s=>r.querySelector(s);const c=a=>q(`[data-act="${a}"]`).click();
const rows=()=>q('[data-o="log"]').children.length;const show=t=>console.warn('LAB',t,'| cur',q('[data-v="cur"]').innerText.replace(/\s+/g,''),'| pH',q('[data-o="pH"]').textContent,'| rows',rows(),'| bars',r.querySelectorAll('svg g rect[width="18"]').length,'| msg',q('[data-o="msg"]').textContent.slice(0,90));
c('meas');show('A');for(let i=0;i<4;i++){c('dil');c('meas');show('dil'+(i+1));}
c('meas');show('again');
q('[data-s="b"]').click();c('meas');show('NaOH A');c('dil');c('meas');show('NaOH B');
q('[data-s="a"]').click();for(let i=0;i<9;i++)c('dil');show('acid J pre');c('meas');show('acid J');console.warn('LAB dil disabled',q('[data-act="dil"]').disabled);
c('th');console.warn('LAB th row',q('[data-o="log"] tr:last-child').innerText.replace(/\s+/g,' '),'circles',r.querySelectorAll('svg circle').length);
})()
