"""Genera la skin victorMC (64x64, brazos clásicos de 4 px).

Concepto: "Victor" = vencedor. Corona de laurel dorada (capa del sombrero),
sudadera azul marino con una "V" dorada en el pecho y "MC" en la espalda,
puños y franjas doradas, vaqueros oscuros y zapatillas blancas.

Uso: python3 make_skin.py [salida.png]
"""
import random
import sys

from PIL import Image

PAL = {
    ".": None,
    # piel
    "S": "#C98B60", "s": "#B47650", "L": "#D99D72", "n": "#A86A45",
    # pelo
    "H": "#2A1B12", "h": "#3F2A1B", "k": "#1B110B",
    # ojos y boca
    "W": "#F4F4F4", "I": "#3C5FA8", "M": "#6E3727", "m": "#93543C",
    # sudadera
    "N": "#22346E", "D": "#1A2858", "E": "#2E4590", "X": "#131C42",
    # dorado
    "G": "#F2C230", "g": "#C8961C", "Y": "#FFE27A", "j": "#9C7012",
    # blanco
    "w": "#EDEDED", "v": "#CDCDCD", "u": "#FFFFFF",
    # pantalón
    "P": "#2B2C33", "p": "#222329", "Q": "#34363F",
    # suela
    "O": "#9C9C9C", "o": "#7A7A7A",
}


def rgba(c):
    if c is None:
        return (0, 0, 0, 0)
    c = c.lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), 255)


img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
px = img.load()
rng = random.Random(29)


def face(x, y, rows):
    rows = [r.replace(" ", "") for r in rows]
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            px[x + i, y + j] = rgba(PAL[ch])


def fill(x, y, w, h, base, vary="", p=0.0):
    """Relleno con un poco de ruido para dar textura."""
    for j in range(h):
        for i in range(w):
            ch = base
            if vary and rng.random() < p:
                ch = rng.choice(vary)
            px[x + i, y + j] = rgba(PAL[ch])


def grid(w, h, base, vary="", p=0.0):
    return [
        "".join(rng.choice(vary) if vary and rng.random() < p else base for _ in range(w))
        for _ in range(h)
    ]


def stamp(rows, overlay):
    """Pone 'overlay' (con '.' transparente) encima de 'rows'."""
    out = []
    for r, o in zip(rows, overlay):
        o = o.replace(" ", "")
        out.append("".join(oc if oc != "." else rc for rc, oc in zip(r, o)))
    return out


# ---------------------------------------------------------------- CABEZA
face(8, 0, grid(8, 8, "H", "hk", 0.35))          # arriba
fill(16, 0, 8, 8, "s")                            # abajo
face(8, 8, [                                      # frente
    "H h H H h H H H",
    "H H L H H H h H",
    "H L S S S S H H",
    "H k k S S k k H",
    "S W I S S I W S",
    "S S S n n S S S",
    "S S s M M s S S",
    "s S S S S S S s",
])
face(0, 8, [                                      # lado derecho (frente = col 7)
    "H H H h H H H H",
    "H h H H H H h H",
    "H H H H H H H H",
    "H H H H H S S H",
    "H H S n S S S S",
    "H H S n s S S S",
    "H S S S S S S S",
    "s s S S S S S s",
])
face(16, 8, [                                     # lado izquierdo (frente = col 0)
    "H H H H h H H H",
    "H h H H H H h H",
    "H H H H H H H H",
    "H S S H H H H H",
    "S S S S n S H H",
    "S S S s n S H H",
    "S S S S S S S H",
    "s S S S S S s s",
])
face(24, 8, [                                     # nuca
    "H H h H H H h H",
    "H H H H h H H H",
    "h H H H H H H h",
    "H H H k H H H H",
    "H H H H H H H H",
    "H k H H H H k H",
    "H H H H H H H H",
    "s s s s s s s s",
])

# --------------------------------------------- SOMBRERO: corona de laurel
face(40, 0, [                                     # arriba: volumen del tupé
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . h H . . .",
    ". . h H H h . .",
])
face(40, 8, [                                     # frente: puntas de laurel
    "Y G h H H h G Y",
    "G g . . . . g G",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
])
LAUREL_SIDE = [
    ". Y . . Y . . Y",
    "G G j G G j G G",
    "j . G j . G j .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
]
face(32, 8, LAUREL_SIDE)                          # lado derecho
face(48, 8, [r[::-1] for r in LAUREL_SIDE])       # lado izquierdo (espejo)
face(56, 8, [                                     # nuca: lazo
    "Y . . . . . . Y",
    "G G G j j G G G",
    ". j G j j G j .",
    ". . . g g . . .",
    ". . . g . g . .",
    ". . . . . . . .",
    ". . . . . . . .",
    ". . . . . . . .",
])

