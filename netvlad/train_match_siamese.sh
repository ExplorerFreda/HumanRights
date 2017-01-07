#!/usr/bin/env sh
set -e

TOOLS=/home/hyshi/caffe/build/tools

$TOOLS/caffe train --solver=match_siamese_solver.prototxt \
--weights=/mnt/sda/backup/45degree/model/VGG_CNN_M.caffemodel

#--weights=/mnt/sda/backup/match/netvlad-7_model_iter_100000.caffemodel
#--snapshot=/mnt/sda/backup/match/model_iter_200000.solverstate

