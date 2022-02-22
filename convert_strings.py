

def conv_bool(bool_string):     #has to come in as a string

    expr = ''
    if bool_string == '0':
        expr = 'Nein'
    else:
        expr = 'Ja'

    return expr



def convert_date(date, no_time):     #--> input: YYYY-MM-DDThh:mm:ss+xx:xx as a string; no_time is a bool
    date_out = f"{str(date[8:10])}/{str(date[5:7])}/{str(date[0:4])}"  #DD/MM/YYYY
    
    if no_time:
        time_ss = None
        time_mm = None
    else:
        time_ss = str(date[11:19])     #hh:mm:ss
        time_mm = time_ss[:-3]         #hh:mm
        
    return date_out, time_mm, time_ss



def get_BL_county(county):

    BL = ''
        
    if county[0] == 'W':
        BL = 'Wien'
    elif county in ['E', 'E*', 'EU', 'GS', 'JE', 'MA', 'ND', 'OP', 'OW']:
        BL = 'Burgenland'
    elif county in ['FE', 'HE', 'K', 'KL', 'SP', 'SV', 'VI', 'VK', 'VL', 'WO']:
        BL = 'Kärnten'
    elif county in ['AM', 'BL', 'BN', 'GD', 'GF', 'HL', 'HO', 'KO', 'KR', 'KS', 'LF', 'MD', 'ME', 'MI', 'NK', 'P', 'PL', 'SB', 'TU', 'WB', 'WN', 'WT', 'WU', 'WY', 'ZT']:
        BL = 'Niederösterreich'
    elif county in ['BR', 'EF', 'FR', 'GM', 'GR', 'KI', 'L', 'LL', 'PE', 'RI', 'RO', 'SD', 'SE', 'SR', 'UU', 'VB', 'WE', 'WL']:
        BL = 'Oberösterreich'
    elif county in ['HA', 'JO', 'S', 'SL', 'TA', 'ZE']:
        BL = 'Salzburg'
    elif county in ['BM', 'DL', 'FB', 'FF', 'G', 'GU', 'HB', 'JU', 'KF', 'LB', 'LE', 'LI', 'MU', 'MZ', 'RA', 'VO', 'WZ']:
        BL = 'Steiermark'
    elif county in ['I', 'IL', 'IM', 'KB', 'KU', 'LA', 'LZ', 'RE', 'SZ']:
        BL = 'Tirol'
    elif county in ['B', 'BZ', 'DO', 'FK']:
        BL = 'Vorarlberg'
            
    return BL



def rewrite_coord(coord):   #rewrite coordinate-string into excel-compatible format
    coord_split = coord.split('.')
    return f"{coord_split[0]},{coord_split[1]}"



def convert_est_code(code):
    
    symbol = ''
    
    if code == 'ESTIMATION':
        symbol = '~'
    elif code == 'MINIMUM':
        symbol = '>'
    elif code == 'NO_VALUE':
        symbol = 'x'

    return symbol



def excel_str_german(detail):
    
    count = detail['count']
    sex = detail['sex']['#text']
    sex_id = detail['sex']['@id']
    age = detail['age']['#text']
    age_id = detail['age']['@id']
    
    excel_str = f"{count}x"
    
    
    if sex_id != 'U':
        if sex_id == 'FT':
            excel_str = (
                f"{excel_str} {sex}"
                if count == '1'
                else f"{excel_str} {sex}e" #Plural
                )
        else:
            excel_str = f"{excel_str} {sex}"
    
    
    if age_id == '3Y':
        excel_str = f"{excel_str} {age}"
    elif age_id == '4Y':
        excel_str = f"{excel_str} {age}"
    elif age_id == '5Y':
        excel_str = f"{excel_str} {age}"
    elif age_id == "PULL":
        excel_str = (
            f"{excel_str} {age}"
            if count == '1'
            else f"{excel_str} Pulli / nicht-flügge"   #Plural
        )
    elif age_id != 'U':
        excel_str = (
            f"{excel_str} {age}"
            if count == '1'
            else f"{excel_str} {age}e" #Plural
        )

    return excel_str



def list_to_excel_str(details):
        excel_str = ""
        for detail in details:
            if excel_str:
                excel_str = f"{excel_str} / {excel_str_german(detail)}"
            else:
                excel_str = f"{excel_str_german(detail)}"
        return excel_str



def admin_type(string):     #Convert admin_hidden into german Überprüfung
    
    out = ''

    if string == 'question':
        out = 'Vermutlich falsch'
    if string == 'incomplete':
        out = 'Korrektur benötigt'
    if string == 'refused':
        out = 'Falsch'
        
    return 
