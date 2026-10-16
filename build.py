# -*- coding: utf-8 -*-
"""يبني الموقع (عربي + إنجليزي) في مجلد public/ — شغّل: python3 build.py"""
import json, os, re, shutil, html as H
from urllib.parse import quote
from config import SITE, VEHICLES, ROUTES
import content as C_AR, content_en as C_EN

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
D = SITE["domain"]
SERVICE_ORDER = C_AR.SERVICE_ORDER

# ---------------------------------------------------------------- strings
T = {
 "ar": dict(code="ar", dir="rtl", og="ar_SA", prefix="", name=SITE["name"], phone_t=SITE["phone_title"],
   pages=C_AR.PAGES, articles=C_AR.ARTICLES, other="en", switch="English",
   home="الرئيسية", blog="مقالات",
   nav=[("", "الرئيسية"), ("jeddah-to-makkah/", "جدة ← مكة"), ("makkah-to-jeddah-airport/", "مكة ← المطار"),
        ("makkah-to-madinah/", "مكة ↔ المدينة"), ("prices/", "الأسعار"), ("blog/", "مقالات")],
   wa="واتساب", wa_book="احجز عبر واتساب", wa_msg="السلام عليكم، أرغب بحجز توصيل", wa_msg_p="السلام عليكم، أرغب بحجز ",
   call="اتصال", sticky_wa="احجز واتساب", frm="يبدأ من", sar="ر.س", route_col="المسار",
   price_note="الأسعار تبدأ من القيم الموضحة بالريال السعودي، ويُؤكد السعر النهائي قبل الحجز.",
   facts=["يبدأ السعر من", "المسافة", "مدة الرحلة", "متاح دائماً"],
   steps_h="كيف تحجز؟", steps=[("أرسل تفاصيل رحلتك", "املأ نموذج الحجز أو راسلنا على واتساب: المسار، التاريخ، الوقت، عدد الركاب ورقم الرحلة."),
        ("نؤكد السعر والسائق", "نرسل لك السعر النهائي، ثم اسم السائق ورقمه ونوع السيارة قبل الموعد."),
        ("السائق في انتظارك", "يستقبلك السائق في الموعد ويوصلك إلى وجهتك مباشرة.")],
   faq_h="أسئلة شائعة",
   f=dict(title="احجز عبر واتساب", route="المسار", date="التاريخ", time="الوقت", pax="عدد الركاب", flight="رقم الرحلة",
          opt="(اختياري)", car="نوع السيارة", name="الاسم", place="العنوان أو الفندق", submit="أرسل الطلب على واتساب",
          note="سيفتح واتساب برسالة جاهزة — اضغط إرسال ونرد عليك بتأكيد السعر."),
   cta_h="تحتاج توصيلاً من مطار جدة الى مكة؟", cta_p="سائق ينتظرك بلوحة باسمك وسعر ثابت يبدأ من {p} ريال.",
   cta_msg="السلام عليكم، أرغب بحجز توصيل من مطار جدة الى مكة", prices_btn="الأسعار",
   foot_routes="المسارات", foot_info="معلومات مفيدة", price_list="جدول الأسعار", book_now="احجز الآن",
   foot_p="توصيل خاص بين مطار جدة ومكة، ومن مكة إلى المدينة والطائف — على مدار الساعة.",
   updated="آخر تحديث:", read="اقرأ المقال", crumbs_label="مسار التنقل", menu="القائمة",
   blog_page=dict(title="مقالات ونصائح للتنقل بين جدة ومكة والمدينة",
        desc="أدلة ونصائح للمعتمرين والزوار: المسافة بين جدة ومكة، طرق الوصول من مطار جدة، قطار الحرمين، الباصات، ودليل المعتمر.",
        h1="مقالات ونصائح للتنقل", lead="أدلة عملية للمعتمرين والزوار حول التنقل بين مطار جدة ومكة والمدينة."),
   contact_h="طرق التواصل", contact_wa="واتساب مباشر", contact_p="متاحون على مدار الساعة طوال أيام الأسبوع.",
   nf=dict(title="الصفحة غير موجودة", h1="الصفحة غير موجودة", lead="ربما تم نقل الصفحة. جرّب أحد المسارات التالية:"),
   cities=["جدة", "مكة المكرمة", "المدينة المنورة", "الطائف"]),
 "en": dict(code="en", dir="ltr", og="en_US", prefix="en/", name=SITE["name_en"], phone_t=SITE["phone_title_en"],
   pages=C_EN.PAGES, articles=C_EN.ARTICLES, other="ar", switch="العربية",
   home="Home", blog="Guides",
   nav=[("", "Home"), ("jeddah-to-makkah/", "Jeddah → Makkah"), ("makkah-to-jeddah-airport/", "Makkah → Airport"),
        ("makkah-to-madinah/", "Makkah ↔ Madinah"), ("prices/", "Prices"), ("blog/", "Guides")],
   wa="WhatsApp", wa_book="Book on WhatsApp", wa_msg="Hello, I'd like to book a transfer", wa_msg_p="Hello, I'd like to book: ",
   call="Call", sticky_wa="Book on WhatsApp", frm="From", sar="SAR", route_col="Route",
   price_note="Prices start from the amounts shown in Saudi riyals; your final price is confirmed before booking.",
   facts=["Starting price", "Distance", "Travel time", "Available"],
   steps_h="How to book", steps=[("Send your trip details", "Fill in the booking form or message us on WhatsApp: route, date, time, passengers and flight number."),
        ("We confirm price & driver", "We send your final price, then the driver's name, phone and car details before pickup."),
        ("Your driver is waiting", "The driver meets you on time and takes you straight to your destination.")],
   faq_h="Frequently asked questions",
   f=dict(title="Book on WhatsApp", route="Route", date="Date", time="Time", pax="Passengers", flight="Flight number",
          opt="(optional)", car="Car type", name="Name", place="Address or hotel", submit="Send request on WhatsApp",
          note="WhatsApp opens with a ready message — tap send and we'll confirm your price."),
   cta_h="Need a ride from Jeddah Airport to Makkah?", cta_p="A driver waiting with your name and a fixed price from {p} SAR.",
   cta_msg="Hello, I'd like to book a transfer from Jeddah Airport to Makkah", prices_btn="Prices",
   foot_routes="Routes", foot_info="Travel guides", price_list="Price list", book_now="Book now",
   foot_p="Private transfers between Jeddah Airport and Makkah, and from Makkah to Madinah and Taif — 24/7.",
   updated="Last updated:", read="Read guide", crumbs_label="Breadcrumb", menu="Menu",
   blog_page=dict(title="Travel Guides: Jeddah, Makkah & Madinah Transport",
        desc="Guides for Umrah pilgrims and visitors: Jeddah to Makkah distance, how to get from Jeddah Airport to Makkah, the Haramain train, buses and an arrival guide.",
        h1="Travel guides", lead="Practical guides for pilgrims and visitors travelling between Jeddah Airport, Makkah and Madinah."),
   contact_h="Contact us", contact_wa="WhatsApp us", contact_p="Available 24 hours a day, 7 days a week.",
   nf=dict(title="Page not found", h1="Page not found", lead="The page may have moved. Try one of these routes:"),
   cities=["Jeddah", "Makkah", "Madinah", "Taif"]),
}
SLUGS = {L: {p["slug"] for p in T[L]["pages"] + T[L]["articles"]} | {"blog/"} for L in T}

