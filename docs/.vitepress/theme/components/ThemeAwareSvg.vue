<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { isDark } from '../index'

const props = defineProps<{
  src: string
  alt?: string
  title?: string
}>()

const svgContent = ref('')
const containerRef = ref<HTMLElement | null>(null)

async function loadSvg() {
  try {
    const response = await fetch(props.src)
    if (!response.ok) throw new Error(`Failed to load ${props.src}`)
    let svg = await response.text()

    // Inject CSS variables into SVG so it reacts to theme changes
    // even when loaded as an external resource via fetch + inline
    const cssVars = `
      <style>
        :root {
          --svg-bg: ${isDark.value ? '#1a1a1f' : '#faf8f5'};
          --svg-panel: ${isDark.value ? '#232329' : '#ffffff'};
          --svg-card: ${isDark.value ? '#2a2a32' : '#fffdfa'};
          --svg-ink: ${isDark.value ? '#e8e6f0' : '#1c1a22'};
          --svg-muted: ${isDark.value ? '#a09eb8' : '#6b6680'};
          --svg-accent: ${isDark.value ? '#ff8c5a' : '#e85524'};
          --svg-accent-soft: ${isDark.value ? 'rgba(255,140,90,0.15)' : 'rgba(232,85,36,0.10)'};
          --svg-wire: ${isDark.value ? '#6b6880' : '#9b96b0'};
          --svg-border: ${isDark.value ? '#3d3d4a' : '#e0dbe8'};
          --svg-shadow: ${isDark.value ? 'rgba(0,0,0,0.4)' : 'rgba(28,26,34,0.06)'};
        }
      </style>
    `

    // Insert CSS variables right after the opening <svg> tag
    svg = svg.replace(/<svg([^>]*)>/i, `<svg$1>${cssVars}`)

    svgContent.value = svg
  } catch (err) {
    console.error('[ThemeAwareSvg] Failed to load SVG:', err)
    svgContent.value = `<div style="padding: 24px; border: 1px dashed var(--yt-border); border-radius: var(--yt-radius-md); color: var(--yt-text-3);">Failed to load SVG: ${props.src}</div>`
  }
}

onMounted(() => {
  loadSvg()
})

watch(isDark, () => {
  loadSvg()
})
</script>

<template>
  <div ref="containerRef" class="theme-aware-svg" role="img" :aria-label="alt || title">
    <div v-html="svgContent" />
  </div>
</template>

<style scoped>
.theme-aware-svg :deep(svg) {
  width: 100%;
  height: auto;
  display: block;
}

.theme-aware-svg :deep(svg) {
  transition: all 0.4s ease;
}

/* Ensure SVG children with fill/stroke using CSS vars transition smoothly */
.theme-aware-svg :deep(svg * [style*='var(--svg']) {
  transition: fill 0.4s ease, stroke 0.4s ease;
}
</style>
