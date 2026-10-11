import build123d as bd
from typing import NotRequired, TypedDict


class MarkingArgs(TypedDict):
    datum: str
    extent: tuple[float, float, float, float]
    fontFile: NotRequired[str]
    recess: NotRequired[float]
    extrusion: NotRequired[float]


def make_marking(keyCap: bd.Compound, data: dict, args: MarkingArgs) -> bd.Compound:

    datum = args.get("datum")
    extent = args.get("extent")
    fontFile = args.get("fontFile")
    recess = args.get("recess")
    extrussion = args.get("extrusion")

    if datum in data:

        text = data[datum]

        ray = bd.Axis((0, 0, 9999), (0, 0, -1))
        res = ray.intersect(keyCap)

        label = bd.Text(text, font_size=5, align=bd.Align.CENTER)

        textObj = [bd.Solid.extrude(f, (0, 0, 999)) for f in label.faces()]

        textObj = bd.Compound(textObj).intersect(keyCap)
        return bd.Compound(textObj)

    else:
        return bd.Compound()
