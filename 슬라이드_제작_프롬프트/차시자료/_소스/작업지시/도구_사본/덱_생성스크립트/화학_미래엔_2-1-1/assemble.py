import re
old=open('tplA.html',encoding='utf-8').read()+open('tplB.html',encoding='utf-8').read()
parts=re.split(r'(?=<!-- ════════ \d+\.)',old)
B={}
for p in parts:
    m=re.match(r'<!-- ════════ (\d+)\.',p)
    if m: B[int(m.group(1))]=p.strip()+'\n'
new={}
for fn in ('new1.html','new2.html'):
    t=open(fn,encoding='utf-8').read()
    for m in re.finditer(r'<!--#(N\d+)-->\n(.*?)(?=<!--#N\d+-->|\Z)',t,re.S): new[m.group(1)]=m.group(2).strip()+'\n'
def R(k,a,b,cnt=1):
    assert a in B[k], (k,a[:40]); B[k]=B[k].replace(a,b,cnt)
SEC='01 · 화학 결합의 전기적 성질'
# 7
R(7,'data-sec="01 · 물의 전기 분해"',f'data-sec="{SEC}"'); R(7,'<span class="no">1</span>물의 전기 분해','<span class="no">2</span>화학 결합의 전기적 성질: 물의 전기 분해')
R(7,'모인 기체의 부피는 (−)극 : (+)극 = <b>2 : 1</b>이다.','기체의 부피비는 (+)극 : (−)극 = <b>1 : 2</b>이다.')
R(7,'(긴 판이 (+)극). 전자는 도선을 따라 (+)극 → 전원 장치 → (−)극으로 이동한다.','(긴 판이 (+)극). 전자는 도선을 따라 (+)극 → 전원 → (−)극으로 이동한다.')
R(7,'연결된 전원 장치의 극','연결된 전원(건전지)의 극')
# 10
R(10,'value="6" data-i="v"','value="9" data-i="v"'); R(10,'<th>부피비 (−) : (+)</th>','<th>부피비 (+) : (−)</th>')
R(10,'<th>(−)극</th><th>(+)극</th>','<th>(+)극</th><th>(−)극</th>')
R(10,'<tr><th>(−)극 기체 부피</th><td><output data-o="vm"></output></td></tr>\n        <tr><th>(+)극 기체 부피</th><td><output data-o="vp"></output></td></tr>','<tr><th>(+)극 기체 부피</th><td><output data-o="vp"></output></td></tr>\n        <tr><th>(−)극 기체 부피</th><td><output data-o="vm"></output></td></tr>')
R(10,'data-act="h2">(−)극 기체에 성냥불','data-act="h2">성냥불 (−)극'); R(10,'data-act="o2">(+)극 기체에 향불','data-act="o2">향불 (+)극')
# 13
R(13,'data-sec="01 · 물의 전기 분해"',f'data-sec="{SEC}"'); R(13,'<span class="no">1</span>','<span class="no">2</span>')
R(13,'<p>원자는 그대로, 짝만 바뀐다: $\\mathrm{H}$ 4 = 4, $\\mathrm{O}$ 2 = 2</p>','<p>빨강 $\\mathrm{O}$, 흰색 $\\mathrm{H}$ — 원자는 그대로, 짝만 바뀐다: $\\mathrm{H}$ 4 = 4, $\\mathrm{O}$ 2 = 2</p>')
R(13,'  </div>\n</section>','  </div>\n  <p class="f21 mt12" data-q><b>Q</b> 물에 전기 에너지를 가하면 분해되는 것은 무엇을 뜻할까?</p>\n  <div class="answer step">수소 원자와 산소 원자 사이의 결합이 끊어진다 → 결합을 형성할 때 <b>전자가 관여</b>하며, 이 결합에는 <b>전기적 성질</b>이 있다.</div>\n</section>')
# 15
R(15,'수소 : 산소 = 2 : 1이다.','산소 : 수소 = 1 : 2이다.')
# 18
R(18,'data-sec="01 · 확인하기"',f'data-sec="{SEC}"'); R(18,'<span class="tag q">확인하기</span>','<span class="no">2</span>')
# 16
R(16,'data-sec="01 · 염화 나트륨의 전기 분해" data-title="염화 나트륨의 전기 분해"',f'data-sec="{SEC}" data-title="염화 나트륨 용융액의 전기 분해"')
R(16,'<span class="no">2</span>염화 나트륨의 전기 분해','<span class="no">2</span>염화 나트륨 용융액의 전기 분해')
R(16,'<p class="f22" data-q><b>Q</b> 이온으로 이루어진 염화 나트륨도 전기 분해될까?</p>','<p class="f22">이온 결합 물질인 염화 나트륨도 액체 상태(용융액)에서는 전기 분해할 수 있다.</p>')
R(16,'<p class="f22">염화 나트륨을 가열하여 녹인 뒤 전류를 흘려 준다.</p>','<p class="f22" data-q><b>Q</b> 염화 나트륨 용융액에 전류를 흘려 주면 각 전극에서 무엇이 생길까?</p>')
# 17
R(17,'data-sec="01 · 염화 나트륨의 전기 분해"',f'data-sec="{SEC}"')
a=B[17].index('      <table class="tight cm211-half mt8">'); b=B[17].index('</table>',a)+len('</table>')
B[17]=B[17][:a]+'''      <div class="card mt8"><p class="f21"><b class="c-minus">(−)극</b> $\\ce{Na+}$이 전자를 얻어 <b>나트륨</b>이 된다.</p>
        <p class="f21 mt8"><b class="c-plus">(+)극</b> $\\ce{Cl-}$이 전자를 잃어 <b>염소</b> 기체가 된다.</p></div>'''+B[17][b:]
R(17,'이온 결합에도 <b>전자가 관여</b>한다.','나트륨과 염소가 결합을 형성할 때 <b>전자가 관여</b>한다.')
R(17,'<span class="no">2</span>이온의 이동과 전극 반응','<span class="no">2</span>이온의 이동과 전극에서의 변화'); R(17,'data-title="이온의 이동과 전극 반응"','data-title="이온의 이동"')
# 19
R(19,'data-sec="01 · 염화 나트륨의 전기 분해"',f'data-sec="{SEC}"')
R(19,'  <p class="f22 mt16 step" data-q><b>Q</b> 그런데 원자들은 왜 전자를 잃거나 얻거나 함께 나누어 결합할까? <span class="c-muted">→ 옥텟 규칙</span></p>\n','  <p class="f22 mt16 step">전기 분해로 <b>공유 결합</b>뿐만 아니라 <b>이온 결합</b>에도 전기적 성질이 있음을 확인할 수 있다.</p>\n')
R(19,'<p class="f22">$\\ce{Na+}$과 $\\ce{Cl-}$의 결합</p>','<p class="f22">$\\ce{Na+}$과 $\\ce{Cl-}$의 결합 (용융액)</p>')
order=[B[1],new['N2'],new['N3'],new['N4'],new['N5'],new['N6'],B[7],new['N8'],new['N9'],B[10],new['N11'],new['N12'],B[13],B[15],B[18],B[16],B[17],B[19]]+[new[k] for k in ('N20','N21','N22','N23','N24','N25','N26')]
open('slides.tpl.html','w',encoding='utf-8').write('\n'.join(order))
print(len(order))
