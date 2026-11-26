import re,sys,glob,html
base='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
pat=sys.argv[1]; n=int(sys.argv[2])
for f in sorted(glob.glob(base+'1-*/slides.html')):
    s=open(f).read()
    secs=re.split(r'(?=<section)',s)
    i=0
    for sec in secs:
        if not sec.startswith('<section'): continue
        i+=1
        t=re.search(r'data-title="([^"]*)"',sec)
        if t and re.search(pat,t.group(1)):
            x=re.sub(r'<svg.*?</svg>','[SVG]',sec,flags=re.S)
            x=re.sub(r'<[^>]+>',' ',x); x=html.unescape(re.sub(r'\s+',' ',x))
            print(f.split('/')[-2][:5],i,t.group(1),'::',x[:n]); print()
