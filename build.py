#!/usr/bin/env python3
"""JR LIQUOR MART (Camarillo, CA) — one Python generator -> ONE-PAGE site + sitemap/robots.
Run:  python3 build.py    (emits index.html + redirect stubs for the old page URLs)
Edit CONTENT here, never hand-edit the generated HTML. Deploy = git push (GitHub Pages).

Built from Wyatt's site-template (see that repo's PLAYBOOK.md). Content is sourced from
the 2026-07-26 research brief (docs/RESEARCH_BRIEF.md): every claim traces to a public
source or the owner. House rules: no fabricated content, no em dashes.

Decisions (2026-07-26, confirmed with Wyatt): dark default + amber/bourbon palette,
Fraunces display; ONE-PAGE layout (was 5 pages; old URLs 301-style stub-redirect to the
matching section); sections = hero, order band, marquee, What We Carry (6 cards),
Gallery, Why, About, Reviews (real verbatim quotes), Contact + map; ORDER buttons link
the store's VERIFIED delivery storefronts (it lists as "JR Food Mart" on Uber Eats and
Postmates, "Jr Liquor & Convenience" on Grubhub; no DoorDash storefront found);
hybrid AI chatbot (worker/ on chat.jrliquormart.com, canned fallback until deployed).
"""

# ============================ CONFIG ============================
import json
from datetime import date

CSSV = "styles.css?v=7"   # bump on ANY css change
JSV  = "app.js?v=2"       # bump on ANY app.js change
CHATV= "chat.js?v=2"      # bump on ANY chat.js change (hybrid AI mode: WORKER_URL in chat.js)

BIZ      = "JR Liquor Mart"
INITIAL  = "JR"                                  # placeholder logo letters (until a real logo drops in)
TAG      = "Old Town Camarillo's neighborhood liquor store since 1997"
CITY     = "Camarillo, CA"
ADDR     = "2616 E Ventura Blvd Unit 106, Camarillo, CA 93010"
PHONE    = "805-388-3288"
PHONE_TEL= "+18053883288"
# TODO: owner's real inbox pending (intake: "I'll provide their email later").
# The form will NOT deliver until this is set to the real lowercase address and the
# owner clicks FormSubmit's one-time activation link (PLAYBOOK §7). Email is hidden
# from the visible pages until then (see footer()/contact()).
EMAIL    = "inbox@example.com"
EMAIL_READY = False                              # flip True once the real inbox is set above
HOURS    = "Open daily 8am-10pm"                 # Apple Maps listing; Sunday verified on Google
DOMAIN   = "jrliquormart.com"
MAPS     = "https://maps.google.com/?q=" + ADDR.replace(" ", "+")
MAP_EMBED= "https://www.google.com/maps?q=" + ADDR.replace(" ", "+") + "&output=embed"
# socials — set to "" to hide a link
INSTAGRAM= "https://www.instagram.com/jrliquormart"
FACEBOOK = ""
TIKTOK   = ""

# ---- SEO: canonical base + share image + LocalBusiness structured data ----
# TODO per-site: add a 1200x630 assets/og-image.jpg + assets/logo.png (none exist yet).
# NOTE: no aggregateRating on purpose — never add one without owner-verified live counts.
BASE   = f"https://{DOMAIN}"
OG_IMG = f"{BASE}/assets/og-image.jpg"
_ap = [x.strip() for x in ADDR.split(",")]
_rp = (_ap[2] if len(_ap) > 2 else "").split()
LD_JSON = json.dumps({
  "@context":"https://schema.org","@type":["LiquorStore","LocalBusiness"],"@id":f"{BASE}/#business",
  "name":BIZ,"description":f"{TAG}. Bourbon and whiskey, a walk-in beer cooler, tequila, wine and snacks.",
  "image":OG_IMG,"logo":f"{BASE}/assets/logo.png",
  "url":f"{BASE}/","telephone":PHONE_TEL,"priceRange":"$",
  "address":{"@type":"PostalAddress","streetAddress":_ap[0] if _ap else ADDR,
             "addressLocality":_ap[1] if len(_ap) > 1 else "","addressRegion":_rp[0] if _rp else "",
             "postalCode":_rp[1] if len(_rp) > 1 else "","addressCountry":"US"},
  "hasMap":MAPS,
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification",
    "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens":"08:00","closes":"22:00"}],
  "sameAs":[s for s in (INSTAGRAM,FACEBOOK,TIKTOK) if s],
}, separators=(",",":"))

