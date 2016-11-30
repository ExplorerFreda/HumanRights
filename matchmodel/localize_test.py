image_num = 1600
test_groundtruth_filename = '/mnt/sda/backup/data/test/groundtruth.txt'
db_filename = '/mnt/sda/backup/match/database.json'
test_filename = '/mnt/sda/backup/match/testvector.json'
threshold = 3 # threshold for location matching
caffe_root = '/home/hyshi/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np
import json
from numpy import matlib as mt

###
# Result: 
#   fine-tuned: 
#   original:  452/1600 = 0.2825
###



def CalcDist(x):
  return np.sum(np.array(x)**2)


vectors = []
fin = open(db_filename)
for line in fin:
  vector = json.loads(line)
  vectors.append(vector)
mat = np.matrix(vectors)
fin.close()


def location(idx):
  return [(idx/4)/int(image_num**0.5/2), (idx/4)%int(image_num**0.5/2)]

correct_match = 0
idx = 0
fin = open(test_filename)
for line in open(test_groundtruth_filename):
  location_groundtruth = int(line.split('\t')[1])
  vec = json.loads(fin.readline())
  delta = mt.repmat(vec, image_num, 1) - mat
  dist_info = map(CalcDist, delta)
  dist_info = [(dist_info[i], i) for i in range(image_num)]
  dist_info = sorted(dist_info, key=lambda x:x[0])
  loc_idx = location(idx)
  for item in dist_info[1:6]:
    loc_idy = location(item[1])
    d = max(abs(loc_idx[0] - loc_idy[0]),abs(loc_idx[1] - loc_idy[1])) 
    if d < threshold:
      correct_match += 1
  print correct_match, idx + 1, float(correct_match) / (idx + 1)
  idx += 1
print correct_match
fin.close()
