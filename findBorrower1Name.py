from findBeneficiaire import findBeneficiaire
import re

def findBorrower1Name(text):
    findBeneficiaire(text) # To change beneficiaireEnd
    from findBeneficiaire import beneficiaireEnd
    shortText = text[beneficiaireEnd:beneficiaireEnd+50]
    # random length doesnt sound very nice
    # print(shortText)
    
    madameEndIndx = shortText.rfind("Madame")
    monsieurEndIndx = shortText.rfind("Monsieur")
    # Search Monsieur after beneficiar until after xx charecter. Return -1 if Non trouve
    
    regexBeforeAfterMadame = r'(?<=Madame).*?(?=,)'
    #has Madame before, any charecters lazy, has comma at the end (Coma doesnt included)
    regexBeforeAfterMonsieur = r'(?<=Monsieur).*?(?=,)'
    
    if(madameEndIndx>0):
        borrower1Name = re.search(regexBeforeAfterMadame, shortText, flags=re.IGNORECASE)
    elif(monsieurEndIndx>0):
        borrower1Name = re.search(regexBeforeAfterMonsieur, shortText, flags=re.IGNORECASE)
    else:
        print("Non trouve name madame or monieur")
    global borrower1NameEnd
    borrower1NameEnd = borrower1Name.span()[1]
    return borrower1Name