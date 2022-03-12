from findBeneficiaire import findBeneficiaire
from findBorrower1Name import findBorrower1Name
import re

def findborrower1workerOrOwner(text):
    from findBeneficiaire import beneficiaireEnd
    from findBorrower1NameNew import Borrower1NameEnd        
    
    shortTextStart = Borrower1NameEnd  
    shortText = text[shortTextStart:shortTextStart+50]
    regex= ".*?,|\."
    # any charecter any long lazy ends with comma or dot.
    borrower1workerOrOwner = re.search(regex, shortText)
    global borrower1workerOrOwnerEnd 
    borrower1workerOrOwnerEnd = borrower1workerOrOwner.span()[1] + shortTextStart
    return borrower1workerOrOwner