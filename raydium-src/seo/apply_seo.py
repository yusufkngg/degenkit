#!/usr/bin/env python3
"""DegenKit SEO pass — idempotent. Run from the site root:  python3 seo/apply_seo.py
Adds/refreshes: meta description, canonical, Open Graph, Twitter, theme-color, manifest, icons,
JSON-LD (Organization, WebSite, WebApplication, FAQPage, BreadcrumbList), robots.txt, llms.txt, sitemap.xml."""
import re, json, html, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://degenkit.app"
TODAY = datetime.date.today().isoformat()
IMG = SITE + "/assets/mascot-hero.png"
ROBOTS_META = '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'

PAGES = {
 "index.html": dict(url="/", title="DegenKit — No-Code Token Launcher (Solana, Ethereum, BNB, Base)",
   desc="Launch tokens with no code on Solana, Ethereum, BNB Chain, Base and Robinhood Chain. Non-custodial, one signature, flat fee, tax tokens included."),
 "launch/index.html": dict(url="/launch/", title="Create a Crypto Token Without Code — Choose Your Network | DegenKit",
   desc="Pick a network and create your token in minutes: Solana, Ethereum, BNB Chain, Base or Robinhood Chain. Non-custodial, no coding, one signature."),
 "launch/solana/index.html": dict(url="/launch/solana/", title="Create a Solana Token Without Code — SPL Token Creator | DegenKit",
   desc="Create an SPL token on Solana in one signature. Set name, symbol, supply and image; mint and freeze authority revoked and metadata locked. Includes Swap, Airdrop, Multisender and Scanner.",
   chain="Solana"),
 "launch/ethereum/index.html": dict(url="/launch/ethereum/", title="Create an Ethereum Token (ERC-20) Without Code | DegenKit",
   desc="Create a fixed-supply ERC-20 or a custom buy/sell tax token on Ethereum with no code. Connect your wallet, fill one form, sign once.",
   chain="Ethereum"),
 "launch/bnb/index.html": dict(url="/launch/bnb/", title="Create a BNB Chain Token (BEP-20) & Tax Token | DegenKit",
   desc="Launch a low-fee BEP-20 token or a tax token on BNB Smart Chain without writing code. Non-custodial: you sign, you own the token.",
   chain="BNB Chain"),
 "launch/base/index.html": dict(url="/launch/base/", title="Create a Base Token (ERC-20) Without Code | DegenKit",
   desc="Launch an ERC-20 or tax token on Base, Coinbase's low-fee Layer 2, with no code. Fill one form and sign once from your own wallet.",
   chain="Base"),
 "launch/robinhood/index.html": dict(url="/launch/robinhood/", title="Create a Robinhood Chain Token Without Code | DegenKit",
   desc="Launch a fixed-supply or tax token on Robinhood Chain with no code. Same simple one-form, one-signature flow, non-custodial.",
   chain="Robinhood Chain"),
 "support/index.html": dict(url="/support/", title="Support | DegenKit",
   desc="Get help with DegenKit: how to contact support and what to include so we can resolve token launch questions faster."),
 "terms/index.html": dict(url="/terms/", title="Terms & Conditions | DegenKit",
   desc="The terms that apply when you use DegenKit, the non-custodial no-code token launcher."),
 "privacy/index.html": dict(url="/privacy/", title="Privacy Policy | DegenKit",
   desc="How DegenKit handles data. The site is non-custodial: private keys and transactions never leave your wallet."),
}
ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "DegenKit", "url": SITE + "/",
       "logo": {"@type": "ImageObject", "url": SITE + "/assets/icon.png", "width": 160, "height": 160},
       "sameAs": ["https://x.com/DegenKitApp"]}

def esc(s): return html.escape(s, quote=True)
def ld(obj): return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def set_tag(h, pattern, tag):
    """Replace first match of pattern with tag, else insert before </head>."""
    if re.search(pattern, h, re.I | re.S):
        return re.sub(pattern, lambda m: tag, h, count=1, flags=re.I | re.S)
    return h.replace("</head>", tag + "\n</head>", 1)

