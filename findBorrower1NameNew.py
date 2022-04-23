import re
from searchDetailed import searchDetailed
from indexConverter import indexConvert
from findBeneficiaire import findBeneficiaire

def findBorrower1NameNew(normalText,DetailedText):
    beneficiaireEnd = findBeneficiaire(normalText).span()[1]
    textToBeneficiare = normalText[:beneficiaireEnd]
    newlineCount =  textToBeneficiare.count("\n")
    start = beneficiaireEnd - newlineCount + 3
    firstBold = searchDetailed(DetailedText,None,"Bold",start)[1]
    convertedFirstBoldEnd = indexConvert(firstBold,normalText)
    # index from search with fonts and normal search are different because they count new line charecter diffirently
    textToFirstboldEnd= normalText[:convertedFirstBoldEnd]
    
    shortText  = normalText[beneficiaireEnd:convertedFirstBoldEnd]
    
    pronounList = ["Madame","Monsieur","Mademoiselle"]
    for noun in pronounList:
        
        NounIndx= shortText.find(noun)
        # Need Monsieur and matmazel
        if NounIndx >0:
            NounIndx += len(noun)
            shortEnd =  convertedFirstBoldEnd +NounIndx
            Borrower1Name = shortText[NounIndx:shortEnd]
    
    global Borrower1NameEnd
    
    Borrower1NameEnd = convertedFirstBoldEnd
    return Borrower1Name