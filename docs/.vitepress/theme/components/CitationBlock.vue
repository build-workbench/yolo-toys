<script setup lang="ts">
/**
 * CitationBlock - Academic Citation Component
 *
 * Renders citations in an academic paper style with numbered references.
 */

defineProps<{
  number: number
  authors?: string
  title?: string
  venue?: string
  year?: string
  url?: string
}>()
</script>

<template>
  <div class="citation-block">
    <span class="citation-number">[{{ number }}]</span>
    <div class="citation-content">
      <!-- Slot for custom citation content -->
      <slot>
        <!-- Default format if props are provided -->
        <span v-if="authors" class="citation-authors">{{ authors }}</span>
        <span v-if="title" class="citation-title">
          <em>{{ title }}</em>
        </span>
        <span v-if="venue" class="citation-venue">{{ venue }}</span>
        <span v-if="year" class="citation-year">({{ year }})</span>
      </slot>
      <a v-if="url" :href="url" target="_blank" rel="noopener" class="citation-link">
        <span class="citation-link-icon">↗</span>
        Link
      </a>
    </div>
  </div>
</template>

<style scoped>
.citation-block {
  display: flex;
  gap: var(--space-3, 12px);
  padding: var(--space-3, 12px) var(--space-4, 16px);
  margin: var(--space-3, 12px) 0;
  border-radius: var(--radius-sm, 8px);
  background: var(--yt-canvas-soft, oklch(0.965 0.007 280));
  border-left: 3px solid var(--yt-brand, #e85524);
  font-size: var(--text-sm, 14px);
}

.citation-number {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm, 8px);
  background: var(--yt-brand-soft, oklch(0.95 0.04 45));
  color: var(--yt-brand, #e85524);
  font-weight: var(--font-bold, 700);
}

.citation-content {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: var(--space-2, 8px);
  color: var(--yt-text-soft, oklch(0.44 0.015 280));
  line-height: var(--leading-relaxed, 1.75);
}

.citation-authors::after {
  content: '.';
  margin-left: 0;
}

.citation-title {
  color: var(--yt-text, oklch(0.22 0.018 280));
  font-weight: var(--font-medium, 500);
}

.citation-title::after {
  content: '.';
  margin-left: 0;
}

.citation-venue {
  font-style: italic;
}

.citation-venue::before {
  content: ' ';
}

.citation-venue::after {
  content: '.';
  margin-left: 0;
}

.citation-year::before {
  content: ' ';
}

.citation-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1, 4px);
  margin-left: var(--space-2, 8px);
  color: var(--yt-brand, #e85524);
  text-decoration: none;
  font-size: var(--text-xs, 12px);
  font-weight: var(--font-semibold, 600);
  transition: opacity var(--duration-fast, 100ms) ease;
}

.citation-link:hover {
  opacity: 0.8;
}

.citation-link-icon {
  font-size: 10px;
}
</style>
