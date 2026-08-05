## 1. README 收敛为中文

- [x] 1.1 将 `README.zh-CN.md` 的中文内容写入 `README.md`，移除 `[English](README.md)` / `[简体中文](README.zh-CN.md)` 语言切换链接
- [x] 1.2 将 `README.md` 中 `https://lessup.github.io/yolo-toys/en/` 链接改为 `https://lessup.github.io/yolo-toys/zh/`
- [x] 1.3 删除 `README.zh-CN.md`

## 2. 删除英文文档树

- [x] 2.1 删除 `docs/en/` 整个目录（60 个文件）

## 3. VitePress 配置中文化

- [x] 3.1 在 `docs/.vitepress/config.ts` 移除 `locales.en` 块（含英文导航、侧边栏、editLink、docFooter、outline）
- [x] 3.2 将顶层 `title` / `description` 改为中文化（如 `YOLO-Toys 白皮书` / 中文描述）
- [x] 3.3 将 `sharedHead` 中 og/twitter 的 `content` 改为中文
- [x] 3.4 简化 `sharedHead` 中的 `lang-redirect` 脚本：仅当路径不以 `/zh/` 开头时重定向到 `/zh/`，移除 `en` 分支与 `localStorage` 探测
- [x] 3.5 将 `locales.zh` 提升为唯一 locale（保留 `label`/`lang`/`link`/`title`/`description` 与中文导航/侧边栏）

## 4. 入口页与主题清理

- [x] 4.1 将 `docs/index.md` 的 `<script setup>` 改为无条件 `router.go('/zh/')`，移除语言探测与 `localStorage` 逻辑
- [x] 4.2 清理 `docs/.vitepress/theme/index.ts` 中针对 `/en/` 的语言偏好追踪分支（保留 `/zh/` 写入或整体移除语言偏好追踪）

## 5. 验证

- [x] 5.1 全仓 grep `/en/`（排除 `docs/superpowers/`、`changelog/`、`node_modules`、`.git`），确认活跃表面无残留英文路径引用
- [x] 5.2 grep `README.zh-CN`，确认无活跃引用（`changelog/`、`VERIFICATION_REPORT.md` 等历史/审计文档中的提及可保留）
- [x] 5.3 若本地 Node 环境可用，运行 `cd docs && npm install --no-package-lock && npm run build` 验证 VitePress 构建；否则交由 CI `docs-pages.yml` 验证