# One-page nav: anchors into index.html sections. The animated "Call the store" button
# stays the primary CTA (call-first business, one CTA intent site-wide).
NAV = [("#top","Home"),("#carry","What We Carry"),("#gallery","Gallery"),
       ("#about","About"),("#contact","Contact")]
FOOT_NAV = NAV

# ---- dark-mode: default dark, toggle persists to localStorage ----
FOUC   = '<script>(function(){try{var t=localStorage.getItem("theme")||"dark";document.documentElement.setAttribute("data-theme",t);}catch(e){}})();</script>'
SUN    = '<svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.4M12 19.6V22M4.2 4.2l1.7 1.7M18.1 18.1l1.7 1.7M2 12h2.4M19.6 12H22M4.2 19.8l1.7-1.7M18.1 5.9l1.7-1.7"/></svg>'
MOON   = '<svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z"/></svg>'
TOGGLE = f'<button class="theme-toggle" type="button" aria-label="Toggle dark mode" title="Toggle theme">{SUN}{MOON}</button>'

# ---- ultra-light line icons (no emoji). Add more as needed. ----
def _svg(p):
    return f'<svg class="ic-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
ICON = {
 "bottle": _svg('<path d="M10 2.5h4M10.5 2.5v3.2L9 9v11a1.5 1.5 0 0 0 1.5 1.5h3A1.5 1.5 0 0 0 15 20V9l-1.5-3.3V2.5"/><path d="M9 13.5h6M9 17h6"/>'),
 "beer":   _svg('<path d="M6.5 8.5h9V20a1.5 1.5 0 0 1-1.5 1.5H8A1.5 1.5 0 0 1 6.5 20z"/><path d="M15.5 10.5H18a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-2.5"/><path d="M6.5 8.5c-.5-3 1-6 4.5-6 1.6 0 2.4.7 2.9 1.6.4-.2.9-.3 1.3-.3 1.6 0 2.8 1.2 2.8 2.7 0 .8-.4 1.5-1 2"/>'),
 "shot":   _svg('<path d="M8 8.5h8L14.7 21a1 1 0 0 1-1 .9h-3.4a1 1 0 0 1-1-.9z"/><path d="M9 12.5h6"/><circle cx="17" cy="4.5" r="2.3"/><path d="M17 2.2v4.6M14.7 4.5h4.6"/>'),
 "wine":   _svg('<path d="M8 2.5h8c0 5.2-1.6 8.5-4 8.5s-4-3.3-4-8.5z"/><path d="M12 11v9M8.5 21.5h7M8.4 6h7.2"/>'),
 "bag":    _svg('<path d="M6 7.5h12l1 12.5a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z"/><path d="M9 10.5V6a3 3 0 0 1 6 0v4.5"/>'),
 "truck":  _svg('<path d="M10 17h4V5H2v12h3M20 17h2v-3.34a4 4 0 0 0-1.17-2.83L19 9h-5v8h1"/><circle cx="7.5" cy="17.5" r="2"/><circle cx="17.5" cy="17.5" r="2"/>'),
 "pin":    _svg('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.5"/>'),
 "snow":   _svg('<path d="M12 3v18M12 3l-2.2 2.2M12 3l2.2 2.2M12 21l-2.2-2.2M12 21l2.2-2.2M4.2 7.5l15.6 9M4.2 7.5l3 .3M4.2 7.5l.3 3M19.8 16.5l-3-.3M19.8 16.5l-.3-3M19.8 7.5L4.2 16.5M19.8 7.5l-3 .3M19.8 7.5l.3 3M4.2 16.5l3-.3M4.2 16.5l.3-3"/>'),
 "star":   _svg('<path d="M12 2l3 6.5 7 .9-5 4.8 1.3 7L12 18l-6.6 3.2L6.7 14 1.7 9.4l7-.9z"/>'),
 "heart":  _svg('<path d="M20.8 5.6a5.5 5.5 0 0 0-7.8 0L12 6.5l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.8 1-1a5.5 5.5 0 0 0 0-7.6z"/>'),
}
def icon(name): return ICON.get(name, "")

