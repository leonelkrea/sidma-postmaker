/**
 * SIDMA Post Engine — render headless con Playwright
 * Uso: node post_engine/render.mjs <post.json>
 * Salida: renders/<post.id>/slide_<n>.png  (1080×1350 px)
 */
import { chromium } from 'playwright';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TEMPLATES = path.join(__dirname, 'templates');
const ASSETS   = path.join(__dirname, 'assets');
const RENDERS  = path.join(__dirname, '..', 'renders');

// ── Inyectar variables en plantilla ──────────────────────────────────────────
function fill(template, vars) {
  return template.replace(/\{\{(\w+)\}\}/g, (_, key) => vars[key] ?? '');
}

// ── Renderizar un post completo ───────────────────────────────────────────────
export async function renderPost(post) {
  const slides = post.visual_content ?? [];
  if (!slides.length) throw new Error(`Post ${post.id} no tiene visual_content`);

  const outDir = path.join(RENDERS, post.id);
  await fs.mkdir(outDir, { recursive: true });

  const browser = await chromium.launch();
  const renderedPaths = [];

  for (const slide of slides) {
    const tplFile = path.join(TEMPLATES, `${slide.type}.html`);
    const tplRaw  = await fs.readFile(tplFile, 'utf-8').catch(() => {
      throw new Error(`Plantilla no encontrada: templates/${slide.type}.html`);
    });

    const html = fill(tplRaw, {
      ASSETS_PATH: `file://${ASSETS}`,
      COUNTER:     `${slide.slide} / ${slides.length}`,
      KICKER:      slide.kicker   ?? '',
      TITLE:       slide.title    ?? '',
      BODY:        slide.text     ?? '',
      NUM:         String(slide.num ?? slide.slide - 1).padStart(2, '0'),
      URL:         slide.url      ?? '',
      CAMPAIGN:    post.campaign  ?? 'SIDMA',
      POST_ID:     post.id        ?? '',
    });

    const page = await browser.newPage();
    await page.setViewportSize({ width: 1080, height: 1350 });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.waitForTimeout(400); // margen para fonts

    const outPath = path.join(outDir, `slide_${slide.slide}.png`);
    await page.screenshot({ path: outPath });
    await page.close();

    renderedPaths.push(`renders/${post.id}/slide_${slide.slide}.png`);
    console.log(`  ✓ slide_${slide.slide}.png`);
  }

  await browser.close();
  return renderedPaths;
}

// ── CLI ───────────────────────────────────────────────────────────────────────
const [, , postArg] = process.argv;
if (!postArg) {
  console.error('Uso: node post_engine/render.mjs <post.json>');
  process.exit(1);
}

const postPath = path.resolve(postArg);
const post     = JSON.parse(await fs.readFile(postPath, 'utf-8'));

console.log(`\nRenderizando ${post.id} — ${post.visual_content?.length ?? 0} slides...`);
const paths = await renderPost(post);
console.log(`\nListo → renders/${post.id}/`);
console.log(paths.join('\n'));
