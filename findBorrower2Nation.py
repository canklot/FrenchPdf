import re

def findBorrower2Nation(text):
    from findBorrower1Nation import Borrower1NationEnd
    shortText = text[Borrower1NationEnd:Borrower1NationEnd+1000]
    
    word1="nationalité"
    word2 = "nationalite"
    nationaliteIndex = shortText.find(word1)
    if nationaliteIndex < 0:
        nationaliteIndex = shortText.find(word2)
        
    nationaliteIndex+= len(word1)
    textAfterNationalite = shortText[nationaliteIndex:].strip()
    
    regex= r"^([\w]+)"
    nation=re.search(regex,textAfterNationalite)
    global Borrower2NationEnd
    Borrower2NationEnd = nation.span()[1]+nationaliteIndex+Borrower1NationEnd
    return nation.group()