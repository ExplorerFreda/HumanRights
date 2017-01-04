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
		cnt = 0
		for line in open(pyramid_filename):
			self.data.append(json.loads(line))
			cnt += 1
			if cnt > 10:
				break

