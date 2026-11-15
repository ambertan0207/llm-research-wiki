#!/usr/bin/env python3
"""Build a dependency-free, static browser site from the LLM research Wiki."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import quote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
PAGES_OUT = ROOT / "wiki-pages"
ASSETS_OUT = ROOT / "wiki-assets"
ENTRY = ROOT / "index.html"

TYPE_LABELS = {
    "topic": "研究主題",
    "concept": "核心概念",
    "source": "研究來源",
    "synthesis": "綜述與比較",
    "question": "待研究問題",
}
TYPE_ICONS = {
    "topic": "🪴",
    "concept": "🧩",
    "source": "📚",
    "synthesis": "🧵",
    "question": "🔎",
}


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    fields: dict[str, str] = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            block = text[3:end]
            for line in block.splitlines():
                match = re.match(r"^([\w-]+):\s*(.*)$", line)
                if match:
                    fields[match.group(1)] = match.group(2).strip().strip('"')
            text = text[end + 4 :].lstrip()
    return fields, text


def scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def build_page_map() -> tuple[list[dict], dict[str, dict]]:
    paths = sorted(WIKI.rglob("*.md"), key=lambda path: path.as_posix().casefold())
    entries: list[dict] = []
    lookup: dict[str, dict] = {}
    for number, path in enumerate(paths, start=1):
        relative = path.relative_to(ROOT).as_posix()
        fields, body = frontmatter(path.read_text(encoding="utf-8-sig"))
        title = scalar(fields.get("title", ""))
        if not title:
            title_match = re.search(r"^#\s+(.+)$", body, re.M)
            title = title_match.group(1).strip() if title_match else path.stem
        kind = scalar(fields.get("type", path.parent.name.rstrip("s"))).lower()
        if kind not in TYPE_LABELS:
            kind = {
                "sources": "source",
                "concepts": "concept",
                "topics": "topic",
                "syntheses": "synthesis",
                "questions": "question",
            }.get(path.parent.name, "concept")
        page_id = f"page-{number:03d}"
        entry = {
            "id": page_id,
            "title": title,
            "type": kind,
            "typeLabel": TYPE_LABELS[kind],
            "icon": TYPE_ICONS[kind],
            "source": relative,
            "href": f"wiki-pages/{page_id}.html",
            "body": body,
            "tags": scalar(fields.get("tags", "[]")).strip("[]"),
        }
        entries.append(entry)
        for key in (path.stem, title, relative, path.relative_to(WIKI).as_posix()):
            lookup[key.casefold()] = entry
    return entries, lookup


def index_summaries() -> dict[str, tuple[str, str]]:
    text = (ROOT / "index.md").read_text(encoding="utf-8-sig")
    result: dict[str, tuple[str, str]] = {}
    current_type = ""
    sections = {
        "研究主題": "topic",
        "概念": "concept",
        "來源": "source",
        "綜述與比較": "synthesis",
        "待研究問題": "question",
    }
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+)$", line)
        if heading:
            current_type = sections.get(heading.group(1).strip(), current_type)
        match = re.match(r"^\s*-\s+\[([^]]+)\]\(([^)]+)\)\s*[—–-]\s*(.+)$", line)
        if match:
            title, target, summary = match.groups()
            result[target.strip().casefold()] = (current_type, summary.strip())
    return result


def safe_attr(value: str) -> str:
    return html.escape(value, quote=True)


def resolve_markdown_link(target: str, source_file: Path, page_lookup: dict[str, dict], page_id: str) -> str:
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or target.startswith("mailto:"):
        return target
    if not parts.path:
        return f"#{quote(parts.fragment)}" if parts.fragment else "#"
    candidate = (source_file.parent / parts.path).resolve()
    if candidate.suffix.lower() == ".md":
        rel = candidate.relative_to(ROOT).as_posix() if candidate.is_relative_to(ROOT) else ""
        entry = page_lookup.get(rel.casefold()) or page_lookup.get(candidate.stem.casefold())
        if entry:
            return f"../{entry['href']}" + (f"#{quote(parts.fragment)}" if parts.fragment else "")
    if candidate.is_relative_to(ROOT):
        local = Path("..") / Path(*candidate.relative_to(ROOT).parts)
        href = local.as_posix()
        return href + (f"#{quote(parts.fragment)}" if parts.fragment else "")
    return target


def inline(text: str, source_file: Path, page_lookup: dict[str, dict], page_id: str) -> str:
    value = html.escape(text, quote=False)
    code_tokens: list[str] = []

    def keep_code(match: re.Match) -> str:
        code_tokens.append(f"<code>{match.group(1)}</code>")
        return f"\x00CODE{len(code_tokens)-1}\x00"

    value = re.sub(r"`([^`]+)`", keep_code, value)

    def wiki_link(match: re.Match) -> str:
        target = html.unescape(match.group(1).strip())
        if "|" in target:
            key, label = (part.strip() for part in target.split("|", 1))
        else:
            key, label = target, target
        entry = page_lookup.get(key.casefold())
        if not entry:
            entry = page_lookup.get(Path(key).stem.casefold())
        if entry:
            return f'<a href="../{entry["href"]}">{html.escape(label)}</a>'
        return html.escape(label)

    value = re.sub(r"\[\[([^\]]+)\]\]", wiki_link, value)

    def md_link(match: re.Match) -> str:
        label, target = match.group(1), html.unescape(match.group(2).strip())
        href = resolve_markdown_link(target, source_file, page_lookup, page_id)
        return f'<a href="{safe_attr(href)}">{label}</a>'

    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", md_link, value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    value = re.sub(r"~~(.+?)~~", r"<del>\1</del>", value)
    for index, token in enumerate(code_tokens):
        value = value.replace(f"\x00CODE{index}\x00", token)
    return value


def render_markdown(body: str, source_file: Path, page_lookup: dict[str, dict], page_id: str) -> str:
    lines = body.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    list_kind = ""
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append("<p>" + inline(" ".join(x.strip() for x in paragraph), source_file, page_lookup, page_id) + "</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal list_kind
        if list_kind:
            output.append(f"</{list_kind}>")
            list_kind = ""

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            flush_paragraph()
            close_list()
            if in_code:
                output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if not line.strip():
            flush_paragraph()
            close_list()
            i += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            flush_paragraph()
            close_list()
            level, text = len(heading.group(1)), heading.group(2).strip()
            output.append(f'<h{level} id="{safe_attr(text)}">{inline(text, source_file, page_lookup, page_id)}</h{level}>' )
            i += 1
            continue
        if re.match(r"^\s*(---+|\*\*\*+|___+)\s*$", line):
            flush_paragraph()
            close_list()
            output.append("<hr>")
            i += 1
            continue
        if line.lstrip().startswith(">"):
            flush_paragraph()
            close_list()
            quote_lines = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            output.append("<blockquote><p>" + inline(" ".join(quote_lines), source_file, page_lookup, page_id) + "</p></blockquote>")
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            flush_paragraph()
            close_list()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
                rows.append(row)
                i += 1
            if len(rows) > 1:
                headers = rows[0]
                body_rows = [row for row in rows[2:] if not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in row)]
                output.append('<div class="table-wrap"><table><thead><tr>' + "".join(f"<th>{inline(cell, source_file, page_lookup, page_id)}</th>" for cell in headers) + "</tr></thead><tbody>")
                for row in body_rows:
                    output.append("<tr>" + "".join(f"<td>{inline(cell, source_file, page_lookup, page_id)}</td>" for cell in row) + "</tr>")
                output.append("</tbody></table></div>")
            continue
        unordered = re.match(r"^\s*[-*+]\s+(.+)$", line)
        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if unordered or ordered:
            flush_paragraph()
            kind = "ul" if unordered else "ol"
            if list_kind != kind:
                close_list()
                output.append(f"<{kind}>")
                list_kind = kind
            item = (unordered or ordered).group(1)
            output.append("<li>" + inline(item, source_file, page_lookup, page_id) + "</li>")
            i += 1
            continue
        close_list()
        paragraph.append(line)
        i += 1
    flush_paragraph()
    close_list()
    if in_code:
        output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(output)


def page_shell(title: str, active: str, content: str, page_lookup: dict[str, dict], home: bool = False) -> str:
    home_href = "index.html" if home else "../index.html"
    page_links = []
    ordered_types = ["topic", "concept", "source", "synthesis", "question"]
    for kind in ordered_types:
        entries = [item for item in page_lookup.values() if item["type"] == kind]
        unique = {item["id"]: item for item in entries}
        if not unique:
            continue
        links = "".join(
            f'<a class="side-link {"active" if item["id"] == active else ""}" href="{home_href.rsplit("/",1)[0] + "/" if not home else ""}{item["href"]}">{html.escape(item["title"])}</a>'
            for item in sorted(unique.values(), key=lambda x: x["title"])
        )
        page_links.append(f'<div class="side-group"><span>{TYPE_LABELS[kind]}</span>{links}</div>')
    sidebar = "\n".join(page_links)
    home_script = """<script>
