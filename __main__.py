import build123d as bd
import argparse

parser = argparse.ArgumentParser(
    prog="key_board",
    description="Parameterized keycaps program",
    epilog="TODO: Add license?",
)

parser.add_argument(
    "-k",
    "--key-cap-thickness",
    help="Key cap thickness in mm.",
    default=2.5,
    type=float,
)
parser.add_argument(
    "-o", "--out", help="Output file base name", default="./result", type=str
)
parser.add_argument("--stem-diameter", dest="stem_diameter", default=6.0, type=float)
parser.add_argument(
    "--stem-height",
    help="Stem height measured as distance below bottom of key cap",
    dest="stem_height",
    default=4.0,
    type=float,
)

# see https://telcontar.net/KBK/Cherry/images/MX/Cherry_8_mm_mount.svgz
parser.add_argument("--vertical-slot-length", default=4.1, type=float)
parser.add_argument("--vertical-slot-width", default=1.17, type=float)
parser.add_argument("--horizontal-slot-length", default=4.1, type=float)
parser.add_argument("--horizontal-slot-width", default=1.17, type=float)
parser.add_argument("--slot-depth", default=6, type=float)
parser.add_argument("--slot-fillet", default=0.3, type=float)

# https://www.brailleauthority.org/size-and-spacing-braille-characters
parser.add_argument("--dot-diameter", default=1.44, type=float)
parser.add_argument("--dot-height", default=0.48, type=float)
parser.add_argument("--dot-horizontal-spacing", default=2.34, type=float)
parser.add_argument("--dot-vertical-spacing", default=2.34, type=float)

args = parser.parse_args()

base_shell = bd.import_step("./mxmecha_dummy_oneKey.step")

# move base shell to origin above XY plane
bb = base_shell.bounding_box()
zDiff = (bb.max.Z - bb.min.Z) / 2
base_shell = base_shell.translate(-bb.center() + (0, 0, zDiff))

# thicken key cap shell into a solid
solids = []
over_trimmer = bd.Box(
    9999, 9999, 9999, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
)
for f in base_shell.faces():
    solids.append(bd.Solid.thicken(f, depth=-args.key_cap_thickness) - over_trimmer)
key_cap = bd.Compound(solids)


# build stem key
al = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
vert = bd.Box(
    args.vertical_slot_width, args.vertical_slot_length, args.slot_depth, align=al
)
hori = bd.Box(
    args.horizontal_slot_length, args.horizontal_slot_width, args.slot_depth, align=al
)


def make_fillet(quadrant: int):
    fillet_radius = args.slot_fillet
    isRightQuad = quadrant in (1, 4)
    isTopQuad = quadrant in (1, 2)
    x = (args.vertical_slot_width + fillet_radius) / 2.0 * (1 if isRightQuad else -1)
    y = (args.horizontal_slot_width + fillet_radius) / 2.0 * (1 if isTopQuad else -1)
    ang = 90 * (quadrant + 1)
    return (
        (
            bd.Box(fillet_radius, fillet_radius, args.slot_depth, align=al)
            - bd.Cylinder(fillet_radius, args.slot_depth, arc_size=90, align=al)
        )
        .rotate(bd.Axis.Z, ang)
        .translate((x, y, 0))
    )


cross = vert + hori + (make_fillet(quad) for quad in (1, 2, 3, 4))

# build stem
ray = bd.Axis((0, 0, 9999), (0, 0, -1))
res = ray.intersect(key_cap)
cap_middle_z_distance = (res.vertices()[-1].Z + res.vertices()[0].Z) / 2
total_height = args.stem_height + cap_middle_z_distance
stem = bd.Cylinder(radius=args.stem_diameter / 2, height=total_height, align=al)
stem = stem - cross
stem = stem.translate((0, 0, cap_middle_z_distance - total_height))

dots = []


def add_dot(x_address, y_address):
    # TODO: Don't use a sphere, use the correct shape of a dot, respect the height
    x = args.dot_horizontal_spacing * x_address
    y = args.dot_vertical_spacing * y_address
    dots.append(bd.Sphere(radius=args.dot_diameter / 2).translate((x, y, 10)))


add_dot(0, 0)
add_dot(1, 1)
add_dot(1, 2)

key_cap = bd.Compound(children=[key_cap, stem] + dots)


# export
bd.export_step(key_cap, f"{args.out}.step")
bd.export_stl(key_cap, f"{args.out}.stl")


print("done")
