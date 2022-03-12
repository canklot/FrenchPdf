from findBeneficiaire import findBeneficiaire
from findBorrower1Name import findBorrower1Name
import re

def findborrower2workerOrOwner(text):
    from findBeneficiaire import beneficiaireEnd
    from findBorrower2Name import Borrower2NameEnd        
    
    shortTextStart = Borrower2NameEnd  
    shortText = text[shortTextStart:shortTextStart+50]
    regex= ".*?,|\."
    # any charecter any long lazy ends with comma or dot.
    borrower2workerOrOwner = re.search(regex, shortText)
    global borrower2workerOrOwnerEnd 
    borrower2workerOrOwnerEnd = borrower2workerOrOwner.span()[1] + shortTextStart
    return borrower2workerOrOwner.group()