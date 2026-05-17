import DefaultTheme from 'vitepress/theme'
import { watch } from 'vue'
import { useRoute } from 'vitepress'
import WhitepaperLanding from './components/WhitepaperLanding.vue'
import ReadingTracks from './components/ReadingTracks.vue'
import FigureFrame from './components/FigureFrame.vue'
import './style.css'

const STORAGE_KEY = 'yolo-toys-lang-preference'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('WhitepaperLanding', WhitepaperLanding)
    app.component('ReadingTracks', ReadingTracks)
    app.component('FigureFrame', FigureFrame)
  },
  setup() {
    const route = useRoute()

    if (typeof window !== 'undefined') {
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
    }
  },
}
