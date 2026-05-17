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

    <section class="yt-whitepaper__tracks">
      <div class="yt-section-label">Reading tracks</div>
      <div class="yt-section-heading">
        Enter through architecture, operations, or extensibility, not through a generic docs dump.
      </div>
      <div class="yt-section-body">
        The site is structured as an academy and project atlas. Each path below is optimized for a different kind of advanced reader.
      </div>
      <slot name="tracks" />
    </section>
  </article>
</template>
