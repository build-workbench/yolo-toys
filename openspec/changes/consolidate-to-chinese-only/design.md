## Context

YOLO-Toys 的公共表面当前是双语对等维护：

- 仓库入口：`README.md`（英）与 `README.zh-CN.md`（中），互相交叉链接。
- GitHub Pages（VitePress，源在 `docs/`）：`docs/en/` 与 `docs/zh/` 两套并列文档树（各 60 文件），由 `docs/.vitepress/config.ts` 的 `locales.en` / `locales.zh` 分别配置导航与侧边栏。
- 入口分发：`docs/index.md` 通过 `localStorage` + `navigator.language` 在 `/zh/` 与 `/en/` 间分发；`config.ts` 的 `head` 注入一段 `lang-redirect` 脚本做同样的事；`theme/index.ts` 在路由变化时写入语言偏好。

项目处于 finalization mode，AGENTS.md 明确"优先减少漂移与冗余而非新增表面"。维护对等英文翻译的成本与项目收尾目标不一致。

## Goals / Non-Goals

### Goals
- README 收敛为单一中文入口，无语言切换链接。
- Pages 仅保留 `docs/zh/`，移除 `docs/en/`、`en` locale 及英文导航/侧边栏。
- 站点入口（`docs/index.md`）与 `head` 重定向脚本简化为直接进入 `/zh/`。
- 站点元数据（title/description/og/twitter）改为中文。
- 不破坏 VitePress 构建：所有保留链接指向 `/zh/` 或外部地址，无死链指向 `/en/`。

### Non-Goals
- 不翻译或删除 `changelog/` 历史发布条目（changelog 仅作发布历史）。
- 不改动 `docs/superpowers/`、`docs/public/` 等非活跃规划/静态资源内容，除非它们直接阻塞构建。
- 不改动运行时代码与测试。
- 不强制更新 GitHub 仓库 `gh` 元数据，除非现有描述显式声明双语。

## Design Decisions

### Decision: README 合并为单一中文 `README.md`

将 `README.zh-CN.md` 的中文内容作为新 `README.md`，删除 `README.zh-CN.md`，并移除 `[English](README.md)` / `[简体中文](README.zh-CN.md)` 切换链接。GitHub 仓库默认入口 `README.md` 即中文，符合目标受众。

**Alternatives considered**
- 保留两文件但都改中文：拒绝，会产生重复内容，违反"公共表面职责互斥"。
- 保留英文 `README.md` 作为主入口：拒绝，与"只保留中文"诉求冲突。

### Decision: 删除整个 `docs/en/` 并移除 `en` locale

VitePress `locales` 移除 `en`，导航/侧边栏仅保留 `zh`。`docs/en/` 整目录删除，避免死链与孤立内容。`config.ts` 顶层 `title`/`description` 与 `sharedHead` 的 og/twitter 元数据改为中文。

**Alternatives considered**
- 保留 `docs/en/` 但不在导航暴露：拒绝，仍可被直接访问且需持续维护翻译漂移，违背"只保留中文"。
- 仅删除 `docs/en/` 内容但保留 locale 占位：拒绝，空 locale 会产生空导航/死链。

### Decision: 入口分发简化为直接 `/zh/`

`docs/index.md` 的 `<script setup>` 改为无条件 `router.go('/zh/')`；`config.ts` `head` 中的 `lang-redirect` 脚本改为：仅当不在 `/zh/` 时重定向到 `/zh/`，移除 `en` 分支与 `localStorage` 语言探测。`theme/index.ts` 移除 `/en/` 路径分支，仅保留 `/zh/` 偏好写入（或整体移除语言偏好追踪，因不再有多语言）。

**Alternatives considered**
- 保留 `localStorage` 语言探测但默认 `zh`：拒绝，仍为单语言场景保留无意义分支。
- 完全移除 `index.md` 重定向、靠 `head` 脚本：拒绝，`index.md` 的 Vue 重定向是 VitePress 入口页，移除会破坏根路径渲染。

### Decision: `changelog/` 与历史规划文档保持原貌

`changelog/` 是发布历史，AGENTS.md 明确"仅用于发布历史"。历史英文条目（`v3.0.0.md`、`v3.1.0.md`、`CHANGELOG.md` 等）不回改。`docs/superpowers/plans/` 是历史规划记录，不作为活跃表面，保持原貌。

**Alternatives considered**
- 同步翻译/删除英文 changelog：拒绝，违反 changelog 仅作历史记录的规则，且破坏历史可追溯性。

## Risks / Trade-offs

- **[Risk] 删除 `docs/en/` 不可逆** → Mitigation: 通过 Git 历史可恢复；实施前确认范围已与用户对齐。
- **[Risk] 残留指向 `/en/` 的链接导致死链** → Mitigation: 实施后全仓 grep `/en/`（排除 `docs/superpowers/`、`changelog/`、`node_modules`），逐一修正；VitePress `ignoreDeadLinks` 仅放行 localhost。
- **[Risk] `theme/index.ts` 移除语言追踪后组件依赖断裂** → Mitigation: 语言偏好追踪仅用于写入 `localStorage`，无组件消费该值做渲染分支，移除安全。
- **[Risk] 站点元数据改中文影响 SEO/社交卡片** → Mitigation: 与"只保留中文"目标一致，可接受。

## Migration Plan

1. 创建并审阅 OpenSpec change artifacts。
2. 合并 README 为中文，删除 `README.zh-CN.md`，修正 README 内文档链接指向 `/zh/`。
3. 删除 `docs/en/` 目录。
4. 改写 `docs/.vitepress/config.ts`：移除 `en` locale、英文导航/侧边栏，中文化顶层元数据与 `sharedHead`，简化 `lang-redirect`。
5. 改写 `docs/index.md` 为直接重定向 `/zh/`。
6. 清理 `docs/.vitepress/theme/index.ts` 中 `/en/` 分支。
7. 全仓 grep 验证无活跃表面残留 `/en/` 引用。
8. 运行 VitePress 构建验证（若本地 Node 环境可用）或交由 CI `docs-pages.yml` 验证。

回滚通过 Git 还原文件即可。
