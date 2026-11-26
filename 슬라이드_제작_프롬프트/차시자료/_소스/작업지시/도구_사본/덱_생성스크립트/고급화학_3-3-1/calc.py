# 고급화학 3-3-1 산화수·반응식 검산: 원자 수·전하·산화수 합·전자 수
import re
from fractions import Fraction as Fr
def formula(f):
    f=re.sub(r'\((s|l|g|aq)\)$','',f)
    def grp(s):
        tot={}; i=0
        while i<len(s):
            if s[i]=='(':
                d=1;j=i+1
                while d: d+= {'(':1,')':-1}.get(s[j],0); j+=1
                m=re.match(r'\d*',s[j:]); n=int(m.group() or 1); sub=grp(s[i+1:j-1])
                for k,v in sub.items(): tot[k]=tot.get(k,0)+v*n
                i=j+len(m.group()); continue
            m=re.match(r'([A-Z][a-z]?)(\d*)',s[i:]); tot[m.group(1)]=tot.get(m.group(1),0)+int(m.group(2) or 1); i+=len(m.group())
        return tot
    return grp(f)
def species(t):
    t=re.sub(r'\((s|l|g|aq)\)$','',t.strip())
    if t=='e-': return {},-1
    if '^' in t:
        body,c=t.split('^'); n=c[:-1]; return formula(body),(int(n) if n else 1)*(1 if c[-1]=='+' else -1)
    if t[-1] in '+-': return formula(t[:-1]),(1 if t[-1]=='+' else -1)
    return formula(t),0
def side(s):
    A={};Q=0
    for term in s.split(' + '):
        m=re.match(r'^(\d+/\d+|\d+)?\s*(.+)$',term.strip()); c=Fr(m.group(1)) if m.group(1) else Fr(1)
        a,q=species(m.group(2))
        for k,v in a.items(): A[k]=A.get(k,0)+c*v
        Q+=c*q
    return A,Q
EQ=[('S1·S15·S18 Zn+H3O+','Zn(s) + 2H3O+(aq) -> Zn^2+(aq) + H2(g) + 2H2O(l)'),
('S15 산화 반쪽','Zn(s) -> Zn^2+(aq) + 2e-'),('S15 환원 반쪽(1/2)','H3O+(aq) + e- -> 1/2 H2(g) + H2O(l)'),('S15 환원 반쪽 ×2','2H3O+(aq) + 2e- -> H2(g) + 2H2O(l)'),
('S4·S5 Na+Cl2','2Na(s) + Cl2(g) -> 2NaCl(s)'),('S5 Na 반쪽','Na -> Na+ + e-'),('S5 Cl 반쪽','Cl2 + 2e- -> 2Cl-'),
('S4 H2+Cl2','H2(g) + Cl2(g) -> 2HCl(g)'),('S4 Mg 연소','2Mg(s) + O2(g) -> 2MgO(s)'),
('S9 CuO+H2','CuO(s) + H2(g) -> Cu(s) + H2O(l)'),
('S14 계수 전','Cu(s) + Ag+(aq) -> Cu^2+(aq) + Ag(s)'),('S14 계수 후','Cu(s) + 2Ag+(aq) -> Cu^2+(aq) + 2Ag(s)'),
('S16 산화수법','MnO4-(aq) + 5Fe^2+(aq) + 8H+(aq) -> Mn^2+(aq) + 5Fe^3+(aq) + 4H2O(l)'),
('S20 환원 반쪽','MnO4-(aq) + 8H+(aq) + 5e- -> Mn^2+(aq) + 4H2O(l)'),('S20 산화 반쪽','H2O2(aq) -> O2(g) + 2H+(aq) + 2e-'),
('S21 예제III-9 전체','2MnO4-(aq) + 6H+(aq) + 5H2O2(aq) -> 2Mn^2+(aq) + 8H2O(l) + 5O2(g)'),
('S22 환원 반쪽','MnO4-(aq) + 4H+(aq) + 3e- -> MnO2(s) + 2H2O(l)'),('S22 산화 반쪽','I-(aq) + 3H2O(l) -> IO3-(aq) + 6H+(aq) + 6e-'),
('S22 산성 합','2MnO4-(aq) + I-(aq) + 2H+(aq) -> 2MnO2(s) + IO3-(aq) + H2O(l)'),('S22 염기성','2MnO4-(aq) + I-(aq) + H2O(l) -> 2MnO2(s) + IO3-(aq) + 2OH-(aq)'),
('S23 확인03','2KMnO4 + 16HCl -> 2KCl + 2MnCl2 + 5Cl2 + 8H2O'),
('S25 연료 전지','2H2(g) + O2(g) -> 2H2O(l)'),('S25 제철','Fe2O3(s) + 3CO(g) -> 2Fe(s) + 3CO2(g)'),
('S25 세포 호흡','C6H12O6(aq) + 6O2(g) -> 6CO2(g) + 6H2O(l)'),('S25 광합성','6CO2(g) + 6H2O(l) -> C6H12O6(aq) + 6O2(g)'),
('S25 음주 측정','2Cr2O7^2-(aq) + 3C2H5OH(aq) + 16H+(aq) -> 4Cr^3+(aq) + 3CH3COOH(aq) + 11H2O(l)'),
('S25 철 부식','2Fe(s) + O2(g) + 2H2O(l) -> 2Fe(OH)2(s)'),
('S25·S29 알칼리 전지','Zn(s) + MnO2(s) + H2O(l) -> ZnO(s) + Mn(OH)2(s)'),
('S29 산화 반쪽','Zn(s) + H2O(l) -> ZnO(s) + 2H+(aq) + 2e-'),('S29 환원 반쪽','2H+(aq) + MnO2(s) + 2e- -> Mn(OH)2(s)'),
('S27 연습2-1 환원','O2(g) + 4H+(aq) + 4e- -> 2H2O(l)'),('S27 연습2-1 산화','NO(g) + 2H2O(l) -> NO3-(aq) + 4H+(aq) + 3e-'),
('S27 연습2-1','3O2(g) + 4NO(g) + 2H2O(l) -> 4NO3-(aq) + 4H+(aq)'),
('S28 연습2-2 환원','CrO4^2-(aq) + 8H+(aq) + 3e- -> Cr^3+(aq) + 4H2O(l)'),('S28 연습2-2 산화','N2O(g) + H2O(l) -> 2NO(g) + 2H+(aq) + 2e-'),
('S28 연습2-2','2CrO4^2-(aq) + 3N2O(g) + 10H+(aq) -> 2Cr^3+(aq) + 6NO(g) + 5H2O(l)')]
ok=0
for s,e in EQ:
    l,r=e.split(' -> '); A,qa=side(l); B,qb=side(r); g=(A==B and qa==qb); ok+=g
    print('일치' if g else '불일치!!',s,'|',e,'|',{k:str(v) for k,v in A.items()},'전하',qa,qb)
