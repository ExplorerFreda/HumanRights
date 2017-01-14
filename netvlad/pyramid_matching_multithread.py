#########################################################################
# File Name: match_with_saliency.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-01-06 05:43:59
# Description: This script is used to compute match score for queries.
#########################################################################

import time
import threading
import json
import numpy as np


class SingleMatcher:
	def __init__(self, database_filename, querybase_filename):
		self.database = list()
		self.querybase = list()
		for line in open(database_filename):
			self.database.append(json.loads(line))
			print len(self.database)
		for line in open(querybase_filename):
			self.querybase.append(json.loads(line))

	def DistSq(self, a, b):
		return np.sum((np.array(a) -np.array(b)) ** 2)

	def match_score(self, qitem, ditem):
		return self.DistSq(qitem,ditem) ** 0.5

	def Retrieval(self, save_filename):
		ret = list()
		for qid, item in enumerate(self.querybase):
			print 'query', qid
			match_queue = list()
			for did, ditem in enumerate(self.database):
				if did % 1000 == 0:
					print did
				match_queue.append([did, self.match_score(item, ditem)])
			match_queue = sorted(match_queue, key = lambda x:x[1])
			ret.append(match_queue[:25])
		fout = open(save_filename, 'w')
		fout.write(json.dumps(ret) + '\n')
		fout.close()


class MyThread:
	def __init__(self):
		self._result = None
	
	def run(self, func, *args):
		result = func(args[0], args[1])
		self._result = result

	def get_result(self):
		return self._result


class PyramidMatcher:
	def __init__(self, database_filename, querybase_filename, l, r):
		self.database = list()
		self.querybase = list()
		cnt = 0
		for line in open(database_filename):
			if l <= cnt < r:
				self.database.append(json.loads(line))
				print 'database', len(self.database)
			cnt += 1
			if cnt > 10:
				break
		for line in open(querybase_filename):
			self.querybase.append(json.loads(line))
			print 'querybase', len(self.querybase)
			if (len(self.querybase)>10):
				break

	def DistSq(self, a, b):
		return np.sum((np.array(a) -np.array(b)) ** 2)

	def match_score(self, qitem, ditem):
		ret = 0
		# layer 1
		ret += self.DistSq(qitem[0],ditem[0]) ** 0.5
		# layer 2
		for i in range(1,5):
			score = 1e10
			for j in range(1,5):
				score = min(score,self.DistSq(qitem[i], ditem[j]) ** 0.5)
			ret += score / 4
		# layer 3
		for i in range(5,14):
			for j in range(5,14):
				score = min(score, self.DistSq(qitem[i], ditem[j]) ** 0.5)
			ret += score / 9
		return ret

	def compute_match_score(self, qid, item):
		match_queue = list()
		for did, ditem in enumerate(self.database):
			if did % 10 == 0:
				print qid, did
			match_queue.append([did, self.match_score(item, ditem)])
		match_queue = sorted(match_queue, key = lambda x:x[1])
		print qid
		return match_queue[:25]


	def Retrieval(self, save_filename):
		ret = list()
		for qid, item in enumerate(self.querybase):
			print 'query', qid
			task = MyThread()
			thread = threading.Thread(target = task.run, args = (
				self.compute_match_score, qid, item))
			thread.start()
			ret.append(task.get_result())
		fout = open(save_filename, 'w')
		fout.write(json.dumps(ret) + '\n')
		fout.close()


#single_matcher = SingleMatcher('../../data/netvlad_vgg-cnn-m_vector.json', 
#	'../../data/netvladQ_vgg-cnn-m_vector.json')
#single_matcher.Retrieval('../../data/netvlad_single_vgg-cnn-m_matchresult.json')

pyramid_matcher = PyramidMatcher('../../data/netvlad_vgg-cnn-m_pyramid_vector.json', 
	'../../data/netvladQ_vgg-cnn-m_pyramid_vector.json', 0, 40000)
pyramid_matcher.Retrieval('../../data/netvlad_pyramid_vgg-cnn-m_matchresult_part0.json')

#pyramid_matcher = PyramidMatcher('../../data/netvlad_vgg-cnn-m_pyramid_vector.json', 
#	'../../data/netvladQ_vgg-cnn-m_pyramid_vector.json', 40000, 80000)
#pyramid_matcher.Retrieval('../../data/netvlad_pyramid_vgg-cnn-m_matchresult_part1.json')

#single_matcher = SingleMatcher('../../data/netvlad_finetune_vector.json', 
#	'../../data/netvladQ_finetune_vector.json')
#single_matcher.Retrieval('../../data/netvlad_single_finetune_matchresult.json')

#pyramid_matcher = PyramidMatcher('../../data/netvlad_finetune_pyramid_vector.json', 
#	'../../data/netvladQ_finetune_pyramid_vector.json')
#pyramid_matcher.Retrieval('../../data/netvlad_pyramid_finetune_matchresult.json')




