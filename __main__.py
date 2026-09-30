import build123d as bd
import argparse

parser = argparse.ArgumentParser(
                    prog='key_board',
                    description='Parameterized keycaps program',
                    epilog='TODO: Add license?')

parser.add_argument('-w', '--wall', help='Wall thickness in mm. Large values violating topology constraints will fail', default=2.5, type=float)
parser.add_argument('-o', '--out', help='Output file base name', default='./result', type=str)
parser.add_argument('--stem-radius', dest='stem_radius', default=4.0, type=float)
parser.add_argument('--stem-height', dest='stem_height', default=10.0, type=float)

args = parser.parse_args()

base_shell = bd.import_step('./mxmecha_dummy_oneKey.step')

# move base shell to origin above XY plane
bb = base_shell.bounding_box()
zDiff = (bb.max.Z - bb.min.Z) / 2
base_shell = base_shell.translate(-bb.center()  + (0,0,zDiff))

# thicken key cap shell into a solid
solids = []
for f in base_shell.faces():
    solids.append(bd.Solid.thicken(f, depth=-args.wall))
key_cap = bd.Compound(solids)

# add stem
ray = bd.Axis((0,0,999),(0,0,-1))
res = ray.intersect(key_cap)
top_z = res.vertices()[-1].Z

b = bd.Cylinder(radius=args.stem_radius, height=args.stem_height)
translation_z = top_z - args.stem_height / 2
b.translate((0,0,-translation_z))
print(top_z)

asdf = bd.Compound(children=[key_cap, b])

# export
bd.export_step(asdf, f'{args.out}.step')
bd.export_stl(asdf, f'{args.out}.stl')

print('done')