import DefaultTheme from 'vitepress/theme'
import { watch } from 'vue'
import { useRoute } from 'vitepress'
import './style.css'

const STORAGE_KEY = 'yolo-toys-lang-preference'

export default {
  extends: DefaultTheme,
  setup() {
    const route = useRoute()

    // 监听路由变化，自动更新语言偏好（仅客户端）
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
  }
}
