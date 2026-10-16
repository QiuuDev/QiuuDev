"""Build portfolio-matched profile artwork. Run locally with fonttools installed."""
from pathlib import Path
from html import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT = instantiateVariableFont(TTFont(ASSETS / "fonts/Orbitron.ttf"), {"wght": 700})
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UPM = FONT["head"].unitsPerEm
BG, PANEL, CYAN, FG, MUTED, LINE = "#020609", "#061018", "#00f5ff", "#e4f2f8", "#8ca9b8", "#15333e"


def text(x, y, value, size=18, color=FG, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(value)}</text>'


def title(x, y, value, size=30, color=FG, outline=False):
    pen = SVGPathPen(GLYPHS)
    advance = 0
    paths = []
    for char in value:
        glyph = GLYPHS[CMAP[ord(char)]]
        pen = SVGPathPen(GLYPHS)
        glyph.draw(pen)
        paths.append(f'<path transform="translate({advance} 0)" d="{pen.getCommands()}"/>')
        advance += glyph.width
    paint = f'fill="none" stroke="{color}" stroke-width="{UPM / size:.2f}"' if outline else f'fill="{color}"'
    return f'<g aria-hidden="true" transform="translate({x} {y}) scale({size / UPM:.5f} {-size / UPM:.5f})" {paint}>{"".join(paths)}</g>'


def rect(x, y, w, h, fill=PANEL, stroke=LINE, radius=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def pill(x, y, label):
    w = len(label) * 8.6 + 24
    return rect(x, y, w, 28, "#07202a", "#164653", 3) + text(x+12, y+19, label, 13, CYAN), w


def svg(name, body, height, width=960, label=""):
    source = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(label or name)}</title><desc id="desc">Muhammad Qodri / QiuuDev. Portfolio identity: dark navy, electric cyan, geometric typography.</desc>
