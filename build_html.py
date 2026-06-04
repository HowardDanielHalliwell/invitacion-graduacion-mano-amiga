import base64, os

folder = r"c:\Users\DanielExelenteHernan\OneDrive - Mano Amiga\Escritorio\Invitación Generación"
logo_b64 = base64.b64encode(open(os.path.join(folder, "BirreMACH.png"), "rb").read()).decode()
bach_b64 = base64.b64encode(open(os.path.join(folder, "BACHILLERATO.png"), "rb").read()).decode()

html = open(os.path.join(folder, "_template.html"), "r", encoding="utf-8").read()
html = html.replace("LOGO_PLACEHOLDER", logo_b64)
html = html.replace("BACH_PLACEHOLDER", bach_b64)

out = os.path.join(folder, "invitacion-graduacion.html")
open(out, "w", encoding="utf-8").write(html)
print(f"OK: {os.path.getsize(out):,} bytes")