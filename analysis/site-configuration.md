---
title: 站点配置
created: 2026-05-21
updated: 2026-05-21
type: config
tags: [config, data]
sources: ["Feishu wiki high-density report"]
---

# 站点配置

本页对应 `data/site.config.json`。本期配置页是静态只读，不做在线编辑后台。

## 配置范围

- 站点标题、副标题、日期、时长、人数。
- 来源链接：飞书 Wiki、妙记、GitHub 仓库。
- 模块开关：项目地图、金句墙、执行仪表盘、Wiki Reader、配置页。
- 成员分组：AI 企服、流量与自媒体、电商与跨境、短视频与投放、方法论与协作。

## 修改方式

1. 修改 `data/site.config.json`。
2. 如涉及成员或金句，修改 `data/members.json` 或 `data/quotes.json`。
3. 运行 `python3 site/build.py`。
4. 提交并推送。
