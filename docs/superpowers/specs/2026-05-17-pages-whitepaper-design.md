# YOLO-Toys GitHub Pages Whitepaper Redesign

## Problem Statement

YOLO-Toys already ships a VitePress-based documentation site, but the current Pages experience still reads like a conventional product docs portal rather than a technical whitepaper and architecture showcase. The baseline engineering stack is already close to `/home/shane/dev/kimi-cli/docs`, yet the site still has four structural gaps:

1. **The homepage under-expresses the project's architectural value.** It introduces features, but it does not create a strong "systems paper" narrative for senior engineers, interviewers, or advanced OSS contributors.
2. **The information architecture is documentation-first instead of cognition-first.** Pages are grouped conventionally, but the user journey from orientation -> architecture -> implementation -> reference -> research is not yet deliberate enough.
3. **The visual system is serviceable but not differentiated.** It lacks a signature whitepaper-style hero, richer diagram framing, stronger typography rhythm, and more deliberate light/dark theme adaptation.
4. **The diagram and SVG strategy is inconsistent.** Mermaid blocks are present, but they are not framed as commercial-grade figures, and the SVG assets do not yet use an explicit token-driven theme strategy for dark/light safety.

## Design Goals

The redesigned site must:

- present YOLO-Toys as a **serious architecture artifact** rather than a demo-only repo
- keep the underlying docs stack aligned with `kimi-cli/docs` where that baseline is already modern and low-maintenance
- create a **whitepaper / academy / architectural atlas** reading experience
- improve information density without making the site feel crowded
- make every visual artifact readable and intentional in both light and dark themes
- preserve clear surface boundaries across README, Pages, long-form docs, and changelog

## Baseline Analysis

### Current YOLO-Toys site

- already uses **VitePress + Mermaid + llms plugin**, the same foundational choice as `kimi-cli/docs`
- already supports **bilingual routing**
- already contains useful raw material: academy essays, ADRs, architecture pages, comparisons, and citations
- diverges from the desired outcome mainly in **theme sophistication, homepage composition, navigation logic, and visual storytelling**

### kimi-cli baseline

`/home/shane/dev/kimi-cli/docs` establishes the canonical foundation we should keep:

- VitePress as the static site engine
- a lightweight `.vitepress/config.ts`
- a custom `theme/style.css`
- markdown-first content authoring
- locale-based navigation and sidebar configuration

The important finding is that **YOLO-Toys does not need a framework migration**. It needs a **same-stack, new-system rewrite**: new theme language, new content topology, new page templates, and stronger figure treatment.

## Approaches Considered

### Approach A — Cosmetic refresh on the current structure

Keep the existing page tree, retune the homepage, and patch the theme.

**Pros**

- lowest risk
- fastest to ship
- minimal churn

**Cons**

- preserves the current mental model
- cannot create a strong academy / atlas / whitepaper narrative
- likely leaves long-term drift between content intent and structure

### Approach B — Whitepaper layer on top of the current VitePress stack (**recommended**)

Keep the `kimi-cli`-style VitePress foundation, but aggressively redesign the site architecture, homepage composition, reusable visual blocks, sidebar taxonomy, and figure system.

**Pros**

- aligns with the requested baseline
- highest long-term payoff without introducing a new build stack
- lets us rebuild narrative, visuals, and navigation coherently
- minimizes operational risk compared with framework migration

**Cons**

- significant content and theme rewrite
- requires careful migration across both locales

### Approach C — Framework replacement (Astro / custom app)

Discard VitePress and rebuild Pages as a custom marketing-doc hybrid site.

**Pros**

- maximum visual freedom
- component-level control

**Cons**

- violates the baseline-alignment request
- higher maintenance and migration cost
- duplicates capabilities already present in `kimi-cli/docs`

## Chosen Direction

Use **Approach B**.

The site will remain a **VitePress documentation system aligned with `kimi-cli/docs` at the engineering layer**, while being completely rewritten at the **experience layer** into a whitepaper-grade documentation product.

## Target Information Architecture

The new English and Chinese trees should guide readers in the following order:

1. **Overview** — what the project is, why it matters, fast orientation
2. **Primer** — quickstart, model surfaces, deployment entry, API preview
3. **Architecture Atlas** — system topology, execution path, handler/registry/cache/runtime internals, ADRs
4. **Academy** — pattern essays, trade-offs, evolution notes, implementation reasoning
5. **Engineering Guides** — extending models, custom handlers, performance tuning, operational patterns
6. **Reference** — endpoint contracts, model matrix, benchmarks, FAQ, changelog
7. **Research** — citations, related projects, comparative analysis, forward-looking evolution notes

### Navigation principle

The top nav should not expose every leaf section. It should expose the site's dominant reading modes:

- Overview
- Primer
- Architecture
- Academy
- Reference
- Research

### Sidebar principle

Each area should feel like a self-contained chapter rather than a folder dump. Sidebars should read like a syllabus or book table of contents.

## Homepage Design

The homepage should become a **whitepaper landing page**, not a default VitePress hero plus feature grid.

### Structure

1. **Hero / thesis**
   - a strong architectural claim
   - short abstract-style copy
   - high-signal action set: Start Reading, Architecture Atlas, API Surface, GitHub
   - right-side or below-fold architectural figure panel

