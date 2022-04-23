import re
from searchDetailed import searchDetailed
from indexConverter import indexConvert

def findBorrower2Name(normalText,DetailedText):
    from findBeneficiaire import beneficiaireEnd
    textToBeneficiare = normalText[:beneficiaireEnd]
    newlineCount =  textToBeneficiare.count("\n")
    start = beneficiaireEnd - newlineCount + 3
    # +3 to pass new line and space chars?
    firstBold = searchDetailed(DetailedText,None,"Bold",start)[1]
    convertedFirstBoldEnd = indexConvert(firstBold,normalText)
    textToFirstboldEnd= normalText[:convertedFirstBoldEnd]
    textAfterBorrower1Name = normalText[convertedFirstBoldEnd:]
    
    secondBoldEnd= searchDetailed(DetailedText,None,"Bold",firstBold+10)[1]
    convertedSecondBoldEnd = indexConvert(secondBoldEnd,normalText)
    textToSecondBoldEnd = normalText[:convertedSecondBoldEnd]
    
    shortText  = normalText[convertedFirstBoldEnd:convertedSecondBoldEnd]
    
    pronounList = ["Madame","Monsieur","Mademoiselle"]
    for noun in pronounList:
        
        NounIndx= shortText.rfind(noun)
        # Need Monsieur and matmazel
        if NounIndx >0:
            NounIndx += len(noun)
            shortEnd = convertedSecondBoldEnd - convertedFirstBoldEnd +NounIndx
            Borrower2Name = shortText[NounIndx:shortEnd]
            
    global Borrower2NameEnd
    Borrower2NameEnd =convertedSecondBoldEnd
    return Borrower2Name
    
    