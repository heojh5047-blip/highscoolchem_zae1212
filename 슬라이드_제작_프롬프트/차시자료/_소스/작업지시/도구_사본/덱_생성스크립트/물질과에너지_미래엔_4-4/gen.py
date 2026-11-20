import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figs44
tpl, out = sys.argv[1], sys.argv[2]
s = open(tpl, encoding='utf-8').read()
ns = dict(vars(figs44))
def rep(m):
    code = m.group(1)
    if code.startswith('!'):
        exec(code[1:], ns); return ''
    return str(eval(code, ns))
res = re.sub(r'⟪(.*?)⟫', rep, s, flags=re.S)
open(out, 'w', encoding='utf-8').write(res)
print('ok', out, len(res))
