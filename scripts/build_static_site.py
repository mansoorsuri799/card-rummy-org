#!/usr/bin/env python3
"""Generate the cardrummy.org static HTML/CSS website (EN + Urdu)."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://cardrummy.org"
SITE = "Card Rummy"
LASTMOD = "2026-10-11"
APK_URL = "https://pkcardrummy.com/?from_gameid=6276686&channelCode=6191689"
SUPPORT_EMAIL = "support@cardrummy.org"

APP = {
    "name": "Card Rummy",
    "developer": "eriocardrummy",
    "version": "V1.231",
    "size": "49MB",
    "os": "Android 5.0+",
    "category": "Cards, Game",
    "language": "English, Urdu",
    "price": "Free",
    "downloadsLabel": "500K+",
    "ratingValue": "4.5",
    "ratingCount": "200000",
    "ratingCountLabel": "200K+",
    "updated": "1 January 2026",
}

NAV = [
    ("/", "Home", "ہوم"),
    ("/download-card-rummy/", "Download", "ڈاؤن لوڈ"),
    ("/deposit-money-in-card-rummy/", "Deposit", "ڈپازٹ"),
    ("/withdraw-money-from-card-rummy/", "Withdraw", "نکالیں"),
    ("/card-rummy-for-pc/", "PC Version", "پی سی ورژن"),
    ("/about-us/", "About Us", "ہمارے بارے"),
    ("/blog/", "Blog", "بلاگ"),
    ("/contact-us/", "Contact Us", "رابطہ"),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def asset(depth: int, path: str) -> str:
    return ("../" * depth) + path.lstrip("/")


def download_btn(depth: int, href: str | None = None) -> str:
    link = href or asset(depth, "download-card-rummy/")
    return f"""
<a class="btn-download" href="{esc(link)}">
  <span class="icon" aria-hidden="true">
    <svg viewBox="0 0 24 24"><path d="M12 3v10m0 0 4-4m-4 4-4-4M5 17v2a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-2" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </span>
  <span class="en">DOWNLOAD NOW</span>
  <span class="ur">ابھی ڈاؤن لوڈ کریں</span>
</a>"""


def header(depth: int, active: str) -> str:
    brand_href = asset(depth, "index.html") if depth == 0 else asset(depth, "")
    # Fix: for depth 0, index is ./index.html or /
    if depth == 0:
        home = "index.html"
    else:
        home = asset(depth, "index.html")

    nav_en = []
    nav_ur = []
    for href, en, ur in NAV:
        path = "index.html" if href == "/" else href.strip("/") + "/index.html"
        # simpler absolute-from-root style relative
        if href == "/":
            link = home
        else:
            link = asset(depth, href.strip("/") + "/index.html")
        cls = "active" if active == href else ""
        nav_en.append(f'<a href="{link}" class="{cls}">{esc(en)}</a>')
        nav_ur.append(f'<a href="{link}" class="{cls}">{esc(ur)}</a>')

    logo = asset(depth, "images/card-rummy.webp")
    return f"""
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{home}">
      <img src="{logo}" width="40" height="40" alt="Card Rummy logo with gold lettering and suit cards">
      <span>Card Rummy</span>
    </a>
    <nav class="nav-desktop en" aria-label="Primary">{"".join(nav_en)}</nav>
    <nav class="nav-desktop ur" aria-label="Primary">{"".join(nav_ur)}</nav>
    <div class="header-actions">
      <div class="lang-toggle" role="group" aria-label="Language">
        <button type="button" data-lang="en" aria-pressed="true">EN</button>
        <button type="button" data-lang="ur" aria-pressed="false">اردو</button>
      </div>
      <button class="menu-btn" type="button" data-menu-toggle aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu">☰</button>
    </div>
  </div>
  <div class="mobile-nav" id="mobile-nav" data-mobile-nav>
    <div class="container">
      <p class="group-label en">Main</p>
      <p class="group-label ur">مین</p>
      <div class="en">{"".join(nav_en)}</div>
      <div class="ur">{"".join(nav_ur)}</div>
      <p class="group-label en">Guides</p>
      <p class="group-label ur">گائیڈز</p>
      <a class="en" href="{asset(depth, 'privacy-policy/index.html')}">Privacy Policy</a>
      <a class="ur" href="{asset(depth, 'privacy-policy/index.html')}">پرائیویسی پالیسی</a>
      <a class="en" href="{asset(depth, 'disclaimer/index.html')}">Disclaimer</a>
      <a class="ur" href="{asset(depth, 'disclaimer/index.html')}">ڈس کلیمر</a>
      <div style="margin-top:1rem">{download_btn(depth)}</div>
    </div>
  </div>
</header>"""


def footer(depth: int) -> str:
    def l(path: str) -> str:
        if path == "/":
            return asset(depth, "index.html") if depth else "index.html"
        return asset(depth, path.strip("/") + "/index.html")

    return f"""
<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <h3>Card Rummy</h3>
      <p class="en" style="color:var(--muted);margin:0">Android guides for Pakistani players — Teen Patti, Rummy, JazzCash & EasyPaisa — on {esc(ORIGIN.replace('https://',''))}.</p>
      <p class="ur urdu-block" style="color:var(--muted);margin:0">پاکستانی کھلاڑیوں کے لیے اینڈرائیڈ گائیڈز — ٹین پتی، رمی، جازکیش اور ایزی پیسہ — {esc(ORIGIN.replace('https://',''))} پر۔</p>
      <div style="margin-top:1rem">{download_btn(depth)}</div>
    </div>
    <div>
      <h3 class="en">Quick Links</h3>
      <h3 class="ur">فوری لنکس</h3>
      <ul>
        <li><a href="{l('/')}">Home</a></li>
        <li><a href="{l('/download-card-rummy/')}">Download</a></li>
        <li><a href="{l('/deposit-money-in-card-rummy/')}">Deposit</a></li>
        <li><a href="{l('/withdraw-money-from-card-rummy/')}">Withdraw</a></li>
      </ul>
    </div>
    <div>
      <h3 class="en">Resources</h3>
      <h3 class="ur">وسائل</h3>
      <ul>
        <li><a href="{l('/card-rummy-for-pc/')}">PC Version</a></li>
        <li><a href="{l('/blog/')}">Blog</a></li>
        <li><a href="{l('/about-us/')}">About Us</a></li>
        <li><a href="{l('/contact-us/')}">Contact</a></li>
      </ul>
    </div>
    <div>
      <h3 class="en">Legal</h3>
      <h3 class="ur">قانونی</h3>
      <ul>
        <li><a href="{l('/privacy-policy/')}">Privacy Policy</a></li>
        <li><a href="{l('/disclaimer/')}">Disclaimer</a></li>
        <li><a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-note">
    <p class="en">© 2026 Card Rummy · cardrummy.org · Play responsibly. No income is guaranteed.</p>
    <p class="ur urdu-block">© 2026 کارڈ رمی · cardrummy.org · ذمہ داری سے کھیلیں۔ آمدنی کی کوئی ضمانت نہیں۔</p>
  </div>
</footer>
<script src="{asset(depth, 'js/main.js')}" defer></script>"""


def breadcrumbs(depth: int, items: list[tuple[str, str]]) -> str:
    """items: list of (label_en, href_or_empty for current)"""
    lis = []
    schema_items = []
    for i, (label, href) in enumerate(items):
        pos = i + 1
        if href:
            link = asset(depth, "index.html") if href == "/" else asset(depth, href.strip("/") + "/index.html")
            lis.append(f'<li><a href="{link}">{esc(label)}</a></li>')
            schema_items.append({"name": label, "url": ORIGIN + ("" if href == "/" else href.rstrip("/") + "/")})
        else:
            lis.append(f'<li aria-current="page">{esc(label)}</li>')
            # last url from previous pattern - caller should pass canonical
    return f"""
<nav class="breadcrumbs container" aria-label="Breadcrumb">
  <ol>{"".join(lis)}</ol>
</nav>"""


def breadcrumb_ld(items: list[tuple[str, str]]) -> dict:
    elements = []
    for i, (name, path) in enumerate(items, 1):
        if path == "/":
            url = ORIGIN + "/"
        elif path:
            url = ORIGIN + path if path.endswith("/") else ORIGIN + path + "/"
        else:
            continue
        elements.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    # fix last item - if last path empty, need full URL passed differently
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements}


def software_ld(page_path: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": APP["name"],
        "operatingSystem": "Android",
        "applicationCategory": "GameApplication",
        "downloadUrl": f"{ORIGIN}/download-card-rummy/",
        "image": f"{ORIGIN}/images/card-rummy.webp",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": APP["ratingValue"],
            "ratingCount": APP["ratingCount"],
            "bestRating": "5",
            "worstRating": "1",
        },
        "author": {"@type": "Organization", "name": APP["developer"]},
        "url": ORIGIN + page_path,
    }


def org_ld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE,
        "url": ORIGIN,
        "logo": f"{ORIGIN}/images/card-rummy.webp",
        "email": SUPPORT_EMAIL,
        "description": "Card Rummy guides for Pakistani Android players: APK download, JazzCash and EasyPaisa cash-outs, and responsible play tips in English and Urdu.",
    }


def website_ld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE,
        "url": ORIGIN,
        "inLanguage": ["en", "ur"],
        "publisher": {"@type": "Organization", "name": SITE},
    }


def faq_ld(faqs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def howto_ld(name: str, description: str, steps: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description,
        "step": [
            {"@type": "HowToStep", "position": i, "name": n, "text": t}
            for i, (n, t) in enumerate(steps, 1)
        ],
    }


def article_ld(title: str, description: str, path: str, image: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "datePublished": LASTMOD,
        "dateModified": LASTMOD,
        "author": {"@type": "Organization", "name": SITE},
        "publisher": {
            "@type": "Organization",
            "name": SITE,
            "logo": {"@type": "ImageObject", "url": f"{ORIGIN}/images/card-rummy.webp"},
        },
        "image": {
            "@type": "ImageObject",
            "url": f"{ORIGIN}/images/{image}",
            "width": 800,
            "height": 1000,
        },
        "mainEntityOfPage": ORIGIN + path,
        "inLanguage": ["en", "ur"],
    }


def page_shell(
    *,
    depth: int,
    active: str,
    title: str,
    description: str,
    canonical_path: str,
    body: str,
    schemas: list[dict],
    og_image: str = "card-rummy-og.webp",
) -> str:
    canonical = ORIGIN + canonical_path
    css = asset(depth, "css/styles.css")
    schema_tags = "\n".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
        for s in schemas
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Card Rummy">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{ORIGIN}/images/{esc(og_image)}">
<meta property="og:locale" content="en_PK">
<meta property="og:locale:alternate" content="ur_PK">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{ORIGIN}/images/{esc(og_image)}">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{asset(depth, 'images/favicon-192.webp')}" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;700&family=Noto+Nastaliq+Urdu:wght@400;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
{schema_tags}
</head>
<body class="lang-en">
{header(depth, active)}
<main id="main">
{body}
</main>
{footer(depth)}
</body>
</html>
"""


def dual(en: str, ur: str, tag: str = "p") -> str:
    return f'<{tag} class="en">{en}</{tag}>\n<{tag} class="ur urdu-block">{ur}</{tag}>'


def dual_html(en: str, ur: str) -> str:
    return f'<div class="en">{en}</div>\n<div class="ur urdu-block">{ur}</div>'


