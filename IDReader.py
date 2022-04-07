from passporteye import read_mrz
import sys,os
from excel import excelFill
import PIL
import numpy as np
from pdf2image import convert_from_path
from IDReaderVanilla import getDataVanilla
from imageExtractor import imageExtract, colorFilter,removeBorder,removeSmallBlobs
from matplotlib import pyplot as plt
import imageio as iio
import detect_mrz_zhang


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

def combineImages(imageNameList,savepath):
    imgs    = [ PIL.Image.open(i) for i in imageNameList ]
    # for a vertical stacking it is simple: use vstack
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    imgs_comb = PIL.Image.fromarray( imgs_comb)
    imgs_comb.save( savepath+'verticalCombined.png' )

def getData(fileIn):
    cwd = os.getcwd()
    traineddataPath= "--tessdata-dir "+cwd+"/tessdata/"
    mrz = read_mrz(fileIn,save_roi=True, extra_cmdline_params=traineddataPath + ' --oem 0 -c tessedit_write_images=true') # ,extra_cmdline_params='--oem 0'
    
    if mrz != None:
        roiImg = mrz.aux['roi']
        #plt.imshow(roiImg, interpolation='nearest')
        #plt.gray()
        #plt.show()
    print("debug")
    return mrz

def read_image(filename):
    with open(filename, "rb") as image:
        img = image.read()
        #byte_img = bytearray(img)
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
        if (mrz !=None) and (mrz.valid_score > 70):
            break
    """ else:
        
        imageList.append(img)
        img = colorFilter(imageList)[0] # filter for images
        mrz = getData(img) """
        # if file is image pass path. Actually it might be better to ust pass image and read image myself
    excelFill(mrz)
  
if __name__ == '__main__':
    if (len(sys.argv)<2):
        print("No arguments. Using default file")
        defaultfile = "IR.png"
        main(defaultfile)
    else:
        main(sys.argv[1])
# Tesseract white list galiba çalışmıyor. File3'de euro simgesi var idnumber da