from extractTextFromPdf import extractTextFromPdf
from findBeneficiaire import findBeneficiaire

def findFileType(filename):
    # To determine if the file is sales contract or Passport like document
    # If the text version has beneficiare in it than its sales contract
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
    