print('반응식',ok,'/',len(EQ))
print('--- 산화수 합 검산 (Σ 개수×산화수 = 전하)')
OX=[('H2O',0,{'H':1,'O':-2}),('CO',0,{'C':2,'O':-2}),('NH4',1,{'N':-3,'H':1}),('Cr2O7',-2,{'Cr':6,'O':-2}),('MnO4',-1,{'Mn':7,'O':-2}),
('H2O2',0,{'H':1,'O':-1}),('NaH',0,{'Na':1,'H':-1}),('OF2',0,{'O':2,'F':-1}),('O2F2',0,{'O':1,'F':-1}),('H2SO4',0,{'H':1,'S':6,'O':-2}),
('Fe3O4',0,{'Fe':Fr(8,3),'O':-2}),('H3O',1,{'H':1,'O':-2}),('CuO',0,{'Cu':2,'O':-2}),('MnO2',0,{'Mn':4,'O':-2}),('Mn(OH)2',0,{'Mn':2,'O':-2,'H':1}),
('ZnO',0,{'Zn':2,'O':-2}),('NO3',-1,{'N':5,'O':-2}),('NO',0,{'N':2,'O':-2}),('N2O',0,{'N':1,'O':-2}),('CrO4',-2,{'Cr':6,'O':-2}),('IO3',-1,{'I':5,'O':-2}),
('KMnO4',0,{'K':1,'Mn':7,'O':-2}),('MnCl2',0,{'Mn':2,'Cl':-1}),('HCl',0,{'H':1,'Cl':-1}),('Fe2O3',0,{'Fe':3,'O':-2}),('CO2',0,{'C':4,'O':-2}),
('C2H5OH',0,{'C':-2,'H':1,'O':-2}),('CH3COOH',0,{'C':0,'H':1,'O':-2}),('C6H12O6',0,{'C':0,'H':1,'O':-2}),('NaCl',0,{'Na':1,'Cl':-1}),('HClO',0,{'H':1,'Cl':1,'O':-2}),('NaClO',0,{'Na':1,'Cl':1,'O':-2}),('ClO4',-1,{'Cl':7,'O':-2}),('SO4',-2,{'S':6,'O':-2}),('NH3',0,{'N':-3,'H':1}),('N3',-1,{'N':Fr(-1,3)})]
bad=0
for f,q,d in OX:
    a=formula(f); s=sum(a[k]*Fr(d[k]) for k in a); g=(s==q and set(a)==set(d)); bad+=not g
    print('일치' if g else '불일치!!',f,q,{k:str(v) for k,v in d.items()})
