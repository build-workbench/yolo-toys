<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'
import { isDark } from '../index'

const props = defineProps<{
  title?: string
  caption?: string
}>()

const mermaidContainer = ref<HTMLDivElement | null>(null)

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
  const isDarkMode = isDark.value
  mermaid.initialize({
    theme: isDarkMode ? 'dark' : 'base',
    themeVariables: isDarkMode
      ? {
          primaryColor: '#2a2a35',
          primaryTextColor: '#e8e6f0',
          primaryBorderColor: '#5a5a6a',
          lineColor: '#8a87a0',
          secondaryColor: '#23232a',
          tertiaryColor: '#1a1a20',
        }
      : {
          primaryColor: '#fff2ec',
          primaryTextColor: '#1e2933',
          primaryBorderColor: '#ffb08b',
          lineColor: '#6f6b73',
          secondaryColor: '#f6f1ee',
          tertiaryColor: '#ece7e4',
        },
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
</style>
