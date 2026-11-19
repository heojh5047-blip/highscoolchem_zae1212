(()=>{const r=document.querySelector('[data-lab="ac231ion"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const rec=()=>q('[data-act="rec"]').click();
for(const s of [0,0.25,0.5,0.75,1]){ set('sh',s); L('salt sh='+s+' '+o('big')+' | '+o('msg').slice(0,40)); }
rec(); q('[data-s="metal"]').click(); L('metal '+o('big')+' | '+o('msg').slice(0,30)); rec();
q('[data-m="ec"]').click();
for(const t of [25,300,350,400]){ set('t',t); L('kno3 '+t+' '+o('big')+' | '+o('msg').slice(0,40)); rec(); }
set('t',25); const aq=q('[data-i="aq"]'); aq.checked=true; aq.dispatchEvent(new Event('change')); L('kno3 aq '+o('big')); rec();
aq.checked=false; aq.dispatchEvent(new Event('change'));
q('[data-s="nacl"]').click(); set('t',400); L('nacl 400 '+o('big')+' | '+o('msg').slice(-30));
q('[data-s="sugar"]').click(); set('t',200); L('sugar 200 '+o('big')+' | '+o('msg').slice(0,40)); rec();
const rows=q('[data-o="log"]').children; L('rows '+rows.length+' | '+[...rows].map(x=>x.textContent).join(' || '));
})()
