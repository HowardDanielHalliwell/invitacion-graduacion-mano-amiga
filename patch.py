import re

FILE = r'c:\Users\DanielExelenteHernan\OneDrive - Mano Amiga\Escritorio\Invitación Generación\invitacion-graduacion-mano-amiga.html'

with open(FILE, 'r', encoding='utf-8') as fh:
    html = fh.read()

# ══════════════════════════════════════════════════════
# 1. CONFETI — CSS
# ══════════════════════════════════════════════════════
CONFETI_CSS = """
  /* ── confeti canvas ── */
  #confeti-cv{position:fixed;inset:0;pointer-events:none;z-index:9998;}
"""
html = html.replace('</style>', CONFETI_CSS + '</style>', 1)

# ── canvas tag (antes del splash) ────────────────────
html = html.replace(
    '<!-- ═══ SPLASH SCREEN ═══ -->',
    '<canvas id="confeti-cv"></canvas>\n<!-- ═══ SPLASH SCREEN ═══ -->',
    1
)

# ── función launchConfetti + llamada ────────────────
CONFETI_FN = '''
    function launchConfetti(){
      var cv=document.getElementById('confeti-cv'),x=cv.getContext('2d');
      cv.width=innerWidth; cv.height=innerHeight;
      var CL=['#C9A84C','#E8C97A','#F5820A','#FFFFFF'], P=[], fr=0;
      for(var i=0;i<100;i++) P.push({
        x:Math.random()*cv.width, y:-20-Math.random()*120,
        w:5+Math.random()*9, h:3+Math.random()*5,
        col:CL[Math.floor(Math.random()*CL.length)],
        rot:Math.random()*Math.PI*2,
        vx:(Math.random()-.5)*4, vy:2.5+Math.random()*4.5,
        rv:(Math.random()-.5)*.24, op:1, circ:Math.random()>.5
      });
      (function dr(){
        x.clearRect(0,0,cv.width,cv.height); fr++;
        for(var i=0;i<P.length;i++){
          var p=P[i]; p.x+=p.vx; p.y+=p.vy; p.rot+=p.rv;
          if(fr>120) p.op=Math.max(0,p.op-.012);
          x.save(); x.globalAlpha=p.op;
          x.translate(p.x,p.y); x.rotate(p.rot);
          x.fillStyle=p.col;
          if(p.circ){ x.beginPath(); x.arc(0,0,p.w/2,0,Math.PI*2); x.fill(); }
          else x.fillRect(-p.w/2,-p.h/2,p.w,p.h);
          x.restore();
        }
        if(fr<240) requestAnimationFrame(dr);
        else x.clearRect(0,0,cv.width,cv.height);
      })();
    }
'''
html = html.replace(
    'alive=false;',
    CONFETI_FN + '    alive=false;',
    1
)
html = html.replace(
    "if(sc)sc.style.removeProperty('display');",
    "if(sc){ sc.style.removeProperty('display'); launchConfetti(); }",
    1
)
print('1. Confeti OK')

# ══════════════════════════════════════════════════════
# 2. TIMER — reemplazar función updateCountdown
# ══════════════════════════════════════════════════════
OLD_TIMER = re.search(r'function updateCountdown\(\).*?setInterval\(updateCountdown, 1000\);', html, re.DOTALL)
if OLD_TIMER:
    NEW_TIMER = """function updateCountdown() {
    const target = new Date('2025-07-17T09:45:00');
    const now = new Date();
    const diff = target - now;
    if (diff <= 0) {
      document.getElementById('cd-d').textContent = '\\u00a1Hoy!';
      ['cd-h','cd-m','cd-s'].forEach(id => document.getElementById(id).textContent = '00');
      return;
    }
    const d = Math.floor(diff / 86400000);
    const h = Math.floor((diff % 86400000) / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    document.getElementById('cd-d').textContent = String(d).padStart(2,'0');
    document.getElementById('cd-h').textContent = String(h).padStart(2,'0');
    document.getElementById('cd-m').textContent = String(m).padStart(2,'0');
    document.getElementById('cd-s').textContent = String(s).padStart(2,'0');
  }
  updateCountdown();
  setInterval(updateCountdown, 1000);"""
    html = html[:OLD_TIMER.start()] + NEW_TIMER + html[OLD_TIMER.end():]
    print('2. Timer OK')
