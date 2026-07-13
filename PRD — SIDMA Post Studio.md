# PRD — SIDMA Post Studio

**Versión:** 1.0 · **Fecha:** 2026-07-13 · **Owner:** Leonel Pérez
**Estado:** Aprobado para Fase 0 y Fase 1; Fase 2 condicionada al éxito de Fase 1.

---

## 1. Visión

Convertir el ecosistema SIDMA (vault de marca + grid de aprobación + pipeline de render) en **el mejor creador de posts de Instagram por prompts**: escribes un prompt en la UI, un agente en la terminal genera 2-3 variantes de post ya renderizadas con la identidad SIDMA, las ciclas visualmente y al aceptar quedan persistidas como contenido aprobado.

**Principio rector:** la consistencia de marca se garantiza **por sistema, no por prompt**. La identidad visual SIDMA vive codificada en plantillas de slide; el prompt solo decide contenido, estructura y ángulo editorial. El agente no puede romper la marca aunque quiera. Esta es la ventaja sobre impeccable: impeccable optimiza UI genérica con reglas de diseño; Post Studio produce resultados de Instagram con identidad blindada.

## 2. Contexto y problema

**Hoy existe:**
- **Cerebro** — vault Obsidian: `01 — Marca/` (brand_profile, Tono y Voz, Identidad Visual), `02 — Campañas/`, `04 — Contenido/` (estrategia temática, pilares).
- **Memoria** — `content_memory.json` (12 posts: 10 descartados, 2 pendientes).
- **Ojos** — `content_manager/` (React/Vite + Express, ~900 LOC): grid con drag & drop, papelera, galería visual, modal de edición.
- **Mano (desconectada)** — `carrusel_export/build.py`: motor de plantillas de marca (cover/requisito/CTA, 1080×1350) que exporta PNG vía `html-to-image`, pero con contenido hardcodeado y 3 scripts clonados.

**Problema:** el flujo de generación es manual y frágil. El agente escribe JSON fuera de la app, el guardado sobreescribe el archivo completo, el render de carruseles requiere editar Python a mano y pasos manuales de navegador. No hay loop prompt → variantes → aprobación.

## 3. Usuarios

- **Leonel (CM humano):** escribe prompts, anota slides, cicla variantes, aprueba/descarta. Nunca debería tocar código ni JSON a mano.
- **Agente CM (Claude Code en terminal):** consume eventos, lee el vault, genera variantes, renderiza, persiste.

## 4. Objetivos y métricas

| Objetivo | Métrica de éxito |
|---|---|
| Reducir tiempo prompt → post renderizado | < 2 min por tanda de variantes |
| Consistencia de marca | 100 % de posts usan plantillas del sistema (0 CSS ad-hoc por post) |
| Cero fricción de aprobación | Accept en UI persiste sin tocar terminal ni archivos |
| KPI de negocio (indirecto) | Más volumen/calidad de contenido → inscripciones SIDMA Legal/Tech 2026 |

## 5. Alcance por fases

### Fase 0 — Limpieza y organización

**Scope:** solo mover/borrar lo listado; no se toca el vault ni `Experiencia-Sidma/`.

Acciones (confirmadas por Leonel 2026-07-13):
- Mover `content_manager/public/A*.png` (~27 MB de renders generados) → `renders/` en la raíz del proyecto (fuera de `public/`; la app los servirá vía endpoint estático de Express apuntando a `renders/`).
- Borrar: `content_memory.backup-2026-06-11.json`, `Sin título.canvas`, `sidma_tech_post.png` (raíz), `.DS_Store` (todos), `carrusel_export/build2.py`, `carrusel_export/build3.py`.
- Reorganizar `carrusel_export/` → `post_engine/` (nuevo nombre del motor, ver Fase 1).
- `content_manager/generate_placeholders.py` y `extend_image.py`: mover a `post_engine/tools/`.

**Fuera de scope / intocable:** `Experiencia-Sidma/` (1.2 GB), todo el vault (`01`–`06`, `HOME.md`), `content_memory.json`, `Recursos/` (PDFs de reglamentos).

