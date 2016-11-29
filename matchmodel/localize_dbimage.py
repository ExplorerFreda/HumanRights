image_num = 10000
delta = 3 # threshold for location matching
caffe_root = '/home/hyshi/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np
import json
from numpy import matlib as mt

###
# Result: 
#   fine-tuned: 4258
#   original: 4253
###

caffe.set_mode_gpu()
db_filename = '/mnt/sda/backup/match/database.json'
dist_filename = '/mnt/sda/backup/match/dist.json'
vectors = []


def CalcDist(x):
  return np.sum(np.array(x)**2)

'''
fout = open(dist_filename, 'w')
fin = open(db_filename)
for line in fin:
  vector = json.loads(line)
  vectors.append(vector)
mat = np.matrix(vectors)
for idx in range(image_num):
  delta = mt.repmat(mat[idx], image_num, 1) - mat
  dist_vector = map(CalcDist, delta)
  fout.write(json.dumps(dist_vector) + '\n')
  print idx
fin.close()
fout.close()
'''

def location(idx):
  return ((idx/4)/int(image_num**0.5/2), (idx/4)%int(image_num**0.5/2))

correct_match = 0

fin = open(dist_filename)
for idx in range(image_num):
  line = fin.readline()
  dist_info = json.loads(line)
  dist_info = [(dist_info[i], i) for i in range(image_num)]
  dist_info = sorted(dist_info, key=lambda x:x[0])
  loc_idx = location(idx)
  for item in dist_info[1:6]:
    loc_idy = location(item[1])
    if max(abs(loc_idx[0] - loc_idy[0]),abs(loc_idx[1] - loc_idy[1])) < delta:
      correct_match += 1
  print correct_match, idx + 1, float(correct_match) / (idx + 1)
print correct_match
fin.close()
