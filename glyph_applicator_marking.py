import build123d as bd


def make_marking(keyCap: bd.Compound, text: str, fontFile) -> bd.Compound:

    label = bd.Text(text, font_size=5, align=bd.Align.CENTER)

    textObj = [bd.Solid.extrude(f, (0, 0, 999)) for f in label.faces()]

    textObj = bd.Compound(textObj).intersect(keyCap)
    return bd.Compound(textObj)