def faq_block(faqs: list[tuple[str, str, str, str]]) -> str:
    """(q_en, a_en, q_ur, a_ur)"""
    parts = ['<div class="faq">']
    for qe, ae, qu, au in faqs:
        parts.append(
            f"""<details>
<summary><span class="en">{esc(qe)}</span><span class="ur">{esc(qu)}</span></summary>
{dual(ae, au)}
</details>"""
        )
    parts.append("</div>")
    return "\n".join(parts)


def apk_table(depth: int) -> str:
    rows = [
        ("App Name", APP["name"], "ایپ کا نام"),
        ("Developer", APP["developer"], "ڈویلپر"),
        ("Category", APP["category"], "کیٹیگری"),
        ("Size", APP["size"], "سائز"),
        ("Latest Version", APP["version"], "تازہ ورژن"),
        ("Required OS", APP["os"], "ضروری سسٹم"),
        ("Update", APP["updated"], "اپ ڈیٹ"),
        ("Downloads", APP["downloadsLabel"], "ڈاؤن لوڈز"),
        ("Rating", f'{APP["ratingValue"]} ★ ({APP["ratingCountLabel"]})', "ریٹنگ"),
        ("Language", APP["language"], "زبان"),
        ("Price", f'{APP["price"]} (0$)', "قیمت"),
    ]
    trs = []
    for en_label, val, ur_label in rows:
        trs.append(
            f"<tr><th><span class='en'>{esc(en_label)}</span><span class='ur'>{esc(ur_label)}</span></th><td>{esc(val)}</td></tr>"
        )
    return f'<div class="table-wrap"><table class="apk-table"><tbody>{"".join(trs)}</tbody></table></div>'


HOME_FAQS = [
    (
        "Is Card Rummy free to download in Pakistan?",
        "Yes. The Android APK is free to install. Optional deposits via JazzCash or EasyPaisa are only needed when you choose paid tables.",
        "کیا کارڈ رمی پاکستان میں مفت ڈاؤن لوڈ ہے؟",
        "ہاں۔ اینڈرائیڈ اے پی کے مفت انسٹال ہوتی ہے۔ جازکیش یا ایزی پیسہ ڈپازٹ صرف تب چاہیے جب آپ پیسے والے ٹیبل کھیلنا چاہیں۔",
    ),
    (
        "Which payments does Card Rummy support?",
        "Most Pakistani players use JazzCash and EasyPaisa inside the wallet screens. Always confirm the in-app reference before you approve a transfer.",
        "کارڈ رمی کن ادائیگیوں کو سپورٹ کرتا ہے؟",
        "زیادہ تر کھلاڑی جازکیش اور ایزی پیسہ استعمال کرتے ہیں۔ ٹرانسفر سے پہلے ایپ کے ریفرنس کی تصدیق ضرور کریں۔",
    ),
    (
        "Is Card Rummy the same as Card Rummy - Ludo on Softonic?",
        "No. Softonic-style “Card Rummy - Ludo” listings are a different casual product. This site covers the eriocardrummy Card Rummy multi-game lobby.",
        "کیا یہ سافٹونک والی کارڈ رمی لڈو ہے؟",
        "نہیں۔ سافٹونک والی لڈو ایپ الگ پروڈکٹ ہے۔ یہاں eriocardrummy کی ملٹی گیم کارڈ رمی لابی مراد ہے۔",
    ),
    (
        "Can I play Card Rummy in Urdu?",
        "This website ships English and Urdu guides. In-app language depends on the build; follow on-screen labels if your lobby stays English.",
        "کیا میں کارڈ رمی اردو میں کھیل سکتا ہوں؟",
        "یہ ویب سائٹ انگریزی اور اردو گائیڈز دیتی ہے۔ ایپ کی زبان بلڈ پر منحصر ہے؛ اگر لابی انگریزی رہے تو اسکرین لیبلز پر چلیں۔",
    ),
]


