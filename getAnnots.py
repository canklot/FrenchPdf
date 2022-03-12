from pydoc import text
import fitz  # this is pymupdf
import os, sys
import contextlib

def getAnnots(filename):
    with fitz.open(filename) as pdf:
        #text =fitz.TextPage.extractText(pdf)
        textlist = []
        for page in pdf.pages(0,10):
            for annot in page.annots():
                textlist += annot
                # doesnt get inside the for I guess that means the page has no annots
            
            #textlist += page.get_text("dict")["blocks"]
    return textlist