print('산화수 불일치',bad)
print('--- 전자 수 (산화수 증가 총량 = 감소 총량)')
EL=[('S1 Zn+2H3O+','Zn 0→+2: +2 ×1','H +1→0: −1 ×2',2,2),('S5 2Na+Cl2','Na 0→+1 ×2','Cl 0→−1 ×2',2,2),('S9 CuO+H2','H 0→+1 ×2','Cu +2→0',2,2),
('S14 Cu+2Ag+','Cu 0→+2','Ag +1→0 ×2',2,2),('S16','Fe +2→+3 ×5','Mn +7→+2 ×1',5,5),('S21','O −1→0 ×10','Mn +7→+2 ×2',10,10),
('S22','I −1→+5 ×1','Mn +7→+4 ×2',6,6),('S23','Cl −1→0 ×10','Mn +7→+2 ×2',10,10),('S25 음주','C −2→0 ×3(에탄올 C 한 개)','Cr +6→+3 ×4',12,12),
('S27','N +2→+5 ×4','O 0→−2 ×6',12,12),('S28','N +1→+2 ×6','Cr +6→+3 ×2',6,6),('S29','Zn 0→+2','Mn +4→+2',2,2)]
for a,b,c,x,y in EL: print('일치' if x==y else '불일치!!',a,b,'/',c,x,y)
print('--- 계산')
n=9.00/65.41; print('연습3 Zn mol',n,'MnO2 g',n*86.94,'(0.138:',0.138*86.94,') H2O g',n*18.02,'(0.138:',0.138*18.02,')')
print('S25 음주 측정 에탄올 C: CH3 −3, CH2OH −1 → 평균 −2; 아세트산 CH3 −3, COOH +3 → 평균 0; 변하는 C는 CH2OH의 C −1 → +3 (+4) ×3 = 12')
print('--- 자동 전자 수 검산: 원소별 (산화수×원자 수) 합의 변화. 산화 증가량 = 환원 감소량 = 주고받은 전자 수, 반쪽 반응은 e- 계수와 같아야 함')
OXD={f:d for f,q,d in OX}
OXD.update({'MgO':{'Mg':2,'O':-2},'Fe(OH)2':{'Fe':2,'O':-2,'H':1},'H2O':{'H':1,'O':-2},'OH':{'O':-2,'H':1},'KCl':{'K':1,'Cl':-1}})
def oxof(body,ch):
    a=formula(body)
    if len(a)==1: k=list(a)[0]; return {k:Fr(ch,a[k])}
    return OXD[body]
def tally(s):
    T={};E=Fr(0)
    for term in s.split(' + '):
        m=re.match(r'^(\d+/\d+|\d+)?\s*(.+)$',term.strip()); c=Fr(m.group(1)) if m.group(1) else Fr(1)
        t=re.sub(r'\((s|l|g|aq)\)$','',m.group(2).strip())
        if t=='e-': E+=c; continue
        if '^' in t: body=t.split('^')[0]; _,ch=species(t)
        elif t[-1] in '+-': body=t[:-1]; ch=1 if t[-1]=='+' else -1
        else: body=t; ch=0
        a=formula(body); d=oxof(body,ch)
        for k,n in a.items(): T[k]=T.get(k,0)+c*n*Fr(d[k])
    return T,E
bad=0
for s,e in EQ:
    if '계수 전' in s: continue
    l,r=e.split(' -> '); A,ea=tally(l); B,eb=tally(r)
    ch={k:B.get(k,0)-A.get(k,0) for k in set(A)|set(B)}
    up=sum(v for v in ch.values() if v>0); dn=-sum(v for v in ch.values() if v<0)
    if ea or eb:   # 반쪽 반응: 산화이면 오른쪽 e- = 증가량, 환원이면 왼쪽 e- = 감소량
        g=(eb==up-dn) if eb else (ea==dn-up); txt=f'e- {ea or eb}, 산화수 변화 +{up} −{dn}'
    else:
        g=(up==dn); txt=f'전자 {up}'+(' (산화 환원 아님)' if up==0 else '')
    bad+=not g; print('일치' if g else '불일치!!',s,txt,{k:str(v) for k,v in ch.items() if v})
print('자동 전자 수 불일치',bad)
