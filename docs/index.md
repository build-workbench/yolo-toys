---
layout: home
hero:
  name: YOLO-Toys
  text: ' '
  actions:
    - theme: brand
      text: 简体中文
      link: /zh/
    - theme: alt
      text: English
      link: /en/
---

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vitepress'

const STORAGE_KEY = 'yolo-toys-lang-preference'

onMounted(() => {
  const router = useRouter()

  // 优先使用保存的语言偏好
  const savedLang = localStorage.getItem(STORAGE_KEY)
  if (savedLang === 'zh' || savedLang === 'en') {
    router.go(`/${savedLang}/`)
    return
  }

  // 首次访问，根据浏览器语言检测
  const browserLang = navigator.language || navigator.userLanguage || ''
  const targetLang = browserLang.startsWith('zh') ? 'zh' : 'en'
  localStorage.setItem(STORAGE_KEY, targetLang)
  router.go(`/${targetLang}/`)
})
</script>
