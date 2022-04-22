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
from skimage.morphology import convex_hull_image
from skimage.color import rgb2gray,hsv2rgb


# return numpyarray not bytes. There is byte convertion here
def imageExtract(filename):
    cwd = os.getcwd()
    doc = fitz.open(cwd+"/uploads/"+filename)
    
    imageList = []
    for i in range(len(doc)):
        page_images = doc.get_page_images(i)
        # 5 is colorspace
        if any( pimg[5] == "" for pimg in page_images):
            for page in doc:  # iterate through the pages
                zoom_x = 3.5  # horizontal zoom
                zoom_y = 3.5 # vertical zoom
                mat = fitz.Matrix(zoom_x, zoom_y) 
                pix = page.get_pixmap(matrix=mat)  # render page to an image
                pix = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, -1))
                
                plt.imshow(pix, interpolation='nearest')
                plt.title('All_page_img')
                plt.show()

                #pix = crop_numpy(pix)
                pix = crop_convex_hull(pix)
                imageList.append(pix)
                 
        else:
            for img in page_images:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.colorspace == None:
                    continue
                elif pix.n == 1:      
                    pix = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, -1))
                    mymax = pix.max()
                    if pix.max() == 255 :
                        pix = (pix - np.min(pix))/np.ptp(pix)
                elif pix.n < 5:       # this is GRAY or RGB
                    #pix.writePNG("p%s-%s.png" % (i, xref))
                    #pix =  pix.pil_tobytes(format="PNG", optimize=True)
                    pix = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
                    
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    #pix =  pix.pil_tobytes(format="JPG", optimize=True)
                    pix = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
                    #pix1.writePNG("p%s-%s.jpg" % (i, xref))
                    #pix1 = None

                plt.imshow(pix)
                plt.title('extract')
                plt.show()

                pix = crop_convex_hull(pix)
                imageList.append(pix)
                pix = None
    return imageList
# First test it then return them in a list. May also save them fur debug

def crop_convex_hull(im):
    if im.shape[2] == 3:
        im = rgb2gray(im)
    plt.imshow(im,cmap="gray")
    plt.title('amigray')
    plt.show()
    im1 = 1 - im # Takes negative of the image
    plt.imshow(im1,cmap="gray")
    plt.title('after substraction')
    plt.show()
    # do some blur or closing etc
    threshold = 0.65
    im1[im1 <= threshold] = 0
    im1[im1 > threshold] = 1
    plt.imshow(im1,cmap="gray")
    plt.title('after threshold')
    plt.show()
    chull = convex_hull_image(im1)
    plt.imshow(chull)
    plt.title('convex hull in the binary image')
    plt.show()
    imageBox = PIL.Image.fromarray((chull*255).astype(np.uint8)).getbbox()
    # add margin
    margin_amount = imageBox[0]
    cropped = PIL.Image.fromarray(im).crop(imageBox)
    cropped = np.asarray(cropped)
    plt.imshow(cropped)
    plt.title('crop_convex_hull')
    plt.show()
    return cropped


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

def white_borders_skimage(img,thickness):
    img_height=img.shape[0]
    img_width=img.shape[1]
    percent_to_pix = int(img_width * thickness / 100)
    
def white_borders(img,thickness):
    img_height=img.shape[0]
    img_width=img.shape[1]
    percent_to_pix = int(img_width * thickness / 100)
    cv2.line(img,(0,0),(0,img_height),(255,255,255),percent_to_pix)
    cv2.line(img,(img_width,0),(img_width,img_height),(255,255,255),percent_to_pix)
    plt.imshow(img, interpolation='nearest')
    plt.title('white border')
    plt.show()
    return img

def cropBorder(img,crop_percent):
    print(type(img))
    img_height=img.shape[0]
    img_width=img.shape[1]
    new_top = int(img_height - (img_height * crop_percent / 100))
    new_right = int(img_width - (img_width * crop_percent / 100))
    new_bottom = int(img_height * crop_percent / 100)
    new_left = int(img_width * crop_percent / 100)
    cropped = img[new_bottom:new_top, new_left:new_right]

    plt.imshow(cropped, interpolation='nearest')
    plt.title('cropped_border')
    plt.show()

    return cropped
    


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
