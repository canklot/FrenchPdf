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

def findWhoWillPay(normalText):
    uniCodetext = unidecode(normalText)
    buyerKeywords = ["frais de négociation à la charge du bénéficiaire",
                    "le bénéficiaire qui en aura seul la charge, s'oblige à verser une rémunération toutes taxes comprises de",
                    "le bénéficiaire à titre d'honoraires de négociation",
                    "le bénéficiaire qui en a seul la charge au terme du mandat doit à l'agence une rémunération de",
                    "le bénéficiaire qui en a seul la charge au terme du mandat doit à l'agence une rémunération toutes taxes comprises de"]
    sellerKeywords = ["frais de négociation à la charge de l'acquéreur",
                    "l'acquéreur qui en aura seul la charge, s'oblige à verser une rémunération toutes taxes comprises de",
                    "l'acquéreur à titre d'honoraires de négociation",
                    "l'acquéreur qui en a seul la charge au terme du mandat doit à l'agence une rémunération de",
                    "l'acquéreur qui en a seul la charge au terme du mandat doit à l'agence une rémunération toutes taxes comprises de"]
    buyerKeywords = unidecode(buyerKeywords)
    sellerKeywords = unidecode(sellerKeywords)

    if buyerKeywords in normalText:
        return "buyer"
    elif sellerKeywords in normalText:
        return "seller"
    else:
        return "cant find"

