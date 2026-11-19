(()=>{const r=document.querySelector('[data-lab="ac231cell"]');const q=s=>r.querySelector(s);const o=k=>q(`[data-o="${k}"]`).textContent;
const L=s=>console.warn('LAB '+s);const set=(k,v)=>{const i=q(`[data-i="${k}"]`);i.value=v;i.dispatchEvent(new Event('input'));};
const cnt=()=>q('[data-act="count"]'), crd=()=>q('[data-act="coord"]'), rec=()=>q('[data-act="rec"]');
L('idle '+o('big')+' | '+o('msg'));
for(const k of ['sc','bcc','fcc','hcp','nacl','cscl','zns']){
  q(`[data-k="${k}"]`).click();
  let steps=[]; for(let i=0;i<6;i++){ cnt().click(); steps.push(o('big')); if(o('big').startsWith('입자 수')) break; }
  crd().click(); const cb=o('big'); crd().click();
  set('sz',100); const m=o('msg'); set('sz',40);
  rec().click();
  L(k+' | '+steps.join(' / ')+' | '+cb+' | pf? '+(m.match(/점유 비율 [\d.]+ %/)||['-'])[0]);
}
set('pr',8); q('[data-k="bcc"]').click(); crd().click(); L('pred8 bcc: '+o('msg').slice(-40)); rec().click(); crd().click();
const rows=q('[data-o="log"]').children; L('rows '+rows.length+' | '+[...rows].map(x=>x.textContent).join(' || '));
q('[data-act="reset"]').click(); L('reset rows '+q('[data-o="log"]').children.length+' '+o('big'));
})()