# ============================ CONTENT DATA ============================
# What we carry: (id, icon, title, short-blurb-for-home-cards, long-copy-for-carry-page, [bullets])
# Copy is grounded in public reviews and the owner's Yelp blurb (see docs/RESEARCH_BRIEF.md).
SERVICES = [
 ("bourbon-whiskey","bottle","Bourbon & Whiskey","A wall of bourbon and whiskey, everyday pours to top-shelf finds.",
  "The bourbon wall is the corner of the store customers talk about most. Everyday labels sit next to top-shelf sippers, and the shelf changes, so if you're hunting a specific bottle, call ahead and we'll check it for you.",
  ["The bourbon wall","Top-shelf selections","Everyday go-tos","Call ahead to check a bottle"]),
 ("beer-cave","beer","The Beer Cave","A walk-in cooler stacked cold, with a serious IPA section.",
  "The walk-in cooler is the store's calling card. Everything inside is cold, the shelves stay stocked, and the IPA section runs deep. Walk in, grab what's cold, go.",
  ["Walk-in beer cave","A deep IPA section","Always cold","Always stocked"]),
 ("tequila-agave","shot","Tequila & Agave","Margarita staples to sipping bottles on the agave shelf.",
  "From margarita-night staples to bottles you sip slow, the agave shelf covers the range. Not sure what to grab? Ask at the counter and we'll point you right.",
  ["The agave shelf","Margarita staples","Sipping bottles","Ask at the counter"]),
 ("wine","wine","Wine","Reds, whites and bubbly for the table tonight.",
  "Wine and spirits at your disposal, in the store's own words. Grab a bottle for dinner, something to bring to the party, or ask the counter for a pick.",
  ["Reds and whites","Bubbly for celebrating","Bottles for tonight","Ask for a pick"]),
 ("snacks-extras","bag","Snacks & Extras","Snacks, cold sodas and energy drinks by the register.",
  "The quick-stop side of the store: snacks, cold sodas and energy drinks, right by the register. In and out in a minute, with free parking just outside the door.",
  ["Snacks","Cold sodas and energy drinks","In and out in a minute","Free parking lot outside"]),
 ("delivery-pickup","truck","Delivery & Pickup","Same-day delivery through the apps, or curbside pickup out front.",
  "Partnered with the delivery apps for same-day delivery, in the store's own words. Prefer to swing by? Curbside and in-store pickup are both easy, with Apple Pay and contactless at the register.",
  ["Same-day delivery via the apps","Curbside and in-store pickup","Apple Pay and contactless","Free parking lot"]),
]
# services() page card photos: id -> (assets file, alt). Licensed stock, generic alts.
_SVC_PHOTO = {
 "bourbon-whiskey": ("shelf","backbar-glow.jpg","Spirits lined up on a lit back bar"),
 "beer-cave":       ("cave","beer-ice.jpg","Beer bottles buried in ice"),
 "tequila-agave":   ("shelf","tequila-limes.jpg","Tequila shots with lime and salt"),
 "wine":            ("store","wine-dark.jpg","Wine bottles on a dark shelf"),
 "snacks-extras":   ("store","snack-wall.jpg","A wall of snacks"),
 "delivery-pickup": ("store","delivery-bag.jpg","A bottle packed in a paper carrier bag"),
}

