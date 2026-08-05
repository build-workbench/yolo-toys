## Why

YOLO-Toys 当前同时维护中英两套公共表面：仓库 `README.md`（英）+ `README.zh-CN.md`（中），以及 GitHub Pages（VitePress）下 `docs/en/` 与 `docs/zh/` 两套各 60 个文件的文档树。项目已进入 finalization mode，目标受众明确为中文用户，双语文档树显著抬高维护成本、产生翻译漂移，并让导航/语言切换逻辑长期背负复杂度。

收尾阶段应优先"减少漂移、降低维护面"，而非继续维护对等翻译。将公共表面收敛为单一中文入口，可消除重复内容、简化 Pages 配置与语言切换脚本，并让 README 与站点元数据一致地面向同一受众。

## What Changes

- 将 `README.zh-CN.md` 内容合并进 `README.md`，使 `README.md` 成为唯一中文仓库入口；删除 `README.zh-CN.md`；移除 README 中的语言切换链接。
- 删除 `docs/en/` 整个英文文档目录（60 个文件）。
- 在 `docs/.vitepress/config.ts` 中移除 `en` locale、英文导航与英文侧边栏，将顶层 `title`/`description` 与 `head` 元数据改为中文，简化 `lang-redirect` 脚本为直接重定向到 `/zh/`。
- 将 `docs/index.md` 的语言探测逻辑改为直接跳转 `/zh/`。
- 清理 `docs/.vitepress/theme/index.ts` 中针对 `/en/` 的语言偏好追踪分支。
- 更新 `README.md` 中指向 `/en/` 的文档链接为 `/zh/`。
- 历史发布记录 `changelog/` 保持原貌，不回改（changelog 仅作发布历史）。

## Capabilities

### Modified Capabilities
- `project-packaging`: 收紧公共表面语言策略——README 与 GitHub Pages 收敛为单一中文入口，站点元数据与导航以中文为准，并明确不再维护对等英文翻译。

## Impact

- 受影响文件：`README.md`、`README.zh-CN.md`（删除）、`docs/index.md`、`docs/.vitepress/config.ts`、`docs/.vitepress/theme/index.ts`、`docs/en/`（整目录删除）。
- 公共 GitHub 仓库元数据（description/topics）若提及 bilingual 应同步为中文定位；本变更不强制改动 `gh` 元数据，除非现有描述显式声明双语。
- 不涉及运行时（`app/`）代码改动，不涉及测试套件逻辑改动。
- `changelog/`、`docs/superpowers/plans/` 等历史/规划文档保持原貌，不作为活跃表面回改。