2. **Evidence strip**
   - model families
   - serving surfaces
   - extensibility patterns
   - observability / deployment signals

3. **Three reading tracks**
   - Interviewer / Reviewer
   - Integrator / Operator
   - Contributor / Extender

4. **System abstract**
   - one concise explanation of how the request path flows through API -> manager -> registry -> handler -> result normalization

5. **Architecture cards**
   - Handler Strategy
   - Registry Dispatch
   - Hybrid Caching
   - Multi-surface serving

6. **Research and comparisons**
   - citations
   - competing / adjacent systems
   - design evolution notes

7. **Reading roadmap**
   - a guided sequence across the major site chapters

## Visual System

The site should look like a cross between:

- an internal architecture memo
- a polished OSS technical manual
- a research-oriented product site

### Visual principles

- more typographic hierarchy, less default VitePress feel
- restrained but distinctive gradients and glow accents
- large-radius figure frames and dense but calm data cards
- clear rhythm between narrative sections, figures, and tables
- high contrast in both themes, with no decorative element allowed to reduce readability

### Color strategy

- keep the project's orange family as identity
- introduce neutral graphite / slate support colors
- reserve saturated accent use for emphasis, not everywhere
- define all visual primitives through CSS custom properties so markdown prose, cards, SVGs, and Mermaid wrappers share the same theme tokens

## Light / Dark Theme and SVG Strategy

This is a first-class requirement.

### Requirements

1. All logo-like SVG assets must use **theme-aware CSS variables** or explicit dual-palette tokens.
2. Inline or referenced SVG figures must avoid hard-coded low-contrast fills for text or strokes.
3. Mermaid diagrams must render inside styled figure shells so they remain readable even when node/background contrast changes.
4. Decorative glows and gradients must never be the only separator for semantic elements.

### Implementation pattern

- define shared doc tokens in `theme/style.css`
- use `currentColor`, CSS variables, or dual-mode fills in SVGs
- add reusable classes for:
  - figure surface
  - figure caption
  - metric cards
  - roadmap blocks
  - comparison matrices
- set Mermaid theme variables to a neutral, token-compatible palette that works in both modes

## Diagram Strategy

Every major diagram should look deliberate and editorialized.

### Diagram classes

1. **Architecture figures** — system topology, component layers, interaction contracts
2. **Flow figures** — request lifecycle, model-loading path, streaming pipeline
3. **Comparison figures** — YOLO-Toys vs Triton / TorchServe / BentoML
4. **Learning figures** — concept maps inside Academy pages

### Quality bar

- each diagram gets a caption and context
- diagrams use consistent naming and legend conventions
- avoid raw default Mermaid blocks without framing
- when Mermaid is insufficient for expressiveness, use hand-authored SVG illustrations

## Content Strategy

The content rewrite should deepen the site's perceived rigor, not just rename folders.

### New or expanded modules

- **overview / project thesis**
- **primer / quick model tour**
- **architecture / system atlas**
- **academy / design pattern essays**
- **research / papers, upstream projects, and evolution notes**
- **reference / benchmark and model matrix normalization**

### Required content improvements

1. Replace shallow summaries with sharper system explanations.
2. Add "why this decision exists" language to architectural pages.
3. Add "related systems" sections where useful.
4. Expand citations into a proper research-support surface.
5. Add evolution-oriented notes explaining what the project optimizes for and what it intentionally does not.

## Reusable Experience Components

The theme should provide reusable markdown-friendly design blocks instead of relying only on ad hoc page HTML.

### Candidate components / patterns

- whitepaper hero section
- stat / signal chips
- architecture layer cards
- reading path grid
- callout panels for trade-offs
- figure frame wrapper
- paper-style reference list block
- comparison matrix styling

The implementation may use lightweight Vue theme components where plain markdown is no longer enough, but the content model should remain markdown-first.

## SEO / Metadata / Public Surface Alignment

The redesign should also align public-facing metadata:

- stronger title and description tags for the site
- improved OG image aligned with the whitepaper tone
- coherent README <-> site positioning
- no duplication of the same long-form content across repository surfaces

## Migration Rules

1. Keep the VitePress baseline.
2. Restructure docs by intent, not by legacy folder shape.
3. Preserve bilingual parity.
4. Prefer content consolidation over duplicate explanations.
5. Upgrade diagrams as part of page rewrites, not as an afterthought.
6. If a page is weak and redundant, rewrite or remove it instead of carrying it forward.

## Testing and Verification Strategy

The redesign is complete only if:

- VitePress builds cleanly
- all locale nav and sidebar links resolve
- light and dark themes remain readable across homepage, prose pages, tables, code, Mermaid blocks, and SVG figures
- the homepage reads as an architecture narrative instead of a default docs landing page
- the resulting structure is clearly distinct from README and changelog responsibilities

## Autonomous Assumptions

Because the user is not available for iterative approval during this session, this design proceeds with the following assumptions:

- the visual companion is not required
- the requested "same technology as kimi-cli" means **same documentation stack and engineering approach**, not a pixel clone
- aggressive restructuring is allowed as long as the result is cleaner, more coherent, and easier to maintain
- the whitepaper / academy direction takes precedence over preserving legacy page names or shallow content