# why-choose-us: (icon, title, body) — each grounded in a quoted public review
FEATURES = [
 ("pin","Old Town local","On E Ventura Blvd in Old Town Camarillo, on the same corner since 1997."),
 ("snow","Always cold","The walk-in Beer Cave keeps every bottle and can cold, all day."),
 ("star","Stocked and organized","Remodeled, clean and stocked deep, from the bourbon wall to the cooler."),
 ("heart","A counter that knows you","Fast, friendly service that treats regulars like friends."),
]

# gallery photos: (category, assets file, caption). LICENSED STOCK (Pexels, LICENSES.md).
# Captions stay generic on purpose: these are category shots, NOT photos of JR's own store.
# When the owner's real photos arrive, swap files and captions can finally say "our" shelves.
GALLERY = [
 ("shelf","top-shelf.jpg","The top shelf"),("cave","beer-ice.jpg","Buried in ice"),("shelf","back-bar.jpg","The back bar"),
 ("store","wine-cubbies.jpg","Wine, resting"),("cave","ice-cold-can.jpg","Ice cold"),("store","wine-rack.jpg","Reds in the rack"),
 ("shelf","backlit-bottles.jpg","Backlit bottles"),("cave","bottle-on-ice.jpg","Cold one, ready"),("store","snack-run.jpg","Snack run"),
]
GCATS = [("all","Everything"),("shelf","The Shelves"),("cave","Served Cold"),("store","Wine & Extras")]

# marquee: category chips only (intake decision). No brand-name claims until the owner
# confirms a stocked-brands list. ("txt", None, label) or ("img","file.png","Alt").
BRANDS = [("txt",None,"The Bourbon Wall"),("txt",None,"Walk-in Beer Cave"),("txt",None,"IPA Section"),
          ("txt",None,"Top Shelf Spirits"),("txt",None,"Wine"),("txt",None,"Snacks & Sodas")]
def brand_chip(kind, f, n):
    if kind == "img":
        return f'<span class="brand-chip"><img src="assets/{f}" alt="{n}" loading="lazy"></span>'
    return f'<span class="brand-chip brand-chip-txt">{n}</span>'

# ---- ORDER: VERIFIED live delivery storefronts (checked 2026-07-26). The store lists as
# "JR Food Mart" on Uber Eats/Postmates (same storefront) and "Jr Liquor & Convenience"
# on Grubhub, all at 2616 Ventura Blvd. NO DoorDash storefront was found in any search;
# add it here only with a real link from the owner. ----
ORDER = [   # order matters: red top-left, green top-right on phones (Wyatt's call)
 ("Grubhub",   "https://www.grubhub.com/restaurant/jr-liquor--convenience-2616-ventura-blvd-camarillo/2353021"),
 ("Uber Eats", "https://www.ubereats.com/store/jr-food-mart/49o0cIPyRlyIK4ThVzmOAQ"),
 ("Postmates", "https://postmates.com/store/jr-food-mart/49o0cIPyRlyIK4ThVzmOAQ"),
]
_ORDER_SLUG = {"doordash":"doordash","grubhub":"grubhub","uber eats":"ubereats","ubereats":"ubereats","postmates":"postmates"}
def order_bar(cls=""):
    if not ORDER: return ""
    btns = "".join(
        f'<a class="order-btn order-{_ORDER_SLUG.get(n.lower(),"pickup")}" href="{u}" target="_blank" rel="noopener">{n}<span class="btn-ic">&rarr;</span></a>'
        for n,u in ORDER)
    return f'<div class="order-bar{" "+cls if cls else ""}"><span class="order-lbl">Order delivery</span><div class="order-btns">{btns}</div></div>'

