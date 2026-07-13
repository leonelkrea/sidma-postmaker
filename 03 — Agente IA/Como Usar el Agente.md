---
tags: [agente, guía, usuario, comandos]
relacionado: "[[cm_agent_instructions]]"
---

# Cómo Usar el Agente de Contenido SIDMA

> Esta guía es para el **usuario humano**. Para las instrucciones del agente, ver [[cm_agent_instructions]].

---

## Flujo de Trabajo Básico

```
1. Abres una nueva conversación con Claude o Gemini
2. Le pegas el contenido de [[cm_agent_instructions]] como system prompt
   (o como primer mensaje si no tienes system prompt)
3. Le dices al agente que lea también [[agent_memory]] y [[brand_profile]]
4. Usas un COMANDO para decirle qué hacer
5. El agente te devuelve JSON que copias en content_memory.json
6. Abres la app (npm run dev) para ver el contenido en el grid
7. Revisas, apruebas o descartas desde la interfaz
8. Das el botón "Guardar Memoria" en la app
9. Al final de la sesión, pides al agente que actualice [[agent_memory]]
```

---

## Los 5 Comandos

### `GENERAR`
Le dices exactamente cuántos posts de qué tipo quieres.

```
GENERAR: 2 carruseles de SIDMA Legal y 1 video de SIDMA Tech
```

```
GENERAR: 3 imágenes de SIDMA Legal sobre preinscripción
```

```
GENERAR: 1 carrusel de glosario y 2 imágenes de noticias para SIDMA Legal
```

**El agente te devolverá JSON.** Cópialo y agrégalo al `content_memory.json`.

---

### `REVISAR`
Cuando un post fue descartado y quieres que el agente lo reescriba con el feedback.

```
REVISAR: mock-legal-1 — el copy suena sensacionalista, reescribir más objetivo
```

```
REVISAR: el video de SIDMA Tech — falta el hook en los primeros 3 segundos
```

---

### `OPTIMIZAR`
Cuando un post está bien pero quieres mejorarlo para un objetivo específico.

```
OPTIMIZAR: mock-legal-1 para máximo engagement en carrusel
```

```
OPTIMIZAR: el post de inscripción para mayor urgencia sin ser sensacionalista
```

---

### `INVESTIGAR`
Cuando necesitas referencias, datos o ideas antes de generar contenido.

```
INVESTIGAR: casos de arbitraje famosos que podría referenciar en un carrusel
```

```
INVESTIGAR: tendencias de formato en Instagram para cuentas de eventos académicos
```

```
INVESTIGAR: términos de LegalTech para explicar en un glosario de SIDMA Tech
```

El agente te dará 3–5 opciones con contexto. Tú eliges las que quieres y luego usas `GENERAR`.

---

### `MEMORIA: mostrar`
El agente lista lo que ha aprendido en la sesión actual + lo que hay en [[agent_memory]].

```
MEMORIA: mostrar
```

---

## Consejos para Mejores Resultados

### Sé específico con el tipo y la fase
```
❌ GENERAR: posts para SIDMA Legal
✅ GENERAR: 2 carruseles de SIDMA Legal enfocados en preinscripción
             con tono de urgencia moderada (cierra el 30 de abril)
```

### Incluye la fase del calendario
El agente genera contenido más preciso si sabe en qué momento del año estás:
```
GENERAR: 1 video de SIDMA Tech
         Fase actual: inscripciones abiertas (1–12 jun)
         Objetivo: que developers que no conocen el mundo legal se interesen
```

### Da contexto de la temática (cuando se sepa)
```
GENERAR: 3 carruseles de SIDMA Legal
         Temática del caso 2026: [SECTOR]
         Usar estrategia creativa temática (voz del sector como periodismo real)
```

---

## Cómo Agregar JSON al Sistema

1. El agente te devuelve un array JSON con los posts
2. Abre el archivo `content_memory.json` en el proyecto
3. Agrega los nuevos posts al array existente
4. Guarda el archivo
5. La app se recarga automáticamente (si `npm run dev` está corriendo)

**O desde la app:** Si el servidor está corriendo, el botón "Guardar Memoria" escribe directamente el estado actual al JSON.

---

## Cómo Dar Feedback al Agente

En la app (grid), cuando descartas un post:
1. Escribe el feedback en el textarea visible en la tarjeta
2. Dale clic al botón de guardar o abre el modal para editar en detalle
3. Copia el feedback y díselo al agente:

```
El post mock-legal-1 fue descartado con este feedback:
"[pegar el texto del feedback]"
Corrígelo y dame la versión nueva.
```

---

## Al Final de Cada Sesión

Pide al agente que actualice [[agent_memory]]:

```
Resume lo que aprendiste en esta sesión:
- ¿Qué posts fueron descartados y por qué?
- ¿Qué posts fueron aprobados? ¿Qué tenían en común?
- ¿Algo nuevo sobre la marca o el tono?

Escribe las actualizaciones para agent_memory.md en formato markdown.
```

Luego pega las actualizaciones en [[agent_memory]].

---

## Registro de Sesiones

Guarda cada sesión en `06 — Sesiones/`. Usa la [[Plantilla de Sesión]].
