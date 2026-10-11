import build123d as bd
from typing import NotRequired, TypedDict


class StemArgs(TypedDict):
    center: NotRequired[tuple[float, float]]
    verticalSlotLength: NotRequired[float]
    verticalSlotWidth: NotRequired[float]
    horizontalSlotLength: NotRequired[float]
    horizontalSlotWidth: NotRequired[float]
    slotDepth: NotRequired[float]
    slotFillet: NotRequired[float]
    stemHeight: NotRequired[float]
    stemDiameter: NotRequired[float]


def make_stem(keyCap: bd.Compound, args: StemArgs) -> bd.Compound:

    # defaults from https://telcontar.net/KBK/Cherry/images/MX/Cherry_8_mm_mount.svgz

    center = args.get("center", (0, 0))
    verticalSlotLength = args.get("verticalSlotLength", 4.1)
    verticalSlotWidth = args.get("verticalSlotWidth", 1.17)
    horizontalSlotLength = args.get("horizontalSlotLength", 4.1)
    horizontalSlotWidth = args.get("horizontalSlotWidth", 1.17)
    slotDepth = args.get("slotDepth", 6)
    slotFillet = args.get("slotFillet", 0.3)
    stemHeight = args.get("stemHeight", 4.0)
    stemDiameter = args.get("stemDiameter", 6.0)

    # build stem key
    al = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    vert = bd.Box(verticalSlotWidth, verticalSlotLength, slotDepth, align=al)
    hori = bd.Box(
        horizontalSlotLength,
        horizontalSlotWidth,
        slotDepth,
        align=al,
    )

    def make_fillet(quadrant: int):
        fillet_radius = slotFillet
        isRightQuad = quadrant in (1, 4)
        isTopQuad = quadrant in (1, 2)
        x = (verticalSlotWidth + fillet_radius) / 2.0 * (1 if isRightQuad else -1)
        y = (horizontalSlotWidth + fillet_radius) / 2.0 * (1 if isTopQuad else -1)
        ang = 90 * (quadrant + 1)
        return (
            (
                bd.Box(fillet_radius, fillet_radius, slotDepth, align=al)
                - bd.Cylinder(fillet_radius, slotDepth, arc_size=90, align=al)
            )
            .rotate(bd.Axis.Z, ang)
            .translate((x, y, 0))
        )

    cross = vert + hori + (make_fillet(quad) for quad in (1, 2, 3, 4))

    # build stem
    ray = bd.Axis((0, 0, 9999), (0, 0, -1))
    res = ray.intersect(keyCap)
    cap_middle_z_distance = (res.vertices()[-1].Z + res.vertices()[0].Z) / 2
    total_height = stemHeight + cap_middle_z_distance
    stem = bd.Cylinder(radius=stemDiameter / 2, height=total_height, align=al)
    stem = stem - cross
    stem = stem.translate((0, 0, cap_middle_z_distance - total_height))

    return stem
