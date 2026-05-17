# YOLO-Toys Pages Whitepaper Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the GitHub Pages site into a bilingual whitepaper-grade architecture showcase while keeping the VitePress stack aligned with `kimi-cli/docs`.

**Architecture:** Keep the current VitePress + Mermaid + markdown-first baseline, then replace the information architecture, homepage composition, visual system, and figure strategy with a new whitepaper-oriented theme layer. The implementation should favor reusable theme components and token-driven styling so homepage sections, prose figures, Mermaid diagrams, and SVG assets all stay coherent in light and dark mode.

**Tech Stack:** VitePress, Vue theme components, Mermaid, CSS custom properties, SVG, markdown, npm

---

## File Structure

- Modify: `docs/.vitepress/config.ts` — replace the current navigation/sidebar taxonomy and metadata with the new Overview / Primer / Architecture / Academy / Reference / Research model.
- Modify: `docs/.vitepress/theme/index.ts` — register new shared theme components.
- Modify: `docs/.vitepress/theme/style.css` — replace the current styling layer with the new whitepaper token system, figure shells, reading grids, comparison surfaces, and light/dark-safe treatments.
- Create: `docs/.vitepress/theme/components/WhitepaperLanding.vue` — reusable landing-page shell for hero, abstract, evidence strip, tracks, and roadmap.
- Create: `docs/.vitepress/theme/components/ReadingTracks.vue` — reusable reader-path grid for interviewer / operator / contributor flows.
- Create: `docs/.vitepress/theme/components/FigureFrame.vue` — consistent captioned figure wrapper for Mermaid and SVG blocks.
- Modify: `docs/en/index.md`, `docs/zh/index.md` — replace the current default home layout content with the whitepaper landing composition.
- Create: `docs/en/primer/index.md`, `docs/zh/primer/index.md` — new quick-orientation section.
- Create: `docs/en/research/index.md`, `docs/zh/research/index.md` — new academic / related-work section landing pages.
- Modify: `docs/en/architecture/index.md`, `docs/zh/architecture/index.md` — turn section homepages into atlas-style chapter openers.
- Modify: `docs/en/academy/index.md`, `docs/zh/academy/index.md` — deepen the academy framing.
- Modify: `docs/en/reference/index.md`, `docs/zh/reference/index.md` — normalize the reference landing pages.
- Modify: `docs/en/architecture/overview.md`, `docs/zh/architecture/overview.md` — rewrite as a true systems atlas page.
- Modify: `docs/en/architecture/request-flow.md`, `docs/zh/architecture/request-flow.md` — rewrite and frame lifecycle diagrams.
- Modify: `docs/en/reference/comparisons.md`, `docs/zh/reference/comparisons.md` — move to whitepaper-quality comparison writing and figures.
- Modify: `docs/en/citations.md`, `docs/zh/citations.md` — keep as the canonical bibliography source while linking it from the new Research entry.
- Create: `docs/public/images/hero-architecture.svg` — theme-safe homepage architecture figure.
- Create: `docs/public/images/request-lifecycle.svg` — theme-safe system flow figure.
- Modify: `docs/public/images/logo.svg` — replace hard-coded fills with theme-safe styling.
- Modify: `assets/images/og-image.svg` — align the social preview asset with the new whitepaper visual language.
- Test: `cd docs && npm run build`

### Task 1: Rebuild the documentation information architecture

**Files:**
- Modify: `docs/.vitepress/config.ts`
- Modify: `docs/en/index.md`
- Modify: `docs/zh/index.md`
- Create: `docs/en/primer/index.md`
- Create: `docs/zh/primer/index.md`
- Create: `docs/en/research/index.md`
- Create: `docs/zh/research/index.md`
- Test: `docs/package.json`

- [ ] **Step 1: Write the failing navigation change first**

