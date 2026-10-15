import argparse
import build123d as bd
import glyph_applicator_braille
import glyph_applicator_cap
import glyph_applicator_marking
import glyph_applicator_stem
import glyph_applicator_nub
import json
import textwrap
from typing import NotRequired, TypedDict
from jsonmerge import merge

parser = argparse.ArgumentParser(
    prog="key_board",
    description="Parameterized keycaps program",
    epilog="TODO: Add license?",
)

parser.add_argument("schemata", type=str, nargs="+")

parser.add_argument(
    "-o", "--out", help="Output file base name", default="./result", type=str
)
parser.add_argument(
    "-x",
    "--build-plate-x",
    help="Allowed width of a row of keys - should be less than the intended printer's build plate width",
    default=150,
    type=float,
)
cliArgs = parser.parse_args()


def applySchemata(target, schemata):
    """merges schemata together"""
    appendArraySchema = schema = {"properties": {"tags": {"mergeStrategy": "append"}}}
    for schema in schemata:
        print(schema)
        with open(schema) as f:
            overlay = json.load(f)
        if "overlays" in overlay:
            overlay = applySchemata(overlay, overlay["overlays"])
            overlay.pop("overlays", None)
        target = merge(target, overlay, appendArraySchema)
    return target


master = applySchemata({}, cliArgs.schemata)


class Key:
    keyCap: bd.Compound
    braille: bd.Compound
    nub: bd.Compound | None
    markings: bd.Compound
    stems: bd.Compound


keys: list[Key] = []


class Recipe(TypedDict):
    cap: NotRequired[glyph_applicator_cap.CapArgs]
    stems: NotRequired[list[glyph_applicator_stem.StemArgs]]
    braille: NotRequired[glyph_applicator_braille.BrailleArgs]
    nub: NotRequired[glyph_applicator_nub.NubArgs]
    markings: NotRequired[list[glyph_applicator_marking.MarkingArgs]]


class Node(TypedDict):
    data: float
    recipe: Recipe
    children: NotRequired[list["Node"]]


def actualize(data, recipe: Recipe):
    """builds and appends a new key to the keys array"""

    key = Key()

    if "cap" in recipe:
        key.keyCap = glyph_applicator_cap.make_cap(recipe["cap"])
    else:
        raise Exception("Cap should be available here")

    if "stems" in recipe:
        stemSolids = []
        for stem in recipe["stems"]:
            stemSolids.extend(glyph_applicator_stem.make_stem(key.keyCap, stem))
        key.stems = bd.Compound(stemSolids)
    else:
        key.stems = bd.Compound()

    if "braille" in recipe:
        key.braille = glyph_applicator_braille.make_cell(
            key.keyCap, data, recipe["braille"]
        )
    else:
        key.braille = bd.Compound()

    if "nub" in recipe:
        key.nub = glyph_applicator_nub.make_nub(key.keyCap, recipe["nub"])
    else:
        key.nub = bd.Compound()

    if "markings" in recipe:
        markingSolids = []
        for marking in recipe["markings"]:

            m = glyph_applicator_marking.make_marking(key.keyCap, data, marking)
            if m:
                markingSolids.extend(m)
                key.keyCap = key.keyCap - m
        key.markings = bd.Compound(markingSolids)
    else:
        key.markings = bd.Compound()

    keys.append(key)


def visit(node, currentData: dict, currentRecipe: Recipe, indent: int):
    """recursively visits and actualizes the keys described in a schema"""
    if "recipe" in node:
        currentRecipe = merge(currentRecipe, node["recipe"])

    if "data" in node:
        currentData = merge(currentData, node["data"])
    elif "recipe" not in node and "children" not in node:
        # short hand for leaf node
        currentData = merge(currentData, node)

    isLeaf = "children" not in node

    print(
        textwrap.indent(
            ("Actualizable" if isLeaf else "Recursable")
            + " data: "
            + json.dumps(currentData, indent="  "),
            "  " * indent,
        )
    )

    if isLeaf:
        actualize(currentData, currentRecipe)
    else:
        # recurse
        for child in node["children"]:
            visit(child, currentData, currentRecipe, indent + 2)


visit(master, {}, {}, 0)

primary: list[bd.Solid] = []
markings: list[bd.Solid] = []
braille: list[bd.Solid] = []
nubs: list[bd.Solid] = []

x = 0
y = 0
maxY = 0
spacing = 2

for key in keys:

    s = key.keyCap.bounding_box().size

    x = x + s.X + spacing
    maxY = max(s.Y + spacing, maxY)

    if x > cliArgs.build_plate_x:
        x = 0
        y = y + maxY
        maxY = 0

    primary.extend(key.keyCap.translate((x, y, 0.0)).solids())
    for stem in key.stems:
        primary.extend(stem.translate((x, y, 0.0)).solids())
    markings.extend(key.markings.translate((x, y, 0.0)).solids())
    braille.extend(key.braille.translate((x, y, 0.0)).solids())
    nubs.extend(key.nub.translate((x, y, 0.0)).solids())

primaryCompond = bd.Compound(primary, label="primary")
markingsCompond = bd.Compound(markings, label="markings")
brailleCompond = bd.Compound(braille, label="braille")
nubsCompond = bd.Compound(nubs, label="nubs")


keyBoard = bd.Compound(
    children=[primaryCompond, markingsCompond, brailleCompond, nubsCompond]
)

bd.export_step(keyBoard, "./resultBasicNOMARK.step")

print("done")
