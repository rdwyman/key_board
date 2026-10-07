import build123d as bd
import argparse
import stem_modeler

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


key_cap = stem_modeler.add_stem(
    key_cap,
    args.vertical_slot_width,
    args.vertical_slot_length,
    args.horizontal_slot_length,
    args.horizontal_slot_width,
    args.slot_depth,
    args.slot_fillet,
    args.stem_height,
    args.stem_diameter,
)


dots = []


def add_dot(x_address, y_address):
    z_sink = 0.0

    # TODO: Don't use a sphere, use the correct shape of a dot, respect the height
    x = args.dot_horizontal_spacing * x_address
    y = args.dot_vertical_spacing * y_address

    ray = bd.Axis((0, 0, 9999), (0, 0, -1))
    res = ray.intersect(key_cap)
    z = res.vertices()[0].Z - z_sink

    radius = args.dot_diameter / 2
    hgt = args.dot_height + z_sink
    scale = hgt / radius

    dot = bd.Sphere(radius=radius / 2)
    dot = dot.scale((1, 1, scale))

    dots.append(dot.translate((x, y, z)))


add_dot(0, 0)
add_dot(1, 1)
add_dot(1, 2)

key_cap = bd.Compound(children=[key_cap] + dots)


# export
bd.export_step(key_cap, f"{args.out}.step")
bd.export_stl(key_cap, f"{args.out}.stl")

print("done")
