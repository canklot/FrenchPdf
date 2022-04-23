import xlrd, xlwt
from xlutils.copy import copy
import sys,os

# Long country names for short codes
country_codes = {'DEU': 'ALLEMAGNE', 'AUT': 'AUTRICHE', 'BEL': 'BELGIQUE', 'BGR': 'BULGARIE', 'CYP': 'CHYPRE', 'HRV': 'CROATIE', 'DNK': 'DANEMARK', 'ESP': 'ESPAGNE', 'EST': 'ESTONIE', 'FIN': 'FINLANDE', 'FRA': 'FRANCE', 'GRC': 'GRÈCE', 'HUN': 'HONGRIE', 'IRL': 'IRLANDE', 'ITA': 'ITALIE', 'LVA': 'LETTONIE', 'LTU': 'LITUANIE', 'MLT': 'MALTE', 'LUX': 'LUXEMBOURG', 'NLD': 'PAYS-BAS', 'POL': 'POLOGNE', 'PRT': 'PORTUGAL', 'CZE': 'REPUBLIQUE TCHÈQUE', 'ROM': 'ROUMANIE', 'SVK': 'SLOVAQUIE', 'SVN': 'SLOVÉNIE', 'SWE': 'SUÈDE', 'AUS': 'AUSTRALIE', 'CAN': 'CANADA', 'KOR': 'CORÉE (République de)', 'USA': "ÉTATS UNIS D'AMÉRIQUE", 'ISL': 'ISLANDE', 'JPN': 'JAPON', 'MEX': 'MEXIQUE', 'NOR': 'NORVÈGE', 'NZL': 'NOUVELLE ZÉLANDE', 'CHE': 'SUISSE', 'TUR': 'TURQUIE', 'AFG': 'AFGHANISTAN', 'ZAF': 'AFRIQUE DU SUD', 'ALB': 'ALBANIE', 'DZA': 'ALGÉRIE', 'AND': 'ANDORRE', 'AGO': 'ANGOLA', 'ANT': 'ANTILLES NÉERLANDAISES', 'SAU': 'ARABIE SAOUDITE', 'ARG': 'ARGENTINE', 'ARM': 'ARMÉNIE', 'ABW': 'ARUBA', 'AZE': 'AZERBAÏDJAN', 'BHS': 'BAHAMAS', 'BHR': 'BAHREÏN', 'BGD': 'BANGLADESH', 'BLZ': 'BÉLIZE', 'BEN': 'BÉNIN', 'BMU': 'BERMUDES', 'BTN': 'BHOUTAN', 'BLR': 'BIÉLORUSSIE', 'MMR': 'BIRMANIE (MYANMAR)', 'BOL': 'BOLIVIE', 'BIH': 'BOSNIE-HERZÉGOVINE', 'BWA': 'BOTSWANA', 'BRA': 'BRÉSIL', 'BRN': 'BRUNEÏ', 'BFA': 'BURKINA FASO', 'BDI': 'BURUNDI', 'KHM': 'CAMBODGE', 'CMR': 'CAMEROUN', 'CPV': 'CAP VERT', 'CAF': 'CENTRAFRICAINE (République)', 'CHL': 'CHILI', 'CHN': 'CHINE', 'COL': 'COLOMBIE', 'COM': 'COMORES', 'COG': 'CONGO', 'COD': 'CONGO (République démocratique du)', 'PRK': 'CORÉE (République populaire démocratique de)', 'CRI': 'COSTA RICA', 'CIV': "CÔTE D'IVOIRE", 'CUB': 'CUBA', 'DJI': 'DJIBOUTI', 'DOM': 'DOMINICAINE (République)', 'DMA': 'DOMINIQUE', 'EGY': 'ÉGYPTE', 'ARE': 'ÉMIRATS ARABES UNIS', 'ECU': 'ÉQUATEUR', 'ERI': 'ÉRYTRÉE', 'ETH': 'ÉTHIOPIE', 'FRO': 'FÉROÉ (Îles)', 'FJI': 'FIDJI', 'GAB': 'GABON', 'GMB': 'GAMBIE', 'GEO': 'GEORGIE', 'GHA': 'GHANA', 'GIB': 'GIBRALTAR', 'GRD': 'GRENADE', 'GRL': 'GROËNLAND', 'GUM': 'GUAM', 'GTM': 'GUATÉMALA', 'GIN': 'GUINÉE', 'GNQ': 'GUINÉE ÉQUATORIALE', 'GNB': 'GUINEÉ-BISSAU', 'GUY': 'GUYANA', 'HTI': 'HAÏTI', 'HND': 'HONDURAS', 'HKG': 'HONG KONG', 'IND': 'INDE', 'IDN': 'INDONÉSIE', 'IRQ': 'IRAK', 'IRN': "IRAN (République islamique d')", 'ISR': 'ISRAËL', 'JAM': 'JAMAÏQUE', 'JOR': 'JORDANIE', 'KAZ': 'KAZAKSTAN', 'KEN': 'KENYA', 'KIR': 'KIRIBATI', 'KWT': 'KOWEÏT', 'KGZ': 'KYRGYZSTAN', 'LAO': 'LAOS (République populaire démocratique du)', 'LSO': 'LESOTHO', 'LBN': 'LIBAN', 'LBR': 'LIBÉRIA', 'LBY': 'LIBYE', 'LIE': 'LIECHTENSTEIN', 'MAC': 'MACAO', 'MKD': 'MACÉDOINE (ancienne République yougoslave de)', 'MDG': 'MADAGASCAR', 'MYS': 'MALAISIE', 'MWI': 'MALAWI', 'MDV': 'MALDIVES', 'MLI': 'MALI', 'FLK': 'MALOUINES (Îles)', 'MAR': 'MAROC', 'MHL': 'MARSHALL (Îles)', 'MUS': 'MAURICE', 'MRT': 'MAURITANIE', 'FSM': 'MICRONÉSIE (États fédérés de)', 'MDA': 'MOLDAVIE', 'MCO': 'MONACO', 'MNG': 'MONGOLIE', 'MNE': 'MONTÉNÉGRO', 'MSR': 'MONTSERRAT', 'MOZ': 'MOZAMBIQUE', 'NAM': 'NAMIBIE', 'NPL': 'NÉPAL', 'NIC': 'NICARAGUA', 'NER': 'NIGER', 'NGA': 'NIGÉRIA', 'OMN': 'OMAN', 'UGA': 'OUGANDA', 'UZB': 'OUZBÉKISTAN', 'PAK': 'PAKISTAN', 'PLW': 'PALAU', 'PAN': 'PANAMA', 'PNG': 'PAPOUASIE NOUVELLE GUINÉE', 'PRY': 'PARAGUAY', 'PER': 'PÉROU', 'PHL': 'PHILIPPINES', 'PCN': 'PITCAÏRN', 'PRI': 'PORTO RICO', 'QAT': 'QUATAR', 'RUS': 'Fédération de RUSSIE', 'RWA': 'RWANDA', 'ESH': 'SAHARA OCCIDENTAL', 'KNA': 'SAINT KITTS ET NEVIS', 'VCT': 'SAINT VINCENT ET GRENADINES', 'SHN': 'SAINTE HÉLÈNE', 'LCA': 'SAINTE LUCIE', 'SLV': 'SALVADOR', 'WSM': 'SAMOA', 'SMR': 'SAN MARIN', 'STP': 'SAO TOMÉ ET PRINCIPE', 'SEN': 'SÉNÉGAL', 'RSB': 'SERBIE', 'SYC': 'SEYCHELLES', 'SLE': 'SIERRA LÉONE', 'SGP': 'SINGAPOUR', 'SLB': 'SALOMON (Îles)', 'SOM': 'SOMALIE', 'SDN': 'SOUDAN', 'LKA': 'SRI LANKA', 'SUR': 'SURINAME', 'SWZ': 'SWAZILAND', 'SYR': 'SYRIE (République arabe syrienne)', 'TJK': 'TADJIKISTAN', 'TWN': 'TAÏWAN', 'TZA': 'TANZANIE', 'TCD': 'TCHAD', 'THA': 'THAÏLANDE', 'TMP': 'TIMOR ORIENTAL', 'TGO': 'TOGO', 'TON': 'TONGA', 'TTO': 'TRINIDAD ET TOBAGO', 'TUN': 'TUNISIE', 'TKM': 'TURKMÉNISTAN', 'UKR': 'UKRAINE', 'URY': 'URUGUAY', 'VUT': 'VANUATU', 'VEN': 'VÉNÉZUELA', 'VNM': 'VIETNAM', 'YEM': 'YEMEN', 'RDC': 'République démocratique du CONGO', 'ZMB': 'ZAMBIE', 'ZWE': 'ZIMBABWE'}

