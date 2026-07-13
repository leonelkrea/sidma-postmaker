import json, html

assets = json.load(open("post_engine/assets.json"))
lib = open("post_engine/html-to-image.js", encoding="utf-8").read()
logo_svg = assets["logo_svg"]

slides = [
    {"type":"cover","kicker":"SIDMA MOOT · 7ª EDICIÓN",
     "title":'¿Qué necesitas para participar en <span class="accent">SIDMA Moot</span>?',
     "sub":"Menos de lo que crees. Estos son los requisitos."},
    {"type":"req","num":"1","text":"Ser mayor de 18 años al momento de la inscripción y estudiante de Derecho o carreras afines."},
    {"type":"req","num":"2","text":"Tener interés en los medios alternativos de resolución de conflictos: la mediación y el arbitraje."},
    {"type":"req","num":"3","text":"Querer desarrollar habilidades de oratoria, redacción y análisis jurídico. Aquí las pones en práctica frente a árbitros en ejercicio."},
    {"type":"req","num":"4","text":"Llenar el formulario de preinscripción, pagar la tarifa de inscripción y completar los datos de cada participante para tu certificado."},
    {"type":"cta","kicker":"INSCRIPCIONES ABIERTAS","title":"Eso es todo.",
     "url":"experienciasidma.com/inscripcion/","sub":"Asegura tu lugar en la 7ª edición."},
]

DECO = ('<div class="deco d1"></div><div class="deco d2"></div>'
        '<div class="deco d3"></div><div class="ring r1"></div><div class="ring r2"></div>')

def slide_html(i, s):
    n = i + 1
    footer = f'<div class="footer"><div class="logo">{logo_svg}</div><div class="counter">{n} / 6</div></div>'
    if s["type"] == "cover":
        body = (f'<div class="content cover">'
                f'<div class="kicker">{s["kicker"]}</div>'
                f'<h1 class="cover-title">{s["title"]}</h1>'
                f'<p class="cover-sub">{s["sub"]}</p>'
                f'<div class="swipe">Desliza para ver los requisitos <span>→</span></div>'
                f'</div>')
    elif s["type"] == "req":
        body = (f'<div class="content req">'
                f'<div class="kicker">REQUISITO</div>'
                f'<div class="req-num">{s["num"]}</div>'
                f'<div class="req-bar"></div>'
                f'<p class="req-text">{html.escape(s["text"])}</p>'
                f'</div>')
    else:
        body = (f'<div class="content cta">'
                f'<div class="kicker">{s["kicker"]}</div>'
                f'<h2 class="cta-title">{s["title"]}</h2>'
                f'<div class="cta-url">{s["url"]}</div>'
                f'<p class="cta-sub">{s["sub"]}</p>'
                f'</div>')
    return f'<div class="slide slide-{s["type"]}" id="slide-{n}">{DECO}{body}{footer}</div>'

cards = []
for i, s in enumerate(slides):
    n = i + 1
    cards.append(f'''<div class="card">
  <div class="preview"><div class="scaler">{slide_html(i, s)}</div></div>
  <div class="controls">
    <button class="btn dl" onclick="downloadSlide({n})">⬇ Descargar PNG</button>
    <button class="btn cp" onclick="copySlide({n})">⧉ Copiar</button>
  </div>
</div>''')
cards_html = "\n".join(cards)

CSS = """
:root{ --navy:#0C1657; --green:#00BF90; --teal:#048D7F; }
@font-face{font-family:'Luxia Display';src:url(data:font/otf;base64,__LUXD__) format('opentype');font-weight:normal;}
@font-face{font-family:'Luxia Regular';src:url(data:font/otf;base64,__LUXR__) format('opentype');}
@font-face{font-family:'Montserrat';src:url(data:font/ttf;base64,__MONT__) format('truetype');font-weight:100 900;}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0a0e2a;font-family:'Montserrat',sans-serif;color:#fff;padding:40px 24px 80px;}
"""
CSS = (CSS.replace("__LUXD__", assets["luxia_display"])
          .replace("__LUXR__", assets["luxia_regular"])
          .replace("__MONT__", assets["montserrat"]))

JS = """
const OPTS={width:1080,height:1080,pixelRatio:1,cacheBust:true,style:{transform:'none',margin:'0'}};
async function downloadAll(){for(let n=1;n<=6;n++){const b=await htmlToImage.toBlob(document.getElementById('slide-'+n),OPTS);const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='sidma_moot_slide_'+n+'.png';document.body.appendChild(a);a.click();a.remove();await new Promise(r=>setTimeout(r,400));}}
"""

HTML = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>Carrusel SIDMA Moot</title>
<style>{CSS}</style></head>
<body>
<div class="gallery">
{cards_html}
</div>
<script>{lib}</script>
<script>{JS}</script>
</body></html>"""

open("post_engine/carrusel_sidma_moot.html","w",encoding="utf-8").write(HTML)
print("OK ->", "post_engine/carrusel_sidma_moot.html")
import os;print("size:", round(os.path.getsize("post_engine/carrusel_sidma_moot.html")/1024), "KB")
