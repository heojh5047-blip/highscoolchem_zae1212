p='tpl.html'; s=open(p,encoding='utf-8').read()
R=[('설계 예시 — 모둠마다 금속판 짝을 바꾼다(아연–구리, 마그네슘–아연 …). 한 가지 전해질(볼타 전지 꼴)과 반쪽 전지 연결(다니엘 전지 꼴) 중 하나를 골라 비교해도 좋다.',
    '설계 예시 — 모둠마다 금속판 짝을 바꾼다(아연–구리, 마그네슘–아연 …).'),
('→ <b>예시</b> 모둠 1의 마그네슘–구리 전지.','→ <b>예시</b> <span class="ans">모둠 1의 마그네슘–구리 전지</span>.'),
('<p class="f21 step mt8"><b>예시</b> (−)극: $\\ce{Zn(s)','<p class="small step mt8"><b>예시</b> (−)극: $\\ce{Zn(s)'),
('<p class="f21 step mt8">$E^\\circ_\\text{전지}=E^\\circ_\\text{환원 전극}','<p class="small step mt8">$E^\\circ_\\text{전지}=E^\\circ_\\text{환원 전극}'),
]
for a,b in R:
    n=s.count(a)
    if n!=1: print('MISS',n,a[:60]); continue
    s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s)
