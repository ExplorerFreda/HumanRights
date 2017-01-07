caffe_root = '/home/hyshi/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np
import json
import os

######### Config NetVLadQ Finetune-Model #############
model  = 'deploy.prototxt'
weights = '/mnt/sda/backup/match/models_save/netvlad-model_iter_100000.caffemodel'
db_filename = '/mnt/sda/backup/match/netvladQ_finetune_vector.json'
pyramid_db_filename = '/mnt/sda/backup/match/netvladQ_finetune_pyramid_vector.json'
######### Config NetVLad Finetune-Model #############

'''
######### Config NetVLad Finetune-Model #############
model  = 'deploy.prototxt'
weights = '/mnt/sda/backup/match/models_save/netvlad-model_iter_100000.caffemodel'
db_filename = '/mnt/sda/backup/match/netvlad_finetune_vector.json'
pyramid_db_filename = '/mnt/sda/backup/match/netvlad_finetune_pyramid_vector.json'
######### Config NetVLad Finetune-Model #############
'''

'''
######### Config NetVLadQ VGG-CNN-Model #############
model  = 'deploy.prototxt'
weights = '/mnt/sda/backup/45degree/model/VGG_CNN_M.caffemodel'
db_filename = '/mnt/sda/backup/match/netvladQ_vgg-cnn-m_vector.json'
pyramid_db_filename = '/mnt/sda/backup/match/netvladQ_vgg-cnn-m_pyramid_vector.json'
######### Config NetVLadQ VGG-CNN-Model #############
'''

'''
######### Config VGG-CNN-M Model #############
model  = 'deploy.prototxt'
weights = '/mnt/sda/backup/45degree/model/VGG_CNN_M.caffemodel'
db_filename = '/mnt/sda/backup/match/netvlad_vgg-cnn-m_vector.json'
pyramid_db_filename = '/mnt/sda/backup/match/netvlad_vgg-cnn-m_pyramid_vector.json'
######### Config VGG-CNN-M Model #############
'''

caffe.set_mode_gpu()
net = caffe.Net(model, weights, caffe.TEST)

transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
transformer.set_channel_swap('data', (2, 1, 0))
transformer.set_raw_scale('data', 255)
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.load('/mnt/sda/backup/45degree/VGG_mean.npy'))



def GetImageFileList(d):
	file_list = []
	if os.path.isfile(d) and (d[-3:] == 'png' or d[-3:] == 'jpg'):
		file_list.append(d)
	elif os.path.isdir(d):
		for f in os.listdir(d):
			new_dir = os.path.join(d,f)
			file_list.extend(GetImageFileList(new_dir))
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


def GenerateDatabasePyramid(db_filename, file_list):
	fout = open(db_filename, 'w')
	for idx, filename in enumerate(file_list):
		image = caffe.io.load_image(filename)
		vector = list()
		subimages = list()
		# generate subimages
		for l in range(1,4):
			length_x = len(image) / l
			length_y = len(image[0]) / l
			for i in range(0,len(image)-3,length_x):
				for j in range(0,len(image[0])-3,length_y):
					subimages.append(image[i:i+length_x,j:j+length_y].copy())
		for subimage in subimages:
			net.blobs['data'].data[...] = transformer.preprocess('data', subimage)
			out = net.forward()
			vector.append(out['fc7'].copy().tolist()[0])
		fout.write(json.dumps(vector)+'\n')
		print 'Pyramid Database', idx, len(vector)
	fout.close()


def OutputFileList(filelist, filename):
	fout = open(filename, 'w')
	for item in filelist:
		fout.write(item + '\n')
	fout.close()


file_list = GetImageFileList('/mnt/sda/backup/NetVLad_Q/')
print 'File List Size:', len(file_list)
GenerateDatabasePyramid(pyramid_db_filename, file_list)
GenerateDatabaseSingle(db_filename, file_list)
OutputFileList(file_list, '/mnt/sda/backup/NetVLad_Q/filelist.txt')
