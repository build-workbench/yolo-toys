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
  ignoreDeadLinks: true,

  head: [
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
          { text: '入门指南', link: '/zh/getting-started/', activeMatch: '/zh/getting-started/' },
          { text: 'API 参考', link: '/zh/api/', activeMatch: '/zh/api/' },
          { text: '架构', link: '/zh/architecture/', activeMatch: '/zh/architecture/' },
          { text: '部署', link: '/zh/deployment/', activeMatch: '/zh/deployment/' },
          { text: '指南', link: '/zh/guides/', activeMatch: '/zh/guides/' },
          { text: '参考', link: '/zh/reference/', activeMatch: '/zh/reference/' },
        ],
        sidebar: {
          '/zh/getting-started/': [
            {
              text: '入门指南',
              items: [
                { text: '介绍', link: '/zh/getting-started/' },
                { text: '快速开始', link: '/zh/getting-started/quickstart' },
                { text: '安装', link: '/zh/getting-started/installation' },
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
              ],
            },
          ],
          '/zh/architecture/': [
            {
              text: '架构',
              items: [
                { text: '概述', link: '/zh/architecture/' },
                { text: '架构总览', link: '/zh/architecture/overview' },
                { text: 'Handler 架构', link: '/zh/architecture/handlers' },
              ],
            },
          ],
          '/zh/deployment/': [
            {
              text: '部署',
              items: [
                { text: '概述', link: '/zh/deployment/' },
                { text: 'Docker', link: '/zh/deployment/docker' },
                { text: '环境配置', link: '/zh/deployment/environments' },
              ],
            },
          ],
          '/zh/guides/': [
            {
              text: '指南',
              items: [
                { text: '概述', link: '/zh/guides/' },
                { text: '添加模型', link: '/zh/guides/adding-models' },
              ],
            },
          ],
          '/zh/reference/': [
            {
              text: '参考',
              items: [
                { text: '概述', link: '/zh/reference/' },
                { text: '模型列表', link: '/zh/reference/models' },
                { text: '常见问题', link: '/zh/reference/faq' },
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
          { text: 'Getting Started', link: '/en/getting-started/', activeMatch: '/en/getting-started/' },
          { text: 'API Reference', link: '/en/api/', activeMatch: '/en/api/' },
          { text: 'Architecture', link: '/en/architecture/', activeMatch: '/en/architecture/' },
          { text: 'Deployment', link: '/en/deployment/', activeMatch: '/en/deployment/' },
          { text: 'Guides', link: '/en/guides/', activeMatch: '/en/guides/' },
          { text: 'Reference', link: '/en/reference/', activeMatch: '/en/reference/' },
        ],
        sidebar: {
          '/en/getting-started/': [
            {
              text: 'Getting Started',
              items: [
                { text: 'Introduction', link: '/en/getting-started/' },
                { text: 'Quick Start', link: '/en/getting-started/quickstart' },
                { text: 'Installation', link: '/en/getting-started/installation' },
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
              ],
            },
          ],
          '/en/architecture/': [
            {
              text: 'Architecture',
              items: [
                { text: 'Overview', link: '/en/architecture/' },
                { text: 'Architecture Overview', link: '/en/architecture/overview' },
                { text: 'Handler Architecture', link: '/en/architecture/handlers' },
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
              ],
            },
          ],
          '/en/guides/': [
            {
              text: 'Guides',
              items: [
                { text: 'Overview', link: '/en/guides/' },
                { text: 'Adding Models', link: '/en/guides/adding-models' },
              ],
            },
          ],
          '/en/reference/': [
            {
              text: 'Reference',
              items: [
                { text: 'Overview', link: '/en/reference/' },
                { text: 'Models', link: '/en/reference/models' },
                { text: 'FAQ', link: '/en/reference/faq' },
              ],
            },
          ],
        },
      },
    },
  },

  themeConfig: {
    outline: [2, 3],
    search: { provider: 'local' },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/LessUp/yolo-toys' },
    ],
  },

  vite: {
    plugins: [llmstxt()],
  },
}))
