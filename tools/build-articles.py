#!/usr/bin/env python3
"""Rebuild the /articles/ directory for championautofinance.github.io.

Fetches the LIVE sitemap from championautofinance.com, so the directory,
search index, and github.io sitemap auto-expand as new articles go live.
Reuses the head/nav/footer chrome from privacy-policy/index.html (the same
WP-mirror CSS as the other backlink pages) and emits a hub page + category
pages whose links all point at the live articles on championautofinance.com.

Run from anywhere: python3 tools/build-articles.py
Also run weekly by .github/workflows/build-articles.yml.
"""
import re, html, pathlib, collections, sys, urllib.request

REPO = pathlib.Path(__file__).resolve().parents[1]
OUT = REPO / "articles"
TPL = (REPO / "privacy-policy" / "index.html").read_text(encoding="utf-8")
LIVE = "https://championautofinance.com"
GH = "https://championautofinance.github.io"

req = urllib.request.Request(
    LIVE + "/sitemap.xml",
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36 CAFS-articles-builder"})
try:
    sitemap = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
except Exception as e:
    sys.exit(f"FATAL: could not fetch live sitemap: {e}")
SLUGS = [m.rstrip("/") for m in re.findall(r"<loc>https://championautofinance\.com/([^<]+)</loc>", sitemap)]
SLUGS = [s for s in SLUGS if s]
CORE = {"how-it-works", "lease-buyouts-refinancing", "dealer-partners", "faqs",
        "contact-us", "privacy-policy", "terms-of-service"}
SLUGS = sorted(set(s for s in SLUGS if s not in CORE))
if len(SLUGS) < 100:
    sys.exit(f"FATAL: only {len(SLUGS)} slugs found in live sitemap — refusing to rebuild")

# ---------------- template split ----------------
head_nav, _, rest = TPL.partition('      <header class="entry-header')
assert rest, "entry-header anchor not found"
_, sep, tail = TPL.partition("\t</main><!-- #main -->")
assert sep, "main-close anchor not found"
tail = sep + tail

# strip privacy-specific feed/oembed lines from the head
head_nav = "\n".join(
    l for l in head_nav.split("\n")
    if "privacy-policy/feed/" not in l and "oembed" not in l
)

def page_html(fname, h1, title, desc, body):
    h = head_nav
    h = h.replace("<title>Privacy Policy &#8211; Champion Auto Finance</title>",
                  f"<title>{html.escape(title)} &#8211; Champion Auto Finance</title>")
    h = h.replace('content="Champion Auto Finance privacy policy and information handling practices."',
                  f'content="{html.escape(desc, quote=True)}"')
    canon = f"{GH}/articles/" if fname == "index.html" else f"{GH}/articles/{fname}"
    h = h.replace(f'<link rel="canonical" href="{GH}/privacy-policy/" />',
                  f'<link rel="canonical" href="{canon}" />')
    h = h.replace('class="privacy-policy wp-singular page-template-default page page-id-3 ',
                  'class="articles wp-singular page-template-default page ')
    header = f'''      <header class="entry-header single-page-header " >
      <div class="row single-page-heading blog-title-left ">
                          <div class="container">
                           <h1 class="section-heading" >{h1}</h1>
                    </div>
      </div>
    </header>

<div id="primary" class="content-area" style="">
\t<main id="main" class="site-main" role="main">

<section id="single-page" class="section articles" style="">
    <div class="container">
\t\t\t<div class="row single-page-content">
<style>
.caf-cols{{columns:3;column-gap:2.5rem;list-style:none;padding-left:0;margin:0 0 2em}}
.caf-cols li{{break-inside:avoid;margin:0 0 .55em}}
@media(max-width:991px){{.caf-cols{{columns:2}}}}
@media(max-width:600px){{.caf-cols{{columns:1}}}}
.caf-cat-list{{list-style:none;padding-left:0}}
.caf-cat-list li{{margin:0 0 1em}}
.caf-cat-list .caf-count{{color:#777;font-size:.9em}}
.caf-search{{margin:0 0 2em}}
.caf-search input{{width:100%;max-width:480px;padding:12px 16px;border:1px solid #ccc;border-radius:4px;font-family:inherit;font-size:1em}}
#caf-search-count{{margin:.75em 0;color:#555}}
</style>
<div class="caf-search">
<input type="search" id="caf-search-input" placeholder="Search all {len(SLUGS)} articles&hellip;" aria-label="Search articles" autocomplete="off">
<p id="caf-search-count" hidden></p>
<ul id="caf-search-results" class="caf-cols" hidden></ul>
</div>
<script src="search-index.js" defer></script>
<script src="search.js" defer></script>
{body}
\t\t\t</div>
    </div>
</section>

'''
    (OUT / fname).write_text(h + header + tail, encoding="utf-8")

# ---------------- titles ----------------
UPPER = {"nj", "ny", "pa", "llc", "ev", "suv", "bmw", "gmc", "vw", "usaa", "nmac",
         "dcu", "faq", "faqs", "bhph", "wrx", "mdx", "rdx", "tlx", "glc", "gle",
         "gla", "glb", "ct", "de", "md", "id", "apr", "gap", "ach", "pti", "lti", "dti",
         "es", "nx", "rx", "ux", "xt5", "gv70", "gv80", "eqe", "eqs", "td", "ssi", "id4"}
KEEP = {"a": "a", "an": "an", "and": "and", "at": "at", "for": "for", "in": "in",
        "is": "Is", "it": "It", "my": "My", "of": "of", "or": "or", "the": "the",
        "to": "to", "vs": "vs.", "with": "with", "after": "After", "out": "Out"}
FIX = [("Mercedes Benz", "Mercedes-Benz"), ("E Tron", "e-tron"), ("Land Rover", "Land Rover"),
       ("F 150", "F-150"), ("Cr V", "CR-V"), ("Hr V", "HR-V"), ("Rav4", "RAV4"),
       ("Id 4", "ID.4"), ("Mach E", "Mach-E"), ("Cx 5", "CX-5"), ("Cx 30", "CX-30"),
       ("Cx 50", "CX-50"), ("Ioniq 5", "Ioniq 5"), ("Buy Here Pay Here", "Buy Here Pay Here"),
       ("1099", "1099"), ("Alfa Romeo", "Alfa Romeo"), ("Xc60", "XC60"), ("Xc90", "XC90"),
       ("Xc40", "XC40"), ("X1", "X1"), ("X3", "X3"), ("X5", "X5"), ("X7", "X7"),
       ("Ix", "iX"), ("I4 ", "i4 "), ("Ix ", "iX "), ("Payment to Income", "Payment-to-Income"),
       ("Trade in", "Trade-In"), ("Trade In", "Trade-In"), ("Co Signer", "Co-Signer"),
       ("Cosigner", "Cosigner"), ("Sign and Drive", "Sign-and-Drive"),
       ("ID4", "ID.4"), ("C Class", "C-Class"), ("E Class", "E-Class"),
       ("S Class", "S-Class"), ("A Class", "A-Class")]

def slug_title(slug):
    words = slug.split("-")
    out = []
    for i, w in enumerate(words):
        if w in UPPER:
            out.append(w.upper())
        elif i > 0 and w in KEEP:
            out.append(KEEP[w])
        else:
            out.append(w.capitalize())
    t = " ".join(out)
    for a, b in FIX:
        t = t.replace(a, b)
    return t

GEO = re.compile(r"-(nj|ny|pa|ct|de|md)$")

def geo_parts(slug, prefix):
    rest = slug[len(prefix):]
    city, st = rest.rsplit("-", 1)
    return slug_title(city), st.upper()

def link(slug, text=None):
    return f'<li><a href="{LIVE}/{slug}/">{html.escape(text or slug_title(slug))}</a></li>'

STATE_NAME = {"NJ": "New Jersey", "NY": "New York", "PA": "Pennsylvania",
              "CT": "Connecticut", "DE": "Delaware", "MD": "Maryland"}

def geo_sections(slugs, prefix):
    groups = collections.defaultdict(list)
    for s in slugs:
        city, st = geo_parts(s, prefix)
        groups[st].append((city, s))
    parts = []
    for st in sorted(groups, key=lambda k: -len(groups[k])):
        items = "\n".join(link(s, f"{c}, {st}") for c, s in sorted(groups[st]))
        parts.append(f"<h2>{STATE_NAME.get(st, st)}</h2>\n<ul class=\"caf-cols\">\n{items}\n</ul>")
    return "\n".join(parts)

# ---------------- categorize ----------------
cats = collections.defaultdict(list)
LENDER_HINTS = ("financial-services", "financial", "credit", "bank", "ally", "chase",
                "capital-one", "us-bank", "wells-fargo", "santander", "usaa", "nmac",
                "westlake", "bridgecrest", "exeter", "truist", "pnc", "td-auto",
                "leasing", "motor-finance", "hyundai-motor", "kia-finance", "dcu",
                "navy-federal", "penfed", "lightstream", "chrysler-capital", "vw-credit")
for s in SLUGS:
    if s.startswith("auto-refinance-") and GEO.search(s):
        cats["refi_geo"].append(s)
    elif s.startswith("lease-buyout-") and GEO.search(s):
        cats["lease_geo"].append(s)
    elif s.startswith("car-payment-help-") and GEO.search(s):
        cats["pay_geo"].append(s)
    elif s.startswith("used-car-dealer-financing-") and GEO.search(s):
        cats["dealer_geo"].append(s)
    elif s.startswith("get-out-of-a-car-lease-") and GEO.search(s):
        cats["exit_geo"].append(s)
    elif s.startswith("upside-down-car-loan-") and GEO.search(s):
        cats["upside_geo"].append(s)
    elif s.startswith("used-car-financing-") and GEO.search(s):
        cats["ucf_geo"].append(s)
    elif GEO.search(s):
        cats["misc_geo"].append(s)
    elif s.endswith("-lease-buyout") and any(h in s for h in LENDER_HINTS):
        cats["lease_lender"].append(s)
    elif s.endswith("-lease-buyout"):
        cats["lease_brand"].append(s)
    elif "lease" in s:
        cats["lease_guide"].append(s)
    elif "dealer" in s or s.endswith("-for-dealers"):
        cats["dealer"].append(s)
    else:
        cats["guides"].append(s)

assert sum(len(v) for v in cats.values()) == len(SLUGS)
for k, v in sorted(cats.items()):
    print(f"{k:14} {len(v)}")
if cats.get("misc_geo"):
    print("misc_geo:", cats["misc_geo"][:10])

OUT.mkdir(exist_ok=True)
back = '<p><a href="./">&larr; All articles</a></p>'

# ---------------- search index + script ----------------
import json
LABELS = [("lease_brand", "Lease Buyouts by Brand & Model"),
          ("lease_lender", "Lease Buyouts by Lender"),
          ("lease_guide", "Lease Buyout Guides"),
          ("misc_geo", "Lease Buyout Guides"),
          ("lease_geo", "Lease Buyouts by City"),
          ("refi_geo", "Auto Refinance by City"),
          ("pay_geo", "Car Payment Help by City"),
          ("exit_geo", "Get Out of a Car Lease"),
          ("upside_geo", "Upside-Down Car Loans"),
          ("ucf_geo", "Used Car Financing"),
          ("dealer", "Dealer Financing"),
          ("dealer_geo", "Dealer Financing by City"),
          ("guides", "Auto Finance Guides")]
index = [{"t": slug_title(s), "u": f"{LIVE}/{s}/", "c": lab}
         for key, lab in LABELS for s in cats[key]]
assert len(index) == len(SLUGS)
(OUT / "search-index.js").write_text(
    "window.CAF_ARTICLES=" + json.dumps(index, separators=(",", ":")) + ";\n",
    encoding="utf-8")

SEARCH_JS = """(function(){
var inp=document.getElementById('caf-search-input');
if(!inp)return;
var out=document.getElementById('caf-search-results');
var cnt=document.getElementById('caf-search-count');
var MAX=200;
function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function run(){
  var q=inp.value.trim().toLowerCase();
  if(q.length<2||!window.CAF_ARTICLES){out.hidden=true;cnt.hidden=true;out.innerHTML='';return;}
  var terms=q.split(/\\s+/);
  var hits=window.CAF_ARTICLES.filter(function(a){
    var h=(a.t+' '+a.c).toLowerCase();
    return terms.every(function(t){return h.indexOf(t)>-1;});
  });
  out.innerHTML=hits.slice(0,MAX).map(function(a){
    return '<li><a href="'+a.u+'">'+esc(a.t)+'</a> <span class="caf-count">&mdash; '+esc(a.c)+'</span></li>';
  }).join('');
  cnt.textContent=hits.length?hits.length+' result'+(hits.length===1?'':'s')+(hits.length>MAX?' (showing first '+MAX+')':''):'No matching articles';
  out.hidden=!hits.length;cnt.hidden=false;
}
inp.addEventListener('input',run);
})();
"""
(OUT / "search.js").write_text(SEARCH_JS, encoding="utf-8")

def flat_page(fname, h1, title, desc, intro, slugs):
    items = "\n".join(link(s) for s in sorted(slugs, key=slug_title))
    body = f"{back}\n<p>{intro}</p>\n<ul class=\"caf-cols\">\n{items}\n</ul>\n{back}"
    page_html(fname, h1, title, desc, body)

def geo_page(fname, h1, title, desc, intro, slugs, prefix):
    body = f"{back}\n<p>{intro}</p>\n{geo_sections(slugs, prefix)}\n{back}"
    page_html(fname, h1, title, desc, body)

flat_page("lease-buyout-brands.html", "Lease Buyouts by Brand &amp; Model",
    "Lease Buyouts by Brand & Model",
    "Lease buyout financing guides for every major vehicle brand and model, from Champion Auto Finance.",
    f'Brand-by-brand and model-by-model guides to financing a lease buyout, published by '
    f'<a href="{LIVE}/">Champion Auto Finance</a>. Start with the '
    f'<a href="{LIVE}/lease-buyout-financing/">lease buyout financing</a> overview.',
    cats["lease_brand"])

flat_page("lease-buyout-lenders.html", "Lease Buyouts by Lender",
    "Lease Buyouts by Bank & Captive Lender",
    "How each captive lender and bank handles lease payoffs and buyouts, from Champion Auto Finance.",
    f'How each captive finance arm and bank handles payoff quotes, third-party buyouts, and titles — from '
    f'<a href="{LIVE}/">Champion Auto Finance</a>.',
    cats["lease_lender"])

flat_page("lease-buyout-guides.html", "Lease Buyout Guides",
    "Lease Buyout Guides & FAQs",
    "Practical guides to lease buyout financing: payoff quotes, taxes, credit, timing, and paperwork.",
    f'Everything about buying out a lease — payoff quotes, taxes and fees, credit, timing, and paperwork — from '
    f'<a href="{LIVE}/lease-buyouts-refinancing/">Champion Auto Finance lease buyouts &amp; refinancing</a>.',
    cats["lease_guide"] + cats["misc_geo"])

def city_list(slugs, prefix):
    items = "\n".join(link(s, "{}, {}".format(*geo_parts(s, prefix))) for s in sorted(slugs))
    return f"<ul class=\"caf-cols\">\n{items}\n</ul>"

local_body = (
    f'{back}\n<p>More local guides from <a href="{LIVE}/">Champion Auto Finance</a> for drivers in '
    f'New Jersey, New York, and Pennsylvania.</p>\n'
    f'<h2>Get Out of a Car Lease</h2>\n{city_list(cats["exit_geo"], "get-out-of-a-car-lease-")}\n'
    f'<h2>Upside-Down Car Loan Help</h2>\n{city_list(cats["upside_geo"], "upside-down-car-loan-")}\n'
    f'<h2>Used Car Financing</h2>\n{city_list(cats["ucf_geo"], "used-car-financing-")}\n'
    f'{back}'
)
page_html("local-guides.html", "More Local Guides",
    "Local Guides: Lease Exits, Upside-Down Loans & Used Car Financing",
    "City-by-city guides to getting out of a car lease, fixing an upside-down car loan, and financing a used car.",
    local_body)

geo_page("lease-buyouts-by-city.html", "Lease Buyouts by City",
    "Lease Buyout Financing by City",
    "Local lease buyout financing pages for New Jersey, New York, and Pennsylvania drivers.",
    f'Local lease buyout financing information from <a href="{LIVE}/">Champion Auto Finance</a>, an NJ-based financing partner.',
    cats["lease_geo"], "lease-buyout-")

geo_page("auto-refinance-by-city.html", "Auto Refinance by City",
    "Auto Refinancing by City",
    "Local auto loan refinancing pages for New Jersey, New York, and Pennsylvania drivers.",
    f'Local auto refinancing information from <a href="{LIVE}/auto-refinance/">Champion Auto Finance auto refinance</a>.',
    cats["refi_geo"], "auto-refinance-")

geo_page("car-payment-help-by-city.html", "Car Payment Help by City",
    "Car Payment Help by City",
    "Local car payment help pages: lowering payments through refinancing and restructuring.",
    f'Local guides to lowering a car payment, from <a href="{LIVE}/car-payment-help/">Champion Auto Finance car payment help</a>.',
    cats["pay_geo"], "car-payment-help-")

dealer_body = (
    f'{back}\n<p>Programs and education for used-vehicle dealers who work with '
    f'<a href="{LIVE}/dealer-partners/">Champion Auto Finance dealer partners</a>.</p>\n'
    "<h2>Dealer Financing Programs &amp; Education</h2>\n<ul class=\"caf-cols\">\n"
    + "\n".join(link(s) for s in sorted(cats["dealer"], key=slug_title))
    + "\n</ul>\n"
    + geo_sections(cats["dealer_geo"], "used-car-dealer-financing-").replace(
        "<h2>", "<h2>Used Car Dealer Financing — ", 3)
    + f"\n{back}"
)
page_html("dealer-financing.html", "Dealer Financing",
    "Dealer Financing Programs & Education",
    "Auto financing programs and education for used-vehicle dealers, from Champion Auto Finance.",
    dealer_body)

flat_page("auto-finance-guides.html", "Auto Finance Guides",
    "Auto Finance & Refinancing Guides",
    "Guides to auto refinancing, negative equity, car payments, credit, and loan basics.",
    f'Refinancing, negative equity, credit, and car-payment guides from '
    f'<a href="{LIVE}/">Champion Auto Finance</a>.',
    cats["guides"])

# ---------------- hub ----------------
hub_cats = [
    ("lease-buyout-brands.html", "Lease Buyouts by Brand &amp; Model", len(cats["lease_brand"]),
     "Brand- and model-specific lease buyout financing guides — Acura through Volvo."),
    ("lease-buyout-lenders.html", "Lease Buyouts by Bank &amp; Captive Lender", len(cats["lease_lender"]),
     "How each captive finance arm and bank handles payoffs, third-party buyouts, and titles."),
    ("lease-buyout-guides.html", "Lease Buyout Guides &amp; FAQs", len(cats["lease_guide"]) + len(cats["misc_geo"]),
     "Payoff quotes, taxes and fees, credit, timing, paperwork, and common mistakes."),
    ("lease-buyouts-by-city.html", "Lease Buyouts by City", len(cats["lease_geo"]),
     "Local lease buyout financing pages across New Jersey, New York, and Pennsylvania."),
    ("auto-refinance-by-city.html", "Auto Refinancing by City", len(cats["refi_geo"]),
     "Local auto loan refinancing pages across NJ, NY, and PA."),
    ("car-payment-help-by-city.html", "Car Payment Help by City", len(cats["pay_geo"]),
     "Local guides to lowering a car payment through refinancing or restructuring."),
    ("local-guides.html", "More Local Guides", len(cats["exit_geo"]) + len(cats["upside_geo"]) + len(cats["ucf_geo"]),
     "City pages for lease exits, upside-down car loans, and used car financing."),
    ("dealer-financing.html", "Dealer Financing Programs &amp; Education", len(cats["dealer"]) + len(cats["dealer_geo"]),
     "Programs and education for used-vehicle dealer partners, including local pages."),
    ("auto-finance-guides.html", "Auto Finance &amp; Refinancing Guides", len(cats["guides"]),
     "Refinancing, negative equity, calculators, credit, and loan-basics articles."),
]
total = sum(n for _, _, n, _ in hub_cats)
cat_items = "\n".join(
    f'<li><h3><a href="{f}">{t}</a> <span class="caf-count">({n} articles)</span></h3><p>{d}</p></li>'
    for f, t, n, d in hub_cats)
hub_body = f'''<p class="lead">Champion Auto Finance publishes {total} articles on lease buyouts, auto refinancing,
car payments, and dealer financing. Browse the full library below — every article lives on
<a href="{LIVE}/">championautofinance.com</a>.</p>
<ul class="caf-cat-list">
{cat_items}
</ul>
<h2>Start here</h2>
<ul>
<li><a href="{LIVE}/lease-buyout-financing/">Lease Buyout Financing</a> — the pillar guide to keeping the car you already lease.</li>
<li><a href="{LIVE}/auto-refinance/">Auto Refinance</a> — how refinancing works and when it makes sense.</li>
<li><a href="{LIVE}/car-payment-help/">Car Payment Help</a> — options when a payment is too high.</li>
<li><a href="{LIVE}/dealer-partners/">Dealer Partners</a> — financing programs for used-vehicle dealers.</li>
</ul>'''
page_html("index.html", "Articles", "Articles",
    "The Champion Auto Finance article library: lease buyouts, auto refinancing, car payment help, and dealer financing.",
    hub_body)

# ---------------- github.io sitemap (idempotent) ----------------
SM = REPO / "sitemap.xml"
sm = SM.read_text(encoding="utf-8")
sm = re.sub(r"  <url>\s*<loc>https://championautofinance\.github\.io/articles/[^<]*</loc>\s*<priority>[^<]*</priority>\s*</url>\n", "", sm)
entries = ['  <url>\n    <loc>{}/articles/</loc>\n    <priority>0.7</priority>\n  </url>'.format(GH)]
entries += ['  <url>\n    <loc>{}/articles/{}</loc>\n    <priority>0.6</priority>\n  </url>'.format(GH, f)
            for f, _, _, _ in hub_cats]
sm = sm.replace("</urlset>", "\n".join(entries) + "\n</urlset>")
SM.write_text(sm, encoding="utf-8")

if cats.get("misc_geo"):
    print(f"NOTE: {len(cats['misc_geo'])} slugs from unrecognized local series landed in "
          f"Lease Buyout Guides — consider adding a category: {cats['misc_geo'][:5]}")
print("wrote", len(list(OUT.glob("*.html"))), "pages, covering", total, "articles")
