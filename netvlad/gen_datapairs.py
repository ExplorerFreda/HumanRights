#########################################################################
# File Name: gen_datapairs.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2016-12-28 02:20:24
# Description: This script is used to generate netvlad data pairs.
#########################################################################

import os
import random


def GetFileList(d):
	file_list = []
	if os.path.isfile(d):
		file_list.append(d)
	elif os.path.isdir(d):
		for f in os.listdir(d):
			new_dir = os.path.join(d,f)
			file_list.extend(GetFileList(new_dir))
	return file_list


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
				

def Dist(a, p):
	return ((a[0] - p[0]) ** 2 + (a[1] - p[1]) ** 2) ** 0.5



def GetNegativePairs(coordinate, max_number):
	epsilon = 0.002
	negative_pairs = list()
	file_list = coordinate.keys()
	while len(negative_pairs) < max_number:
		a = file_list[random.randint(0, len(file_list)-1)]
		p = file_list[random.randint(0, len(file_list)-1)]
		coordinate_a = coordinate[a][:2]
		coordinate_p = coordinate[p][:2]
		if Dist(coordinate_a, coordinate_p) > epsilon:
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


netvlad_homefolder = '/mnt/sda/backup/NetVLad/'
[positive_pairs, coordinate] = GetPositivePairs(netvlad_homefolder)
negative_pairs = GetNegativePairs(coordinate, len(positive_pairs) * 2)
OutputPairs('data/pair_a.txt', 'data/pair_p.txt', 'data/val_a.txt', 'val_p.txt', positive_pairs, negative_pairs)


# ============== For Debug ================
#d = 'd:\\HumanRightsData'
# [positive_pairs, coordinate] = GetPositivePairs(d)
# negative_pairs = GetNegativePairs(coordinate, len(positive_pairs) * 2)
# OutputPairs('data/pair_a.txt', 'data/pair_p.txt', positive_pairs, negative_pairs)

# d = '/mnt/d/Project/CMU/samples/server_files/'
# [positive_pairs, coordinate] = GetPositivePairs(d)
# OutputPairs('data/pair_a.txt', 'data/pair_p.txt', positive_pairs, [])
# print len(positive_pairs), len(coordinate)
# print os.listdir(d)
# print GetFileList(d)
