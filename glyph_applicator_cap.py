from typing import TypedDict
import build123d as bd


class CapArgs(TypedDict):
    capShellFile: str
    capSolidFile: str
    keyCapThickness: float


def make_cap(args: CapArgs) -> bd.Compound:
    if "capShellFile" in args:
        capShellFile = args["capShellFile"]

        keyCapThickness = args.get("keyCapThickness", 2.5)

        baseShell = bd.import_step(capShellFile)

        # move base shell to origin above XY plane
        bb = baseShell.bounding_box()
        zDiff = (bb.max.Z - bb.min.Z) / 2
        baseShell = baseShell.translate(-bb.center() + (0, 0, zDiff))

        # thicken key cap shell into a solid
        solids = []
        overTrimmer = bd.Box(
            9999, 9999, 9999, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
        )
        for f in baseShell.faces():
            solids.append(bd.Solid.thicken(f, depth=-keyCapThickness) - overTrimmer)
    elif "capSolidFile" in args:
        # center the cap on origin
        cap = bd.import_step(args["capSolidFile"])
        bb = cap.bounding_box()
        cap = cap.translate(-bb.center())
        solids = cap.solids()
    else:
        raise Exception("Expected either a cap shell or a cap solid file")

    return bd.Compound(solids)