def build_home() -> None:
    depth = 0
    crumbs_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"}],
    }
    body = f"""
<section class="hero container">
  <div class="hero-grid">
    <div>
      <p class="eyebrow en">cardrummy.org · Android · Pakistan</p>
      <p class="eyebrow ur urdu-block">cardrummy.org · اینڈرائیڈ · پاکستان</p>
      <h1 class="en">Play Card Rummy on Android with Local PKR Payouts</h1>
      <h1 class="ur urdu-block">اینڈرائیڈ پر کارڈ رمی کھیلیں اور مقامی پی کے آر ادائیگیاں حاصل کریں</h1>
      <p class="lead en">Card Rummy is a multi-game Android lobby where Pakistani players open Teen Patti, Rummy, Dragon vs Tiger, and related tables, then move funds with JazzCash or EasyPaisa. This site explains download, account binding, and cash-out steps without promising income.</p>
      <p class="lead ur urdu-block">کارڈ رمی ایک ملٹی گیم اینڈرائیڈ لابی ہے جہاں پاکستانی کھلاڑی ٹین پتی، رمی، ڈریگن بمقابلہ ٹائیگر اور متعلقہ ٹیبل کھولتے ہیں، پھر جازکیش یا ایزی پیسہ سے رقم منتقل کرتے ہیں۔ یہ سائٹ ڈاؤن لوڈ، اکاؤنٹ بائنڈنگ اور کیش آؤٹ کے مراحل بتاتی ہے — آمدنی کی ضمانت کے بغیر۔</p>
      <div class="hero-cta">
        {download_btn(depth)}
        <a class="btn-secondary en" href="deposit-money-in-card-rummy/index.html">JazzCash deposit guide</a>
        <a class="btn-secondary ur" href="deposit-money-in-card-rummy/index.html">جازکیش ڈپازٹ گائیڈ</a>
      </div>
      <div class="rating-row">
        <div class="rating-badge" aria-label="Rated 4.5 out of 5 from 200000 ratings">
          <span class="stars">★★★★☆</span>
          <strong>{APP["ratingValue"]}</strong>
          <span>({APP["ratingCountLabel"]})</span>
        </div>
        <span class="stat"><strong>Free</strong> · Android · Game</span>
        <span class="stat"><strong>{APP["size"]}</strong> · {APP["version"]}</span>
      </div>
    </div>
    <figure class="hero-visual">
      <img src="images/card-rummy.webp" width="512" height="512" alt="Card Rummy app icon with gold Rummy lettering for Pakistan Android download" fetchpriority="high">
    </figure>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Card Rummy APK details</h2>
    <h2 class="ur urdu-block">کارڈ رمی اے پی کے کی تفصیلات</h2>
    <p class="en prose">Keep this table handy when you compare the file on your phone. Matching version, size, and developer name reduces the risk of installing an unrelated “Card Rummy” clone from an app aggregator.</p>
    <p class="ur urdu-block prose">فون پر فائل کا موازنہ کرتے وقت یہ جدول سامنے رکھیں۔ ورژن، سائز اور ڈویلپر نام میل کھانے سے غلط کلون انسٹال ہونے کا خطرہ کم ہوتا ہے۔</p>
    {apk_table(depth)}
  </div>
</section>

<section class="section">
  <div class="container prose">
    <h2 class="en">How the Card Rummy lobby works in Pakistan</h2>
    <h2 class="ur urdu-block">پاکستان میں کارڈ رمی لابی کیسے کام کرتی ہے</h2>
    <p class="en">Card Rummy opens as a hub rather than a single ruleset. After login you see categories for cards, tables, and event banners. Chips fund the tables you choose; JazzCash and EasyPaisa sit behind the wallet menus when you add or remove PKR.</p>
    <p class="ur urdu-block">کارڈ رمی ایک ہب کی طرح کھلتی ہے، صرف ایک گیم نہیں۔ لاگ اِن کے بعد کارڈز، ٹیبلز اور ایونٹ بینرز نظر آتے ہیں۔ چپس آپ کے منتخب ٹیبل کو فنڈ کرتی ہیں؛ جازکیش اور ایزی پیسہ والیٹ مینو کے پیچھے ہوتے ہیں۔</p>
    <p class="en">Players who treat the first session as a systems check — install, bind, tiny deposit, tiny withdraw — understand the flow before stakes rise. That habit matters more than chasing every lobby banner on day one.</p>
    <p class="ur urdu-block">جو کھلاڑی پہلا سیشن سسٹم چیک سمجھ کر کرتے ہیں — انسٹال، بائنڈ، چھوٹا ڈپازٹ، چھوٹا نکلوانا — وہ داؤ بڑھانے سے پہلے فلو سمجھ لیتے ہیں۔</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Games inside Card Rummy worth opening first</h2>
    <h2 class="ur urdu-block">کارڈ رمی میں پہلے کھولنے والی گیمز</h2>
    <div class="grid-3" style="margin-top:1rem">
      <article class="feature"><h3 class="en">Teen Patti tables</h3><h3 class="ur">ٹین پتی</h3><p class="en">Familiar pacing for Pakistani players. Start on lower blinds while you learn the lobby timers.</p><p class="ur urdu-block">پاکستانی کھلاڑیوں کے لیے مانوس۔ لابی ٹائمر سیکھتے ہوئے کم بلائنڈز سے شروع کریں۔</p></article>
      <article class="feature"><h3 class="en">13-card Rummy</h3><h3 class="ur">۱۳ کارڈ رمی</h3><p class="en">Sequence-focused rounds that reward patience. Not the same product as casual “Rummy Ludo” store listings.</p><p class="ur urdu-block">ترتیب پر مبنی راؤنڈز۔ کیژوئل رمی لڈو اسٹور لسٹنگ سے الگ پروڈکٹ۔</p></article>
      <article class="feature"><h3 class="en">Dragon vs Tiger & quick tables</h3><h3 class="ur">ڈریگن بمقابلہ ٹائیگر</h3><p class="en">Short rounds for players who want fast results. Cap your session time before you sit.</p><p class="ur urdu-block">مختصر راؤنڈز۔ بیٹھنے سے پہلے سیشن کا وقت مقرر کریں۔</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Bonuses that actually change a first session</h2>
    <h2 class="ur urdu-block">وہ بونس جو پہلے سیشن میں فرق لاتے ہیں</h2>
    <div class="prose">
      <p class="en">Welcome chips, daily login rewards, and recharge rebates appear early. Read each offer sheet for minimum deposit and game eligibility before you celebrate the banner art. A clear small bonus beats a large one you cannot withdraw under the rules.</p>
      <p class="ur urdu-block">ویلکم چپس، ڈیلی لاگ اِن اور ریچارج ریبیت جلدی نظر آتے ہیں۔ بینر دیکھ کر خوش ہونے سے پہلے کم از کم ڈپازٹ اور گیم اہلیت پڑھیں۔</p>
      <p class="en">For a week-one claim order, read our <a href="blog/card-rummy-bonuses-first-week/index.html">bonus planning article</a>. Deposit mechanics stay on the <a href="deposit-money-in-card-rummy/index.html">deposit guide</a>.</p>
      <p class="ur urdu-block">پہلے ہفتے کا پلان <a href="blog/card-rummy-bonuses-first-week/index.html">بونس آرٹیکل</a> میں ہے۔ ڈپازٹ کے مراحل <a href="deposit-money-in-card-rummy/index.html">ڈپازٹ گائیڈ</a> پر ہیں۔</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Download and install the latest Android build</h2>
    <h2 class="ur urdu-block">تازہ اینڈرائیڈ بلڈ ڈاؤن لوڈ اور انسٹال کریں</h2>
    <div class="prose">
      <p class="en">Use the on-site <a href="download-card-rummy/index.html">Card Rummy download page</a> so you see version notes and affiliate disclosure in one place. Allow installs only for the browser or Files app that fetched the APK, then disable unknown sources again.</p>
      <p class="ur urdu-block"><a href="download-card-rummy/index.html">ڈاؤن لوڈ صفحہ</a> استعمال کریں تاکہ ورژن نوٹس اور افیلی ایٹ وضاحت ایک جگہ ملیں۔ صرف اسی براؤزر/فائلز کو اجازت دیں جس نے اے پی کے لی، پھر ان نان سورسز بند کر دیں۔</p>
    </div>
    <div class="cta-band">
      <div>
        <strong class="en">Ready for the APK steps?</strong>
        <strong class="ur">اے پی کے مراحل کے لیے تیار؟</strong>
        <p class="en" style="margin:0.3rem 0 0;color:var(--muted)">Full install walkthrough with HowTo markup.</p>
        <p class="ur urdu-block" style="margin:0.3rem 0 0;color:var(--muted)">مکمل انسٹال گائیڈ HowTo مارک اپ کے ساتھ۔</p>
      </div>
      {download_btn(depth)}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Register, login, and bind your account</h2>
    <h2 class="ur urdu-block">رجسٹر، لاگ اِن اور اکاؤنٹ بائنڈ کریں</h2>
    <div class="prose">
      <p class="en">Guest mode is fine for browsing tiles. Withdrawals and referrals need a registered profile with OTP and, when offered, bound email. Fix OTP stalls and bind issues in our <a href="blog/card-rummy-login-otp-bind-email-fixes/index.html">login guide</a>.</p>
      <p class="ur urdu-block">گیسٹ موڈ دیکھنے کے لیے ٹھیک ہے۔ نکلوانے اور ریفرل کے لیے OTP والا رجسٹرڈ پروفائل اور بائنڈ ای میل چاہیے۔ مسائل کے لیے <a href="blog/card-rummy-login-otp-bind-email-fixes/index.html">لاگ اِن گائیڈ</a> دیکھیں۔</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Deposit and withdraw with JazzCash or EasyPaisa</h2>
    <h2 class="ur urdu-block">جازکیش یا ایزی پیسہ سے ڈپازٹ اور نکلوائیں</h2>
    <div class="grid-2" style="margin-top:1rem">
      <a class="feature" href="deposit-money-in-card-rummy/index.html" style="color:inherit">
        <h3 class="en">Deposit guide</h3><h3 class="ur">ڈپازٹ گائیڈ</h3>
        <p class="en">Small test top-ups, reference IDs, and what to screenshot when a balance is slow to update.</p>
        <p class="ur urdu-block">چھوٹا ٹیسٹ ٹاپ اپ، ریفرنس آئی ڈی، اور بیلنس دیر سے آئے تو کیا اسکرین شاٹ لیں۔</p>
      </a>
      <a class="feature" href="withdraw-money-from-card-rummy/index.html" style="color:inherit">
        <h3 class="en">Withdraw guide</h3><h3 class="ur">نکلوانے کی گائیڈ</h3>
        <p class="en">Wallet binding, minimum cash-out checks, and patience rules while EasyPaisa or JazzCash processes PKR.</p>
        <p class="ur urdu-block">والیٹ بائنڈنگ، کم از کم کیش آؤٹ، اور پروسیسنگ کے دوران صبر کے اصول۔</p>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Card Rummy screens you will recognize</h2>
    <h2 class="ur urdu-block">کارڈ رمی کی وہ اسکرینز جو آپ پہچانیں گے</h2>
    <div class="shot-grid" style="margin-top:1rem">
      <figure class="shot">
        <a class="shot-link" href="images/card-rummy-game-interface.webp" data-lightbox data-caption-en="Lobby interface" data-caption-ur="لابی">
          <img src="images/card-rummy-game-interface.webp" width="1200" height="560" alt="Card Rummy game lobby interface on Android" loading="lazy">
          <figcaption><span class="en">Lobby interface</span><span class="ur">لابی</span><span class="hint en">Click to enlarge</span><span class="hint ur">بڑا دیکھیں</span></figcaption>
        </a>
      </figure>
      <figure class="shot">
        <a class="shot-link" href="images/card-rummy-games.webp" data-lightbox data-caption-en="Games collection" data-caption-ur="گیمز">
          <img src="images/card-rummy-games.webp" width="1200" height="560" alt="Card Rummy games collection tiles" loading="lazy">
          <figcaption><span class="en">Games collection</span><span class="ur">گیمز</span><span class="hint en">Click to enlarge</span><span class="hint ur">بڑا دیکھیں</span></figcaption>
        </a>
      </figure>
      <figure class="shot">
        <a class="shot-link" href="images/card-rummy-earn-bonus.webp" data-lightbox data-caption-en="Bonuses" data-caption-ur="بونس">
          <img src="images/card-rummy-earn-bonus.webp" width="1200" height="560" alt="Card Rummy bonuses and rewards screen" loading="lazy">
          <figcaption><span class="en">Bonuses</span><span class="ur">بونس</span><span class="hint en">Click to enlarge</span><span class="hint ur">بڑا دیکھیں</span></figcaption>
        </a>
      </figure>
      <figure class="shot">
        <a class="shot-link" href="images/card-rummy-add-money.webp" data-lightbox data-caption-en="Add money" data-caption-ur="پیسے شامل">
          <img src="images/card-rummy-add-money.webp" width="1200" height="560" alt="Card Rummy add money deposit screen" loading="lazy">
          <figcaption><span class="en">Add money</span><span class="ur">پیسے شامل</span><span class="hint en">Click to enlarge</span><span class="hint ur">بڑا دیکھیں</span></figcaption>
        </a>
      </figure>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Fix common install and IP exceed errors</h2>
    <h2 class="ur urdu-block">عام انسٹال اور IP Exceed مسائل ٹھیک کریں</h2>
    <div class="prose">
      <p class="en">Shared Wi-Fi, VPNs, and repeated guest accounts often trigger IP exceed locks. Install failures usually mean unknown-sources permission, storage space, or a mismatched APK signature. Work through the dedicated <a href="blog/card-rummy-ip-exceed-install-fix/index.html">troubleshooting article</a>.</p>
      <p class="ur urdu-block">شیئرڈ وائی فائی، وی پی این اور بار بار گیسٹ اکاؤنٹ IP exceed پیدا کر سکتے ہیں۔ انسٹال فیل ہونے پر پرمیشن، اسٹوریج یا دستخط چیک کریں۔ تفصیل <a href="blog/card-rummy-ip-exceed-install-fix/index.html">ٹربل شوٹنگ آرٹیکل</a> میں ہے۔</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Practical tips without guaranteed-win claims</h2>
    <h2 class="ur urdu-block">عملی ٹپس — جیت کی ضمانت کے بغیر</h2>
    <ul class="list-check en">
      <li>Set a weekly PKR entertainment limit before you open JazzCash.</li>
      <li>Leave when the limit hits — bonuses are not a reason to stretch funds.</li>
      <li>Prefer bound accounts over guest profiles once money is involved.</li>
      <li>Learn one game’s pacing before hopping across every tile in the lobby.</li>
    </ul>
    <ul class="list-check ur urdu-block">
      <li>جازکیش کھولنے سے پہلے ہفتہ وار پی کے آر حد لکھ لیں۔</li>
      <li>حد پوری ہو تو رک جائیں — بونس فنڈ کھینچنے کی وجہ نہیں۔</li>
      <li>پیسے کے بعد گیسٹ کے بجائے بائنڈ اکاؤنٹ رکھیں۔</li>
      <li>ہر ٹائل پر جانے سے پہلے ایک گیم کا بہاؤ سیکھیں۔</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Pros and cons in plain English</h2>
    <h2 class="ur urdu-block">فوائد اور نقصانات سادہ زبان میں</h2>
    <div class="pros-cons" style="margin-top:1rem">
      <div class="panel">
        <h3 class="en">Pros</h3><h3 class="ur">فوائد</h3>
        <ul class="list-check en"><li>Local wallet rails many Pakistanis already use</li><li>Multiple card and quick tables in one APK</li><li>Free install with optional deposits</li></ul>
        <ul class="list-check ur urdu-block"><li>مقامی والیٹ جو بہت سے لوگ استعمال کرتے ہیں</li><li>ایک اے پی کے میں کئی ٹیبلز</li><li>مفت انسٹال، ڈپازٹ اختیاری</li></ul>
      </div>
      <div class="panel cons">
        <h3 class="en">Cons</h3><h3 class="ur">نقصانات</h3>
        <ul class="list-check en"><li>Real-money play can lose funds quickly</li><li>APK installs need careful source checks</li><li>Network locks can interrupt logins</li></ul>
        <ul class="list-check ur urdu-block"><li>حقیقی رقم جلدی ہار بھی سکتے ہیں</li><li>اے پی کے ماخذ احتیاط سے چیک کریں</li><li>نیٹ ورک لاک لاگ اِن روک سکتا ہے</li></ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <h2 class="en">Safety notes before you deposit</h2>
    <h2 class="ur urdu-block">ڈپازٹ سے پہلے حفاظتی نوٹس</h2>
    <p class="en">Never share JazzCash or EasyPaisa OTPs with anyone claiming to be support in chat groups. Read our <a href="blog/is-card-rummy-safe-for-pakistan-players/index.html">Pakistan safety checklist</a> before the first top-up. Real-money gaming can be restricted depending on your situation — this site is educational, not legal advice.</p>
    <p class="ur urdu-block">چیٹ گروپس میں سپورٹ بن کر OTP نہ مانگیں۔ پہلے ٹاپ اپ سے پہلے <a href="blog/is-card-rummy-safe-for-pakistan-players/index.html">سیفٹی چیک لسٹ</a> پڑھیں۔ حقیقی رقم والی گیمنگ آپ کی صورت پر منحصر ہو سکتی ہے — یہ سائٹ تعلیمی ہے، قانونی مشورہ نہیں۔</p>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <h2 class="en">Customer support options</h2>
    <h2 class="ur urdu-block">کسٹمر سپورٹ کے اختیارات</h2>
    <p class="en">Prefer the in-app help icon for account-specific errors so agents see your user ID. For website questions about these guides, email <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a> via our <a href="contact-us/index.html">contact page</a>.</p>
    <p class="ur urdu-block">اکاؤنٹ مسائل کے لیے ایپ کے ہیلپ آئیکن کو ترجیح دیں۔ ان گائیڈز کے بارے میں <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a> یا <a href="contact-us/index.html">رابطہ صفحہ</a> استعمال کریں۔</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="en">Frequently asked questions</h2>
    <h2 class="ur urdu-block">عمومی سوالات</h2>
    {faq_block(HOME_FAQS)}
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="cta-band">
      <div class="prose" style="margin:0">
        <h2 class="en" style="margin:0">Start with a careful Card Rummy install</h2>
        <h2 class="ur urdu-block" style="margin:0">احتیاط سے کارڈ رمی انسٹال کریں</h2>
        <p class="en" style="margin:0.4rem 0 0">Download on-domain, bind the account, then test wallets with small PKR amounts.</p>
        <p class="ur urdu-block" style="margin:0.4rem 0 0">سائٹ سے ڈاؤن لوڈ کریں، اکاؤنٹ بائنڈ کریں، پھر چھوٹی رقم سے والیٹ ٹیسٹ کریں۔</p>
      </div>
      {download_btn(depth)}
    </div>
  </div>
</section>
"""
    html_out = page_shell(
        depth=depth,
        active="/",
        title="Card Rummy APK Pakistan – Download & JazzCash Guide",
        description="Download Card Rummy APK for Pakistan with English & Urdu guides. Learn JazzCash and EasyPaisa deposit, withdraw, and safe Android install steps on cardrummy.org.",
        canonical_path="/",
        body=body,
        schemas=[website_ld(), org_ld(), software_ld("/"), faq_ld([(a[0], a[1]) for a in HOME_FAQS])],
    )
    (ROOT / "index.html").write_text(html_out, encoding="utf-8")
    print("wrote index.html")


