#!/bin/bash
pushd "${0%/*}"
blender --python blender_to_scene.py --background $@
popd
