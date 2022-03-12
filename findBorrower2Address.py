import re

def findBorrower2Address(text):
    from findBeneficiaire import beneficiaireEnd
    shortText = text[beneficiaireEnd:beneficiaireEnd+999]
    regexAddressStart =  r"(demeurant.*?à)(?![\s\S]*(demeurant.*?à))"
    AddressStart = re.search(regexAddressStart,shortText,flags=re.DOTALL).span()[1]
    #return last occurance of "demeurant.*?à" Use regex101 for explanation
    shorterText = shortText[AddressStart:]
    regexAddressEnd = ", *$|\. *$"
    AddressEndLocal = re.search(regexAddressEnd,shorterText,flags=re.MULTILINE|re.DOTALL).span()[1]
    
    AddressStr = shorterText[:AddressEndLocal]
    #global Borrower2AddressEnd 
    #Borrower2AddressEnd = AddressEndLocal+beneficiaireEnd
    
    return AddressStr.replace("\n"," ")