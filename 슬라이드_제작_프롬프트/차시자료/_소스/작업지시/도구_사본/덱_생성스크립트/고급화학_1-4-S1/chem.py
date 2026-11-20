# -*- coding: utf-8 -*-
"""탄소 골격(나무) → 정규형·3차원 좌표. gen.py가 exec한다."""
import math
# ── 정규형 (labs.js와 같은 알고리즘: 중심에서 뿌리 내린 괄호 문자열, 중심 2개면 작은 것)
def _cr(adj,v,p): return '('+''.join(sorted(_cr(adj,w,v) for w in adj[v] if w!=p))+')'
def _centers(adj):
    deg={v:len(adj[v]) for v in adj}; leaves=[v for v in adj if deg[v]<=1]; rem=len(adj); out=set()
    while rem>2:
        nl=[]
        for v in leaves:
            out.add(v); rem-=1
            for w in adj[v]:
                if w not in out:
                    deg[w]-=1
                    if deg[w]==1: nl.append(w)
        leaves=nl
    return [v for v in adj if v not in out]
def canon_edges(n,edges):
    adj={i:[] for i in range(n)}
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    return min(_cr(adj,c,None) for c in _centers(adj))
def skel(L,br):
    """주 사슬 L개(0..L-1) + 가지 메틸(br: 1부터 센 탄소 번호 목록). 반환: n, edges, chain, branch{가지 C: 붙은 C}"""
    edges=[(i,i+1) for i in range(L-1)]; branch={}; n=L
    for p in br: edges.append((p-1,n)); branch[n]=p-1; n+=1
    return n,edges,list(range(L)),branch
