import xlrd, xlwt
from xlutils.copy import copy

path = "./pdf_files/" 

borrower1NameCoor =       (29,2)
borrower1AddressCoor =    (30,2)
borrower1BirthdayCoor =   (32,2)
borrower1BirthPlaceCoor = (33,2)
borrower1NationCoor =     (34,2)
borrower1MarriedCoor =    (38,2)
borrower1JobCoor=         (43,2)

borrower2NameCoor =       (29,5)
borrower2AddressCoor =    (30,5)
borrower2BirthdayCoor=    (32,5)
borrower2BirthPlaceCoor = (33,5)
borrower2NationCoor =     (34,5)
borrower2MarriedCoor =    (38,5)
borrower2JobCoor=         (43,5)



def exceFill(filename,borrower1Name,borrower1Address,borrower1Birthday,borrower1BirthPlace,borrower1Nation,borrower1Married,borrower1Job):
    
    read_book = xlrd.open_workbook(path+ filename, formatting_info=True) #Make Readable Copy
    write_book = copy(read_book) #Make Writeable Copy
    write_sheet1 = write_book.get_sheet(0) #Get sheet 1 in writeable copy
    
    write_sheet1.write(1, 11, 'test') #Write 'test' to cell (B, 11)
    
        
    write_sheet1.write(borrower1NameCoor[0],borrower1NameCoor[1],borrower1Name)
    write_sheet1.write(borrower1AddressCoor[0],borrower1AddressCoor[1],borrower1Address)
    write_sheet1.write(borrower1BirthdayCoor[0],borrower1BirthdayCoor[1],borrower1Birthday)
    write_sheet1.write(borrower1BirthPlaceCoor[0],borrower1BirthPlaceCoor[1],borrower1BirthPlace)
    write_sheet1.write(borrower1NationCoor[0],borrower1NationCoor[1],borrower1Nation)
    write_sheet1.write(borrower1MarriedCoor[0],borrower1MarriedCoor[1],borrower1Married)
    write_sheet1.write(borrower1JobCoor[0],borrower1JobCoor[1],borrower1Job)
    
    
    write_book.save(path + filename + "_Borrower1.xls") #Save the newly written copy. Enter the same as the old path to write over
    
