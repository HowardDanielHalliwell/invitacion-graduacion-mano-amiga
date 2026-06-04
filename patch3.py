import re

FILE = r'c:\Users\DanielExelenteHernan\OneDrive - Mano Amiga\Escritorio\Invitación Generación\invitacion-graduacion-mano-amiga.html'

with open(FILE, 'r', encoding='utf-8') as fh:
    html = fh.read()

# ══════════════════════════════════════════════════════
# 1. TIMER — quitar bloque actual e inyectarlo antes de </body>
# ══════════════════════════════════════════════════════
OLD_TIMER_BLOCK = """  // Cuenta regresiva
  function updateCountdown() {
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
  console.log('Timer iniciado', new Date());
  setInterval(updateCountdown, 1000);"""

NEW_TIMER_SCRIPT = """<script>
window.addEventListener('load', function() {
  function updateCountdown() {
    const target = new Date('2025-07-17T09:45:00');
    const now = new Date();
    const diff = target - now;
    if (diff <= 0) {
      document.getElementById('cd-d').textContent = '\\u00a1Hoy!';
      ['cd-h','cd-m','cd-s'].forEach(id => {
        document.getElementById(id).textContent = '00';
      });
      return;
    }
    document.getElementById('cd-d').textContent = String(Math.floor(diff/86400000)).padStart(2,'0');
    document.getElementById('cd-h').textContent = String(Math.floor((diff%86400000)/3600000)).padStart(2,'0');
    document.getElementById('cd-m').textContent = String(Math.floor((diff%3600000)/60000)).padStart(2,'0');
    document.getElementById('cd-s').textContent = String(Math.floor((diff%60000)/1000)).padStart(2,'0');
  }
  updateCountdown();
  setInterval(updateCountdown, 1000);
});
</script>"""

if OLD_TIMER_BLOCK in html:
    html = html.replace(OLD_TIMER_BLOCK, '', 1)
    print('1a. Bloque timer eliminado del script original OK')
else:
    print('1a. ADVERTENCIA: bloque timer no encontrado exacto — revisar manualmente')

if '</body>' in html:
    html = html.replace('</body>', NEW_TIMER_SCRIPT + '\n</body>', 1)
    print('1b. Timer inyectado antes de </body> OK')
else:
    print('1b. ADVERTENCIA: </body> no encontrado')

# ══════════════════════════════════════════════════════
# 2. TEXTO — agregar "la" al final de la frase
# ══════════════════════════════════════════════════════
OLD_TEXT = '<p class="invitation-label">Con orgullo te invitamos a</p>'
NEW_TEXT = '<p class="invitation-label">Con orgullo te invitamos a la</p>'

if OLD_TEXT in html:
    html = html.replace(OLD_TEXT, NEW_TEXT, 1)
    print('2. Texto "a la" OK')
else:
    print('2. ADVERTENCIA: texto no encontrado exacto')

# ══════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as fh:
    fh.write(html)
print(f'\nArchivo guardado: {len(html):,} chars')