else:
    print('2. Timer: no encontrado — revisar manualmente')

# ══════════════════════════════════════════════════════
# 3. WHATSAPP href
# ══════════════════════════════════════════════════════
NEW_HREF = 'href="https://wa.me/?text=%F0%9F%8E%93%20*Ceremonia%20de%20Graduaci%C3%B3n*%20%F0%9F%8E%93%0AXXII%20Generaci%C3%B3n%20de%20Bachillerato%0AColegio%20Mano%20Amiga%20Chalco%0A%0A%F0%9F%93%85%2017%20de%20Julio%202025%0A%F0%9F%95%99%209%3A45%20a.m.%0A%F0%9F%93%8D%20Auditorio%20del%20Colegio%0AAv.%20Cuauht%C3%A9moc%20MZ%201844%20-%20Lote%202%2C%20Col.%20Concepci%C3%B3n%2C%20Xico%2C%20M%C3%A9xico%2056615%0A%0A%F0%9F%97%BA%20https%3A%2F%2Fmaps.google.com%2F%3Fq%3DAv.%2BCuauht%C3%A9moc%2BMZ%2B1844%2BLote%2B2%2BCol%2BConcepci%C3%B3n%2BXico%2BM%C3%A9xico%2B56615"'

old_href = re.search(r'href="https://wa\.me/\?text=[^"]*"', html)
if old_href:
    html = html[:old_href.start()] + NEW_HREF + html[old_href.end():]
    print('3. WhatsApp href OK')
else:
    print('3. WhatsApp: href no encontrado')

# ══════════════════════════════════════════════════════
# 4. DIRECCIÓN Y MAPA — celda Lugar
# ══════════════════════════════════════════════════════
MAP_CSS = """
  .detail-addr{
    font-family:'Montserrat',sans-serif;
    font-size:8px;font-weight:300;color:#777;
    text-align:center;line-height:1.5;margin-top:2px;
  }
  .btn-mapa{
    display:inline-block;margin-top:5px;
    background:#0D1F3C;color:#E8C97A;
    font-family:'Montserrat',sans-serif;font-size:9px;font-weight:500;
    padding:4px 10px;border-radius:20px;text-decoration:none;
    letter-spacing:.5px;transition:opacity .2s;
  }
  .btn-mapa:hover{opacity:.8;}
"""
html = html.replace('</style>', MAP_CSS + '</style>', 1)

MAP_BLOCK = """          <span class="detail-label">Lugar</span>
          <span class="detail-venue">Auditorio</span>
          <span class="detail-venue-sub">Colegio Mano Amiga</span>
          <span class="detail-venue-sub">Chalco</span>
          <span class="detail-addr">Av. Cuauhtémoc MZ 1844 - Lote 2<br>Col. Concepción, Xico, Méx.</span>
          <a class="btn-mapa"
             href="https://maps.google.com/?q=Av.+Cuauht%C3%A9moc+MZ+1844+Lote+2+Col+Concepci%C3%B3n+Xico+M%C3%A9xico+56615"
             target="_blank" rel="noopener">📍 Ver en mapa</a>"""

OLD_LUGAR = """          <span class="detail-label">Lugar</span>
          <span class="detail-venue">Auditorio</span>
          <span class="detail-venue-sub">Colegio Mano Amiga</span>
          <span class="detail-venue-sub">Chalco</span>"""

if OLD_LUGAR in html:
    html = html.replace(OLD_LUGAR, MAP_BLOCK, 1)
    print('4. Dirección + mapa OK')
else:
    print('4. Celda Lugar: bloque no encontrado exacto')

# ══════════════════════════════════════════════════════
# 5. FORMATO — scroll-wrapper más ancho + padding
# ══════════════════════════════════════════════════════
html = html.replace(
    'width: min(620px, 95vw);',
    'width: min(720px, 95vw);',
    1
)
html = html.replace(
    'padding: 52px 60px 44px;',
    'padding: 48px 72px 44px;',
    1
)
html = html.replace(
    '.scroll-content { padding: 36px 28px 32px; }',
    '.scroll-content { padding: 32px 28px 28px; }',
    1
)
print('5. Formato OK')

# ══════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as fh:
    fh.write(html)
print(f'\nArchivo guardado: {len(html):,} chars')
