image_num = 1600
image_dir = '/mnt/sda/backup/data/database/'
new_image_dir = '/mnt/sda/backup/data/train/'

from PIL import Image
import random
import cv2


fout = open(new_image_dir + 'groundtruth.txt', 'w')
cnt = 0
for idx in range(image_num):
  image_name = image_dir + str(idx) + '.jpg'
  im = Image.open(image_name)

  # genetate 400*400 subimage
  for i in range(3):
    out = im.rotate(random.randint(-30,30), expand=1)
    centx = out.size[0] / 2
    centy = out.size[1] / 2
    lenx = out.size[0] / 4
    leny = out.size[1] / 4
    leftx = random.randint(centx - lenx, centx + lenx - 300)
    upy = random.randint(centy - leny, centy + leny - 300)
    sub_image = (leftx, upy, leftx + 300, upy + 300)
    out = out.crop(sub_image)
    out.save(new_image_dir + str(cnt) + '.jpg')
    fout.write(str(cnt) + '\t' + str(idx) + '\n')
    print cnt, out.size
    cnt += 1
  # generate 200*200 subimage
  for i in range(3):
    out = im.rotate(random.randint(-30,30), expand=1)
    centx = out.size[0] / 2
    centy = out.size[1] / 2
    lenx = out.size[0] / 4
    leny = out.size[1] / 4
    leftx = random.randint(centx - lenx, centx + lenx - 200)
    upy = random.randint(centy - leny, centy + leny - 200)
    sub_image = (leftx, upy, leftx + 200, upy + 200)
    out = out.crop(sub_image)
    out.save(new_image_dir + str(cnt) + '.jpg')
    fout.write(str(cnt) + '\t' + str(idx) + '\n')
    print cnt, out.size
    cnt += 1


fout.close()