<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#123340" stroke-width=".6"/></pattern><radialGradient id="glow"><stop stop-color="#00f5ff" stop-opacity=".12"/><stop offset="1" stop-color="#00f5ff" stop-opacity="0"/></radialGradient></defs>
<style>text{{font-family:Consolas,"Liberation Mono",monospace}}.orbit{{transform-origin:760px 194px;animation:orbit 35s linear infinite}}.pulse{{animation:pulse 4s ease-in-out infinite}}.scan{{animation:scan 7s ease-in-out infinite}}@keyframes orbit{{to{{transform:rotate(360deg)}}}}@keyframes pulse{{50%{{opacity:.35}}}}@keyframes scan{{50%{{transform:translateX(250px)}}}}@media(prefers-reduced-motion:reduce){{.orbit,.pulse,.scan{{animation:none}}}}</style>
{rect(1,1,width-2,height-2,BG,LINE,10)}{body}</svg>'''
    (ASSETS / f"portfolio-{name}.svg").write_text(source, encoding="utf-8")


def section(number, name, subtitle):
    body = text(30, 27, f"{number} /", 13, CYAN) + title(91, 31, name, 22)
    body += text(930, 29, subtitle, 11, MUTED, 'text-anchor="end" letter-spacing="1"')
    body += f'<path d="M30 48H930" stroke="{LINE}"/><path d="M30 48H102" stroke="{CYAN}"/>'
    svg(f"section-{number}", body, 62, label=f"{number} / {name}")
    compact = text(24,27,f"{number} /",15,CYAN) + title(87,31,name,22)
    compact += f'<path d="M24 48H576" stroke="{LINE}"/><path d="M24 48H96" stroke="{CYAN}"/>'
    svg(f"section-{number}-mobile",compact,62,600,label=f"{number} / {name}")


def hero(mobile=False):
    if mobile:
        b = '<rect x="12" y="12" width="576" height="450" fill="url(#grid)" opacity=".55"/>'
        b += text(28,38,"QIU // DEVELOPER PORTFOLIO",14,CYAN,'letter-spacing="2"')
        b += '<circle class="pulse" cx="35" cy="77" r="4" fill="#00f5ff"/>' + text(49,82,"FRONT-END DEVELOPER @ TALIKAMA",13,MUTED)
        b += title(26,155,"MUHAMMAD",49,CYAN,True) + title(26,222,"QODRI",70)
        b += text(30,263,"QiuuDev / BoringDev",18,CYAN)
        b += text(30,305,"WEB DEVELOPMENT / MOBILE APPS",17)
        b += text(30,333,"PHP  /  DART + FLUTTER  /  PYTHON",16,MUTED)
        b += rect(28,361,544,77,"#06202a","#164653",4)
        b += text(44,389,"Lazy by nature. Efficient by choice.",16,CYAN)
        b += text(44,416,"Automated by design.",16,CYAN)
        b += text(30,463,"MATARAM, INDONESIA  /  VIEW PORTFOLIO",12,MUTED)
        svg("hero-mobile",b,486,600,"Muhammad Qodri — Front-End Developer at Talikama Creative. PHP, Dart/Flutter, Python. Lazy by nature. Efficient by choice. Automated by design.")
        return
    b = '<rect x="12" y="12" width="936" height="400" fill="url(#grid)" opacity=".55"/><circle cx="760" cy="194" r="210" fill="url(#glow)"/>'
    b += text(34,37,"QIU // DEVELOPER PORTFOLIO",12,CYAN,'letter-spacing="2.3"')
    b += text(924,37,"MATARAM, INDONESIA",11,MUTED,'text-anchor="end" letter-spacing="1.5"')
    b += '<circle class="pulse" cx="40" cy="79" r="4" fill="#00f5ff"/>' + text(53,84,"FRONT-END DEVELOPER @ TALIKAMA CREATIVE",12,MUTED)
    b += title(30,150,"MUHAMMAD",53,CYAN,True) + title(29,220,"QODRI",78)
    b += text(34,258,"QiuuDev / BoringDev",18,CYAN)
    b += text(34,292,"WEB DEVELOPMENT / MOBILE APPS / AUTOMATION",14)
    b += text(34,320,"PHP  /  DART + FLUTTER  /  PYTHON",13,MUTED)
    b += f'<circle cx="760" cy="194" r="119" fill="none" stroke="{LINE}"/><g class="orbit"><circle cx="760" cy="194" r="133" fill="none" stroke="{CYAN}" stroke-dasharray="80 30 2 32" opacity=".55"/><circle cx="760" cy="61" r="4" fill="{CYAN}"/></g>'
    b += '<path d="M798 143H730L708 165V219L730 241H784L806 219V165Z M768 213L825 270" fill="none" stroke="#00f5ff" stroke-width="10" stroke-linejoin="bevel"/>'
    b += text(760,354,"BUILD LESS MANUAL WORK.",12,CYAN,'text-anchor="middle" letter-spacing="1.3"')
    b += f'<path d="M34 347H540" stroke="{LINE}"/><path class="scan" d="M34 347H180" stroke="{CYAN}"/>'
    b += text(34,378,"Lazy by nature. Efficient by choice.",15,CYAN) + text(34,402,"Automated by design.",15,CYAN)
    svg("hero",b,426,label="Muhammad Qodri — Front-End Developer at Talikama Creative. Web, mobile and automation. Lazy by nature. Efficient by choice. Automated by design.")


def about(mobile=False):
    w=600 if mobile else 960
    lines = [
        ("NAME", "Muhammad Qodri / QiuuDev"),
        ("WORK", "Front-End Developer, part-time"),
        ("TEAM", "Talikama Creative"),
        ("STUDY", "Computer Science, Universitas Bumigora"),
        ("FOCUS", "Web apps, mobile apps, automation"),
    ]
    b = text(28,32,"qiu@workspace:~$ whoami",16,CYAN)
    b += f'<path d="M28 50H{w-28}" stroke="{LINE}"/>'
    if mobile:
        for i,(label,value) in enumerate(lines):
            y=80+i*58
            b+=text(28,y,label,12,CYAN,'letter-spacing="1.4"')+text(28,y+23,value,18)
        b+=text(28,393,"I turn repetitive work into useful tools.",18,MUTED)
        height=420
    else:
        for i,(label,value) in enumerate(lines):
            y=82+i*36
            b+=text(30,y,label,12,CYAN,'letter-spacing="1.4"')+text(143,y,value,18)
        b+=text(30,292,"I build practical interfaces and automate the repetitive parts.",17,MUTED)
        height=321
    svg("about-mobile" if mobile else "about",b,height,w,"About Muhammad Qodri: part-time Front-End Developer at Talikama Creative, Computer Science student at Universitas Bumigora. Web apps, mobile apps, automation.")


def toolkit(mobile=False):
    w=600 if mobile else 960
    b=""
    rows=[("01", "PHP", "Web applications / APIs / MySQL"), ("02","DART / FLUTTER","Mobile interfaces / app workflows"),("03","PYTHON","Automation / Flask / ML projects")]
    for i,(n,name,desc) in enumerate(rows):
        if mobile:
            x,y,cw=24,24+i*114,552
        else:
            x,y,cw=24+i*310,24,292
        b+=rect(x,y,cw,96)
        b+=text(x+16,y+22,n,11,CYAN)+title(x+16,y+50,name,19)
        b+=text(x+16,y+77,desc,16 if mobile else 12,MUTED)
    y=388 if mobile else 158
    b+=text(26,y,"ALSO IN MY TOOLKIT",12,CYAN,'letter-spacing="1.5"')
    tags=["JavaScript","TypeScript","React / Next.js","HTML / CSS","Laravel","WordPress","Git","Firebase","Supabase"]
    x,y=24,y+16
    for tag in tags:
        needed=len(tag)*8.6+24
        if x+needed>w-24:
            x,y=24,y+37
        p,pw=pill(x,y,tag)
        b+=p
        x+=pw+10
    svg("toolkit-mobile" if mobile else "toolkit",b,y+51,w,"Core stacks: PHP, Dart/Flutter, Python. Also JavaScript, TypeScript, React/Next.js, HTML/CSS, Laravel, WordPress, Git, Firebase and Supabase.")


PROJECTS=[
    ("generator","01","LOMBOK GENERATOR","CLIENT WEBSITE / PUBLIC CODE","Live document previews, quotations and invoice PDFs.","HTML / CSS / JAVASCRIPT / jsPDF",["Document preview + PDF export","Built for a client"],"#00f5ff"),
    ("prime","02","PRIME TRANS INDO","CLIENT WEBSITE / WORDPRESS","A vehicle rental website delivered independently.","WORDPRESS / FRONT-END DEVELOPMENT",["Vehicle rental website","Talikama Creative client work"],"#00f5ff"),
    ("schedule","03","QIU SCHEDULE","WEB APPLICATION / PUBLIC CODE","Scheduling, notifications and calendar workflows.","PHP / MYSQL / JAVASCRIPT",["Calendar + scheduling","Notifications + profiles"],"#00f5ff"),
    ("stride","04","STRIDE RUNNING COACH","FLUTTER APPLICATION / MVP","A personal running companion with local activity data.","DART / FLUTTER / LOCAL STORAGE",["Training plans + activity logs","Rule-based coaching"],"#00f5ff"),
    ("python","05","CYBERBULLYING DETECTOR","PYTHON PROJECT / PUBLIC CODE","Text classification experiments with a Flask interface.","PYTHON / FLASK / MACHINE LEARNING",["Text processing workflow","Browser extension companion"],"#00f5ff"),
]


def project(p,mobile=False):
    key,n,name,kicker,desc,stack,features,accent=p
    w=600 if mobile else 960
    b=text(26,29,f"{n} / {kicker}",11,CYAN,'letter-spacing="1"')
    size=22 if mobile else 27
    b+=title(25,75,name,size)
    if mobile:
        # Wrap on words using conservative monospace metrics.
        words=desc.split(); lines=[""]
        for word in words:
            if len(lines[-1])+len(word)+1>46: lines.append("")
            lines[-1]+=(" " if lines[-1] else "")+word
        for i,line in enumerate(lines): b+=text(26,110+i*25,line,17,MUTED)
        y=110+len(lines)*25+14
        b+=text(26,y,stack,13,CYAN)
        b+=f'<path d="M26 {y+20}H574" stroke="{LINE}"/>'
        for i,f in enumerate(features): b+=text(26,y+49+i*27,"+ "+f,16,FG)
        b+=text(574,y+110,"EXPLORE PROJECT  /  OPEN",12,CYAN,'text-anchor="end"')
        h=y+135
    else:
        b+=text(26,111,desc,17,MUTED)+text(26,146,stack,12,CYAN)
        b+=f'<path d="M670 28V164" stroke="{LINE}"/>'
        for i,f in enumerate(features): b+=text(692,68+i*28,f,12)
        b+=text(692,146,"EXPLORE PROJECT  /  OPEN",11,CYAN)
        h=190
    svg(f"project-{key}"+("-mobile" if mobile else ""),b,h,w,f"{name}. {desc} {stack}. {kicker}.")


def contact(mobile=False):
    w=600 if mobile else 960
    b=title(28,52,"LET'S BUILD SOMETHING.",23 if mobile else 32)
    b+=text(28,88,"Websites, applications and fewer manual steps.",16,MUTED)
    b+=f'<path d="M28 112H{w-28}" stroke="{LINE}"/>'
    b+=text(28,145,"qodriodi91@gmail.com",19,CYAN)
    b+=text(28,177,"Mataram, Indonesia / Remote collaboration",15,MUTED)
    b+=text(28,219,"QIU // CODE WITH INTENT. AUTOMATE THE REST.",12,CYAN)
    svg("contact-mobile" if mobile else "contact",b,246,w,"Contact Muhammad Qodri: qodriodi91@gmail.com. Mataram, Indonesia. Websites, applications and automation.")


def picture(name,alt,url=None):
    out=f'''<picture>
  <source media="(max-width: 768px)" srcset="assets/portfolio-{name}-mobile.svg">
  <img src="assets/portfolio-{name}.svg" width="100%" alt="{escape(alt,quote=True)}">
