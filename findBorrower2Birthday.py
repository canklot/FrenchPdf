import re

def findBorrower2Birthday(text):
    from findBorrower2PlaceOfBirth import Borrower2PlaceOfBirthEnd
    shortText= text[Borrower2PlaceOfBirthEnd:Borrower2PlaceOfBirthEnd+100]
    regexEnd = "\.|,"
    birthdayEndLocal = re.search(regexEnd,shortText,flags=re.DOTALL|re.IGNORECASE).span()[1]
    birthdayStr = shortText[2:birthdayEndLocal]
    birthdayEnd=birthdayEndLocal+Borrower2PlaceOfBirthEnd
    return birthdayStr.replace("\n"," ")