# ---------------------------------------------------------------- TORSO
face(20, 16, grid(8, 4, "N", "D", 0.2))           # arriba
face(28, 16, grid(8, 4, "D", "X", 0.2))           # abajo
NAVY_8x12 = grid(8, 12, "N", "D", 0.06)
face(20, 20, stamp(NAVY_8x12, [                   # frente: "V" dorada
    "E E s s s s E E",
    "D E w s s w E D",
    ". . w E E w . .",
    ". . v . . v . .",
    "Y G . . . . G g",
    ". Y G . . G g .",
    ". . Y G G g . .",
    ". . . G g . . .",
    ". . . . . . . .",
    ". E E E E E E .",
    ". D D D D D D .",
    "X X X X X X X X",
]))
face(32, 20, stamp(grid(8, 12, "N", "D", 0.06), [  # espalda: capucha + "MC"
    "E E E E E E E E",
    "E D D X X D D E",
    ". E D D D D E .",
    ". . E E E E . .",
    ". . . . . . . .",
    "G . . . G . G G",
    "G G . G G . G .",
    "G . G . G . G .",
    "g . . . g . g .",
    "g . . . g . g g",
    ". . . . . . . .",
    "X X X X X X X X",
]))
for sx in (16, 28):                               # costados
    face(sx, 20, stamp(grid(4, 12, "N", "D", 0.07), [
        "E E E E", ". . . .", ". . . .", ". . . .", ". . . .", ". . . .",
        ". . . .", ". . . .", ". . . .", ". . . .", ". . . .", "X X X X",
    ]))

# chaqueta (capa exterior): cuello de la capucha en 3D
face(20, 32, [                                    # arriba: anillo de capucha
    "E E E E E E E E",
    "E . . . . . . E",
    "E . . . . . . E",
    "E . . . . . . E",
])
face(20, 36, ["E E . . . . E E"] + [". . . . . . . ."] * 11)
face(32, 36, [
    "E E E E E E E E",
    "E D D X X D D E",
    ". E D D D D E .",
    ". . E E E E . .",
] + [". . . . . . . ."] * 8)
face(16, 36, ["E . . ."] + [". . . ."] * 11)       # costado der. (atrás = col 0)
face(28, 36, [". . . E"] + [". . . ."] * 11)       # costado izq. (atrás = col 3)


# ---------------------------------------------------------------- BRAZOS
def arm(top, bottom, outer, front, inner, back, mirror):
    face(*top, grid(4, 4, "N", "E", 0.25))
    fill(*bottom, 4, 4, "s")
    sleeve = lambda: grid(4, 9, "N", "D", 0.07)
    cuff_hand = ["G G G G", "S S S S", "s S S s"]
    stripe = [". Y G .", ". Y G .", ". Y G .", ". Y G .", ". Y G .",
              ". Y G .", ". Y G .", ". Y G .", ". g g ."]
    if mirror:
        stripe = [r[::-1] for r in stripe]
    face(*outer, stamp(sleeve(), stripe) + cuff_hand)
    face(*front, stamp(sleeve(), ["E . . ."] * 9 if not mirror else [". . . E"] * 9) + cuff_hand)
    face(*inner, sleeve() + ["g g g g", "S S S S", "s S S s"])
    face(*back, sleeve() + ["G G G G", "S S S S", "s S S s"])


# brazo derecho
arm((44, 16), (48, 16), (40, 20), (44, 20), (48, 20), (52, 20), mirror=False)
# brazo izquierdo
arm((36, 48), (40, 48), (40, 52), (36, 52), (32, 52), (44, 52), mirror=True)

# mangas (capa exterior): puños dorados en relieve
EMPTY_ARM = [". . . ."] * 9
for (ox, oy) in ((40, 36), (44, 36), (48, 36), (52, 36),     # manga der.
                 (48, 52), (52, 52), (56, 52), (60, 52)):    # manga izq.
    face(ox, oy, EMPTY_ARM + ["Y G G g", ". . . .", ". . . ."])


# ---------------------------------------------------------------- PIERNAS
def leg(top, bottom, outer, front, inner, back, mirror):
    face(*top, grid(4, 4, "p", "P", 0.3))
    fill(*bottom, 4, 4, "o")
    jeans = lambda: grid(4, 9, "P", "p", 0.12)
    knee = ["p p p p", ". . . .", ". . . .", ". . . .", ". . . .",
            ". Q Q .", ". . . .", ". . . .", "Q Q Q Q"]
    face(*front, stamp(jeans(), knee) + ["w v v w", "w w w w", "O O O O"])
    swoosh = ["w w w w", "w G G Y", "O O O O"]
    if mirror:
        swoosh = [r.replace(" ", "")[::-1] for r in swoosh]
    face(*outer, stamp(jeans(), ["p p p p"] + [". . . ."] * 8) + swoosh)
    face(*inner, stamp(jeans(), ["p p p p"] + [". . . ."] * 8) + ["w w w w", "w w w w", "O O O O"])
    face(*back, stamp(jeans(), ["p p p p"] + [". . . ."] * 8) + ["w G G w", "w w w w", "O O O O"])


# pierna derecha
leg((4, 16), (8, 16), (0, 20), (4, 20), (8, 20), (12, 20), mirror=False)
# pierna izquierda
leg((20, 48), (24, 48), (24, 52), (20, 52), (16, 52), (28, 52), mirror=True)

out = sys.argv[1] if len(sys.argv) > 1 else "victorMC.png"
img.save(out)
print("skin guardada en", out)
