import regex
# re module doesnt support \k


def findPrice(normalText):
    myregex = r"\d+.*€|\d+.*EUR|\d+.*\$"
    myregex2 = r"(?<=PRIX).*?\K\d+.*?€"
    myregex3 = r"(?<=PRIX).*?\K[\d,\.]+€"
    myregex4= r"(?<=PRIX).*?\K[\d,\. ]+€"
    myregex5 = r"(?<=PRIX).*?\K\d[\d,\. ]+(€|(EUR))"
    myregex6 = r"(?<=\nPRIX).*?\K\d[\d,\. ]+(€|(EUR))"
    myregex7 = r"(?<=\n(PRIX)|(P R I X)).*?\K\d[\d,\. ]+(€|(EUR))"
    myregex8 = r"(?<=\n(PRIX)|(P R I X)).{1,500}?\K\d[\d,\. ]+(€|(EUR))"
    # Has newline and PRIX or P R I X and go max 500 chars until you see a digit. Clear selection. Capture digit comma dots spaces until € or(EUR 
    # When using regex101 need to use \\n
    regresult = regex.search(myregex8,normalText,flags=regex.DOTALL)
    
    if regresult != None:
        price = regresult.group()
        commaIndx = price.find(",")
        price = price[:commaIndx]
        price = price.replace(" ","")
        price = price.replace(".","")
    else:
        fee = "Cant find"
    
    return price