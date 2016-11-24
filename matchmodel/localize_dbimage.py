image_num = 10000
caffe_root = '/home/hyshi/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np
import json
from numpy import matlib as mt

caffe.set_mode_gpu()
db_filename = '/mnt/sda/backup/match/database.json'
dist_filename = '/mnt/sda/backup/match/dist.json'
vectors = []

fout = open(dist_filename, 'w')

def CalcDist(x):
  return np.sum(np.array(x)**2)



for line in open(db_filename):
  vector = json.loads(line)
  vectors.append(vector)
mat = np.matrix(vectors)
for idx in range(image_num):
  delta = mt.repmat(mat[idx], image_num, 1) - mat
  dist_vector = map(CalcDist, delta)
  fout.write(json.dumps(dist_vector) + '\n')
  print idx

fout.close()
