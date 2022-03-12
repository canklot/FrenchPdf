import re

def findBorrower1Adress(text):
    from findborrower1workerOrOwner import borrower1workerOrOwnerEnd
    shortText = text[borrower1workerOrOwnerEnd:borrower1workerOrOwnerEnd+150]
    regexAddressStart = "demeurant.*?à"
    # starts with demeurant, any charecter, until a 
    regexAddressEnd = ", *$|\. *$"
    # comma or dot  may have space at the end of line
    AddressStart=re.search(regexAddressStart,shortText,flags=re.DOTALL).span()[1]
    AddressEndLocal = re.search(regexAddressEnd,shortText,flags=re.MULTILINE|re.DOTALL).span()[0]
    AddressStr = shortText[AddressStart:AddressEndLocal]
    global AddressEnd 
    AddressEnd = AddressEndLocal+borrower1workerOrOwnerEnd
    
    # This method return string not re object like other functions
    return AddressStr.replace("\n"," ")
    