```ts
// docs/.vitepress/config.ts
nav: [
  { text: 'Overview', link: '/en/' },
  { text: 'Primer', link: '/en/primer/' },
  { text: 'Architecture', link: '/en/architecture/' },
  { text: 'Academy', link: '/en/academy/' },
  { text: 'Reference', link: '/en/reference/' },
  { text: 'Research', link: '/en/research/' },
]
```

- [ ] **Step 2: Run the docs build to confirm the new section links fail before the pages exist**

Run: `cd /home/shane/lessup/yolo-toys/docs && npm run build`
Expected: FAIL with dead-link or missing-page output for `/en/primer/`, `/zh/primer/`, `/en/research/`, or `/zh/research/`

- [ ] **Step 3: Create the missing chapter entry pages**

```md
<!-- docs/en/primer/index.md -->
# Primer

Use this chapter to understand YOLO-Toys in fifteen minutes: core surfaces, model families, serving modes, and where to go next.

## Reading path

1. Read the project thesis
2. Scan the model matrix
3. Jump into the architecture atlas
```

```md
<!-- docs/en/research/index.md -->
# Research

This chapter collects citations, adjacent systems, and evolution notes that explain the intellectual context around YOLO-Toys.
```

- [ ] **Step 4: Mirror the same structure for Chinese and rerun the build**

Run: `cd /home/shane/lessup/yolo-toys/docs && npm run build`
Expected: PASS or fail later on theme/content issues, but not on missing Primer/Research chapter indexes

- [ ] **Step 5: Commit the IA groundwork**

```bash
git add docs/.vitepress/config.ts docs/en/index.md docs/zh/index.md docs/en/primer/index.md docs/zh/primer/index.md docs/en/research/index.md docs/zh/research/index.md
git commit -m "docs: rebuild pages information architecture"
```

### Task 2: Build the reusable whitepaper theme layer

**Files:**
- Modify: `docs/.vitepress/theme/index.ts`
- Modify: `docs/.vitepress/theme/style.css`
- Create: `docs/.vitepress/theme/components/WhitepaperLanding.vue`
- Create: `docs/.vitepress/theme/components/ReadingTracks.vue`
- Create: `docs/.vitepress/theme/components/FigureFrame.vue`
- Test: `docs/en/index.md`

- [ ] **Step 1: Make the homepage reference the new components before they exist**

```md
<!-- docs/en/index.md -->
<WhitepaperLanding
  chapter="Architecture Whitepaper"
  title="A multi-model vision serving stack designed for comparison, extensibility, and operational clarity."
/>
```

- [ ] **Step 2: Run the docs build to confirm unresolved component failure**

Run: `cd /home/shane/lessup/yolo-toys/docs && npm run build`
Expected: FAIL with component resolution errors such as `Failed to resolve component: WhitepaperLanding`

- [ ] **Step 3: Implement the components and register them in the theme**

```ts
// docs/.vitepress/theme/index.ts
import DefaultTheme from 'vitepress/theme'
import WhitepaperLanding from './components/WhitepaperLanding.vue'
import ReadingTracks from './components/ReadingTracks.vue'
import FigureFrame from './components/FigureFrame.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('WhitepaperLanding', WhitepaperLanding)
    app.component('ReadingTracks', ReadingTracks)
    app.component('FigureFrame', FigureFrame)
  },
}
```

```vue
<!-- docs/.vitepress/theme/components/FigureFrame.vue -->
<script setup lang="ts">
defineProps<{ title: string; caption?: string }>()
</script>

<template>
  <figure class="yt-figure">
    <figcaption class="yt-figure__title">{{ title }}</figcaption>
    <div class="yt-figure__body">
      <slot />
    </div>
    <p v-if="caption" class="yt-figure__caption">{{ caption }}</p>
  </figure>
</template>
```

- [ ] **Step 4: Replace the old theme tokens with the new whitepaper tokens and rerun the build**

Run: `cd /home/shane/lessup/yolo-toys/docs && npm run build`
Expected: PASS or fail only on later content/asset issues, not on missing component registration

