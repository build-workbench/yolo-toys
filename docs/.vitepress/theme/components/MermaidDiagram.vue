<script setup lang="ts">
/**
 * MermaidDiagram - Theme-Aware Mermaid Diagram Renderer
 *
 * Renders Mermaid diagrams with theme-aware styling.
 * Colors are aligned with design tokens from tokens.css.
 */

import { ref, watch, onMounted, nextTick } from 'vue'
import { isDark } from '../index'

const props = defineProps<{
  title?: string
  caption?: string
}>()

const mermaidContainer = ref<HTMLDivElement | null>(null)

// Theme variables aligned with tokens.css
const lightTheme = {
  primaryColor: '#fffdfa',
  primaryTextColor: '#1c1a22',
  primaryBorderColor: '#e0dbe8',
  lineColor: '#9b96b0',
  secondaryColor: '#ffffff',
  tertiaryColor: '#faf8f5',
  fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
  fontSize: '14px',
}

const darkTheme = {
  primaryColor: '#2a2a32',
  primaryTextColor: '#e8e6f0',
  primaryBorderColor: '#5a5a6a',
  lineColor: '#6b6880',
  secondaryColor: '#232329',
  tertiaryColor: '#1a1a1f',
  fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
  fontSize: '14px',
}

async function renderMermaid() {
  if (!mermaidContainer.value) return

  // Wait for mermaid to be available (loaded by vitepress-plugin-mermaid)
  const checkMermaid = () => {
    if (typeof window !== 'undefined' && (window as any).mermaid) {
      return (window as any).mermaid
    }
    return null
  }

  let attempts = 0
  let mermaid = checkMermaid()
  while (!mermaid && attempts < 50) {
    await new Promise(r => setTimeout(r, 100))
    mermaid = checkMermaid()
    attempts++
  }

  if (!mermaid) {
    console.warn('[MermaidDiagram] Mermaid not available after 5s')
    return
  }

  // Re-initialize mermaid with theme-aware config
  const themeVars = isDark.value ? darkTheme : lightTheme
  mermaid.initialize({
    theme: 'base',
    themeVariables: themeVars,
  })

  // Find and render the diagram
  const codeBlock = mermaidContainer.value.querySelector('.language-mermaid, pre code.language-mermaid')
  if (codeBlock) {
    const code = codeBlock.textContent || ''
    try {
      const id = `mermaid-${Math.random().toString(36).slice(2)}`
      const { svg } = await mermaid.render(id, code)
      mermaidContainer.value.innerHTML = svg
    } catch (err) {
      console.error('[MermaidDiagram] Render failed:', err)
    }
  }
}

onMounted(() => {
  nextTick(() => {
    renderMermaid()
  })
})

watch(isDark, () => {
  nextTick(() => {
    renderMermaid()
  })
})
</script>

<template>
  <figure class="yt-figure mermaid-figure">
    <figcaption v-if="title" class="yt-figure__title">{{ title }}</figcaption>
    <div ref="mermaidContainer" class="yt-figure__body mermaid-body">
      <slot />
    </div>
    <p v-if="caption" class="yt-figure__caption">{{ caption }}</p>
  </figure>
</template>

<style scoped>
.mermaid-figure {
  margin: 0;
}

.mermaid-body :deep(svg) {
  max-width: 100%;
  height: auto;
}

/* Smooth transition for theme changes */
.mermaid-body :deep(svg *) {
  transition: fill var(--duration-slow, 300ms) var(--ease-in-out, ease-in-out),
              stroke var(--duration-slow, 300ms) var(--ease-in-out, ease-in-out);
}
</style>
