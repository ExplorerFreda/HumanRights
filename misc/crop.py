from PIL import Image
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET 
from os import system

list = [
'0.xml','1.xml','10.xml','1000.xml','1001.xml','1002.xml','1003.xml','1004.xml',
'1005.xml','1006.xml','1007.xml','1008.xml','1009.xml','1010.xml','1011.xml',
'1012.xml','1013.xml','1014.xml','1015.xml','1016.xml','1017.xml','1018.xml',
'1019.xml','1080.xml','1081.xml','1082.xml','1083.xml','1084.xml','1085.xml',
'1086.xml','1087.xml','1088.xml','1089.xml','1090.xml','1091.xml','1092.xml',
'1093.xml','1094.xml','1095.xml','1096.xml','1097.xml','1098.xml','1099.xml',
'11.xml','12.xml','13.xml','14.xml','15.xml','16.xml','17.xml','18.xml','19.xml',
'2.xml','3.xml','4.xml','5.xml','6.xml','7.xml','720.xml','721.xml','722.xml','723.xml',
'724.xml','725.xml','726.xml','727.xml','728.xml','729.xml','730.xml','731.xml',
'732.xml','733.xml','734.xml','735.xml','736.xml','737.xml','738.xml','739.xml',
'8.xml','80.xml','81.xml','82.xml','83.xml','84.xml','840.xml','841.xml','842.xml',
'843.xml','844.xml','845.xml','846.xml','847.xml','848.xml','849.xml','85.xml',
'850.xml','851.xml','852.xml','853.xml','854.xml','855.xml','856.xml','857.xml',
'858.xml','859.xml','86.xml','87.xml','88.xml','89.xml','9.xml','90.xml','900.xml',
'901.xml','902.xml','903.xml','904.xml','905.xml','906.xml','907.xml','908.xml',
'909.xml','91.xml','910.xml','911.xml','912.xml','913.xml','914.xml','915.xml',
'916.xml','917.xml','918.xml','919.xml','92.xml','920.xml','921.xml','922.xml',
'923.xml','924.xml','925.xml','926.xml','927.xml','928.xml','929.xml','93.xml',
'930.xml','931.xml','932.xml','933.xml','934.xml','935.xml','936.xml','937.xml',
'938.xml','939.xml','94.xml','95.xml','96.xml','97.xml','98.xml','99.xml']
img_dir = '/mnt/sda/backup/data/database/'
xml_dir = '/mnt/sda/backup/data/salient_label/'
new_img_dir = '/mnt/sda/backup/data/salient_database/'

def ScanPoints(filename):
    ret = []
    tree = ET.parse(filename)
    root = tree.getroot()
    for item in root.find('object').find('polygon').findall('pt'):
        x = item.find('x').text
        y = item.find('y').text
        ret.append((x,y))
    return ret

def WritePointInfo(a, b):
    fout = open('in.txt', 'w')
    fout.write(str(len(a)) + ' ' + str(len(b)) + '\n')
    for item in a:
        fout.write(str(item[0]) + ' ' + str(item[1]) + '\n')
    for item in b:
        fout.write(str(item[0]) + ' ' + str(item[1]) + '\n')
    fout.close()
    
cnt = 0
gout = open(new_img_dir + 'groundtruth.txt', 'w')
for item in list:
    img_filename = img_dir + item.replace('xml','jpg')
    im = Image.open(img_filename)
    polygon = ScanPoints(xml_dir + item)
    for cropsize in range(2, 5):
        lenx = im.size[0] // cropsize
        leny = im.size[1] // cropsize
        for lx in range(0, im.size[0] - lenx + 1, lenx):
            for uy in range(0, im.size[1] - leny + 1, leny):
                out = im.crop((lx,uy,lx+lenx,uy+leny))
                square = [(lx, uy), (lx, uy+leny), (lx+lenx, uy+leny), (lx+lenx, uy)]
                # Compute area
                WritePointInfo(polygon, square)
                system('./main')
                fin = open('out.txt')
                area = float(fin.readline())
                fin.close()
                area_rate = area / lenx / leny
		if area_rate < 0.4:
		    area_label = 0
		elif area_rate < 0.7:
		    area_label = 1
		else:
		    area_label = 2
		new_filename = new_img_dir + str(cnt) + '.jpg'
		gout.write(new_filename + ' ' + str(area_label) + '\n')
		out.save(new_filename)
		cnt += 1
    print item, cnt
gout.close()
