import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import llmstxt from 'vitepress-plugin-llms'

const rawBase = process.env.VITEPRESS_BASE
const base = rawBase
  ? rawBase.startsWith('/')
    ? rawBase.endsWith('/') ? rawBase : `${rawBase}/`
    : `/${rawBase}/`
  : '/'

const sharedHead = [
  ['meta', { name: 'theme-color', content: '#e85524' }],
  ['meta', { name: 'og:type', content: 'website' }],
  ['meta', { property: 'og:title', content: 'YOLO-Toys 白皮书' }],
  ['meta', { property: 'og:description', content: 'YOLO-Toys 多模型视觉推理平台的架构白皮书与研究导读。' }],
  ['meta', { property: 'og:image', content: 'https://lessup.github.io/yolo-toys/assets/images/og-image.svg' }],
  ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
  ['meta', { name: 'twitter:title', content: 'YOLO-Toys 白皮书' }],
  ['meta', { name: 'twitter:description', content: 'YOLO-Toys 架构图谱、学院、参考与研究导读。' }],
  ['meta', { name: 'twitter:image', content: 'https://lessup.github.io/yolo-toys/assets/images/og-image.svg' }],
  [
    'script',
    { id: 'lang-redirect' },
    `((() => {
  if (location.pathname.match(/\\/(zh)(\\/|\$)/)) return;

  window.location.replace('zh/');
})())`,
  ],
]

const sharedThemeConfig = {
  outline: [2, 3] as [number, number],
  search: { provider: 'local' as const },
  socialLinks: [
    { icon: 'github', link: 'https://github.com/LessUp/yolo-toys' },
  ],
  footer: {
    message: 'Released under the MIT License.',
    copyright: 'Copyright © 2024-present LessUp',
  },
}

