#!/usr/bin/env python3
"""DegenKit blog builder. Reads blog-src/posts/*.md and writes static pages into /blog.
No dependencies, no runtime JS needed for content. All text is HTML-escaped; raw HTML in posts is never passed through.
Usage:  python3 blog-src/build.py
"""
import html, re, sys, math, datetime, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
POSTS = ROOT / "blog-src" / "posts"
OUT = ROOT / "blog"
SITE = "https://degenkit.app"
AUTHOR = "DegenKit"
DEFAULT_COVER = "/assets/mascot-hero.png"

esc = lambda s: html.escape(str(s), quote=True)

# ---------------------------------------------------------------- helpers
def parse_front(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        raise ValueError("missing front matter (--- ... ---)")
    meta = {}
    last = None
    for line in m.group(1).splitlines():
        st = line.strip()
        if st.startswith("- ") and last:                      # YAML list item (tags: / - Guide)
            meta[last] = (meta.get(last, "") + "," if meta.get(last) else "") + st[2:].strip().strip('"').strip("'")
        elif ":" in line and not st.startswith("#"):
            k, v = line.split(":", 1)
            last = k.strip().lower()
            v = v.strip().strip('"').strip("'")
            if last == "tags": v = v.strip("[]")
            meta[last] = v
    return meta, m.group(2)

def safe_url(u, allow_rel=True):
    u = u.strip()
    if re.match(r"^(https?://|mailto:)", u, re.I): return u
    if allow_rel and re.match(r"^(/|#|\.{0,2}/|[A-Za-z0-9_\-./]+$)", u) and not re.match(r"^\s*(javascript|data|vbscript):", u, re.I): return u
    return "#"

def inline(s):
    """Minimal, safe inline markdown: code, bold, italic, links."""
    codes = []
    def keep(m):
        codes.append("<code>%s</code>" % esc(m.group(1))); return "\0%d\0" % (len(codes) - 1)
    s = re.sub(r"`([^`]+)`", keep, s)
    s = esc(s)
    def link(m):
        text, url = m.group(1), html.unescape(m.group(2))
        url = safe_url(url)
        ext = re.match(r"^https?://", url, re.I) and not url.startswith(SITE)
        extra = ' target="_blank" rel="noopener noreferrer"' if ext else ""
        return '<a href="%s"%s>%s</a>' % (esc(url), extra, text)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\0(\d+)\0", lambda m: codes[int(m.group(1))], s)
    return s

def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

VIDEO = re.compile(r"\.(mp4|webm)(\?.*)?$", re.I)

def media(alt, src, caption):
    src = safe_url(src)
    cap = '<figcaption>%s</figcaption>' % inline(caption) if caption else ""
    if VIDEO.search(src):
        body = '<video src="%s" autoplay loop muted playsinline preload="metadata" aria-label="%s"></video>' % (esc(src), esc(alt))
    else:
        body = '<img src="%s" alt="%s" loading="lazy" decoding="async">' % (esc(src), esc(alt))
    return "<figure>%s%s</figure>" % (body, cap)

def render(md):
    lines = md.replace("\r\n", "\n").split("\n")
    out, i, toc = [], 0, []
    para = []
    def flush():
        nonlocal para
        if para:
            out.append("<p>%s</p>" % inline(" ".join(x.strip() for x in para))); para = []
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            flush(); i += 1; continue
        if ln.startswith("```"):
            flush(); i += 1; buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % esc("\n".join(buf))); continue
        m = re.match(r"^(#{2,3})\s+(.*)$", ln)
        if m:
            flush(); lvl = len(m.group(1)); txt = m.group(2).strip(); sid = slugify(txt)
            if lvl == 2: toc.append((sid, txt))
            out.append('<h%d id="%s">%s</h%d>' % (lvl, esc(sid), inline(txt), lvl)); i += 1; continue
        if re.match(r"^(-{3,}|\*{3,})\s*$", ln):
            flush(); out.append("<hr>"); i += 1; continue
        m = re.match(r'^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)\s*$', ln)
        if m:
            flush(); out.append(media(m.group(1), m.group(2), m.group(3) or "")); i += 1; continue
        m = re.match(r"^@\[youtube\]\(([A-Za-z0-9_-]{6,15})\)\s*$", ln)
        if m:
            flush()
            out.append('<figure class="embed"><iframe src="https://www.youtube-nocookie.com/embed/%s" title="YouTube video" loading="lazy" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></figure>' % m.group(1)); i += 1; continue
        m = re.match(r"^:::(tip|note|warning)\s*(.*)$", ln)
        if m:
            flush(); kind, title = m.group(1), m.group(2).strip(); i += 1; buf = []
            while i < len(lines) and lines[i].strip() != ":::":
                buf.append(lines[i]); i += 1
            i += 1
            out.append('<aside class="callout %s">%s%s</aside>' % (kind, ("<strong>%s</strong>" % inline(title)) if title else "", render("\n".join(buf))[0])); continue
        if ln.startswith(">"):
            flush(); buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].lstrip()); i += 1
            out.append("<blockquote>%s</blockquote>" % "".join("<p>%s</p>" % inline(p) for p in "\n".join(buf).split("\n\n") if p.strip())); continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", ln)
        if m:
            flush(); ordered = m.group(2)[0].isdigit(); items = []
            while i < len(lines):
                mm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                if not mm: break
                items.append(mm.group(3)); i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag)); continue
        para.append(ln); i += 1
    flush()
    return "\n".join(out), toc

