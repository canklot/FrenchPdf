from site import removeduppaths
import fitz  # this is pymupdf
import os, sys
import contextlib
import collections
from operator import itemgetter

def DuplicateRemover(mylist):
    mylist = list(dict.fromkeys(mylist))
    return mylist

def extractTextFromPdf(filename):
    with open(os.devnull, "w") as f, contextlib.redirect_stderr(f):
    # Preventing error messages by redirecting stderr
    # Because I keep getting "mupdf: kid not found in parent's kids array" but the code still works
    # The reason is some pdf fls has scan documents in it
        with fitz.open(filename) as pdf:
            text =""
            #for page in pdf.pages(0,15):
            for page in pdf.pages():
                # Firt ten pages
                text += page.get_text()
            
    with open(filename+" extracted.txt",'w',encoding = 'utf-8') as file:
        file.write(text)
        
    return text

def extractTextFromPdfWords(filename):
    with open(os.devnull, "w") as f, contextlib.redirect_stderr(f):
    # Preventing error messages by redirecting stderr
    # Because I keep getting "mupdf: kid not found in parent's kids array" but the code still works
    # The reason is some pdf fls has scan documents in it
        with fitz.open(filename) as pdf:
            words =[]
            text = ""
            #for page in pdf.pages(0,15):
            for page in pdf.pages():
                # Firt ten pages
                words += page.get_text("words")
        for word in words:
            text += word[4] 
    #with open(filename+" extracted.txt",'w',encoding = 'utf-8') as file:
        #file.write(text)
        
    return text

def extractTextFromPdfOrdered(filename):
    with open(os.devnull, "w") as f, contextlib.redirect_stderr(f):
    # Preventing error messages by redirecting stderr
    # Because I keep getting "mupdf: kid not found in parent's kids array" but the code still works
    # The reason is some pdf fls has scan documents in it
    
    # if span bbx is local than sum with block bbox 
        with fitz.open(filename) as pdf:
            text =""
            mylist = []
            spans = []
            indx=0
            for page in pdf.pages():
                mylist += page.get_text("dict")["blocks"]
                for paragraph in mylist:
                    if 'lines' not in paragraph:
                        continue
                    for line in paragraph["lines"]:
                        for span in line["spans"]:
                            spans.append(span)
                            debtext = span["text"]
                            #if "conforme du" in debtext:
                            #    print("debugee")
                            
                            #if "730" in span["text"]: print("debug point")
                            #text += span["text"]
            
    #with open(filename+" extracted.txt",'w',encoding = 'utf-8') as file:
        #file.write(text)
    
    onlyTextAndBbox30 = []
    
    for span in spans:
        onlyTextAndBbox30.append(list((span["text"],span["bbox"][3],span["bbox"][0]))) 
        if "pouvant grever" in span["text"]:print(span["text"])
    spansnodup = [dict(t) for t in {tuple(d.items()) for d in spans}]
    #spanitems = spans.items()
    #sortedspans =sorted(spans, key=lambda student: student["bbox"][3])
    sortedspans = sorted(spansnodup, key=lambda k: (k["bbox"][3],k["bbox"][0]))
    #spans.sort(key=lambda b: (b["bbox"][0]))
    for span in sortedspans:

        text += span["text"]
    return text