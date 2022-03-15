from extractTextFromPdf import extractTextFromPdf, extractTextFromPdfWords
from findBorrower2Nation import findBorrower2Nation
from findborrower1workerOrOwner import findborrower1workerOrOwner
from findBorrower1Adress import findBorrower1Adress
from findBorrowerOnePlaceOfBirth import findBorrowerOnePlaceOfBirth
from findBorrowerOneBirthday import findBorrowerOneBirthday
from countBorrowers import countBorrowers
from findBorrower2PlaceOfBirth import findBorrower2PlaceOfBirth
from findBorrower2Birthday import findBorrower2Birthday
from extractTextFromPdfWithFonts import extractTextFromPdfWithFonts
from findBorrower2Name import findBorrower2Name
from findBorrower1Nation import findBorrower1Nation
from findBorrower1NameNew import findBorrower1NameNew
from findBorrower2Address import findBorrower2Address
from findBorrower1Married import findBorrower1Married
from findBorrower2Married import findBorrower2Married
from findBorrower2WorkerOrOwner import findborrower2workerOrOwner
from findPrice import findPrice
from excelFiller import exceFill , exceFillerBorrower2
from findPropType import findPropType
from findPropAddress import findPropAddress
from findStatusOfProp import findStatusOfProp
from findDeadLine import findDeadLine
from findExpDate import findExpDate
from findDownPaymentDetails import findDownPaymentAndContruction, findRate,findDuration,findMortgage
from findFee import findFeeAgency,findFeeNotary ,findWhoWillPay
import re
import sys

from searchDetailed import searchDetailed


