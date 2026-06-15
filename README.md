# 广州创业项目交流会 Wiki

<!-- SIUSER-REPO-GUIDE:START -->
## Repository Guide

### What This Repository Does

广州创业者圆桌：围绕 AI startup / founder roundtable / startup ecosystem 的项目。

English summary: guangzhou-founder-roundtable-2026 for guangzhou-founder-roundtable-2026 for AI startup, founder roundtable, startup ecosystem.

### Online Entry Points

- GitHub repository: https://github.com/siuserxiaowei/guangzhou-founder-roundtable-2026
- Live / GitHub Pages: https://siuserxiaowei.github.io/guangzhou-founder-roundtable-2026/
- Default branch: `main`
- Primary language: `HTML`

### How To Read / Learn This Repository

1. 先读本 README，确认项目目标、在线入口和本地运行方式。
2. 打开上方 Live / GitHub Pages 链接，先从最终效果理解项目。
3. 按仓库目录从入口文件、数据文件、脚本和文档依次阅读。
4. 如果要修改内容，先小范围改动，再运行本 README 中的验证命令。

### Clone This Repository

```bash
git clone https://github.com/siuserxiaowei/guangzhou-founder-roundtable-2026.git
cd guangzhou-founder-roundtable-2026
```

### Run Or View Locally

```bash
python3 -m http.server 8000
```

然后打开 `http://127.0.0.1:8000/`。

### Repository Map

| Path | Purpose |
| --- | --- |
| `README.md` | 项目入口说明，先读这里。 |
| `index.html` | 静态站首页或页面入口。 |
| `data/` | 数据、索引或结构化内容。 |
| `SCHEMA.md` | 项目文件。 |
| `analysis/` | 项目目录。 |
| `changelog/` | 项目目录。 |
| `guide/` | 项目目录。 |
| `index.md` | 项目文件。 |
| `members/` | 项目目录。 |
| `quotes/` | 项目目录。 |
| `site/` | 项目目录。 |

### Maintenance Notes

- Keep this README in sync when the project purpose, live link, or run commands change.
- Prefer small, focused commits when changing code, data, or generated pages.
- Run the relevant build or validation command before publishing changes.
- If this is a generated/static archive, update the source data first, then regenerate the public files.

### Privacy And Safety

- Do not commit API keys, tokens, passwords, cookies, private URLs, or internal account data.
- Keep private source material out of public GitHub Pages output unless it has been explicitly cleared for publication.
- When in doubt, run a quick secret scan such as `rg -n "token|secret|password|access_key|authorization"` before pushing.
<!-- SIUSER-REPO-GUIDE:END -->

<!-- SIUSER-SEO-INTRO:START -->

## 项目介绍 / Project Introduction

**中文介绍**：广州创业者圆桌会议资料与机会梳理，记录 AI 创业、增长、产品和本地创业生态的讨论。

**English**: Meeting materials and opportunity mapping for a Guangzhou founder roundtable, covering AI startups, growth, products, and the local builder ecosystem.

**SEO 关键词 / SEO Keywords**: Guangzhou startup, founder roundtable, AI startup, 创业者圆桌, startup ecosystem

<!-- SIUSER-SEO-INTRO:END -->

> 2026-05-20 广州创业社群线下沙龙的高信息密度复盘站。  
> 在线站点：<https://siuserxiaowei.github.io/guangzhou-founder-roundtable-2026/>

本仓库把一场约 4 小时 40 分钟、约 20 位创业者参与的项目诊断会，整理成可检索、可复盘、可传播的 Wiki：成员项目页、赛道分析页、项目地图、金句墙、执行仪表盘和资料来源说明。

## 快速入口

- `index.md`：Wiki 总索引。
- `guide/how-to-read.md`：如何阅读这份复盘。
- `analysis/project-map.md`：项目地图与赛道结构。
- `analysis/action-dashboard.md`：待办与 7 天行动建议。
- `quotes/golden-quotes.md`：金句墙。
- `data/site.config.json`：站点配置与模块开关。

## 本地构建

```bash
python3 site/build.py
python3 -m http.server 8123
```

打开 <http://127.0.0.1:8123/> 预览。

<!-- SIUSER-CONTACT:START -->

## 联系我 / Contact

想交流 AI 工具、内容自动化、SEO、私域增长或项目合作，可以扫码加我微信。

For collaboration on AI tools, content automation, SEO, private-domain growth, or product experiments, scan the WeChat QR code below.

<img src="https://raw.githubusercontent.com/siuserxiaowei/siuserxiaowei/main/assets/contact/wechat-qrcode.jpg" width="180" alt="WeChat QR code / 微信二维码" />

**关键词 / Keywords**: Guangzhou startup, founder roundtable, AI startup, 创业者圆桌, AI tools, AI automation, GitHub Pages, SEO

<!-- SIUSER-CONTACT:END -->
