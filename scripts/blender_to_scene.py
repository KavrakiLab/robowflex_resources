import bpy
from bpy.app.handlers import persistent
import subprocess
import sys
import os


@persistent
def load_handler(dummy):
    # Change working directory to script location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Get base name of .blend file
    filename = bpy.path.basename(bpy.context.blend_data.filepath)

    # Unselect all objects
    for ob in bpy.context.scene.objects:
        ob.select_set(False)

    scene = {'world': {'collision_objects': []}}
    for ob in bpy.context.scene.objects:
        if ob.type != 'MESH':
            continue

        # Select and export mesh as COLLADA file.
        ob.select_set(True)

        bpy.ops.object.transform_apply(location=True,
                                       rotation=True,
                                       scale=True)

        bpy.ops.wm.collada_export(
            filepath=os.path.abspath(f'../objects/{filename}/{ob.name}.dae'),
            selected=True)
        ob.select_set(False)

        scale = [1, 1, 1]
        position = list(ob.location)
        q = list(ob.rotation_quaternion)
        quaternion = q[1:] + q[:1]  # Rotate quaternion to XYZW order

        # Add object to scene.
        scene['world']['collision_objects'].append({
            'id':
            ob.data.name,
            'meshes': [{
                'resource':
                f'package://robowflex_resources/objects/{filename}/{ob.name}.dae',
                'dimensions': scale
            }],
            'mesh_poses': [{
                'position': position,
                'orientation': quaternion
            }]
        })

    output = dump(scene, Dumper=Dumper, default_flow_style=False)
    output_filename = os.path.abspath(f'../objects/{filename}/{filename}.yaml')
    with open(output_filename, 'w') as f:
        f.write(output)

    print(f"Wrote scene to {output_filename}")


def initialize_path():
    try:
        output = subprocess.check_output(
            ["python3", "-c", "import sys; print('\\n'.join(sys.path))"])
        paths = output.decode().strip().split('\n')

        for path in paths:
            if not path in sys.path:
                sys.path.append(path)

    except subprocess.CalledProcessError:
        print("Unable to call system Python3")
        return ""


# Initialize Python path with system Python
initialize_path()

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Install handler to run after loading .blend file
bpy.app.handlers.load_post.append(load_handler)
