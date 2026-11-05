import sys,re
sys.path.insert(0,sys.argv[1])
import figs
src=open(sys.argv[1]+'/slides.tpl.html').read()
out=re.sub(r'\{\{(\w+)\}\}',lambda m:getattr(figs,m.group(1))(),src)
open(sys.argv[2],'w').write(out)
print('ok',len(out))