def fmt_date(d):
    return d.strftime("%B %-d, %Y")

def load_posts():
    posts = []
    for f in sorted(POSTS.glob("*.md")):
        if f.name.startswith("_"): continue
        meta, body = parse_front(f.read_text(encoding="utf-8"))
        if meta.get("draft", "").lower() in ("true", "yes", "1"): continue
        for req in ("title", "date", "excerpt"):
            if not meta.get(req): raise SystemExit("%s: missing '%s'" % (f.name, req))
        slug = slugify(meta.get("slug") or f.stem)
        date = datetime.date.fromisoformat(meta["date"])
        html_body, toc = render(body)
        words = len(re.findall(r"\w+", body))
        posts.append(dict(
            title=meta["title"], slug=slug, date=date, excerpt=meta["excerpt"],
            cover=meta.get("cover", ""), cover_alt=meta.get("cover_alt", meta["title"]),
            tags=[t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            body=html_body, minutes=max(1, math.ceil(words / 200)),
        ))
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts

# ---------------------------------------------------------------- page shell
HEAD_SCRIPTS = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18369032243"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-18369032243');
</script>
<!-- X Pixel base code -->
<script>
!function(e,t,n,s,u,a){e.twq||(s=e.twq=function(){s.exe?s.exe.apply(s,arguments):s.queue.push(arguments);
},s.version='1.1',s.queue=[],u=t.createElement(n),u.async=!0,u.src='https://static.ads-twitter.com/uwt.js',
a=t.getElementsByTagName(n)[0],a.parentNode.insertBefore(u,a))}(window,document,'script');
twq('config','rfyik');
</script>
<!-- End X Pixel base code -->"""

HEADER = """<header>
  <div class="header-row">
    <a class="logo" href="/"><img src="/assets/icon.png" alt="" class="logo-icon"><span class="logo-text">DegenKit</span></a>
    <nav class="site-nav">
      <a class="navlink" href="/#features">Features</a>
      <a class="navlink" href="/#roadmap">Roadmap</a>
      <a class="navlink" href="/blog/">Blog</a>
      <a class="navlink" href="/#faq">FAQ</a>
    </nav>
    <div class="header-actions">
      <button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle light/dark theme" title="Toggle theme">◐</button>
      <a class="btn-launch" href="/launch/">Launch App</a>
    </div>
  </div>
</header>"""

FOOTER = """<footer>
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="logo"><img src="/assets/icon.png" alt="" class="logo-icon"><span class="logo-text">DegenKit</span></div>
        <p>Token creation, without the guesswork. Launch on Solana, Ethereum, BNB Chain, Base and Robinhood Chain.</p>
      </div>
      <div class="footer-cols">
        <div class="footer-col"><h4>Site</h4><a href="/">Home</a><a href="/launch/">Launch App</a><a href="/blog/">Blog</a></div>
        <div class="footer-col"><h4>Legal</h4><a href="/terms/">Terms &amp; Conditions</a><a href="/privacy/">Privacy Policy</a></div>
        <div class="footer-col"><h4>Help</h4><a href="/support/">Support</a></div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© %d DegenKit. All rights reserved.</p>
      <div class="footer-socials"><a class="social-icn" href="https://x.com/DegenKitApp" target="_blank" rel="noopener" aria-label="X / Twitter">𝕏</a></div>
    </div>
  </div>
</footer>""" % datetime.date.today().year

THEME_JS = """<script>
(function(){var r=document.documentElement,b=document.getElementById('themeToggle');
if(b)b.addEventListener('click',function(){var n=r.getAttribute('data-theme')==='light'?'dark':'light';r.setAttribute('data-theme',n);try{localStorage.setItem('degenkit-theme',n)}catch(e){}});
document.querySelectorAll('[data-copy]').forEach(function(el){el.addEventListener('click',function(){var u=el.getAttribute('data-copy'),t=el.textContent;
(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){el.textContent='Copied ✓';setTimeout(function(){el.textContent=t},1600)}).catch(function(){window.prompt('Copy link',u)})})});})();
</script>"""

PRE_THEME = "<script>try{var t=localStorage.getItem('degenkit-theme');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}</script>"

def page(title, desc, canonical, body, og_image=None, og_type="website", jsonld="", extra_meta=""):
    img = og_image or SITE + "/assets/mascot-hero.png"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD_SCRIPTS}
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<link rel="alternate" type="application/rss+xml" title="DegenKit Blog" href="/blog/rss.xml">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#0B0B0E">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta property="og:locale" content="en_US">
{extra_meta}
<meta property="og:site_name" content="DegenKit">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@DegenKitApp">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(img)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
<link rel="stylesheet" href="/assets/theme-icons.css">
<link rel="stylesheet" href="/assets/blog.css">
{PRE_THEME}
{jsonld}
</head>
<body>
{HEADER}
{body}
{FOOTER}
{THEME_JS}
</body>
</html>
"""

