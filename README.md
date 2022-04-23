# README #

Hi here is a short jump start guide

### What is this repository for? ###

* A website for parsing sale contract PDF files and extracting borrower data such as names, address, birthday etc.
* A website for reading machine readable fields from ID cards and Passwords
* Web interface with flask and gunicorn. Heroku as deployment server.
* PyMuPDF as pdf tool. Regex for parsing text.
* Passport eye as mrz reader. OpenCV and scikit as image manupilation libraries. Also Nump as image/data processing


### How do I get set up? ###

* Install all dependencies inside requirement.txt
* To run on local web server run this: "gunicorn flaskMy:app --log-file -" or "python3 -m gunicorn flaskMy:app --log-file -"
* To run only the passport reader run IDReader.py. You can either edit default file name inside the code or pass a file as arguments
* To run PDF parser only on the local machine run main.py
* To deploy on heroku login with "heroku login" login from web interface. You can get the password and username from fiduce or me


### Who do I talk to? ###

* You contact me on github/canklot

### Notes ###
* You can print images in passport eye with this : 
skimage_io.imshow(img_small) 
skimage_io.show()

* You can print contourn in passport eye image.py with this function 

def plot_cont(img,contours):
# Display the image and plot all contours found
fig, ax = plt.subplots()

print("contours")
ax.imshow(img, cmap=plt.cm.gray)

if isinstance(contours, list):
    for contour in contours:
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
else:
    ax.plot(contours[:, 1], contours[:, 0], linewidth=2)
ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()