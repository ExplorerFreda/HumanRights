#########################################################################
# File Name: compute_MAP.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-01-15 23:32:25
# Description: This script is used to compute MAP for NetVLAD dataset.
#########################################################################


import json
import numpy as np

result_filename = '../../data/netvlad_pyramid_finetune_matchresult.json'
filelist = '../../data/filelist.txt'
filelist_Q = '../../data/filelist_Q.txt'

posDistSqThr = 625


def location(filename):
	filename = filename[:filename.rfind('/')]
	location = filename[filename.rfind('/')+1:].split('_')
	return [float(location[0]),float(location[1])]


def get_location(filename):
	ret = []
	for line in open(filename):
		name = line[line.rfind('/')+1:].strip()
		name = name.replace('jpg','csv')
		location = open('../../data/geo-location/'+name).readline().split(',')
		location = [float(location[-2]), float(location[-1])]
		ret.append(location)
	return ret


def distsq(a, b):
	return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


db_loc = map(location, open(filelist).readlines())
q_loc = get_location(filelist_Q)
match_result = json.loads(open(result_filename).readline())

delta = 15
matched = 0
total = 0
matchset = set()
for i, item in enumerate(match_result):
	mini = 1e20
	geoq = q_loc[i]
	for item2 in db_loc:
		mini = min(mini, distsq(geoq,item2))
	if mini > posDistSqThr:
		continue
	total += 1
	matchset.add(i)


#for delta in [1, 2, 3, 4, 5, 10, 15, 20, 25]:
for delta in [25]:
	MAP_final = 0
	total_final = 0
	for i, item in enumerate(match_result):
		print i, len(match_result)
		if i not in matchset:
			continue
		geoq = q_loc[i]
		total = 0
		precision = 0
		matched = 0
		for subitem in item[:delta]:
			geodb = db_loc[subitem[0]]
			if distsq(geoq, geodb) < posDistSqThr:
				matched = 1
			total += 1
			if matched == 1:
				precision += float(matched) / total
				break
		if precision > 0:
			MAP_final += precision
			total_final += 1
	MAP_final /= total_final
	print result_filename, delta, MAP_final, total_final


