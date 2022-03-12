import xlrd, xlwt
from xlutils.copy import copy

path = "./pdf_files/" 


borrower2NameCoor =       (29,5)
borrower2AddressCoor =    (30,5)
borrower2BirthdayCoor=    (32,5)
borrower2BirthPlaceCoor = (33,5)
borrower2NationCoor =     (34,5)
borrower2MarriedCoor =    (38,5)
borrower2JobCoor=         (43,5)



def exceFillerBorrower2(filename,borrower2Name,borrower2Address,borrower2Birthday,borrower2BirthPlace,borrower2Nation,borrower2Married,borrower2Job):
    
    read_book = xlrd.open_workbook(path+ filename, formatting_info=True) #Make Readable Copy
    write_book = copy(read_book) #Make Writeable Copy
    write_sheet2 = write_book.get_sheet(0) #Get sheet 2 in writeable copy
    
        
    write_sheet2.write(borrower2NameCoor[0],borrower2NameCoor[1],borrower2Name)
    write_sheet2.write(borrower2AddressCoor[0],borrower2AddressCoor[1],borrower2Address)
    write_sheet2.write(borrower2BirthdayCoor[0],borrower2BirthdayCoor[1],borrower2Birthday)
    write_sheet2.write(borrower2BirthPlaceCoor[0],borrower2BirthPlaceCoor[1],borrower2BirthPlace)
    write_sheet2.write(borrower2NationCoor[0],borrower2NationCoor[1],borrower2Nation)
    write_sheet2.write(borrower2MarriedCoor[0],borrower2MarriedCoor[1],borrower2Married)
    write_sheet2.write(borrower2JobCoor[0],borrower2JobCoor[1],borrower2Job)
    
    
    write_book.save(path + filename + "_Borrower2.xls") #Save the newly written copy. Enter the same as the old path to write over
