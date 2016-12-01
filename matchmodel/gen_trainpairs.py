import random

threshold = 3
db_dir = '/mnt/sda/backup/data/database/'
data_dir = '/mnt/sda/backup/data/train/'
groundtruth = '/mnt/sda/backup/data/train/groundtruth.txt'
#groundtruth = '/mnt/sda/backup/data/train/val.txt'
pair_a_file = data_dir + 'pair_groundtruth_a.txt'
pair_p_file = data_dir + 'pair_groundtruth_p.txt'
#pair_a_file = data_dir + 'pair_val_a.txt'
#pair_p_file = data_dir + 'pair_val_p.txt'

grndtruth_dict = dict()
maxi = -1e10
mini = 1e10
for line in open(groundtruth):
	[idx, grd] = line.split('\t')
	idx = int(idx)
	grd = int(grd)
	grndtruth_dict[idx] = grd
	maxi = max(maxi, grd)
	mini = min(mini, grd)

image_num = 1600
def location(idx):
  return [(idx/4)/int(image_num**0.5/2), (idx/4)%int(image_num**0.5/2)]

# positive & negative pairs
a = []
p = []
l = []

# pos (shift)
for idx in range(mini,maxi+1):
	loc = location(idx)
	pending = []
	if loc[0] != 0:
		pending.append(((loc[0]-1)*int(image_num**0.5/2) + loc[1]) * 4 + idx%4)
	if loc[0] != int(image_num**0.5/2) - 1:
		pending.append(((loc[0]+1)*int(image_num**0.5/2) + loc[1]) * 4 + idx%4)
	if loc[1] != 0:
		pending.append((loc[0]*int(image_num**0.5/2) + loc[1] - 1) * 4 + idx%4)
	if loc[1] != int(image_num**0.5/2) - 1:
		pending.append((loc[0]*int(image_num**0.5/2) + loc[1] + 1) * 4 + idx%4)
	for i in range(5):
		for pend in pending:
			a.append(db_dir + str(idx) + '.jpg')
			p.append(db_dir + str(pend) + '.jpg')
			l.append(1)

for idx in grndtruth_dict:
	# pos
	for i in range(5):
		a.append(data_dir + str(idx) + '.jpg')
		p.append(db_dir + str(grndtruth_dict[idx]) + '.jpg')
		l.append(1)
	# nega 
	cnt = 10
	while cnt > 0:
		grd = grndtruth_dict[idx]
		pairp = random.randint(mini, maxi)
		locx = location(pairp)
		locy = location(grd)
		if max(abs(locx[0]-locy[0]), abs(locx[1]-locy[1])) < threshold:
			continue
		a.append(data_dir + str(idx) + '.jpg')
		p.append(db_dir + str(pairp) + '.jpg')
		l.append(0)
		cnt -= 1
print len(a)

# shuffle pairs
fouta = open(pair_a_file, 'w')
foutp = open(pair_p_file, 'w')
idx = [i for i in range(len(a))]
random.shuffle(idx)
for item in idx:
	fouta.write(a[item] + ' ' + str(l[item]) + '\n')
	foutp.write(p[item] + ' ' + str(l[item]) + '\n')
fouta.close()
foutp.close()


