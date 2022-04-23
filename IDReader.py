from passporteye import read_mrz
import sys,os
from excel import excelFill
import PIL
import numpy as np
from pdf2image import convert_from_path
from IDReaderVanilla import getDataVanilla
from imageExtractor import imageExtract, cropBorder,white_borders
from matplotlib import pyplot as plt
from matplotlib import image as pltimage
import io
import detect_mrz_zhang
import cv2
import math


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
    img_type = type(img)
    if img_type not in  (bytearray,bytes) :

        success, encoded_image = cv2.imencode('.png', img)
        img = encoded_image.tobytes()
    mrz = read_mrz(img,save_roi=True, extra_cmdline_params=traineddataPath + ' --oem 0 -c tessedit_write_images=true') # ,extra_cmdline_params='--oem 0'
    
    if mrz != None:
        roiImg = mrz.aux['roi']
        plt.imshow(roiImg, interpolation='nearest')
        plt.gray()
        plt.title('ROI')
        plt.show()
    print("mrz results")
    if (mrz !=None): mrz = check_france(mrz)
    return mrz

def calculate_checksum(str_numbers):
    seven_three_one = [7,3,1,7,3,1,7,3,1,7,3,1]
    letter_values = {"A":10,"B":11,"C":12,"D":13,"E":14,"F":15,"G":16,"H":17,"I":18,"J":19,"K":20,"L":21,"M":22,"N":23,"O":24,"P":25,"Q":26,"R":27,"S":28,"T":29,"U":30,"V":31,"W":32,"X":33,"Y":34,"Z":35}
    numbers = [ x for x in list(str_numbers) ] # inte çevirmeyi kaldırdım geri koy alta
    numbers = [ letter_values[element] if element in letter_values  else element for element in numbers]
    numbers = [ int(element) if type(element) == str else element for element in numbers ]
    #search yaparken upper yap
    sum = 0
    # ends with shortests
    for num, sto in zip(numbers,seven_three_one):
        sum += num * sto
    remainder = sum % 10
    return remainder


def check_france(mrz):
    
    if mrz.type == "ID" and mrz.country == "FRA" and mrz.valid == False:
        mrz.mrz_type = "TDF"
        raw_text = mrz.aux['raw_text']
        mrz.last_name = raw_text[5:30].replace("<","")
        mrz.surname = mrz.last_name
        #issuanceoffice1
        #issuanceoffice2
        #issuance_date
        #issuanceoffice1
        #issue_number3
        
        mrz.number = raw_text[37:49]
        mrz.check_number =  raw_text[49]
        mrz.names = raw_text[50:63].replace("<<"," ")
        mrz.date_of_birth = raw_text[64:70]
        mrz.check_date_of_birth = raw_text[70]
        mrz.sex = raw_text[71]
        mrz.check_composite = raw_text[72]

        # 731 check
        
        cal_check_numbers = calculate_checksum( mrz.number)
        cal_check_date_of_birth = calculate_checksum( mrz.date_of_birth)
        
        mrz.valid_date_of_birth = True if cal_check_date_of_birth  == int(mrz.check_date_of_birth)  else False
        mrz.valid_number = True if cal_check_numbers  == int(mrz.check_number)  else False

        mrz.expiration_date = " "
        mrz.nationality = " "

        fra_valid_score = 20
        if mrz.valid_date_of_birth : fra_valid_score += 35
        if mrz.valid_number : fra_valid_score += 35
        mrz.valid_score = fra_valid_score
    print("viva la revolution")
    return mrz

def read_image(filename):
    img=  cv2.imread(filename)
    return img

def pipeline_normal():
    pass
def pipeline_filter():
    pass
def check_valid(mrz):
    mrz = getData(image)
    if (mrz !=None) and (mrz.valid_score > 50):
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
       
        mrz = getData(image)
        if (mrz !=None) and (mrz.valid_score > 50):
            break
        
        np270 = np.rot90(image,3)

        plt.imshow(np270,cmap="gray")
        plt.title('rotated 270')
        plt.show()
        

        mrz = getData(np270)
        if (mrz !=None) and (mrz.valid_score > 50):
            break

        np90 = np.rot90(image,1)

        plt.imshow(np90,cmap="gray")
        plt.title('rotated 90')
        plt.show()

        mrz = getData(np90)
        if (mrz !=None) and (mrz.valid_score > 50):
            break

        image = white_borders(image,14.5)
        mrz = getData(image)
        if (mrz !=None) and (mrz.valid_score > 50):
            break

        

    excelFill(mrz)
  
if __name__ == '__main__':
    if (len(sys.argv)<2):
        print("No arguments. Using default file")
        defaultfile = "DenisFloch_ID_Apr19.pdf"
        main(defaultfile)
    else:
        main(sys.argv[1])
# Tesseract white list galiba çalışmıyor. File3'de euro simgesi var idnumber da

#if mrz_lines[0][0].upper() == 'V': return 'MRVB' 
#return "TDF" if mrz_lines[0][2:5].upper() == "FRA" else 'TD2'