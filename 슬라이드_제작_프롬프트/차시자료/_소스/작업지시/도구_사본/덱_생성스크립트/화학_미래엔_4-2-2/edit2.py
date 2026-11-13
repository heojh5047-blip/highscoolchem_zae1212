import sys,re
p='tpl.html'; s=open(p,encoding='utf-8').read()
a=s.index('<table class="tight cm422-err mt8">'); b=s.index('</table>',a)+len('</table>')
new='''<table class="tight cm422-err mt8">
    <tr><th>원인</th><th>함량(%)이 크게 나온 경우</th><th>함량(%)이 작게 나온 경우</th></tr>
    <tr><td>식초의 희석</td><td class="l">물을 적게 넣어 <span class="blank"><span class="step">덜 묽힘</span></span></td><td class="l">물을 많이 넣어 <span class="blank"><span class="step">더 묽힘</span></span></td></tr>
    <tr><td>식초의 부피</td><td class="l">피펫으로 계획한 10 mL보다 <b>많이</b> 넣음</td><td class="l">피펫으로 계획한 10 mL보다 <b>적게</b> 넣음</td></tr>
    <tr><td>뷰렛 사용</td><td class="l">꼭지 아래쪽 공기를 빼지 않아 $V'$이 크게 측정됨</td><td class="l">조작 중 용액을 흘려 $V'$이 작게 측정됨</td></tr>
    <tr><td>중화점 판단</td><td class="l">중화점을 <span class="blank"><span class="step">지난 뒤</span></span>까지 넣음</td><td class="l">중화점에 <span class="blank"><span class="step">도달하기 전</span></span>에 멈춤</td></tr>
  </table>'''
s=s[:a]+new+s[b:]
R=[('<div class="col"><p class="f21 step">→ 두 식초를 <b>같은 부피</b>씩 덜어 같은 비율로 묽히고, 페놀프탈레인을 넣어 <b>같은 표준 용액</b>으로 적정한다.</p>\n          <p class="f21 step mt8">→ 중화점까지 넣은 부피가 큰 식초(A)에 아세트산이 더 많다.</p>',
'<div class="col"><p class="f21 step">→ (예시) 두 식초를 같은 양씩 담고 <b>마그네슘</b> 조각을 넣으면 기포가 더 활발하게 발생하는 쪽의 산성도가 크다.</p>\n          <p class="f21 step mt8">→ 또는 <b>같은 부피</b>를 같은 표준 용액으로 적정하면, 중화점까지 넣은 부피가 큰 식초(A)에 아세트산이 더 많다.</p>')]
for x,y in R:
    if s.count(x)!=1: sys.exit('miss '+x[:50])
    s=s.replace(x,y)
open(p,'w',encoding='utf-8').write(s); print('ok')
