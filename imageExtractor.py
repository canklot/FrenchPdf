import fitz
import os
import numpy as np
import cv2
import PIL
import io
# pip install PyMuPDF
from matplotlib import pyplot as plt
from matplotlib.colors import hsv_to_rgb
from skimage import io as skimage_io 
from skimage import transform, morphology, filters, measure, color,img_as_ubyte


def imageExtract(filename):
    cwd = os.getcwd()
    doc = fitz.open(cwd+"/uploads/"+filename)
    imageList = []
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG("p%s-%s.png" % (i, xref))
                pix =  pix.pil_tobytes(format="PNG", optimize=True)
                imageList.append(pix)
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix =  pix.pil_tobytes(format="JPG", optimize=True)
                imageList.append(pix)
                pix1.writePNG("p%s-%s.jpg" % (i, xref))
                pix1 = None
            pix = None
    return imageList
# First test it then return them in a list. May also save them fur debug

def remove_color(hsv_start, hsv_end):
    pass

def resize(img_in):
    max_width = 900
    
    scale_percent = (100*max_width)/ img_in.shape[1] # percent of original size
    width = int(img_in.shape[1] * scale_percent / 100)
    height = int(img_in.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img_in, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow("resized", resized)
    waitUntilX("resized")
    cv2.destroyAllWindows()
    
    return resized, scale_percent

def removeSmallBlobs(img_in):
    if not isinstance(img_in, np.ndarray):
        pil_image = PIL.Image.open(io.BytesIO(img_in))
        img_in = np.array(pil_image)  
        img_in = color.rgb2gray(img_in)
    img_in = cv2.convertScaleAbs(img_in)
    img_in, scale_percent = resize(img_in)
    contours, hierarchy = cv2.findContours(img_in,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #scale_percent = int(scale_percent)-100
    threshhold_blob_area = 2 * scale_percent /100

    for i in range (1,len(contours)):
        index_level = int(hierarchy[0][i][1])
        if index_level <= i :
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            print(area)
            if area <= threshhold_blob_area:
                cv2.drawContours(img_in,[cnt],-1,255,-1,1)

    cv2.imshow("blobs_removed", img_in)
    waitUntilX("blobs_removed")
    cv2.destroyAllWindows()

    return img_in

def waitUntilX(window):
    while True:
        k = cv2.waitKey(100) # change the value from the original 0 (wait forever) to something appropriate
        if k == 27:
            print('ESC')
            cv2.destroyAllWindows()
            break        
        if cv2.getWindowProperty(window,cv2.WND_PROP_VISIBLE) < 1:        
            break        
    cv2.destroyAllWindows()

def find_id(img):
    pass


def removeBorder(img_in):
    
    gray = skimage_io.imread(img_in, as_gray=True, plugin='imageio')
    

    gray = removeSmallBlobs(gray)

    resized , scalefactor = resize(gray)
    cs = measure.find_contours(resized, 0.5) #0.5

    # Display the image and plot all contours found
    fig, ax = plt.subplots()
    ax.imshow(resized,cmap=plt.cm.gray)#, cmap=plt.cm.gray

    for contour in cs:
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()

def adaptive_gaussian(img):
    img = img_as_ubyte(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img,5)
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    plt.imshow(th3, interpolation='nearest', cmap='gray')
    plt.title('adaptive_gaussian')
    plt.show()
    return th3


def colorFilter(imageList):
    convertedList = []
    for image in imageList:
        pil_image = PIL.Image.open(io.BytesIO(image))
        
        image = np.array(pil_image)  
        #image = adaptive_gaussian(image)
        

        plt.imshow(image,interpolation='nearest')
        plt.show()

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


        plt.imshow(hsv, interpolation='nearest')
        plt.title('afterhsv')
        plt.show()

        lower_color= np.array([0,0,0])
        upper_color = np.array([255,255,70])

        mask = cv2.inRange(hsv, lower_color, upper_color)
        cv2.imshow('normal mask', mask)
        waitUntilX('normal mask')

        res = cv2.bitwise_and(hsv,hsv, mask= mask)
        cv2.imshow('masked res', mask)
        waitUntilX('masked res')

        invertedmask = cv2.bitwise_not(mask)
        cv2.imshow('inverted mask', invertedmask)
        waitUntilX('inverted mask')
        
        #res = cv2.bitwise_and(image,image, mask= invertedmask)

        #rgb = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)

        print("after rgb")
        plt.imshow(invertedmask, interpolation='nearest')
        plt.show()

        #invertedmask = removeSmallBlobs(invertedmask)
        
        success, encoded_image = cv2.imencode('.png', invertedmask)
        rgb = encoded_image.tobytes()
        
        convertedList.append(rgb)
    return convertedList
