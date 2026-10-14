from pathlib import Path
from xml.sax.saxutils import escape
import subprocess, io, json
from PIL import Image
import cairosvg
R=Path(__file__).parent
LINES=['A timetable is one of the most','critical documents that','kickstarts academic activities','in tertiary institutions.']
BASE='''<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="2160" viewBox="0 0 640 360">
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#152630"/><stop offset="1" stop-color="#080f16"/></linearGradient><linearGradient id="rim" x2="0" y2="1"><stop stop-color="#667781"/><stop offset="1" stop-color="#202e38"/></linearGradient><radialGradient id="glow"><stop stop-color="#258d86" stop-opacity=".22"/><stop offset="1" stop-color="#258d86" stop-opacity="0"/></radialGradient></defs>
<rect width="640" height="360" fill="url(#bg)"/>
<ellipse cx="165" cy="195" rx="245" ry="185" fill="url(#glow)"/>
<path d="M0 330 Q160 210 285 330 T640 300" stroke="#88d4c6" opacity=".045" stroke-width="40" fill="none"/>
<ellipse cx="169" cy="315" rx="125" ry="9" fill="#000" opacity=".3"/>
'''
SCREEN='''<rect x="25" y="66" width="286" height="228" rx="11" fill="url(#rim)"/>
<rect x="28" y="69" width="280" height="222" rx="9" fill="#09131c"/>
<rect x="35" y="77" width="266" height="204" rx="4" fill="#f8fbfc"/>
<rect x="35" y="77" width="266" height="29" rx="4" fill="#116f67"/>
<rect x="35" y="100" width="266" height="6" fill="#116f67"/>
<circle cx="48" cy="91" r="6" fill="#c7fff0"/>
<path d="M45 91l2 2 4-5" fill="none" stroke="#116f67" stroke-width="1.2"/>
<text x="60" y="94" font-family="Liberation Sans" font-weight="bold" font-size="10" fill="white">Academic Timetable</text>
<text x="47" y="119" font-family="Liberation Sans" font-size="7" fill="#52646c">SEMESTER 1</text>
<text x="290" y="119" text-anchor="end" font-family="Liberation Sans" font-size="7" fill="#52646c">WEEKLY SCHEDULE</text>
<rect x="44" y="128" width="248" height="135" rx="3" fill="#fff" stroke="#d4e1e4" stroke-width=".6"/>
<rect x="44" y="128" width="248" height="19" fill="#e8f1f2"/>
'''
cols=[('Time',65),('Mon',112),('Tue',152),('Wed',192),('Thu',232),('Fri',272)]
for name,x in cols:
 SCREEN+=f'<text x="{x}" y="140" text-anchor="middle" font-family="Liberation Sans" font-weight="bold" font-size="7" fill="#244b50">{name}</text>'
for x in [92,132,172,212,252]:
 SCREEN+=f'<path d="M{x} 128V263" stroke="#d4e1e4" stroke-width=".5"/>'
for i,time in enumerate(['08:00','09:00','10:00','11:00','12:00','13:00']):
 y=147+i*19.3
 SCREEN+=f'<path d="M44 {y}H292" stroke="#d4e1e4" stroke-width=".5"/><text x="65" y="{y+12}" text-anchor="middle" font-family="Liberation Sans" font-size="7" fill="#52646c">{time}</text>'
 # Clearly drawn sample course blocks; all text is vector, not a screen photograph.
 courses=['MAT 101','CSC 102','ENG 103','PHY 104','GST 105']
 for j in range(5):
  if (i+j)%4==0: continue
  x=94+j*40; color=['#d6f0e9','#dfebfb','#f8e8cf'][(i+j)%3]
  SCREEN+=f'<rect x="{x}" y="{y+2}" width="36" height="15" rx="2" fill="{color}"/><text x="{x+18}" y="{y+12}" text-anchor="middle" font-family="Liberation Sans" font-weight="bold" font-size="6.5" fill="#28434c">{courses[(i+j)%5]}</text>'
SCREEN+='''<circle cx="168" cy="287" r="1.7" fill="#88d4c6"/>
<path d="M154 294h28l5 15h-38z" fill="#3c505c"/>
<rect x="132" y="308" width="72" height="5" rx="2.5" fill="#607580"/>'''
def svg(t):
 a=min(1,max(0,t/.78))
 result=BASE+f'<g opacity="{a}">'+SCREEN+'</g>'
 for i,line in enumerate(LINES):
  delay=.13+.52*i/(len(LINES)-1)
  opacity=min(1,max(0,(t-delay)/.26))
  result+=f'<text x="332" y="{141+23*i}" font-family="Liberation Sans" font-size="20" font-weight="bold" fill="#f2f2f2" opacity="{opacity}">{escape(line)}</text>'
 return result+'</svg>'
(R/'composition.svg').write_text(svg(100))
p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size','3840x2160','-framerate','10','-i','-','-an','-c:v','libx264','-threads','4','-preset','medium','-b:v','20M','-minrate','20M','-maxrate','20M','-bufsize','40M','-x264-params','nal-hrd=cbr:force-cfr=1','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(R/'timetable-clear-4k.mp4')],stdin=subprocess.PIPE)
final=None
for frame in range(35):
 if frame>=10 and final is not None:
  image=final
 else:
  image=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg(frame/10).encode()))).convert('RGB')
  if frame==10: final=image
 if frame==34: image.save(R/'preview.png')
 p.stdin.write(image.tobytes())
p.stdin.close(); assert p.wait()==0
(R/'timing.json').write_text(json.dumps({'resolution':[3840,2160],'fps':10,'duration_seconds':3.5,'reveal_seconds':.78,'text_first_fully_visible_seconds':1,'final_hold_seconds':2.5,'text':' '.join(LINES),'graphics':'Entire scene rebuilt as vector SVG; timetable is illustrative.'},indent=2))
print('Rendered clean 4K video')
