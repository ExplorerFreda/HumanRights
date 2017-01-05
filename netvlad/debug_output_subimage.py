import caffe
import json
import cv
import cv2
import numpy as np
from scipy import misc
from PIL import Image


def OutputDatabasePyramid(file_list):
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
		for idsub, subimage in enumerate(subimages):
			subimage = np.array(subimage.tolist())
			misc.imsave('data/%d_%d.png'%(idx,idsub), subimage)


file_list = [x[:-1] for x in open('/mnt/sda/backup/NetVLad/filelist.txt').readlines()]
OutputDatabasePyramid(file_list[:10])
