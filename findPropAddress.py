import regex
from searchDetailed import searchDetailed
from indexConverter import indexConvert
from unidecode import unidecode

def findPropAddress(normalText,detailedText):
    unicodeText = unidecode(normalText)
    #LieuditIndx = unicodeText.lower().find("lieudit")
    RegexLieudit = r"Lieudit.{1,90}ca"
    LieuditIndx = regex.search(RegexLieudit,unicodeText,flags=regex.MULTILINE|regex.DOTALL|regex.IGNORECASE).span()[0]
    TextNearLieudit= unicodeText[LieuditIndx-999:LieuditIndx+100]
    DesignationIndx = TextNearLieudit.lower().find("designation")
    if DesignationIndx == -1: DesignationIndx = TextNearLieudit.lower().find("d e s i g n a t i o n")
    TextDesignationToLieudit = TextNearLieudit[DesignationIndx:]
    myregex = r"((\bde\b)|(\ba\b)|(situe))(\K)(.{1,40}?)(\d{5})(.{1,100}?)[\.,»>]\s*?$"
    regresult = regex.search(myregex,TextDesignationToLieudit,flags=regex.MULTILINE|regex.DOTALL|regex.IGNORECASE)
    if regresult != None:
        propAddress = regresult.group()
        propAddress = propAddress.replace("\n"," ")
    else:
        propAddress = "Non trouve"
    return propAddress










            
def findPropAddressOld(normalText,detailedText):
    unicodeText = unidecode(normalText)
    designStartDetailed = searchDetailed(detailedText,"designation","Bold")[1]
    designStartNormal = indexConvert(designStartDetailed,normalText)
    shortText = unicodeText[designStartNormal:designStartNormal+250]
    
    starterList = [" situe "," situee "," a "," de "]
    
    startIndx = -1
    startWord = None
    for word in starterList:
        wordIndx = shortText.find(word)
        if wordIndx != -1:
            if wordIndx > startIndx:
                startWord = word
                startIndx = wordIndx + len(startWord)
        
    textAfterStart = shortText[startIndx:] 
    
    regexEnd =  ", *?\\n|\. *?\\n"  
    # Dot or comma at the end of line
    endIndx = regex.search(regexEnd,textAfterStart,flags=regex.MULTILINE).span()[0]
    
    propAddress = textAfterStart[:endIndx]
    propAddress = propAddress.replace("\n"," ")
    return propAddress

def findPropAddressold2(normalText,detailedText):
    # Either detailed search or index converter has problems. Returns a little more than it should return
    unicodeText = unidecode(normalText)
    lieuditIndx = unicodeText.lower().find("lieudit")
    #shortTextLieudit = unicodeText[lieuditIndx-500+lieuditIndx+300]
    texttoLieudit = unicodeText[:lieuditIndx]
    searchstart = texttoLieudit.count("\n")+lieuditIndx
    designStartDetailed = searchDetailed(detailedText,"designation","Bold",searchstart-3000)[1]
    designStartNormal = indexConvert(designStartDetailed,normalText)
    shortText = unicodeText[designStartNormal-50:designStartNormal+250]
    myregex = r"(D\s*?E\s*?S\s*?I\s*?G\s*?N\s*?A\s*?T\s*?I\s*?O\s*?N)(.*?)((\Wde\W)|(\Wa\W)|(situe))+?(\K)(.{1,40}?)(\d)(.*?)[\.\,\»]$"
    regresult = regex.search(myregex,shortText,flags=regex.MULTILINE|regex.DOTALL|regex.IGNORECASE)
    
    starterList = ["situe"," a "," de "]
    wordindx = -2
    smallestWord = None
    smallestindx = 999999999
    
    while wordindx != -1:
        for word in starterList:
            if wordindx < smallestindx:
                if regresult != None:
                    wordindx = regresult.group().find(word)
                    smallestWord = word
        if smallestWord !=None:
            shortText = shortText.replace(smallestWord,"")        
        regresult = regex.search(myregex,shortText,flags=regex.MULTILINE|regex.DOTALL|regex.IGNORECASE)
        
    
            
    
    if regresult != None:
        propAddress = regresult.group()
    else:
        propAddress = "Non trouve"
    
    return propAddress