# ── 3차원
def v_add(a,b): return tuple(x+y for x,y in zip(a,b))
def v_sub(a,b): return tuple(x-y for x,y in zip(a,b))
def v_mul(a,k): return tuple(x*k for x in a)
def v_dot(a,b): return sum(x*y for x,y in zip(a,b))
def v_nrm(a): l=math.sqrt(v_dot(a,a)); return tuple(x/l for x in a)
def v_crs(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
HA=math.radians(109.4712/2)
def _two_free(d1,d2):
    b=v_nrm(v_add(d1,d2)); nn=v_nrm(v_crs(d1,d2))
    return [v_add(v_mul(b,-math.cos(HA)),v_mul(nn,math.sin(HA))),v_add(v_mul(b,-math.cos(HA)),v_mul(nn,-math.sin(HA)))]
def build3d(L,br,CC=1.54,CH=1.09):
    import itertools
    nb=len(set(br)); best=None
    for ch in itertools.product((0,1),repeat=nb):
        r=_build3d(L,br,CC,CH,ch)
        if best is None or r[2]>best[2]: best=r
    assert best[2]>1.85,(L,br,best[2])
    return best[0],best[1]
def _build3d(L,br,CC,CH,choice):
    """알케인 좌표: 지그재그 주 사슬(xy 평면) + 메틸 가지 + 엇갈린 H. 반환 atoms[(el,xyz)], bonds[(i,j,1)]"""
    n,edges,chain,branch=skel(L,br)
    zz=[(math.sin(HA),(1 if k%2==0 else -1)*math.cos(HA),0.0) for k in range(max(L,2)+1)]
    pos={}; dirs={i:[] for i in range(n)}
    pos[0]=(0.0,0.0,0.0)
    for k in range(L-1):
        pos[k+1]=v_add(pos[k],v_mul(zz[k],CC)); dirs[k].append(zz[k]); dirs[k+1].append(v_mul(zz[k],-1))
    atoms=[('C',None)]*n; H=[]
    def free(c):
        D=dirs[c]
        if len(D)==4: return []
        if len(D)==3:
            s=v_add(v_add(D[0],D[1]),D[2]); return [v_nrm(v_mul(s,-1))]
        if len(D)==2: return _two_free(D[0],D[1])
        if len(D)==1:
            if c in branch: par=branch[c]
            else: par=1 if c==0 else c-1
            other=[d for d in dirs[par] if v_dot(d,v_mul(D[0],-1))<0.99]
            if c==0 and L>1 and not other: a=v_mul(zz[1],-1)
            elif c==L-1 and c not in branch and not other: a=zz[L-1]
            else: a=v_mul(other[0],-1)
            # a는 D[0]과 109.47° — 맞춤
            return [a]+_two_free(D[0],a)
        return [(0,1,0)]
    if L==1:
        pos[0]=(0,0,0)
        RT=math.sqrt(8)/3
        for d in [(0,1,0)]+[(RT*math.sin(math.radians(p)),-1/3,RT*math.cos(math.radians(p))) for p in (0,120,240)]: H.append((0,d))
    else:
        # 사슬 탄소: 가지 먼저
        for c in chain:
            fr=free(c); bs=[b for b,p in branch.items() if p==c]
            # 가지는 +n 쪽(첫 자유 자리)부터, 두 번째 가지는 다음 자리
            order=fr[1:]+fr[:1] if len(fr)==3 else fr
            if bs and len(bs)==1 and choice[sorted(set(branch[x] for x in branch)).index(c)]: order=order[::-1]
            for b in bs:
                d=order.pop(0); pos[b]=v_add(pos[c],v_mul(d,CC)); dirs[c].append(d); dirs[b].append(v_mul(d,-1))
        for c in range(n):
            for d in free(c): H.append((c,d)); dirs[c].append(d)
    out=[('C',pos[i]) for i in range(n)]; bonds=[(a,b,1) for a,b in edges]
    for c,d in H:
        out.append(('H',v_add(pos[c],v_mul(d,CH)))); bonds.append((c,len(out)-1,1))
    # 검산
    deg=[0]*len(out)
    for a,b,_ in bonds: deg[a]+=1; deg[b]+=1
    assert all(deg[i]==4 for i in range(n)) and all(deg[i]==1 for i in range(n,len(out))), (L,br,deg)
    assert len(out)-n==2*n+2, (L,br)
    for a,b,_ in bonds:
        dd=math.dist(out[a][1],out[b][1]); assert abs(dd-(CC if b<n else CH))<1e-6
    for c in range(n):
        nb=[b if a==c else a for a,b,_ in bonds if c in (a,b)]
        for i in range(4):
            for j in range(i+1,4):
                u=v_nrm(v_sub(out[nb[i]][1],out[c][1])); w=v_nrm(v_sub(out[nb[j]][1],out[c][1]))
                ang=math.degrees(math.acos(max(-1,min(1,v_dot(u,w))))); assert abs(ang-109.47)<0.6,(L,br,ang)
    mind=9.0
    bset={(a,b) for a,b,_ in bonds}|{(b,a) for a,b,_ in bonds}
    for i in range(len(out)):
        for j in range(i+1,len(out)):
            if (i,j) in bset: continue
            share=any((i,k) in bset and (k,j) in bset for k in range(len(out)))
            if not share: mind=min(mind,math.dist(out[i][1],out[j][1]))
    ctr=v_mul(tuple(sum(p[1][m] for p in out) for m in range(3)),1/len(out))
    return [(e,v_sub(p,ctr)) for e,p in out],bonds,mind
def butene(cis=True):
    """2-뷰텐 평면 좌표(C=C 1.34, C–C 1.50, C–H 1.09, 120°). 원자 0 C1, 1 C2, 2 C3, 3 C4 …; side = C3 쪽(돌리는) 원자"""
    def u(a): return (math.cos(math.radians(a)),math.sin(math.radians(a)),0.0)
    C2=(-0.67,0,0); C3=(0.67,0,0)
    C1=v_add(C2,v_mul(u(120),1.50)); H2=v_add(C2,v_mul(u(240),1.09))
    C4=v_add(C3,v_mul(u(60 if cis else -60),1.50)); H3=v_add(C3,v_mul(u(-60 if cis else 60),1.09))
    at=[('C',C1),('C',C2),('C',C3),('C',C4),('H',H2),('H',H3)]; bd=[(0,1,1),(1,2,2),(2,3,1),(1,4,1),(2,5,1)]
    side=[3,5]
    for ci,par in ((0,1),(3,2)):
        d1=v_nrm(v_sub(at[par][1],at[ci][1]))
        # 엇갈림: 이웃 탄소의 다른 결합 반대 방향 하나를 평면 밖으로
        other=v_nrm(v_sub(at[2 if par==1 else 1][1],at[par][1]))
        a=v_mul(other,-1); a=v_nrm(v_sub(a,v_mul(d1,v_dot(a,d1))))
        nn=v_nrm(v_crs(d1,a)); hs=[]
        for ph in (0,120,240):
            p=math.radians(ph+60); perp=v_add(v_mul(a,math.cos(p)),v_mul(nn,math.sin(p)))
            hs.append(v_add(v_mul(d1,-1/3),v_mul(perp,math.sqrt(8)/3)))
        for d in hs:
            at.append(('H',v_add(at[ci][1],v_mul(d,1.09)))); bd.append((ci,len(at)-1,1))
            if ci==3: side.append(len(at)-1)
    return at,bd,side
