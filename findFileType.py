from extractTextFromPdf import extractTextFromPdf
from findBeneficiaire import findBeneficiaire

def findFileType(filename):
    if filename[-3:]=="pdf":
        text = extractTextFromPdf(filename)
        beneficiare = findBeneficiaire(text)
        if beneficiare != "cant find":
            print("Contract")
            return "Contract"
        else :
            return "IdPass"
    else:
        print("IdPass")
        return "IdPass"
    


