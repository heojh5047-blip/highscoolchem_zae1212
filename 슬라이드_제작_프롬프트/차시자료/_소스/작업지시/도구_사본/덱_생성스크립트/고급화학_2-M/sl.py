import re,sys,glob
f=glob.glob(sys.argv[1]+'*/slides.html')[0]
s=open(f).read()
secs=re.split(r'<section',s)[1:]
for n in sys.argv[2].split(','):
  x=secs[int(n)-1]
  x=re.sub(r'<svg.*?</svg>','[SVG]',x,flags=re.S)
  x=re.sub(r'<(br|/p|/li|/tr|/div|/h2|/h3)[^>]*>','\n',x)
  x=re.sub(r'<[^>]+>',' ',x)
  x=re.sub(r'[ \t]+',' ',x); x=re.sub(r'\n\s*\n+','\n',x)
  print('=== S'+n); print(x.strip()[:int(sys.argv[3]) if len(sys.argv)>3 else 3000])
