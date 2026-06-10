import re, os

FOLDER = r'c:\Users\DanielExelenteHernan\OneDrive - Mano Amiga\Escritorio\Invitación Generación'
FILE   = FOLDER + r'\invitacion-misa.html'
LOGO   = open(FOLDER + r'\logo_misa_b64.txt').read().strip()

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════
# 1. REEMPLAZAR CSS del sobre/destello por CSS del libro
# ══════════════════════════════════════════════════════
OLD_CSS = """/* ══════════════════════════════════════════════════
   ENVELOPE SCENE
══════════════════════════════════════════════════ */
/* ── Destello al aterrizar ── */
#destello{
  position:fixed;inset:0;
  pointer-events:none;
  z-index:50;
  opacity:0;
  background:radial-gradient(ellipse at center,
    rgba(232,201,122,.55) 0%,
    rgba(201,168,76,.25) 40%,
    transparent 70%);
  filter:blur(20px);
}"""

LIBRO_CSS = """/* ══════════════════════════════════════════════════
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

if OLD_CSS in html:
    html = html.replace(OLD_CSS, LIBRO_CSS, 1)
    print('1. CSS OK')
else:
    print('1. CSS: bloque no encontrado')

# ══════════════════════════════════════════════════════
# 2. REEMPLAZAR HTML del destello por HTML del libro
# ══════════════════════════════════════════════════════
# search with regex
m_html = re.search(r'<!-- [^\n]* DESTELLO [^\n]* -->\s*<div id="destello"></div>', html)
if m_html:
    TAPA_CONTENT = f'''      <div class="tapa-inner">
        <svg class="tapa-corner tl" viewBox="0 0 20 20"><path d="M2,2 L2,10 M2,2 L10,2" stroke="#C9A84C" stroke-width="1.5" fill="none"/></svg>
        <svg class="tapa-corner tr" viewBox="0 0 20 20"><path d="M2,2 L2,10 M2,2 L10,2" stroke="#C9A84C" stroke-width="1.5" fill="none"/></svg>
        <svg class="tapa-corner bl" viewBox="0 0 20 20"><path d="M2,2 L2,10 M2,2 L10,2" stroke="#C9A84C" stroke-width="1.5" fill="none"/></svg>
        <svg class="tapa-corner br" viewBox="0 0 20 20"><path d="M2,2 L2,10 M2,2 L10,2" stroke="#C9A84C" stroke-width="1.5" fill="none"/></svg>
        <svg width="26" height="34" viewBox="0 0 26 34" fill="none">
          <line x1="13" y1="2" x2="13" y2="32" stroke="#C9A84C" stroke-width="1.5"/>
          <line x1="2" y1="13" x2="24" y2="13" stroke="#C9A84C" stroke-width="1.5"/>
          <circle cx="13" cy="13" r="3.5" stroke="#C9A84C" stroke-width="1" fill="none"/>
        </svg>
        <img class="tapa-logo" src="data:image/png;base64,{LOGO}" alt="Mano Amiga">
        <div class="tapa-orn"><div class="tapa-orn-bar"></div><div class="tapa-orn-dia"></div><div class="tapa-orn-bar"></div></div>
        <p class="tapa-title-sm">Misa de</p>
        <p class="tapa-title-lg">Fin de Cursos</p>
        <div class="tapa-orn"><div class="tapa-orn-bar"></div><div class="tapa-orn-dia"></div><div class="tapa-orn-bar"></div></div>
        <p class="tapa-school">Colegio Mano Amiga Chalco</p>
      </div>'''

    TAPA_MIR = TAPA_CONTENT.replace('class="tapa-inner"', 'class="tapa-inner" style="transform:scaleX(-1)"', 1)

    LIBRO_HTML = f'''<!-- ═══ LIBRO ═══ -->
<div id="libro-wrapper">
  <div id="libro">
    <div id="tapa-izq" class="tapa">
{TAPA_CONTENT}
    </div>
    <div id="tapa-der" class="tapa">
{TAPA_MIR}
    </div>
    <div id="lomo"></div>
  </div>
</div>'''
    html = html[:m_html.start()] + LIBRO_HTML + html[m_html.end():]
    print('2. HTML OK')
else:
    print('2. HTML: bloque no encontrado')

# ══════════════════════════════════════════════════════
# 3. REEMPLAZAR JS de carta cayendo por JS del libro
# ══════════════════════════════════════════════════════
m_js = re.search(
    r'// ── Carta que cae del cielo ─.*?setTimeout\(startFall, FALL_START\);\s*\}\)\(\);',
    html, re.DOTALL
)
if m_js:
    LIBRO_JS = """// ── Libro que se abre ─────────────────────────────────────────
(function(){
  const wrapper = document.getElementById('libro-wrapper');
  const tapIzq  = document.getElementById('tapa-izq');
  const tapDer  = document.getElementById('tapa-der');
  const card    = document.getElementById('full-card');

  card.style.opacity       = '0';
  card.style.pointerEvents = 'none';

  // Fase 1: libro aparece (fade-in)
  setTimeout(()=>{ wrapper.style.opacity = '1'; }, 80);

  // Fase 2: tapas se abren (800ms)
  setTimeout(()=>{
    tapIzq.classList.add('open');
    tapDer.classList.add('open');
  }, 800);

  // Fase 3: libro hace fade-out (2300ms)
  setTimeout(()=>{ wrapper.classList.add('hide'); }, 2300);

  // Fase 4: tarjeta aparece con fadeUp stagger (2800ms)
  setTimeout(()=>{
    wrapper.style.display = 'none';
    card.style.transition = 'opacity .6s ease';
    card.style.opacity    = '1';
    card.style.pointerEvents = 'auto';
    const secs = card.querySelectorAll(
      '.card-logo,.orn-line,.inv-label,.title-misa,.title-fin,' +
      '.school-label,.quote-wrap,.cd-wrap,.ev-cols,.sig-wrap,.wa-wrap'
    );
    secs.forEach((el,i)=>{
      el.style.opacity   = '0';
      el.style.transform = 'translateY(16px)';
      el.style.transition= 'none';
      setTimeout(()=>{
        el.style.transition = 'opacity .45s ease, transform .45s ease';
        el.style.opacity    = '1';
        el.style.transform  = 'translateY(0)';
      }, i * 100);
    });
  }, 2800);
})();"""
    html = html[:m_js.start()] + LIBRO_JS + html[m_js.end():]
    print('3. JS OK')
else:
    print('3. JS: bloque no encontrado')

# ══════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'\nArchivo guardado: {len(html):,} chars')