# REAL public reviews, quoted verbatim (sources in docs/RESEARCH_BRIEF.md).
# (name, context, quote, stars). Bracketed letters mark a corrected typo, nothing else is edited.
TESTIMONIALS = [
 ("Haley P.","Yelp review",
  "I love their IPA section. Everything is cold. They recently redesigned the place and everything looks nice, clean, and organized.",4),
 ("Vic H.","Yelp review",
  "Great service, good people behind the counter and always fast! I've been shopping at JR for about 3 years now and there has never been a problem!",5),
 ("Miguel A.","Yelp review",
  "They have a very large selection [of] liquor and beer. Prices are pretty reasonable. Easy parking and easy to get in and out.",4),
 ("Google reviewer","July 2022",
  "Brian and Alex stock a great shop! The renovations are awesome - huge bourbon selection, walk-in be[er] cooler, and a great new Pepsi setup with all the Gatorlyte I'm after.",5),
 ("Google reviewer","November 2022",
  "Newly remodeled inside. Looks great, always stocked and always cold.",5),
 ("Google reviewer","April 2022",
  "Very friendly and courteous staff, as well as top shelf selections. The JR Smoke Zone next door is excellent as well.",5),
]

# ============================ TILES (placeholder / real) ============================
def tile(cat, label, box=False):
    # CSS gradient placeholder — renders with NO image. Swap to photo() once assets exist.
    return (f'<figure class="tile tile-ph{" tile-box" if box else ""}" data-cat="{cat}">'
            f'<span class="tile-label">{label}</span><span class="tile-swap">photo</span></figure>')
def photo(cat, file, label, lightbox=False):
    # REAL image version. Drop {file} in assets/ and call this instead of tile().
    extra = f' data-full="assets/{file}"' if lightbox else ""
    role = ' role="button" tabindex="0"' if lightbox else ""
    return (f'<figure class="tile" data-cat="{cat}"{extra}{role}>'
            f'<img src="assets/{file}" alt="{label}" loading="lazy"><figcaption>{label}</figcaption></figure>')

# ============================ SHARED CHROME ============================
def head(title, desc, page="", path="index.html"):
    canon = f"{BASE}/{path}"
    return f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:url" content="{canon}">
<meta property="og:site_name" content="{BIZ}"><meta property="og:image" content="{OG_IMG}">
<meta property="og:locale" content="en_US"><meta name="theme-color" content="#b8791a">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMG}">
<link rel="icon" href="favicon.ico?v=2" sizes="48x48 32x32 16x16">
<link rel="icon" type="image/png" href="assets/favicon.png?v=2" sizes="256x256">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png?v=2">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{CSSV}">
<script type="application/ld+json">{LD_JSON}</script>
{FOUC}
</head><body class="{page}">
<a class="skip" href="#main">Skip to content</a>'''

def brandmark(cls=""):
    # Placeholder logo = gradient initials square + wordmark. Swap the <span class="brand-b"> for
    # <img src="assets/logo.png"> once a real logo exists.
    return (f'<a class="brand {cls}" href="index.html" aria-label="{BIZ} home">'
            f'<span class="brand-b">{INITIAL}</span><span class="brand-name">{BIZ}</span></a>')

def nav(active):
    links = "".join(
        '<a href="{}"{}>{}</a>'.format(h, ' class="active"' if h == active else "", t)
        for h, t in NAV)
    mlinks = "".join(f'<a href="{h}">{t}</a>' for h,t in NAV)
    return f'''<div class="nav-shell"><header class="nav"><div class="nav-in">
  {brandmark()}
  <nav class="nav-links">{links}</nav>
  {TOGGLE}
  <a class="btn btn-primary btn-sm nav-cta cta-anim" href="tel:{PHONE_TEL}">Call the store<span class="btn-ic">&rarr;</span></a>
  <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header></div>
