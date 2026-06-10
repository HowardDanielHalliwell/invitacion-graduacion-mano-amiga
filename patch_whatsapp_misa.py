import re

FILE = r'c:\Users\DanielExelenteHernan\OneDrive - Mano Amiga\Escritorio\Invitación Generación\invitacion-misa.html'
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

NEW_FN = (
    'function compartirMisa(){\n'
    '  const mensaje = `Tenemos el honor de invitarte a nuestra Misa de Fin de Cursos\n'
    'Colegio Mano Amiga Chalco\n'
    '\n'
    'Fecha: 3 de Julio 2026\n'
    'Hora: 11:00 a.m.\n'
    'Lugar: Catedral San Juan Diego\n'
    'Av. Alfredo del Mazo Esq. Tezozómoc, Xico, Méx.\n'
    '\n'
    'Mapa: https://maps.app.goo.gl/STc9iKLNTyhd79rh8\n'
    '\n'
    'Ver invitación: https://invitacion-misa-mano-amiga.vercel.app`;\n'
    '  if(navigator.share){\n'
    '    navigator.share({\n'
    "      title:'Misa de Fin de Cursos — Mano Amiga Chalco',\n"
    '      text: mensaje\n'
    '    });\n'
    '  } else {\n'
    "    window.open('https://wa.me/?text='+encodeURIComponent(mensaje),'_blank');\n"
    '  }\n'
    '}'
)

html, n = re.subn(
    r'function compartirMisa\(\)\{.*?\n\}',
    NEW_FN, html, count=1, flags=re.DOTALL
)
print(f'Reemplazos: {n}')

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Guardado: {len(html):,} chars')
