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

def getData(img):
    cwd = os.getcwd()
    traineddataPath= "--tessdata-dir "+cwd+"/tessdata/"
    img_type = type(img)
    if img_type not in  (bytearray,bytes) :
        # Passporteye only works with binary image
        success, encoded_image = cv2.imencode('.png', img)
        img = encoded_image.tobytes()
    mrz = read_mrz(img,save_roi=True, extra_cmdline_params=traineddataPath + ' --oem 0 -c tessedit_write_images=true') # ,extra_cmdline_params='--oem 0'
    
    if mrz != None:
        # Print MRZ field on screen
        roiImg = mrz.aux['roi']
        plt.imshow(roiImg, interpolation='nearest')
        plt.gray()
        plt.title('ROI')
        plt.show()
    if (mrz !=None): mrz = check_france(mrz)
    # Passport eye cant process old france ID. So I process it myself
    return mrz

def calculate_checksum(str_numbers):
    # 731 cheksum calculation. More info https://planetcalc.com/9535/
    seven_three_one = [7,3,1,7,3,1,7,3,1,7,3,1]
    letter_values = {"A":10,"B":11,"C":12,"D":13,"E":14,"F":15,"G":16,"H":17,"I":18,"J":19,"K":20,"L":21,"M":22,"N":23,"O":24,"P":25,"Q":26,"R":27,"S":28,"T":29,"U":30,"V":31,"W":32,"X":33,"Y":34,"Z":35}
    numbers = [ x for x in list(str_numbers) ] # Turns one string to seperate char list 
    numbers = [ letter_values[element] if element in letter_values  else element for element in numbers] # Turn letters to numbers
    numbers = [ int(element) if type(element) == str else element for element in numbers ] # Turn everything to int
    sum = 0
    for num, sto in zip(numbers,seven_three_one):
        sum += num * sto
    remainder = sum % 10
    return remainder


def check_france(mrz):
    if mrz.type == "ID" and mrz.country == "FRA" and mrz.valid == False:
        # If its old type of French ID with 2 line we need to process the raw data.
        # https://en.wikipedia.org/wiki/National_identity_card_(France)
        mrz.mrz_type = "TDF"
        raw_text = mrz.aux['raw_text']
        mrz.last_name = raw_text[5:30].replace("<","")
        mrz.surname = mrz.last_name
        mrz.number = raw_text[37:49]
        mrz.check_number =  raw_text[49]
        mrz.names = raw_text[50:63].replace("<<"," ")
        mrz.date_of_birth = raw_text[64:70]
        mrz.check_date_of_birth = raw_text[70]
        mrz.sex = raw_text[71]
        mrz.check_composite = raw_text[72]

        # Calculate the cheksums after processing the raw data
        cal_check_numbers = calculate_checksum(mrz.number)
        cal_check_date_of_birth = calculate_checksum(mrz.date_of_birth)
        
        # If calculated checksum and cheksum on the ID is same assign True to valid flags
        mrz.valid_date_of_birth = True if cal_check_date_of_birth  == int(mrz.check_date_of_birth)  else False
        mrz.valid_number = True if cal_check_numbers  == int(mrz.check_number)  else False

        # Remove old and wrong info
        mrz.expiration_date = " "
        mrz.nationality = " "

        # If valid flags truee increment valid score
        fra_valid_score = 20
        if mrz.valid_date_of_birth : fra_valid_score += 35
        if mrz.valid_number : fra_valid_score += 35
        mrz.valid_score = fra_valid_score
    return mrz

def main (fileName):
    cwd = os.getcwd()
    img= cv2.imread(cwd+"/uploads/"+fileName)
    imageList = []
   
    if fileName[-3:]=="pdf":
         # Extract images from pdf files.
        imageList = imageExtract(fileName)
    else:
        # If file is just a image. Add it to the list
        imageList.append(img)

    for image in imageList:
        # Read the data from image. If valid return it
        mrz = getData(image)
        if (mrz !=None) and (mrz.valid_score > 50):
            break

        # Try again by rotating it to right
        np270 = np.rot90(image,3)
        plt.imshow(np270,cmap="gray")
        plt.title('rotated 270')
        plt.show()
        mrz = getData(np270)
        if (mrz !=None) and (mrz.valid_score > 50):
            break

        # Try again by rotating it to left
        np90 = np.rot90(image,1)
        plt.imshow(np90,cmap="gray")
        plt.title('rotated 90')
        plt.show()
        mrz = getData(np90)
        if (mrz !=None) and (mrz.valid_score > 50):
            break
        
        # Try again after painting the borders white. For ID's with thick borders like cameroon
        image = white_borders(image,14.5)
        mrz = getData(image)
        if (mrz !=None) and (mrz.valid_score > 50):
            break

    # Put the data on excel file
    excelFill(mrz)
  
if __name__ == '__main__':
    if (len(sys.argv)<2):
        print("No arguments. Using default file")
        defaultfile = "DenisFloch_ID_Apr19.pdf"
        main(defaultfile)
    else:
        main(sys.argv[1])