import math, random
out={}
# honeycomb (graphene) in box 0..220 x 0..130, offset later
s=16; pts=set(); edges=set()
w=math.sqrt(3)*s
def hexv(cx,cy): return [(round(cx+s*math.cos(math.radians(60*k+30)),1),round(cy+s*math.sin(math.radians(60*k+30)),1)) for k in range(6)]
for r in range(4):
  for c in range(6):
    cx=20+c*w+(w/2 if r%2 else 0); cy=18+r*1.5*s
    v=hexv(cx,cy)
    for i in range(6):
      a,b=v[i],v[(i+1)%6]; edges.add(tuple(sorted([a,b]))); pts.add(a); pts.add(b)
L=''.join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for a,b in sorted(edges))
P=''.join(f'<circle cx="{x}" cy="{y}" r="4"/>' for x,y in sorted(pts))
out['HEX']=f'<g data-anim="draw" data-dur="1.6" fill="none" stroke="#5B6B7F" stroke-width="2.5">{L}</g><g fill="#3B3B3B">{P}</g>'
xs=[p[0] for p in pts]; ys=[p[1] for p in pts]; print('hex bbox',min(xs),max(xs),min(ys),max(ys))
# crystal 5x4 r9
C=''.join(f'<circle cx="{14+i*22}" cy="{14+j*22}" r="10"/>' for i in range(5) for j in range(4))
out['CRYS']=f'<g fill="#B7C2CE" stroke="#5B6B7F" stroke-width="1.5">{C}</g>'
random.seed(7); placed=[]
tries=0
while len(placed)<22 and tries<5000:
  tries+=1; r=10 if len(placed)%2==0 else 7
  x=random.uniform(r+2,108-r); y=random.uniform(r+2,86-r)
  if all((x-a)**2+(y-b)**2>(r+rr+1)**2 for a,b,rr in placed): placed.append((x,y,r))
print('amor',len(placed))
A=''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{"#B7C2CE" if r==10 else "#E0B44C"}"/>' for x,y,r in placed)
out['AMOR']=f'<g stroke="#5B6B7F" stroke-width="1.5">{A}</g>'
import json; json.dump(out,open(__file__.replace('gen.py','gen.json'),'w'),ensure_ascii=False)