# ---------------------------------------------------------------- helpers
def minp(k): return min(ROUTES[k]["prices"].values())
def fill(t): return re.sub(r"\[\[p:(\w+)\]\]", lambda m: str(minp(m.group(1))), t)
def esc(t): return H.escape(t, quote=True)
def path(L, slug): return "/" + T[L]["prefix"] + slug
def absu(L, slug): return D + path(L, slug)
def wa(text=""): return f"https://wa.me/{SITE['whatsapp']}" + (f"?text={quote(text)}" if text else "")
def rv(r, field, L): return r[field] if L == "ar" else r[field + "_en"]
def rurl(k, L): return path(L, ROUTES[k]["url"].lstrip("/"))
def veh(L): return [(v[0], v[1], v[2]) if L == "ar" else (v[0], v[3], v[4]) for v in VEHICLES]
def full_title(t, L):
    parts = fill(t).split(" | "); parts.insert(1, T[L]["phone_t"]); return " | ".join(parts)

ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.4-.2Z"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1L6.6 10.8Z"/></svg>'
LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="var(--brand)"/><path d="M8 20h16l-2-6a2 2 0 0 0-1.9-1.4h-8.2A2 2 0 0 0 10 14l-2 6Zm0 0v3m16-3v3M11 20v-1m10 1v-1" stroke="var(--gold)" stroke-width="2" fill="none" stroke-linecap="round"/><circle cx="16" cy="8" r="2" fill="var(--gold)"/></svg>'

