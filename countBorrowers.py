import re

def countBorrowers(text):
    from findBeneficiaire import beneficiaireEnd
    shortText=text[beneficiaireEnd:beneficiaireEnd+1000]
    regex = r"Né.{0,4}? à"
    global results
    results = re.findall(regex,shortText,flags=re.DOTALL|re.IGNORECASE)
    return len(results)