import json
assets = json.load(open("carrusel_export/assets.json"))
lib = open("carrusel_export/html-to-image.js", encoding="utf-8").read()
svgs = json.load(open("carrusel_export/slides_svg.json"))

CSS = """
@font-face{font-family:'Montserrat';src:url(data:font/ttf;base64,__MONT__) format('truetype');font-weight:100 900;}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0a0e2a;font-family:'Montserrat',sans-serif;color:#fff;padding:40px 24px 90px;}
.head{max-width:1200px;margin:0 auto 30px;}
.head h1{font-weight:800;font-size:30px;}
.head p{color:#b9c0e0;font-size:14px;margin-top:10px;line-height:1.6;max-width:820px;}
.head code{background:#1a1f45;padding:2px 7px;border-radius:6px;color:#7fe9cf;font-size:13px;}
.head .all{margin-top:16px;background:#048D7F;color:#fff;border:none;border-radius:10px;padding:11px 20px;font-weight:600;cursor:pointer;font-size:14px;}
.gallery{display:flex;flex-wrap:wrap;gap:34px;max-width:1200px;margin:0 auto;justify-content:center;}
.card{display:flex;flex-direction:column;gap:12px;width:360px;}
.preview{width:360px;height:360px;border-radius:18px;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.45);background:#0C1657;}
.preview svg{width:360px;height:360px;display:block;}
.controls{display:flex;gap:8px;}
.btn{flex:1;border:none;border-radius:10px;padding:11px 6px;font-family:'Montserrat';font-weight:600;font-size:12.5px;cursor:pointer;transition:.15s;white-space:nowrap;}
.btn.dl{background:#00BF90;color:#04210a;}
.btn.dl:hover{background:#19d6a6;}
.btn.cp{background:#1c2250;color:#cdd4ff;}
.btn.cp:hover{background:#2a3170;}
.btn.fig{background:#7c5cff;color:#fff;}
.btn.fig:hover{background:#9277ff;}
#toast{position:fixed;left:50%;bottom:30px;transform:translateX(-50%) translateY(20px);background:#11163a;border:1px solid #2a3170;color:#eafff7;padding:13px 22px;border-radius:12px;font-weight:600;font-size:14px;opacity:0;pointer-events:none;transition:.25s;z-index:99;box-shadow:0 10px 30px rgba(0,0,0,.5);}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
""".replace("__MONT__", assets["montserrat"])

cards=[]
for i,svg in enumerate(svgs):
    n=i+1
    cards.append(f'''<div class="card">
  <div class="preview" id="prev-{n}">{svg}</div>
  <div class="controls">
    <button class="btn dl" onclick="dlPng({n})">⬇ PNG</button>
    <button class="btn cp" onclick="copyPng({n})">⧉ PNG</button>
    <button class="btn fig" onclick="copySvg({n})">⧉ SVG→Figma</button>
  </div>
</div>''')
cards_html="\n".join(cards)
svgs_js = json.dumps(svgs)

JS = """
const SVGS=__SVGS__;
function toast(m){const t=document.getElementById('toast');t.textContent=m;t.classList.add('show');clearTimeout(window.__t);window.__t=setTimeout(()=>t.classList.remove('show'),2400);}
function svgNode(n){return document.querySelector('#prev-'+n+' svg');}
const OPTS={width:1080,height:1080,pixelRatio:1,cacheBust:true,style:{width:'1080px',height:'1080px'}};
function dl(blob,name){const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500);}
async function blobOf(n){return await htmlToImage.toBlob(svgNode(n),OPTS);}
async function dlPng(n){toast('Generando PNG '+n+'…');dl(await blobOf(n),'sidma_moot_slide_'+n+'.png');toast('Slide '+n+' descargado ✓');}
async function copyPng(n){const b=await blobOf(n);try{if(navigator.clipboard&&window.ClipboardItem&&window.isSecureContext){await navigator.clipboard.write([new ClipboardItem({'image/png':b})]);toast('PNG '+n+' copiado ✓');return;}throw 0;}catch(e){toast('Copia de imagen no disponible aquí. Descargando…');dl(b,'sidma_moot_slide_'+n+'.png');}}
async function copySvg(n){const s=SVGS[n-1];try{await navigator.clipboard.writeText(s);toast('SVG '+n+' copiado ✓ — pega con Cmd+V en Figma');}catch(e){toast('No se pudo copiar (abre desde localhost).');}}
async function dlAll(){toast('Generando las 6…');for(let n=1;n<=6;n++){dl(await blobOf(n),'sidma_moot_slide_'+n+'.png');await new Promise(r=>setTimeout(r,400));}toast('6 PNG descargados ✓');}
"""
JS = JS.replace("__SVGS__", svgs_js)

HTML=f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carrusel SIDMA Moot — Requisitos</title><style>{CSS}</style></head>
<body>
<div class="head">
  <h1>Carrusel · ¿Qué necesitas para participar en SIDMA Moot?</h1>
  <p>6 slides 1080×1080 con la identidad de SIDMA. <b>⬇ PNG</b> descarga el slide · <b>⧉ PNG</b> copia la imagen · <b>⧉ SVG→Figma</b> copia el slide como SVG editable: pégalo con <b>Cmd+V dentro de Figma</b> y se convierte en capas (texto, formas) editables. Copiar requiere abrir desde <code>localhost</code>.</p>
  <button class="all" onclick="dlAll()">⬇ Descargar los 6 PNG</button>
</div>
<div class="gallery">
{cards_html}
</div>
<div id="toast"></div>
<script>{lib}</script>
<script>{JS}</script>
</body></html>"""
open("carrusel_export/carrusel_sidma_moot.html","w",encoding="utf-8").write(HTML)
import os;print("OK ->", round(os.path.getsize("carrusel_export/carrusel_sidma_moot.html")/1024),"KB")
