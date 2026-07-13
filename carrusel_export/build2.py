import json, html
assets = json.load(open("carrusel_export/assets.json"))
lib = open("carrusel_export/html-to-image.js", encoding="utf-8").read()

# logo svg inner (strip outer <svg ...> wrapper, keep paths)
logo_full = assets["logo_svg"].replace("\n","")
inner = logo_full[logo_full.index(">")+1 : logo_full.rindex("</svg>")]
LOGO_S = 230/233
LOGO_Y = 1080-74-67.124

W=1080; PADX=96
GRAD = ('<linearGradient id="g" x1="0" y1="0" x2="0" y2="1080" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#0C1657"/><stop offset="0.5" stop-color="#0B2268"/>'
        '<stop offset="0.82" stop-color="#047878"/><stop offset="1" stop-color="#00BF90"/></linearGradient>')
BLUR = '<filter id="b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="42"/></filter>'

def esc(s): return html.escape(s, quote=True)

def base(extra_defs="", deco="", body="", counter="1 / 6"):
    logo = f'<g transform="translate({PADX},{LOGO_Y:.1f}) scale({LOGO_S:.4f})">{inner}</g>'
    cnt = f'<text x="984" y="981" text-anchor="end" font-family="Montserrat" font-weight="600" font-size="26" letter-spacing="2" fill="#FFFFFF" fill-opacity="0.65">{counter}</text>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">'
            f'<defs>{GRAD}{BLUR}{extra_defs}</defs>'
            f'<rect width="1080" height="1080" fill="url(#g)"/>'
            f'{deco}{body}{logo}{cnt}</svg>')

def lines(arr, x, y0, lh, size, weight, fill, fop=1, ls=0, spans=None):
    t=(f'<text x="{x}" y="{y0}" font-family="Montserrat" font-weight="{weight}" font-size="{size}" '
       f'fill="{fill}" fill-opacity="{fop}"' + (f' letter-spacing="{ls}"' if ls else '') + '>')
    out=[]
    for i,ln in enumerate(arr):
        dy = 0 if i==0 else lh
        if spans and i in spans:
            # spans[i] = list of (text, fill)
            parts="".join(f'<tspan fill="{f}">{esc(tx)}</tspan>' for tx,f in spans[i])
            out.append(f'<tspan x="{x}" dy="{dy}">{parts}</tspan>')
        else:
            out.append(f'<tspan x="{x}" dy="{dy}">{esc(ln)}</tspan>')
    return t+"".join(out)+"</text>"

GREEN="#00BF90"; WHITE="#FFFFFF"; TEAL="#048D7F"; NAVY="#0C1657"

def deco_std(extra_ring=False):
    d=(f'<ellipse cx="1000" cy="60" rx="280" ry="280" fill="{GREEN}" fill-opacity="0.15" filter="url(#b)"/>'
       f'<ellipse cx="50" cy="980" rx="210" ry="210" fill="{TEAL}" fill-opacity="0.24" filter="url(#b)"/>')
    if extra_ring:
        d+=f'<circle cx="1010" cy="770" r="150" fill="none" stroke="{WHITE}" stroke-opacity="0.12" stroke-width="2"/>'
    return d

def cover():
    k=lines(["SIDMA MOOT · 7ª EDICIÓN"],PADX,300,0,25,600,GREEN,1,5)
    title=lines(["¿Qué necesitas","para participar en","SIDMA Moot?"],PADX,372,97,92,800,WHITE,1,0,
                spans={2:[("SIDMA Moot",GREEN),("?",WHITE)]})
    sub=lines(["Menos de lo que crees. Estos son los","requisitos."],PADX,665,56,40,400,WHITE,0.85)
    sw=lines(["Desliza para ver los requisitos  →"],PADX,888,0,27,500,WHITE,0.7)
    return base(deco=deco_std(True), body=k+title+sub+sw, counter="1 / 6")

def req(num, txt_lines, size, counter):
    k=lines(["REQUISITO"],PADX,250,0,25,600,GREEN,1,6)
    n=lines([num],PADX,470,0,300,900,GREEN)
    bar=f'<rect x="{PADX}" y="505" width="120" height="7" rx="4" fill="{GREEN}"/>'
    lh = round(size*1.32)
    t=lines(txt_lines,PADX,600,lh,size,600,WHITE)
    return base(deco=deco_std(), body=k+n+bar+t, counter=counter)

def cta():
    k=lines(["INSCRIPCIONES ABIERTAS"],PADX,360,0,25,600,GREEN,1,5)
    title=lines(["Eso es todo."],PADX,470,0,104,900,WHITE)
    url_txt="experienciasidma.com/inscripcion/"
    pill_w = int(len(url_txt)*42*0.545)+76
    pill=(f'<rect x="{PADX}" y="512" width="{pill_w}" height="86" rx="18" fill="{GREEN}"/>'
          f'<text x="{PADX+38}" y="568" font-family="Montserrat" font-weight="700" font-size="42" fill="{NAVY}">{esc(url_txt)}</text>')
    sub=lines(["Asegura tu lugar en la 7ª edición."],PADX,665,0,44,400,WHITE,0.9)
    return base(deco=deco_std(True), body=k+title+pill+sub, counter="6 / 6")

slides=[
  cover(),
  req("1",["Ser mayor de 18 años al","momento de la inscripción y","estudiante de Derecho o","carreras afines."],54,"2 / 6"),
  req("2",["Tener interés en los medios","alternativos de resolución de","conflictos: la mediación y el","arbitraje."],54,"3 / 6"),
  req("3",["Querer desarrollar habilidades de","oratoria, redacción y análisis jurídico.","Aquí las pones en práctica frente a","árbitros en ejercicio."],48,"4 / 6"),
  req("4",["Llenar el formulario de preinscripción,","pagar la tarifa de inscripción y","completar los datos de cada","participante para tu certificado."],48,"5 / 6"),
  cta(),
]
json.dump(slides, open("carrusel_export/slides_svg.json","w"))
print("OK", len(slides), "svgs; sizes:", [len(s) for s in slides])
