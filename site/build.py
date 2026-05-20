#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "index.html"
PAGE_DIRS = ["guide", "members", "analysis", "quotes", "changelog"]


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    _, meta_text, body = text.split("---", 2)
    meta = {}
    for raw in meta_text.strip().splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            try:
                value = json.loads(value.replace("'", '"'))
            except json.JSONDecodeError:
                value = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        meta[key.strip()] = value
    return meta, body.strip()


def collect_pages():
    pages = []
    files = [ROOT / "index.md"]
    for page_dir in PAGE_DIRS:
        files.extend(sorted((ROOT / page_dir).glob("*.md")))

    for path in files:
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        route = "home-index" if path.name == "index.md" else path.stem
        group = meta.get("type") or (path.parent.name if path.parent != ROOT else "guide")
        title = meta.get("title") or path.stem
        pages.append(
            {
                "route": route,
                "path": str(path.relative_to(ROOT)),
                "title": title,
                "group": group,
                "tags": meta.get("tags", []),
                "body": body,
                "updated": meta.get("updated", ""),
            }
        )
    return pages


def build():
    config = read_json("data/site.config.json")
    members = read_json("data/members.json")
    quotes = read_json("data/quotes.json")
    actions = read_json("data/actions.json")
    pages = collect_pages()

    sectors = Counter(member["sector"] for member in members)
    stage_counts = Counter(member["stage"] for member in members)
    priority_counts = Counter(member["priority"] for member in members)

    groups = [
        {"id": "guide", "label": "导览"},
        {"id": "member", "label": "成员诊断"},
        {"id": "analysis", "label": "可视化分析"},
        {"id": "quotes", "label": "金句传播"},
        {"id": "config", "label": "配置"},
        {"id": "source", "label": "资料来源"},
        {"id": "changelog", "label": "更新记录"},
    ]

    payload = {
        "config": config,
        "pages": pages,
        "members": members,
        "quotes": quotes,
        "actions": actions,
        "groups": groups,
        "sectorCounts": sectors,
        "stageCounts": stage_counts,
        "priorityCounts": priority_counts,
        "builtAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    html = TEMPLATE
    for key, value in {
        "__TITLE__": config["title"],
        "__SUBTITLE__": config["subtitle"],
        "__DATE__": config["date"],
        "__DURATION__": config["duration"],
        "__PEOPLE__": str(config["people"]),
        "__PAYLOAD__": json.dumps(payload, ensure_ascii=False),
    }.items():
        html = html.replace(key, value)

    OUT.write_text(html, encoding="utf-8")
    print(f"built {OUT}")
    print(f"pages={len(pages)} members={len(members)} quotes={len(quotes)} actions={len(actions)}")


TEMPLATE = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>__TITLE__</title>
<meta name="description" content="广州创业项目交流会的独立 Wiki 复盘站，包含成员项目诊断、赛道矩阵、项目地图、执行仪表盘和金句墙。" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=Noto+Sans+SC:wght@400;500;700;800;900&family=Noto+Serif+SC:wght@700;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>
:root{
  --bg:#0f1110;
  --panel:#171a16;
  --panel-2:#1f241e;
  --ink:#f4f0df;
  --muted:#aaa78f;
  --line:rgba(244,240,223,.14);
  --green:#a9d46e;
  --teal:#69c9bd;
  --gold:#f1bd54;
  --red:#ea6a5f;
  --blue:#8bb7ff;
  --shadow:0 24px 80px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;
  min-height:100vh;
  color:var(--ink);
  background:
    radial-gradient(circle at 8% 0%, rgba(169,212,110,.16), transparent 32rem),
    radial-gradient(circle at 92% 10%, rgba(105,201,189,.16), transparent 30rem),
    linear-gradient(180deg,#10120f,#11140f 45%,#0d0f0c);
  font-family:"Noto Sans SC",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  letter-spacing:0;
}
a{color:inherit}
button,input,select{font:inherit}
.app{display:grid;grid-template-columns:320px minmax(0,1fr);min-height:100vh}
.sidebar{
  position:sticky;
  top:0;
  height:100vh;
  overflow:auto;
  padding:22px 18px;
  border-right:1px solid var(--line);
  background:rgba(13,16,12,.92);
  backdrop-filter:blur(24px);
  z-index:20;
}
.brand{display:grid;gap:10px;margin-bottom:18px}
.brand-mark{
  width:42px;height:42px;border-radius:8px;
  background:linear-gradient(135deg,var(--green),var(--teal));
  display:grid;place-items:center;color:#10120f;font-weight:900;
  box-shadow:0 0 0 1px rgba(255,255,255,.14),0 18px 40px rgba(105,201,189,.18);
}
.brand h1{margin:0;font-size:20px;line-height:1.2;font-weight:900}
.brand p{margin:0;color:var(--muted);font-size:13px;line-height:1.7}
.search{
  width:100%;height:44px;border-radius:8px;border:1px solid var(--line);
  background:#0e100d;color:var(--ink);padding:0 12px;outline:none;
}
.search:focus{border-color:rgba(169,212,110,.75);box-shadow:0 0 0 3px rgba(169,212,110,.13)}
.quick{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0 18px}
.quick a,.nav a{
  text-decoration:none;
  color:var(--muted);
  border:1px solid transparent;
}
.quick a{
  padding:10px 12px;border-radius:8px;background:rgba(255,255,255,.035);
  font-size:13px;color:var(--ink);
}
.quick a:hover,.nav a:hover{border-color:var(--line);color:var(--ink);background:rgba(255,255,255,.04)}
.group{margin:18px 0}
.group-title{
  color:var(--gold);
  font:700 12px/1 "IBM Plex Mono",monospace;
  text-transform:uppercase;
  letter-spacing:0;
  margin:0 0 8px;
}
.nav{display:grid;gap:3px}
.nav a{
  display:block;padding:8px 10px;border-radius:7px;font-size:14px;line-height:1.35;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.nav a.active{color:#11140f;background:var(--green);border-color:transparent;font-weight:800}
.nav .path{display:block;color:rgba(244,240,223,.45);font-size:11px;margin-top:2px}
.content{min-width:0}
.topbar{
  position:sticky;top:0;z-index:10;height:60px;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 28px;border-bottom:1px solid var(--line);
  background:rgba(16,18,15,.74);backdrop-filter:blur(18px);
}
.crumb{color:var(--muted);font-size:13px}
.built{color:rgba(244,240,223,.52);font:600 12px/1 "IBM Plex Mono",monospace}
.main{max-width:1200px;margin:0 auto;padding:34px 28px 80px}
.hero{
  min-height:calc(100vh - 110px);
  display:grid;align-content:center;gap:28px;
  padding:24px 0 44px;
}
.eyebrow{
  display:inline-flex;align-items:center;gap:8px;color:#10120f;background:var(--gold);
  width:max-content;border-radius:999px;padding:8px 12px;font-weight:900;font-size:12px;
}
.hero h2{
  margin:0;
  font-family:"Noto Serif SC",serif;
  font-size:clamp(42px,7vw,92px);
  line-height:1.02;
  letter-spacing:0;
  max-width:1040px;
}
.hero-lead{max-width:820px;color:#d6d0b4;font-size:19px;line-height:1.9;margin:0}
.metric-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.metric{
  min-height:126px;border:1px solid var(--line);border-radius:8px;padding:18px;
  background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.025));
  box-shadow:var(--shadow);
}
.metric strong{display:block;font:800 34px/1 "IBM Plex Mono",monospace;color:var(--green);margin-bottom:10px}
.metric span{color:var(--muted);font-size:14px;line-height:1.5}
.section{margin:44px 0}
.section h3,.article h1{
  font-family:"Noto Serif SC",serif;
  font-size:34px;
  margin:0 0 18px;
  letter-spacing:0;
}
.section-intro{color:var(--muted);line-height:1.8;max-width:820px}
.insight-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.insight{
  border:1px solid var(--line);border-radius:8px;padding:18px;background:rgba(255,255,255,.04);
}
.insight h4{margin:0 0 8px;font-size:18px}
.insight p{margin:0;color:#d2ccb0;line-height:1.75}
.visual-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:16px}
.panel{
  border:1px solid var(--line);border-radius:8px;background:rgba(23,26,22,.86);
  padding:18px;box-shadow:var(--shadow);
}
.panel h4{margin:0 0 14px;font-size:18px}
.bars{display:grid;gap:10px}
.bar-row{display:grid;grid-template-columns:130px minmax(0,1fr) 34px;gap:10px;align-items:center}
.bar-label{color:#ded8bd;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bar-track{height:12px;border-radius:999px;background:rgba(255,255,255,.08);overflow:hidden}
.bar-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,var(--green),var(--teal))}
.bar-num{text-align:right;color:var(--gold);font:700 13px/1 "IBM Plex Mono",monospace}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{
  border:1px solid var(--line);border-radius:999px;padding:8px 11px;
  background:rgba(255,255,255,.035);color:#ddd5b9;font-size:13px;
}
.member-tools{
  display:grid;grid-template-columns:minmax(0,1fr) 180px 180px;gap:10px;margin-bottom:16px;
}
.member-tools input,.member-tools select{
  height:42px;border-radius:8px;border:1px solid var(--line);background:#10130f;color:var(--ink);padding:0 12px;
}
.member-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.member-card{
  display:grid;gap:10px;text-decoration:none;border:1px solid var(--line);border-radius:8px;
  padding:16px;background:rgba(255,255,255,.04);min-height:230px;
}
.member-card:hover{border-color:rgba(169,212,110,.7);background:rgba(169,212,110,.07)}
.member-card h4{margin:0;font-size:18px}
.meta{display:flex;flex-wrap:wrap;gap:6px}
.pill{border-radius:999px;padding:5px 8px;background:rgba(105,201,189,.12);color:#aee9df;font-size:12px}
.member-card p{margin:0;color:#d4ceb3;line-height:1.65;font-size:14px}
.action-board{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.action-card{
  border:1px solid var(--line);border-radius:8px;background:rgba(255,255,255,.04);
  padding:16px;min-height:180px;
}
.action-card time{font:800 13px/1 "IBM Plex Mono",monospace;color:var(--gold)}
.action-card h4{margin:10px 0 8px;font-size:17px}
.action-card p{margin:0;color:#d4ceb3;line-height:1.65}
.quote-wall{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.quote-card{
  min-height:260px;border-radius:8px;border:1px solid rgba(241,189,84,.34);
  background:
    linear-gradient(145deg,rgba(241,189,84,.18),rgba(105,201,189,.08)),
    rgba(255,255,255,.04);
  padding:22px;display:grid;align-content:space-between;gap:18px;
}
.quote-card blockquote{margin:0;font-family:"Noto Serif SC",serif;font-size:27px;line-height:1.28;font-weight:900}
.quote-card .tag{color:var(--gold);font-weight:800;font-size:13px}
.article{
  max-width:880px;
  border:1px solid var(--line);
  border-radius:8px;
  background:rgba(23,26,22,.78);
  padding:34px;
  box-shadow:var(--shadow);
}
.article h1{font-size:38px}
.article h2{font-size:25px;margin:34px 0 12px;border-top:1px solid var(--line);padding-top:22px}
.article h3{font-size:20px;margin:26px 0 10px}
.article p,.article li{color:#d8d1b8;line-height:1.86;font-size:16px}
.article blockquote{margin:18px 0;padding:14px 18px;border-left:4px solid var(--green);background:rgba(169,212,110,.08);color:#eee8ce}
.article table{width:100%;border-collapse:collapse;margin:18px 0;font-size:14px}
.article th,.article td{border:1px solid var(--line);padding:10px;vertical-align:top}
.article th{background:rgba(255,255,255,.06);color:var(--gold);text-align:left}
.article code{font-family:"IBM Plex Mono",monospace;background:rgba(255,255,255,.08);padding:2px 5px;border-radius:4px}
.article pre{overflow:auto;background:#0b0d0b;border:1px solid var(--line);border-radius:8px;padding:16px}
.article a{color:#bde987;text-decoration:none;border-bottom:1px solid rgba(189,233,135,.35)}
.article img{max-width:100%;height:auto;border-radius:8px}
.config-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.config-card{border:1px solid var(--line);border-radius:8px;background:rgba(255,255,255,.04);padding:16px}
.config-card h4{margin:0 0 10px;color:var(--gold)}
.config-card pre{white-space:pre-wrap;word-break:break-word;color:#d8d1b8}
.empty{padding:24px;color:var(--muted);border:1px dashed var(--line);border-radius:8px}
.mobile-menu{
  display:none;position:fixed;left:14px;top:12px;z-index:40;width:42px;height:42px;border-radius:8px;
  border:1px solid var(--line);background:rgba(16,18,15,.9);color:var(--ink);
}
.scrim{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:15}
@media (max-width:980px){
  .app{grid-template-columns:1fr}
  .sidebar{position:fixed;left:0;top:0;bottom:0;transform:translateX(-104%);transition:.2s ease;width:min(86vw,340px)}
  .sidebar.open{transform:translateX(0)}
  .scrim.open,.mobile-menu{display:block}
  .topbar{padding-left:70px}
  .metric-grid,.insight-grid,.visual-grid,.member-grid,.action-board,.quote-wall,.config-grid{grid-template-columns:1fr}
  .member-tools{grid-template-columns:1fr}
  .main{padding:24px 16px 60px}
  .article{padding:22px}
  .hero h2{font-size:44px}
}
</style>
</head>
<body>
<button class="mobile-menu" id="mobileMenu" aria-label="打开目录">☰</button>
<div class="scrim" id="scrim"></div>
<div class="app">
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <div class="brand-mark">GZ</div>
      <h1>__TITLE__</h1>
      <p>__DATE__ · __DURATION__ · __PEOPLE__ 人左右<br>创业者交流答疑 / 高信息密度 Wiki</p>
    </div>
    <input class="search" id="search" placeholder="搜索成员、赛道、卡点、金句..." />
    <div class="quick">
      <a href="#home">洞察总览</a>
      <a href="#project-map">项目地图</a>
      <a href="#golden-quotes">金句墙</a>
      <a href="#action-dashboard">执行仪表盘</a>
    </div>
    <nav id="nav"></nav>
  </aside>
  <main class="content">
    <div class="topbar">
      <div class="crumb" id="crumb">会议洞察总览</div>
      <div class="built">built __DATE__</div>
    </div>
    <div class="main" id="app"></div>
  </main>
</div>
<script>
const DATA = __PAYLOAD__;
const {config, pages, members, quotes, actions, groups, sectorCounts, stageCounts, priorityCounts} = DATA;
const byRoute = Object.fromEntries(pages.map(page => [page.route, page]));
const nav = document.getElementById('nav');
const app = document.getElementById('app');
const crumb = document.getElementById('crumb');
const search = document.getElementById('search');
const sidebar = document.getElementById('sidebar');
const scrim = document.getElementById('scrim');
const mobileMenu = document.getElementById('mobileMenu');

mermaid.initialize({startOnLoad:false, theme:'dark', securityLevel:'loose'});
marked.use({
  renderer: {
    link(href, title, text) {
      const clean = String(href || '');
      const label = text || clean;
      if (clean.startsWith('#')) return `<a href="${clean}">${label}</a>`;
      return `<a href="${clean}" target="_blank" rel="noreferrer">${label}</a>`;
    }
  }
});

function routeTitle(route){
  return byRoute[route]?.title || route;
}

function pageLink(route, label){
  return `<a href="#${route}">${label || routeTitle(route)}</a>`;
}

function normalizeWikiLinks(md){
  return md.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (_, route, label) => `[${label}](#${route.trim()})`)
           .replace(/\[\[([^\]]+)\]\]/g, (_, route) => `[${routeTitle(route.trim())}](#${route.trim()})`);
}

function markdown(md){
  const normalized = normalizeWikiLinks(md || '').replace(/([：:，,。；;）)])\*\*(?=\S)/g, '$1** ');
  return marked.parse(normalized);
}

function pageGroup(page){
  if (['guide','member','analysis','quotes','config','source','changelog'].includes(page.group)) return page.group;
  if (page.group === 'member') return 'member';
  if (page.group === 'analysis') return 'analysis';
  if (page.group === 'quote') return 'quotes';
  if (page.group === 'changelog') return 'changelog';
  return 'guide';
}

function renderNav(filter=''){
  const q = filter.trim().toLowerCase();
  const visible = pages.filter(page => {
    if (page.route === 'home-index') return true;
    const hay = `${page.title} ${page.path} ${(page.tags||[]).join(' ')} ${page.body}`.toLowerCase();
    return !q || hay.includes(q);
  });
  nav.innerHTML = groups.map(group => {
    const items = visible.filter(page => pageGroup(page) === group.id);
    if (!items.length) return '';
    return `<section class="group"><h2 class="group-title">${group.label}</h2><div class="nav">${items.map(page =>
      `<a href="#${page.route}" data-route="${page.route}"><span>${page.title}</span><span class="path">${page.path}</span></a>`
    ).join('')}</div></section>`;
  }).join('');
  markActive();
}

function markActive(){
  const route = location.hash.replace(/^#/, '') || 'home';
  document.querySelectorAll('.nav a').forEach(a => a.classList.toggle('active', a.dataset.route === route));
}

function barChart(counter){
  const entries = Object.entries(counter).sort((a,b)=>b[1]-a[1]);
  const max = Math.max(...entries.map(([,v])=>v), 1);
  return `<div class="bars">${entries.map(([label,value])=>`
    <div class="bar-row"><div class="bar-label" title="${label}">${label}</div><div class="bar-track"><div class="bar-fill" style="width:${Math.max(8, value/max*100)}%"></div></div><div class="bar-num">${value}</div></div>
  `).join('')}</div>`;
}

function homeMembersPreview(){
  const top = members.filter(m => ['高','方法论'].includes(m.priority)).slice(0, 9);
  return `<div class="member-grid">${top.map(memberCard).join('')}</div>`;
}

function memberCard(m){
  return `<a class="member-card" href="#${m.slug}">
    <div>
      <h4>${m.name}</h4>
      <div class="meta"><span class="pill">${m.sector}</span><span class="pill">${m.stage}</span><span class="pill">${m.priority}</span></div>
    </div>
    <p><strong>卡点：</strong>${m.bottleneck}</p>
    <p><strong>下一步：</strong>${m.action}</p>
  </a>`;
}

function renderHome(){
  crumb.textContent = '会议洞察总览';
  app.innerHTML = `
    <section class="hero">
      <div class="eyebrow">Founder Roundtable Wiki</div>
      <h2>一场 4 小时 40 分钟的创业项目体检。</h2>
      <p class="hero-lead">${config.subtitle} 这个站点把会议整理成可查阅、可筛选、可复盘、可截图传播的 Wiki：每个人的项目、卡点、建议、下一步都被放进同一张地图里。</p>
      <div class="metric-grid">
        <div class="metric"><strong>${config.duration}</strong><span>录音时长，从开场规则到资源合作答疑</span></div>
        <div class="metric"><strong>${members.length}</strong><span>成员与公共答疑页面，覆盖项目发言人、主持人与社群角色</span></div>
        <div class="metric"><strong>${Object.keys(sectorCounts).length}</strong><span>赛道标签，包含 AI 企服、跨境、自媒体、电商、短视频等</span></div>
        <div class="metric"><strong>${actions.length}</strong><span>保留时间点的会议待办，可直接进入执行看板</span></div>
      </div>
    </section>
    <section class="section">
      <h3>先看四个结论</h3>
      <div class="insight-grid">
        <article class="insight"><h4>先问谁付钱</h4><p>30 秒讲不清楚项目，往往不是表达问题，而是还没想清楚客户、需求、成交和交付。</p></article>
        <article class="insight"><h4>流量不是 IP 的敌人</h4><p>很多项目先做流量更实际。把真实需求讲透，把流量做起来，IP 会自然长出来。</p></article>
        <article class="insight"><h4>AI 企服要有可视化证据</h4><p>课程、案例库、PPT、演示包和行业样板，都是让老板相信你能交付的证据。</p></article>
        <article class="insight"><h4>短期现金流和长期事业分开看</h4><p>存款不足的人先做快钱和代做，拿正反馈；能扛半年的人才适合长期产品型探索。</p></article>
      </div>
    </section>
    <section class="section visual-grid">
      <div class="panel"><h4>赛道分布</h4>${barChart(sectorCounts)}</div>
      <div class="panel"><h4>阶段分布</h4>${barChart(stageCounts)}</div>
    </section>
    <section class="section">
      <h3>重点项目入口</h3>
      <p class="section-intro">下面这些页面适合作为第一轮阅读入口。想查全员，请进入 ${pageLink('project-map','项目地图')}。</p>
      ${homeMembersPreview()}
    </section>
    <section class="section">
      <h3>传播页</h3>
      <div class="quote-wall">${quotes.slice(0,3).map(quoteCard).join('')}</div>
    </section>
  `;
}

function quoteCard(q){
  const text = q.text || q.quote || '';
  const tag = q.tag || q.theme || '金句';
  const context = q.context || q.note || '';
  return `<article class="quote-card"><blockquote>${text}</blockquote><div><div class="tag">${tag}</div><p>${context}</p></div></article>`;
}

function renderProjectMap(){
  return `<section class="section">
    <h3>项目地图</h3>
    <p class="section-intro">按成员、赛道、阶段、卡点、行动项筛选。它比纯会议纪要更适合复盘：你能迅速看到谁适合合作，谁需要流量，谁需要产品化，谁要先修现金流。</p>
    <div class="member-tools">
      <input id="memberFilter" placeholder="筛选成员、卡点、行动..." />
      <select id="sectorFilter"><option value="">全部赛道</option>${Object.keys(sectorCounts).map(s=>`<option>${s}</option>`).join('')}</select>
      <select id="stageFilter"><option value="">全部阶段</option>${Object.keys(stageCounts).map(s=>`<option>${s}</option>`).join('')}</select>
    </div>
    <div class="member-grid" id="memberGrid">${members.map(memberCard).join('')}</div>
  </section>
  <section class="section visual-grid">
    <div class="panel"><h4>赛道密度</h4>${barChart(sectorCounts)}</div>
    <div class="panel"><h4>优先级分布</h4>${barChart(priorityCounts)}</div>
  </section>`;
}

function wireProjectMap(){
  const q = document.getElementById('memberFilter');
  const sector = document.getElementById('sectorFilter');
  const stage = document.getElementById('stageFilter');
  const grid = document.getElementById('memberGrid');
  if (!q || !sector || !stage || !grid) return;
  const refresh = () => {
    const keyword = q.value.trim().toLowerCase();
    const items = members.filter(m => {
      const hay = `${m.name} ${m.title} ${m.sector} ${m.stage} ${m.bottleneck} ${m.action}`.toLowerCase();
      return (!keyword || hay.includes(keyword)) && (!sector.value || m.sector === sector.value) && (!stage.value || m.stage === stage.value);
    });
    grid.innerHTML = items.length ? items.map(memberCard).join('') : '<div class="empty">没有匹配的成员。换一个关键词试试。</div>';
  };
  [q, sector, stage].forEach(el => el.addEventListener('input', refresh));
}

function renderActionDashboard(){
  return `<section class="section">
    <h3>执行仪表盘</h3>
    <p class="section-intro">这里保留原会议待办的时间点和对象，再补一层“7 天内应该怎么动”的执行视角。</p>
    <div class="action-board">${actions.map(action => `
      <article class="action-card">
        <time>${action.time}</time>
        <h4>${action.title || action.owner}</h4>
        <p><strong>${action.owner}</strong><br>${action.detail || action.action || ''}</p>
      </article>
    `).join('')}</div>
  </section>
  <section class="section">
    <h3>7 天行动建议</h3>
    <div class="member-grid">${members.filter(m => !['主持人','资源合作答疑'].includes(m.name)).slice(0,24).map(memberCard).join('')}</div>
  </section>`;
}

function renderQuoteWall(){
  return `<section class="section">
    <h3>金句海报墙</h3>
    <p class="section-intro">这些卡片按传播场景排版，大字号、短语义、适合截图分享。每张卡片背后都对应一类创业判断。</p>
    <div class="quote-wall">${quotes.map(quoteCard).join('')}</div>
  </section>`;
}

function renderConfig(){
  return `<section class="section">
    <h3>配置页</h3>
    <p class="section-intro">本期是静态只读配置页。真实修改通过 <code>data/site.config.json</code>、<code>data/members.json</code>、<code>data/actions.json</code> 和 <code>data/quotes.json</code> 完成。</p>
    <div class="config-grid">
      <article class="config-card"><h4>站点配置</h4><pre>${escapeHtml(JSON.stringify(config, null, 2))}</pre></article>
      <article class="config-card"><h4>模块开关</h4><pre>${escapeHtml(JSON.stringify(config.modules || {}, null, 2))}</pre></article>
      <article class="config-card"><h4>成员分组</h4><pre>${escapeHtml(JSON.stringify(sectorCounts, null, 2))}</pre></article>
      <article class="config-card"><h4>数据规模</h4><pre>${escapeHtml(JSON.stringify({pages:pages.length,members:members.length,quotes:quotes.length,actions:actions.length,builtAt:DATA.builtAt}, null, 2))}</pre></article>
    </div>
  </section>`;
}

function escapeHtml(str){
  return String(str).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[ch]));
}

async function renderPage(route){
  const page = byRoute[route];
  if (!page) {
    if (route === 'home') return renderHome();
    app.innerHTML = '<div class="empty">页面不存在。</div>';
    crumb.textContent = 'Not found';
    return;
  }
  crumb.textContent = page.title;
  let extra = '';
  if (route === 'project-map') extra = renderProjectMap();
  if (route === 'action-dashboard') extra = renderActionDashboard();
  if (route === 'golden-quotes') extra = renderQuoteWall();
  if (route === 'site-configuration') extra = renderConfig();
  app.innerHTML = `<article class="article">${markdown(page.body)}</article>${extra}`;
  wireProjectMap();
  await renderMermaid();
}

async function renderMermaid(){
  const blocks = [...document.querySelectorAll('code.language-mermaid')];
  for (let i = 0; i < blocks.length; i++) {
    const code = blocks[i];
    const source = code.textContent;
    const holder = document.createElement('div');
    holder.className = 'mermaid';
    holder.textContent = source;
    code.closest('pre').replaceWith(holder);
  }
  if (document.querySelector('.mermaid')) {
    await mermaid.run({querySelector:'.mermaid'});
  }
}

function navigate(){
  closeMenu();
  const route = location.hash.replace(/^#/, '') || 'home';
  markActive();
  if (route === 'home') renderHome();
  else renderPage(route);
}

function openMenu(){
  sidebar.classList.add('open');
  scrim.classList.add('open');
}

function closeMenu(){
  sidebar.classList.remove('open');
  scrim.classList.remove('open');
}

search.addEventListener('input', () => renderNav(search.value));
mobileMenu.addEventListener('click', openMenu);
scrim.addEventListener('click', closeMenu);
window.addEventListener('hashchange', navigate);
renderNav();
navigate();
</script>
</body>
</html>
'''


if __name__ == "__main__":
    build()
