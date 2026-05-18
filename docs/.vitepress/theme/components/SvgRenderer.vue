<script setup lang="ts">
/**
 * SvgRenderer - Theme-Aware SVG Renderer
 *
 * This component loads SVG files and renders them inline.
 * All theming is handled by CSS variables defined in tokens.css.
 *
 * KEY PRINCIPLE: No hardcoded colors are injected into the SVG!
 * The SVG should use var(--svg-*) variables directly.
 * These variables are defined at document level and update automatically
 * when the theme changes.
 *
 * OPTIMIZATION: SVG content is cached to avoid repeated fetches.
 */

import { ref, onMounted, watch } from 'vue'

const props = defineProps<{
  src: string
  alt?: string
  title?: string
}>()

const svgContent = ref('')
const isLoading = ref(true)
const error = ref('')

// SVG content cache - shared across all instances
const svgCache = new Map<string, string>()

async function loadSvg() {
  if (!props.src) return

  // Check cache first
  if (svgCache.has(props.src)) {
    svgContent.value = svgCache.get(props.src)!
    isLoading.value = false
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const response = await fetch(props.src)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    let svg = await response.text()

    // Sanitize: Remove any existing <style> blocks that might have
    // hardcoded colors (from older SVG versions)
    svg = svg.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, (match) => {
      if (match.includes('var(--')) {
        return match
      }
      return ''
    })

    // Inject a minimal style block that references document-level CSS variables
    const styleBlock = `<style>
  .canvas, .bg { fill: var(--svg-canvas); }
  .surface, .panel { fill: var(--svg-surface); stroke: var(--svg-border); }
  .surface-alt, .card { fill: var(--svg-surface-alt); stroke: var(--svg-border); }
  .ink { fill: var(--svg-ink); font-family: var(--font-sans); }
  .ink-soft { fill: var(--svg-ink-soft); }
  .muted { fill: var(--svg-muted); font-family: var(--font-sans); }
  .muted-soft { fill: var(--svg-muted-soft); }
  .brand, .accent { fill: var(--svg-brand); }
  .brand-soft, .accent-soft { fill: var(--svg-brand-soft); }
  .accent-blue { fill: var(--svg-accent); }
  .wire { stroke: var(--svg-wire); stroke-width: 3; fill: none; }
  .wire-alt { stroke: var(--svg-wire-alt); }
  .border { stroke: var(--svg-border); }
  .border-strong { stroke: var(--svg-border-strong); }
  .shadow { fill: var(--svg-shadow); }
  .success { fill: var(--svg-success); }
  .warning { fill: var(--svg-warning); }
  .danger { fill: var(--svg-danger); }
</style>`

    svg = svg.replace(/<svg([^>]*)>/i, `<svg$1>${styleBlock}`)

    // Cache the result
    svgCache.set(props.src, svg)
    svgContent.value = svg
  } catch (err) {
    console.error('[SvgRenderer] Failed to load SVG:', err)
    error.value = err instanceof Error ? err.message : 'Unknown error'
    svgContent.value = ''
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadSvg()
})

watch(() => props.src, () => {
  loadSvg()
})
</script>

<template>
  <div
    class="svg-renderer"
    :class="{ 'svg-renderer--loading': isLoading }"
    role="img"
    :aria-label="alt || title"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="svg-renderer__placeholder">
      <svg width="100%" height="200" viewBox="0 0 400 200">
        <rect fill="var(--svg-canvas)" width="400" height="200" rx="16" />
        <text
          fill="var(--svg-muted)"
          x="200"
          y="105"
          text-anchor="middle"
          font-family="var(--font-sans)"
          font-size="14"
        >
          Loading diagram...
        </text>
      </svg>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="svg-renderer__error">
      <svg width="100%" height="200" viewBox="0 0 400 200">
        <rect fill="var(--svg-canvas)" width="400" height="200" rx="16" />
        <text
          fill="var(--svg-danger)"
          x="200"
          y="95"
          text-anchor="middle"
          font-family="var(--font-sans)"
          font-size="14"
        >
          Failed to load SVG
        </text>
        <text
          fill="var(--svg-muted)"
          x="200"
          y="115"
          text-anchor="middle"
          font-family="var(--font-sans)"
          font-size="12"
        >
          {{ error }}
        </text>
      </svg>
    </div>

    <!-- SVG Content -->
    <div v-else v-html="svgContent" class="svg-renderer__content" />
  </div>
</template>

<style scoped>
.svg-renderer {
  width: 100%;
}

.svg-renderer__content :deep(svg) {
  width: 100%;
  height: auto;
  display: block;
}

.svg-renderer__content :deep(svg *) {
  /* Smooth transitions for theme changes */
  transition: fill var(--duration-slow, 300ms) var(--ease-in-out, ease-in-out),
              stroke var(--duration-slow, 300ms) var(--ease-in-out, ease-in-out),
              background-color var(--duration-slow, 300ms) var(--ease-in-out, ease-in-out);
}

.svg-renderer__placeholder,
.svg-renderer__error {
  width: 100%;
}
</style>
