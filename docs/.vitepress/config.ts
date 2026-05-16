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
  ['meta', { name: 'theme-color', content: '#ff6b35' }],
  ['meta', { name: 'og:type', content: 'website' }],
  [
    'script',
    { id: 'lang-redirect' },
    `((() => {
  if (location.pathname.match(/\\/(zh|en)(\\/|$)/)) return;

  const STORAGE_KEY = 'yolo-toys-lang-preference';
  const saved = localStorage.getItem(STORAGE_KEY);

  if (saved === 'zh' || saved === 'en') {
    window.location.replace(saved + '/');
    return;
  }

  const lang = navigator.language || navigator.userLanguage || '';
  const target = lang.startsWith('zh') ? 'zh' : 'en';
  localStorage.setItem(STORAGE_KEY, target);
  window.location.replace(target + '/');
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
  title: 'YOLO-Toys Whitepaper',
  description: 'A bilingual architecture and research guide for the YOLO-Toys multi-model vision serving stack.',
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
          { text: '学院', link: '/zh/academy/' },
          { text: '参考', link: '/zh/reference/' },
          { text: '研究', link: '/zh/research/' },
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
          '/zh/academy/': [
            {
              text: '学院',
              items: [
                { text: '学院首页', link: '/zh/academy/' },
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
              ],
            },
          ],
        },
      },
    },
    en: {
      label: 'English',
      lang: 'en-US',
      link: '/en/',
      title: 'YOLO-Toys Whitepaper',
      description: 'A whitepaper-grade architecture and research guide for the YOLO-Toys serving stack.',
      themeConfig: {
        nav: [
          { text: 'Overview', link: '/en/' },
          { text: 'Primer', link: '/en/primer/' },
          { text: 'Architecture', link: '/en/architecture/' },
          { text: 'Academy', link: '/en/academy/' },
          { text: 'Reference', link: '/en/reference/' },
          { text: 'Research', link: '/en/research/' },
        ],
        editLink: {
          pattern: 'https://github.com/LessUp/yolo-toys/edit/master/docs/:path',
          text: 'Edit this page on GitHub',
        },
        lastUpdatedText: 'Last updated',
        docFooter: {
          prev: 'Previous',
          next: 'Next',
        },
        outline: {
          label: 'On this page',
        },
        sidebar: {
          '/en/primer/': [
            {
              text: 'Primer',
              items: [
                { text: 'Primer Home', link: '/en/primer/' },
                { text: 'Quickstart', link: '/en/getting-started/quickstart' },
                { text: 'Installation', link: '/en/getting-started/installation' },
                { text: 'Deployment Overview', link: '/en/deployment/' },
              ],
            },
          ],
          '/en/architecture/': [
            {
              text: 'Architecture Atlas',
              items: [
                { text: 'Chapter Home', link: '/en/architecture/' },
                { text: 'System Overview', link: '/en/architecture/overview' },
                { text: 'Request Lifecycle', link: '/en/architecture/request-flow' },
                { text: 'Handler Topology', link: '/en/architecture/handlers' },
              ],
            },
            {
              text: 'Decision Records',
              items: [
                { text: '001: Handler Pattern', link: '/en/architecture/adr/001-handler-pattern' },
                { text: '002: Registry Pattern', link: '/en/architecture/adr/002-registry-pattern' },
                { text: '003: Caching Strategy', link: '/en/architecture/adr/003-caching-strategy' },
              ],
            },
          ],
          '/en/academy/': [
            {
              text: 'Academy',
              items: [
                { text: 'Academy Home', link: '/en/academy/' },
                { text: 'Handler Pattern', link: '/en/academy/handler-pattern' },
                { text: 'Registry Pattern', link: '/en/academy/registry-pattern' },
                { text: 'Caching Strategy', link: '/en/academy/caching-strategy' },
                { text: 'OpenSpec System', link: '/en/academy/openspec-system' },
              ],
            },
          ],
          '/en/reference/': [
            {
              text: 'Reference',
              items: [
                { text: 'Reference Home', link: '/en/reference/' },
                { text: 'Model Matrix', link: '/en/reference/models' },
                { text: 'Benchmarks', link: '/en/reference/benchmarks' },
                { text: 'Comparisons', link: '/en/reference/comparisons' },
                { text: 'FAQ', link: '/en/reference/faq' },
                { text: 'Changelog', link: '/en/reference/changelog' },
              ],
            },
          ],
          '/en/research/': [
            {
              text: 'Research',
              items: [
                { text: 'Research Home', link: '/en/research/' },
                { text: 'Bibliography', link: '/en/citations' },
                { text: 'Comparative Analysis', link: '/en/reference/comparisons' },
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
      primaryColor: '#fff2ec',
      primaryTextColor: '#1e2933',
      primaryBorderColor: '#ffb08b',
      lineColor: '#6f6b73',
      secondaryColor: '#f6f1ee',
      tertiaryColor: '#ece7e4',
    },
  },
  vite: {
    plugins: [llmstxt()],
  },
}))
