caffe_root = '/home/hyshi/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np
import json
from numpy import matlib as mt

caffe.set_mode_gpu()
db_filename = '/mnt/sda/backup/match/database.json'
vectors = []


for line in open(db_filename):
  vector = json.loads(line)
  vectors.append(vector)
mat = np.matrix(vectors)
for idx in range(10000):
  delta = mt.repmat(mat[idx],10000,1) - mat

