from typing import TypedDict
import build123d as bd
from keycap_types import D1, D2, D3, D4, D5, D6, D7, D8


class BrailleApplicatorContext(TypedDict):
    datum: str
    encoding: str
    center: tuple[float, float]
    dotDiameter: float
    dotHeight: float
    dotHorizontalSpacing: float
    dotVerticalSpacing: float


def add_cell(
    key_cap: bd.Compound,
    dotHorizontalSpacing: float,
    center: tuple[float, float],
    dotVerticalSpacing: float,
    dotDiameter: float,
    dotHeight: float,
):

    brailleCode = D1 | D2 | D4 | D6

    z_sink = 0.0
    is_8_dot = False
    dot_objs = []

    def add_dot(x_translate: float, y_translate: float):

        if is_8_dot:
            y_translate = y_translate + 0.5

        x = dotHorizontalSpacing * x_translate + center[0]
        y = dotVerticalSpacing * y_translate + center[1]

        ray = bd.Axis((x, y, 99), (0, 0, -1))

        res = key_cap.intersect(ray)
        if not res:
            return

        z = res.vertices().sort_by(bd.Axis.Z).last.Z - z_sink

        radius = dotDiameter / 2
        hgt = dotHeight + z_sink
        scale = hgt / radius

        dot = bd.Sphere(radius=radius / 2)
        dot = dot.scale((1, 1, scale))

        dot_objs.append(dot.translate((x, y, z)))

    mod_8_dot = 0.5 if is_8_dot else 0

    dots = []
    if brailleCode & D1:
        add_dot(-0.5, 1.0 + mod_8_dot)
    if brailleCode & D2:
        add_dot(+0.5, 1.0 + mod_8_dot)
    if brailleCode & D3:
        add_dot(-0.5, 0.0 + mod_8_dot)
    if brailleCode & D4:
        add_dot(+0.5, 0.0 + mod_8_dot)
    if brailleCode & D5:
        add_dot(-0.5, -1.0 + mod_8_dot)
    if brailleCode & D6:
        add_dot(+0.5, -1.0 + mod_8_dot)
    if brailleCode & D7:
        add_dot(-0.5, -2.0 + mod_8_dot)
    if brailleCode & D8:
        add_dot(+0.5, -2.0 + mod_8_dot)

    key_cap = bd.Compound(children=[key_cap] + dot_objs)
    return key_cap
