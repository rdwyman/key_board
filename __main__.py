import build123d as bd
import glyph_applicator_braille
import glyph_applicator_marking
import glyph_applicator_stem
import json
import textwrap
from typing import NotRequired, TypedDict
from jsonmerge import merge

with open("./mxMechanical.json") as f:
    args = json.load(f)

# parser = argparse.ArgumentParser(
#     prog="key_board",
#     description="Parameterized keycaps program",
#     epilog="TODO: Add license?",
# )

# parser.add_argument(
#     "-k",
#     "--key-cap-thickness",
#     help="Key cap thickness in mm.",
#     default=2.5,
#     type=float,
# )
# parser.add_argument(
#     "-o", "--out", help="Output file base name", default="./result", type=str
# )
# parser.add_argument("--stem-diameter", dest="stem_diameter", default=6.0, type=float)
# parser.add_argument(
#     "--stem-height",
#     help="Stem height measured as distance below bottom of key cap",
#     dest="stem_height",
#     default=4.0,
#     type=float,
# )

# # see https://telcontar.net/KBK/Cherry/images/MX/Cherry_8_mm_mount.svgz
# parser.add_argument("--vertical-slot-length", default=4.1, type=float)
# parser.add_argument("--vertical-slot-width", default=1.17, type=float)
# parser.add_argument("--horizontal-slot-length", default=4.1, type=float)
# parser.add_argument("--horizontal-slot-width", default=1.17, type=float)
# parser.add_argument("--slot-depth", default=6, type=float)
# parser.add_argument("--slot-fillet", default=0.3, type=float)

# # https://www.brailleauthority.org/size-and-spacing-braille-characters
# parser.add_argument("--dot-diameter", default=1.44, type=float)
# parser.add_argument("--dot-height", default=0.48, type=float)
# parser.add_argument("--dot-horizontal-spacing", default=2.34, type=float)
# parser.add_argument("--dot-vertical-spacing", default=2.34, type=float)
#
# args = parser.parse_args()


class KeyParts:
    keyCap: bd.Compound
    braille: bd.Compound
    markings: bd.Compound
    stem: bd.Compound


class Recipe(TypedDict):
    pass
    # cap: NotRequired[CapArgs]
    # stem: NotRequired[StemArgs]
    # braille: NotRequired[list[BrailleArgs]]
    # nub: NotRequired[NubArgs]
    # markings: NotRequired[list[MarkingArgs]]


class Node(TypedDict):
    data: float
    recipe: Recipe
    children: NotRequired[list["Node"]]


def visit(node, currentData: dict, currentRecipe: Recipe, indent: int):
    if "recipe" in node:
        currentRecipe = merge(currentRecipe, node["recipe"])

    if "data" in node:
        currentData = merge(currentData, node["data"])
    elif "recipe" not in node and "children" not in node:
        # short hand for leaf node
        currentData = merge(currentData, node)

    is_leaf = "children" not in node

    print(
        textwrap.indent(
            ("Actualizable" if is_leaf else "Recursable")
            + " data: "
            + json.dumps(currentData, indent="  "),
            "  " * indent,
        )
    )

    if is_leaf:
        # actualize
        a = 3
    else:
        # recurse
        for child in node["children"]:
            visit(child, currentData, currentRecipe, indent + 2)


visit(args, {}, {}, 0)


keyParts = KeyParts()


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
keyParts.keyCap = bd.Compound(solids)


keyParts.stem = glyph_applicator_stem.make_stem(
    keyParts.keyCap,
    args.vertical_slot_width,
    args.vertical_slot_length,
    args.horizontal_slot_length,
    args.horizontal_slot_width,
    args.slot_depth,
    args.slot_fillet,
    args.stem_height,
    args.stem_diameter,
)

keyParts.braille = glyph_applicator_braille.make_cell(
    keyParts.keyCap,
    args.dot_horizontal_spacing,
    (0, 0),
    args.dot_vertical_spacing,
    args.dot_diameter,
    args.dot_height,
)


keyParts.markings = glyph_applicator_marking.make_marking(keyParts.keyCap, "R", "asdf")

cap = keyParts.keyCap
print(cap)
cap = bd.Compound(cap.solids())

cap = cap - keyParts.braille - keyParts.markings


part = bd.Compound(children=[cap, keyParts.markings, keyParts.braille, keyParts.stem])


bd.export_step(part, f"{args.out}.step")

print("done")
