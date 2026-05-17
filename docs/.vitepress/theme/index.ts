import DefaultTheme from 'vitepress/theme'
import { watch, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vitepress'

// Components
import WhitepaperLanding from './components/WhitepaperLanding.vue'
import ReadingTracks from './components/ReadingTracks.vue'
import FigureFrame from './components/FigureFrame.vue'
import SvgRenderer from './components/SvgRenderer.vue'
import MermaidDiagram from './components/MermaidDiagram.vue'
import CitationBlock from './components/CitationBlock.vue'
import CrossReference from './components/CrossReference.vue'

// Styles
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
    // SVG theme variables are now handled entirely by CSS (tokens.css)
    // No JS injection needed!
  }
}

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // Register components
    app.component('WhitepaperLanding', WhitepaperLanding)
    app.component('ReadingTracks', ReadingTracks)
    app.component('FigureFrame', FigureFrame)
    app.component('SvgRenderer', SvgRenderer)
    app.component('MermaidDiagram', MermaidDiagram)
    app.component('CitationBlock', CitationBlock)
    app.component('CrossReference', CrossReference)

    // Legacy alias for backwards compatibility during transition
    app.component('ThemeAwareSvg', SvgRenderer)
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
