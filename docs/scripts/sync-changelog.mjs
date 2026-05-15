#!/usr/bin/env node
/**
 * Sync CHANGELOG.md to docs/en/reference/changelog.md and docs/zh/reference/changelog.md
 *
 * This script copies the content from changelog/CHANGELOG.md to the docs site,
 * with formatting changes for both English and Chinese versions.
 *
 * Run from the docs directory: node scripts/sync-changelog.mjs
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const docsDir = join(__dirname, "..");
const rootDir = join(docsDir, "..");

const sourcePath = join(rootDir, "changelog", "CHANGELOG.md");
const targetPathEn = join(docsDir, "en", "reference", "changelog.md");
const targetPathZh = join(docsDir, "zh", "reference", "changelog.md");

const HEADER_EN = `# Changelog

This page documents the changes in each YOLO-Toys release.

`;

const HEADER_ZH = `# 更新日志

此页面记录 YOLO-Toys 各版本的变更。

`;

// Check if source file exists
if (!existsSync(sourcePath)) {
  console.error(`Source changelog not found: ${sourcePath}`);
  process.exit(1);
}

// Read the source file
let content = readFileSync(sourcePath, "utf-8");

// Remove the HTML comment block at the top
content = content.replace(/<!--[\s\S]*?-->\n*/g, "");

// Remove the "# Changelog" title (we'll add our own header)
content = content.replace(/^# Changelog\n+/, "");

// Convert title format: ## [0.1.0] - 2024-01-15 -> ## 0.1.0 (2024-01-15)
content = content.replace(
  /^## \[([^\]]+)\] - (\d{4}-\d{1,2}-\d{1,2})/gm,
  "## $1 ($2)"
);

// Remove subsection headers like ### Added, ### Changed, ### Fixed
content = content.replace(/^### (Added|Changed|Fixed|Improved)\n+/gm, "");

// Ensure target directories exist
const targetDirEn = dirname(targetPathEn);
const targetDirZh = dirname(targetPathZh);

if (!existsSync(targetDirEn)) {
  mkdirSync(targetDirEn, { recursive: true });
}
if (!existsSync(targetDirZh)) {
  mkdirSync(targetDirZh, { recursive: true });
}

// Write the target files
writeFileSync(targetPathEn, HEADER_EN + content.trim() + "\n");
writeFileSync(targetPathZh, HEADER_ZH + content.trim() + "\n");

console.log("✅ Changelog synced successfully");
console.log(`   EN: ${targetPathEn}`);
console.log(`   ZH: ${targetPathZh}`);
