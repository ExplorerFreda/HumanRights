filename = '/mnt/sda/backup/infolabel/train_label/grndtruth.txt'
output_filename = '/mnt/sda/backup/infolabel/pair_info/train_a.info'
direct = '/mnt/sda/backup/infolabel/train_label/%d.jpg'

fout = open(output_filename, 'w')

cnt = 0
train_data = []
for line in open(filename):
  cnt += 1
  if cnt < 100:
    continue
  if line[:-1] == '0':
    train_data.append(direct%cnt + ' 0\n')
    train_data.append(direct%cnt + ' 0\n')
    train_data.append(direct%cnt + ' 0\n')
    train_data.append(direct%cnt + ' 0\n')
  elif line[:-1] == '1':
    train_data.append(direct%cnt + ' 1\n')

import random
random.shuffle(train_data)
for line in train_data:
  fout.write(line)
fout.close()