**Done when:** repo ordenado según el árbol de §7, `npm run dev` + `node server.js` arrancan, el grid carga los 12 posts y la galería visual muestra los renders desde su nueva ubicación.

### Fase 1 — Motor de plantillas (`post_engine/`)

Generalizar `build.py` en un motor data-driven:

- **FR-1.1** Plantillas de slide por tipo (`cover`, `bullet/req`, `quote`, `cta`, `single`) como HTML+CSS con la identidad SIDMA (colores, tipografía, logo, decoración, contador `n/N`) parametrizadas solo por contenido.
- **FR-1.2** Entrada única: un JSON de post (esquema §8). Un comando (`node post_engine/render.mjs <post.json>` o equivalente) produce los PNG 1080×1350 finales en `renders/<post_id>/`.
- **FR-1.3** Render headless con **Playwright** (sin pasos manuales de navegador; sustituye el flujo actual de `html-to-image` abierto a mano).
- **FR-1.4** Soporte para formatos: carrusel (2–10 slides), imagen única. Video queda fuera (v2).
- **FR-1.5** Las plantillas leen tokens de marca de un único archivo (`post_engine/brand.css` o `tokens.json`) derivado de `01 — Marca/Identidad Visual.md`.

**Done when:** de un JSON de post sale la tanda completa de PNGs con un solo comando, pixel-idéntica en estilo a los carruseles A23/A25/A27 existentes (validación visual de Leonel sobre 1 carrusel de prueba).

### Fase 2 — Loop vivo estilo impeccable

Adaptación del patrón de impeccable live (cola de eventos HTTP + agente como worker en long-poll):

- **FR-2.1** `server.js` crece a: cola de eventos persistente (journal append-only en `.studio/journal.jsonl`), `POST /api/events` (UI → cola), `GET /poll` (long-poll del agente, timeout largo), `GET /api/stream` (SSE hacia la UI para estados: `queued → generating → ready`).
- **FR-2.2** UI — barra de prompt global: texto libre + selectores de campaña (Legal/Tech), tipo (carrusel/imagen) y pilar de contenido. Emite evento `generate`.
- **FR-2.3** UI — feedback anclado: comentarios sobre un slide concreto de un post existente (equivalente a las anotaciones de impeccable: la posición del comentario define el alcance del cambio). Emite evento `iterate` con `post_id`, `slide`, `comment`.
- **FR-2.4** UI — ciclado de variantes: cuando el agente responde `ready`, la tarjeta muestra las variantes (A/B/C) con navegación; `accept` fija una variante (evento `accept`), `discard` las descarta todas (evento `discard`).
- **FR-2.5** Skill `/sidma-live` (en `.claude/skills/sidma-live/`): protocolo del agente — poll loop; en `generate`/`iterate`: leer `brand_profile.md` + `Tono y Voz.md` + campaña correspondiente, producir 2-3 variantes de post-JSON con direcciones editoriales distintas, renderizar con el motor de Fase 1, responder `done`; en `accept`: persistir la variante elegida en `content_memory.json` con `status: approved` (escritura por post, no archivo completo); volver a poll. Recuperación vía journal si el poll se interrumpe.
- **FR-2.6** Endpoint de escritura granular: `PATCH /api/posts/:id` (sustituye al `POST /api/posts` que sobreescribe todo el archivo; ese endpoint se elimina).

**Done when:** Leonel escribe un prompt en la UI y, sin tocar la terminal, en < 2 min aparecen variantes ciclables; accept persiste el post como aprobado con sus PNGs en `renders/`; un comentario sobre un slide produce una nueva versión de solo ese post; matar y relanzar el poll no pierde eventos.

## 6. Arquitectura del loop (referencia: impeccable live)

```
┌─────────────┐  POST /api/events   ┌──────────────┐   GET /poll (long-poll)  ┌──────────────┐
│  UI (React) │ ──────────────────▶ │  server.js   │ ◀──────────────────────  │ Claude Code  │
│  grid+prompt│ ◀────────────────── │  cola+journal│  ────────────────────▶   │ /sidma-live  │
└─────────────┘   SSE /api/stream   └──────────────┘   reply done/ready       └──────┬───────┘
                                                                                      │ lee vault,
                                                                              genera JSON, invoca
                                                                              post_engine → PNGs
```

