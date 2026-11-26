(()=>{const r=document.querySelector('[data-lab="ac113fill"]');const q=s=>r.querySelector(s);const O=k=>q(`[data-o="${k}"]`).innerText.replace(/\n/g,' / ');
const set=(v)=>{const i=q('[data-i="z"]');i.value=v;i.dispatchEvent(new Event('input'));};
const act=a=>q(`[data-act="${a}"]`).click(); const chg=v=>q(`[data-q="${v}"]`).click();
const box=k=>q(`rect[data-k="${k}"]`).dispatchEvent(new MouseEvent('click',{bubbles:true}));
const W=t=>console.warn('LAB '+t,'|',O('cnt'),'|',O('info'),'|',O('msg'));
W('init C');for(let i=0;i<6;i++)act('add');W('C added');act('check');W('C check');act('rec');
set(7);W('N new');for(let i=0;i<7;i++)act('add');W('N add');act('check');W('N check');
box(2);box(2);W('N 2px->d');act('check');W('N hund?');act('rec');
set(19);for(let i=0;i<19;i++)act('add');act('check');W('K');act('rec');
set(24);for(let i=0;i<24;i++)act('add');act('check');W('Cr aufbau');act('fill');act('check');W('Cr fill');act('rec');
set(29);act('fill');act('check');W('Cu');
set(26);chg(2);for(let i=0;i<24;i++)act('add');act('check');W('Fe2+ naive');act('fill');act('check');W('Fe2+ fill');act('rec');
set(17);chg(-1);act('fill');act('check');W('Cl-');
set(20);chg(2);act('fill');W('Ca2+');act('rec');
set(1);chg(3);W('H+3 invalid');
set(11);act('clear');box(0);box(0);box(0);box(1);box(1);box(1);box(2);box(2);box(2);
for(let k=3;k<6;k++){box(k);box(k);box(k);} box(6);W('Na manual 1s2s2p+3s?');act('check');W('Na check');
console.warn('LAB rows',q('[data-o="log"]').children.length,O('log'));})()
