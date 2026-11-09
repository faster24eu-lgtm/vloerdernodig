"""Builds the service pages from index.html's <style>, header and footer.
Run from the repo root: python3 _build/pages.py"""
import re,json,html
idx=open('index.html',encoding='utf-8').read()
STYLE=re.search(r'<style>.*?</style>',idx,re.S).group(0)
STYLE=STYLE.replace('</style>','.crumbs{font-size:14px;color:#cfd3d8;margin:0 0 10px}.crumbs a{color:#fff}\n.prose{max-width:760px}.prose h2{font-size:clamp(22px,3.6vw,28px);line-height:1.25;margin:36px 0 10px}.prose h2:first-child{margin-top:0}.prose p,.prose li{color:#33383e}.prose ul{padding-left:20px}.note{background:var(--soft);border-left:4px solid var(--brand);padding:14px 18px;border-radius:8px}\n.more{display:flex;flex-wrap:wrap;gap:10px;list-style:none;padding:0;margin:0}.more a{display:inline-block;background:#fff;border:1px solid var(--line);padding:8px 14px;border-radius:99px;font-weight:600;font-size:15px;text-decoration:none;color:var(--ink)}\n</style>')
BASE='https://vloerdernodig.com'
PAGES=[]
def page(slug,title,desc,h1,lead,crumb,body,faq,service,area=None):
    PAGES.append((slug,crumb))
    url=f'{BASE}/{slug}/'
    svc={"@context":"https://schema.org","@type":"Service","name":service,"serviceType":service,"url":url,
         "provider":{"@id":BASE+"/#bedrijf","@type":"HomeAndConstructionBusiness","name":"Vloerder Nodig","url":BASE+"/","telephone":"+3233756737"},
         "areaServed":[{"@type":"City","name":a} for a in (area or [])] or [{"@type":"AdministrativeArea","name":"Vlaanderen"}]}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},{"@type":"ListItem","position":2,"name":crumb,"item":url}]}
    fq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    ld=''.join(f'<script type="application/ld+json">\n{json.dumps(x,ensure_ascii=False,indent=1)}\n</script>\n' for x in (svc,bc,fq))
    faqh='\n'.join(f'    <details><summary><h3>{html.escape(q,quote=False)}</h3></summary><div>{html.escape(a,quote=False)}</div></details>' for q,a in faq)
    return slug,f'''<!DOCTYPE html>
<html lang="nl-BE">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title,quote=False)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:locale" content="nl_BE">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Vloerder Nodig">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Vloerder Nodig: vloertegels, wandtegels en badkamers betegelen">
<meta name="twitter:card" content="summary_large_image">
{ld}{STYLE}
</head>
<body>

<header class="top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Vloerder Nodig home">
      <span class="logo-mark" aria-hidden="true"><span></span><span></span><span></span><span></span></span>
      Vloerder Nodig
    </a>
    <nav class="menu" aria-label="Hoofdmenu">
      <a href="/#tegelwerken">Tegelwerken</a>
      <a href="/#prijzen">Prijzen</a>
      <a href="/#werkwijze">Werkwijze</a>
      <a href="/#regio">Regio</a>
      <a href="#faq">Vragen</a>
    </nav>
    <a class="btn btn-main top-call" href="tel:+3233756737">Bel nu</a>
  </div>
</header>

<main>
<section class="hero" aria-label="Introductie">
  <div class="wrap">
    <div>
      <p class="crumbs"><a href="/">Home</a> › {html.escape(crumb)}</p>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="ctas">
        <a class="btn btn-main" href="tel:+3233756737">Bel 03 375 67 37</a>
        <a class="btn btn-ghost" href="#faq">Veelgestelde vragen</a>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap prose">
{body.strip(chr(10))}
  </div>
</section>

<section class="alt" id="faq">
  <div class="wrap">
    <h2 class="sec">Veelgestelde vragen</h2>
{faqh}
  </div>
</section>

<section>
  <div class="wrap">
    <h2 class="sec">Andere tegelwerken</h2>
    <ul class="more">
%MORE%
    </ul>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <h2 class="sec">Gratis opmeting aanvragen?</h2>
    <p>Bel ons, vertel wat er moet gebeuren en we plannen een opmeting in.</p>
    <div class="ctas">
      <a class="btn btn-ghost" href="tel:+3233756737">Bel 03 375 67 37</a>
    </div>
  </div>
</section>
</main>

%FOOTER%

<div class="mbar">
  <a class="btn btn-main" href="tel:+3233756737">Bel nu: 03 375 67 37</a>
</div>

</body>
</html>
'''
exec(open('_build/content.py',encoding='utf-8').read())
FOOTER=re.search(r'<footer>.*?</footer>',open('index.html',encoding='utf-8').read(),re.S).group(0)
FOOTER=FOOTER.replace('href="#','href="/#')
for slug,doc in OUT:
    more='\n'.join(f'      <li><a href="/{s}/">{html.escape(c)}</a></li>' for s,c in PAGES if s!=slug)
    import os; os.makedirs(slug,exist_ok=True)
    open(f'{slug}/index.html','w',encoding='utf-8').write(doc.replace('%MORE%',more).replace('%FOOTER%',FOOTER))
    print(slug)
