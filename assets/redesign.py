from pathlib import Path
import re
p=Path('_site/index.html')
s=p.read_text(encoding='utf-8')
data=s[s.index('const DATA ='):s.index('// ── SCENE')]
panel=s[s.index('let currentPart = null;'):s.index('// ── LEGEND')]
colors={'頭臉頸':'#d78335','眼':'#268bd2','鼻':'#d49a24','口':'#d84a4a','耳':'#12a897','精神神經':'#9451d2','軀幹':'#5966cf','胸腹部臟器':'#cf5689','上肢':'#24a267','下肢':'#089ec4','皮膚':'#bd544e'}
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 650" aria-label="人體部位互動連線圖">']
def part(n,shapes):
    svg.append(f'<g data-part="{n}" role="button" tabindex="0" aria-label="查看{n}" fill="{colors[n]}" fill-opacity=".22" stroke="{colors[n]}" stroke-width="2">{shapes}</g>')
def rect(x,y,w,h,r=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
def ellipse(x,y,rx,ry):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>'
part('頭臉頸',ellipse(240,90,38,38)+rect(229,126,22,32))
part('皮膚','<path d="M190 158 Q240 143 290 158 L293 350 Q291 381 280 395 H200 Q188 375 187 350 Z"/>')
part('上肢',rect(161,168,23,220,11)+rect(296,168,23,220,11))
part('下肢',rect(204,393,33,219,16)+rect(243,393,33,219,16))
part('胸腹部臟器',ellipse(215,233,19,43)+ellipse(266,233,19,43)+ellipse(217,309,20,13)+ellipse(266,309,20,13)+ellipse(241,358,21,23))
part('軀幹',''.join(rect(236,y,9,22,4) for y in range(183,381,29)))
part('精神神經',ellipse(240,62,25,12))
part('耳',ellipse(202,91,5,12)+ellipse(278,91,5,12))
part('眼',ellipse(225,88,7,7)+ellipse(255,88,7,7))
part('鼻','<path d="M240 94 L235 105 H245 Z"/>')
part('口',ellipse(240,116,10,4))
labels=[('眼',8,66,225,88),('鼻',8,140,240,100),('口',8,214,240,116),('上肢',8,314,174,265),('軀幹',8,424,240,310),('下肢',8,534,220,492),('精神神經',340,34,250,59),('耳',340,108,277,90),('頭臉頸',340,182,250,141),('胸腹部臟器',340,328,268,233),('皮膚',340,460,288,363)]
for n,x,y,tx,ty in labels:
    c=colors[n]
    edge=x+132 if x==8 else x
    svg.append(f'<g class="map-label" data-part="{n}" role="button" tabindex="0" aria-label="查看{n}" style="color:{c}"><path d="M{edge} {y+22} L{tx} {ty}" fill="none" stroke="currentColor" opacity=".65"/><circle cx="{tx}" cy="{ty}" r="3" fill="currentColor"/><rect x="{x}" y="{y}" width="132" height="44" rx="20" fill="white" stroke="currentColor" stroke-width="2"/><text x="{x+66}" y="{y+23}" text-anchor="middle" dominant-baseline="middle" fill="currentColor" font-size="16" font-weight="600">{n}</text></g>')
svg.append('</svg>')
nav=''.join(f'<button type="button" data-part="{n}" style="border-color:{c}">{n}</button>' for n,c in colors.items())
layout='<section id="canvas-container"><header class="map-heading"><h1>勞工保險失能種類給付標準</h1><p>點選人體部位、連線標籤或按鈕查看給付資料</p></header><div class="body-map">'+''.join(svg)+'</div><nav class="part-picker" aria-label="全部11個失能部位">'+nav+'</nav><p class="map-note">人體位置為分類示意，非醫療診斷圖。</p></section>'
s=re.sub(r'<div id="canvas-container">.*?<div id="info-panel">',lambda m:layout+'<div id="info-panel">',s,count=1,flags=re.S)
s=re.sub(r'<script type="importmap">.*?</script>','',s,flags=re.S)
behavior='Object.assign(COLORS, {'+','.join('"'+n+'":0x'+c[1:] for n,c in colors.items())+'});'+"""
function choosePart(name){
 showInfo(name);
 document.querySelectorAll('[data-part]').forEach(el=>{const on=el.dataset.part===name;el.classList.toggle('selected',on);el.setAttribute('aria-pressed',String(on));});
 document.getElementById('panel-body').scrollTop=0;
 if(matchMedia('(max-width:767px)').matches) document.getElementById('info-panel').scrollIntoView({behavior:'smooth',block:'start'});
}
document.querySelectorAll('[data-part]').forEach(el=>{
 el.setAttribute('aria-pressed','false');
 el.addEventListener('click',()=>choosePart(el.dataset.part));
 if(el.tagName.toLowerCase()!=='button')el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choosePart(el.dataset.part);}});
});
"""
s=re.sub(r'<script type="module">.*?</script>',lambda m:'<script>'+data+panel+behavior+'</script>',s,count=1,flags=re.S)
css="""
#canvas-container{display:block;flex:1;height:100dvh;min-height:0;max-height:none;overflow-y:auto;padding:14px 12px;box-sizing:border-box;background:#fff}.map-heading{text-align:center;color:#194e82}.map-heading h1{font-size:20px;line-height:1.5}.map-heading p{font-size:13px;color:#62758b;line-height:1.7}.body-map{max-width:620px;margin:auto}.body-map svg{display:block;width:100%;height:auto;max-height:calc(100dvh - 200px);font-family:inherit}.body-map [data-part]{cursor:pointer}.body-map [data-part]:focus-visible{outline:3px solid #194e82}.map-label:hover rect,.map-label.selected rect{fill:#eaf3ff;stroke-width:3}.body-map g.selected{stroke-width:3.5}.part-picker{display:flex;flex-wrap:wrap;gap:7px;justify-content:center;max-width:640px;margin:8px auto;max-height:none;overflow:visible}.part-picker button{font:inherit;font-size:14px;min-height:44px;padding:8px 12px;border:1px solid;border-radius:10px;background:#fff;color:#31445a;cursor:pointer}.part-picker button.selected{background:#eaf3ff;box-shadow:inset 0 0 0 1px #194e82}.map-note{text-align:center;font-size:11px;color:#718398;margin:10px 0}
@media(max-width:767px){body{display:block;height:auto;overflow:auto}#canvas-container{width:100%;height:auto;min-height:0;max-height:none;overflow:visible;padding:16px 8px 8px}.map-heading h1{font-size:18px}.map-heading p{font-size:12px}.body-map svg{max-height:none}.part-picker button{flex:1 0 27%}#info-panel{width:100%;min-height:250px;overflow:visible;border-left:0;border-top:1px solid #dce5ef}#panel-body{overflow:visible}#placeholder{min-height:160px}}
"""
s=s.replace('</style>',css+'</style>',1).replace('勞保局失能種類互動3D圖','勞保失能種類人體互動連線圖').replace('請點選左側人形圖上的部位','請點選人體圖或部位按鈕').replace('🫁','')
assert 'new THREE.' not in s
assert len(re.findall('class="map-label"',s))==11
p.write_text(s,encoding='utf-8')
