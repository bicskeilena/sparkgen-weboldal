"""Build the Netlify deploy folder from index.html (artifact source) + legal/*.html.
Output: deploy/index.html, deploy/adatkezeles/index.html, deploy/impresszum/index.html (+ fonts.css)."""
import os, re, shutil
here = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(here, 'docs')
os.makedirs(D, exist_ok=True)
src = open(os.path.join(here, 'index.html')).read()

i = src.index('</style>') + len('</style>')
head, body = src[:i], src[i:]
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
# self-hosted fonts instead of Google Fonts
head = re.sub(r'<link rel="preconnect"[^>]*>\n', '', head)
head = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\n', '<link rel="stylesheet" href="/fonts.css">\n', head)
shutil.copytree(os.path.join(here, 'img'), os.path.join(D, 'img'), dirs_exist_ok=True)
shutil.copytree(os.path.join(here, 'fonts'), os.path.join(D, 'fonts'), dirs_exist_ok=True)
open(os.path.join(D, 'fonts.css'), 'w').write(open(os.path.join(here, 'fonts.css')).read())
head = head.replace('</style>', 'html,body{margin:0}\nimg{max-width:100%}\n'
    '.legal{max-width:860px;padding-block:clamp(24px,4vw,48px) clamp(48px,6vw,80px)}\n'
    '.legal h1{font-size:clamp(2rem,4vw,2.8rem);margin-bottom:8px}\n'
    '.legal h2{font-size:1.35rem;margin:40px 0 12px}\n'
    '.legal h3{font-size:1.08rem;margin:26px 0 10px;color:var(--blue)}\n'
    '.legal p{margin:0 0 12px}\n'
    '.legal .meta-line{color:var(--muted);font-size:.95rem}\n'
    '.legal ul{margin:0 0 12px;padding-left:1.2em;display:grid;gap:6px}\n'
    '.legal li::marker{color:var(--blue)}\n'
    '.facts{margin:0 0 14px;border-top:1px solid var(--line)}\n'
    '.facts div{display:grid;grid-template-columns:220px 1fr;gap:16px;padding:10px 0;border-bottom:1px solid var(--line)}\n'
    '.facts dt{font-family:var(--font-display);font-weight:600}\n'
    '.facts dd{margin:0;color:var(--muted)}\n'
    '@media (max-width:640px){.facts div{grid-template-columns:1fr;gap:2px}}\n'
    '.legal a{color:var(--blue)}\n'
    '</style>')

def meta(title, desc, url):
    return ('<!doctype html>\n<html lang="hu">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="theme-color" content="#2447F5">\n'
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
        '<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        f'<link rel="canonical" href="{url}">\n'
        '<meta property="og:type" content="website">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{desc}">\n'
        '<meta property="og:image" content="https://sparkgen.hu/og-image.png">\n'
        '<meta property="og:locale" content="hu_HU">\n'
        '<meta name="twitter:card" content="summary_large_image">\n')

def fix_links(b):
    b = b.replace('https://sparkgen.hu/', '/')
    b = b.replace('href="#irj"', 'href="mailto:info@sparkgen.hu"')
    b = b.replace('<a href="#top">Impresszum</a>', '<a href="/impresszum/">Impresszum</a>')
    b = b.replace('<a href="#top">Adatkezelés</a>', '<a href="/adatkezeles/">Adatkezelés</a>')
    b = b.replace('<a href="#top">Tájékoztató az üzleti megkeresésekről</a>', '<a href="/adatkezeles/#megkeresesek">Tájékoztató az üzleti megkeresésekről</a>')
    b = b.replace('class="logo" href="#top"', 'class="logo" href="/"')
    return b

def page(title, desc, url, h, b):
    h = h.replace('<title>SparkGen Studio</title>', f'<title>{title}</title>')
    return meta(title, desc, url) + h + '\n</head>\n<body>\n' + b.strip() + '\n</body>\n</html>\n'

body = fix_links(body)
home = page('SparkGen Studio · Leadgenerálás B2B cégeknek, garanciával',
            'Van egy jó terméked, de döcög az értékesítés? Adjunk neki szikrát.', 'https://sparkgen.hu/', head, body)
open(os.path.join(D, 'index.html'), 'w').write(home)

# legal pages: same svg defs + header + footer, own <main>
pre = body[:body.index('<main')]
post = body[body.index('</main>') + len('</main>'):]
for slug, title in [('adatkezeles', 'Adatkezelési tájékoztató · SparkGen Studio'), ('impresszum', 'Impresszum · SparkGen Studio')]:
    content = open(os.path.join(here, 'legal', slug + '.html')).read()
    main = f'<main id="top" lang="hu">\n  <div class="wide legal">\n{content}  </div>\n</main>'
    os.makedirs(os.path.join(D, slug), exist_ok=True)
    open(os.path.join(D, slug, 'index.html'), 'w').write(
        page(title, 'SparkGen Studio, Bicskei Léna Magdolna e.v.', f'https://sparkgen.hu/{slug}/', head, pre + main + post))
open(os.path.join(D, 'CNAME'), 'w').write('sparkgen.hu\n')
open(os.path.join(D, '.nojekyll'), 'w').write('')
for f in os.listdir(os.path.join(here, 'static')):
    shutil.copy(os.path.join(here, 'static', f), os.path.join(D, f))
print('built: index, adatkezeles, impresszum -> docs/')
