import DefaultTheme from 'vitepress/theme'
import { watch, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vitepress'
import WhitepaperLanding from './components/WhitepaperLanding.vue'
import ReadingTracks from './components/ReadingTracks.vue'
import FigureFrame from './components/FigureFrame.vue'
import ThemeAwareSvg from './components/ThemeAwareSvg.vue'
import MermaidDiagram from './components/MermaidDiagram.vue'
import './style.css'

const STORAGE_KEY = 'yolo-toys-lang-preference'

/**
 * Global reactive theme state that tracks VitePress dark mode.
 * This is more reliable than prefers-color-scheme because it follows
 * the VitePress theme toggle button, not just system preferences.
 */
export const isDark = ref(false)

function updateThemeState() {
  if (typeof document !== 'undefined') {
    const html = document.documentElement
    isDark.value = html.classList.contains('dark')
    // Sync SVG theme variables to the document so inline SVGs can react
    syncSvgThemeVariables(isDark.value)
  }
}

/**
 * Injects CSS custom properties into :root so that inline SVGs
 * (both <img> src SVGs and inline <svg>) can use them.
 */
function syncSvgThemeVariables(dark: boolean) {
  const root = document.documentElement
  if (dark) {
    root.style.setProperty('--svg-bg', '#1a1a1f')
    root.style.setProperty('--svg-panel', '#232329')
    root.style.setProperty('--svg-card', '#2a2a32')
    root.style.setProperty('--svg-ink', '#e8e6f0')
    root.style.setProperty('--svg-muted', '#a09eb8')
    root.style.setProperty('--svg-accent', '#ff8c5a')
    root.style.setProperty('--svg-accent-soft', 'rgba(255,140,90,0.15)')
    root.style.setProperty('--svg-wire', '#6b6880')
    root.style.setProperty('--svg-border', '#3d3d4a')
    root.style.setProperty('--svg-shadow', 'rgba(0,0,0,0.4)')
  } else {
    root.style.setProperty('--svg-bg', '#faf8f5')
    root.style.setProperty('--svg-panel', '#ffffff')
    root.style.setProperty('--svg-card', '#fffdfa')
    root.style.setProperty('--svg-ink', '#1c1a22')
    root.style.setProperty('--svg-muted', '#6b6680')
    root.style.setProperty('--svg-accent', '#e85524')
    root.style.setProperty('--svg-accent-soft', 'rgba(232,85,36,0.10)')
    root.style.setProperty('--svg-wire', '#9b96b0')
    root.style.setProperty('--svg-border', '#e0dbe8')
    root.style.setProperty('--svg-shadow', 'rgba(28,26,34,0.06)')
  }
}

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('WhitepaperLanding', WhitepaperLanding)
    app.component('ReadingTracks', ReadingTracks)
    app.component('FigureFrame', FigureFrame)
    app.component('ThemeAwareSvg', ThemeAwareSvg)
    app.component('MermaidDiagram', MermaidDiagram)
  },
  setup() {
    const route = useRoute()

    if (typeof window !== 'undefined') {
      // ---- Language preference tracking ----
      watch(
        () => route.path,
        (path) => {
          if (path.includes('/zh/')) {
            localStorage.setItem(STORAGE_KEY, 'zh')
          } else if (path.includes('/en/')) {
            localStorage.setItem(STORAGE_KEY, 'en')
          }
        },
        { immediate: true }
      )

      // ---- Dark mode detection via MutationObserver ----
      onMounted(() => {
        updateThemeState()

        const observer = new MutationObserver((mutations) => {
          for (const mutation of mutations) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
              updateThemeState()
            }
          }
        })

        observer.observe(document.documentElement, {
          attributes: true,
          attributeFilter: ['class'],
        })

        onUnmounted(() => {
          observer.disconnect()
        })
      })
    }
  },
}
