# 广州创业项目交流会 Wiki

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