def crumbs_html(depth: int, trail: list[tuple[str, str | None]]) -> str:
    """trail: (label, path or None for current). path '/' or '/foo/' """
    lis = []
    for label, path in trail:
        if path is None:
            lis.append(f'<li aria-current="page">{esc(label)}</li>')
        elif path == "/":
            link = asset(depth, "index.html") if depth else "index.html"
            lis.append(f'<li><a href="{link}">{esc(label)}</a></li>')
        else:
            link = asset(depth, path.strip("/") + "/index.html")
            lis.append(f'<li><a href="{link}">{esc(label)}</a></li>')
    return f'<nav class="breadcrumbs container" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def crumbs_ld(trail: list[tuple[str, str]]) -> dict:
    """All items including current with full path strings."""
    elements = []
    for i, (name, path) in enumerate(trail, 1):
        url = ORIGIN + "/" if path == "/" else ORIGIN + path
        elements.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements}


def write_page(rel_dir: str, filename: str, html_out: str) -> None:
    path = ROOT / rel_dir if rel_dir else ROOT
    path.mkdir(parents=True, exist_ok=True)
    (path / filename).write_text(html_out, encoding="utf-8")
    print("wrote", (path / filename).relative_to(ROOT))


def build_download() -> None:
    depth = 1
    steps = [
        ("Open the Card Rummy download page", "Stay on cardrummy.org so version notes and disclosure stay visible."),
        ("Start the APK download", "Tap the download button. If an affiliate endpoint opens, it is disclosed on this page."),
        ("Allow install permission once", "Enable unknown apps only for the browser or Files app that fetched the package."),
        ("Install and verify details", "Confirm developer eriocardrummy, size near 49MB, and version V1.231 before first login."),
        ("Disable unknown sources again", "Turn the permission off after install to reduce later risk."),
    ]
    steps_ur = [
        ("کارڈ رمی ڈاؤن لوڈ صفحہ کھولیں", "cardrummy.org پر رہیں تاکہ ورژن نوٹس اور وضاحت نظر آئیں۔"),
        ("اے پی کے ڈاؤن لوڈ شروع کریں", "بٹن دبائیں۔ اگر افیلی ایٹ لنک کھلے تو اس صفحے پر اس کی وضاحت موجود ہے۔"),
        ("ایک بار انسٹال اجازت دیں", "صرف اسی براؤزر یا فائلز کو اجازت دیں جس نے فائل لی۔"),
        ("انسٹال کر کے تفصیل چیک کریں", "ڈویلپر، سائز تقریباً 49MB اور ورژن V1.231 کی تصدیق کریں۔"),
        ("ان نان سورسز دوبارہ بند کریں", "انسٹال کے بعد اجازت بند کر دیں۔"),
    ]
    faqs = [
        (
            "Where should I download Card Rummy from?",
            "Start on this cardrummy.org download guide. Avoid random Telegram forwards that skip version checks.",
            "کارڈ رمی کہاں سے ڈاؤن لوڈ کریں؟",
            "اس cardrummy.org گائیڈ سے شروع کریں۔ بغیر ورژن چیک کے بے ترتیب ٹیلیگرام لنکس سے بچیں۔",
        ),
        (
            "Why does Android warn about unknown apps?",
            "Sideloaded APKs are not Play Store installs. The warning is normal — grant permission only to the app that downloaded the file.",
            "اینڈرائیڈ ان نان ایپس کی وارننگ کیوں دیتا ہے؟",
            "سائیڈ لوڈ پلے اسٹور نہیں۔ وارننگ عام ہے — اجازت صرف ڈاؤن لوڈ کرنے والی ایپ کو دیں۔",
        ),
    ]
    step_html = ['<div class="steps">']
    for (ne, te), (nu, tu) in zip(steps, steps_ur):
        step_html.append(
            f'<div class="step"><div><h3 class="en">{esc(ne)}</h3><h3 class="ur">{esc(nu)}</h3>'
            f'<p class="en">{esc(te)}</p><p class="ur urdu-block">{esc(tu)}</p></div></div>'
        )
    step_html.append("</div>")

    body = f"""
{crumbs_html(depth, [("Home", "/"), ("Download Card Rummy", None)])}
<section class="hero container">
  <h1 class="en">Download Card Rummy APK for Android in Pakistan</h1>
  <h1 class="ur urdu-block">پاکستان میں اینڈرائیڈ کے لیے کارڈ رمی اے پی کے ڈاؤن لوڈ کریں</h1>
  <p class="lead en">Install the latest Card Rummy build with clear version checks, English and Urdu steps, and an honest note when an affiliate download endpoint is used.</p>
  <p class="lead ur urdu-block">تازہ کارڈ رمی بلڈ انسٹال کریں — ورژن چیک، انگریزی و اردو مراحل، اور افیلی ایٹ ڈاؤن لوڈ کی کھلی وضاحت کے ساتھ۔</p>
  <div class="hero-cta">
    <a class="btn-download" href="{esc(APK_URL)}" rel="noopener sponsored">
      <span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3v10m0 0 4-4m-4 4-4-4M5 17v2a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-2" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <span class="en">DOWNLOAD NOW</span><span class="ur">ابھی ڈاؤن لوڈ کریں</span>
    </a>
  </div>
  <p class="disclose en">Affiliate disclosure: the download button may open a partner APK endpoint used to track installs. You remain on this guide for instructions; we do not hide the destination.</p>
  <p class="disclose ur urdu-block">افیلی ایٹ وضاحت: ڈاؤن لوڈ بٹن پارٹنر اے پی کے لنک کھول سکتا ہے جو انسٹالز ٹریک کرتا ہے۔ ہدایات اسی گائیڈ پر رہتی ہیں؛ منزل چھپائی نہیں جاتی۔</p>
  <div class="rating-row">
    <div class="rating-badge"><span class="stars">★★★★☆</span><strong>{APP["ratingValue"]}</strong><span>({APP["ratingCountLabel"]})</span></div>
    <span class="stat">Free · Android · Game · {APP["version"]} · {APP["size"]}</span>
  </div>
</section>
<section class="section"><div class="container"><h2 class="en">APK facts to verify</h2><h2 class="ur urdu-block">تصدیق کے لیے اے پی کے حقائق</h2>{apk_table(depth)}</div></section>
<section class="section"><div class="container"><h2 class="en">Installation steps</h2><h2 class="ur urdu-block">انسٹال کے مراحل</h2>{''.join(step_html)}</div></section>
<section class="section"><div class="container prose">
  <h2 class="en">After install</h2><h2 class="ur urdu-block">انسٹال کے بعد</h2>
  <p class="en">Register with OTP, bind email when available, then follow the <a href="{asset(depth, 'deposit-money-in-card-rummy/index.html')}">deposit guide</a> only with a budgeted amount. Stuck on IP exceed? Read the <a href="{asset(depth, 'blog/card-rummy-ip-exceed-install-fix/index.html')}">fix article</a>.</p>
  <p class="ur urdu-block">OTP سے رجسٹر کریں، ای میل بائنڈ کریں، پھر بجٹ کے ساتھ <a href="{asset(depth, 'deposit-money-in-card-rummy/index.html')}">ڈپازٹ گائیڈ</a> دیکھیں۔ IP exceed ہو تو <a href="{asset(depth, 'blog/card-rummy-ip-exceed-install-fix/index.html')}">فکس آرٹیکل</a> پڑھیں۔</p>
</div></section>
<section class="section"><div class="container"><h2 class="en">Download FAQs</h2><h2 class="ur urdu-block">ڈاؤن لوڈ سوالات</h2>{faq_block(faqs)}</div></section>
"""
    html_out = page_shell(
        depth=depth,
        active="/download-card-rummy/",
        title="Download Card Rummy APK Android – Official Guide",
        description="Download Card Rummy APK for Android in Pakistan. Verify V1.231, 49MB, eriocardrummy, and install safely with English & Urdu steps on cardrummy.org.",
        canonical_path="/download-card-rummy/",
        body=body,
        schemas=[
            crumbs_ld([("Home", "/"), ("Download Card Rummy", "/download-card-rummy/")]),
            software_ld("/download-card-rummy/"),
            howto_ld(
                "How to download and install Card Rummy APK",
                "Install Card Rummy on Android with version checks for Pakistani players.",
                steps,
            ),
            faq_ld([(f[0], f[1]) for f in faqs]),
        ],
    )
    write_page("download-card-rummy", "index.html", html_out)


def build_deposit() -> None:
    depth = 1
    steps = [
        ("Open Wallet inside Card Rummy", "Use your registered account, not a disposable guest profile."),
        ("Choose JazzCash or EasyPaisa", "Select the wallet you control and can receive OTPs for."),
        ("Enter a small test amount first", "Confirm the reference ID and screenshot the success screen."),
        ("Verify chips after the payment clears", "If balance is late, wait a few minutes before retrying the same amount."),
        ("Only then scale deposits", "Increase size after a successful round-trip test, never before."),
    ]
    faqs = [
        (
            "What is a safe first Card Rummy deposit?",
            "Use the smallest amount that still unlocks the payment method you need. Confirm the wallet name matches your own JazzCash or EasyPaisa account.",
            "پہلا محفوظ ڈپازٹ کتنا ہو؟",
            "اتنی چھوٹی رقم جتنی ادائیگی کا طریقہ کھول دے۔ والیٹ نام اپنا جازکیش یا ایزی پیسہ ہونا چاہیے۔",
        ),
        (
            "Deposit succeeded but chips did not arrive?",
            "Keep the order ID, wait briefly, then contact in-app support the same day. Do not send money to personal numbers outside the app.",
            "ڈپازٹ ہو گیا مگر چپس نہیں آئیں؟",
            "آرڈر آئی ڈی رکھیں، تھوڑا انتظار کریں، اسی دن ایپ سپورٹ سے رابطہ کریں۔ ایپ سے باہر ذاتی نمبر پر رقم نہ بھیجیں۔",
        ),
    ]
    step_html = '<div class="steps">' + "".join(
        f'<div class="step"><div><h3>{esc(n)}</h3><p>{esc(t)}</p></div></div>' for n, t in steps
    ) + "</div>"
    body = f"""
{crumbs_html(depth, [("Home", "/"), ("Deposit Money", None)])}
<section class="hero container">
  <h1 class="en">Deposit Money in Card Rummy with JazzCash & EasyPaisa</h1>
  <h1 class="ur urdu-block">جازکیش اور ایزی پیسہ سے کارڈ رمی میں ڈپازٹ کریں</h1>
  <p class="lead en">Add PKR to Card Rummy using the wallets Pakistani players already trust — with a small test payment before larger top-ups.</p>
  <p class="lead ur urdu-block">پاکستانی کھلاڑیوں کے مانوس والیٹس سے کارڈ رمی میں پی کے آر شامل کریں — بڑے ٹاپ اپ سے پہلے چھوٹا ٹیسٹ ضرور کریں۔</p>
  <div class="hero-cta">{download_btn(depth)}</div>
</section>
<section class="section"><div class="container"><h2 class="en">Deposit steps</h2><h2 class="ur urdu-block">ڈپازٹ کے مراحل</h2>{step_html}
<p class="en" style="color:var(--muted);margin-top:1rem">اردو خلاصہ: رجسٹرڈ اکاؤنٹ میں والیٹ کھولیں، جازکیش یا ایزی پیسہ چنیں، چھوٹی رقم بھیجیں، ریفرنس محفوظ کریں، بیلنس چیک کریں۔</p>
</div></section>
<section class="section"><div class="container prose">
  <h2 class="en">Payment methods Pakistani players use</h2>
  <h2 class="ur urdu-block">پاکستانی کھلاڑی کون سی ادائیگی استعمال کرتے ہیں</h2>
  <p class="en">JazzCash and EasyPaisa cover most successful first deposits. Banking options may appear depending on the build. Never pay a stranger’s personal wallet because a chat admin “accelerates” your chips.</p>
  <p class="ur urdu-block">جازکیش اور ایزی پیسہ عام ہیں۔ بینکنگ بلڈ پر منحصر ہو سکتی ہے۔ چیٹ ایڈمن کے کہنے پر اجنبی کے والیٹ میں رقم نہ بھیجیں۔</p>
  <p class="en">When you are ready to cash out later, use the <a href="{asset(depth, 'withdraw-money-from-card-rummy/index.html')}">withdraw guide</a> instead of repeating steps here.</p>
  <p class="ur urdu-block">بعد میں نکلوانے کے لیے <a href="{asset(depth, 'withdraw-money-from-card-rummy/index.html')}">نکلوانے کی گائیڈ</a> دیکھیں۔</p>
</div></section>
<section class="section"><div class="container"><h2 class="en">Deposit FAQs</h2><h2 class="ur urdu-block">ڈپازٹ سوالات</h2>{faq_block(faqs)}</div></section>
"""
    html_out = page_shell(
        depth=depth,
        active="/deposit-money-in-card-rummy/",
        title="Deposit in Card Rummy – JazzCash & EasyPaisa",
        description="How to deposit money in Card Rummy with JazzCash and EasyPaisa in Pakistan. Small test payments, reference IDs, and English & Urdu steps.",
        canonical_path="/deposit-money-in-card-rummy/",
        body=body,
        schemas=[
            crumbs_ld([("Home", "/"), ("Deposit Money", "/deposit-money-in-card-rummy/")]),
            howto_ld("How to deposit money in Card Rummy", "JazzCash and EasyPaisa deposit steps for Card Rummy.", steps),
            faq_ld([(f[0], f[1]) for f in faqs]),
        ],
    )
    write_page("deposit-money-in-card-rummy", "index.html", html_out)


