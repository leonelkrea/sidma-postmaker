---
tags: [marca, visual, colores, tipografía]
relacionado: "[[brand_profile]]"
---

# Identidad Visual — SIDMA

> Fuente oficial: `/Volumes/ARC Reactor/Code Projects SSD/Borrar/social-media-manager/Style/`
> Ver también: [[brand_profile]] · [[Tono y Voz]]

---

## Paleta de Colores

| Nombre | Hex | RGB | Uso |
|---|---|---|---|
| **Navy Profundo** | `#0C1657` | 12, 22, 87 | Fondo principal, headers, texto de alto contraste |
| **Verde Vibrante** | `#00BF90` | 0, 191, 144 | CTA principal, highlights, estados de éxito |
| **Teal Oscuro** | `#048D7F` | 4, 141, 127 | Acentos secundarios, hover, botones secundarios |
| **Blanco** | `#FFFFFF` | 255, 255, 255 | Texto sobre fondos oscuros, tarjetas |

### Reglas de Uso
- Texto sobre fondo blanco → usar `#0C1657` o `#048D7F`
- Texto sobre fondo oscuro/gradiente → usar `#FFFFFF`
- **Nunca** texto negro puro sobre fondos de marca

---

## Gradientes Oficiales

### Gradiente Vertical (uso principal en posts)
```css
background: linear-gradient(to bottom, #0C1657 0%, #00BF90 100%);
```
```tailwind
bg-gradient-to-b from-[#0C1657] to-[#00BF90]
```

### Gradiente Horizontal
```css
background: linear-gradient(to right, #0C1657 0%, #00BF90 100%);
```
```tailwind
bg-gradient-to-r from-[#0C1657] to-[#00BF90]
```

---

## Tipografías

| Fuente | Peso | Archivo | Uso |
|---|---|---|---|
| **Luxia Display** | Display | `Luxia-Display.otf` | Títulos principales, portadas, impacto visual |
| **Luxia Regular** | Regular | `Luxia-Regular.otf` | Subtítulos, texto de apoyo ligero |
| **Montserrat** | Variable (100–900) | `Montserrat-VariableFont_wght.ttf` | Cuerpo de texto, copies, UI |
| **Montserrat Italic** | Variable italic | `Montserrat-Italic-VariableFont_wght.ttf` | Énfasis, citas, variedad |

### Jerarquía Tipográfica Sugerida para Posts
```
Titular:     Luxia Display, grande y bold
Subtítulo:   Luxia Regular o Montserrat SemiBold
Cuerpo:      Montserrat Regular (400)
Énfasis:     Montserrat Bold (700) o Italic
```

---

## Logos

| Archivo | Descripción | Cuándo usar |
|---|---|---|
| `Logo white + Color.svg` | Logo con gradiente Navy→Verde | Aplicación principal, fondos oscuros |
| `Logo Monocolor.svg` | Logo todo blanco (233×68px) | Fondos de color sólido, uso restringido |
| `Icon Monocolor.svg` | Solo el ícono, sin wordmark (137×137px) | Perfil Instagram, favicon, badges |

---

## Aplicación en Contenido de Instagram

### Para slides con fondo de marca
```
Fondo:           Gradiente Navy→Verde (#0C1657 → #00BF90)
Texto principal: Blanco #FFFFFF, fuente Luxia Display
Texto cuerpo:    Blanco #FFFFFF, fuente Montserrat
Acento/dato:     Verde #00BF90 sobre Navy (si fondo es solo navy)
```

### Para slides informativos / glosario
```
Fondo:           Navy #0C1657
Encabezado:      Verde #00BF90, Luxia Display
Definición:      Blanco #FFFFFF, Montserrat Regular
```

### Para slides de noticias / temáticos
```
Estilo:          Periódico / revista → puede romper el esquema de marca
                 pero siempre incluir el ícono SIDMA como watermark
```

---

## Para el Agente IA — Cómo Describir Imágenes

Cuando el agente describe el contenido visual de un slide, usar este formato:

```
[IMAGEN/SLIDE N]
Fondo: [color o gradiente]
Titular: "[texto]" — Luxia Display, blanco
Subtítulo: "[texto]" — Montserrat SemiBold, blanco/verde
Ícono: [descripción si aplica]
Watermark: Logo SIDMA, esquina inferior derecha
```
