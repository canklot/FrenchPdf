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
    # Extract images from pdf
    cwd = os.getcwd()
    doc = fitz.open(cwd+"/uploads/"+filename)
    
    imageList = []
    for i in range(len(doc)):
        page_images = doc.get_page_images(i)
        # 5 is colorspace
        if any( pimg[5] == "" for pimg in page_images):
            # If pdf file has weird images in it without a colorspace dont extract images
            # Instead take a screen shoot of the whole page
            for page in doc:  # Iterate through the pages
                zoom_x = 3.5  # Horizontal zoom
                zoom_y = 3.5  # Vertical zoom
                mat = fitz.Matrix(zoom_x, zoom_y) 
                pix = page.get_pixmap(matrix=mat)  # Render page to an image
                pix = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, -1)) 
                # Convert PyMuPDF.pix to numpy
                
                """ plt.imshow(pix, interpolation='nearest')
                plt.title('All_page_img')
                plt.show() """

                pix = crop_convex_hull(pix)
                imageList.append(pix)  
        else:
            # If all the images inside pdf has a colorspace and things look normal extract images
            for img in page_images:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5: # this is GRAY or RGB
                    pix = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, -1))
                    mymax = pix.max()
                    if pix.max() == 255 :
                        # Some grey images has 255 as white. Scale them to between 1 and 0
                        pix = (pix - np.min(pix))/np.ptp(pix)
                else:# CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    #pix =  pix.pil_tobytes(format="JPG", optimize=True) # If you need PIL image. But I am using numpy array
                    pix = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))

                """ plt.imshow(pix)
                plt.title('extract')
                plt.show() """

                pix = crop_convex_hull(pix)
                imageList.append(pix)
                pix = None
    return imageList

def add_margin_bbox(imageBox,margin_percent,im):
    # Tesseract perform better with some margin around the text
    # So add some margin on bounding box of cropped image
    # Info: PIL coordinates start from left upper corner (0,0)
    left = imageBox[0]
    up = imageBox[1]
    right = imageBox[2]
    down = imageBox[3]
    margin_amount_horizontal = (right - left) / 100 * margin_percent
    margin_amount_vertical = (down - up) / 100 * margin_percent

    new_left = max(1,left - margin_amount_horizontal)
    new_right = min(im.shape[1],right + margin_amount_horizontal)
    new_up= min(1,up + margin_amount_vertical)
    new_down =max(im.shape[0],down - margin_amount_vertical)
    imageBox_new = (new_left,new_up,new_right,new_down)
    return imageBox_new

def crop_convex_hull(im):
    # Crops white spaces in the image
    if im.shape[2] == 3:
        #If its rgb image turn it to gray
        im = rgb2gray(im)
    # There are a lot of plt.show calls because of debuging
    """ plt.imshow(im,cmap="gray")
    plt.title('amigray')
    plt.show() """
    im1 = 1 - im # Takes negative of the image
    """ plt.imshow(im1,cmap="gray")
    plt.title('after substraction')
    plt.show() """
    # do some blur or closing etc here for better cropping
    threshold = 0.65
    im1[im1 <= threshold] = 0
    im1[im1 > threshold] = 1
    """ plt.imshow(im1,cmap="gray")
    plt.title('after threshold')
    plt.show() """
    chull = convex_hull_image(im1)
    
    """ plt.imshow(chull)
    plt.title('convex hull in the binary image')
    plt.show() """

    imageBox = PIL.Image.fromarray((chull*255).astype(np.uint8)).getbbox()
    imageBox_new = add_margin_bbox(imageBox,10,im)
    cropped = PIL.Image.fromarray(im).crop(imageBox_new)
    cropped = np.asarray(cropped)

    """ plt.imshow(cropped)
    plt.title('crop_convex_hull')
    plt.show() """

    return cropped

def white_borders_skimage(img,thickness):
    img_height=img.shape[0]
    img_width=img.shape[1]
    percent_to_pix = int(img_width * thickness / 100)
    # To save space I was going to use skimage not OpenCV but didnt finished it
    
def white_borders(img,thickness):
    # Draw white line on the borders of the image to cover up thick lines in some ID cards like cameroon
    img_height=img.shape[0]
    img_width=img.shape[1]
    percent_to_pix = int(img_width * thickness / 100)
    cv2.line(img,(0,0),(0,img_height),(255,255,255),percent_to_pix)
    cv2.line(img,(img_width,0),(img_width,img_height),(255,255,255),percent_to_pix)

    """ plt.imshow(img, interpolation='nearest')
    plt.title('white border')
    plt.show() """

    return img

