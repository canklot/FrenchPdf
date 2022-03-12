""" import re
from searchDetailed import searchDetailed
from indexConverter import indexConvert
def findBeneficiaire(normalText,detailedText):
    #make new one with fonts
    regex = r"^BENEFICIAIRE+\s*$"
    regex2 = r"^BÉNÉFICIAIRE+\s*$" 
    regex3 = r"^ACQUEREUR+\s*$"
    # Starts with BENEFICIAIRE. After that might have spaces or not. And ends with new line. At least thats what I hope it does. Regex can be confusing
    # Also includes spaces at the end until encounters another charecter
    # I am not sure if its check the string starts with new line or not
    
    beneficiare = None
    if beneficiare == None:
        beneficiare = searchDetailed(detailedText,"BENEFICIAIRE","Bold")
    elif beneficiare == None:
        beneficiare = searchDetailed(detailedText,"BÉNÉFICIAIRE","Bold")
    elif beneficiare == None:
        beneficiare = searchDetailed(detailedText,"ACQUEREUR","Bold")
    elif beneficiare == None:
        raise ValueError('Cant find BENEFICIAIRE')
    
    benIndx = beneficiare.span()[1]
    benIndx = indexConvert (benIndx,normalText)
    global beneficiaireEnd
    beneficiaireEnd = benIndx
    
    return beneficiare """