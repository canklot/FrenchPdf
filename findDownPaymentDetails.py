from dbm import dumb
import decimal
from distutils.spawn import spawn
import regex
from unidecode import unidecode
from decimal import Decimal

def findTotalAmount(normalText):
    # Use unidecode in every search. Turns out unicode flag is something diffirent :(
    unicodeText = unidecode(normalText)
    myregex = r"(C\s*O\s*U\s*T).{0,900}?((ENSEMBLE)|(Total))+?.{0,50}?\W{0,100}?\K\d[\d.:, ]+"
    regresult = regex.search(myregex,unicodeText,flags=regex.DOTALL|regex.IGNORECASE)
    
    if regresult != None:
        amount = regresult.group()
        amount = amount[:amount.find(",")]
        amount = amount.replace(".","")
        amount = amount.replace(" ","")
        amount = int(amount)
    else:
        amount = "Non trouve"
        
    print("Total amount: " + str(amount))
    return amount

def findMortgage(normalText):
    unicodeText = unidecode(normalText)
    myregex = r"(SUSPEN).{0,500}?((montant)|(maximal)|(maximum))+?.{0,200}?\K\d[\d\., ]+"
    myregex2 = r".{0,500}?((montant)|(maximal)|(maximum))+?.{0,200}?\K\d[\d\., ]+"
    # deleted |(pret)
    shortText = unicodeText[DurationEnd-999:DurationEnd+999] 
    regresult = regex.search(myregex2,shortText,flags=regex.DOTALL|regex.IGNORECASE)
    if regex != None:
        mortgage = regresult.group()
        mortgage = mortgage[:mortgage.find(",")]
        mortgage = mortgage.replace(".","")
        mortgage = mortgage.replace(" ","")
        mortgage = int(mortgage)
    else:
        mortgage = "Non trouve"
    
    print("Mortgage: " + str(mortgage))
    return mortgage

def findDownPaymentAndContruction(normalText):
    construction = 0
    # If negative save it as positive and say Aucun?
    TotalAmount = findTotalAmount(normalText)
    Mortgage = findMortgage(normalText)
    if isinstance(TotalAmount, int):
        if isinstance(Mortgage, int):
            Downpayment = TotalAmount-Mortgage
            if Downpayment < 0:
                construction = -1 * Downpayment
                Downpayment = 0
    else:
        Downpayment = "Non trouve"
    
    return {"Downpayment":Downpayment,"Construction":construction}

def findRate(normalText):
    # Can also add assurance. But In file 7 no assurance.
    unicodeText = unidecode(normalText)
    myregex1 = r"(SUSPEN).{0,900}?\K\d[\d,\.]*?\W*?%"
    myregex2 = r"(SUSPEN).{0,900}?TAUX.{0,100}?\K\d[\d,\.]*?\W*?%"
    #myregex3 = "((" + myregex2 + ")|( "+ myregex1 + "))+"
    myregex4 = r"\d[\d,\.]*?\W*?%"
    
    shortText = unicodeText[DurationEnd-999:DurationEnd+999]   
    regresult =  regex.search(myregex4,shortText,flags=regex.DOTALL|regex.IGNORECASE)

        
    if regresult != None:
        rate = regresult.group()
        rate = rate.replace("%","").strip()
        rate = rate.replace(",",".")
        rate = round(Decimal(rate), 2)
        # float has some weird behaviors they say use decimal they say
        rate = str(rate)+"%"
        
    else:
        rate = "Non trouve"
    return rate

def findDuration(normalText):
    
    unicodeText = unidecode(normalText)
    myregex = r"(Duree).{0,50}?\K\d{1,50}?\s{0,50}?\s*?((ans)|(mois))"
    regresult = regex.search(myregex,unicodeText,flags=regex.DOTALL|regex.IGNORECASE)
    
    if regresult != None:
        Duration = regresult.group()
        ansIndx = Duration.find("ans")
        if ansIndx > -1:
            Duration = Duration[:ansIndx]      
        elif Duration.find("mois") > -1:
            moisIndx = Duration.find("mois")
            Duration = Duration[:moisIndx].strip()
            # To remove mois at the end
            Duration = int(Duration)/12
            Duration = str(Duration)
            # Converts months to years
    else:
        Duration = "Non trouve"
    global DurationEnd 
    DurationEnd = regresult.span()[1]
    return Duration