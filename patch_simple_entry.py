import re, os

FOLDER = r'c:\Users\DanielExelenteHernan\OneDrive - Mano Amiga\Escritorio\Invitación Generación'
FILE   = FOLDER + r'\invitacion-misa.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════
# 1. ELIMINAR CSS del libro (bloque entero)
# ══════════════════════════════════════════════════════
OLD_LIBRO_CSS = """/* ══════════════════════════════════════════════════
   LIBRO
══════════════════════════════════════════════════ */
#libro-wrapper{
  position:fixed;inset:0;
  display:flex;align-items:center;justify-content:center;
  background:var(--cream);
  perspective:1200px;
  z-index:100;
  opacity:0;
  transition:opacity .5s ease;
}
#libro{
  position:relative;
  width:min(560px,90vw);
  height:min(76vh,520px);
  transform-style:preserve-3d;
}
.tapa{
  position:absolute;
  width:50%;height:100%;
  background:linear-gradient(135deg,#2A1A0E 0%,#3D2510 40%,#4A3520 100%);
  border:2px solid var(--gold);
  transform-style:preserve-3d;
  overflow:hidden;
  transition:transform 1.4s cubic-bezier(0.4,0,0.2,1),
             box-shadow 1.4s ease;
  backface-visibility:hidden;
}
.tapa::after{
  content:'';position:absolute;inset:0;
  background-image:repeating-linear-gradient(
    45deg,transparent,transparent 3px,
    rgba(255,255,255,.02) 3px,rgba(255,255,255,.02) 4px);
  pointer-events:none;
}
#tapa-izq{left:0;transform-origin:right center;border-right:none;}
#tapa-izq.open{
  transform:rotateY(-175deg);
  box-shadow:-10px 0 48px rgba(0,0,0,.5);
}
#tapa-der{right:0;transform-origin:left center;border-left:none;}
#tapa-der.open{
  transform:rotateY(175deg);
  box-shadow:10px 0 48px rgba(0,0,0,.5);
}
#lomo{
  position:absolute;
  left:calc(50% - 8px);width:16px;height:100%;
  background:linear-gradient(to right,
    var(--gold-dk),var(--gold),var(--gold-lt),var(--gold),var(--gold-dk));
  z-index:10;
  box-shadow:0 0 14px rgba(201,168,76,.5);
}
.tapa-inner{
  position:absolute;inset:0;
  padding:28px 20px;
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:10px;
}
.tapa-inner::before{
  content:'';position:absolute;inset:10px;
  border:1px solid rgba(201,168,76,.35);pointer-events:none;
}
.tapa-corner{position:absolute;width:20px;height:20px;}
.tapa-corner.tl{top:16px;left:16px;}
.tapa-corner.tr{top:16px;right:16px;transform:rotate(90deg);}
.tapa-corner.bl{bottom:16px;left:16px;transform:rotate(-90deg);}
.tapa-corner.br{bottom:16px;right:16px;transform:rotate(180deg);}
.tapa-logo{width:68px;height:auto;opacity:.88;}
.tapa-title-sm{
  font-family:'Great Vibes',cursive;
  font-size:clamp(20px,3.8vw,30px);
  color:var(--gold-lt);text-align:center;line-height:1.1;
}
.tapa-title-lg{
  font-family:'Great Vibes',cursive;
  font-size:clamp(26px,5vw,38px);
  color:var(--gold);text-align:center;line-height:1.05;
}
.tapa-school{
  font-family:'Montserrat',sans-serif;
  font-size:clamp(6px,1.1vw,8px);font-weight:400;
  letter-spacing:2.5px;color:rgba(232,201,122,.55);
  text-transform:uppercase;text-align:center;
}
.tapa-orn{display:flex;align-items:center;gap:6px;width:78%;}
.tapa-orn-bar{flex:1;height:1px;background:rgba(201,168,76,.4);}
.tapa-orn-dia{width:5px;height:5px;background:var(--gold);transform:rotate(45deg);flex-shrink:0;}
#libro-wrapper.hide{opacity:0;pointer-events:none;}"""

if OLD_LIBRO_CSS in html:
    html = html.replace(OLD_LIBRO_CSS, '', 1)
    print('1. CSS libro eliminado OK')
else:
    print('1. CSS libro: bloque no encontrado')

# ══════════════════════════════════════════════════════
# 2. AGREGAR opacity/transform/transition a #full-card
# ══════════════════════════════════════════════════════
OLD_CARD_CSS = """#full-card{
  position:relative;z-index:10;
  min-height:100vh;
  display:flex;flex-direction:column;align-items:center;
  padding:48px 0 60px;
}"""

NEW_CARD_CSS = """#full-card{
  position:relative;z-index:10;
  min-height:100vh;
  display:flex;flex-direction:column;align-items:center;
  padding:48px 0 60px;
  opacity:0;
  transform:scale(0.92);
  transition:opacity 1.2s cubic-bezier(0.16,1,0.3,1) .3s,
             transform 1.2s cubic-bezier(0.16,1,0.3,1) .3s;
}"""

if OLD_CARD_CSS in html:
    html = html.replace(OLD_CARD_CSS, NEW_CARD_CSS, 1)
    print('2. CSS full-card OK')
else:
    print('2. CSS full-card: bloque no encontrado')

# ══════════════════════════════════════════════════════
# 3. ELIMINAR HTML del libro-wrapper
# ══════════════════════════════════════════════════════
m_html = re.search(
    r'<!-- [^\n]*LIBRO[^\n]* -->\n<div id="libro-wrapper">.*?^</div>\n',
    html, re.DOTALL | re.MULTILINE
)
if m_html:
    html = html[:m_html.start()] + html[m_html.end():]
    print('3. HTML libro eliminado OK')
else:
    print('3. HTML libro: bloque no encontrado')

# ══════════════════════════════════════════════════════
# 4. REEMPLAZAR JS del libro por animacion simple
# ══════════════════════════════════════════════════════
m_js = re.search(
    r'// ── Libro que se abre ─.*?\}\)\(\);',
    html, re.DOTALL
)
if m_js:
    NEW_JS = """// ── Entrada fade + scale ──────────────────────────────────────────
(function(){
  const card = document.getElementById('full-card');
  const secs = card.querySelectorAll(
    '.card-logo,.orn-line,.inv-label,.title-misa,.title-fin,' +
    '.school-label,.quote-wrap,.cd-wrap,.ev-cols,.sig-wrap,.wa-wrap'
  );
  secs.forEach(el=>{
    el.style.opacity   = '0';
    el.style.transform = 'translateY(16px)';
  });
  // Dispara la transicion CSS (doble rAF para que el navegador registre el estado inicial)
  requestAnimationFrame(()=>{ requestAnimationFrame(()=>{
    card.style.opacity   = '1';
    card.style.transform = 'scale(1)';
  }); });
  // Stagger de secciones al terminar la animacion (0.3s delay + 1.2s duracion)
  setTimeout(()=>{
    secs.forEach((el,i)=>{
      el.style.transition = 'none';
      setTimeout(()=>{
        el.style.transition = 'opacity .45s ease, transform .45s ease';
        el.style.opacity    = '1';
        el.style.transform  = 'translateY(0)';
      }, i * 80);
    });
  }, 1500);
})();"""
    html = html[:m_js.start()] + NEW_JS + html[m_js.end():]
    print('4. JS OK')
else:
    print('4. JS: bloque no encontrado')

# ══════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'\nArchivo guardado: {len(html):,} chars')