- [ ] **Step 5: Commit the theme foundation**

```bash
git add docs/.vitepress/theme/index.ts docs/.vitepress/theme/style.css docs/.vitepress/theme/components
git commit -m "feat: add whitepaper docs theme components"
```

### Task 3: Rewrite the bilingual landing and chapter opener pages

**Files:**
- Modify: `docs/en/index.md`
- Modify: `docs/zh/index.md`
- Modify: `docs/en/architecture/index.md`
- Modify: `docs/zh/architecture/index.md`
- Modify: `docs/en/academy/index.md`
- Modify: `docs/zh/academy/index.md`
- Modify: `docs/en/reference/index.md`
- Modify: `docs/zh/reference/index.md`
- Test: `docs/.vitepress/theme/components/WhitepaperLanding.vue`

- [ ] **Step 1: Replace the default VitePress hero content with the new whitepaper composition**

```md
<!-- docs/en/index.md -->
<WhitepaperLanding
  chapter="Architecture Whitepaper"
  eyebrow="YOLO-Toys"
  title="One service, multiple vision model families, and a deliberately documented serving architecture."
  abstract="YOLO-Toys packages detection, segmentation, pose, open-vocabulary inference, captioning, and VQA behind a single FastAPI + WebSocket runtime."
/>
```

- [ ] **Step 2: Run the build and verify any newly referenced assets or pages still missing**

Run: `cd /home/shane/lessup/yolo-toys/docs && npm run build`
Expected: FAIL on the next missing dependency only, such as a new SVG figure or a still-unwritten chapter link

- [ ] **Step 3: Fill in the chapter opener pages with syllabus-style summaries**

```md
<!-- docs/en/architecture/index.md -->
# Architecture Atlas

This chapter maps how requests move through the runtime and why the handler, registry, and cache boundaries look the way they do.

## Chapter map

- System overview
- Request lifecycle
- Architectural decisions
- Extension boundaries
```

- [ ] **Step 4: Mirror the same whitepaper framing in Chinese and rerun the build**

Run: `cd /home/shane/lessup/yolo-toys/docs && npm run build`
Expected: PASS or fail only on deep-content asset issues, not on section-entry structure

- [ ] **Step 5: Commit the content skeleton rewrite**

```bash
git add docs/en/index.md docs/zh/index.md docs/en/architecture/index.md docs/zh/architecture/index.md docs/en/academy/index.md docs/zh/academy/index.md docs/en/reference/index.md docs/zh/reference/index.md
git commit -m "docs: rewrite landing and chapter opener pages"
```

### Task 4: Upgrade architecture, comparison, and research content with figure framing

**Files:**
- Modify: `docs/en/architecture/overview.md`
- Modify: `docs/zh/architecture/overview.md`
- Modify: `docs/en/architecture/request-flow.md`
- Modify: `docs/zh/architecture/request-flow.md`
- Modify: `docs/en/reference/comparisons.md`
- Modify: `docs/zh/reference/comparisons.md`
- Modify: `docs/en/citations.md`
- Modify: `docs/zh/citations.md`
- Test: `docs/public/images/hero-architecture.svg`

- [ ] **Step 1: Add figure-wrapped content that references the new SVG assets before they exist**

```md
<FigureFrame
  title="Figure 1. Serving topology"
  caption="The runtime keeps HTTP, WebSocket, handler dispatch, and result normalization separate."
>
  <img src="/images/hero-architecture.svg" alt="YOLO-Toys serving topology" />
</FigureFrame>
```

- [ ] **Step 2: Run the build to confirm missing asset errors**

Run: `cd /home/shane/lessup/yolo-toys/docs && npm run build`
Expected: FAIL on missing `/images/hero-architecture.svg` or `/images/request-lifecycle.svg`

- [ ] **Step 3: Rewrite the pages as atlas / research pages instead of summary notes**

