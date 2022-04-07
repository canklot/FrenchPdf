import xlrd, xlwt
from xlutils.copy import copy
import sys,os
import pandas as pd

coorDict={"type"            :(1,0 ),
          "country"         :(1,1 ),
          "nationality"     :(1,2 ),
          "number"          :(1,3 ),
          "names"           :(1,4 ),
          "surname"         :(1,5 ),
          "date_of_birth"   :(1,6 ),
          "place_of_birth"  :(1,7 ),
          "address"         :(1,8 ),
          "sex"             :(1,9 ),
          "expiration_date" :(1,10),
          "authority"       :(1,12),
          "colorOfEye"      :(1,13),
          "height"          :(1,14),
          "motherName"      :(1,15),
          "job"             :(1,16),
          "picture"         :(1,17)
          }
def countryCodes(code_in):
    cwd = os.getcwd()
    filename = "/files/ISO Country code.xls"
    df = pd.read_excel (cwd+filename) # I can hard code the excel file. So I dont have to read file or use pandas
    #print (df)
    # index 0 is out of bounds for axis 0 with size 0
    if code_in in df.values:
        country=df.loc[df.code==code_in, 'country'].values[0]
        return country
    else: return "cant find"

#mrzType,number,names,surname,sex,birthday
def excelFill(mrz):
    cwd = os.getcwd()
    path = cwd+ "/files/" # Change this on flask
    fileName = "template_IdPass.xls"
    read_book = xlrd.open_workbook(path+ fileName, formatting_info=True) #Make Readable Copy
    write_book = copy(read_book) #Make Writeable Copy
    write_sheet1 = write_book.get_sheet(0) #Get sheet 1 in writeable copy
    
    #write_sheet1.write(1, 11, 'test') #Write 'test' to cell (B, 11)
    for field in coorDict:
        if hasattr(mrz, field):    
            value =  getattr(mrz, field)
            if field == "type":
                docType = value
                if value == "IR":
                    value = "Carte de resident"
            elif "date" in field: #Convert date to human readeble form
                value= str(value[4:6])+"/"+str(value[2:4])+"/"+str(value[:2])
            elif field == "country":
                value = countryCodes(value)
                country = value
            elif field == "nationality":
                if docType != "IR":
                    value = country
                else: value = countryCodes(value)
            elif field == "sex":
                if value == "F": value="Femme"
                elif value == "M": value="Homme"
        
                
        else: value = "cant find"
        write_sheet1.write(*coorDict[field], value) # Write values one by one
        
    fileName= fileName.replace(".xls","")# prevent .xls repating in the file name
    write_book.save(path + fileName + "Final.xls") #Enter the same as the old path to write over