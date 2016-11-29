image_num = 1600
image_dir = '/mnt/sda/backup/data/database/'
new_image_dir = '/mnt/sda/backup/data/test/'

from PIL import Image
import random
import cv2

def location(idx):
  return [idx/4//20, idx/4%20]

fout = open(new_image_dir + 'groundtruth.txt', 'w')
cnt = 0
for idx in range(image_num):
  loc = location(idx)
  if loc[0] < 5 or loc[0] > 14 or loc[1] < 5 or loc[1] > 14:
    continue
  image_name = image_dir + str(idx) + '.jpg'
  im = Image.open(image_name)

  # genetate 400*400 subimage
  for i in range(2):
    out = im.rotate(random.randint(-30,30), expand=1)
    centx = out.size[0] / 2
    centy = out.size[1] / 2
    lenx = out.size[0] / 4
    leny = out.size[1] / 4
    leftx = random.randint(centx - lenx, centx + lenx - 350)
    upy = random.randint(centy - leny, centy + leny - 350)
    sub_image = (leftx, upy, leftx + 350, upy + 350)
    out = out.crop(sub_image)
    out.save(new_image_dir + str(cnt) + '.jpg')
    fout.write(str(cnt) + '\t' + str(idx) + '\n')
    print cnt, out.size
    cnt += 1
  # generate 200*200 subimage
  for i in range(2):
    out = im.rotate(random.randint(-30,30), expand=1)
    centx = out.size[0] / 2
    centy = out.size[1] / 2
    lenx = out.size[0] / 4
    leny = out.size[1] / 4
    leftx = random.randint(centx - lenx, centx + lenx - 250)
    upy = random.randint(centy - leny, centy + leny - 250)
    sub_image = (leftx, upy, leftx + 250, upy + 250)
    out = out.crop(sub_image)
    out.save(new_image_dir + str(cnt) + '.jpg')
    fout.write(str(cnt) + '\t' + str(idx) + '\n')
    print cnt, out.size
    cnt += 1


fout.close()
