import re
def findBorrower1Married(text):
    from findBorrower1Nation import Borrower1NationEnd
    from findBeneficiaire import beneficiaireEnd
    shortText= text[beneficiaireEnd:Borrower1NationEnd]
    regexCel = r"célibataire|celibataire"
    celibataire = re.search(regexCel,shortText,flags=re.IGNORECASE)
    if celibataire == None:
        return "Marie"
    else:
        return "Celibataire"