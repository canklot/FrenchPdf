import fitz  # this is pymupdf
import os, sys
import contextlib

def extractTextFromPdfWithFonts(filename):
    with open(os.devnull, "w") as f, contextlib.redirect_stderr(f):
        with fitz.open(filename) as pdf:
            #text =fitz.TextPage.extractText(pdf)
            textlist = []
            for page in pdf.pages():
                # Firt ten pages
                textlist += page.get_text("dict")["blocks"]
    return textlist