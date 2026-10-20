"""Páginas internas de Aequitas (areas.html, nosotros.html) con head/header/footer del index.
Uso: python _scripts/generar_paginas.py   (correr DESPUÉS de generar_extras.py, así heredan el link a privacidad)
Idempotente: se puede volver a correr cuando cambia el index."""
import re
from pathlib import Path

D = Path(__file__).resolve().parent.parent
idx = (D / "index.html").read_text(encoding="utf8")

head_tpl = idx[:idx.index("<title>")]
links_head = idx[idx.index('<link rel="preconnect"'):idx.index("</head>")]
links_head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", links_head, flags=re.S)
links_head = re.sub(r'<meta property="og:.*?>\n|<meta name="twitter:.*?>\n', "", links_head)
top = idx[idx.index("<!-- ============ HEADER ============ -->"):idx.index("<main>")]
f0 = idx.index("<!-- ============ FOOTER ============ -->")
foot = idx[f0:idx.index('<a class="wa-float', f0)]
tail = idx[idx.index('<a class="wa-float', f0):]

def interna(s):
    s = re.sub(r'href="#(?!")', 'href="./index.html#', s)
    return s.replace('href="./index.html#inicio"', 'href="./index.html"')

top, foot = interna(top), interna(foot)

def page(name, title, desc, body, og_title=None):
    og = (f'<meta property="og:type" content="website">\n<meta property="og:locale" content="es_AR">\n'
          f'<meta property="og:title" content="{og_title or title}">\n<meta property="og:description" content="{desc}">\n'
          f'<meta property="og:image" content="https://i.imgur.com/L8saYA4.png">\n<meta name="twitter:card" content="summary">\n')
    html = (head_tpl + f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            '<meta name="theme-color" content="#141414">\n<link rel="icon" type="image/png" href="./favicon.png">\n'
            '<link rel="apple-touch-icon" href="./favicon.png">\n' + og + links_head + "</head>\n<body>\n\n"
            + top + "<main>\n" + body + "\n</main>\n\n" + foot + tail)
    (D / name).write_text(html, encoding="utf8", newline="\n")
    print("ok", name)

def cabecera(titulo, rojo, ruta, bajada, foto):
    return f'''<!-- ============ CABECERA (recurso cuñas corporativas) ============ -->
<section class="page-hero">
  <div class="page-hero-bg" style="background-image:url(img/{foto})" aria-hidden="true"></div>
  <span class="dots dots-tl" aria-hidden="true"></span>
  <span class="hairline hl-2" aria-hidden="true" data-overflow-ok></span>
  <span class="shard shard-k" aria-hidden="true"></span>
  <span class="shard shard-r" aria-hidden="true"></span>
  <div class="wrap page-hero-in">
    <nav class="ruta rise" aria-label="Ruta"><a href="./index.html">Inicio</a><i class="ti ti-chevron-right" aria-hidden="true"></i><span>{ruta}</span></nav>
    <h1 class="page-h1 rise d1">{titulo} <span>{rojo}</span></h1>
    <span class="red-line rise d2" aria-hidden="true"></span>
    <p class="hero-sub rise d2">{bajada}</p>
  </div>
</section>
'''

# ---------------- ÁREAS ----------------
# Los ítems de cada área son temas generales del rubro: validarlos con el estudio.
AREAS = [
    ("familia", "ti-users", "Derecho de Familia",
     "Acompañamos a las familias en momentos que requieren contención y claridad, buscando acuerdos cuando es posible y defendiendo tus derechos cuando hace falta.",
     ["Divorcios", "Cuota alimentaria", "Cuidado personal y régimen de comunicación", "Uniones convivenciales"]),
    ("trabajo", "ti-briefcase", "Trabajo y accidentes de trabajo",
     "Asesoramos a trabajadores en sus reclamos laborales y en los accidentes y enfermedades ocurridos con motivo del trabajo.",
     ["Despidos e indemnizaciones", "Trabajo no registrado", "Accidentes de trabajo y enfermedades laborales", "Reclamos ante la ART"]),
    ("salud", "ti-heart-plus", "Amparos de salud",
     "Brindamos especial atención a los amparos por cuestiones de salud, cuando una obra social o prepaga no brinda la cobertura que corresponde.",
     ["Cobertura de tratamientos y medicamentos", "Prestaciones por discapacidad", "Reclamos a obras sociales y prepagas", "Medidas urgentes"]),
    ("sucesiones", "ti-file-certificate", "Sucesiones y Derecho Civil",
     "Te acompañamos en el trámite sucesorio de principio a fin y en las cuestiones civiles que necesiten respaldo profesional.",
     ["Sucesiones", "Contratos", "Daños y perjuicios", "Cuestiones patrimoniales"]),
    ("empresarial", "ti-building", "Empresarial y Tributario",
     "Asesoramiento jurídico integral para empresas, comercios y entidades, con foco en la prevención.",
     ["Asesoramiento a empresas y comercios", "Contratos comerciales", "Cuestiones tributarias", "Entidades y asociaciones"]),
    ("previsional", "ti-shield-check", "Previsional y Seguridad Social",
     "Te orientamos en los trámites y reclamos previsionales, en el ámbito federal y de la Provincia de Buenos Aires.",
     ["Jubilaciones y pensiones", "Reajustes de haberes", "Reclamos previsionales", "Seguridad social"]),
]
bloques = []
for i, (aid, ic, tit, txt, items) in enumerate(AREAS):
    oscuro = i % 2 == 0           # alterna oscuro / claro (la cabecera es clara)
    lis = "".join(f"<li>{x}</li>" for x in items)
    deco = ('<span class="shard shard-r-br-sm" aria-hidden="true"></span>' if oscuro and i == 0 else
            '<span class="dots dots-dk" aria-hidden="true"></span>' if oscuro else
            '<span class="dots dots-ct" aria-hidden="true"></span>')
    bloques.append(f'''<section class="sec area-blk{' dark' if oscuro else ' light-blk'}{' rev' if i % 2 else ''}" id="{aid}">
  {deco}
  <div class="wrap area-grid">
    <div class="area-tit reveal">
      <span class="area-num">0{i+1}</span>
      <span class="area-ic"><i class="ti {ic}" aria-hidden="true"></i></span>
      <h2 class="h2">{tit}</h2>
    </div>
    <div class="area-txt reveal">
      <p class="area-lead">{txt}</p>
      <ul class="area-items">{lis}</ul>
      <a class="btn btn-red js-wa" href="#" data-msg="Hola, quisiera solicitar un turno por una consulta sobre {tit}.">Consultar sobre esta área</a>
    </div>
  </div>
</section>''')
cab = cabecera("Nuestras", "áreas.", "Áreas", "Asesoramiento jurídico integral para personas y entidades.", "pluma.jpg")
# índice de áreas dentro de la cabecera (una franja aparte rompería la alternancia claro/oscuro)
indice = '    <nav class="area-index rise d3" aria-label="Áreas">' + "".join(f'<a href="#{a[0]}">{a[2]}</a>' for a in AREAS) + '</nav>\n'
cuerpo = cab.replace('  </div>\n</section>\n', indice + '  </div>\n</section>\n', 1) + "\n" + "\n\n".join(bloques)
page("areas.html", "Áreas | Aequitas Estudio Jurídico · Olavarría",
     "Áreas de Aequitas Estudio Jurídico en Olavarría: familia, trabajo y accidentes de trabajo, amparos de salud, sucesiones y civil, empresarial y tributario, previsional.",
     cuerpo)

