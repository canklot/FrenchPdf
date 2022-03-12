import re

def findBorrowerOnePlaceOfBirth(text):
    from findBorrower1Adress import AddressEnd
    shortText= text[AddressEnd:AddressEnd+150]
    regexStart = "Né.*?à"
    regexEnd = "le"
    placeOfBirthStart = re.search(regexStart,shortText,flags=re.DOTALL|re.IGNORECASE).span()[1]
    shorterText=shortText[placeOfBirthStart:]
    placeOfBirthEndLocal = re.search(regexEnd,shorterText,flags=re.DOTALL|re.IGNORECASE).span()[0]
    placeOfBirthStr = shorterText[:placeOfBirthEndLocal]
    global placeOfBirthEnd
    diff= len(shortText)-len(shorterText)
    placeOfBirthEnd = placeOfBirthEndLocal + AddressEnd +diff +len(regexEnd)
    return placeOfBirthStr.replace("\n"," ")
