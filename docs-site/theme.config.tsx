import { useRouter } from 'next/router'
import { LanguageToggle } from './components/LanguageToggle'

const config = {
  logo: (
    <>
      <span className="font-bold text-xl flex items-center gap-2">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="text-primary-600 dark:text-primary-400"
        >
          <rect x="2" y="2" width="20" height="20" rx="4" stroke="currentColor" strokeWidth="2"/>
          <circle cx="8" cy="8" r="2" fill="currentColor"/>
          <circle cx="16" cy="16" r="2" fill="currentColor"/>
          <circle cx="8" cy="16" r="1.5" fill="currentColor"/>
          <circle cx="16" cy="8" r="1.5" fill="currentColor"/>
        </svg>
        YOLO-Toys
      </span>
    </>
  ),
  project: {
    link: 'https://github.com/LessUp/yolo-toys',
  },
  docsRepositoryBase: 'https://github.com/LessUp/yolo-toys/tree/main/docs-site',
  useNextSeoProps() {
    const { asPath } = useRouter()
    const title = asPath === '/'
      ? 'YOLO-Toys - Multi-model Vision Inference Service'
      : '%s – YOLO-Toys'
    return {
      titleTemplate: title,
      description: 'Multi-model vision inference service with unified FastAPI + WebSocket interface',
      openGraph: {
        type: 'website',
        locale: 'en_US',
        url: 'https://lessup.github.io/yolo-toys',
        siteName: 'YOLO-Toys',
      },
      twitter: {
        cardType: 'summary_large_image',
      },
    }
  },
  head: (
    <>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="description" content="Multi-model vision inference service with unified FastAPI + WebSocket interface" />
      <meta property="og:title" content="YOLO-Toys" />
      <meta property="og:description" content="Multi-model vision inference service with YOLO, DETR, OWL-ViT, Grounding DINO, BLIP" />
      <link rel="icon" type="image/svg+xml" href="/yolo-toys/favicon.svg" />
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
    </>
  ),
  search: {
    placeholder: 'Search...',
  },
  toc: {
    title: 'On This Page',
  },
  editLink: {
    text: 'Edit this page on GitHub →',
  },
  feedback: {
    content: 'Question? Give us feedback →',
    labels: 'documentation',
  },
  footer: {
    text: (
      <div className="flex flex-col gap-2">
        <span>
          MIT {new Date().getFullYear()} ©{' '}
          <a href="https://github.com/LessUp" target="_blank" rel="noreferrer" className="hover:text-primary-600 transition-colors">
            LessUp
          </a>
        </span>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          Built with Nextra, Next.js & Tailwind CSS
        </span>
      </div>
    ),
  },
  // File-based i18n - we handle this through file structure
  // Nextra will use the path-based navigation
  darkMode: true,
  nextThemes: {
    defaultTheme: 'system',
    storageKey: 'yolo-toys-theme',
  },
  banner: {
    key: 'v3.1.0-release',
    text: (
      <a href="https://github.com/LessUp/yolo-toys/releases" target="_blank" rel="noreferrer">
        🎉 YOLO-Toys v3.1.0 is released. Read more →
      </a>
    ),
  },
  navbar: {
    extraContent: <LanguageToggle />,
  },
  sidebar: {
    defaultMenuCollapseLevel: 1,
    toggleButton: true,
  },
  navigation: {
    prev: true,
    next: true,
  },
}

export default config
