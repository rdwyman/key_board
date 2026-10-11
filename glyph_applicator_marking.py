import build123d as bd


def make_marking(
    keyCap: bd.Compound, text: str, fontFile: str, recess: float, extrusion: float
) -> bd.Compound:

    ray = bd.Axis((0, 0, 9999), (0, 0, -1))
    res = ray.intersect(keyCap)

    label = bd.Text(text, font_size=5, align=bd.Align.CENTER)

    textObj = [bd.Solid.extrude(f, (0, 0, 999)) for f in label.faces()]

    textObj = bd.Compound(textObj).intersect(keyCap)
    return bd.Compound(textObj)
