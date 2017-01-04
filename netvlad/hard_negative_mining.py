#########################################################################
# File Name: hard_negative_mining.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-01-02 15:22:55
# Description: This script is used to mine hard-negative pairs after the first 
# 	time training.
#########################################################################

import json
import numpy as np
import random
import os

################## For Run #######################
netvlad_homefolder = '/mnt/sda/backup/NetVLad/'
input_filename = '/mnt/sda/backup/match/netvlad_vector.json'
list_filename = '/mnt/sda/backup/NetVLad/filelist.txt'
################## For Run #######################

################ For Debug #######################
# input_filename = '../vector.json'
# list_filename = '../list.json'
# output_filename_a = 'data/hard_negative_pair_a.txt'
# output_filename_p = 'data/hard_negative_pair_p.txt'
################ For Debug #######################

def SquareDist(v1, v2):
	return np.sum((v1-v2)**2)


def Dist(v1, v2):
	return np.sum((v1-v2)**2) ** 0.5


def GetBoundary(vectors):
	count = 0
	sum_dist = 0
	for i in range(10000):
		l = random.randint(0, len(vectors)-1)
		r = random.randint(0, len(vectors)-1)
		dist = Dist(vectors[l], vectors[r])
		sum_dist += dist
		count += 1
	return sum_dist / count


def GetPositivePairs(home_folder):
	positive_pairs = list()
	coordinate = dict()
	for folder in os.listdir(home_folder):
		folder = os.path.join(home_folder, folder)
		if not os.path.isdir(folder):
			continue
		for sub_folder in os.listdir(folder):
			sub_folder = os.path.join(folder, sub_folder)
			if not os.path.isdir(sub_folder):
				continue
			image_paths = list()
			for f in os.listdir(sub_folder):
				f = os.path.join(sub_folder, f)
				if f[-3:] == 'csv':
					coordinate[f[:-4]+'.png'] = [float(x) for x in open(f).readline().split(',')]
				else:
					image_paths.append(f)
			for i in range(0, len(image_paths)):
				positive_pairs.append([image_paths[i], image_paths[(i+1)%len(image_paths)]])
		print folder, len(positive_pairs)
	return [positive_pairs, coordinate]
	

def GetNegativePairs(file_list, vectors, coordinate, delta, max_number):
	epsilon = 0.002
	negative_pairs = list()
	while len(negative_pairs) < max_number:
		number_a = random.randint(0, len(file_list)-1)
		number_p = random.randint(0, len(file_list)-1)
		a = file_list[number_a]
		p = file_list[number_p]
		coordinate_a = np.array(coordinate[a][:2])
		coordinate_p = np.array(coordinate[p][:2])
		if Dist(coordinate_a, coordinate_p) > epsilon and Dist(vectors[number_a], vectors[number_p]) <= delta: 
			negative_pairs.append([a,p])
	return negative_pairs



def OutputPairs(filename_a, filename_p, validation_a, validation_p, positive, negative):
	pairs = positive
	pairs.extend(negative)
	random.shuffle(pairs)
	fout_a = open(filename_a, 'w')
	fout_p = open(filename_p, 'w')
	for pair in pairs[3000:]:
		a = pair[0]
		p = pair[1]
		if a[:-7] == p[:-7]: # positive
			fout_a.write(a + ' 1\n')
			fout_p.write(p + ' 1\n')
		else: # negative
			fout_a.write(a + ' 0\n')
			fout_p.write(p + ' 0\n')
	fout_a.close()
	fout_p.close()

	fout_a = open(validation_a, 'w')
	fout_p = open(validation_p, 'w')
	for pair in pairs[:3000]:
		a = pair[0]
		p = pair[1]
		if a[:-7] == p[:-7]: # positive
			fout_a.write(a + ' 1\n')
			fout_p.write(p + ' 1\n')
		else: # negative
			fout_a.write(a + ' 0\n')
			fout_p.write(p + ' 0\n')
	fout_a.close()
	fout_p.close()


files = list()
vectors = list()
for line in open(list_filename):
	files.append(line[:-1])
for line in open(input_filename):
	vector = json.loads(line)
	vectors.append(np.array(vector))
delta = GetBoundary(vectors)
print 'Delta is:', delta
[positive_pairs, coordinate] = GetPositivePairs(netvlad_homefolder)
negative_pairs = GetNegativePairs(files, vectors, coordinate, delta, len(positive_pairs) * 2)
OutputPairs('data/pair_new_a.txt', 'data/pair_new_p.txt', 'data/val_new_a.txt', 'data/val_new_p.txt', positive_pairs, negative_pairs)

