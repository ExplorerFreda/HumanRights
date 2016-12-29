caffe_root = '/home/hyshi/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np
import json



######### Config NetVLad Finetuned #############
model  = 'deploy.prototxt'
weights = '/mnt/sda/backup/match/netvlad_model_iter_20000.caffemodel'
db_filename = '/mnt/sda/backup/match/netvlad_vector.json'
######### Config NetVLad Finetuned #############

'''
######### Config VGG-CNN-M Model #############
model  = 'deploy.prototxt'
weights = '/mnt/sda/backup/45degree/model/VGG_CNN_M.caffemodel'
db_filename = '/mnt/sda/backup/match/netvlad_vgg-cnn-m_vector.json'
######### Config VGG-CNN-M Model #############
'''


def GetFileList(d):
	file_list = []
	if os.path.isfile(d):
		file_list.append(d)
	elif os.path.isdir(d):
		for f in os.listdir(d):
			new_dir = os.path.join(d,f)
			file_list.extend(GetFileList(new_dir))
	return file_list


def GenerateDatabaseSingle(db_filename, file_list):
	fout = open(db_filename, 'w')
	for idx, filename in enumerate(file_list):
		image = caffe.io.load_image(filename)
		net.blobs['data'].data[...] = transformer.preprocess('data', image)
		out = net.forward()
		vector = out['fc7'].copy()
		fout.write(json.dumps(vector.tolist()[0])+'\n')
		print 'Single Database', idx
	fout.close()


def GenerateDataBasePyramid(db_filename, file_list):
	fout = open(db_filename, 'w')
	for idx, filename in enumerate(file_list):
		image = caffe.io.load_image(filename)
		print type(image)
		vector = list()
		for subimage in subimages:
			net.blobs['data'].data[...] = transformer.preprocess('data', subimage)
			out = net.forward()
			vector.append(out['fc7'].copy().tolist()[0])
		fout.write(json.dumps(vector)+'\n')
		print 'Pyramid Database', idx, len(vector)
	fout.close()



file_list = GetFileList('/mnt/sda/backup/NetVLad/')

caffe.set_mode_gpu()
net = caffe.Net(model, weights, caffe.TEST)

transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
transformer.set_channel_swap('data', (2, 1, 0))
transformer.set_raw_scale('data', 255)
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.load('/mnt/sda/backup/45degree/VGG_mean.npy'))

GenerateDatabaseSingle(db_filename, file_list)