def cover_html(p, cls="cover"):
    if p["cover"]:
        return '<div class="%s"><img src="%s" alt="%s" loading="lazy" decoding="async"></div>' % (cls, esc(safe_url(p["cover"])), esc(p["cover_alt"]))
    return '<div class="%s ph"><img src="/assets/icon.png" alt=""></div>' % cls

def tags_html(p):
    return "".join('<span class="chip">%s</span>' % esc(t) for t in p["tags"][:3])

def card(p, cls="card"):
    return f"""<a class="{cls}" href="/blog/{p['slug']}/">
  {cover_html(p)}
  <div class="c-body">
    <div class="c-meta">{tags_html(p)}<span>{fmt_date(p['date'])}</span></div>
    <h2>{esc(p['title'])}</h2>
    <p>{esc(p['excerpt'])}</p>
  </div>
</a>"""

def abs_url(u):
    return u if re.match(r"^https?://", u) else SITE + (u if u.startswith("/") else "/" + u)

# ---------------------------------------------------------------- builders
def build_index(posts):
    if posts:
        f = posts[0]
        feat = f"""<a class="feature" href="/blog/{f['slug']}/">
  {cover_html(f, 'cover')}
  <div class="f-body">
    <div class="c-meta">{tags_html(f)}<span>{fmt_date(f['date'])} · {f['minutes']} min read</span></div>
    <h2>{esc(f['title'])}</h2>
    <p>{esc(f['excerpt'])}</p>
    <span class="more">Read the post →</span>
  </div>
</a>"""
        rest = "".join(card(p) for p in posts[1:])
        grid = f'<div class="grid">{rest}</div>' if rest else ""
    else:
        feat, grid = '<p class="empty">First post coming soon.</p>', ""
    body = f"""<main class="bwrap">
  <section class="b-hero">
    <div class="eyebrow" style="display:inline-flex;">Blog</div>
    <h1>Notes from the runway</h1>
    <p>Updates, guides and launch playbooks from DegenKit.</p>
  </section>
  {feat}
  {grid}
</main>"""
    import json as _j
    idx_ld = '<script type="application/ld+json">%s</script>' % _j.dumps({
        "@context": "https://schema.org", "@type": "Blog", "name": "DegenKit Blog", "url": SITE + "/blog/", "inLanguage": "en",
        "publisher": {"@type": "Organization", "name": AUTHOR, "url": SITE + "/"},
        "blogPost": [{"@type": "BlogPosting", "headline": q["title"], "url": f"{SITE}/blog/{q['slug']}/", "datePublished": q["date"].isoformat()} for q in posts]}).replace("</", "<\\/")
    idx_ld += '<script type="application/ld+json">%s</script>' % _j.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "DegenKit", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"}]})
    (OUT / "index.html").write_text(page("DegenKit Blog — Token Launch Guides & Playbooks", "Practical guides on launching a token: authorities, metadata, taxes, airdrops, liquidity, risk checks and choosing a network.", SITE + "/blog/", body, jsonld=idx_ld), encoding="utf-8")

