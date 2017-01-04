#########################################################################
# File Name: generate_tokyotimes_datapairs.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-01-04 11:44:45
# Description: This script is used to generate data pairs for training 
# 	and validation.
#########################################################################

import scipy.io as sio
import numpy as np
import random


class PairGenerator:

	def __init__(self, filename):
		self.filename = filename
		print self.filename
		data = sio.loadmat(self.filename)
		self.whichSet = data['dbStruct']['whichSet'][0][0]
		self.dbImageFns = data['dbStruct']['dbImageFns'][0][0]
		self.utmDb = data['dbStruct']['utmDb'][0][0]
		self.dbTimeStamp = data['dbStruct']['dbTimeStamp'][0][0]
		self.qImageFns = data['dbStruct']['qImageFns'][0][0]
		self.utmQ = data['dbStruct']['utmQ'][0][0]
		self.qTimeStamp = data['dbStruct']['qTimeStamp'][0][0]
		self.numImages = data['dbStruct']['numImages'][0][0]
		self.numQueries = data['dbStruct']['numQueries'][0][0]
		self.posDistThr = data['dbStruct']['posDistThr'][0][0]
		self.posDistSqThr = data['dbStruct']['posDistSqThr'][0][0]
		self.nonTrivPosDistSqThr = data['dbStruct']['nonTrivPosDistSqThr'][0][0]


	def DistSq(self, a, b):
		return np.sum((a - b) ** 2)


	def GeneratePairs(self):
		print 'Begin to generate pairs.'
		positive_pairs = list()
		negative_pairs = list()
		cnt = 0

		for qi in xrange(self.numQueries):
			print 'Query', qi, len(positive_pairs), len(negative_pairs)
			for di in xrange(self.numImages):
				dist = self.DistSq(
				np.array([self.utmDb[0][di], self.utmDb[1][di]]), 
				np.array([self.utmQ[0][qi], self.utmQ[1][qi]]))
				qFilename = self.qImageFns[qi][0][0]
				dbFilename = self.dbImageFns[di][0][0]
				qAngle = int(qFilename[qFilename.rfind('_')-3:qFilename.rfind('_')])
				dbAngle = int(dbFilename[dbFilename.rfind('_')-3:dbFilename.rfind('_')])
				if dist <= self.nonTrivPosDistSqThr and abs(dbAngle-qAngle) % 360 <= 30:
					positive_pairs.append([dbFilename, qFilename])
				elif dist > self.posDistSqThr and random.randint(0,1000) == 0:
					negative_pairs.append([dbFilename, qFilename])
		return [positive_pairs, negative_pairs]


	def OutputPairs(filename_a, filename_p, positive, negative):
		print filename_a, filename_p, len(positive) + len(negative)
		pairs = positive
		pairs.extend(negative)
		random.shuffle(pairs)
		fout_a = open(filename_a, 'w')
		fout_p = open(filename_p, 'w')
		for pair in pairs:
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



generator = PairGenerator('/mnt/sda/backup/TokyoTM/tokyoTimeMachine/tokyoTM_train.mat')
[positive, negative] = generator.GeneratePairs()
generator.OutputPairs('data/train_a.txt', 'data/train_p.txt', positive, negative)

generator = PairGenerator('/mnt/sda/backup/TokyoTM/tokyoTimeMachine/tokyoTM_val.mat')
[positive, negative] = generator.GeneratePairs()
generator.OutputPairs('data/val_a.txt', 'data/val_p.txt', positive, negative)



