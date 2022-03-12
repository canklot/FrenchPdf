import re

def findBorrower2PlaceOfBirth(text):
    from findBorrowerOnePlaceOfBirth import placeOfBirthEnd as Borrower1placeOfBirthEnd
    shortText= text[Borrower1placeOfBirthEnd:Borrower1placeOfBirthEnd+800]
    
    regexStart = r"Né.{0,4}? à"
    start= re.search(regexStart,shortText,flags=re.DOTALL|re.IGNORECASE).span()[1]
    
    shorterText = shortText[start:]
    regexEnd = "le"
    
    end = re.search(regexEnd,shorterText,flags=re.DOTALL|re.IGNORECASE).span()[0]
    place = shorterText[:end]
    
    global Borrower2PlaceOfBirthEnd
    global Borrower2PlaceOfBirthStart
    
    Borrower2PlaceOfBirthStart = Borrower1placeOfBirthEnd +start
    Borrower2PlaceOfBirthEnd = Borrower1placeOfBirthEnd +start + end 
    return place.strip()
    