import sys, re, importlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
deck = sys.argv[1]   # a | b
mod = importlib.import_module('figs_' + deck)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), deck + '.html'), encoding='utf-8').read()
miss = set()
def rep(m):
    k = m.group(1)
    if k not in mod.F: miss.add(k); return m.group(0)
    return mod.F[k]
out = re.sub(r'\{\{([A-Z0-9_]+)\}\}', rep, src)
if miss: print('MISSING', miss); sys.exit(1)
dst = sys.argv[2]
open(dst, 'w', encoding='utf-8').write(out)
print('wrote', dst, len(out))