<div class="mobile-menu" id="mobile-menu">{mlinks}<a class="btn btn-primary cta-anim" href="tel:{PHONE_TEL}">Call the store<span class="btn-ic">&rarr;</span></a></div>'''

# NOTE: the template's cta() closing band was cut in the one-page merge: the #contact
# section (big phone card + form + map) is the page's closer, and a "call ahead" band
# stacked right after it repeated the same message.

def _social():
    out = []
    if INSTAGRAM: out.append(f'<a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a>')
    if FACEBOOK:  out.append(f'<a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a>')
    if TIKTOK:    out.append(f'<a href="{TIKTOK}" target="_blank" rel="noopener">TikTok</a>')
    return "".join(out)

def chat_widget():
    return '''<div class="cw" id="cw">
  <button class="cw-bubble" id="cw-bubble" type="button" aria-label="Open assistant" aria-expanded="false" aria-controls="cw-panel">
    <svg class="cw-i cw-i-chat" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 21l2.1-5.4A8.5 8.5 0 1 1 21 11.5Z"/></svg>
    <svg class="cw-i cw-i-x" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
  </button>
  <div class="cw-panel" id="cw-panel" role="dialog" aria-modal="false" aria-labelledby="cw-title" hidden>
    <div class="cw-head"><span class="cw-avatar" aria-hidden="true">''' + INITIAL + '''</span>
      <div class="cw-head-t"><strong id="cw-title">JR Assistant</strong><span><span class="cw-dot"></span> Ask about hours, delivery, or what we carry</span></div>
      <button class="cw-x-btn" id="cw-close" type="button" aria-label="Close chat"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    </div>
    <div class="cw-log" id="cw-log" role="log" aria-live="polite" aria-label="Chat messages"></div>
    <form class="cw-form" id="cw-form" autocomplete="off">
      <label for="cw-input" class="sr-only">Type your message</label>
      <input id="cw-input" class="cw-input" type="text" placeholder="Type your message..." maxlength="600" autocomplete="off">
      <button class="cw-send" id="cw-send" type="submit" aria-label="Send message"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
    </form>
    <p class="cw-note">AI assistant, answers can be off. Don't share passwords or card numbers.</p>
  </div>
</div>'''

def footer():
    cols = "".join(f'<a href="{h}">{t}</a>' for h,t in FOOT_NAV)
    email_line = f'<a href="mailto:{EMAIL}">{EMAIL}</a>' if EMAIL_READY else ""
    return f'''<footer><div class="wrap foot-grid">
  <div class="foot-brand">{brandmark("brand-foot")}
    <p>{TAG}.</p>
    <div class="foot-social">{_social()}</div>
  </div>
  <div class="foot-col"><h5>Explore</h5>{cols}</div>
  <div class="foot-col"><h5>Visit</h5>
    <a href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a>
    <a href="tel:{PHONE_TEL}">{PHONE}</a>
    {email_line}
    <span class="foot-note">{HOURS}</span>
    <span class="foot-note">Next door: JR Smoke Zone</span>
  </div>
</div>
<div class="legal wrap"><span>&copy; 2026 {BIZ}. All rights reserved.</span><span>21+ only. Please drink responsibly.</span></div>
</footer>
<div class="callbar" aria-label="Contact us">
  <a href="tel:{PHONE_TEL}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>Call us</a>
  <a href="sms:{PHONE_TEL}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 21l2.1-5.4A8.5 8.5 0 1 1 21 11.5Z"/></svg>Text us</a>