def seo_block(p):
    u = SITE + p["url"]
    return "\n".join([
        f'<!-- seo:start -->',
        f'<title>{esc(p["title"])}</title>',
        f'<meta name="description" content="{esc(p["desc"])}">',
        f'<link rel="canonical" href="{u}">',
        ROBOTS_META,
        f'<meta name="theme-color" content="#0B0B0E">',
        f'<meta property="og:site_name" content="DegenKit">',
        f'<meta property="og:locale" content="en_US">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{esc(p["title"])}">',
        f'<meta property="og:description" content="{esc(p["desc"])}">',
        f'<meta property="og:url" content="{u}">',
        f'<meta property="og:image" content="{IMG}">',
        f'<meta property="og:image:alt" content="DegenKit mascot">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:site" content="@DegenKitApp">',
        f'<meta name="twitter:title" content="{esc(p["title"])}">',
        f'<meta name="twitter:description" content="{esc(p["desc"])}">',
        f'<meta name="twitter:image" content="{IMG}">',
        f'<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">',
        f'<link rel="manifest" href="/manifest.webmanifest">',
        f'<!-- seo:end -->'])

def jsonld_for(name, p, h):
    out = []
    if name == "index.html":
        out.append({"@context": "https://schema.org", **ORG})
        out.append({"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
                    "name": "DegenKit", "inLanguage": "en", "publisher": {"@id": SITE + "/#org"}})
        out.append({"@context": "https://schema.org", "@type": "WebApplication", "name": "DegenKit", "url": SITE + "/",
                    "applicationCategory": "FinanceApplication", "operatingSystem": "Any (web browser)",
                    "browserRequirements": "Requires JavaScript and a Web3 wallet",
                    "description": p["desc"], "publisher": {"@id": SITE + "/#org"},
                    "featureList": ["No-code token creation", "Solana, Ethereum, BNB Chain, Base and Robinhood Chain",
                                    "Non-custodial: you sign every transaction", "Buy/sell tax tokens on EVM chains",
                                    "Token authorities, metadata, burn, airdrop, multisender, scanner and swap tools on Solana"]})
        qa = []
        for m in re.finditer(r'<details class="faq-item[^"]*"[^>]*>\s*<summary>(.*?)</summary>\s*<div class="a">(.*?)</div>', h, re.S):
            q = strip_tags(re.sub(r'<span class="plus">.*?</span>', "", m.group(1), flags=re.S)); a = strip_tags(m.group(2))
            if q and a: qa.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
        if qa: out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qa})
    elif name.startswith("launch/") and p.get("chain"):
        out.append({"@context": "https://schema.org", "@type": "WebApplication", "name": f"DegenKit — {p['chain']} token creator",
                    "url": SITE + p["url"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any (web browser)",
                    "description": p["desc"], "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@id": SITE + "/#org"}})
        out.append(crumbs([("DegenKit", "/"), ("Launch", "/launch/"), (p["chain"], p["url"])]))
    elif name == "launch/index.html":
        out.append(crumbs([("DegenKit", "/"), ("Launch", "/launch/")]))
    else:
        out.append(crumbs([("DegenKit", "/"), (p["title"].split(" |")[0], p["url"])]))
    return "\n".join(ld(o) for o in out)

