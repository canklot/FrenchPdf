# Converts detailed index to normal text index
# They are different because one of them counts new line as one charecter other count it as 2
import re

def indexConvert(DetailedIndx,NormalText):
    IndexWithNewline = 0
    INndexWithoutNewLine = 0
    for charecter in NormalText:
        IndexWithNewline += 1
        if charecter == "\n":
            INndexWithoutNewLine -= 0
        
        else:
            INndexWithoutNewLine +=1
        if INndexWithoutNewLine > DetailedIndx:
            return IndexWithNewline
        