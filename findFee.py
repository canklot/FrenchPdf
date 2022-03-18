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
        fee = "Non trouve"
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
        fee = "Non trouve"
    return fee

def findWhoWillPay(normalText):
    unicodetext = unidecode(normalText)
    regexBuyer = r"((N\s*E\s*G\s*O\s*C\s*I\s*A\s*T\s*I\s*O\s*N)|(C\s*O\s*M\s*M\s*I\s*S\s*S\s*I\s*O\s*N\s*D\s*’*?\s*A\s*G\s*E\s*N\s*C\s*E))(.{0,500})(BENEFICIAIRE)"
    regexBuyerSmall = r"((N\s*E\s*G\s*O\s*C\s*I\s*A\s*T\s*I\s*O\s*N)|(C\s*O\s*M\s*M\s*I\s*S\s*S\s*I\s*O\s*N\s*D\s*’*?\s*A\s*G\s*E\s*N\s*C\s*E))(.{0,500})(?i:BENEFICIAIRE)"
    # or charge du beneficiaire. for file 10
    regSeller =  r"((N\s*E\s*G\s*O\s*C\s*I\s*A\s*T\s*I\s*O\s*N)|(C\s*O\s*M\s*M\s*I\s*S\s*S\s*I\s*O\s*N))(.{0,500})((PROMETTANT)|(VENDEUR))"

    regResultBuyer = regex.search(regexBuyer,unicodetext,flags=regex.DOTALL)
    regREsultSeller = regex.search(regSeller,unicodetext,flags=regex.DOTALL)
    regResultBuyerSmall = regex.search(regexBuyerSmall,unicodetext,flags=regex.DOTALL)
    if regResultBuyer != None:
        return "buyer"
    elif regREsultSeller != None:
        return "seller"
    elif regResultBuyerSmall != None:
        return "buyer"
    else: 
        return "Non trouve"

def findWhoWillPayOld(normalText):
    uniCodetext = unidecode(normalText)
    buyerKeywords = ["frais de négociation à la charge du bénéficiaire",
                    "le bénéficiaire qui en aura seul la charge, s'oblige à verser une rémunération toutes taxes comprises de",
                    "le bénéficiaire à titre d'honoraires de négociation",
                    "le bénéficiaire qui en a seul la charge au terme du mandat doit à l'agence une rémunération de",
                    "le bénéficiaire qui en a seul la charge au terme du mandat doit à l'agence une rémunération toutes taxes comprises de"
                    "Le bénéficiaire qui en a seul la charge aux termes du mandat"]

    sellerKeywords = ["frais de négociation à la charge de l'acquéreur",
                    "l'acquéreur qui en aura seul la charge, s'oblige à verser une rémunération toutes taxes comprises de",
                    "l'acquéreur à titre d'honoraires de négociation",
                    "l'acquéreur qui en a seul la charge au terme du mandat doit à l'agence une rémunération de",
                    "l'acquéreur qui en a seul la charge au terme du mandat doit à l'agence une rémunération toutes taxes comprises de"]
    buyerKeywords = [unidecode(x) for x in buyerKeywords]
    sellerKeywords = [unidecode(x) for x in sellerKeywords]

    for sentence in buyerKeywords:     
        if sentence in normalText.lower():
            return "buyer"
    for sentence in sellerKeywords:     
        if sentence in normalText.lower():
            return "seller"
    
    return "Non trouve"