# ---------------------------------------------------------------- components
def price_table(keys, L):
    t = T[L]
    head = "".join(f"<th>{esc(n)}<small>{esc(s)}</small></th>" for _, n, s in veh(L))
    rows = ""
    for k in keys:
        r = ROUTES[k]
        cells = "".join(f'<td><b>{r["prices"][v]}</b> {t["sar"]}</td>' for v, _, _ in veh(L))
        nm = esc(rv(r, "name", L))
        name = f'<a href="{rurl(k, L)}">{nm}</a>' if len(keys) > 1 else nm
        rows += f'<tr><th scope="row">{name}<small>{esc(rv(r, "km", L))} · {esc(rv(r, "time", L))}</small></th>{cells}</tr>'
    return (f'<div class="table-wrap"><table class="prices"><thead><tr><th>{t["route_col"]}</th>{head}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div><p class="note">{esc(t["price_note"])}</p>')

def steps(L):
    t = T[L]
    li = "".join(f"<li><span>{i}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></li>" for i, (a, b) in enumerate(t["steps"], 1))
    return f'<section class="block"><h2>{t["steps_h"]}</h2><ol class="steps">{li}</ol></section>'

def route_cards(current, L):
    t = T[L]; pages = {p["slug"]: p for p in t["pages"]}; cards = ""
    for slug in SERVICE_ORDER:
        if slug == current: continue
        p = pages[slug]; r = ROUTES[p["route"]]
        cards += (f'<a class="card" href="{path(L, slug)}"><h3>{esc(p["h1"])}</h3>'
                  f'<p>{esc(rv(r, "km", L))} · {esc(rv(r, "time", L))}</p><span>{t["frm"]} <b>{minp(p["route"])}</b> {t["sar"]}</span></a>')
    return f'<div class="cards">{cards}</div>'

def booking_form(route_key, L, big=False):
    f = T[L]["f"]
    opts = "".join(f'<option value="{esc(rv(r, "name", L))}"{" selected" if k == route_key else ""}>{esc(rv(r, "name", L))}</option>'
                   for k, r in ROUTES.items())
    cars = "".join(f'<option>{esc(n)} — {esc(s)}</option>' for _, n, s in veh(L))
    return f'''<form class="book{' big' if big else ''}" id="book" data-wa="{SITE['whatsapp']}" data-lang="{L}" novalidate>
<h2 class="book-title">{f["title"]}</h2>
<label>{f["route"]}<select name="route">{opts}</select></label>
<div class="row"><label>{f["date"]}<input type="date" name="date" required></label>
<label>{f["time"]}<input type="time" name="time"></label></div>
<div class="row"><label>{f["pax"]}<input type="number" name="pax" min="1" max="50" value="2" inputmode="numeric"></label>
<label>{f["flight"]} <small>{f["opt"]}</small><input name="flight" placeholder="SV1234" autocomplete="off" dir="ltr"></label></div>
<label>{f["car"]}<select name="car">{cars}</select></label>
<label>{f["name"]}<input name="name" autocomplete="name"></label>
<label>{f["place"]} <small>{f["opt"]}</small><input name="place"></label>
<button type="submit" class="btn wa">{ICON_WA}<span>{f["submit"]}</span></button>
<p class="form-note">{f["note"]}</p>
</form>'''

def faq_html(faqs, L):
    if not faqs: return ""
    items = "".join(f"<details><summary>{esc(fill(q))}</summary><p>{esc(fill(a))}</p></details>" for q, a in faqs)
    return f'<section class="block" id="faq"><h2>{T[L]["faq_h"]}</h2><div class="faq">{items}</div></section>'

