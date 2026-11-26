import re,sys,glob
B='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
def slides(d):
    h=open(glob.glob(B+d+'*/slides.html')[0],encoding='utf-8').read()
    return re.findall(r'<section.*?</section>',h,re.S)
def txt(s):
    s=re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S)
    s=re.sub(r'<span class="blank">','[',s)
    s=re.sub(r'<[^>]+>',' ',s); s=re.sub(r'[ \t]+',' ',s); s=re.sub(r'\n\s*\n+','\n',s)
    return s.strip()
d=sys.argv[1]
S=slides(d)
for a in sys.argv[2:]:
    n=int(a); print(f'--- {d} #{n}'); print(txt(S[n-1]))
