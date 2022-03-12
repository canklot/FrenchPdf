import re

def findBorrower1Nation(text):
    from findBeneficiaire import beneficiaireEnd
    shortText = text[beneficiaireEnd:beneficiaireEnd+1000]
    
    word1="nationalité"
    word2 = "nationalite"
    nationaliteIndex = shortText.find(word1)
    if nationaliteIndex < 0:
        nationaliteIndex = shortText.find(word2)
    
    nationaliteIndex+= len(word1)
    textAfterNationalite = shortText[nationaliteIndex:].strip()
    
    regex= r"^([\w]+)"
    nation=re.search(regex,textAfterNationalite)
    global Borrower1NationEnd
    Borrower1NationEnd = nation.span()[1] + beneficiaireEnd + nationaliteIndex
    return nation.group()
    