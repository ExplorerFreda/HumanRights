caffe_root = '/home/hyshi/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np

caffe.set_mode_gpu()
img_file = '/mnt/sda/backup/data/salient_database/%d.jpg'
model  = '/home/hyshi/jointmodel/classifymodel/deploy.prototxt'
weights = '/mnt/sda/backup/classify/model_iter_400.caffemodel'
net = caffe.Net(model, weights, caffe.TEST)

transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
transformer.set_channel_swap('data', (2, 1, 0))
transformer.set_raw_scale('data', 255)
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.load('/mnt/sda/backup/45degree/VGG_mean.npy'))


cnt = 0
fin = open('/mnt/sda/backup/data/salient_database/val.txt')
for idx in range(116):
  input_image = caffe.io.load_image(img_file%idx)
  net.blobs['data'].data[...] = transformer.preprocess('data', input_image)
###  print net.blobs['data'].data[...]
  out = net.forward()
  prediction = out['prob']
  ground_truth = float(fin.readline().split()[1])
  if ground_truth == 1.0:
    cnt += 1
  print prediction, ground_truth
print cnt