export default withMermaid(defineConfig({
  base,
  title: 'YOLO-Toys 白皮书',
  description: 'YOLO-Toys 多模型视觉推理平台的架构白皮书与研究导读。',
  lastUpdated: true,
  cleanUrls: true,
  ignoreDeadLinks: [/^http:\/\/localhost/],
  sitemap: {
    hostname: 'https://lessup.github.io/yolo-toys/',
  },
  head: sharedHead,
  locales: {
    zh: {
      label: '简体中文',
      lang: 'zh-CN',
      link: '/zh/',
      title: 'YOLO-Toys 白皮书',
      description: 'YOLO-Toys 多模型视觉推理平台的架构白皮书与研究导读。',
      themeConfig: {
        nav: [
          { text: '总览', link: '/zh/' },
          { text: '导读', link: '/zh/primer/' },
          { text: '架构', link: '/zh/architecture/' },
          { text: '理论', link: '/zh/theory/' },
          { text: '学院', link: '/zh/academy/' },
          { text: '参考', link: '/zh/reference/' },
          { text: '研究', link: '/zh/research/' },
          { text: 'API', link: '/zh/api/' },
        ],
        editLink: {
          pattern: 'https://github.com/LessUp/yolo-toys/edit/master/docs/:path',
          text: '在 GitHub 上编辑此页',
        },
        lastUpdatedText: '最后更新',
        docFooter: {
          prev: '上一页',
          next: '下一页',
        },
        outline: {
          label: '目录',
        },
        sidebar: {
          '/zh/primer/': [
            {
              text: '项目导读',
              items: [
                { text: '导读首页', link: '/zh/primer/' },
                { text: '快速开始', link: '/zh/getting-started/quickstart' },
                { text: '安装', link: '/zh/getting-started/installation' },
                { text: '部署概览', link: '/zh/deployment/' },
              ],
            },
          ],
          '/zh/architecture/': [
            {
              text: '架构图谱',
              items: [
                { text: '章节首页', link: '/zh/architecture/' },
                { text: '系统总览', link: '/zh/architecture/overview' },
                { text: '请求流程', link: '/zh/architecture/request-flow' },
                { text: '处理器体系', link: '/zh/architecture/handlers' },
                { text: '模型加载', link: '/zh/architecture/model-loading' },
                { text: '中间件栈', link: '/zh/architecture/middleware-stack' },
                { text: '配置注入', link: '/zh/architecture/config-injection' },
                { text: '模型缓存', link: '/zh/architecture/model-cache' },
                { text: '安全模型', link: '/zh/architecture/security-model' },
              ],
            },
            {
              text: '架构决策',
              items: [
                { text: '001: Handler Pattern', link: '/zh/architecture/adr/001-handler-pattern' },
                { text: '002: Registry Pattern', link: '/zh/architecture/adr/002-registry-pattern' },
                { text: '003: Caching Strategy', link: '/zh/architecture/adr/003-caching-strategy' },
              ],
            },
          ],
          '/zh/theory/': [
            {
              text: '理论与算法',
              items: [
                { text: '章节首页', link: '/zh/theory/' },
              ],
            },
            {
              text: '检测算法',
              items: [
                { text: '检测概览', link: '/zh/theory/detection/' },
                { text: 'YOLO 家族演进', link: '/zh/theory/detection/yolo-family' },
                { text: 'DETR 架构', link: '/zh/theory/detection/detr-transformer' },
                { text: '检测范式对比', link: '/zh/theory/detection/detection-paradigms' },
              ],
            },
            {
              text: '视觉语言模型',
              items: [
                { text: 'VLM 概览', link: '/zh/theory/vlm/' },
                { text: 'OWL-ViT', link: '/zh/theory/vlm/owl-vit' },
                { text: 'Grounding DINO', link: '/zh/theory/vlm/grounding-dino' },
                { text: 'BLIP', link: '/zh/theory/vlm/blip' },
              ],
            },
            {
              text: '训练背景',
              items: [
                { text: '训练概览', link: '/zh/theory/training/' },
                { text: '损失函数', link: '/zh/theory/training/loss-functions' },
              ],
            },
          ],
          '/zh/academy/': [
            {
              text: '学院',
              items: [
                { text: '学院首页', link: '/zh/academy/' },
                { text: '深度模块', link: '/zh/academy/deep-modules' },
                { text: 'Handler 模式', link: '/zh/academy/handler-pattern' },
                { text: 'Registry 模式', link: '/zh/academy/registry-pattern' },
                { text: '缓存策略', link: '/zh/academy/caching-strategy' },
                { text: 'OpenSpec 体系', link: '/zh/academy/openspec-system' },
              ],
            },
          ],
          '/zh/reference/': [
            {
              text: '参考',
              items: [
                { text: '参考首页', link: '/zh/reference/' },
                { text: '模型矩阵', link: '/zh/reference/models' },
                { text: '配置参考', link: '/zh/reference/configuration-reference' },
                { text: 'Prometheus 指标', link: '/zh/reference/metrics-reference' },
                { text: '性能基准', link: '/zh/reference/benchmarks' },
                { text: '竞品对比', link: '/zh/reference/comparisons' },
                { text: 'FAQ', link: '/zh/reference/faq' },
                { text: '更新日志', link: '/zh/reference/changelog' },
              ],
            },
          ],
          '/zh/research/': [
            {
              text: '研究',
              items: [
                { text: '研究首页', link: '/zh/research/' },
                { text: '参考文献', link: '/zh/citations' },
                { text: '竞品探究', link: '/zh/reference/comparisons' },
                { text: '演进思考', link: '/zh/research/evolution' },
              ],
            },
          ],
        },
      },
    },
  },
  themeConfig: sharedThemeConfig,
  mermaid: {
    theme: 'base',
    themeVariables: {
      // Aligned with design tokens from tokens.css
      primaryColor: 'var(--svg-surface-alt, #fffdfa)',
      primaryTextColor: 'var(--svg-ink, #1c1a22)',
      primaryBorderColor: 'var(--svg-border, #e0dbe8)',
      lineColor: 'var(--svg-wire, #9b96b0)',
      secondaryColor: 'var(--svg-surface, #ffffff)',
      tertiaryColor: 'var(--svg-canvas, #faf8f5)',
      fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
      fontSize: '14px',
    },
  },
  vite: {
    plugins: [llmstxt()],
  },
}))