def build_withdraw() -> None:
    depth = 1
    steps = [
        ("Bind a wallet you control", "Withdraw only to your own JazzCash or EasyPaisa number."),
        ("Check minimum cash-out and fees", "Read the on-screen minimum before you submit."),
        ("Request a modest first withdrawal", "Prove the path works before moving larger balances."),
        ("Keep the request ID", "Screenshot pending and success states for support."),
        ("Wait through normal processing", "Avoid re-submitting the same amount repeatedly in one hour."),
    ]
    faqs = [
        (
            "How long do Card Rummy withdrawals take?",
            "Timing varies by wallet load and review checks. Start with a small cash-out so you learn the real pacing on your account.",
            "نکلوانے میں کتنا وقت لگتا ہے؟",
            "والیٹ لوڈ اور ریویو پر منحصر ہے۔ پہلے چھوٹی رقم نکال کر اپنے اکاؤنٹ کا اصل وقت سیکھیں۔",
        ),
        (
            "Can I withdraw bonuses immediately?",
            "Some rewards need wagering or eligible games first. Read the offer sheet before you assume chips are withdrawable.",
            "کیا بونس فوراً نکلوا سکتے ہیں؟",
            "کچھ انعامات پر شرط یا مخصوص گیمز لازم ہو سکتی ہیں۔ پہلے آفر شیٹ پڑھیں۔",
        ),
    ]
    step_html = '<div class="steps">' + "".join(
        f'<div class="step"><div><h3>{esc(n)}</h3><p>{esc(t)}</p></div></div>' for n, t in steps
    ) + "</div>"
    body = f"""
{crumbs_html(depth, [("Home", "/"), ("Withdraw Money", None)])}
<section class="hero container">
  <h1 class="en">Withdraw Money from Card Rummy to Local Wallets</h1>
  <h1 class="ur urdu-block">کارڈ رمی سے مقامی والیٹس میں رقم نکلوائیں</h1>
  <p class="lead en">Move PKR from Card Rummy to JazzCash or EasyPaisa with bound wallets, modest first cash-outs, and clear records for support.</p>
  <p class="lead ur urdu-block">باؤنڈ والیٹ، پہلی چھوٹی کیش آؤٹ، اور سپورٹ کے لیے ریکارڈ کے ساتھ کارڈ رمی سے جازکیش یا ایزی پیسہ میں پی کے آر منتقل کریں۔</p>
  <div class="hero-cta">{download_btn(depth)}</div>
</section>
<section class="section"><div class="container"><h2 class="en">Withdrawal steps</h2><h2 class="ur urdu-block">نکلوانے کے مراحل</h2>{step_html}
<p class="ur urdu-block" style="color:var(--muted)">مختصر اردو: اپنا والیٹ بائنڈ کریں، کم از کم حد پڑھیں، پہلی چھوٹی درخواست بھیجیں، آئی ڈی محفوظ رکھیں، بار بار دوبارہ نہ بھیجیں۔</p>
</div></section>
<section class="section"><div class="container prose">
  <h2 class="en">Before you cash out</h2><h2 class="ur urdu-block">کیش آؤٹ سے پہلے</h2>
  <p class="en">Finish account binding and confirm deposits landed under the same profile. If login is locked, fix that via the <a href="{asset(depth, 'blog/card-rummy-ip-exceed-install-fix/index.html')}">IP exceed guide</a> before opening a ticket about missing funds.</p>
  <p class="ur urdu-block">بائنڈنگ مکمل کریں اور ڈپازٹ اسی پروفائل میں چیک کریں۔ لاگ اِن لاک ہو تو فنڈز کی ٹکٹ سے پہلے <a href="{asset(depth, 'blog/card-rummy-ip-exceed-install-fix/index.html')}">IP گائیڈ</a> دیکھیں۔</p>
</div></section>
<section class="section"><div class="container"><h2 class="en">Withdraw FAQs</h2><h2 class="ur urdu-block">نکلوانے کے سوالات</h2>{faq_block(faqs)}</div></section>
"""
    html_out = page_shell(
        depth=depth,
        active="/withdraw-money-from-card-rummy/",
        title="Withdraw from Card Rummy – JazzCash Guide",
        description="Withdraw money from Card Rummy to JazzCash or EasyPaisa. Bound wallets, first cash-out checks, and English & Urdu help on cardrummy.org.",
        canonical_path="/withdraw-money-from-card-rummy/",
        body=body,
        schemas=[
            crumbs_ld([("Home", "/"), ("Withdraw Money", "/withdraw-money-from-card-rummy/")]),
            howto_ld("How to withdraw money from Card Rummy", "Cash out Card Rummy balance to JazzCash or EasyPaisa.", steps),
            faq_ld([(f[0], f[1]) for f in faqs]),
        ],
    )
    write_page("withdraw-money-from-card-rummy", "index.html", html_out)


def build_pc() -> None:
    depth = 1
    steps = [
        ("Install a reputable Android emulator on Windows or macOS", "Download the emulator from its official site, not a bundled crack."),
        ("Create a virtual Android device with Google services if required", "Allocate enough RAM so Card Rummy tables stay smooth."),
        ("Install the same APK you verified on phone", "Use the build from our download guide — do not mix random APK signatures."),
        ("Log in with your bound account", "Expect a security check if the emulator IP differs from your phone."),
        ("Keep deposits modest on first emulator sessions", "Confirm controls and network stability before larger play."),
    ]
    body = f"""
{crumbs_html(depth, [("Home", "/"), ("Card Rummy for PC", None)])}
<section class="hero container">
  <h1 class="en">Card Rummy for PC via Android Emulator</h1>
  <h1 class="ur urdu-block">اینڈرائیڈ ایمولیٹر کے ذریعے پی سی پر کارڈ رمی</h1>
  <p class="lead en">Card Rummy ships as an Android APK. On Windows or macOS you play through an emulator using the same verified package and bound account.</p>
  <p class="lead ur urdu-block">کارڈ رمی اینڈرائیڈ اے پی کے ہے۔ ونڈوز یا میک پر تصدیق شدہ پیکج اور باؤنڈ اکاؤنٹ کے ساتھ ایمولیٹر سے کھیلیں۔</p>
  <div class="hero-cta">{download_btn(depth)}</div>
</section>
<section class="section"><div class="container"><h2 class="en">PC setup steps</h2><h2 class="ur urdu-block">پی سی سیٹ اپ</h2>
<div class="steps">{"".join(f'<div class="step"><div><h3>{esc(n)}</h3><p>{esc(t)}</p></div></div>' for n,t in steps)}</div>
<p class="ur urdu-block" style="color:var(--muted);margin-top:1rem">اردو: رسمی ایمولیٹر لگائیں، ورچوئل ڈیوائس بنائیں، وہی اے پی کے انسٹال کریں، باؤنڈ اکاؤنٹ سے لاگ اِن کریں، پہلے سیشن میں کم ڈپازٹ رکھیں۔</p>
</div></section>
<section class="section"><div class="container prose">
  <h2 class="en">PC tips</h2><h2 class="ur urdu-block">پی سی ٹپس</h2>
  <p class="en">Emulator IPs trigger security gates more often than mobile data. Bind email first. Prefer mouse click accuracy on rummy tables and keep the laptop cooler during long sessions.</p>
  <p class="ur urdu-block">ایمولیٹر IP فون سے زیادہ سیکیورٹی چیک کھولتا ہے۔ پہلے ای میل بائنڈ کریں۔ لمبے سیشن میں لیپ ٹاپ ٹھنڈا رکھیں۔</p>
</div></section>
"""
    html_out = page_shell(
        depth=depth,
        active="/card-rummy-for-pc/",
        title="Card Rummy for PC – Emulator Download Guide",
        description="Play Card Rummy on PC with an Android emulator. English & Urdu setup steps using the same verified APK as mobile.",
        canonical_path="/card-rummy-for-pc/",
        body=body,
        schemas=[
            crumbs_ld([("Home", "/"), ("Card Rummy for PC", "/card-rummy-for-pc/")]),
            howto_ld("How to play Card Rummy on PC", "Use an Android emulator to run Card Rummy on computer.", steps),
        ],
    )
    write_page("card-rummy-for-pc", "index.html", html_out)


