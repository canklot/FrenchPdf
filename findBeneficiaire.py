import re
from searchDetailed import searchDetailed
from indexConverter import indexConvert

def findBeneficiaire(text):
     #make new one with fonts
    myregex1 = r"^BENEFICIAIRE+\s*$"
    myregex2 = r"^BÉNÉFICIAIRE+\s*$" 
    myregex3 = r"^ACQUEREUR+\s*$"
    # Starts with BENEFICIAIRE. After that might have spaces or not. And ends with new line. At least thats what I hope it does. Regex can be confusing
    # Also includes spaces at the end until encounters another charecter
    # I am not sure if its check the string starts with new line or not
    myregexlist = [myregex1,myregex2,myregex3]
    smalBen = None
    bignum = 999999999
    benindx = bignum
    for myregex in myregexlist:
        beneficiare=re.search(myregex, text, flags=re.IGNORECASE|re.MULTILINE)
        if beneficiare != None:
            if beneficiare.span()[0] < benindx:
                smalben = beneficiare
                benindx = beneficiare.span()[0]
    if benindx == bignum:
        raise ValueError('Non trouve BENEFICIAIRE')
    
    global beneficiaireEnd
    beneficiaireEnd = smalben.span()[1]
    
    return smalben

def oldfindBeneficiaire(text):
    #make new one with fonts. Dont it doesnt work LoL
    # Make this a list 
    myregex1 = r"^BENEFICIAIRE+\s*$"
    myregex2 = r"^BÉNÉFICIAIRE+\s*$" 
    myregex3 = r"^ACQUEREUR+\s*$"
    myregexlist = [myregex1,myregex2,myregex3]
    # Starts with BENEFICIAIRE. After that might have spaces or not. And ends with new line. At least thats what I hope it does. Regex can be confusing
    # Also includes spaces at the end until encounters another charecter
    # I am not sure if its check the string starts with new line or not
    
    benindx = 999999999
    for myregex in myregexlist:
        beneficiare=re.search(myregex, text, flags=re.IGNORECASE|re.MULTILINE)
        if beneficiare != None:
            if beneficiare.span()[0] < benindx:
                benindx = beneficiare.span()[0]
    if beneficiare == None:
        raise ValueError('Non trouve BENEFICIAIRE')
    
    global beneficiaireEnd
    beneficiaireEnd = beneficiare.span()[1]
    
    return beneficiare

def oldfindBenFonts(normalText,detailedText):
    #make new one with fonts
    regex = r"^BENEFICIAIRE+\s*$"
    regex2 = r"^BÉNÉFICIAIRE+\s*$" 
    regex3 = r"^ACQUEREUR+\s*$"
    # Starts with BENEFICIAIRE. After that might have spaces or not. And ends with new line. At least thats what I hope it does. Regex can be confusing
    # Also includes spaces at the end until encounters another charecter
    # I am not sure if its check the string starts with new line or not
    
    # There are many bold beneficiare  regex is better
    beneficiare = None
    if beneficiare == None:
        beneficiare = searchDetailed(detailedText,"BENEFICIAIRE","Bold")
    elif beneficiare == None:
        beneficiare = searchDetailed(detailedText,"BÉNÉFICIAIRE","Bold")
    elif beneficiare == None:
        beneficiare = searchDetailed(detailedText,"ACQUEREUR","Bold")
    elif beneficiare == None:
        raise ValueError('Non trouve BENEFICIAIRE')
    
    benIndx = beneficiare[1]
    benIndx = indexConvert (benIndx,normalText)
    global beneficiaireEnd
    beneficiaireEnd = benIndx
    
    return beneficiare