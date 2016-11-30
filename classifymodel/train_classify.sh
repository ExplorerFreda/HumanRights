#!/usr/bin/env sh
set -e

TOOLS=/home/hyshi/caffe/build/tools

$TOOLS/caffe train --solver=classify_solver.prototxt \
-weights /mnt/sda/backup/45degree/model/VGG_CNN_M.caffemodel