</div>
{chat_widget()}
<script src="{JSV}"></script>
<script src="{CHATV}"></script></body></html>'''

# ============================ THE PAGE (one-page site) ============================
def home():
    brow = "".join(brand_chip(*b) for b in BRANDS); brands = brow + brow
    feats = "".join(f'<div class="feat"><span class="ic-badge">{icon(k)}</span><h3>{t}</h3><p>{d}</p></div>' for k,t,d in FEATURES)
    tst = "".join(
        f'<blockquote class="tst"><div class="tst-stars">{"★"*s}</div><p>&ldquo;{q}&rdquo;</p><cite>{n}<span>{r}</span></cite></blockquote>'
        for n,r,q,s in TESTIMONIALS)
    cards = ""
    for sid,ic,title,short,long,bullets in SERVICES:
        bl = "".join(f"<li>{b}</li>" for b in bullets)
        pcat, pfile, palt = _SVC_PHOTO.get(sid, ("store","snack-wall.jpg",title))
        # Cards are informational; the ONE order-button cluster lives in the hero, and the
        # nav CTA + callbar always offer the call. No per-card buttons.
        act = ""
        cards += f'''<article class="prod-card" id="{sid}">
        <div class="prod-img">{photo(pcat,pfile,palt)}</div>
        <div class="prod-body"><span class="ic-badge">{icon(ic)}</span><h2>{title}</h2>
        <p>{long}</p><ul class="ticks">{bl}</ul>
        {act}</div>
      </article>'''
    filt = "".join(f'<button class="gfilter{" active" if c=="all" else ""}" data-cat="{c}">{t}</button>' for c,t in GCATS)
    tiles = "".join(photo(c,f,l,lightbox=True) for c,f,l in GALLERY)
    svc_opts = "".join(f"<option>{s[2]}</option>" for s in SERVICES)
    return head(f"{BIZ} | Liquor Store in Old Town Camarillo, CA",
                f"{TAG}. The bourbon wall, the walk-in Beer Cave, wine, tequila and snacks, with same-day delivery. Call {PHONE}.",
                "home","") + nav("#top") + f'''
<main id="main">
<section class="hero" id="top"><div class="wrap hero-in">
  <div class="hero-copy reveal">
    <span class="eyebrow">Old Town Local &middot; Est. 1997</span>
    <h1>The bourbon wall, the <span class="hl">Beer Cave</span>, and a counter that knows your name.</h1>
    <p>Keeping Old Town Camarillo stocked and cold since 1997, with same-day delivery and curbside pickup.</p>
    <div class="hero-btns"><a class="btn btn-primary btn-lg cta-anim" href="tel:{PHONE_TEL}">Call the store<span class="btn-ic">&rarr;</span></a>
    <a class="btn btn-ghost btn-lg" href="#carry">See what we carry</a></div>
    {order_bar()}
  </div>
  <div class="hero-art reveal d1"><div class="hero-frame">{photo("shelf","hero-shelf.jpg","Bottles glowing on an amber-lit shelf")}</div></div>
</div></section>

<section class="section" id="carry"><div class="wrap">
  <div class="sec-head center reveal">
    <h2>One good stop, corner to corner</h2>
    <p>Hunting a specific bottle? Call and we'll check the shelf before you drive over.</p></div>
  <div class="prod-grid stagger reveal">{cards}</div>
</div></section>

<section class="section band" id="gallery"><div class="wrap">
  <div class="sec-head center reveal"><h2>A taste of the good stuff</h2>
    <p>Licensed stock shots holding the spot until we shoot the real shelves.</p></div>
  <div class="gfilters reveal">{filt}</div>
  <div class="gal-grid gal-masonry" id="gal">{tiles}</div>
</div></section>

<section class="brands"><div class="wrap brands-in">
  <span class="brands-label">Inside the store</span>
  <div class="brands-marquee"><div class="brands-track">{brands}</div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head center reveal"><h2>Why Camarillo keeps coming back</h2></div>
  <div class="feat-grid stagger reveal">{feats}</div>
</div></section>

<section class="section band" id="about"><div class="wrap about-in">
  <div class="about-copy reveal">
    <h2>Old Town local since 1997</h2>
    <p class="lead">JR Liquor Mart has held down the same corner of E Ventura Blvd since 1997.</p>
    <p>The store got a full remodel a few years back, and customers noticed: clean, organized, stocked deep and always cold. The bourbon wall and the walk-in Beer Cave are the two corners people talk about most, and the counter treats regulars like friends.</p>
    <p>Next door is JR Smoke Zone, our sister shop. Between the two, this corner of Old Town has you covered.</p>
    <div class="about-facts">
      <div><strong>1997</strong><span>On this corner since</span></div>
      <div><strong>8am-10pm</strong><span>Open daily</span></div>
      <div><strong>Old Town</strong><span>E Ventura Blvd, Camarillo</span></div>
    </div>
  </div>
  <div class="about-art reveal d1"><div class="art-frame">{photo("store","night-window.jpg","Bottles in a shop window at night")}</div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">Real reviews</span><h2>What customers say</h2>
    <p class="sample-note">Quoted word for word from public Yelp and Google reviews.</p></div>
  <div class="tst-grid stagger reveal">{tst}</div>
