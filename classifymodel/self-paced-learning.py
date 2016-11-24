caffe_root = '/home/hyshi/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np



new_train_filename = '/mnt/sda/backup/infolabel/pair_info/train_step2_a.info'

caffe.set_mode_gpu()
img_file = '/mnt/sda/backup/infolabel/train_label/%d.jpg'
model  = '/home/hyshi/exp/classifymodel/deploy.prototxt'
weights = '/mnt/sda/backup/classify/model_step1_iter_10000.caffemodel'
net = caffe.Classifier(model, weights)

transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
transformer.set_mean('data', np.load('/mnt/sda/backup/45degree/VGG_mean.npy'))
transformer.set_raw_scale('data', 1)


cnt = 0
fout = open(new_train_filename, 'w')
for idx in range(100,2352):
  input_image = caffe.io.load_image(img_file%idx)
  prediction = net.predict([input_image])[0]
  if max(prediction) > 0.7:
    print idx, prediction
    p = -1
    if prediction[0] > max(prediction) - 1e-5:
      p = 0
    else:
      p = 1
    fout.write(img_file%idx)
    fout.write(' ' + str(p) + '\n')
    cnt += 1
fout.close()
print cnt