# Coordinates of the fields on excel template file
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
          "picture"         :(1,17),
          "valid_score"     :(1,18)
          }
         
def countryCodes(code_in):
    # Convert short code to long name
    if code_in in country_codes:
        country=country_codes[code_in]
        return country
    else: return " " 

#mrzType,number,names,surname,sex,birthday
def excelFill(mrz):
    cwd = os.getcwd()
    # Path to excel files
    path = cwd+ "/files/" 
    fileName = "template_IdPass.xls"
    read_book = xlrd.open_workbook(path+ fileName, formatting_info=True) # Make Readable Copy
    write_book = copy(read_book) # Make Writeable Copy
    write_sheet1 = write_book.get_sheet(0) # Get sheet 1 in writeable cop
    
    # Example write_sheet1.write(1, 11, 'test') # Write 'test' to cell (B, 11)

    for field in coorDict:
        # Loop in field names and coordinates
        style0 = xlwt.easyxf('font: color-index black')
        # Default style for font color
        if hasattr(mrz, field):
            value =  getattr(mrz, field)

            if field == "type":
                docType = value
                if value == "IR":
                    value = "Carte de resident"
            elif( "date" in field) and (field != None) and (field != " ") and (field != ""): 
                # Convert date to human readeble form. The dates on mrz are in YY/MM/DD format
                # Converts it to DD/MM/YY and puts slashes between them
                value= str(value[4:6])+"/"+str(value[2:4])+"/"+str(value[:2])
            elif field == "country":
                # Convert country code to long country name
                country = countryCodes(value)
            elif field == "nationality":
                # If its ID card is not an ID card for foreigners
                # Nationality and issuing country are the same
                # If its foreigner card. Nationality is nationality field inside the mrz
                if docType != "IR":
                    value = country
                else: value = countryCodes(value)
            elif field == "sex":
                # Converts sex to french words for male and female
                if value == "F": value="Femme"
                elif value == "M": value="Homme"
                
            # This block makes the font red or green based on checksum value
            if field == "date_of_birth":
                # Dont make this if to elif. Date formatter consumes it first and never runs this block then
                if mrz.valid_date_of_birth == True:
                    style0 = xlwt.easyxf('font: color-index green')
                elif mrz.valid_date_of_birth == False:
                    style0 = xlwt.easyxf('font: color-index red')
            elif field == "number" :
                if mrz.valid_number == True:
                    style0 = xlwt.easyxf('font: color-index green')
                elif  mrz.valid_number == False:
                    style0 = xlwt.easyxf('font: color-index red')
            elif field == "expiration_date":
                if mrz.valid_expiration_date == True:
                    style0 = xlwt.easyxf('font: color-index green')
                elif  mrz.valid_expiration_date == False:
                    style0 = xlwt.easyxf('font: color-index red')
        
        # If field in not present in mrz then make it blank 
        else: value = " "
        write_sheet1.write(*coorDict[field], value, style0) # Write values one by one
        
    fileName= fileName.replace(".xls","") # prevent .xls repating in the file name
    write_book.save(path + fileName + "Final.xls") # Writes the excel file to disk