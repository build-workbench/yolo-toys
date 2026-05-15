import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import llmstxt from 'vitepress-plugin-llms'

const rawBase = process.env.VITEPRESS_BASE
const base = rawBase
  ? rawBase.startsWith('/')
    ? rawBase.endsWith('/') ? rawBase : `${rawBase}/`
    : `/${rawBase}/`
  : '/'

export default withMermaid(defineConfig({
  base,
  title: 'YOLO-Toys Docs',
  description: 'YOLO-Toys Documentation',
  lastUpdated: true,
  cleanUrls: true,
  ignoreDeadLinks: [
    // 忽略 localhost 链接（用于开发示例）
    /^http:\/\/localhost/,
  ],

  sitemap: {
    hostname: 'https://lessup.github.io/yolo-toys/'
  },

  head: [
    ['meta', { name: 'theme-color', content: '#FF6B35' }],
    ['meta', { name: 'og:type', content: 'website' }],
    [
      'script',
      { id: 'lang-redirect' },
      `((() => {
  // 已在语言路径下，跳过
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
})())`
    ]
  ],

  locales: {
    zh: {
      label: '简体中文',
      lang: 'zh-CN',
      link: '/zh/',
      title: 'YOLO-Toys 文档',
      description: 'YOLO-Toys 多模型视觉推理服务文档',
      themeConfig: {
        nav: [
          { text: '学院', link: '/zh/academy/', activeMatch: '/zh/academy/' },
          { text: '指南', link: '/zh/guides/', activeMatch: '/zh/guides/' },
          { text: 'API', link: '/zh/api/', activeMatch: '/zh/api/' },
          { text: '架构', link: '/zh/architecture/', activeMatch: '/zh/architecture/' },
          { text: '部署', link: '/zh/deployment/', activeMatch: '/zh/deployment/' },
          { text: '参考', link: '/zh/reference/', activeMatch: '/zh/reference/' },
        ],
        editLink: {
          pattern: 'https://github.com/LessUp/yolo-toys/edit/master/docs/:path',
          text: '在 GitHub 上编辑此页'
        },
        lastUpdatedText: '最后更新',
        docFooter: {
          prev: '上一页',
          next: '下一页'
        },
        outline: {
          label: '目录'
        },
        sidebar: {
          '/zh/academy/': [
            {
              text: '深度学院',
              items: [
                { text: '概述', link: '/zh/academy/' },
                { text: 'Handler 模式', link: '/zh/academy/handler-pattern' },
                { text: 'Registry 模式', link: '/zh/academy/registry-pattern' },
                { text: '缓存策略', link: '/zh/academy/caching-strategy' },
                { text: 'OpenSpec 体系', link: '/zh/academy/openspec-system' },
              ],
            },
          ],
          '/zh/guides/': [
            {
              text: '开发指南',
              items: [
                { text: '概述', link: '/zh/guides/' },
                { text: '添加模型', link: '/zh/guides/adding-models' },
                { text: '自定义 Handler', link: '/zh/guides/custom-handler' },
                { text: '性能调优', link: '/zh/guides/performance-tuning' },
              ],
            },
          ],
          '/zh/api/': [
            {
              text: 'API 参考',
              items: [
                { text: '概述', link: '/zh/api/' },
                { text: 'REST API', link: '/zh/api/rest-api' },
                { text: 'WebSocket', link: '/zh/api/websocket' },
                { text: '错误码', link: '/zh/api/error-codes' },
              ],
            },
          ],
          '/zh/architecture/': [
            {
              text: '系统架构',
              items: [
                { text: '概述', link: '/zh/architecture/' },
                { text: '系统总览', link: '/zh/architecture/overview' },
                { text: 'Handler 架构', link: '/zh/architecture/handlers' },
                { text: '请求流程', link: '/zh/architecture/request-flow' },
              ],
            },
            {
              text: '架构决策记录',
              items: [
                { text: '001: Handler 模式', link: '/zh/architecture/adr/001-handler-pattern' },
                { text: '002: Registry 模式', link: '/zh/architecture/adr/002-registry-pattern' },
                { text: '003: 缓存策略', link: '/zh/architecture/adr/003-caching-strategy' },
              ],
            },
          ],
          '/zh/deployment/': [
            {
              text: '部署运维',
              items: [
                { text: '概述', link: '/zh/deployment/' },
                { text: 'Docker', link: '/zh/deployment/docker' },
                { text: '环境配置', link: '/zh/deployment/environments' },
                { text: 'Kubernetes', link: '/zh/deployment/kubernetes' },
                { text: '监控告警', link: '/zh/deployment/monitoring' },
              ],
            },
          ],
          '/zh/reference/': [
            {
              text: '参考资料',
              items: [
                { text: '概述', link: '/zh/reference/' },
                { text: '模型列表', link: '/zh/reference/models' },
                { text: '性能基准', link: '/zh/reference/benchmarks' },
                { text: '竞品对比', link: '/zh/reference/comparisons' },
                { text: '常见问题', link: '/zh/reference/faq' },
                { text: '更新日志', link: '/zh/reference/changelog' },
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
      title: 'YOLO-Toys Docs',
      description: 'YOLO-Toys Multi-model Vision Inference Service',
      themeConfig: {
        nav: [
          { text: 'Academy', link: '/en/academy/', activeMatch: '/en/academy/' },
          { text: 'Guides', link: '/en/guides/', activeMatch: '/en/guides/' },
          { text: 'API', link: '/en/api/', activeMatch: '/en/api/' },
          { text: 'Architecture', link: '/en/architecture/', activeMatch: '/en/architecture/' },
          { text: 'Deployment', link: '/en/deployment/', activeMatch: '/en/deployment/' },
          { text: 'Reference', link: '/en/reference/', activeMatch: '/en/reference/' },
        ],
        editLink: {
          pattern: 'https://github.com/LessUp/yolo-toys/edit/master/docs/:path',
          text: 'Edit this page on GitHub'
        },
        lastUpdatedText: 'Last updated',
        docFooter: {
          prev: 'Previous',
          next: 'Next'
        },
        outline: {
          label: 'On this page'
        },
        sidebar: {
          '/en/academy/': [
            {
              text: 'Academy',
              items: [
                { text: 'Overview', link: '/en/academy/' },
                { text: 'Handler Pattern', link: '/en/academy/handler-pattern' },
                { text: 'Registry Pattern', link: '/en/academy/registry-pattern' },
                { text: 'Caching Strategy', link: '/en/academy/caching-strategy' },
                { text: 'OpenSpec System', link: '/en/academy/openspec-system' },
              ],
            },
          ],
          '/en/guides/': [
            {
              text: 'Guides',
              items: [
                { text: 'Overview', link: '/en/guides/' },
                { text: 'Adding Models', link: '/en/guides/adding-models' },
                { text: 'Custom Handler', link: '/en/guides/custom-handler' },
                { text: 'Performance Tuning', link: '/en/guides/performance-tuning' },
              ],
            },
          ],
          '/en/api/': [
            {
              text: 'API Reference',
              items: [
                { text: 'Overview', link: '/en/api/' },
                { text: 'REST API', link: '/en/api/rest-api' },
                { text: 'WebSocket', link: '/en/api/websocket' },
                { text: 'Error Codes', link: '/en/api/error-codes' },
              ],
            },
          ],
          '/en/architecture/': [
            {
              text: 'Architecture',
              items: [
                { text: 'Overview', link: '/en/architecture/' },
                { text: 'System Overview', link: '/en/architecture/overview' },
                { text: 'Handlers', link: '/en/architecture/handlers' },
                { text: 'Request Flow', link: '/en/architecture/request-flow' },
              ],
            },
            {
              text: 'ADR',
              items: [
                { text: '001: Handler Pattern', link: '/en/architecture/adr/001-handler-pattern' },
                { text: '002: Registry Pattern', link: '/en/architecture/adr/002-registry-pattern' },
                { text: '003: Caching Strategy', link: '/en/architecture/adr/003-caching-strategy' },
              ],
            },
          ],
          '/en/deployment/': [
            {
              text: 'Deployment',
              items: [
                { text: 'Overview', link: '/en/deployment/' },
                { text: 'Docker', link: '/en/deployment/docker' },
                { text: 'Environments', link: '/en/deployment/environments' },
                { text: 'Kubernetes', link: '/en/deployment/kubernetes' },
                { text: 'Monitoring', link: '/en/deployment/monitoring' },
              ],
            },
          ],
          '/en/reference/': [
            {
              text: 'Reference',
              items: [
                { text: 'Overview', link: '/en/reference/' },
                { text: 'Models', link: '/en/reference/models' },
                { text: 'Benchmarks', link: '/en/reference/benchmarks' },
                { text: 'Comparisons', link: '/en/reference/comparisons' },
                { text: 'FAQ', link: '/en/reference/faq' },
                { text: 'Changelog', link: '/en/reference/changelog' },
              ],
            },
          ],
        },
      },
    },
  },

  themeConfig: {
    logo: '/images/logo.svg',
    outline: [2, 3],
    search: { provider: 'local' },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/LessUp/yolo-toys' },
    ],
    editLink: {
      pattern: 'https://github.com/LessUp/yolo-toys/edit/master/docs/:path',
      text: 'Edit this page on GitHub'
    },
    lastUpdatedText: 'Last updated',
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024-present LessUp'
    },
  },

  mermaid: {
    theme: 'base',
    themeVariables: {
      primaryColor: '#FF6B35',
      primaryTextColor: '#24292f',
      primaryBorderColor: '#d0d7de',
      lineColor: '#57606a',
      secondaryColor: '#f6f8fa',
      tertiaryColor: '#eaefef'
    }
  },

  vite: {
    plugins: [llmstxt()],
  },
}))