def build_about() -> None:
    depth = 1
    body = f"""
{crumbs_html(depth, [("Home", "/"), ("About Us", None)])}
<section class="hero container">
  <h1 class="en">About Card Rummy on cardrummy.org</h1>
  <h1 class="ur urdu-block">cardrummy.org پر کارڈ رمی کے بارے میں</h1>
</section>
<section class="section"><div class="container prose">
  <p class="en">cardrummy.org publishes practical English and Urdu guides for the Card Rummy Android lobby used in Pakistan. We focus on install hygiene, JazzCash and EasyPaisa flows, account binding, and responsible play — not income promises.</p>
  <p class="ur urdu-block">cardrummy.org پاکستان میں استعمال ہونے والی کارڈ رمی اینڈرائیڈ لابی کے لیے انگریزی اور اردو گائیڈز شائع کرتا ہے۔ ہمارا زور انسٹال احتیاط، جازکیش/ایزی پیسہ، اکاؤنٹ بائنڈنگ اور ذمہ دار کھیل پر ہے — آمدنی کے وعدوں پر نہیں۔</p>
  <p class="en">We are an independent information site. App features and payment screens can change with new builds; when they do, we update these pages and the sitemap lastmod dates.</p>
  <p class="ur urdu-block">ہم ایک آزاد معلومات کی سائٹ ہیں۔ ایپ کی خصوصیات بدل سکتی ہیں؛ تبدیلی پر صفحات اور سائٹ میپ کی تاریخیں اپ ڈیٹ کرتے ہیں۔</p>
  <p class="en">Contact: <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>
</div></section>
"""
    html_out = page_shell(
        depth=depth,
        active="/about-us/",
        title="About Us – Card Rummy Guides Pakistan",
        description="About cardrummy.org: English and Urdu Card Rummy guides for Pakistani Android players, focused on safe install and local payments.",
        canonical_path="/about-us/",
        body=body,
        schemas=[crumbs_ld([("Home", "/"), ("About Us", "/about-us/")]), org_ld()],
    )
    write_page("about-us", "index.html", html_out)


def build_contact() -> None:
    depth = 1
    body = f"""
{crumbs_html(depth, [("Home", "/"), ("Contact Us", None)])}
<section class="hero container">
  <h1 class="en">Contact Card Rummy Guides</h1>
  <h1 class="ur urdu-block">کارڈ رمی گائیڈز سے رابطہ</h1>
  <p class="lead en">Reach us for website and guide questions. For in-app balances, use Card Rummy’s own support icon so agents see your user ID.</p>
  <p class="lead ur urdu-block">ویب سائٹ سوالات کے لیے ہم سے رابطہ کریں۔ بیلنس مسائل کے لیے ایپ کا سپورٹ آئیکن استعمال کریں۔</p>
</section>
<section class="section"><div class="container panel">
  <h2 class="en">Email</h2><h2 class="ur urdu-block">ای میل</h2>
  <p><a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>
  <p class="en" style="color:var(--muted)">Include your app version, Android model, and screenshots when reporting install or guide issues.</p>
  <p class="ur urdu-block" style="color:var(--muted)">مسئلہ بتاتے وقت ایپ ورژن، فون ماڈل اور اسکرین شاٹس شامل کریں۔</p>
</div></section>
"""
    html_out = page_shell(
        depth=depth,
        active="/contact-us/",
        title="Contact Us – Card Rummy Support",
        description="Contact cardrummy.org about Card Rummy guides. Email support@cardrummy.org for website help in English or Urdu.",
        canonical_path="/contact-us/",
        body=body,
        schemas=[crumbs_ld([("Home", "/"), ("Contact Us", "/contact-us/")])],
    )
    write_page("contact-us", "index.html", html_out)


def build_privacy() -> None:
    depth = 1
    body = f"""
{crumbs_html(depth, [("Home", "/"), ("Privacy Policy", None)])}
<section class="hero container">
  <h1 class="en">Privacy Policy</h1>
  <h1 class="ur urdu-block">پرائیویسی پالیسی</h1>
  <p class="meta">Last updated: {LASTMOD}</p>
</section>
<section class="section"><div class="container prose">
  <p class="en">cardrummy.org provides informational pages about the Card Rummy Android app. We do not operate the game servers or your JazzCash wallet.</p>
  <p class="ur urdu-block">cardrummy.org کارڈ رمی کے بارے میں معلومات دیتا ہے۔ ہم گیم سرور یا آپ کا جازکیش والیٹ نہیں چلاتے۔</p>
  <h2 class="en">Information we may collect</h2>
  <h2 class="ur urdu-block">ممکنہ معلومات</h2>
  <p class="en">If you email us, we receive the address and message content you send. Standard server logs may include IP address, browser type, and pages visited for security and diagnostics.</p>
  <p class="ur urdu-block">ای میل پر آپ کا پتہ اور پیغام آتا ہے۔ سرور لاگز میں IP، براؤزر اور صفحات سیکیورٹی کے لیے ہو سکتے ہیں۔</p>
  <h2 class="en">Cookies and local storage</h2>
  <h2 class="ur urdu-block">کوکیز اور لوکل اسٹوریج</h2>
  <p class="en">We use local storage to remember your English/Urdu language preference on this device. We do not sell personal data.</p>
  <p class="ur urdu-block">زبان کی ترجیح یاد رکھنے کے لیے لوکل اسٹوریج استعمال ہوتی ہے۔ ہم ذاتی ڈیٹا فروخت نہیں کرتے۔</p>
  <h2 class="en">Third-party links</h2>
  <h2 class="ur urdu-block">تیسرے فریق کے لنکس</h2>
  <p class="en">Download buttons may open partner endpoints disclosed on the download page. Their privacy practices are separate from cardrummy.org.</p>
  <p class="ur urdu-block">ڈاؤن لوڈ بٹن پارٹنر لنکس کھول سکتا ہے جن کی پرائیویسی الگ ہوتی ہے۔</p>
  <h2 class="en">Contact</h2>
  <p><a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>
</div></section>
"""
    html_out = page_shell(
        depth=depth,
        active="/privacy-policy/",
        title="Privacy Policy – Card Rummy",
        description="Privacy Policy for cardrummy.org Card Rummy guides. How we handle emails, logs, and language preference storage.",
        canonical_path="/privacy-policy/",
        body=body,
        schemas=[crumbs_ld([("Home", "/"), ("Privacy Policy", "/privacy-policy/")])],
    )
    write_page("privacy-policy", "index.html", html_out)


def build_disclaimer() -> None:
    depth = 1
    body = f"""
{crumbs_html(depth, [("Home", "/"), ("Disclaimer", None)])}
<section class="hero container">
  <h1 class="en">Disclaimer</h1>
  <h1 class="ur urdu-block">ڈس کلیمر</h1>
</section>
<section class="section"><div class="container prose">
  <p class="en">cardrummy.org offers educational guides only. We do not guarantee winnings, withdrawal timing, bonus eligibility, or uninterrupted app access. Real-money play involves risk of loss.</p>
  <p class="ur urdu-block">cardrummy.org صرف تعلیمی گائیڈز دیتا ہے۔ جیت، نکلوانے کا وقت، بونس یا بلا رکاوٹ رسائی کی ضمانت نہیں۔ حقیقی رقم میں نقصان ممکن ہے۔</p>
  <p class="en">Nothing on this site is legal, financial, or tax advice. Online gaming rules in Pakistan can be complex and may change. You are responsible for complying with laws that apply to you.</p>
  <p class="ur urdu-block">یہ قانونی یا مالی مشورہ نہیں۔ پاکستان میں آن لائن گیمنگ کے قواعد تبدیل ہو سکتے ہیں۔ اپنے قوانین کی پابندی آپ کی ذمہ داری ہے۔</p>
  <p class="en">App names, logos, and trademarks belong to their owners. Affiliate relationships, when used, are disclosed next to download calls to action.</p>
  <p class="ur urdu-block">نام اور ٹریڈ مارکس مالکان کے ہیں۔ افیلی ایٹ تعلق ڈاؤن لوڈ CTA کے پاس ظاہر کیا جاتا ہے۔</p>
</div></section>
"""
    html_out = page_shell(
        depth=depth,
        active="/disclaimer/",
        title="Disclaimer – Card Rummy",
        description="Disclaimer for cardrummy.org: educational Card Rummy guides only, no income guarantees, play responsibly.",
        canonical_path="/disclaimer/",
        body=body,
        schemas=[crumbs_ld([("Home", "/"), ("Disclaimer", "/disclaimer/")])],
    )
    write_page("disclaimer", "index.html", html_out)


