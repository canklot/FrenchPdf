import xlrd, xlwt
from xlutils.copy import copy

path = "./pdf_files/" 

borrower1NameCoor       = (29,2)
borrower1AddressCoor    = (30,2)
borrower1BirthdayCoor   = (32,2)
borrower1BirthPlaceCoor = (33,2)
borrower1NationCoor     = (34,2)
borrower1MarriedCoor    = (38,2)
borrower1JobCoor        = (43,2)

borrower2NameCoor       = (29,5)
borrower2AddressCoor    = (30,5)
borrower2BirthdayCoor   = (32,5)
borrower2BirthPlaceCoor = (33,5)
borrower2NationCoor     = (34,5)
borrower2MarriedCoor    = (38,5)
borrower2JobCoor        = (43,5)

propPriceCooor          = (54,2)
downPaymentCoor         = (54,5)
mortgageCoor            = (56,5)
agencyFeeCoor           = (64,2)
notaryFeeCoor           = (65,2)
propAddressCoor         = (21,2)
propType                = (22,2)
propStatus              = (24,2)


listOfCoords = [borrower1NameCoor,borrower1AddressCoor,borrower1BirthdayCoor,borrower1BirthPlaceCoor,borrower1NationCoor,
                borrower1MarriedCoor,borrower1JobCoor,propPriceCooor,downPaymentCoor,mortgageCoor,agencyFeeCoor,notaryFeeCoor,
                propAddressCoor,propType,propStatus]

listOfCoords2 =[borrower2NameCoor,borrower2AddressCoor,borrower2BirthdayCoor,
                borrower2BirthPlaceCoor,borrower2NationCoor,borrower2MarriedCoor,borrower2JobCoor,]

b1ending = "_b1"
# The order is important. 
#filename,borrower1Name,borrower1Address,borrower1Birthday,borrower1BirthPlace,borrower1Nation,borrower1Married,borrower1Job)
def exceFill(filename,argsDict):
    
    read_book = xlrd.open_workbook(path+ filename, formatting_info=True) #Make Readable Copy
    write_book = copy(read_book) #Make Writeable Copy
    write_sheet1 = write_book.get_sheet(0) #Get sheet 1 in writeable copy
    #write_sheet1.write(1, 11, 'test') #Write 'test' to cell (B, 11)

    for coor, field in zip(listOfCoords,argsDict):
        write_sheet1.write(coor[0],coor[1],argsDict[field])
    
    write_book.save(path + filename + "_final.xls") #Save the newly written copy. Enter the same as the old path to write over
    



# filename,borrower2Name,borrower2Address,borrower2Birthday,borrower2BirthPlace,borrower2Nation,borrower2Married,borrower2Job
def exceFillerBorrower2(filename,argsDict):
    
    read_book = xlrd.open_workbook(path+ filename+"_final.xls", formatting_info=True) #Make Readable Copy
    write_book = copy(read_book) #Make Writeable Copy
    write_sheet2 = write_book.get_sheet(0) #Get sheet 2 in writeable copy
    
    for coor, field in zip(listOfCoords2,argsDict):
        write_sheet2.write(coor[0],coor[1],argsDict[field])
        
    filename= filename.replace(".xls","")
    write_book.save(path + filename + "_final.xls") #Save the newly written copy. Enter the same as the old path to write over