def build_post(p, posts):
    url = f"{SITE}/blog/{p['slug']}/"
    tagset = set(t.lower() for t in p["tags"])
    others = sorted([x for x in posts if x["slug"] != p["slug"]],
                    key=lambda x: (-len(tagset & set(t.lower() for t in x["tags"])), -x["date"].toordinal()))[:3]
    related = ""
    if others:
        related = '<section class="related"><h3>Keep reading</h3><div class="grid">%s</div></section>' % "".join(card(x) for x in others)
    share_text = urllib.parse.quote(p["title"] + " — via @DegenKitApp")
    share_url = urllib.parse.quote(url, safe="")
    og_img = abs_url(p["cover"]) if p["cover"] else None
    jsonld = '<script type="application/ld+json">%s</script>' % __import__("json").dumps({
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["excerpt"],
        "datePublished": p["date"].isoformat(), "dateModified": p["date"].isoformat(),
        "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "url": url, "inLanguage": "en",
        "image": og_img or SITE + "/assets/mascot-hero.png",
        "keywords": ", ".join(p["tags"]),
        "author": {"@type": "Organization", "name": AUTHOR, "url": SITE + "/"},
        "publisher": {"@type": "Organization", "name": AUTHOR, "url": SITE + "/",
                      "logo": {"@type": "ImageObject", "url": SITE + "/assets/icon.png"}},
    }).replace("</", "<\\/")
    jsonld += '<script type="application/ld+json">%s</script>' % __import__("json").dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "DegenKit", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}).replace("</", "<\\/")
    extra = '<meta property="article:published_time" content="%s">\n<meta property="article:modified_time" content="%s">\n<meta property="og:image:alt" content="%s">' % (p["date"].isoformat(), p["date"].isoformat(), esc(p["cover_alt"] or p["title"]))
    for t in p["tags"][:5]: extra += '\n<meta property="article:tag" content="%s">' % esc(t)
    body = f"""<main class="bwrap">
  <article class="post">
    <div class="p-head">
      <nav aria-label="Breadcrumb"><a class="back" href="/blog/">← All posts</a></nav>
      <div class="chips">{tags_html(p)}</div>
      <h1>{esc(p['title'])}</h1>
      <p class="lede">{esc(p['excerpt'])}</p>
      <div class="byline"><img src="/assets/icon.png" alt=""><span><b>{AUTHOR}</b><i>{fmt_date(p['date'])} · {p['minutes']} min read</i></span></div>
    </div>
    {cover_html(p, 'cover hero')}
    <div class="prose">
{p['body']}
    </div>
    <div class="share">
      <b>Share this post</b>
      <div class="share-btns">
        <a class="s-x" href="https://x.com/intent/post?text={share_text}&amp;url={share_url}" target="_blank" rel="noopener noreferrer">Share on 𝕏</a>
        <button class="s-copy" type="button" data-copy="{esc(url)}">Copy link</button>
      </div>
    </div>
    <aside class="cta">
      <div><h3>Ready to launch your token?</h3><p>Pick a network, set the details, sign once. No code.</p></div>
      <a class="btn-launch" href="/launch/">Launch App</a>
    </aside>
  </article>
  {related}
</main>"""
    d = OUT / p["slug"]; d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(page(f"{p['title']} | DegenKit Blog", p["excerpt"], url, body, og_img, "article", jsonld, extra), encoding="utf-8")

def build_rss(posts):
    items = "".join(f"<item><title>{esc(p['title'])}</title><link>{SITE}/blog/{p['slug']}/</link><guid>{SITE}/blog/{p['slug']}/</guid>"
                    f"<pubDate>{p['date'].strftime('%a, %d %b %Y 00:00:00 +0000')}</pubDate><description>{esc(p['excerpt'])}</description></item>" for p in posts)
    (OUT / "rss.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>DegenKit Blog</title><link>{SITE}/blog/</link>'
                                 f'<description>Updates, guides and launch playbooks from DegenKit.</description>{items}</channel></rss>', encoding="utf-8")

def update_sitemap(posts):
    sm = ROOT / "sitemap.xml"
    if not sm.exists(): return
    s = sm.read_text(encoding="utf-8")
    s = re.sub(r"[ \t]*<url><loc>[^<]*/blog/[^<]*</loc>.*?</url>\n?", "", s)
    entries = f'  <url><loc>{SITE}/blog/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>\n'
    entries += "".join(f'  <url><loc>{SITE}/blog/{p["slug"]}/</loc><lastmod>{p["date"].isoformat()}</lastmod><priority>0.6</priority></url>\n' for p in posts)
    s = s.replace("</urlset>", entries + "</urlset>")
    sm.write_text(s, encoding="utf-8")

def main():
    OUT.mkdir(exist_ok=True)
    posts = load_posts()
    slugs = [p["slug"] for p in posts]
    if len(slugs) != len(set(slugs)): raise SystemExit("duplicate slug")
    for p in posts: build_post(p, posts)
    build_index(posts); build_rss(posts); update_sitemap(posts)
    print("built %d post(s): %s" % (len(posts), ", ".join(slugs)))

if __name__ == "__main__":
    main()
