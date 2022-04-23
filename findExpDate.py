import regex
from unidecode import unidecode

def findExpDate(normalText):
    # exactly four
    myregex= r"(expirant).{1,100}((le )|(a ))\K\d{1,4}.{1,20}\d+"
    uniCodetext = unidecode(normalText)
    regresult = regex.search(myregex,uniCodetext,flags=regex.DOTALL|regex.IGNORECASE)
    
    if regresult == None:
        myregex3 = r"((REGULARISATION)).{1,999}?(AU PLUS TARD LE )\K\d{1,4}.{1,20}\d{4}"
        regresult = regex.search(myregex3,uniCodetext,flags=regex.DOTALL|regex.IGNORECASE)
    if regresult != None:
        expDate =regresult.group()
        expDate = expDate.replace("\n"," ").strip()
    else:
        expDate ="Non trouve"
    return expDate
    