#!/bin/bash

rosrun xacro xacro `rospack find robowflex_resources`/stretch/urdf/stretch_description.xacro use_nominal_extrinsics:=true > `rospack find robowflex_resources`/stretch/urdf/stretch_uncalibrated.urdf

cp `rospack find robowflex_resources`/stretch/urdf/stretch_uncalibrated.urdf `rospack find robowflex_resources`/stretch/urdf/stretch.urdf
