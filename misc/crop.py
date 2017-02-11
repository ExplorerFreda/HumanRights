from PIL import Image
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET 
from os import system


xml_dir = '../../data/collection/%d.xml'
img_dir = '../../data/frames/%d.jpg'

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
    
gout = open('groundtruth.txt', 'w')
for idx in range(1, 100+1):
    cnt = 0
    img_filename = img_dir%idx
    xml_filename = xml_dir%idx
    im = Image.open(img_filename)
    polygon = ScanPoints(xml_filename)
    for cropsize in range(1, 4):
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
                gout.write(str(idx) + ' ' + str(cnt) + ' ' + str(area_rate) + '\n') 
                cnt += 1
    print idx, cnt
gout.close()
