import re

FILE = r'c:\Users\DanielExelenteHernan\OneDrive - Mano Amiga\Escritorio\Invitación Generación\invitacion-graduacion-mano-amiga.html'
MAP_SHORT = 'https://maps.app.goo.gl/z5i5deGXQhGKLmnG9'

with open(FILE, 'r', encoding='utf-8') as fh:
    html = fh.read()

# ══════════════════════════════════════════════════════
# 1. MAPS — reemplazar TODOS los links de Google Maps
# ══════════════════════════════════════════════════════

# 1a. Link literal en btn-mapa
old_map_literal = 'href="https://maps.google.com/?q=Av.+Cuauht%C3%A9moc+MZ+1844+Lote+2+Col+Concepci%C3%B3n+Xico+M%C3%A9xico+56615"'
new_map_literal = f'href="{MAP_SHORT}"'
if old_map_literal in html:
    html = html.replace(old_map_literal, new_map_literal, 1)
    print('1a. Maps btn-mapa OK')
else:
    print('1a. Maps btn-mapa: no encontrado')

# 1b. Link URL-encoded dentro del href de WhatsApp (cualquier maps.google.com codificado)
old_map_encoded = 'https%3A%2F%2Fmaps.google.com%2F%3Fq%3DAv.%2BCuauht%C3%A9moc%2BMZ%2B1844%2BLote%2B2%2BCol%2BConcepci%C3%B3n%2BXico%2BM%C3%A9xico%2B56615'
new_map_encoded = 'https%3A%2F%2Fmaps.app.goo.gl%2Fz5i5deGXQhGKLmnG9'
if old_map_encoded in html:
    html = html.replace(old_map_encoded, new_map_encoded)
    print('1b. Maps WA encoded OK')
else:
    print('1b. Maps WA encoded: no encontrado (se reemplazará junto con todo el href en paso 3)')

print('1. Maps OK')

# ══════════════════════════════════════════════════════
# 2. TIMER — agregar console.log antes del setInterval
# ══════════════════════════════════════════════════════
OLD_INTERVAL = '  updateCountdown();\n  setInterval(updateCountdown, 1000);'
NEW_INTERVAL = "  updateCountdown();\n  console.log('Timer iniciado', new Date());\n  setInterval(updateCountdown, 1000);"

if OLD_INTERVAL in html:
    html = html.replace(OLD_INTERVAL, NEW_INTERVAL, 1)
    print('2. Timer console.log OK')
else:
    print('2. Timer: bloque no encontrado exacto')

# ══════════════════════════════════════════════════════
# 3. WHATSAPP href — texto nuevo con link corto
# ══════════════════════════════════════════════════════
NEW_WA_TEXT = (
    '%F0%9F%8E%93%20*CEREMONIA%20DE%20GRADUACI%C3%93N*%20%F0%9F%8E%93%0A'
    '*XXII%20Generaci%C3%B3n%20de%20Bachillerato*%0A'
    'Colegio%20Mano%20Amiga%20Chalco%0A%0A'
    '%F0%9F%93%85%20*Fecha%3A*%2017%20de%20Julio%202025%0A'
    '%F0%9F%95%99%20*Hora%3A*%209%3A45%20a.m.%0A'
    '%F0%9F%93%8D%20*Lugar%3A*%20Auditorio%20del%20Colegio%0A'
    'Av.%20Cuauht%C3%A9moc%20MZ%201844%20-%20Lote%202%0A'
    'Col.%20Concepci%C3%B3n%2C%20Xico%2C%20M%C3%A9x.%2056615%0A%0A'
    '%F0%9F%97%BA%20*Mapa%3A*%20https%3A%2F%2Fmaps.app.goo.gl%2Fz5i5deGXQhGKLmnG9'
)
NEW_WA_HREF = f'href="https://wa.me/?text={NEW_WA_TEXT}"'

old_wa = re.search(r'href="https://wa\.me/\?text=[^"]*"', html)
if old_wa:
    html = html[:old_wa.start()] + NEW_WA_HREF + html[old_wa.end():]
    print('3. WhatsApp href OK')
else:
    print('3. WhatsApp: href no encontrado')

# ══════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as fh:
    fh.write(html)
print(f'\nArchivo guardado: {len(html):,} chars')
