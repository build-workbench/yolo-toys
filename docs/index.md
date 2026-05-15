---
layout: home
---

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vitepress'

onMounted(() => {
  const router = useRouter()
  const STORAGE_KEY = 'yolo-toys-lang-preference'
  const saved = localStorage.getItem(STORAGE_KEY)

  if (saved === 'zh') {
    router.go('/zh/')
  } else if (saved === 'en') {
    router.go('/en/')
  } else {
    const lang = navigator.language || navigator.userLanguage || ''
    const target = lang.startsWith('zh') ? 'zh' : 'en'
    localStorage.setItem(STORAGE_KEY, target)
    router.go(`/${target}/`)
  }
})
</script>
