#!/usr/bin/env python3
"""Wrap the generated SVG in a print-ready A4 HTML, plus a monthly emotion tracker."""

with open("/Users/ckk/Desktop/duygu-carki/duygu-carki.svg") as f:
    svg = f.read()

CORES = [
    ("Mutlu", "#F4C430"), ("Şaşkın", "#E8833A"), ("Kızgın", "#DB504A"),
    ("Korkmuş", "#9B6FB0"), ("Üzgün", "#4F8FCB"), ("Sakin", "#56B27E"),
]

legend = "".join(
    f'<span class="chip"><i style="background:{c}"></i>{n}</span>' for n, c in CORES
)

# 31-day grid: each box has the day number and a blank circle to color
boxes = "".join(
    f'<div class="day"><span class="num">{d}</span><span class="dot"></span></div>'
    for d in range(1, 32)
)

html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>Duygu Çarkı ve Duygu Takvimim</title>
<style>
  @page {{ size: A4; margin: 12mm; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: 'Nunito', 'Segoe UI', Verdana, sans-serif; color: #333; }}
  .page {{ width: 186mm; min-height: 263mm; margin: 0 auto; padding: 4mm 0;
           display: flex; flex-direction: column; align-items: center;
           page-break-after: always; }}
  .page:last-child {{ page-break-after: auto; }}
  h1 {{ font-size: 26px; margin: 2mm 0 0; color: #2b2b2b; text-align: center; }}
  .sub {{ font-size: 13px; color: #777; margin: 1mm 0 3mm; text-align: center; }}
  .wheel {{ width: 165mm; max-width: 100%; }}
  .howto {{ font-size: 12.5px; color: #555; max-width: 165mm; margin-top: 3mm;
            line-height: 1.5; }}
  .howto b {{ color: #333; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 6px 14px; justify-content: center;
             margin: 3mm 0 4mm; }}
  .chip {{ font-size: 13px; font-weight: 700; display: inline-flex; align-items: center; }}
  .chip i {{ width: 13px; height: 13px; border-radius: 50%; display: inline-block;
             margin-right: 5px; border: 1px solid rgba(0,0,0,.15); }}
  .grid {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px;
           width: 165mm; }}
  .day {{ border: 1.5px solid #e3ddcb; border-radius: 9px; aspect-ratio: 1 / 1;
          display: flex; flex-direction: column; align-items: center;
          justify-content: center; background: #FFFDF7; }}
  .day .num {{ font-size: 12px; font-weight: 800; color: #999; align-self: flex-start;
               margin: 4px 0 0 6px; }}
  .dot {{ width: 26px; height: 26px; border-radius: 50%; border: 2px dashed #cfc6b0;
          margin-top: 2px; }}
  .note {{ font-size: 11.5px; color: #888; margin-top: 4mm; max-width: 165mm;
           text-align: center; }}
</style>
</head>
<body>
  <section class="page">
    <h1>Duygu Çarkı 🎡</h1>
    <div class="sub">Bugün içinden hangi duygu geçiyor? Çarkta bul ve göster.</div>
    <div class="wheel">{svg}</div>
    <div class="howto">
      <b>Nasıl kullanılır?</b> Ortadaki 6 ana duygudan sana en yakın olanı seç
      (örneğin <b>Mutlu</b>). Sonra o rengin dış halkasındaki daha ince
      duygulardan birini bul (örneğin <b>Minnettar</b> ya da <b>Heyecanlı</b>).
      Duygunun adını yüksek sesle söyle ve “Bu duyguyu ne zaman hissettim?”
      diye birlikte konuşun. Doğru ya da yanlış duygu yoktur — hepsi değerlidir. 💛
    </div>
  </section>

  <section class="page">
    <h1>Duygu Takvimim 📅</h1>
    <div class="sub">Her gün kendini nasıl hissettiysen o renkle daireyi boya.</div>
    <div class="legend">{legend}</div>
    <div class="grid">{boxes}</div>
    <div class="note">
      Ay: ____________  •  Günün sonunda “Bugün en çok hangi duyguyu yaşadın?”
      diye sor ve o ana duygunun rengiyle boya. Hafta sonunda birlikte
      çarka bakıp konuşun.
    </div>
  </section>
</body>
</html>
"""

with open("/Users/ckk/Desktop/duygu-carki/duygu-carki.html", "w") as f:
    f.write(html)
print("HTML written, len:", len(html))
