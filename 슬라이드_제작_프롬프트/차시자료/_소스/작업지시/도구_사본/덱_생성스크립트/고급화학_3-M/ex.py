import re,sys,html
pat=sys.argv[2]
s=open(sys.argv[1]).read()
secs=re.split(r'<section',s)[1:]
for i,x in enumerate(secs,1):
  t=re.search(r'data-title="([^"]*)"',x); t=t.group(1) if t else ''
  if re.search(pat,t):
    x=re.sub(r'<svg.*?</svg>','[SVG]',x,flags=re.S)
    x=re.sub(r'<[^>]+>',' ',x); x=html.unescape(re.sub(r'\s+',' ',x))
    print(f'#{i} {t}: {x[:1400]}\n')
