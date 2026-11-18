# 알케인 구조 이성질체 수(탄소 골격 = 최대 차수 4인 나무) 세기와 알켄(사슬, C=C 1개, 시스-트랜스 포함) 세기
def canon_rooted(adj,v,p):
    return '('+''.join(sorted(canon_rooted(adj,w,v) for w in adj[v] if w!=p))+')'
def centers(adj):
    n=len(adj); deg={v:len(adj[v]) for v in adj}; leaves=[v for v in adj if deg[v]<=1]; rem=n; removed=set()
    while rem>2:
        nl=[]
        for v in leaves:
            removed.add(v); rem-=1
            for w in adj[v]:
                if w not in removed:
                    deg[w]-=1
                    if deg[w]==1: nl.append(w)
        leaves=nl
    return [v for v in adj if v not in removed]
def canon(adj):
    return min(canon_rooted(adj,c,None) for c in centers(adj))
def grow(maxn):
    lv={1:{'()':{0:[]}}}
    for n in range(2,maxn+1):
        d={}
        for adj in lv[n-1].values():
            for v in adj:
                if len(adj[v])<4:
                    a={k:list(x) for k,x in adj.items()}; a[n-1]=[v]; a[v].append(n-1)
                    c=canon(a)
                    if c not in d: d[c]=a
        lv[n]=d
    return lv
lv=grow(14)
cnt=[len(lv[n]) for n in range(1,15)]
print('alkane isomers n=1..14',cnt)
# 알켄: (나무, 2중 결합 변) 쌍
def alkenes(n):
    seen={}; stereo=0
    for adj in lv[n].values():
        for v in adj:
            for w in adj[v]:
                if v<w and len(adj[v])<=3 and len(adj[w])<=3:
                    # 정규형: 변을 가운데 두고 양쪽 뿌리 문자열
                    a=canon_rooted(adj,v,w); b=canon_rooted(adj,w,v); key=min(a+'='+b,b+'='+a)
                    # 같은 골격을 다른 표지로 두 번 세지 않도록 전체 정규형 포함
                    k2=(canon(adj),key)
                    if k2 in seen: continue
                    def subs(x,y):
                        s=[canon_rooted(adj,u,x) for u in adj[x] if u!=y]
                        s+=['H']*(2-len(s)); return s
                    sv=subs(v,w); sw=subs(w,v)
                    ct = sv[0]!=sv[1] and sw[0]!=sw[1]
                    seen[k2]=ct
    tot=sum(2 if c else 1 for c in seen.values())
    return len(seen),tot
for n in (2,3,4,5,6): print('C%dH%d'%(n,2*n),'constitutional',*alkenes(n))
