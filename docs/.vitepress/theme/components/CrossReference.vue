<script setup lang="ts">
/**
 * CrossReference - Cross-reference Component
 *
 * Creates styled links to related content within the documentation.
 */

defineProps<{
  href: string
  label?: string
  section?: string
}>()
</script>

<template>
  <a :href="href" class="cross-reference">
    <span v-if="section" class="cross-section">{{ section }}</span>
    <span class="cross-label">
      <slot>{{ label }}</slot>
    </span>
    <span class="cross-arrow">→</span>
  </a>
</template>

<style scoped>
.cross-reference {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2, 8px);
  padding: var(--space-1, 4px) var(--space-3, 12px);
  border-radius: var(--radius-sm, 8px);
  background: var(--yt-accent-soft, oklch(0.94 0.03 260));
  color: var(--yt-accent, #4f6cf5);
  font-size: var(--text-sm, 14px);
  font-weight: var(--font-medium, 500);
  text-decoration: none;
  transition: all var(--duration-fast, 100ms) ease;
}

.cross-reference:hover {
  background: var(--yt-accent, #4f6cf5);
  color: var(--yt-text-inverted, oklch(0.98 0.01 60));
}

.cross-section {
  font-size: var(--text-xs, 12px);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider, 0.05em);
  opacity: 0.7;
}

.cross-section::after {
  content: ':';
  margin-right: var(--space-1, 4px);
}

.cross-arrow {
  font-size: 12px;
  opacity: 0.8;
  transition: transform var(--duration-fast, 100ms) ease;
}

.cross-reference:hover .cross-arrow {
  transform: translateX(2px);
}
</style>