</picture>'''
    return f'<a href="{url}">\n{out}\n</a>' if url else out


def build():
    for mobile in (False,True):
        hero(mobile); about(mobile); toolkit(mobile); contact(mobile)
        for p in PROJECTS: project(p,mobile)
    for n,name,sub in [("01","ABOUT","THE PERSON BEHIND THE CODE"),("02","TOOLKIT","CORE STACKS + SUPPORTING TOOLS"),("03","SELECTED WORK","CLIENT WEBSITES + PUBLIC PROJECTS"),("04","ACTIVITY","PUBLIC GITHUB DATA"),("05","CONNECT","LET'S TALK ABOUT YOUR PROJECT")]: section(n,name,sub)
    content=[picture("hero","Muhammad Qodri / QiuuDev. Front-End Developer at Talikama Creative. Web, mobile and automation. Lazy by nature. Efficient by choice. Automated by design.","https://portfolio-qodri.netlify.app/"),
        '<p align="center"><a href="https://portfolio-qodri.netlify.app/"><b>VIEW PORTFOLIO ↗</b></a> &nbsp; · &nbsp; <a href="https://github.com/QiuuDev?tab=repositories">EXPLORE REPOSITORIES ↗</a></p>',
        picture("section-01","01 / About"),picture("about","Part-time Front-End Developer at Talikama Creative. Computer Science student at Universitas Bumigora. I build web apps, mobile apps and automation."),
        '<details>\n<summary>About me · Bahasa Indonesia</summary>\n\nSaya Muhammad Qodri, juga dikenal sebagai QiuuDev / BoringDev. Saya bekerja paruh waktu sebagai Front-End Developer di Talikama Creative sambil kuliah Ilmu Komputer di Universitas Bumigora. Saya membangun aplikasi web, aplikasi mobile, dan otomatisasi. PHP, Dart/Flutter, serta Python adalah fokus utama saya; teknologi lain saya gunakan sesuai kebutuhan proyek.\n\nPrinsip saya: **Lazy by nature. Efficient by choice. Automated by design.**\n\n</details>',
        picture("section-02","02 / Toolkit"),picture("toolkit","Core: PHP, Dart/Flutter, Python. Also JavaScript, TypeScript, React/Next.js, HTML/CSS, Laravel, WordPress, Git, Firebase and Supabase."),picture("section-03","03 / Selected work")]
    links=["https://lombokgenerator.xyz/","https://primetransindo.com/","https://github.com/QiuuDev/Qiu_Schedule","https://github.com/QiuuDev/stride-running-coach","https://github.com/QiuuDev/cyberbullying-detector"]
    for p,url in zip(PROJECTS,links):
        content.append(picture("project-"+p[0],f"{p[2]}. {p[4]} {p[5]}.",url))
        if p[0]=="generator": content.append('<p><a href="https://lombokgenerator.xyz/">Live website ↗</a> &nbsp; · &nbsp; <a href="https://github.com/QiuuDev/generator_invoice">Public repository ↗</a></p>')
    content.append('''<details>
