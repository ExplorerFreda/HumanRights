#########################################################################
# File Name: pyramid_saliency_score_estimation.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-01-04 18:15:23
# Description: This script is used to estimate saliency score of each patch 
#	of image.
#########################################################################

import json
import numpy as np
import random


class SaliencyScoreEstimation:
	def __init__(self, filelist_filename, pyramid_filename):
		self.data = list()
		self.filelist = list()
		for line in open(filelist_filename):
			self.filelist.append(line[:-1])
		for line in open(pyramid_filename):
			self.data.append(json.loads(line))
			print 'load', len(self.data)
			if len(self.data) >= 3000:
				break
	
	def DistSq(self, a, b):
		return np.sum((a - b) ** 2)

	def EstimateScore(self):
		total_match_score = [[0 for y in range(len(self.data[0]))] 
			for x in range(len(self.data))]
		result = list()
		for i in xrange(len(self.data)):
			print i, '/', len(self.data)
			for j in xrange(len(self.data[0])):
				for k in xrange(100):
					p = random.randint(0, len(self.data)-1)
					if self.filelist[i][:-7] == self.filelist[p][:-7]:
						continue
					if j == 0: # discuss about the size
						q = 1
					elif j <= 4:
						q = random.randint(1,4)
					else:
						q = random.randint(5,13)
					total_match_score[i][j] += self.DistSq(
						np.array(self.data[i][j]), np.array(self.data[p][q])) ** 0.5
				total_match_score[i][j] /= 100
				result.append((i,j,total_match_score[i][j]))
		result = sorted(result, key = lambda x:x[2])
		fout = open('output.txt','w')
		for item in result:
			fout.write(json.dumps(item)+'\n')
		fout.close()



estimater = SaliencyScoreEstimation('../../data/filelist.txt', 
	'../../data/netvlad_vgg-cnn-m_pyramid_vector.json')
estimater.EstimateScore()
