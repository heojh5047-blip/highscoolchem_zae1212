(async()=>{const r=document.querySelector('[data-lab="cm112mass"]'); const sl=ms=>new Promise(f=>setTimeout(f,ms));
const O=k=>r.querySelector(`[data-o="${k}"]`).textContent; const Ov=k=>r.querySelector(`[data-ov="${k}"]`).textContent;
const act=a=>r.querySelector(`[data-act="${a}"]`).click(); const sub=k=>r.querySelector(`[data-s="${k}"]`).click();
const setn=v=>{const i=r.querySelector('[data-i="n"]'); i.value=v; i.dispatchEvent(new Event('input'));};
const out=[];
for(const [k,v,tare] of [['C',2,1],['Glu',2,1],['NaCl',7,1],['H2O',10,0],['EtOH',20,1],['Cu',4,1]]){
  sub(k); setn(v); if(tare) act('tare'); out.push(`${k} n=${O('n')} M=${O('M')} w=${O('w')} disp0=${Ov('disp')}`);
  act('pour'); await sl(2000); act('rec'); out.push(`  after disp=${Ov('disp')} N=${Ov('N')} msg=${O('msg').slice(0,70)}`); }
out.push('rows='+r.querySelectorAll('tbody[data-o="log"] tr').length+' last='+r.querySelector('tbody[data-o="log"] tr:last-child').textContent.slice(0,80));
act('rec'); act('reset'); out.push('reset rows='+r.querySelectorAll('tbody[data-o="log"] td[colspan]').length+' n='+O('n'));
sub('Glu'); setn(10); act('tare'); act('pour'); await sl(2000);
out.forEach(x=>console.warn('LAB '+x)); return 1;})()
