import build123d as bd

step = bd.import_step('./mxmecha_dummy_oneKey.step')

print(step.bounding_box())

bb = step.bounding_box()
zDiff = (bb.max.Z - bb.min.Z) / 2


step = step.translate(-bb.center()  + (0,0,zDiff))

print(step.bounding_box())

smallerStep = step.scale(0.8, about=(0,0,0))


comp = bd.Compound([smallerStep] + [step])

bd.export_step(comp, "./shelled.step")