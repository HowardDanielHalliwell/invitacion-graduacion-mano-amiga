import base64, re

FOLDER = r'c:\Users\DanielExelenteHernan\OneDrive - Mano Amiga\Escritorio\Invitación Generación'
FILE   = FOLDER + r'\invitacion-graduacion-mano-amiga.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

with open(FOLDER + r'\BirreMACH.png', 'rb') as f:
    birre = 'data:image/png;base64,' + base64.b64encode(f.read()).decode()
with open(FOLDER + r'\BACHILLERATO.png', 'rb') as f:
    bach  = 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

print(f'BirreMACH: {len(birre)} chars  |  BACHILLERATO: {len(bach)} chars')

# ─── PASO 1A: CSS del splash ─────────────────────────────────────────────────
SPLASH_CSS = """
  /* ── SPLASH ─────────────────────────────────────── */
  #splash{
    position:fixed;inset:0;z-index:9999;background:#000;
    display:flex;flex-direction:column;
    align-items:center;justify-content:center;gap:22px;
    transition:opacity .8s ease;
  }
  #splash.fade{opacity:0;pointer-events:none;}
  #splash-cv{position:absolute;inset:0;width:100%;height:100%;}
  #splash-inner{
    position:relative;z-index:10;
    display:flex;flex-direction:column;align-items:center;gap:18px;
  }
  #splash-logo{
    width:clamp(90px,16vw,130px);height:auto;
    opacity:0;transform:scale(.48);
    transition:opacity .9s ease,transform .9s cubic-bezier(.175,.885,.32,1.3);
    filter:drop-shadow(0 0 24px rgba(201,168,76,.65)) drop-shadow(0 0 50px rgba(201,168,76,.25));
  }
  #splash-logo.sp-show{opacity:1;transform:scale(1);}
  #splash-title{
    font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:clamp(13px,2.8vw,20px);font-weight:400;
    color:#E8C97A;letter-spacing:4px;text-transform:uppercase;
    text-align:center;min-height:1.5em;
    text-shadow:0 0 20px rgba(201,168,76,.75);
  }
  #splash-sub{
    font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:clamp(11px,2.2vw,16px);font-weight:300;
    color:#E8C97A;letter-spacing:4px;text-align:center;min-height:1.3em;
    text-shadow:0 0 16px rgba(201,168,76,.55);
  }
  .sp-cur{
    display:inline-block;width:2px;height:.85em;
    background:#C9A84C;vertical-align:middle;margin-left:2px;
    animation:spBlink .65s infinite;
  }
  @keyframes spBlink{0%,100%{opacity:1}50%{opacity:0}}
"""
html = html.replace('</style>', SPLASH_CSS + '\n</style>', 1)

# ─── PASO 1B: HTML del splash (logo BirreMACH incrustado) ────────────────────
SPLASH_HTML = (
    '<!-- ═══ SPLASH SCREEN ═══ -->\n'
    '<div id="splash">\n'
    '  <canvas id="splash-cv"></canvas>\n'
    '  <div id="splash-inner">\n'
    '    <img id="splash-logo" src="' + birre + '" alt="Mano Amiga">\n'
    '    <div id="splash-title"><span class="sp-cur"></span></div>\n'
    '    <div id="splash-sub"><span class="sp-cur"></span></div>\n'
    '  </div>\n'
    '</div>\n\n'
)
# Ocultar el scroll-wrapper y poner el splash antes
html = html.replace(
    '<div class="scroll-wrapper">',
    SPLASH_HTML + '<div class="scroll-wrapper" id="main-scroll" style="display:none">',
    1
)

# ─── PASO 1C: JS del splash ───────────────────────────────────────────────────
SPLASH_JS = r"""
  // ═══ SPLASH ═══════════════════════════════════════════════════════════════
  (function(){
    var cv=document.getElementById('splash-cv'),ctx=cv.getContext('2d');
    function rs(){cv.width=innerWidth;cv.height=innerHeight;}
    rs();addEventListener('resize',rs);

    var P=[],alive=true;
    for(var i=0;i<60;i++)P.push({
      x:Math.random()*innerWidth,y:Math.random()*innerHeight,
      r:.7+Math.random()*1.8,op:.15+Math.random()*.5,
      vx:(Math.random()-.5)*.25,vy:-.1-Math.random()*.2,
      t:Math.random()*Math.PI*2
    });
    (function draw(){
      if(!alive)return;
      ctx.clearRect(0,0,cv.width,cv.height);
      for(var i=0;i<P.length;i++){
        var p=P[i];p.t+=.009;
        p.x+=p.vx+Math.sin(p.t*.7)*.14;p.y+=p.vy;
        if(p.y<-4){p.y=cv.height+4;p.x=Math.random()*cv.width;}
        if(p.x<-4)p.x=cv.width+4;if(p.x>cv.width+4)p.x=-4;
        ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
        ctx.fillStyle='rgba(201,168,76,'+p.op+')';ctx.fill();
      }
      requestAnimationFrame(draw);
    })();

    function typeIn(el,text,ms,done){
      var cur=el.querySelector('.sp-cur'),i=0;
      var ti=setInterval(function(){
        el.insertBefore(document.createTextNode(text[i]),cur);
        i++;
        if(i>=text.length){
          clearInterval(ti);
          if(cur)setTimeout(function(){cur.style.display='none';},500);
          if(done)done();
        }
      },ms);
    }

    // Logo aparece a 300ms
    setTimeout(function(){
      document.getElementById('splash-logo').classList.add('sp-show');
    },300);

    // Heading typewriter a 800ms (45ms/letra)
    var HDG='XXII GENERACIÓN DE BACHILLERATO';
    var SUB='Colegio Mano Amiga Chalco';
    setTimeout(function(){
      typeIn(document.getElementById('splash-title'),HDG,45,function(){
        // Sub-título después del heading
        setTimeout(function(){
          typeIn(document.getElementById('splash-sub'),SUB,60,null);
        },300);
      });
    },800);

    // Fade out a 5s → mostrar pergamino
    setTimeout(function(){
      alive=false;
      document.getElementById('splash').classList.add('fade');
      setTimeout(function(){
        document.getElementById('splash').style.display='none';
        var sc=document.getElementById('main-scroll');
        if(sc)sc.style.removeProperty('display');
      },850);
    },5000);
  })();
"""
html = html.replace('</script>', SPLASH_JS + '\n</script>', 1)

# ─── PASO 2: Corregir logos existentes en el pergamino ───────────────────────
# Buscar todas las imágenes base64 en el HTML resultante
imgs = re.findall(r'data:image/png;base64,[A-Za-z0-9+/=]+', html)
print(f'Imágenes base64 en el HTML: {len(imgs)}')
# imgs[0] = splash logo (ya es birre, recién insertado)
# imgs[1] = logo-img (original del pergamino → reemplazar con BirreMACH)
# imgs[2] = bachillerato-img (original → reemplazar con BACHILLERATO)
if len(imgs) >= 3:
    html = html.replace(imgs[1], birre)
    html = html.replace(imgs[2], bach)
    print('logo-img y bachillerato-img reemplazados correctamente.')
elif len(imgs) == 2:
    html = html.replace(imgs[1], birre)
    print('Solo 1 logo original encontrado; se reemplazó logo-img.')
else:
    print('ADVERTENCIA: no se encontraron logos para reemplazar.')

# ─── Escribir resultado ───────────────────────────────────────────────────────
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Archivo guardado: {len(html):,} caracteres.')