</div></section>

<section class="section band" id="contact"><div class="wrap">
  <div class="sec-head center reveal"><h2>Come by or call</h2>
    <p>2616 E Ventura Blvd Unit 106, in Old Town Camarillo. {HOURS}.</p></div>
  <div class="contact-in">
  <form class="cform reveal" action="https://formsubmit.co/{EMAIL}" method="POST">
    <input type="hidden" name="_subject" value="New message from jrliquormart.com">
    <input type="hidden" name="_template" value="table">
    <input type="text" name="_honey" style="display:none">
    <div class="f-row"><label>Name<input name="name" required></label>
    <label>Phone<input name="phone" type="tel"></label></div>
    <label>Email<input name="email" type="email" required></label>
    <label>What are you after?
      <select name="category"><option value="">Pick one</option>{svc_opts}<option>Something else</option></select></label>
    <label>What can we check for you?<textarea name="message" rows="5" placeholder="Bottle, brand, size, when you need it..."></textarea></label>
    <button class="btn btn-primary btn-lg" type="submit">Send it<span class="btn-ic">&rarr;</span></button>
    <p class="form-fine">Fastest answer: call or text {PHONE}.</p>
  </form>
  <aside class="contact-side reveal d1">
    <div class="cside-card"><h3>Call or text</h3><a class="big-phone" href="tel:{PHONE_TEL}">{PHONE}</a></div>
    <div class="cside-card"><h3>Delivery &amp; pickup</h3><p>Same-day delivery through the apps up top (we're listed as JR Food Mart), or park free in the lot and come in.</p></div>
    <div class="cside-card"><h3>Visit</h3><p>{ADDR}</p><a href="{MAPS}" target="_blank" rel="noopener">Get directions &rarr;</a></div>
    <div class="cside-card"><h3>Hours</h3><p>{HOURS}</p></div>
    <div class="cside-card"><h3>Follow</h3><div class="cside-social">{_social()}</div></div>
  </aside>
  </div>
</div></section>
<section class="map-sec"><iframe src="{MAP_EMBED}" title="{BIZ} location map" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></section>
</main>
<div class="lightbox" id="lightbox" aria-hidden="true"><button class="lb-close" aria-label="Close">&times;</button><img src="" alt=""></div>
{footer()}'''

# ============================ BUILD ============================
PAGES = {"index.html": home}
# Old multi-page URLs live on as instant redirects into their one-page sections
# (kept out of the sitemap, noindexed, canonical -> the front page).
STUBS = {"services.html":("#carry","What We Carry"),"gallery.html":("#gallery","Gallery"),
         "about.html":("#about","About"),"contact.html":("#contact","Contact")}

def stub(anchor, title):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | {BIZ}</title><meta name="robots" content="noindex">
<link rel="canonical" href="{BASE}/">
<meta http-equiv="refresh" content="0;url=index.html{anchor}">
</head><body><p>This page moved to the front page. <a href="index.html{anchor}">Continue to {BIZ}</a>.</p></body></html>'''

def sitemap():
    today = date.today().isoformat()
    return (f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"<url><loc>{BASE}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url></urlset>")

def build():
    for fn, f in PAGES.items():
        open(fn,"w",encoding="utf-8").write(f())
    for fn,(anchor,title) in STUBS.items():
        open(fn,"w",encoding="utf-8").write(stub(anchor,title))
    open("sitemap.xml","w",encoding="utf-8").write(sitemap())
    open("robots.txt","w",encoding="utf-8").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    print("built: index.html + redirect stubs:", ", ".join(STUBS), "+ sitemap.xml, robots.txt")

if __name__ == "__main__":
    build()
