# tpl.html의 섹션(data-title) 하나를 new/<n>.html 내용으로 통째로 바꾼다
import re,sys,os
H=os.path.dirname(os.path.abspath(__file__)); p=os.path.join(H,'tpl.html'); s=open(p,encoding='utf-8').read()
for fn in sys.argv[1:]:
    new=open(fn,encoding='utf-8').read().strip()
    t=re.search(r'data-title="([^"]+)"',new).group(1)
    pat=re.compile(r'<section[^>]*data-title="'+re.escape(t)+r'">.*?</section>',re.S)
    assert len(pat.findall(s))==1,(t,len(pat.findall(s)))
    s=pat.sub(lambda m:new,s)
    print('replaced',t)
open(p,'w',encoding='utf-8').write(s)