```md
## Why this boundary exists

The API layer is intentionally thin. Model selection, cache lookup, handler dispatch, and result shaping live below the route surface so new model families can be added without multiplying endpoint-specific logic.

## Trade-offs

- lower integration cost than bespoke per-model services
- higher responsibility in the central manager layer
- explicit normalization cost in exchange for a stable API
```

- [ ] **Step 4: Add the missing SVGs and rerun the build**

Run: `cd /home/shane/lessup/yolo-toys/docs && npm run build`
Expected: PASS or reveal only final theme/metadata polish issues

- [ ] **Step 5: Commit the deep-content rewrite**

```bash
git add docs/en/architecture/overview.md docs/zh/architecture/overview.md docs/en/architecture/request-flow.md docs/zh/architecture/request-flow.md docs/en/reference/comparisons.md docs/zh/reference/comparisons.md docs/en/citations.md docs/zh/citations.md docs/public/images/hero-architecture.svg docs/public/images/request-lifecycle.svg
git commit -m "docs: upgrade architecture and research chapters"
```

### Task 5: Fix theme-safe SVGs, metadata, and final visual polish

**Files:**
- Modify: `docs/.vitepress/config.ts`
- Modify: `docs/.vitepress/theme/style.css`
- Modify: `docs/public/images/logo.svg`
- Modify: `assets/images/og-image.svg`
- Test: `docs/.vitepress/dist`

- [ ] **Step 1: Move SVG colors onto theme-safe tokens**

```svg
<!-- docs/public/images/logo.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <style>
    .yt-badge { fill: var(--vp-c-brand-1, #ff6b35); }
    .yt-mark { fill: var(--vp-c-neutral-inverse, #ffffff); }
  </style>
  <rect class="yt-badge" width="100" height="100" rx="20" />
  <text class="yt-mark" x="50" y="65" text-anchor="middle">YT</text>
</svg>
```

- [ ] **Step 2: Rebuild the site and inspect the generated output for the new metadata**

Run: `cd /home/shane/lessup/yolo-toys/docs && npm run build && rg "Architecture Whitepaper|technical whitepaper|og:image" .vitepress/dist -n`
Expected: MATCHES in generated HTML for the updated title/description/OG fields

- [ ] **Step 3: Tune Mermaid, figure shells, and metadata until the output is consistent**

```ts
// docs/.vitepress/config.ts
head: [
  ['meta', { name: 'theme-color', content: '#ff6b35' }],
  ['meta', { property: 'og:title', content: 'YOLO-Toys Architecture Whitepaper' }],
  ['meta', { property: 'og:image', content: 'https://lessup.github.io/yolo-toys/assets/images/og-image.svg' }],
]
```

- [ ] **Step 4: Run the final docs build**

Run: `cd /home/shane/lessup/yolo-toys/docs && npm run build`
Expected: PASS with no dead links and no unresolved component or asset errors

- [ ] **Step 5: Commit the final Pages polish**

```bash
git add docs/.vitepress/config.ts docs/.vitepress/theme/style.css docs/public/images/logo.svg assets/images/og-image.svg
git commit -m "feat: finalize whitepaper pages redesign"
```

## Self-Review

### Spec coverage

- **Information architecture** — covered by Task 1 and Task 3
- **Homepage redesign** — covered by Task 2 and Task 3
- **Visual system / theme** — covered by Task 2 and Task 5
- **Dark/light SVG and diagram safety** — covered by Task 4 and Task 5
- **Architecture / research depth** — covered by Task 4
- **Public metadata alignment** — covered by Task 5

### Placeholder scan

No `TODO`, `TBD`, or implicit "write tests later" steps remain. Every task lists exact files, commands, and the minimum code shape needed to execute the task.

### Type consistency

The plan uses the same component names throughout: `WhitepaperLanding`, `ReadingTracks`, and `FigureFrame`. The page taxonomy is consistently `Overview / Primer / Architecture / Academy / Reference / Research`.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-17-pages-whitepaper-redesign.md`.

Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints
