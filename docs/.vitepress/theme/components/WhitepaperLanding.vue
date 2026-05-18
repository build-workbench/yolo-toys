<script setup lang="ts">
defineProps<{
  eyebrow: string
  chapter: string
  title: string
  abstract: string
  primaryLabel: string
  primaryHref: string
  secondaryLabel: string
  secondaryHref: string
  tertiaryLabel: string
  tertiaryHref: string
  githubHref: string
}>()
</script>

<template>
  <article class="yt-whitepaper">
    <section class="yt-whitepaper__hero">
      <div class="yt-whitepaper__copy">
        <div class="yt-kicker">
          <span class="yt-kicker__eyebrow">{{ eyebrow }}</span>
          <span class="yt-kicker__chapter">{{ chapter }}</span>
        </div>
        <h1 class="yt-whitepaper__title">{{ title }}</h1>
        <p class="yt-whitepaper__abstract">{{ abstract }}</p>
        <div class="yt-whitepaper__actions">
          <a class="yt-button yt-button--primary" :href="primaryHref">{{ primaryLabel }}</a>
          <a class="yt-button" :href="secondaryHref">{{ secondaryLabel }}</a>
          <a class="yt-button" :href="tertiaryHref">{{ tertiaryLabel }}</a>
          <a class="yt-button yt-button--ghost" :href="githubHref" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </div>

      <div class="yt-whitepaper__figure">
        <slot name="figure" />
      </div>
    </section>

    <section class="yt-signal-strip">
      <slot name="signals" />
    </section>

    <!-- Stats Grid — technical metrics highlight -->
    <section v-if="$slots.stats" class="yt-whitepaper__stats">
      <slot name="stats" />
    </section>

    <!-- Blueprint — architecture layer overview -->
    <section v-if="$slots.blueprint" class="yt-whitepaper__blueprint">
      <slot name="blueprint" />
    </section>

    <section class="yt-whitepaper__tracks">
      <div class="yt-section-label">Reading tracks</div>
      <div class="yt-section-heading">
        Enter through architecture, operations, or research — each path is optimized for a different kind of expert reader.
      </div>
      <div class="yt-section-body">
        The site is structured as a technical whitepaper with an academy and research wing. Every reading track is designed for advanced readers who want both the how and the why.
      </div>
      <slot name="tracks" />
    </section>
  </article>
</template>