def render_section(s, page, L):
    c = s.get("component")
    if c == "prices":     return f'<section class="block"><h2>{esc(s["h2"])}</h2>{price_table(s["routes"], L)}</section>'
    if c == "prices_all": return f'<section class="block"><h2>{esc(s["h2"])}</h2>{price_table(list(ROUTES), L)}</section>'
    if c == "steps":      return steps(L)
    if c == "routes":     return f'<section class="block"><h2>{esc(s["h2"])}</h2>{route_cards(page["slug"], L)}</section>'
    return f'<section class="block prose"><h2>{esc(s["h2"])}</h2>{fill(s["html"])}</section>'

# ---------------------------------------------------------------- schema
def org(L):
    return {"@type": "LocalBusiness", "@id": f"{absu(L, '')}#business", "name": T[L]["name"], "url": absu(L, ""),
            "telephone": "+" + SITE["phone"], "priceRange": "$$",
            "areaServed": [{"@type": "City", "name": n} for n in T[L]["cities"]],
            "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "opens": "00:00", "closes": "23:59",
                "dayOfWeek": ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}}

def schema(page, kind, trail, L):
    g = [{"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": absu(L, s)} for i, (s, n) in enumerate(trail, 1)]}]
    if page["slug"] == "":
        g += [org(L), {"@type": "WebSite", "@id": f"{absu(L, '')}#website", "url": absu(L, ""), "name": T[L]["name"], "inLanguage": L}]
    if kind == "service":
        r = ROUTES[page["route"]]
        g.append({"@type": "TaxiService", "name": page["h1"], "url": absu(L, page["slug"]), "description": fill(page["desc"]),
                  "provider": {"@id": f"{absu(L, '')}#business"} if page["slug"] == "" else org(L),
                  "areaServed": rv(r, "name", L),
                  "offers": {"@type": "AggregateOffer", "priceCurrency": "SAR",
                             "lowPrice": min(r["prices"].values()), "highPrice": max(r["prices"].values())}})
    if kind == "article":
        g.append({"@type": "Article", "headline": page["h1"], "description": page["desc"], "inLanguage": L,
                  "datePublished": page["date"], "dateModified": SITE["updated"], "mainEntityOfPage": absu(L, page["slug"]),
                  "author": {"@type": "Organization", "name": T[L]["name"]},
                  "publisher": {"@type": "Organization", "name": T[L]["name"]}})
    if page.get("faqs"):
        g.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": fill(q),
                  "acceptedAnswer": {"@type": "Answer", "text": fill(a)}} for q, a in page["faqs"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False)