# ---------------- NOSOTROS ----------------
cuerpo = cabecera("Quiénes", "somos.", "Quiénes somos", "Responsabilidad y confianza en cada caso.", "cuaderno.jpg")
cuerpo += '''
<!-- ============ EL ESTUDIO (oscura) ============ -->
<section class="sec dark estudio">
  <span class="shard shard-r-br-sm" aria-hidden="true"></span>
  <span class="dots dots-dk" aria-hidden="true"></span>
  <div class="wrap estudio-grid">
    <div class="estudio-logo reveal" aria-hidden="true"><img src="./img/logo-blanco.png" alt="" width="1200" height="951" loading="lazy"></div>
    <div class="estudio-txt reveal">
      <p class="divtitle divtitle-l"><span>El estudio</span></p>
      <h2 class="h2">Asesoramiento jurídico <span>integral.</span></h2>
      <p class="sub">Somos los Dres. Walter Sánchez y Maximiliano Gallo Cabrera. Nos desarrollamos en diferentes áreas del derecho: Familia, Trabajo y accidentes de trabajo, Sucesiones, Empresarial y Tributario, Derecho Previsional y de la Seguridad Social, con especial atención a los amparos por cuestiones de salud.</p>
      <p class="sub">Buscamos ofrecer un amplio asesoramiento jurídico integral para personas y entidades con absoluta responsabilidad y confianza.</p>
      <ul class="pilares">
        <li><span class="ic"><i class="ti ti-school" aria-hidden="true"></i></span><span>Egresados de la Universidad Nacional de Lomas de Zamora</span></li>
        <li><span class="ic"><i class="ti ti-certificate" aria-hidden="true"></i></span><span>Matriculados en el Colegio de Abogados del Departamento Judicial de Azul</span></li>
        <li><span class="ic"><i class="ti ti-scale" aria-hidden="true"></i></span><span>Ámbito federal y de la Provincia de Buenos Aires</span></li>
      </ul>
    </div>
  </div>
</section>

<!-- ============ EQUIPO (clara) ============ -->
<section class="sec equipo">
  <span class="dots dots-ct" aria-hidden="true"></span>
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="divtitle"><span>Equipo</span></p>
      <h2 class="h2">Los abogados <span>del estudio.</span></h2>
    </div>
    <div class="equipo-grid">
      <article class="abogado reveal">
        <span class="abogado-ini" aria-hidden="true">WS</span>
        <h3>Dr. Walter Sánchez</h3>
        <p class="mat">Mat. Prov. Tº XIII Fº 168</p>
        <a href="https://www.instagram.com/walter_matias_sanchez/" target="_blank" rel="noopener"><i class="ti ti-brand-instagram" aria-hidden="true"></i>@walter_matias_sanchez</a>
      </article>
      <article class="abogado reveal">
        <span class="abogado-ini" aria-hidden="true">MG</span>
        <h3>Dr. Maximiliano Gallo Cabrera</h3>
        <p class="mat">Mat. Prov. Tº XII Fº 25<br>Fed. Tº 703 Fº 732</p>
        <a href="https://www.instagram.com/maxgallocabrera/" target="_blank" rel="noopener"><i class="ti ti-brand-instagram" aria-hidden="true"></i>@maxgallocabrera</a>
      </article>
    </div>
    <div class="equipo-cta reveal">
      <p>Coronel Suárez 2717, Olavarría · Turnos al 2284-308672 / 2284-649166</p>
      <a class="btn btn-red js-wa" href="#" data-msg="Hola, quisiera solicitar un turno.">Solicitar turno</a>
    </div>
  </div>
</section>'''
page("nosotros.html", "Quiénes somos | Aequitas Estudio Jurídico · Olavarría",
     "Aequitas Estudio Jurídico: Dres. Walter Sánchez y Maximiliano Gallo Cabrera, egresados de la UNLZ y matriculados en el Colegio de Abogados de Azul. Olavarría.",
     cuerpo)
