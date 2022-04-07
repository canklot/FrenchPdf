from PIL import Image
import os
import pytesseract

def getDataVanilla(filename):
    cwd = os.getcwd()
    filename = cwd+"/uploads/"+filename
    traineddataPath= "--tessdata-dir "+cwd+"/tessdata/ "
    whitelistParam = "tessedit_char_whitelist abcdefghijklmnopqrstuvwxyz<"
    myconfig = traineddataPath + '--oem 0 --psm 6 -c tessedit_write_images=true' + whitelistParam
    myfile = Image.open(filename)
    out1 = pytesseract.image_to_string(myfile,config=myconfig)
    out2 = pytesseract.image_to_string(filename) # Thiis bypass image convertion?

    # Get bounding box estimates
    print(pytesseract.image_to_boxes(Image.open('test.png')))

    # Get verbose data including boxes, confidences, line and page numbers
    print(pytesseract.image_to_data(Image.open('test.png')))

    # Get information about orientation and script detection
    print(pytesseract.image_to_osd(Image.open('test.png')))
