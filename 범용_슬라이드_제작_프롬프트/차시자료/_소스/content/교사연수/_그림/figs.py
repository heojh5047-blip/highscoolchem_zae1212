# 교사연수 덱 공용 그림(SVG 조각) — 직접 그린 그림. GHS 그림문자는 UN GHS 규격 꼴(빨간 마름모 테, 흰 바탕, 검은 상징)을 따라 다시 그림.
INK, PLUS, MINUS, FIELD, EQUI, GRAV, MUTED = '#16233D', '#D7263D', '#1F6FD1', '#2E9E6A', '#E08A2C', '#8C99A6', '#5B6B7F'
BF, OX, RD = '#7B4FC8', '#C2410C', '#0E7490'
GHS_RED = '#D52B2B'   # GHS: 빨간 테두리

_SYM = {
 # GHS01 폭발성: 가운데 작은 폭탄과 오른쪽 위로 흩어지는 파편·선
 '01': '<circle cx="45" cy="54" r="6.5"/>'
       '<g stroke="#000" stroke-width="1.3" stroke-linecap="round" fill="none">'
       '<path d="M49 50 L63 27 M50 51 L69 34 M51 52 L74 43 M52 54 L77 51 M51 57 L73 60 M48 59 L60 68 M41 58 L27 63 M40 55 L22 57 M41 52 L28 47 M46 60 L44 68 M47 48 L52 31 M43 49 L37 38"/></g>'
       '<path d="M56 30 l3 -3 l2 4 z M66 39 l4 -1 l-1 4 z M60 45 l3 0 l-1 3 z M70 57 l3 1 l-2 3 z M30 52 l-3 2 l3 2 z M36 43 l-2 -3 l4 0 z M59 64 l3 1 l-2 3 z M31 60 l-4 1 l2 3 z M64 33 l2 -3 l2 3 z"/>',
 # GHS02 인화성: 여러 갈래 불꽃 + 아래 막대
 '02': '<path d="M50 70 C38 70 32 63 33 54 C34 47 38 44 37 37 C42 41 43 46 43 50 C44 43 46 36 51 25 C52 33 56 37 58 43 C59 39 60 37 62 34 C65 41 68 47 67 55 C66 64 60 70 50 70 Z"/>'
       '<path d="M50 67 C45 67 42 63 43 58 C44 55 46 53 46 50 C48 53 49 55 49 58 C50 55 52 52 53 49 C55 53 57 56 56 60 C56 64 54 67 50 67 Z" fill="#fff"/>'
       '<rect x="34" y="74" width="32" height="4"/>',
 # GHS03 산화성: 고리(O) 위를 감싼 불꽃 + 아래 막대
 '03': '<path d="M34 60 C32 52 35 47 35 40 C39 43 40 46 41 49 C42 41 45 33 49 23 C50 31 53 35 55 40 C56 36 57 33 60 29 C64 37 67 44 66 52 C66 56 65 59 66 61 Z"/>'
       '<circle cx="50" cy="61" r="11.5" fill="#fff" stroke="#000" stroke-width="5.5"/>'
       '<rect x="34" y="75" width="32" height="4"/>',
 # GHS04 고압가스: 비스듬히 누운 가스 실린더(오른쪽 위에 목)
 '04': '<g transform="rotate(-13 50 52)"><rect x="22" y="46" width="44" height="12" rx="6"/><path d="M64 46.5 C69 47.5 71 49 74 49.5 V54.5 C71 55 69 56.5 64 57.5 Z"/><rect x="73.5" y="49" width="4.5" height="6" rx="1"/></g>',
 # GHS05 부식성: 위의 시험관 2개에서 떨어지는 액체 — 왼쪽 금속판, 오른쪽 손
 '05': '<g fill="#fff" stroke="#000" stroke-width="1.8"><g transform="rotate(-16 40 31)"><rect x="31" y="28.5" width="17" height="5.5" rx="2.75"/><path d="M31.5 31.2 h8" stroke-width="1.2"/></g>'
       '<g transform="rotate(16 60 31)"><rect x="52" y="28.5" width="17" height="5.5" rx="2.75"/><path d="M60.5 31.2 h8" stroke-width="1.2"/></g></g>'
       '<path d="M33 35 q1 3 -1 5 q-2 -2 1 -5 z M67 35 q-1 3 1 5 q2 -2 -1 -5 z"/>'
       '<g stroke="#000" stroke-width="1.6" stroke-linecap="round" fill="none"><path d="M33 43 v3 M67 43 v3"/>'
       '<path d="M30 53 c-1 -2 1 -3 0 -5 M34 52 c-1 -2 1 -3 0 -5 M38 53 c-1 -2 1 -3 0 -5 M62 52 c-1 -2 1 -3 0 -5 M66 51 c-1 -2 1 -3 0 -5 M70 52 c-1 -2 1 -3 0 -5"/></g>'
       '<path d="M24 55.5 H44 V60.5 H24 Z"/><path d="M30 55.5 l2 2 l2 -2 z M36 55.5 l1.5 1.5 l1.5 -1.5 z" fill="#fff"/>'
       '<path d="M57 57 C59 54 64 54 67 56 L75 56 C76.5 56 76.5 58 75 58 L69 58 L74 59 C75.5 59 75.5 61 74 61 L68 61 L72 62 C73.5 62 73.5 64 72 64 L62 64 C59 64 57 61 57 57 Z" fill="#fff" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>',
 # GHS06 급성 독성: 윤곽선 해골과 엇갈린 뼈
 '06': '<g fill="#fff" stroke="#000" stroke-width="2" stroke-linejoin="round">'
       '<path d="M30 57 L70 75 M30 75 L70 57" stroke-width="5.2" stroke-linecap="round"/>'
       '<path d="M30 57 L70 75 M30 75 L70 57" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
       '<circle cx="28.5" cy="55" r="2.3"/><circle cx="27" cy="58.5" r="2.3"/><circle cx="71.5" cy="77" r="2.3"/><circle cx="73" cy="73.5" r="2.3"/>'
       '<circle cx="71.5" cy="55" r="2.3"/><circle cx="73" cy="58.5" r="2.3"/><circle cx="28.5" cy="77" r="2.3"/><circle cx="27" cy="73.5" r="2.3"/>'
       '<path d="M50 30 C42 30 38 35 38 41.5 C38 45.5 40 48 43 49.5 V55.5 H57 V49.5 C60 48 62 45.5 62 41.5 C62 35 58 30 50 30 Z"/></g>'
       '<ellipse cx="45.5" cy="42" rx="3.4" ry="3.8"/><ellipse cx="54.5" cy="42" rx="3.4" ry="3.8"/><path d="M50 45.5 l-1.8 3.2 h3.6 z"/>'
       '<path d="M46.5 51 v4.5 M50 51 v4.5 M53.5 51 v4.5" stroke="#000" stroke-width="1.2"/>',
 # GHS07 경고: 느낌표
 '07': '<path d="M44.5 27 C44.5 22 55.5 22 55.5 27 L52.5 58 H47.5 Z"/><circle cx="50" cy="66.5" r="5"/>',
 # GHS08 건강 유해성: 사람 상반신과 가슴의 흰 별 모양 균열
 '08': '<path d="M50 21 C44.5 21 42 25.5 42 31 C42 36.5 44.5 40.5 47 42 V44.5 C39 45.5 32 48.5 28.5 54 C30 64 38 74 50 81 C62 74 70 64 71.5 54 C68 48.5 61 45.5 53 44.5 V42 C55.5 40.5 58 36.5 58 31 C58 25.5 55.5 21 50 21 Z"/>'
       '<g stroke="#fff" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" fill="none">'
       '<path d="M50 59 L47 50 L49 46 M50 59 L54 51 L53 46 M50 59 L40 54 L34 55 M50 59 L60 54 L66 54 M50 59 L41 64 L36 70 M50 59 L59 65 L63 71 M50 59 L48 68 L50 76 M50 59 L53 67"/></g>'
       '<path d="M50 54 l1.6 3.4 l3.6 .6 l-2.7 2.5 l.6 3.6 l-3.1 -1.8 l-3.1 1.8 l.6 -3.6 l-2.7 -2.5 l3.6 -.6 z" fill="#fff"/>',
 # GHS09 수생환경 유해성: 마른 나무, 수면 선, 죽은 물고기
 '09': '<g stroke="#000" stroke-linecap="round" fill="none">'
       '<path d="M36 64 V29" stroke-width="4.4"/><path d="M36 46 L27 36 M36 40 L44 29 M36 52 L45 44 M27 36 L26 30 M27 36 L22 34 M44 29 L47 25 M44 29 L49 31 M45 44 L50 41 M36 34 L32 27" stroke-width="2.2"/>'
       '<path d="M24 56 H60" stroke-width="2.8"/></g>'
       '<path d="M22 76 C30 70 38 68 44 69 C52 70 58 72 66 70 L74 74 V76 Z"/>'
       '<path d="M47 69 C49 62 57 57 65 56 L70 51 L71 59 C66 64 58 69 50 70 Z"/><path d="M53 65 l2 2 M55 65 l-2 2" stroke="#fff" stroke-width="1.2"/>',
}
GHS_NAME = {'01': '폭발성', '02': '인화성', '03': '산화성', '04': '고압가스', '05': '부식성',
            '06': '급성 독성', '07': '경고', '08': '건강 유해성', '09': '수생환경 유해성'}