BLOGS = [
    {
        "slug": "is-card-rummy-safe-for-pakistan-players",
        "title": "Is Card Rummy Safe for Pakistan Players?",
        "description": "A practical safety check for Card Rummy in Pakistan: APK source, account binding, JazzCash habits, and red flags before you deposit.",
        "h1_en": "Safety checks every Card Rummy player in Pakistan should run",
        "h1_ur": "پاکستان میں ہر کارڈ رمی کھلاڑی کو چلانے والے حفاظتی چیکس",
        "image": "card-rummy.webp",
        "image_alt": "Card Rummy app icon used in a Pakistan safety review",
        "sections": [
            (
                "What “safe” should mean for Card Rummy",
                "سیفٹی کا مطلب کیا ہونا چاہیے",
                [
                    "Safety for Card Rummy is not a slogan on a download button. It means you know where the APK came from, your login is bound to a real phone number or email, and you understand that real-money play can lose funds as easily as it can return them.",
                    "Pakistani players usually care about three outcomes: the install does not carry mystery permissions, JazzCash or EasyPaisa transfers match the amounts they typed, and customer support answers when a withdrawal stalls.",
                    "This guide stays practical. It does not promise risk-free earnings. It shows how to reduce avoidable mistakes before your first deposit.",
                ],
                [
                    "کارڈ رمی کی سیفٹی صرف ڈاؤن لوڈ بٹن کا نعرہ نہیں۔ مطلب یہ ہے کہ اے پی کے کا ماخذ معلوم ہو، لاگ اِن بائنڈ ہو، اور آپ سمجھیں کہ حقیقی رقم ہار بھی سکتے ہیں۔",
                    "پاکستانی کھلاڑی عموماً تین باتیں دیکھتے ہیں: مشکوک پرمیشنز نہ ہوں، جازکیش/ایزی پیسہ رقم درست ہو، اور نکلوانے میں رکاوٹ پر سپورٹ جواب دے۔",
                    "یہ گائیڈ عملی ہے۔ خطرے سے پاک آمدنی کا وعدہ نہیں۔ پہلے ڈپازٹ سے پہلے غلطیاں کم کرنے کا طریقہ بتاتی ہے۔",
                ],
            ),
            (
                "Verify the APK path before you install",
                "انسٹال سے پہلے اے پی کے راستہ چیک کریں",
                [
                    "Start on cardrummy.org and open the dedicated download guide rather than random Telegram forwards. Compare the listed version, file size, and developer name with what your phone shows after the file finishes downloading.",
                    "Android will ask you to allow installs from that source. Grant the permission only for the browser or file manager you trust, then turn the setting off again.",
                    "If a link jumps straight to an unrelated tracker domain without any disclosure, pause. Our download page explains when an affiliate endpoint is used.",
                ],
                [
                    "بے ترتیب ٹیلیگرام کے بجائے cardrummy.org کی ڈاؤن لوڈ گائیڈ سے شروع کریں۔ ورژن، سائز اور ڈویلپر کا موازنہ کریں۔",
                    "اینڈرائیڈ انسٹال اجازت مانگے گا — صرف بھروسے مند براؤزر کو دیں، پھر بند کر دیں۔",
                    "بغیر وضاحت کے عجیب ٹریکر ڈومین پر جائیں تو رک جائیں۔ ہمارا ڈاؤن لوڈ صفحہ افیلی ایٹ کی وضاحت کرتا ہے۔",
                ],
            ),
            (
                "Deposit habits that protect JazzCash users",
                "جازکیش صارفین کی عادتیں",
                [
                    "Make a small first deposit so you can confirm the wallet name, reference ID, and in-app balance update. Screenshot the confirmation before you leave the payment screen.",
                    "Never share OTP codes with anyone claiming to be Card Rummy support in WhatsApp groups. Official support will not need your JazzCash PIN.",
                    "Set a weekly spend limit in your own notes app. When the limit is hit, stop for the week.",
                ],
                [
                    "پہلا چھوٹا ڈپازٹ کر کے والیٹ نام، ریفرنس اور بیلنس چیک کریں۔ اسکرین شاٹ لیں۔",
                    "واٹس ایپ گروپس میں سپورٹ بن کر OTP نہ دیں۔ جازکیش پن کسی کو نہ بتائیں۔",
                    "ہفتہ وار حد لکھیں؛ پوری ہو تو رک جائیں۔",
                ],
            ),
        ],
        "faqs": [
            (
                "Is Card Rummy legal to discuss and download in Pakistan?",
                "Online real-money gaming sits in a legal grey area that can change. This site provides app guidance, not legal advice.",
                "کیا پاکستان میں کارڈ رمی ڈاؤن لوڈ قانونی ہے؟",
                "حقیقی رقم والی آن لائن گیمنگ قانونی طور پر پیچیدہ ہو سکتی ہے۔ یہ سائٹ ایپ گائیڈنس دیتی ہے، قانونی مشورہ نہیں۔",
            ),
            (
                "Does a high rating mean Card Rummy is risk-free?",
                "No. Ratings reflect popularity patterns, not guaranteed profit or zero disputes.",
                "کیا اعلیٰ ریٹنگ کا مطلب بغیر خطرہ ہے؟",
                "نہیں۔ ریٹنگ مقبولیت کی نشاندہی کرتی ہے، منافع یا صفر تنازعات کی ضمانت نہیں۔",
            ),
        ],
    },
    {
        "slug": "card-rummy-login-otp-bind-email-fixes",
        "title": "Card Rummy Login, OTP & Bind Email Fixes",
        "description": "Fix Card Rummy login stalls, missing OTP, guest-to-registered upgrades, and email binding so your Pakistan account stays recoverable.",
        "h1_en": "Get Card Rummy login and email binding working the first week",
        "h1_ur": "پہلے ہفتے میں کارڈ رمی لاگ اِن اور ای میل بائنڈنگ چلائیں",
        "image": "card-rummy-bind-mail.webp",
        "image_alt": "Card Rummy bind email and account security screen",
        "sections": [
            (
                "Choose register over endless guest sessions",
                "گیسٹ کے بجائے رجسٹر چنیں",
                [
                    "Card Rummy lets you peek at the lobby as a guest. Long-term progress, referrals, and withdrawals need a registered profile tied to your mobile number.",
                    "Enter a Pakistani mobile number, wait for the OTP, and create a password you do not reuse on JazzCash.",
                    "Keep the app in the foreground while SMS arrives so Android does not delay the notification.",
                ],
                [
                    "گیسٹ سے لابی دیکھ سکتے ہیں، مگر نکلوانے کے لیے رجسٹرڈ پروفائل چاہیے۔",
                    "پاکستانی نمبر دیں، OTP کا انتظار کریں، جازکیش والا پاس ورڈ نہ دہرائیں۔",
                    "SMS آتے وقت ایپ کھلی رکھیں۔",
                ],
            ),
            (
                "When the OTP never arrives",
                "جب OTP نہ آئے",
                [
                    "Confirm +92 format, toggle airplane mode, then request a new code after the cooldown.",
                    "Dual-SIM phones sometimes deliver OTP to the inactive SIM — switch the default SMS SIM and retry.",
                    "Note the exact error text and app version before contacting in-app support.",
                ],
                [
                    "+92 فارمیٹ چیک کریں، ایئرپلین موڈ ٹوگل کریں، کول ڈاؤن کے بعد نیا کوڈ لیں۔",
                    "ڈوئل سم پر SMS والی سم درست کریں۔",
                    "ایرر ٹیکسٹ اور ورژن نوٹ کر کے ایپ سپورٹ سے رابطہ کریں۔",
                ],
            ),
            (
                "Bind email so recovery is not a gamble",
                "ای میل بائنڈ کریں",
                [
                    "Inside account security, bind an inbox you check daily and store a screenshot of the success state.",
                    "Bound email helps when you change phones or hit regional IP locks.",
                    "Log out and log back in once before you deposit a larger amount.",
                ],
                [
                    "روزانہ چیک ہونے والی ای میل بائنڈ کریں اور کامیابی کا اسکرین شاٹ رکھیں۔",
                    "فون تبدیل یا IP لاک پر بازیابی آسان ہوتی ہے۔",
                    "بڑا ڈپازٹ سے پہلے ایک بار لاگ آؤٹ/لاگ اِن کریں۔",
                ],
            ),
        ],
        "faqs": [
            (
                "Can I log in to Card Rummy on two Android phones?",
                "Many sessions allow one active device at a time. Bind email first so you can recover if a lock appears.",
                "کیا دو فونز پر لاگ اِن ہو سکتا ہے؟",
                "اکثر ایک فعال ڈیوائس ہوتی ہے۔ پہلے ای میل بائنڈ کریں۔",
            ),
            (
                "What if I uninstall without binding email?",
                "You may still recover with mobile OTP, but email binding makes the process smoother.",
                "بغیر ای میل بائنڈ ان انسٹال کر دیا؟",
                "موبائل OTP سے ممکن ہے، مگر ای میل بائنڈنگ آسان بناتی ہے۔",
            ),
        ],
    },
    {
        "slug": "card-rummy-bonuses-first-week",
        "title": "Card Rummy Bonuses: What to Claim in Week One",
        "description": "Prioritize Card Rummy welcome chips, deposit offers, daily login rewards, and referral value without chasing every banner.",
        "h1_en": "A first-week bonus plan for Card Rummy in Pakistan",
        "h1_ur": "پاکستان میں کارڈ رمی کے پہلے ہفتے کا بونس پلان",
        "image": "card-rummy-earn-bonus.webp",
        "image_alt": "Card Rummy bonuses and rewards screen for new players",
        "sections": [
            (
                "Read the wagering note before you celebrate",
                "خوشی سے پہلے شرط نامہ پڑھیں",
                [
                    "Welcome chips, recharge rebates, and event spins look generous in the banner row. The useful question is how those rewards convert into withdrawable balance.",
                    "Note minimum deposit, game eligibility, and turnover requirements on each offer sheet.",
                    "Keep a simple phone note with claim dates so you do not miss a daily login streak you already started.",
                ],
                [
                    "بینرز خوبصورت لگتے ہیں؛ اصل سوال نکلوانے کے قابل بیلنس کا ہے۔",
                    "ہر آفر پر کم از کم ڈپازٹ اور اہلیت نوٹ کریں۔",
                    "کلیم کی تاریخیں فون نوٹ میں لکھیں۔",
                ],
            ),
            (
                "Day one: welcome value and a tiny deposit test",
                "پہلا دن: ویلکم ویلیو اور چھوٹا ڈپازٹ",
                [
                    "Claim registration rewards before cash tables. Use those chips to learn pacing.",
                    "When ready, make a small JazzCash or EasyPaisa deposit using the deposit guide and confirm whether a rebate applied.",
                    "Missing rebate? Capture the order ID and ask support the same day.",
                ],
                [
                    "کیش ٹیبل سے پہلے رجسٹریشن انعام لیں۔",
                    "چھوٹا ڈپازٹ کر کے ریبیت چیک کریں۔",
                    "غائب ہو تو آرڈر آئی ڈی کے ساتھ اسی دن سپورٹ سے پوچھیں۔",
                ],
            ),
            (
                "Daily login, rebate, and VIP — without burnout",
                "ڈیلی لاگ اِن اور VIP بغیر برن آؤٹ",
                [
                    "Open the app at a set time, claim, and leave if you did not plan a session.",
                    "Skip recharge rebate until you already decided to add funds that week.",
                    "Treat VIP as a side effect of play you enjoy, not a target that forces deposits.",
                ],
                [
                    "مقرر وقت پر کلیم کریں؛ بغیر پلان کے لمبا نہ کھیلیں۔",
                    "جب تک ڈپازٹ کا فیصلہ نہ ہو ریبیت نہ بھگائیں۔",
                    "VIP کو اضافی ڈپازٹ کا ہدف نہ بنائیں۔",
                ],
            ),
        ],
        "faqs": [
            (
                "Should I deposit only to unlock bonuses?",
                "No. Deposit because you budgeted entertainment spend. Bonuses are optional extras.",
                "کیا صرف بونس کے لیے ڈپازٹ کریں؟",
                "نہیں۔ بجٹ شدہ تفریح کے لیے ڈپازٹ کریں؛ بونس اختیاری ہیں۔",
            ),
            (
                "Where are full deposit steps?",
                "Use the dedicated deposit guide on cardrummy.org for JazzCash and EasyPaisa steps.",
                "مکمل ڈپازٹ مراحل کہاں ہیں؟",
                "cardrummy.org کی الگ ڈپازٹ گائیڈ دیکھیں۔",
            ),
        ],
    },
    {
        "slug": "card-rummy-ip-exceed-install-fix",
        "title": "Card Rummy IP Exceed & Install Errors Fixed",
        "description": "Clear Card Rummy IP exceed locks, failed APK installs, and update loops on Android with steps Pakistani players can follow.",
        "h1_en": "Fix Card Rummy IP exceed and Android install problems",
        "h1_ur": "کارڈ رمی IP Exceed اور انسٹال مسائل ٹھیک کریں",
        "image": "card-rummy-game-interface.webp",
        "image_alt": "Card Rummy interface shown while troubleshooting install errors",
        "sections": [
            (
                "What the IP exceed message usually means",
                "IP Exceed عموماً کیا مطلب رکھتا ہے",
                [
                    "Card Rummy may show an IP exceed notice when too many accounts or logins appear from one network. Shared Wi-Fi, hotspots, and VPNs are common triggers.",
                    "The message is a security gate, not proof that your JazzCash was taken. Stop creating new guest profiles on the same Wi-Fi.",
                    "Write down the exact wording, time, and whether you were on Wi-Fi or mobile data.",
                ],
                [
                    "ایک نیٹ ورک سے زیادہ لاگ اِن پر IP exceed آ سکتا ہے۔ شیئرڈ وائی فائی اور وی پی این عام وجوہات ہیں۔",
                    "یہ سیکیورٹی گیٹ ہے، جازکیش چوری کا ثبوت نہیں۔ نئے گیسٹ اکاؤنٹ بنانا بند کریں۔",
                    "عین متن، وقت اور نیٹ ورک قسم نوٹ کریں۔",
                ],
            ),
            (
                "Unlock path that works for most players",
                "زیادہ تر کھلاڑیوں والا ان لاک راستہ",
                [
                    "Switch Wi-Fi and mobile data, force-close the app, and reopen after two minutes. Turn VPNs fully off.",
                    "Log in with your bound number rather than a fresh guest account.",
                    "Still blocked? Contact in-app support with user ID and screenshot. Avoid remote-access “unlock services.”",
                ],
                [
                    "وائی فائی/موبائل ڈیٹا بدلیں، ایپ بند کر کے دو منٹ بعد کھولیں۔ وی پی این مکمل بند کریں۔",
                    "نئے گیسٹ کے بجائے باؤنڈ نمبر سے لاگ اِن کریں۔",
                    "پھر بھی بلاک ہو تو یوزر آئی ڈی کے ساتھ ایپ سپورٹ۔ ریموٹ ایکسیس خدمات سے بچیں۔",
                ],
            ),
            (
                "APK install failures on Android",
                "اینڈرائیڈ پر انسٹال فیل",
                [
                    "Allow unknown apps only for the downloader, then retry from Files.",
                    "“App not installed” after an update often means a signature mismatch — uninstall only after bind email is confirmed, then install from our download page.",
                    "Free at least twice the APK size in storage before retrying.",
                ],
                [
                    "صرف ڈاؤن لوڈر کو ان نان اجازت دیں، فائلز سے دوبارہ کوشش کریں۔",
                    "دستخط مختلف ہوں تو ای میل بائنڈ کے بعد پرانا ان انسٹال کر کے ہماری گائیڈ سے نیا لگائیں۔",
                    "کم از کم اے پی کے سے دوگنا خالی اسٹوریج رکھیں۔",
                ],
            ),
        ],
        "faqs": [
            (
                "Does IP exceed mean my money is gone?",
                "Not by itself. It usually blocks login from a network. Contact support with bound account details before creating replacements.",
                "کیا IP Exceed کا مطلب رقم ختم؟",
                "خود بخود نہیں۔ عموماً لاگ اِن رکتا ہے۔ نیا اکاؤنٹ بنانے سے پہلے سپورٹ سے رابطہ کریں۔",
            ),
            (
                "Can a VPN fix IP exceed?",
                "VPNs often cause the lock. Turn the VPN off and retry on local mobile data.",
                "کیا وی پی این IP Exceed ٹھیک کرے گا؟",
                "وی پی این اکثر مسئلہ بنتا ہے۔ بند کر کے موبائل ڈیٹا پر کوشش کریں۔",
            ),
        ],
    },
]


