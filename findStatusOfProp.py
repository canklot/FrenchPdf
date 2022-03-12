import regex
from unidecode import unidecode


def findStatusOfProp(normalText):
    
    UnicodeNormalText = unidecode(normalText)
    firstSearch = UnicodeNormalText.find("VENTE EN L'ETAT FUTUR")
    secondSearch = UnicodeNormalText.find("contrat de reservation")
    
    if firstSearch > 0 or secondSearch > 0:
        return "Neuf"
    else:
        return "Ancien"