import extractTextFromPdf
import findBeneficiaire

def findFileTyple(filename):
    if fileName[-3:]=="pdf":
        text = extractTextFromPdf(filename)
        beneficiare = findBeneficiaire(text)
        if beneficiare != None:
            return "Contract"
    else:
        return "IdPass"
    