# ---------------------------------------------------------------- layout
def layout(page, kind, body, trail, L, noindex=False):
    t = T[L]; O = t["other"]; slug = page["slug"]
    title = full_title(page["title"], L) if not noindex else page["title"]
    desc = fill(page["desc"])
    alt = ""; other_href = path(O, "")
    if not noindex and slug in SLUGS[O]:
        other_href = path(O, slug)
        alt = (f'<link rel="alternate" hreflang="ar" href="{absu("ar", slug)}">\n'
               f'<link rel="alternate" hreflang="en" href="{absu("en", slug)}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{absu("ar", slug)}">')
    nav = "".join(f'<a href="{path(L, s)}"{" aria-current=\"page\"" if s == slug else ""}>{esc(n)}</a>' for s, n in t["nav"])
    bc = ""
    if len(trail) > 1:
        bc = f'<nav class="crumbs" aria-label="{t["crumbs_label"]}"><ol>' + "".join(
            f'<li><a href="{path(L, s)}">{esc(n)}</a></li>' if i < len(trail) else f'<li aria-current="page">{esc(n)}</li>'
            for i, (s, n) in enumerate(trail, 1)) + "</ol></nav>"
    ga = ""
    if SITE["ga4_id"]:
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={SITE["ga4_id"]}"></script>'
              f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{SITE['ga4_id']}');</script>")
    gsc = f'<meta name="google-site-verification" content="{SITE["gsc_verification"]}">' if SITE["gsc_verification"] else ""
    pages = {p["slug"]: p for p in t["pages"]}
    foot_routes = "".join(f'<li><a href="{path(L, s)}">{esc(pages[s]["h1"])}</a></li>' for s in SERVICE_ORDER)
    foot_blog = "".join(f'<li><a href="{path(L, a["slug"])}">{esc(a["crumb"])}</a></li>' for a in t["articles"])
    robots = "noindex" if noindex else "index,follow,max-image-preview:large"
    return f'''<!doctype html>
<html lang="{L}" dir="{t["dir"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{absu(L, slug)}">
{alt}
<meta name="robots" content="{robots}">
<meta property="og:type" content="{'article' if kind == 'article' else 'website'}">
<meta property="og:locale" content="{t["og"]}">
<meta property="og:site_name" content="{esc(t['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{absu(L, slug)}">
<meta name="theme-color" content="#0f3b35">
{gsc}
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;700&display=swap">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{schema(page, kind, trail, L)}</script>
{ga}
</head>
<body>
<header class="top">
 <div class="wrap bar">
  <a class="brand" href="{path(L, '')}">{LOGO}<span>{esc(t['name'])}</span></a>
  <button class="menu-btn" aria-expanded="false" aria-controls="nav" aria-label="{t['menu']}"><span></span><span></span><span></span></button>
  <nav id="nav" class="nav">{nav}<a class="lang" href="{other_href}" hreflang="{O}" lang="{O}">{t['switch']}</a><a class="btn wa sm" href="{wa(t['wa_msg'])}" data-ev="whatsapp_click">{ICON_WA}<span>{t['wa']}</span></a></nav>
 </div>
</header>
<main>
{bc}
{body}
</main>
<footer class="foot">
 <div class="wrap cols">
  <div><a class="brand" href="{path(L, '')}">{LOGO}<span>{esc(t['name'])}</span></a>
   <p>{esc(t['foot_p'])}</p>
   <p><a href="tel:+{SITE['phone']}" data-ev="phone_click">{ICON_PHONE} <span dir="ltr">{esc(SITE['phone_display'])}</span></a></p>
   <p><a href="{other_href}" hreflang="{O}" lang="{O}">{t['switch']}</a></p></div>
  <div><h2>{t['foot_routes']}</h2><ul>{foot_routes}<li><a href="{path(L, 'prices/')}">{t['price_list']}</a></li></ul></div>
  <div><h2>{t['foot_info']}</h2><ul>{foot_blog}<li><a href="{path(L, 'contact/')}">{t['book_now']}</a></li></ul></div>
 </div>
 <p class="copy wrap">© 2026 {esc(t['name'])}</p>
</footer>
<div class="sticky">
 <a class="btn call" href="tel:+{SITE['phone']}" data-ev="phone_click">{ICON_PHONE}<span>{t['call']}</span></a>
 <a class="btn wa" href="{wa(t['wa_msg'])}" data-ev="whatsapp_click">{ICON_WA}<span>{t['sticky_wa']}</span></a>
</div>
<script src="/assets/app.js" defer></script>
</body>
</html>'''

# ---------------------------------------------------------------- page bodies
def service_body(p, L):
    t = T[L]; r = ROUTES[p["route"]]
    facts = [f'{minp(p["route"])} {t["sar"]}', rv(r, "km", L), rv(r, "time", L), "24/7"]
    fl = "".join(f"<li><b>{esc(v)}</b><span>{esc(k)}</span></li>" for v, k in zip(facts, t["facts"]))
    hero = f'''<section class="hero"><div class="wrap hero-grid">
<div class="hero-text"><h1>{esc(p["h1"])}</h1><p class="lead">{esc(fill(p["lead"]))}</p>
<ul class="facts">{fl}</ul>
<div class="cta"><a class="btn wa" href="{wa(t['wa_msg_p'] + p['h1'])}" data-ev="whatsapp_click">{ICON_WA}<span>{t['wa_book']}</span></a>
<a class="btn ghost" href="tel:+{SITE['phone']}" data-ev="phone_click">{ICON_PHONE}<span dir="ltr">{esc(SITE['phone_display'])}</span></a></div></div>
{booking_form(p["route"], L)}
</div></section>'''
    secs = "".join(render_section(s, p, L) for s in p["sections"])
    return hero + f'<div class="wrap content">{secs}{faq_html(p["faqs"], L)}</div>'

