import build123d as bd


def add_stem(
    key_cap: bd.Compound,
    vertical_slot_width: float,
    vertical_slot_length: float,
    horizontal_slot_length: float,
    horizontal_slot_width: float,
    slot_depth: float,
    slot_fillet: float,
    stem_height: float,
    stem_diameter: float,
):
    pass

    # build stem key
    al = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    vert = bd.Box(vertical_slot_width, vertical_slot_length, slot_depth, align=al)
    hori = bd.Box(
        horizontal_slot_length,
        horizontal_slot_width,
        slot_depth,
        align=al,
    )

    def make_fillet(quadrant: int):
        fillet_radius = slot_fillet
        isRightQuad = quadrant in (1, 4)
        isTopQuad = quadrant in (1, 2)
        x = (vertical_slot_width + fillet_radius) / 2.0 * (1 if isRightQuad else -1)
        y = (horizontal_slot_width + fillet_radius) / 2.0 * (1 if isTopQuad else -1)
        ang = 90 * (quadrant + 1)
        return (
            (
                bd.Box(fillet_radius, fillet_radius, slot_depth, align=al)
                - bd.Cylinder(fillet_radius, slot_depth, arc_size=90, align=al)
            )
            .rotate(bd.Axis.Z, ang)
            .translate((x, y, 0))
        )

    cross = vert + hori + (make_fillet(quad) for quad in (1, 2, 3, 4))

    # build stem
    ray = bd.Axis((0, 0, 9999), (0, 0, -1))
    res = ray.intersect(key_cap)
    cap_middle_z_distance = (res.vertices()[-1].Z + res.vertices()[0].Z) / 2
    total_height = stem_height + cap_middle_z_distance
    stem = bd.Cylinder(radius=stem_diameter / 2, height=total_height, align=al)
    stem = stem - cross
    stem = stem.translate((0, 0, cap_middle_z_distance - total_height))

    return bd.Compound(children=[key_cap, stem])
