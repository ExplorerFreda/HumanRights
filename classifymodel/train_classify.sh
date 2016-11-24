#!/usr/bin/env sh
set -e

TOOLS=/home/hyshi/caffe/build/tools

$TOOLS/caffe train --solver=classify_solver.prototxt \
-weights /mnt/sda/backup/classify/model_step1_iter_10000.caffemodel
# -weights /mnt/sda/backup/45degree/model/VGG_CNN_M.caffemodel