def patch_page(name, p):
    f = ROOT / name
    full = f.read_text(encoding="utf-8")
    i = full.index("</head>")
    h, rest = full[:i], full[i:]          # only ever touch the <head>
    faq_src = full                         # FAQ lives in the body
    # drop previous SEO block + our JSON-LD + old per-tag SEO so the page has exactly one of each
    h = re.sub(r"<!-- seo:start -->.*?<!-- seo:end -->\n?", "", h, flags=re.S)
    h = re.sub(r"<!-- seo:ld -->.*?<!-- /seo:ld -->\n?", "", h, flags=re.S)
    for pat in [r"<title>.*?</title>\s*", r'<meta name="description"[^>]*>\s*', r'<link rel="canonical"[^>]*>\s*',
                r'<meta property="og:[^"]*"[^>]*>\s*', r'<meta name="twitter:[^"]*"[^>]*>\s*', r'<meta name="robots"[^>]*>\s*',
                r'<meta name="theme-color"[^>]*>\s*', r'<link rel="apple-touch-icon"[^>]*>\s*', r'<link rel="manifest"[^>]*>\s*',
                r'<script type="application/ld\+json">.*?</script>\s*']:
        h = re.sub(pat, "", h, flags=re.S | re.I)
    block = seo_block(p) + "\n<!-- seo:ld -->\n" + jsonld_for(name, p, faq_src) + "\n<!-- /seo:ld -->"
    # place after the viewport meta (keeps charset/viewport first), else before </head>
    m = re.search(r'<meta name="viewport"[^>]*>', h, re.I)
    h = h[:m.end()] + "\n" + block + h[m.end():] if m else h + block + "\n"
    f.write_text(h + rest, encoding="utf-8")

def write_static():
    (ROOT / "robots.txt").write_text(f"""# DegenKit — everything public is open to search engines and AI search/answer crawlers.
User-agent: *
Allow: /

User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /
User-agent: YandexBot
Allow: /
User-agent: Baiduspider
Allow: /
User-agent: DuckDuckBot
Allow: /
User-agent: Applebot
Allow: /
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {SITE}/sitemap.xml
""", encoding="utf-8")
    (ROOT / "llms.txt").write_text(f"""# DegenKit

> DegenKit ({SITE}) is a no-code, non-custodial token launcher. Create a token on Solana, Ethereum, BNB Chain, Base or Robinhood Chain by filling one form and signing one transaction from your own wallet. DegenKit never holds keys or funds.

## Launch a token
- [Choose a network]({SITE}/launch/): network selector
- [Solana]({SITE}/launch/solana/): SPL tokens, mint/freeze authority revoked and metadata locked at creation; tools: Authorities, Update Metadata, Burn, Airdrop, Multisender, Scanner, Swap
- [Ethereum]({SITE}/launch/ethereum/): fixed-supply ERC-20 and tax tokens
- [BNB Chain]({SITE}/launch/bnb/): BEP-20 and tax tokens
- [Base]({SITE}/launch/base/): ERC-20 and tax tokens
- [Robinhood Chain]({SITE}/launch/robinhood/): fixed-supply and tax tokens

## Learn
- [Blog]({SITE}/blog/): guides on token launches, authorities, taxes, airdrops and risk checks
- [Support]({SITE}/support/)
- [Terms]({SITE}/terms/) · [Privacy]({SITE}/privacy/)
""", encoding="utf-8")
    (ROOT / "manifest.webmanifest").write_text(json.dumps({
        "name": "DegenKit", "short_name": "DegenKit", "description": "No-code, non-custodial multi-chain token launcher.",
        "start_url": "/", "scope": "/", "display": "standalone", "background_color": "#0B0B0E", "theme_color": "#0B0B0E",
        "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2), encoding="utf-8")
    # sitemap: static section only; blog entries are (re)added by blog-src/build.py
    pri = {"/": ("weekly", "1.0"), "/launch/": ("weekly", "0.9"), "/launch/solana/": ("weekly", "0.9"),
           "/launch/ethereum/": ("weekly", "0.9"), "/launch/bnb/": ("weekly", "0.8"), "/launch/base/": ("weekly", "0.8"),
           "/launch/robinhood/": ("weekly", "0.8"), "/support/": ("monthly", "0.5"), "/terms/": ("yearly", "0.3"),
           "/privacy/": ("yearly", "0.3")}
    rows = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n" for u, (c, pr) in pri.items())
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}</urlset>\n', encoding="utf-8")

if __name__ == "__main__":
    for n, p in PAGES.items(): patch_page(n, p)
    write_static()
    print("SEO applied to", len(PAGES), "pages; now run: python3 blog-src/build.py")