def main(pdfname):
    #extracted = extractTextFromPdf("./pdf_files/"+pdfname+".pdf")
    #extractedDetailed = extractTextFromPdfWithFonts("./pdf_files/"+pdfname+".pdf")
    extracted = extractTextFromPdf("./uploads/"+pdfname)
    extractedDetailed = extractTextFromPdfWithFonts("./uploads/"+pdfname)
    # Call print with functions and reduce lines. Also strip before return
    #Borrower1Name = findBorrower1Name(extracted).group()
    Borrower1Name = findBorrower1NameNew(extracted,extractedDetailed)
    Borrower1Job = findborrower1workerOrOwner(extracted).group()[:-1] #removing comma
    Borrower1Adress = findBorrower1Adress(extracted)
    Borrower1PlaceOfBirth = findBorrowerOnePlaceOfBirth(extracted)
    Borrower1Birthday = findBorrowerOneBirthday(extracted)
    Borrower1Nation = findBorrower1Nation(extracted)
    Borrower1Married = findBorrower1Married(extracted)
    PropPice = findPrice(extracted)
    propType = findPropType(extracted)
    PropStatus = findStatusOfProp(extracted)
    Deadline = findDeadLine(extracted)
    ExpretionDate = findExpDate(extracted)
    Duration = findDuration(extracted)
    IntRate = findRate(extracted)
    mortgage= findMortgage(extracted)
    whoWillPay = findWhoWillPay(extracted)
    if findWhoWillPay == "buyer":
        FeeAgency =findFeeAgency(extracted)
        FeeNotary = findFeeNotary(extracted)
    elif findWhoWillPay == "seller":
        FeeAgency = "sera a la charge du vendeur"
        FeeNotary = "sera a la charge du vendeur"
    BorrowerCount = countBorrowers(extracted)
    propAddress =  findPropAddress(extracted,extractedDetailed)
    # list, text,font
    print("----------------------------------------------------\n")
    print("Borrower 1 Name: " + Borrower1Name.strip("., "))
    print("Borrower 1 Address: " + Borrower1Adress.strip("., "))
    print("Borrower 1 Birthday: "+ Borrower1Birthday.strip("., "))
    print("Borrower 1 Place of Birth: "+ Borrower1PlaceOfBirth.strip("., "))
    print("Borrower 1 Nation: " + Borrower1Nation.strip("., "))
    print("borrower 1 Married: " + Borrower1Married.strip("., "))
    print("Borrower 1 Job: " + Borrower1Job.strip("., "))
    print("Borrower count: "+ str(BorrowerCount))
    print("\n")
    print("Prop Price: " + PropPice.strip("., "))
    print("Prop Type: " + propType)
    print("Prop status: " + PropStatus)
    print("Deadline: " + Deadline)
    print("Expiration date: " + ExpretionDate)
    DownPaymentAndContruction = findDownPaymentAndContruction(extracted)
    Downpayment =  DownPaymentAndContruction["Downpayment"]
    Contruction = DownPaymentAndContruction["Construction"]
    print("Down payment: " + str(Downpayment).strip("., "))
    print("Contruction: " + str(Contruction).strip("., "))
    print("Interest rate: " + IntRate )
    print("Duration: " + Duration)
    print("Fee Agency: " + FeeAgency)
    print("Fee Notatary: " + FeeNotary)
    print("Prop Address: " +propAddress)
    
    
    
    
    paramsDict1 = {"Borrower1Name":Borrower1Name,"Borrower1Adress":Borrower1Adress,"Borrower1Birthday":Borrower1Birthday,
                    "Borrower1PlaceOfBirth":Borrower1PlaceOfBirth,"Borrower1Nation":Borrower1Nation,"Borrower1Married":Borrower1Married,
                    "Borrower1Job":Borrower1Job,
                    "PropPice":PropPice,"Downpayment":Downpayment,"mortgage":mortgage,"FeeAgency":FeeAgency,"FeeNotary":FeeNotary,
                    "propAddress":propAddress,"propType":propType,"PropStatus":PropStatus
                    }

    #exceFill("template.xls",Borrower1Name,Borrower1Adress,Borrower1Birthday,Borrower1PlaceOfBirth,Borrower1Nation,Borrower1Married,Borrower1Job )
    exceFill("template.xls", paramsDict1)
    
    if (BorrowerCount > 1):
        Borrower2PlaceOfBirth = findBorrower2PlaceOfBirth(extracted)
        Borrower2Birthday = findBorrower2Birthday(extracted)
        Borrower2Name= findBorrower2Name(extracted,extractedDetailed)
        Borrower2Nation = findBorrower2Nation(extracted)
        Borrower2Address = findBorrower2Address(extracted)
        Borrower2Married = findBorrower2Married(extracted)
        Borrower2Job = findborrower2workerOrOwner(extracted)
        print("\n")
        print("Borrower 2 place of birth: "+ Borrower2PlaceOfBirth.strip("., "))
        print("Borrower 2 Birth day: "+ Borrower2Birthday.strip("., "))
        print("Borrower 2 Name: "+ Borrower2Name.strip("., "))
        print("Borrower 2 Nation: " + Borrower2Nation.strip("., "))
        print("Borrower 2 Address: " + Borrower2Address.strip("., "))
        print("Borrower 2 Married: " + Borrower2Married.strip("., "))
        print("Borrower 2 Job: " + Borrower2Job.strip("., "))
        
        paramsDict = {  "Borrower2Name":Borrower2Name,"Borrower2Address":Borrower2Address,"Borrower2Birthday":Borrower2Birthday,
                        "Borrower2PlaceOfBirth":Borrower2PlaceOfBirth,
                        "Borrower2Nation":Borrower2Nation,"Borrower2Married":Borrower2Married,"Borrower2Job":Borrower2Job,
                        "Borrower2Address":Borrower2Address,"Borrower2Birthday":Borrower2Birthday,"Borrower2PlaceOfBirth":Borrower2PlaceOfBirth,
                        "Borrower2Nation":Borrower2Nation,"Borrower2Married":Borrower2Married,"Borrower2Job":Borrower2Job,
                        }
        #Borrower2Name,Borrower2Address,Borrower2Birthday,Borrower2PlaceOfBirth,Borrower2Nation,Borrower2Married,Borrower2Job
        exceFillerBorrower2("template.xls", paramsDict)    
    return "Main ended mydude"

if __name__ == "__main__":
    if (len(sys.argv)<2):
        print("no arguments, file name, given")
        defaultfile = "file7"
        main(defaultfile)
    else:
        main(sys.argv[1])



        