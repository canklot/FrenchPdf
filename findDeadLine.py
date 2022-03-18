import regex
from unidecode import unidecode
def findDeadLine(normalText):
    myregex = r"(La condition suspensive).{0,500}?(au plus tard le )\K\d+.*?\d{2,4}"
    # may need lazy
    unicodeNormalText = unidecode(normalText)
    deadLine = regex.search(myregex,unicodeNormalText,flags=regex.DOTALL|regex.IGNORECASE)
    
    if deadLine != None:
        deadLineDate = deadLine.group()
    else:
        deadLineDate = "Non trouve"
    
    return deadLineDate.replace("\n", "").strip()