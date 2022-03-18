import re

def findBorrower2Married(text):
    from findBorrower1Nation import Borrower1NationEnd
    from findBorrower2Nation import Borrower2NationEnd
    shortText = text[Borrower1NationEnd:Borrower2NationEnd]
    
    regexCel = r"célibataire|celibataire"
    celibataire = re.search(regexCel,shortText,flags=re.IGNORECASE)
    if celibataire == None:
        return "Marie"
    else:
        return "Celibataire"