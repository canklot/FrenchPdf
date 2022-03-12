from unidecode import unidecode
from regex import regex

def findFeeAgency(normalText):
    myregex= r"(NEGOCIATION).{1,500}?\K\d[\d,\. ]+(€|(EUR))"
    uniCodetext = unidecode(normalText)
    regresult = regex.search(myregex,uniCodetext,flags=regex.DOTALL|regex.IGNORECASE)
    
    if regresult != None:
        fee = regresult.group()
        commaIndx = fee.find(",")
        fee = fee[:commaIndx]
        fee = fee.replace(" ","")
        fee = fee.replace(".","")
    else:
        fee = "Cant find"
    return fee

def findFeeNotary(normalText):
    # In file 5 when extracting text it goes to newline at this part. Need to order based on coordinates
    myregex= r"(cout).{0,500}?((frais.{0,50}?vente)|(provision sur))(.{0,95}?)\K\d[\d,\. ]{3,20}"
    uniCodetext = unidecode(normalText)
    regresult = regex.search(myregex,uniCodetext,flags=regex.DOTALL|regex.IGNORECASE)
    
    if regresult != None:
        fee = regresult.group()
        commaIndx = fee.find(",")
        fee = fee[:commaIndx]
        fee = fee.replace(" ","")
        fee = fee.replace(".","")
    else:
        fee = "Cant find"
    return fee