def build_blog_index() -> None:
    depth = 1
    cards = []
    for post in BLOGS:
        cards.append(
            f"""<article class="blog-card">
  <img src="{asset(depth, 'images/' + post['image'])}" width="800" height="1000" alt="{esc(post['image_alt'])}" style="border-radius:10px;aspect-ratio:16/10;object-fit:cover;width:100%;height:auto">
  <p class="meta">{LASTMOD} · 7–8 min</p>
  <h3><a href="{asset(depth, 'blog/' + post['slug'] + '/index.html')}">{esc(post['title'])}</a></h3>
  <p class="en" style="color:var(--muted);margin:0">{esc(post['description'])}</p>
  <p class="ur urdu-block" style="color:var(--muted);margin:0">{esc(post['h1_ur'])}</p>
</article>"""
        )
    body = f"""
{crumbs_html(depth, [("Home", "/"), ("Blog", None)])}
<section class="hero container">
  <h1 class="en">Card Rummy Blog – Safety, Login, Bonuses & Fixes</h1>
  <h1 class="ur urdu-block">کارڈ رمی بلاگ — سیفٹی، لاگ اِن، بونس اور فکسز</h1>
  <p class="lead en">Four focused guides that support the main app pages without duplicating deposit or withdraw instructions.</p>
  <p class="lead ur urdu-block">چار مرکوز گائیڈز جو ڈپازٹ/نکلوانے کے صفحات دہرائے بغیر مدد کرتی ہیں۔</p>
</section>
<section class="section"><div class="container grid-2">{"".join(cards)}</div></section>
"""
    html_out = page_shell(
        depth=depth,
        active="/blog/",
        title="Card Rummy Blog – Guides for Pakistan Players",
        description="Card Rummy blog in English and Urdu: safety checks, login fixes, first-week bonuses, and IP exceed troubleshooting.",
        canonical_path="/blog/",
        body=body,
        schemas=[crumbs_ld([("Home", "/"), ("Blog", "/blog/")])],
    )
    write_page("blog", "index.html", html_out)


def build_blog_posts() -> None:
    for post in BLOGS:
        depth = 2
        sections_html = []
        for (h_en, h_ur, en_ps, ur_ps) in post["sections"]:
            blocks = [f"<h2 class='en'>{esc(h_en)}</h2><h2 class='ur urdu-block'>{esc(h_ur)}</h2>"]
            for pe, pu in zip(en_ps, ur_ps):
                blocks.append(f"<p class='en'>{pe}</p><p class='ur urdu-block'>{pu}</p>")
            sections_html.append('<div class="prose" style="margin-bottom:1.5rem">' + "".join(blocks) + "</div>")
        body = f"""
{crumbs_html(depth, [("Home", "/"), ("Blog", "/blog/"), (post["title"], None)])}
<section class="hero container">
  <p class="meta">{LASTMOD}</p>
  <h1 class="en">{esc(post["h1_en"])}</h1>
  <h1 class="ur urdu-block">{esc(post["h1_ur"])}</h1>
  <figure class="hero-visual" style="max-width:420px;margin-top:1.25rem">
    <img src="{asset(depth, 'images/' + post['image'])}" width="800" height="1000" alt="{esc(post['image_alt'])}">
  </figure>
</section>
<section class="section"><div class="container">{"".join(sections_html)}
  <p class="en">Related: <a href="{asset(depth, 'download-card-rummy/index.html')}">Download Card Rummy</a> · <a href="{asset(depth, 'deposit-money-in-card-rummy/index.html')}">Deposit guide</a> · <a href="{asset(depth, 'withdraw-money-from-card-rummy/index.html')}">Withdraw guide</a></p>
  <p class="ur urdu-block">متعلقہ: <a href="{asset(depth, 'download-card-rummy/index.html')}">ڈاؤن لوڈ</a> · <a href="{asset(depth, 'deposit-money-in-card-rummy/index.html')}">ڈپازٹ</a> · <a href="{asset(depth, 'withdraw-money-from-card-rummy/index.html')}">نکلوائیں</a></p>
</div></section>
<section class="section"><div class="container"><h2 class="en">FAQs</h2><h2 class="ur urdu-block">سوالات</h2>{faq_block(post["faqs"])}</div></section>
"""
        path = f"/blog/{post['slug']}/"
        html_out = page_shell(
            depth=depth,
            active="/blog/",
            title=post["title"] + " | Card Rummy",
            description=post["description"],
            canonical_path=path,
            body=body,
            og_image=post["image"] if post["image"] != "card-rummy.webp" else "card-rummy-og.webp",
            schemas=[
                crumbs_ld([("Home", "/"), ("Blog", "/blog/"), (post["title"], path)]),
                article_ld(post["title"], post["description"], path, post["image"]),
                faq_ld([(f[0], f[1]) for f in post["faqs"]]),
            ],
        )
        write_page(f"blog/{post['slug']}", "index.html", html_out)


def build_robots_and_sitemaps() -> None:
    pages = [
        ("/", 1.0, "daily"),
        ("/download-card-rummy/", 0.9, "weekly"),
        ("/deposit-money-in-card-rummy/", 0.9, "weekly"),
        ("/withdraw-money-from-card-rummy/", 0.9, "weekly"),
        ("/card-rummy-for-pc/", 0.9, "weekly"),
        ("/about-us/", 0.6, "monthly"),
        ("/blog/", 0.8, "weekly"),
        ("/contact-us/", 0.6, "monthly"),
        ("/privacy-policy/", 0.4, "yearly"),
        ("/disclaimer/", 0.4, "yearly"),
    ]
    for post in BLOGS:
        pages.append((f"/blog/{post['slug']}/", 0.7, "monthly"))

    url_xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, pri, freq in pages:
        url_xml.append(
            f"  <url><loc>{ORIGIN}{loc}</loc><lastmod>{LASTMOD}</lastmod>"
            f"<changefreq>{freq}</changefreq><priority>{pri}</priority></url>"
        )
    url_xml.append("</urlset>")
    (ROOT / "index.xml").write_text("\n".join(url_xml) + "\n", encoding="utf-8")

    images = [
        ("/", "card-rummy.webp", "Card Rummy app icon for Pakistan Android download"),
        ("/", "card-rummy-game-interface.webp", "Card Rummy lobby interface"),
        ("/", "card-rummy-games.webp", "Card Rummy games collection"),
        ("/", "card-rummy-earn-bonus.webp", "Card Rummy bonuses screen"),
        ("/", "card-rummy-add-money.webp", "Card Rummy deposit screen"),
        ("/download-card-rummy/", "card-rummy.webp", "Card Rummy APK download icon"),
        ("/blog/is-card-rummy-safe-for-pakistan-players/", "card-rummy.webp", "Card Rummy safety review icon"),
        ("/blog/card-rummy-login-otp-bind-email-fixes/", "card-rummy-bind-mail.webp", "Card Rummy bind email screen"),
        ("/blog/card-rummy-bonuses-first-week/", "card-rummy-earn-bonus.webp", "Card Rummy first-week bonuses"),
        ("/blog/card-rummy-ip-exceed-install-fix/", "card-rummy-game-interface.webp", "Card Rummy troubleshooting interface"),
    ]
    img_xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    # group by page
    by_page: dict[str, list[tuple[str, str]]] = {}
    for page, file, title in images:
        by_page.setdefault(page, []).append((file, title))
    for page, items in by_page.items():
        img_xml.append(f"  <url><loc>{ORIGIN}{page}</loc>")
        for file, title in items:
            img_xml.append(
                f"    <image:image><image:loc>{ORIGIN}/images/{file}</image:loc>"
                f"<image:title>{esc(title)}</image:title>"
                f"<image:caption>{esc(title)}</image:caption></image:image>"
            )
        img_xml.append("  </url>")
    img_xml.append("</urlset>")
    (ROOT / "image-sitemap.xml").write_text("\n".join(img_xml) + "\n", encoding="utf-8")

    (ROOT / "sitemap-index.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>{ORIGIN}/index.xml</loc><lastmod>{LASTMOD}</lastmod></sitemap>
  <sitemap><loc>{ORIGIN}/image-sitemap.xml</loc><lastmod>{LASTMOD}</lastmod></sitemap>
</sitemapindex>
""",
        encoding="utf-8",
    )

    robots = f"""# As a condition of accessing this website, you agree to abide by the following
# content signals:

# (a)  If a Content-Signal = yes, you may collect content for the corresponding
#      use.
# (b)  If a Content-Signal = no, you may not collect content for the corresponding
#      use.
# (c)  If the website operator does not include a Content-Signal for a
#      corresponding use, the website operator neither grants nor restricts
#      permission via Content-Signal with respect to the corresponding use.

# The content signals and their meanings are:

# search:   building a search index and providing search results (e.g., returning
#           hyperlinks and short excerpts from your website's contents). Search does not
#           include providing AI-generated search summaries.
# ai-input: inputting content into one or more AI models (e.g., retrieval
#           augmented generation, grounding, or other real-time taking of content for
#           generative AI search answers).
# ai-train: training or fine-tuning AI models.
# use:      how AI systems may consume the content (immediate, reference, or full).

# ANY RESTRICTIONS EXPRESSED VIA CONTENT SIGNALS ARE EXPRESS RESERVATIONS OF
# RIGHTS UNDER ARTICLE 4 OF THE EUROPEAN UNION DIRECTIVE 2019/790 ON COPYRIGHT
# AND RELATED RIGHTS IN THE DIGITAL SINGLE MARKET.

# BEGIN Cloudflare Managed content

User-agent: *
Content-Signal: search=yes,ai-train=no,use=reference
Allow: /

User-agent: Amazonbot
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: CloudflareBrowserRenderingCrawler
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: GPTBot
Disallow: /

User-agent: meta-externalagent
Disallow: /

# END Cloudflare Managed Content

User-agent: *
Disallow: /scripts/
Disallow: /src/
Disallow: /node_modules/

Sitemap: {ORIGIN}/sitemap-index.xml
"""
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    print("wrote robots + sitemaps")


def main() -> None:
    build_home()
    build_download()
    build_deposit()
    build_withdraw()
    build_pc()
    build_about()
    build_contact()
    build_privacy()
    build_disclaimer()
    build_blog_index()
    build_blog_posts()
    build_robots_and_sitemaps()
    print("Done — static site ready for", ORIGIN)


if __name__ == "__main__":
    main()
