from passporteye import read_mrz
import sys,os
from excel import excelFill
import PIL
import numpy as np
from pdf2image import convert_from_path
from IDReaderVanilla import getDataVanilla
from imageExtractor import imageExtract, colorFilter,removeSmallBlobs, cropBorder,white_borders
from matplotlib import pyplot as plt
from matplotlib import image as pltimage
import io
import detect_mrz_zhang
import cv2


def pdf2Image(path):
    saveNameList = []
    cwd = os.getcwd()
    images = convert_from_path(path)
    for i in range(len(images)):
        # Save pages as images in the pdf
        saveName = cwd+"/files/"+'page'+ str(i) +'.png'
        saveNameList.append(saveName)
        images[i].save(saveName, 'PNG')
        # Maybe find a way to combine all images
    combineImages(saveNameList,cwd+"/uploads/")

def getData(img):
    cwd = os.getcwd()
    traineddataPath= "--tessdata-dir "+cwd+"/tessdata/"
    if type(img) != bytearray:
        success, encoded_image = cv2.imencode('.png', img)
        img = encoded_image.tobytes()
    mrz = read_mrz(img,save_roi=True, extra_cmdline_params=traineddataPath + ' --oem 0 -c tessedit_write_images=true') # ,extra_cmdline_params='--oem 0'
    
    if mrz != None:
        roiImg = mrz.aux['roi']
        plt.imshow(roiImg, interpolation='nearest')
        plt.gray()
        plt.show()
    print("debug")
    return mrz

def read_image(filename):
    img=  cv2.imread(filename)
    return img

def pipeline_normal():
    pass
def pipeline_filter():
    pass


def main (fileName):
    cwd = os.getcwd()
    img= read_image(cwd+"/uploads/"+fileName)
    imageList = []
    if fileName[-3:]=="pdf":
        imageList = imageExtract(fileName)
         # filter for pdf
    else:
        imageList.append(img)

    #imageList = colorFilter(imageList)

    for image in imageList:
        #mrz_zhang = detect_mrz_zhang.detect_mrz(image)
        #image = removeBorder(image)
        #image = removeSmallBlobs(image)
        mrz = getData(image)
        if (mrz !=None) and (mrz.valid_score > 50):
            break
        #image = cropBorder(image, 7.5)
        image = white_borders(image,14.5)
        mrz = getData(image)
        if (mrz !=None) and (mrz.valid_score > 50):
            break
    excelFill(mrz)
  
if __name__ == '__main__':
    if (len(sys.argv)<2):
        print("No arguments. Using default file")
        defaultfile = "sishi_passport.pdf"
        main(defaultfile)
    else:
        main(sys.argv[1])
# Tesseract white list galiba çalışmıyor. File3'de euro simgesi var idnumber da