import build123d as bd

step = bd.import_step('./mxmecha_dummy_oneKey.step')

print(step.bounding_box())

bb = step.bounding_box()
zDiff = (bb.max.Z - bb.min.Z) / 2


step = step.translate(-bb.center()  + (0,0,zDiff))

print(step.bounding_box())

smallerStep = step.scale(0.8, about=(0,0,0))

my_solids = []
for f in step.faces():
    my_solids.append(bd.Solid.thicken(f, depth=-1.5))

x = bd.Compound(my_solids)

bd.export_step(x, "./shelled.step")
bd.export_stl(x, "./tryMe.stl")