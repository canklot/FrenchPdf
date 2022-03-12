

def searchDetailed(DetailedText, searchme=None, font=None ,start=None,stop=None):
    if searchme != None:
        searchme = searchme.lower()
    # Case insensitive search
    result = (None,None)
    charindex = 0
    for item in DetailedText:
        if 'lines' not in item:
            continue
        # For some reason deatailedText might contaion images WHY?
        for lines in item["lines"]:
            for span in lines["spans"]: 
                textSpan =span["text"]
                textFont=span["font"]
                for charecters in span["text"]:
                    # Loops to end of textSpan then words check begins
                    
                    #print(charecters ,end="")
                    
                    
                    
                        # Other functions findBeneficiare counts newline chars as 2 charecters
                        # When extracting with fonts new line charecters are didnt extracted
                        # Because it treats pdf as lines and it only goes to end of line but doesnt include new line char
                    charindex += 1
                    #print(charecters ,end="")
                    
                    if stop != None:
                        if(charindex>stop):
                            return
                        
                    if start != None:
                        if(charindex<start):
                            #print(" continue ")
                            continue
                
                if stop != None:
                        if(charindex>stop):
                            return
                        
                if start != None:
                        if(charindex<start):
                            continue
                #print("\n\n\n\n\n\n\n SEARCHSTARTED \n\n\n\n")
                if((font != None) and (searchme!=None)):
                    if (searchme in textSpan.lower() ):
                        if(font in textFont):
                            return (span,charindex)
                
                elif(font != None) and (searchme==None):
                    if textSpan.strip() != "":
                        # Space charecter also has font
                        
                            
                        if(font in textFont):
                            result = (span,charindex)
                            #return (span,charindex)
                        if (result!=(None,None)):
                            if ( font not in textFont):
                                return result
                            
                elif ((font == None) and (searchme!=None)):
                    if (searchme in textSpan.lower() ):
                        return (span,charindex)
                        
                
    