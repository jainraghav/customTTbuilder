import pdfplumber
from decimal import Decimal
from PIL import Image
import os
import shutil
import argparse

class Options():
    def __init__(self):
        parser = argparse.ArgumentParser(description='Custom TT Builder',
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('--tmplt_path', type=str, default="TT-1.jpg" ,help='Path to the empty TimeTable template image')
        parser.add_argument('--save_as', type=str, default="custom_TT.jpg"  ,help='Final saved time table img name')
        parser.add_argument('--pdfpath', type=str, default="TimeTable.pdf"  ,help='input TimeTable pdf file path')
        parser.add_argument('--sublist', nargs='+',help='Course codes input list', required=True)

        self.parser = parser

    def parse(self):
        return self.parser.parse_args()

def process(pdfpath,input):
    pdf = pdfplumber.open(pdfpath)
    p0 = pdf.pages[0]
    print("Analysing pdf...")
    xtab = p0.debug_tablefinder()
    im  = p0.to_image()
    orig_size = im.original.size

    boxes=[]
    for a in xtab.cells:
      box = (float(a[0]),float(a[1]),float(a[2]),float(a[3]))
      boxes.append(box)
    x = p0.extract_words()

    relevant=[]
    for words in x:
        if words['text'] in input:
            words['bottom'] = float(words['bottom'])
            words['top'] = float(words['top'])
            words['x0'] = float(words['x0'])
            words['x1'] = float(words['x1'])
            relevant.append(words)
    finalpaste=[]
    for x in relevant:
        for y in boxes:
            if check_overlap(y,(x['x0'],x['top'],x['x1'],x['bottom'])):
                finalpaste.append(y)
    return finalpaste,p0

def cropNsave(p0,directory,finalpaste):
    if not os.path.exists(directory):
        os.mkdir(directory)
    for bbox in finalpaste:
        name = str(bbox[0])+'#'+str(bbox[1])+'#'+str(bbox[2])+'#'+str(bbox[3])
        p0.crop(bbox).to_image().save(directory+name+'.jpg')

def paste_everything(directory,base,saved_image):
    for file in os.listdir(directory):
        cords = file[:-4].split('#')
        cords = [int(float(x)) for x in cords]
        #print(cords,file)
        small_box = Image.open(directory+file)
        base.paste(small_box, (cords[0],cords[1]))
        base.save(saved_image)
    shutil.rmtree(directory)
    print("Custom Time Table saved as "+"'"+saved_image+"'")

def check_overlap(A,B):
    if A[3]<=B[1]:
        return False
    if A[1]>=B[3]:
        return False
    if A[2]<=B[0]:
        return False
    if A[0]>=B[2]:
        return False

    return True

if __name__ == '__main__':
    args = Options().parse()

    #input = ["ML","AI","IA","EVS","Tcom","CN"]
    input = args.sublist
    ttpdf_path = args.pdfpath
    finalpaste,p0 = process(ttpdf_path,input)
    #Saving
    print("Saving boxes to extract...")
    directory = "saved_boxes/"
    cropNsave(p0,directory,finalpaste)

    base = Image.open(args.tmplt_path)
    orig_size = p0.to_image().original.size
    base = base.resize((orig_size[0],orig_size[1]),Image.ANTIALIAS)
    #Pasting boxes on the template
    print("Almost Ready...")
    saved_image = args.save_as
    paste_everything(directory,base,saved_image)
