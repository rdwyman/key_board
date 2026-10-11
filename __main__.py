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

parser.add_argument(
    "-o", "--out", help="Output file base name", default="./result", type=str
)

# TODO: Get from command line
# TODO: Deep merge multiple JSON documents on top of each other
with open("./mxMechanical.json") as f:
    args = json.load(f)


class KeyParts:
    keyCap: bd.Compound
    braille: bd.Compound
    nub: bd.Compound
    markings: bd.Compound
    stems: bd.Compound


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

    keyParts = KeyParts()

    if "cap" in recipe:
        keyParts.keyCap = glyph_applicator_cap.make_cap(recipe["cap"])
    else:
        raise Exception("Cap should be available here")

    if "stems" in recipe:
        stemSolids = []
        for stem in recipe["stems"]:
            stemSolids.extend(glyph_applicator_stem.make_stem(keyParts.keyCap, stem))
        keyParts.stems = bd.Compound(stemSolids)

    if "braille" in recipe:
        keyParts.braille = glyph_applicator_braille.make_cell(
            keyParts.keyCap, data, recipe["braille"]
        )

    if "nub" in recipe:
        keyParts.nub = glyph_applicator_nub.make_nub(keyParts.keyCap, recipe["nub"])

    if "markings" in recipe:
        markingSolids = []
        for marking in recipe["markings"]:
            markingSolids.extend(
                glyph_applicator_marking.make_marking(keyParts.keyCap, data, marking)
            )
        keyParts.markings = bd.Compound(markingSolids)


def visit(node, currentData: dict, currentRecipe: Recipe, indent: int):
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


visit(args, {}, {}, 0)


bd.export_step(part, f"{args.out}.step")

print("done")
