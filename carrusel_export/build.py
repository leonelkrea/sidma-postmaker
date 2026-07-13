import json, html

assets = json.load(open("carrusel_export/assets.json"))
lib = open("carrusel_export/html-to-image.js", encoding="utf-8").read()
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
.page-head{max-width:1180px;margin:0 auto 32px;}
.page-head h1{font-family:'Luxia Display';font-size:34px;font-weight:400;letter-spacing:.5px;}
.page-head p{color:#b9c0e0;font-size:15px;margin-top:10px;line-height:1.6;max-width:760px;}
.page-head .tools{margin-top:18px;display:flex;gap:12px;flex-wrap:wrap;}
.page-head code{background:#1a1f45;padding:3px 8px;border-radius:6px;color:#7fe9cf;font-size:13px;}
.gallery{display:flex;flex-wrap:wrap;gap:36px;max-width:1180px;margin:0 auto;justify-content:center;}
.card{display:flex;flex-direction:column;gap:14px;}
.preview{width:360px;height:360px;overflow:hidden;border-radius:18px;box-shadow:0 18px 50px rgba(0,0,0,.45);}
.scaler{width:1080px;height:1080px;transform:scale(.33333);transform-origin:top left;}
.controls{display:flex;gap:10px;}
.btn{flex:1;border:none;border-radius:10px;padding:12px 10px;font-family:'Montserrat';font-weight:600;font-size:14px;cursor:pointer;transition:.15s;}
.btn.dl{background:var(--green);color:#04210a;}
.btn.dl:hover{background:#19d6a6;}
.btn.cp{background:#1c2250;color:#cdd4ff;}
.btn.cp:hover{background:#2a3170;}
.btn-all{background:var(--teal);color:#fff;border:none;border-radius:10px;padding:12px 22px;font-weight:600;cursor:pointer;font-size:14px;}
.btn-all:hover{background:#05a394;}

/* ---------- SLIDE 1080x1080 ---------- */
.slide{position:relative;width:1080px;height:1080px;overflow:hidden;
  background:linear-gradient(158deg,#0C1657 0%,#0a275a 40%,#066a6c 74%,#00BF90 112%);
  font-family:'Montserrat';}
.deco{position:absolute;border-radius:50%;filter:blur(2px);}
.d1{width:520px;height:520px;top:-180px;right:-140px;background:radial-gradient(circle at 30% 30%,rgba(0,191,144,.35),rgba(0,191,144,0) 70%);}
.d2{width:380px;height:380px;bottom:-120px;left:-120px;background:radial-gradient(circle at 50% 50%,rgba(4,141,127,.40),rgba(4,141,127,0) 70%);}
.d3{width:160px;height:160px;top:140px;left:80px;background:radial-gradient(circle at 35% 35%,rgba(255,255,255,.14),rgba(255,255,255,0) 70%);}
.ring{position:absolute;border-radius:50%;border:2px solid rgba(255,255,255,.10);}
.r1{width:300px;height:300px;bottom:160px;right:-80px;}
.r2{width:120px;height:120px;top:60px;right:240px;border-color:rgba(0,191,144,.30);}

.content{position:absolute;inset:0;padding:96px 96px 0;display:flex;flex-direction:column;justify-content:center;z-index:2;}
.kicker{font-weight:700;font-size:25px;letter-spacing:5px;color:var(--green);text-transform:uppercase;margin-bottom:30px;}

/* cover */
.cover-title{font-family:'Luxia Display';font-weight:400;font-size:90px;line-height:1.04;color:#fff;letter-spacing:.5px;}
.cover-title .accent{color:var(--green);}
.cover-sub{margin-top:34px;font-size:40px;line-height:1.4;color:rgba(255,255,255,.85);font-weight:400;max-width:780px;}
.swipe{position:absolute;left:96px;bottom:150px;font-size:26px;color:rgba(255,255,255,.7);font-weight:500;letter-spacing:.5px;}
.swipe span{color:var(--green);font-weight:700;margin-left:6px;}

/* requisito */
.req-num{font-family:'Luxia Display';font-size:300px;line-height:.82;color:var(--green);text-shadow:0 8px 40px rgba(0,191,144,.25);}
.req-bar{width:120px;height:7px;border-radius:4px;background:var(--green);margin:18px 0 40px;}
.req-text{font-size:54px;line-height:1.32;font-weight:600;color:#fff;max-width:880px;}

/* cta */
.cta-title{font-family:'Luxia Display';font-weight:400;font-size:104px;color:#fff;}
.cta-url{display:inline-block;margin:42px 0 0;background:var(--green);color:#04210a;font-weight:700;
  font-size:42px;padding:22px 38px;border-radius:18px;letter-spacing:.3px;align-self:flex-start;}
.cta-sub{margin-top:40px;font-size:44px;color:rgba(255,255,255,.9);font-weight:400;}

.footer{position:absolute;left:96px;right:96px;bottom:74px;display:flex;align-items:center;justify-content:space-between;z-index:2;}
.footer .logo svg{width:230px;height:auto;display:block;opacity:.95;}
.counter{font-size:26px;font-weight:600;color:rgba(255,255,255,.65);letter-spacing:2px;}

#toast{position:fixed;left:50%;bottom:34px;transform:translateX(-50%) translateY(20px);background:#11163a;
  border:1px solid #2a3170;color:#eafff7;padding:14px 24px;border-radius:12px;font-weight:600;font-size:15px;
  opacity:0;pointer-events:none;transition:.25s;z-index:99;box-shadow:0 10px 30px rgba(0,0,0,.5);}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
"""
CSS = (CSS.replace("__LUXD__", assets["luxia_display"])
          .replace("__LUXR__", assets["luxia_regular"])
          .replace("__MONT__", assets["montserrat"]))

JS = """
const OPTS={width:1080,height:1080,pixelRatio:1,cacheBust:true,style:{transform:'none',margin:'0'}};
function toast(m){const t=document.getElementById('toast');t.textContent=m;t.classList.add('show');
  clearTimeout(window.__tt);window.__tt=setTimeout(()=>t.classList.remove('show'),2200);}
function dl(blob,name){const u=URL.createObjectURL(blob);const a=document.createElement('a');
  a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500);}
async function blobOf(n){return await htmlToImage.toBlob(document.getElementById('slide-'+n),OPTS);}
async function downloadSlide(n){toast('Generando slide '+n+'…');const b=await blobOf(n);dl(b,'sidma_moot_slide_'+n+'.png');toast('Slide '+n+' descargado ✓');}
async function copySlide(n){
  const b=await blobOf(n);
  try{
    if(navigator.clipboard&&window.ClipboardItem&&window.isSecureContext){
      await navigator.clipboard.write([new ClipboardItem({'image/png':b})]);
      toast('Slide '+n+' copiado al portapapeles ✓');return;
    }throw new Error('insecure');
  }catch(e){toast('Para copiar, abre desde localhost. Descargando en su lugar…');dl(b,'sidma_moot_slide_'+n+'.png');}
}
async function downloadAll(){toast('Generando las 6…');for(let n=1;n<=6;n++){const b=await blobOf(n);dl(b,'sidma_moot_slide_'+n+'.png');await new Promise(r=>setTimeout(r,400));}toast('6 slides descargados ✓');}
"""

HTML = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carrusel SIDMA Moot — ¿Qué necesitas para participar?</title>
<style>{CSS}</style></head>
<body>
<div class="page-head">
  <h1>Carrusel · ¿Qué necesitas para participar en SIDMA Moot?</h1>
  <p>6 slides en formato 1080×1080 con la identidad gráfica de SIDMA. Usa <b>Descargar PNG</b> para guardar cada slide, o <b>Copiar</b> para pegarlo directo (Instagram, Canva, chat). El botón <b>Copiar</b> requiere abrir esta página desde <code>localhost</code> (ver instrucciones del chat); la descarga funciona siempre.</p>
  <div class="tools"><button class="btn-all" onclick="downloadAll()">⬇ Descargar los 6 PNG</button></div>
</div>
<div class="gallery">
{cards_html}
</div>
<div id="toast"></div>
<script>{lib}</script>
<script>{JS}</script>
</body></html>"""

open("carrusel_export/carrusel_sidma_moot.html","w",encoding="utf-8").write(HTML)
print("OK ->", "carrusel_export/carrusel_sidma_moot.html")
import os;print("size:", round(os.path.getsize("carrusel_export/carrusel_sidma_moot.html")/1024), "KB")