(() => {
  const input = document.getElementById('wiki-search');
  if (!input) return;
  const cards = [...document.querySelectorAll('.knowledge-card')];
  const sections = [...document.querySelectorAll('.collection')];
  const status = document.getElementById('search-status');
  function filter() {
    const query = input.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const card of cards) {
      const show = !query || card.dataset.search.includes(query);
      card.hidden = !show;
      if (show) visible++;
    }
    for (const section of sections) {
      section.hidden = !section.querySelector('.knowledge-card:not([hidden])');
    }
    status.textContent = query ? `找到 ${visible} 個相關頁面` : '';
    const url = new URL(location.href);
    query ? url.searchParams.set('q', query) : url.searchParams.delete('q');
    history.replaceState(null, '', url);
  }
  input.addEventListener('input', filter);
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName)) {
      event.preventDefault(); input.focus();
    }
    if (event.key === 'Escape' && document.activeElement === input) {
      input.value = ''; filter(); input.blur();
    }
  });
  input.value = new URLSearchParams(location.search).get('q') || '';
  filter();
})();
</script>""" if home else ""
    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="LLM 研究 Wiki：來源可追溯、頁面互相連結並持續整理。">
  <meta name="theme-color" content="#F7F1E5">
  <title>{html.escape(title)}｜LLM 研究 Wiki</title>
  <link rel="stylesheet" href="{home_href.rsplit('/', 1)[0] + '/' if not home else ''}wiki-assets/site.css">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="{home_href}"><span class="brand-mark">研</span><span><strong>LLM 研究 Wiki</strong><small>從來源長出知識連結</small></span></a>
    <nav class="topnav"><a href="{home_href}">首頁</a><a href="{home_href}#collections">知識頁</a><a href="{home_href.rsplit('/', 1)[0] + '/' if not home else ''}AGENTS.md">AI 維護規則</a></nav>
  </header>
  <div class="layout">
    <aside class="sidebar"><a class="back-home" href="{home_href}">← 回到 Wiki 首頁</a>{sidebar}</aside>
    <main class="main-content">{content}</main>
  </div>
  <footer class="site-footer"><span>LLM Wiki · 以原始來源為依據，持續累積可追溯的研究知識</span><a href="{home_href}">回到首頁 ↑</a></footer>
  {home_script}
</body>
</html>'''


def first_summary(body: str) -> str:
    text = re.sub(r"^#.*$", "", body, flags=re.M).strip()
    text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r"[`*_>#|]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text[:150].rstrip()


def build() -> int:
    entries, lookup = build_page_map()
    summaries = index_summaries()
    for item in entries:
        source = ROOT / item["source"]
        key = item["source"].casefold()
        candidates = [item["source"], "wiki/" + source.relative_to(WIKI).as_posix()]
        summary = next((summaries[c.casefold()][1] for c in candidates if c.casefold() in summaries), "")
        if not summary:
            summary = first_summary(item["body"])
        item["summary"] = summary
        rendered = render_markdown(item["body"], source, lookup, item["id"])
        tags = [scalar(tag) for tag in item["tags"].split(",") if scalar(tag)]
        tag_html = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in tags)
        content = f'''<article class="wiki-page">
  <nav class="breadcrumbs"><a href="../index.html">首頁</a><span>›</span><span>{html.escape(item["typeLabel"])}</span></nav>
  <header class="page-header"><div class="eyebrow">{item["icon"]}　{html.escape(item["typeLabel"])}</div><h1>{html.escape(item["title"])}</h1><div class="page-meta">{tag_html}</div></header>
  <div class="prose">{rendered}</div>
  <div class="page-bottom"><a href="../index.html">← 回到知識總覽</a><a href="../{item["source"]}">查看 Markdown 原頁 ↗</a></div>
</article>'''
        out = PAGES_OUT / f'{item["id"]}.html'
        out.write_text(page_shell(item["title"], item["id"], content, lookup), encoding="utf-8")

    categories = []
    for kind in ["topic", "concept", "source", "synthesis", "question"]:
        group = [item for item in entries if item["type"] == kind]
        if not group:
            continue
        cards = "".join(
            f'''<a class="knowledge-card" href="{item["href"]}" data-search="{safe_attr((item["title"] + " " + item["summary"] + " " + item["typeLabel"]).casefold())}">
  <span class="card-icon">{item["icon"]}</span><span class="card-copy"><small>{html.escape(item["typeLabel"])}</small><strong>{html.escape(item["title"])}</strong><span>{html.escape(item["summary"])}</span></span><span class="card-arrow">↗</span>
</a>'''
            for item in group
        )
        categories.append(f'<section class="collection" id="section-{kind}"><div class="section-title"><h2>{TYPE_ICONS[kind]}　{TYPE_LABELS[kind]}</h2><span>{len(group):02d} 頁</span></div><div class="card-grid">{cards}</div></section>')

    source_count = sum(item["type"] == "source" for item in entries)
    concept_count = sum(item["type"] == "concept" for item in entries)
    topic_count = sum(item["type"] == "topic" for item in entries)
    summary_count = sum(item["type"] == "synthesis" for item in entries)
    intro = f'''<section class="hero">
  <div class="hero-copy"><span class="eyebrow">PERSONAL RESEARCH KNOWLEDGE BASE</span><h1>讓研究知識，<br><em>一篇一篇累積起來。</em></h1><p>這是一個以大型語言模型研究為核心的個人 Wiki。原始文獻保存在來源層，AI 整理成彼此連結、可以追溯依據的知識頁，讓每次閱讀都能接續前一次的研究。</p><a class="primary-button" href="#collections">開始逛知識頁 <span>↓</span></a></div>
  <div class="hero-art" aria-hidden="true"><div class="orbit orbit-one">LLM</div><div class="orbit orbit-two">研究</div><div class="book-stack"><span>來源</span><span>概念</span><span>綜述</span></div><span class="spark spark-one">✳</span><span class="spark spark-two">✦</span><div class="tape"></div></div>
</section>
<section class="stats"><div><strong>{source_count:02d}</strong><span>篇來源研究</span></div><div><strong>{concept_count:02d}</strong><span>個概念頁</span></div><div><strong>{topic_count:02d}</strong><span>個研究主題</span></div><div><strong>{summary_count:02d}</strong><span>份跨篇綜述</span></div></section>
<section class="how"><div><span class="eyebrow">HOW THIS WIKI GROWS</span><h2>來源 → 知識 → 新問題</h2></div><p><strong>raw</strong> 保存原始文獻　·　<strong>wiki</strong> 整理重點與連結　·　<strong>AGENTS.md</strong> 告訴 AI 如何持續維護</p></section>'''
    search = '''<section class="search-area" id="collections"><div><span class="eyebrow">BROWSE THE WIKI</span><h2>找一頁開始讀</h2></div><label class="search-box"><span aria-hidden="true">⌕</span><input id="wiki-search" type="search" placeholder="搜尋主題、概念、論文……" autocomplete="off"><kbd>/</kbd></label></section><p class="search-status" id="search-status" aria-live="polite"></p>'''
    home_content = intro + search + "\n".join(categories) + '''<section class="rules-callout"><div><span class="eyebrow">THE WIKI SCHEMA</span><h2>讓 AI 知道怎麼接著做</h2><p>新增文獻時保存原檔、建立來源頁、更新相關概念與索引；回答研究問題時先查 Wiki，引用證據並標明未知。</p></div><a href="AGENTS.md" class="secondary-button">閱讀 AGENTS.md →</a></section>'''
    ENTRY.write_text(page_shell("首頁", "", home_content, lookup, home=True), encoding="utf-8")

    css = r'''
:root{--cream:#F7F1E5;--paper:#FFFDF8;--lav:#C8BEDA;--blue:#B9CAD5;--pink:#E6C5CC;--peach:#E9B9AE;--sage:#B9C6AE;--ink:#403C45;--muted:#736e78;--line:#e6ddd3;--purple:#665a72;--shadow:0 16px 42px #43392e12}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:radial-gradient(ellipse at 92% 3%,#e6c5cc55,transparent 26%),radial-gradient(ellipse at 0% 60%,#b9cad522,transparent 24%),#f2ede4;font-family:"Aptos","Microsoft JhengHei","PingFang TC",sans-serif;line-height:1.65}.topbar{height:78px;padding:0 max(24px,calc((100vw - 1240px)/2));display:flex;align-items:center;justify-content:space-between;background:#fffdf8d9;border-bottom:1px solid #e5ddd4;backdrop-filter:blur(10px)}.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--ink)}.brand-mark{width:42px;height:42px;border-radius:15px;background:var(--lav);display:grid;place-items:center;font-family:"DFKai-SB","BiauKai",serif;font-size:20px;box-shadow:inset 0 0 0 4px #ffffff55}.brand strong,.brand small{display:block}.brand strong{font-size:15px;letter-spacing:.04em}.brand small{font-size:11px;color:var(--muted)}.topnav{display:flex;gap:25px}.topnav a,.site-footer a{font-size:13px;text-decoration:none;color:#635d67}.topnav a:hover,.site-footer a:hover{color:var(--purple)}.layout{width:min(1240px,calc(100% - 40px));margin:30px auto 70px;display:grid;grid-template-columns:230px minmax(0,1fr);gap:26px;align-items:start}.sidebar{position:sticky;top:18px;max-height:calc(100vh - 36px);overflow:auto;padding:18px 14px;background:#fffdf8c9;border:1px solid var(--line);border-radius:18px}.back-home{display:block;color:var(--purple);text-decoration:none;font-weight:700;font-size:13px;padding:4px 8px 14px;border-bottom:1px solid var(--line)}.side-group{padding:14px 0 5px}.side-group>span{display:block;padding:0 8px 6px;text-transform:uppercase;letter-spacing:.11em;font-size:10px;color:#8a828c;font-weight:800}.side-link{display:block;padding:6px 8px;border-radius:9px;text-decoration:none;color:#5e5962;font-size:12px;line-height:1.45}.side-link:hover,.side-link.active{background:#eee8f1;color:#53495e}.main-content{min-width:0}.hero{position:relative;min-height:365px;padding:48px 54px;display:grid;grid-template-columns:1.35fr .65fr;align-items:center;gap:20px;border:1px solid #fff9;border-radius:26px;background:linear-gradient(112deg,#f7f1e5 0 63%,#eee8f2 63%);box-shadow:var(--shadow);overflow:hidden}.hero:after{position:absolute;content:"";right:15%;top:14px;width:90px;height:19px;background:#c8bedaa6;transform:rotate(4deg);clip-path:polygon(2% 0,100% 7%,96% 100%,0 93%)}.eyebrow{font-size:11px;letter-spacing:.16em;font-weight:800;color:#817984}.hero h1{font-family:"DFKai-SB","BiauKai","Noto Serif TC",serif;font-size:clamp(36px,4.3vw,57px);line-height:1.25;letter-spacing:.04em;margin:14px 0 13px}.hero h1 em{font-style:normal;color:#70637c}.hero p{font-size:15px;line-height:1.8;color:#69636e;max-width:620px;margin:0 0 22px}.primary-button,.secondary-button{display:inline-flex;gap:15px;align-items:center;text-decoration:none;border-radius:999px;padding:10px 18px;font-weight:700;font-size:13px}.primary-button{background:#665b72;color:#fffdf8}.primary-button:hover{background:#50465c}.hero-art{height:250px;position:relative;display:grid;place-items:center}.orbit{position:absolute;display:grid;place-items:center;border-radius:50%;font-family:"DFKai-SB","BiauKai",serif;font-weight:700}.orbit-one{width:194px;height:194px;background:#d9d1e2;border:1px dashed #fff9;box-shadow:inset 0 0 0 10px #ffffff44;font-size:25px;transform:rotate(-10deg)}.orbit-two{width:104px;height:104px;background:#e8c7ca;right:6%;bottom:12%;font-size:18px;transform:rotate(9deg)}.book-stack{z-index:1;display:flex;flex-direction:column;gap:8px;transform:rotate(5deg)}.book-stack span{width:130px;padding:7px 14px;border-radius:7px 16px 16px 7px;text-align:center;font-size:13px;font-weight:700;background:#fffaf3;border-left:8px solid var(--peach);box-shadow:0 6px 15px #4c414014}.book-stack span:nth-child(2){border-color:var(--sage);transform:translateX(10px)}.book-stack span:nth-child(3){border-color:var(--blue);transform:translateX(-6px)}.spark{position:absolute;color:#9a89a7}.spark-one{top:23%;right:16%;font-size:35px}.spark-two{bottom:14%;left:8%;font-size:24px}.stats{display:grid;grid-template-columns:repeat(4,1fr);margin:18px 0 32px;padding:18px;background:#fffdf8;border:1px solid var(--line);border-radius:18px;box-shadow:0 8px 25px #453c3310}.stats div{text-align:center;border-right:1px solid var(--line)}.stats div:last-child{border:0}.stats strong,.stats span{display:block}.stats strong{font:700 27px Georgia,serif;color:#645a70}.stats span{font-size:11px;color:var(--muted)}.how{display:flex;justify-content:space-between;align-items:end;gap:20px;padding:5px 2px 21px}.how h2,.search-area h2,.rules-callout h2{font-family:"DFKai-SB","BiauKai",serif;margin:4px 0 0;font-size:24px;letter-spacing:.03em}.how p{font-size:12px;color:#6d6771;margin:0}.search-area{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:19px 21px;background:#ede8f1;border-radius:18px 18px 0 0}.search-box{width:min(420px,52%);height:44px;display:flex;align-items:center;gap:10px;padding:0 13px;background:#fffdf8;border:1px solid #ddd4e3;border-radius:13px;color:#857a8d}.search-box>span{font:28px Georgia}.search-box input{min-width:0;flex:1;border:0;outline:0;color:var(--ink);background:transparent;font:13px inherit}.search-box kbd{padding:1px 7px;border:1px solid #ded7e2;border-radius:5px;background:#f8f5fa;font-size:11px}.search-status{min-height:12px;margin:0;padding:0 21px;background:#ede8f1;color:#6d6374;font-size:11px}.collection{padding:25px 21px 7px;background:#fffdf8;border-bottom:1px solid var(--line)}.collection:last-of-type{padding-bottom:30px;border-radius:0 0 18px 18px}.section-title{display:flex;justify-content:space-between;align-items:center;margin-bottom:13px}.section-title h2{font-family:"DFKai-SB","BiauKai",serif;font-size:19px;margin:0}.section-title>span{font-size:11px;color:#8b838c}.card-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.knowledge-card{position:relative;display:grid;grid-template-columns:36px minmax(0,1fr) 17px;align-items:start;gap:10px;padding:13px 14px;background:#fffefa;border:1px solid #eee6dd;border-radius:14px;text-decoration:none;color:var(--ink);transition:transform .16s,box-shadow .16s}.knowledge-card:hover{transform:translateY(-2px);box-shadow:0 7px 18px #463d3210}.card-icon{width:34px;height:34px;display:grid;place-items:center;background:#f0ebf3;border-radius:11px;font-size:17px}.collection:nth-of-type(2) .card-icon{background:#eef2eb}.collection:nth-of-type(3) .card-icon{background:#f7eceb}.card-copy{min-width:0}.card-copy small{display:block;color:#877e8a;font-size:10px;margin-bottom:2px}.card-copy strong{display:block;font-size:13px;line-height:1.45;margin-bottom:4px}.card-copy>span{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;color:#726c75;font-size:11px;line-height:1.5}.card-arrow{color:#9a8da3;font-size:14px}.rules-callout{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-top:20px;padding:23px 25px;background:#e8eee7;border:1px solid #dbe5d8;border-radius:18px}.rules-callout p{font-size:12px;color:#5e665c;max-width:650px;margin:5px 0 0}.secondary-button{white-space:nowrap;border:1px solid #c8d4c3;color:#52634f;background:#f7fbf5}.secondary-button:hover{background:#fff}.site-footer{display:flex;justify-content:space-between;gap:12px;padding:20px max(24px,calc((100vw - 1240px)/2));border-top:1px solid #ded6cc;color:#817b83;font-size:11px}.breadcrumbs{display:flex;gap:9px;align-items:center;font-size:11px;color:#8a838d;margin:1px 0 18px}.breadcrumbs a,.page-bottom a{color:#695e75;text-decoration:none}.page-header{position:relative;padding:27px 31px 24px;margin-bottom:16px;background:linear-gradient(115deg,#fffdf8,#f0ebf3);border:1px solid #fff;border-radius:19px;box-shadow:0 8px 24px #43392e0a}.page-header .eyebrow{display:block}.page-header h1{font-family:"DFKai-SB","BiauKai",serif;line-height:1.35;font-size:clamp(26px,3vw,38px);margin:9px 0 13px}.page-meta{display:flex;flex-wrap:wrap;gap:6px}.tag{padding:3px 9px;border-radius:999px;background:#f4f0f7;color:#71677a;font-size:10px}.prose{padding:30px clamp(20px,5vw,58px);background:#fffdf8;border:1px solid #eee5dc;border-radius:19px;box-shadow:0 8px 25px #43392e08;overflow:hidden}.prose h1{font-family:"DFKai-SB","BiauKai",serif;font-size:28px;line-height:1.4;margin:0 0 18px}.prose h2{font-family:"DFKai-SB","BiauKai",serif;font-size:22px;margin:32px 0 12px;padding-bottom:8px;border-bottom:1px solid #eee4dc}.prose h3{font-size:17px;margin:24px 0 8px;color:#5e5668}.prose h4{font-size:15px}.prose p,.prose li{font-size:14px;line-height:1.85;color:#524d56}.prose li{padding:2px 0}.prose a{color:#645679;text-decoration-thickness:1px;text-underline-offset:3px}.prose blockquote{margin:16px 0;padding:10px 15px;border-left:4px solid var(--peach);background:#fcf6ee;border-radius:0 12px 12px 0;color:#6b626c}.prose blockquote p{margin:0}.prose code{padding:2px 5px;border-radius:5px;background:#f0edf2;font:12px Consolas,monospace;color:#5e5668}.prose pre{max-width:100%;overflow:auto;padding:15px;border-radius:12px;background:#f3f0f4}.prose pre code{padding:0;background:transparent}.prose hr{border:0;border-top:1px solid var(--line);margin:27px 0}.table-wrap{max-width:100%;overflow:auto;margin:15px 0 22px;border:1px solid var(--line);border-radius:12px}.prose table{width:100%;border-collapse:collapse;min-width:520px;font-size:12px}.prose th,.prose td{padding:9px 11px;text-align:left;vertical-align:top;border-bottom:1px solid #eee5dc}.prose th{background:#f1edf4;color:#5b5364;font-weight:700}.prose tr:nth-child(even) td{background:#fffaf4}.page-bottom{display:flex;justify-content:space-between;gap:12px;margin:14px 2px;font-size:12px}.empty-state{display:none;padding:30px;text-align:center;color:#817986}.empty-state.visible{display:block}
@media(max-width:900px){.layout{grid-template-columns:190px minmax(0,1fr);gap:16px}.hero{padding:35px;grid-template-columns:1.2fr .8fr}.hero-art{transform:scale(.86)}.how{align-items:start;flex-direction:column;gap:5px}}
@media(max-width:680px){.topbar{height:auto;min-height:68px;padding:11px 16px}.topnav{gap:12px}.topnav a{font-size:11px}.layout{width:calc(100% - 24px);display:block;margin:14px auto 40px}.sidebar{position:static;max-height:none;display:flex;gap:7px;align-items:center;overflow:auto;padding:8px;margin-bottom:12px;white-space:nowrap}.back-home{border:0;padding:7px 9px;white-space:nowrap}.side-group{display:contents}.side-group>span{display:none}.side-link{padding:7px 10px;background:#fffdf8;border:1px solid var(--line);white-space:nowrap}.side-link.active{background:#eee8f1}.hero{min-height:0;padding:28px 23px;display:block}.hero h1{font-size:35px}.hero p{font-size:13px}.hero-art{position:absolute;right:-60px;bottom:-28px;width:190px;height:160px;opacity:.48;transform:scale(.7)}.hero-copy{position:relative;z-index:1}.stats{margin:12px 0 21px;padding:12px 6px}.stats strong{font-size:21px}.stats span{font-size:9px}.stats div{padding:0 4px}.how{padding-bottom:14px}.how h2,.search-area h2{font-size:21px}.search-area{padding:15px;align-items:stretch;flex-direction:column;gap:9px}.search-box{width:100%}.collection{padding:20px 13px 5px}.card-grid{grid-template-columns:1fr}.rules-callout{align-items:flex-start;flex-direction:column;padding:19px}.site-footer{padding:16px;flex-direction:column}.page-header{padding:21px}.prose{padding:22px 17px}.prose p,.prose li{font-size:13px}.page-bottom{font-size:10px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
'''
    (ASSETS_OUT / "site.css").write_text(css, encoding="utf-8")
    return len(entries)


if __name__ == "__main__":
    count = build()
    print(f"Built Wiki website: {count} pages → {ENTRY.relative_to(ROOT)} and {PAGES_OUT.relative_to(ROOT)}")