<summary>More public projects</summary>

- [HoloPage Komik](https://github.com/QiuuDev/holopage-komik) — PHP comic reading web application.
- [Health Workout App](https://github.com/QiuuDev/health-workout-app) — Flutter health and workout application.
- [Flutter Firebase CRUD](https://github.com/QiuuDev/flutter-firebase-crud) — Flutter application with Firebase data workflows.
- [All public repositories](https://github.com/QiuuDev?tab=repositories) — more projects and experiments.

</details>''')
    content.append(picture("section-04","04 / Activity"))
    for name,alt in [("activity","Public repository statistics and recent pushes. The card shows its refresh date."),("contributions","GitHub contribution calendar. The card shows its refresh date.")]:
        content.append(f'''<picture>
  <source media="(max-width: 768px)" srcset="assets/{name}-mobile-dark.svg">
  <img src="assets/{name}-dark.svg" width="100%" alt="{alt}">
</picture>''')
    content.append('<sub>Public repository data, refreshed automatically. Contribution counts follow GitHub’s calendar. <a href="https://github.com/QiuuDev/QiuuDev/actions/workflows/profile.yml">Refresh status</a>.</sub>')
    content.extend([picture("section-05","05 / Connect"),picture("contact","Contact Muhammad Qodri: qodriodi91@gmail.com. Websites, applications and automation.","mailto:qodriodi91@gmail.com"),'<p align="center"><a href="https://portfolio-qodri.netlify.app/"><b>PORTFOLIO ↗</b></a> &nbsp; · &nbsp; <a href="https://www.linkedin.com/in/muhammad-qodri-4956a731a/">LINKEDIN ↗</a> &nbsp; · &nbsp; <a href="https://www.instagram.com/odi.qiu/">INSTAGRAM ↗</a> &nbsp; · &nbsp; <a href="https://wa.me/6285964403427">WHATSAPP ↗</a></p>'])
    (ROOT/"README.md").write_text("\n\n".join(content)+"\n",encoding="utf-8")
    print("Built 28 responsive identity assets and README.md.")


if __name__=="__main__": build()