def simple_hero(p, extra=""):
    return (f'<section class="hero slim"><div class="wrap"><h1>{esc(p["h1"])}</h1>'
            f'<p class="lead">{esc(fill(p["lead"]))}</p>{extra}</div></section>')

def cta_box(L):
    t = T[L]
    return (f'<aside class="cta-box"><h2>{t["cta_h"]}</h2><p>{t["cta_p"].format(p=minp("airport_makkah"))}</p>'
            f'<a class="btn wa" href="{wa(t["cta_msg"])}" data-ev="whatsapp_click">{ICON_WA}<span>{t["wa_book"]}</span></a> '
            f'<a class="btn ghost" href="{path(L, "prices/")}">{t["prices_btn"]}</a></aside>')

def article_body(a, L):
    meta = f'<p class="meta">{T[L]["updated"]} <time datetime="{SITE["updated"]}">{SITE["updated"]}</time></p>'
    secs = "".join(render_section(s, a, L) for s in a["sections"])
    return simple_hero(a, meta) + f'<div class="wrap content narrow">{secs}{cta_box(L)}{faq_html(a["faqs"], L)}</div>'

def prices_body(p, L):
    secs = "".join(render_section(s, p, L) for s in p["sections"])
    return simple_hero(p) + f'<div class="wrap content">{secs}{faq_html(p["faqs"], L)}</div>'

def contact_body(p, L):
    t = T[L]
    info = (f'<div class="contact-info"><h2>{t["contact_h"]}</h2>'
            f'<a class="btn wa" href="{wa(t["wa_msg"])}" data-ev="whatsapp_click">{ICON_WA}<span>{t["contact_wa"]}</span></a>'
            f'<a class="btn ghost" href="tel:+{SITE["phone"]}" data-ev="phone_click">{ICON_PHONE}<span dir="ltr">{esc(SITE["phone_display"])}</span></a>'
            f'<p>{t["contact_p"]}</p></div>')
    return simple_hero(p) + f'<div class="wrap content contact-grid">{booking_form(p["route"], L, True)}{info}</div>'

def blog_index(L):
    t = T[L]; p = dict(t["blog_page"], slug="blog/")
    cards = "".join(f'<a class="card" href="{path(L, a["slug"])}"><h3>{esc(a["h1"])}</h3><p>{esc(a["desc"])}</p><span>{t["read"]}</span></a>' for a in t["articles"])
    return p, simple_hero(p) + f'<div class="wrap content"><div class="cards">{cards}</div></div>'

# ---------------------------------------------------------------- write
def write(rel, text):
    fp = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f: f.write(text)

def build_lang(L):
    t = T[L]; pre = t["prefix"]; home = ("", t["home"]); urls = []
    for p in t["pages"]:
        trail = [home] if p["slug"] == "" else [home, (p["slug"], p["crumb"])]
        body = {"service": service_body, "prices": prices_body, "contact": contact_body}[p["kind"]](p, L)
        write(pre + p["slug"] + "index.html", layout(p, p["kind"], body, trail, L))
        urls.append((L, p["slug"], "1.0" if p["slug"] == "" else "0.8"))
    bp, bbody = blog_index(L)
    write(pre + "blog/index.html", layout(bp, "blog", bbody, [home, ("blog/", t["blog"])], L)); urls.append((L, "blog/", "0.5"))
    for a in t["articles"]:
        write(pre + a["slug"] + "index.html",
              layout(a, "article", article_body(a, L), [home, ("blog/", t["blog"]), (a["slug"], a["crumb"])], L))
        urls.append((L, a["slug"], "0.7"))
    return urls

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    urls = build_lang("ar") + build_lang("en")
    nf = dict(T["ar"]["nf"], slug="404", desc=T["ar"]["nf"]["title"])
    write("404.html", layout(nf, "404", simple_hero(nf) + f'<div class="wrap content">{route_cards("", "ar")}</div>',
                             [("", T["ar"]["home"])], "ar", noindex=True))
    sm = "".join(f"<url><loc>{absu(L, s)}</loc><lastmod>{SITE['updated']}</lastmod><priority>{pr}</priority></url>" for L, s, pr in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {D}/sitemap.xml\n")
    print(f"✓ built {len(urls)} pages (ar + en) + 404 → {OUT}")

if __name__ == "__main__":
    main()