def ghs_g(code, x=0, y=0, s=1.0):
    """GHS 그림문자 하나(<g>) — 원래 크기 100×100"""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M50 3 L97 50 L50 97 L3 50 Z" fill="#fff" stroke="{GHS_RED}" stroke-width="4.6" stroke-linejoin="miter"/>'
            f'<g fill="#000">{_SYM[code]}</g></g>')

def ghs_svg(code, px=96, extra=''):
    return (f'<svg viewBox="0 0 100 100" width="{px}" height="{px}" role="img" aria-label="GHS 그림문자 {GHS_NAME[code]}" data-audit="skip"{extra}>'
            + ghs_g(code) + '</svg>')

# 보호구·설비 아이콘 (64×64, 선 그림)
_IC = {
 'coat': '<path d="M22 10 L32 18 L42 10 L54 18 L50 30 L46 28 V56 H18 V28 L14 30 L10 18 Z" fill="#fff"/><path d="M32 18 V56"/><path d="M24 38 h5 M35 38 h5"/>',
 'glove': '<path d="M20 56 V30 C20 26 26 26 26 30 V22 C26 18 32 18 32 22 V20 C32 16 38 16 38 20 V24 C38 20 44 20 44 24 V40 L50 34 C53 31 57 35 54 38 L44 52 V56 Z" fill="#E8F1FB"/>',
 'goggle': '<path d="M8 28 C8 22 14 20 20 20 H44 C50 20 56 22 56 28 V36 C56 42 50 44 44 44 C38 44 36 38 32 38 C28 38 26 44 20 44 C14 44 8 42 8 36 Z" fill="#E8F1FB"/><path d="M8 30 H4 M56 30 H60"/>',
 'mask': '<path d="M14 26 C14 20 50 20 50 26 V38 C50 48 40 52 32 52 C24 52 14 48 14 38 Z" fill="#fff"/><path d="M14 30 L6 26 M50 30 L58 26 M14 38 L6 42 M50 38 L58 42"/><circle cx="32" cy="38" r="6" fill="#E8F1FB"/>',
 'eyewash': '<path d="M14 54 H50 M32 54 V36"/><path d="M20 36 H44 L40 28 H24 Z" fill="#E8F1FB"/><path d="M26 22 C26 16 30 14 30 10 M38 22 C38 16 34 14 34 10" stroke="#1F6FD1"/>',
 'ext': '<rect x="22" y="20" width="20" height="36" rx="6" fill="#FDF1F3" stroke="#D7263D"/><path d="M28 20 V14 H38 M38 14 L48 18 M32 14 V10"/><rect x="26" y="30" width="12" height="10" rx="2" fill="#fff" stroke="#D7263D"/>',
 'shower': '<path d="M14 58 V10 H40 V18"/><path d="M30 18 H50 L46 24 H34 Z" fill="#E8F1FB"/><path d="M36 30 l-2 6 M40 30 v6 M44 30 l2 6 M38 42 l-1 5 M42 42 l1 5" stroke="#1F6FD1"/><path d="M28 58 H52"/>',
 'fan': '<circle cx="32" cy="32" r="22" fill="#fff"/><path d="M32 32 C30 20 38 14 42 18 C44 24 36 28 32 32 C44 32 48 40 44 44 C38 46 34 38 32 32 C24 42 16 40 16 34 C18 28 26 30 32 32 Z" fill="#E8F1FB"/><circle cx="32" cy="32" r="3"/>',
 'battery': '<rect x="12" y="18" width="36" height="28" rx="5" fill="#fff"/><rect x="48" y="26" width="5" height="12" rx="1"/><path d="M28 24 L22 34 H30 L26 42" stroke="#E08A2C"/>',
 'sensor': '<rect x="12" y="10" width="22" height="20" rx="4" fill="#E8F1FB"/><path d="M23 30 V54"/><circle cx="23" cy="56" r="3" fill="#16233D"/><path d="M34 20 C44 20 46 30 52 30"/><path d="M44 46 H58 M46 50 H56" stroke="#1F6FD1"/>',
 'printer': '<rect x="10" y="12" width="44" height="40" rx="4" fill="#fff"/><path d="M10 22 H54"/><path d="M26 22 V30 H38 V22"/><path d="M22 48 H42 L38 40 H26 Z" fill="#E8F1FB"/>',
}
def icon(name, px=64, stroke=INK):
    return (f'<svg viewBox="0 0 64 64" width="{px}" height="{px}" aria-hidden="true" data-audit="skip">'
            f'<g fill="none" stroke="{stroke}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{_IC[name]}</g></svg>')