La terminal no recibe nada "mágico": el agente es un consumidor de cola. Verdad canónica: el journal (como `.impeccable/live/sessions/`).

## 7. Estructura de carpetas objetivo (tras Fase 0/1)

```
SIDMA/
├── 01 — Marca/ … 06 — Sesiones/     # vault intacto
├── content_memory.json               # DB de posts (no se mueve)
├── content_manager/                  # app React + server.js
├── post_engine/                      # motor de plantillas y render
│   ├── templates/                    # cover.html, bullet.html, quote.html, cta.html
│   ├── brand.css | tokens.json       # identidad visual única
│   ├── render.mjs                    # JSON → PNGs (Playwright)
│   └── tools/                        # extend_image.py, generate_placeholders.py
├── renders/                          # PNGs generados (git-ignored si se versiona)
├── Recursos/                         # PDFs reglamentos
├── Experiencia-Sidma/                # intocable
└── PRD — SIDMA Post Studio.md
```

## 8. Modelo de datos — Post v2

Extiende el esquema actual (compatible hacia atrás; migración trivial con 12 posts):

```jsonc
{
  "id": "A38",
  "status": "pending | approved | discarded",
  "type": "image | carousel | video",
  "campaign": "SIDMA Legal 2026 | SIDMA Tech 2026",
  "pillar": "string?",                      // pilar de contenido del vault
  "prompt_origin": "string?",               // prompt que lo generó
  "copy": "string",                         // caption de Instagram
  "visual_content": [{ "slide": 1, "type": "cover|bullet|quote|cta", "text": "..." }],
  "images": ["renders/A38/slide_1.png"],
  "feedback": "string",
  "variants": [ /* post-objects alternativos; null tras accept */ ],
  "history": [{ "ts": "...", "event": "generate|iterate|accept", "prompt": "..." }]
}
```

## 9. No-goals (v1)

- Publicación directa a Instagram (API de Meta) — el output son PNGs + copy listos para publicar.
- Video/Reels.
- Multi-marca o multi-tenant: el motor es SIDMA-specific a propósito (la especificidad ES el producto).
- Auth/deploy remoto: todo corre en localhost.
- Editar la identidad visual desde la UI.

## 10. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Render Playwright no fiel a los carruseles actuales | Gate de Fase 1: validación visual contra A23/A25/A27 antes de Fase 2 |
| Long-poll frágil ante cierres de terminal | Journal append-only + comando de resume (patrón impeccable §Recovery) |
| Escritura concurrente a `content_memory.json` | Toda escritura pasa por `server.js` (PATCH por post); el agente nunca escribe el archivo directo en Fase 2 |
| Variantes genéricas / pérdida de voz | El prompt de sistema del skill siempre inyecta `brand_profile.md` + `Tono y Voz.md`; temática del caso 2026 pendiente → placeholder en skill |
| Scope creep hacia editor de diseño | No-goal §9: la UI nunca edita estilos, solo contenido |

## 11. Criterios de aceptación globales

1. `npm run dev` levanta UI + server con un solo comando (`concurrently`).
2. Un prompt en la UI produce variantes renderizadas sin intervención en terminal (más allá de tener `/sidma-live` corriendo).
3. Ningún post aprobado contiene estilos fuera de `post_engine/templates/`.
4. Matar el agente a mitad de generación y relanzarlo no pierde el evento ni duplica posts.
5. El vault sigue siendo la única fuente de verdad de marca; el skill la lee, no la duplica.

## 12. Orden de ejecución

1. **Fase 0** (limpieza) → gate: app funciona.
2. **Fase 1** (post_engine) → gate: validación visual de Leonel.
3. **Fase 2** (loop vivo) → gate: criterios §11 completos.

Decisión abierta: ninguna. `Experiencia-Sidma/` queda explícitamente intocable hasta nueva orden.
