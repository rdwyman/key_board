import build123d as bd
from typing import NotRequired, TypedDict


class MarkingArgs(TypedDict):
    datum: str
    fontSize: float
    center: tuple[float, float]
    fontFile: NotRequired[str]
    recess: NotRequired[float]
    extrusion: NotRequired[float]


def make_marking(
    keyCap: bd.Compound, data: dict, args: MarkingArgs
) -> bd.Compound | None:

    datum = args.get("datum")
    fontSize = args.get("fontSize")
    center = args.get("center")
    fontFile = args.get("fontFile")
    recess = args.get("recess", 0)
    extrussion = args.get("extrussion", 0)

    # always extrude a hair to ensure correct boolean operations
    extrussion = extrussion + 0.005

    if datum in data:

        text = data[datum]

        bb = keyCap.bounding_box()
        if fontFile:
            fontFaces = bd.FontManager().register_font(fontFile)
            label = bd.Text(
                text, font_size=fontSize, align=bd.Align.CENTER, font=fontFaces[0]
            ).translate((center[0] * bb.size.X / 2, center[1] * bb.size.Y / 2, 0))
        else:
            label = bd.Text(
                text,
                font_size=fontSize,
                align=bd.Align.CENTER,
            ).translate((center[0] * bb.size.X / 2, center[1] * bb.size.Y / 2, 0))

        textObj = [bd.Solid.extrude(f, (0, 0, 50)) for f in label.faces()]

        textObj = bd.Compound(bd.Compound(textObj).intersect(keyCap))

        textObj = textObj.translate((0, 0, extrussion + recess))

        return textObj

    else:
        return None
