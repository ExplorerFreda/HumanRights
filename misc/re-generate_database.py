import os
raw_data_dir = '/mnt/sda/backup/streetview45/dbdata/'
new_dbdata_dir = '/mnt/sda/backup/data/database/'

for x in range(15,35):
  for y in range(15,35):
    for a in range(4):
      idx = (x * 50 + y) * 4 + a
      new_idx = ((x - 15) * 20 + y - 15) * 4 + a
      os.system('cp ' + raw_data_dir + str(idx) + '.jpg ' + new_dbdata_dir)
      os.system('mv ' + new_dbdata_dir + str(idx) + '.jpg ' + new_dbdata_dir + str(new_idx) + '.jpg')
os.system('ls ' + new_dbdata_dir + ' | wc -l')
