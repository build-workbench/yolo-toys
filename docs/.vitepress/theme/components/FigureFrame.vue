<script setup lang="ts">
defineProps<{
  title: string
  caption?: string
}>()
</script>

<template>
  <figure class="yt-figure">
    <figcaption class="yt-figure__title">{{ title }}</figcaption>
    <div class="yt-figure__body">
      <slot />
    </div>
    <p v-if="caption" class="yt-figure__caption">{{ caption }}</p>
  </figure>
</template>
