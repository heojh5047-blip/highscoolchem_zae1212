import sys,re
sys.path.insert(0,'.')
import figs
t=open('tpl.html').read()
a,b,c=figs.procfigs()
m={'cover':figs.cover(),'think':figs.think(),'ioniz':figs.ioniz(),'kabars':figs.kabars(),'kbbars':figs.kbbars(),'pairs':figs.pairs(),'dom':figs.dom(),'ladder':figs.ladder(),'proc1':a,'proc2':b,'proc3':c,'resplot':figs.resplot()}
t=re.sub(r'\{\{(\w+)\}\}',lambda x:m[x.group(1)],t)
open(sys.argv[1],'w').write(t)
