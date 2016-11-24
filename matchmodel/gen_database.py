caffe_root = '/home/hyshi/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np
import json

caffe.set_mode_gpu()
img_file = '/mnt/sda/backup/streetview45/dbdata/%d.jpg'
model  = '/home/hyshi/exp/matchmodel/deploy.prototxt'
weights = '/mnt/sda/backup/match/model_iter_200000.caffemodel'
db_filename = '/mnt/sda/backup/match/database.json'
net = caffe.Net(model, weights, caffe.TEST)

transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
transformer.set_mean('data', np.load('/mnt/sda/backup/45degree/VGG_mean.npy'))
transformer.set_raw_scale('data', 1)
transformer.set_transpose('data',(2,0,1))


fout = open(db_filename, 'w')
for idx in range(10000):
  image = caffe.io.load_image(img_file%idx)
  net.blobs['data'].data[...] = transformer.preprocess('data', image)
  out = net.forward()
  vector = out['fc7'].copy()
  fout.write(json.dumps(vector.tolist()[0])+'\n')
  print idx
fout.close()
