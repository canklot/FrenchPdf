import regex
from searchDetailed import searchDetailed
from indexConverter import indexConvert
from unidecode import unidecode

def findPropAddress(normalText,detailedText):
    unicodeText = unidecode(normalText)
    RegexLieudit = r"Lieudit.{1,90}ca"
    LieuditIndx = regex.search(RegexLieudit,unicodeText,flags=regex.MULTILINE|regex.DOTALL|regex.IGNORECASE).span()[0]
    TextNearLieudit= unicodeText[LieuditIndx-999:LieuditIndx+100]
    DesignationIndx = TextNearLieudit.lower().find("designation")
    if DesignationIndx == -1: DesignationIndx = TextNearLieudit.lower().find("d e s i g n a t i o n")
    # Sometimes titles can have spaces between letter. So if normal search fails try again with spaces
    TextDesignationToLieudit = TextNearLieudit[DesignationIndx:]
    myregex = r"((\bde\b)|(\ba\b)|(situe))(\K)(.{1,40}?)(\d{5})(.{1,100}?)[\.,»>]\s*?$"
    regresult = regex.search(myregex,TextDesignationToLieudit,flags=regex.MULTILINE|regex.DOTALL|regex.IGNORECASE)
    if regresult != None:
        propAddress = regresult.group()
        propAddress = propAddress.replace("\n"," ")
    else:
        propAddress = "Non trouve"
    return propAddress
