import regex

def findPropType(normalText):
    myregex = r"(DESIGNATION).{1,200}\K((Maison)|(ensemble immobilier)|(pavillon)|(immeuble))"
    myregex2 = r"((DESIGNATION)|(D E S I G N A T I O N)).{1,200}\K((Maison)|(ensemble immobilier)|(pavillon)|(immeuble))"
    regresult = regex.search(myregex2,normalText,flags=regex.DOTALL|regex.IGNORECASE)
    if(regresult!=None):
        propType = regresult.group()
    else:
        propType = "Non trouve"
    
    if propType.lower()== "immeuble":
        propType="Immeuble"
    elif propType.lower()== "pavillon":
        propType="Maison"
    elif propType.lower()== "ensemble immobilier":
        propType="Appartement"
        
    return propType