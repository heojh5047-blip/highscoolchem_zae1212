(()=>{const r=document.querySelector('[data-lab="cm411kw"]');const q=s=>r.querySelector(s);
[1,3,11,13].forEach(k=>{q(`[data-s="${k}"]`).click();console.warn('LAB k',k,q('[data-v="oh"]').innerText.replace(/\s+/g,''),q('[data-o="kind"]').textContent);});
const s=q('[data-i="k"]');s.value=5;s.dispatchEvent(new Event('input'));console.warn('LAB slider5',q('[data-v="h"]').innerText.replace(/\s+/g,''),q('[data-v="oh"]').innerText.replace(/\s+/g,''),q('[data-o="msg"]').textContent);})()
