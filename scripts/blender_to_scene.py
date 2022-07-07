#!/usr/bin/env -S blender --background --python

import bpy
from bpy.app.handlers import persistent
import subprocess
import sys


def add_path(path):
    if not path in sys.path:
        sys.path.append(path)


def initialize_path():
    try:
        output = subprocess.check_output(
            ["python3", "-c", "import sys; print('\\n'.join(sys.path))"])
        paths = output.decode().strip().split('\n')

        for path in paths:
            add_path(path)

    except subprocess.CalledProcessError:
        print("Unable to call system Python3")
        return ""


@persistent
def load_handler(dummy):
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    scene = {'world': {'collision_objects': []}}

    for ob in bpy.context.scene.objects:
        ob.select_set(False)

    for ob in bpy.context.scene.objects:
        ob.select_set(True)
        bpy.ops.wm.collada_export(
            filepath=f'../objects/{filename}/{ob.data.name}.dae',
            selected=True)

        q = list(ob.matrix_world.to_quaternion())
        q = q[1:] + q[:1]  # Rotate quaternion to XYZW order
        scene['world']['collision_objects'].append({
            'id':
            ob.data.name,
            'meshes': [{
                'resource':
                f'package://robowflex_resources/objects/{filename}/{ob.data.name}.dae',
                'dimensions': list(ob.scale)
            }],
            'mesh_poses': [{
                'position': list(ob.matrix_world.to_translation()),
                'orientation': q
            }]
        })

        ob.select_set(False)

    output = dump(scene, Dumper=Dumper, default_flow_style=False)
    with open(f'../objects/{filename}/{filename}.yaml', 'w') as f:
        f.write(output)

    print(output)


initialize_path()
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

bpy.app.handlers.load_post.append(load_handler)
