"""Renderiza una vista previa 3D (ortográfica) de una skin 64x64.

Uso: python3 render_preview.py skin.png preview.png [titulo]
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

# (origen uv, tamaño (w, h, d), posición mínima (x, y, z), inflado)
# x+ = izquierda del personaje, y+ = arriba, z+ = frente.
PARTS = [
    ((0, 0), (8, 8, 8), (-4, 24, -4), 0.0),     # cabeza
    ((16, 16), (8, 12, 4), (-4, 12, -2), 0.0),  # torso
    ((40, 16), (4, 12, 4), (-8, 12, -2), 0.0),  # brazo der.
    ((32, 48), (4, 12, 4), (4, 12, -2), 0.0),   # brazo izq.
    ((0, 16), (4, 12, 4), (-4, 0, -2), 0.0),    # pierna der.
    ((16, 48), (4, 12, 4), (0, 0, -2), 0.0),    # pierna izq.
    ((32, 0), (8, 8, 8), (-4, 24, -4), 0.5),    # sombrero
    ((16, 32), (8, 12, 4), (-4, 12, -2), 0.25), # chaqueta
    ((40, 32), (4, 12, 4), (-8, 12, -2), 0.25), # manga der.
    ((48, 48), (4, 12, 4), (4, 12, -2), 0.25),  # manga izq.
    ((0, 32), (4, 12, 4), (-4, 0, -2), 0.25),   # pantalón der.
    ((0, 48), (4, 12, 4), (0, 0, -2), 0.25),    # pantalón izq.
]

SHADE = {"top": 1.0, "bottom": 0.55, "front": 0.92, "back": 0.92, "right": 0.74, "left": 0.74}


def quads_for(tex, part):
    (u, v), (w, h, d), (bx, by, bz), inf = part
    # tamaño real del cubo inflado; cada píxel de textura escala igual
    x0, y0, z0 = bx - inf, by - inf, bz - inf
    x1, y1, z1 = bx + w + inf, by + h + inf, bz + d + inf
    sx, sy, sz = (x1 - x0) / w, (y1 - y0) / h, (z1 - z0) / d
    out = []

    def emit(name, uv0, cols, rows, corner):
        for j in range(rows):
            for i in range(cols):
                c = tex.getpixel((uv0[0] + i, uv0[1] + j))
                if c[3] == 0:
                    continue
                out.append((name, c, corner(i, j)))

    # frente (z = z1)
    emit("front", (u + d, v + d), w, h, lambda i, j: [
        (x0 + i * sx, y1 - j * sy, z1), (x0 + (i + 1) * sx, y1 - j * sy, z1),
        (x0 + (i + 1) * sx, y1 - (j + 1) * sy, z1), (x0 + i * sx, y1 - (j + 1) * sy, z1)])
    # espalda (z = z0)
    emit("back", (u + 2 * d + w, v + d), w, h, lambda i, j: [
        (x1 - i * sx, y1 - j * sy, z0), (x1 - (i + 1) * sx, y1 - j * sy, z0),
        (x1 - (i + 1) * sx, y1 - (j + 1) * sy, z0), (x1 - i * sx, y1 - (j + 1) * sy, z0)])
    # lado derecho del personaje (x = x0), col 0 = atrás
    emit("right", (u, v + d), d, h, lambda i, j: [
        (x0, y1 - j * sy, z0 + i * sz), (x0, y1 - j * sy, z0 + (i + 1) * sz),
        (x0, y1 - (j + 1) * sy, z0 + (i + 1) * sz), (x0, y1 - (j + 1) * sy, z0 + i * sz)])
    # lado izquierdo (x = x1), col 0 = frente
    emit("left", (u + d + w, v + d), d, h, lambda i, j: [
        (x1, y1 - j * sy, z1 - i * sz), (x1, y1 - j * sy, z1 - (i + 1) * sz),
        (x1, y1 - (j + 1) * sy, z1 - (i + 1) * sz), (x1, y1 - (j + 1) * sy, z1 - i * sz)])
    # arriba (y = y1), fila d-1 = frente
    emit("top", (u + d, v), w, d, lambda i, j: [
        (x0 + i * sx, y1, z0 + j * sz), (x0 + (i + 1) * sx, y1, z0 + j * sz),
        (x0 + (i + 1) * sx, y1, z0 + (j + 1) * sz), (x0 + i * sx, y1, z0 + (j + 1) * sz)])
    # abajo (y = y0)
    emit("bottom", (u + d + w, v), w, d, lambda i, j: [
        (x0 + i * sx, y0, z1 - j * sz), (x0 + (i + 1) * sx, y0, z1 - j * sz),
        (x0 + (i + 1) * sx, y0, z1 - (j + 1) * sz), (x0 + i * sx, y0, z1 - (j + 1) * sz)])
    return out


NORMALS = {"front": (0, 0, 1), "back": (0, 0, -1), "right": (-1, 0, 0),
           "left": (1, 0, 0), "top": (0, 1, 0), "bottom": (0, -1, 0)}


def render(tex, yaw_deg, pitch_deg, scale, size):
    yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)

    def rot(p):
        x, y, z = p
        x, z = x * math.cos(yaw) + z * math.sin(yaw), -x * math.sin(yaw) + z * math.cos(yaw)
        y, z = y * math.cos(pitch) - z * math.sin(pitch), y * math.sin(pitch) + z * math.cos(pitch)
        return x, y, z

    def xf(p):
        return rot((p[0], p[1] - 16, p[2]))  # centra el modelo

    quads = []
    for part in PARTS:
        for name, color, corners in quads_for(tex, part):
            if rot(NORMALS[name])[2] <= 1e-6:  # cara de espaldas a la cámara
                continue
            pts = [xf(c) for c in corners]
            depth = sum(p[2] for p in pts) / 4
            quads.append((depth, name, color, pts))
    quads.sort(key=lambda q: q[0])

    ss = 3  # supersampling
    im = Image.new("RGBA", (size[0] * ss, size[1] * ss), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    cx, cy = size[0] * ss / 2, size[1] * ss / 2
    for _, name, c, pts in quads:
        k = SHADE[name]
        col = (int(c[0] * k), int(c[1] * k), int(c[2] * k), 255)
        poly = [(cx + p[0] * scale * ss, cy - p[1] * scale * ss) for p in pts]
        dr.polygon(poly, fill=col, outline=col)
    return im.resize(size, Image.LANCZOS)


def main():
    skin, out = sys.argv[1], sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else None
    tex = Image.open(skin).convert("RGBA")
    W, H = 1500, 820
    bg = Image.new("RGBA", (W, H))
    top, bot = (24, 32, 66), (9, 12, 28)
    for y in range(H):
        t = y / H
        ImageDraw.Draw(bg).line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))

    views = [render(tex, -30, 12, 17, (520, 700)), render(tex, 150, 12, 17, (520, 700))]
    bg.alpha_composite(views[0], (0, 90))
    bg.alpha_composite(views[1], (450, 90))

    flat = tex.resize((384, 384), Image.NEAREST)
    panel = Image.new("RGBA", (400, 400), (255, 255, 255, 24))
    panel.alpha_composite(flat, (8, 8))
    bg.alpha_composite(panel, (1040, 250))

    d = ImageDraw.Draw(bg)
    try:
        big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except OSError:
        big = small = ImageFont.load_default()
    if title:
        d.text((40, 28), title, font=big, fill=(242, 194, 48))
    d.text((1040, 660), "textura 64x64", font=small, fill=(200, 205, 225))
    bg.convert("RGB").save(out)
    print("vista previa guardada en", out)


if __name__ == "__main__":
    main()
