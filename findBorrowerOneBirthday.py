import re

def findBorrowerOneBirthday(text):
    from findBorrowerOnePlaceOfBirth import placeOfBirthEnd
    shortText= text[placeOfBirthEnd:placeOfBirthEnd+150]
    regexEnd = "\.|,"
    birthdayEndLocal = re.search(regexEnd,shortText,flags=re.DOTALL|re.IGNORECASE).span()[1]
    birthdayStr = shortText[:birthdayEndLocal]
    birthdayEnd=birthdayEndLocal+placeOfBirthEnd
    return birthdayStr.replace("\n"," ")
    