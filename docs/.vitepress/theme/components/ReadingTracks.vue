<script setup lang="ts">
defineProps<{
  tracks: Array<{
    title: string
    summary: string
    href: string
  }>
}>()
</script>

<template>
  <div class="yt-reading-tracks">
    <a
      v-for="track in tracks"
      :key="track.title"
      class="yt-reading-track"
      :href="track.href"
    >
      <div class="yt-reading-track__title">{{ track.title }}</div>
      <p class="yt-reading-track__summary">{{ track.summary }}</p>
      <span class="yt-reading-track__cta">Open chapter</span>
    </a>
  </div>
</template>
