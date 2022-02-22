
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 12:32:41 2022

@author: Luca Rigon
"""


import ornitho
import os
import inspect
import csv
import datetime
import time

t0 = time.time()

ornitho.consumer_key = "2a6336a9e173754865dc86897424b32b061b91f1f"
ornitho.consumer_secret = "fb924af60f9590f78d23d068cc4072fd"
ornitho.user_email = "support@ornitho.at"
ornitho.user_pw = "sternaparadisea"
ornitho.api_base = "https://www.ornitho.at/api/"


ornitho.cache_enabled = True          # Enable/Disable caching
ornitho.cache_name = "ornitho_cache"  # Name of the cache
ornitho.cache_backend = "redis"       # Set caching backend, possible values: sqlite, memory, mongodb, redis
ornitho.cache_expire_after = 600      # Set expiration time for cached responses




def get_species_info(species_name):
    species = ornitho.Species.list_all()
    
    for spec in species:
        if spec.german_name == species_name:
            print(f"{spec.german_name} found at ID = {spec.id_}")
            print(spec._raw_data)
            return spec.id_, spec.german_name, spec.latin_name, spec.taxo_group.name, spec.family.latin_name, spec.sys_order
        
    print('Species not found!')
    return 0



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
        
    return out




def return_obs_details(raw_data_list, taxo='Vögel'):
    #expected output: array(['ID_SIGHTING', 'ID_SPECIES', 'NAME_SPECIES', 'LATIN_SPECIES', 
                            #'TAXONOMY_NAME', 'FAMILY_NAME', 'SYS_ORDER', 'DATE', 'TIMING',
                            #'ID_FORM', 'TIME_START', 'TIME_STOP', 'FULL_FORM', 'DAILY_TEXT_COMMENT_REM', 
                            #'ID_PLACE', 'PLACE', 'MUNICIPALITY','COUNTY', 'COUNTRY', 
                            #'COORD_LAT', 'COORD_LON', 'GRID_NAME', 'PRECISION, 'ALTITUDE', 
                            #'ESTIMATION_CODE', 'TOTAL_COUNT', 'DETAIL', 
                            #'ATLAS_CODE', 'ID_OBSERVATION_DETAIL', 'OBSERVATION_DETAIL', 
                            #'SECOND_HAND', 'HIDDEN', 'ADMIN_HIDDEN', 'COMMENT', 
                            #'PRIVATE_COMMENT', 'MEDIA_HAS_MEDIA', 'ANONYMOUS', 'NO_COMMERCIAL_USE', 
                            #'SEARCH_EXPORT_ENTITY_SHORT_NAME', 'SEARCH_EXPORT_ENTITY_FULL_NAME', 
                            #'SEARCH_EXPORT_ENTITY_TRA_SHORT_NAME', 'SEARCH_EXPORT_ENTITY_TRA_FULL_NAME', 
                            #'PROTOCOL', 'HAS_RING_INFO', 
                            #'HAS_DEATH_INFO', 'INSERT_DATE', 'UPDATE_DATE'])
    
    row = []
    species_data = raw_data_list.get('species')#[1]
    place_data = raw_data_list.get('place')#[2]
    rest_data = raw_data_list.get('observers')[0]
    
    
    
    #append id_sighting
    ID = rest_data['id_sighting']
    row.append(ID)
    
    
    
    #Append Species info to row:
    row.extend([species_data['@id'], species_data['name'], species_data['latin_name'], taxo, species_data['sys_order']])

    
    #Append date and timing infos to row:
    date_time = rest_data['timing']
    NO_TIME = int(date_time['@notime']) #bool
    date, time, _ = convert_date(date_time['@ISO8601'], NO_TIME)
    
    row.extend([date, time])

        
    
    #Append Form info to row:
    if 'form' in raw_data_list.keys():
        form_data = raw_data_list.get('form')
        row.extend([form_data['@id'], form_data['time_start'], form_data['time_stop'], form_data['full_form']])
        if ('comment' in form_data):
            row.append(form_data['comment'])
        else:
            row.append(None)
    else:
        row.extend([0, '00:00', '00:00', 0, None])
        
    
    
    
    #Append Place informations to row
    BL = get_BL_county(place_data['county'])
    row.extend([place_data['@id'], place_data['name'], place_data['municipality'], place_data['county'], BL, rewrite_coord(place_data['coord_lat']), rewrite_coord(place_data['coord_lon']), rest_data['atlas_grid_name'], place_data['place_type'], rest_data['altitude']])
    
    
    
    #Append Observation details
    details = None
    Br_code = ''
    obs_id = '0'
    obs_detail = ''
    
    if 'details' in rest_data:
        details = list_to_excel_str(rest_data['details'])
    if 'atlas_code' in rest_data:
        Br_code = rest_data['atlas_code']['#text']
    if 'observation_detail' in rest_data:
        obs_id = rest_data['observation_detail']['@id']
        obs_detail = rest_data['observation_detail']['#text']
        
    row.extend([convert_est_code(rest_data['estimation_code']), rest_data['count'], details, Br_code, obs_id, obs_detail])
    
    
    
    #Append comments/private comments/eventual modifications
    hidden = 'Nein'
    admin_hidden = ''
    comment = ''
    hidden_comment = ''
    has_media = 'Nein'
    
    if 'hidden' in rest_data:
        hidden = conv_bool(rest_data['hidden'])
    if 'admin_hidden' in rest_data:
        admin_hidden = admin_type(rest_data['admin_hidden_type'])
    if 'comment' in rest_data:
        comment = rest_data['comment']
    if 'hidden_comment' in rest_data:
        hidden_comment = rest_data['hidden_comment']
    if 'medias' in rest_data:
        has_media = 'Ja'
        
    row.extend([conv_bool(rest_data['second_hand']), hidden, admin_hidden, comment, hidden_comment, has_media, conv_bool(rest_data['anonymous'])])
    
    
    
    #Append Observer Details - kein Zugriff
    row.extend(['', '-', '0', '-', '0', ''])
    
    
    
    #Append if ring/mortality info are present
    ring_info = 'Nein'
    mortality_info = 'Nein'
    
    if 'extended_info' in rest_data:
        if 'ring' in rest_data['extended_info']:
            ring_info = 'Ja'
        if 'mortality' in rest_data['extended_info']:
            mortality_info = 'Ja'
    
    row.extend([ring_info, mortality_info])
    
    
    
    #Append Insert Date and eventual Update Date
    insert_date_raw = rest_data['insert_date']
    ins_NO_TIME = int(insert_date_raw['@notime']) #bool
    ins_date, _, ins_time = convert_date(insert_date_raw['@ISO8601'], ins_NO_TIME)
    upd_date = ins_date
    upd_time = ins_time
    
    if 'update_date' in rest_data:
        update_date_raw = rest_data['update_date']
        upd_NO_TIME = int(update_date_raw['@notime']) #bool
        upd_date, _, upd_time = convert_date(update_date_raw['@ISO8601'], upd_NO_TIME)
    
    row.extend([f"{ins_date} {ins_time}", f"{upd_date} {upd_time}"])
    
    
    
    return row






#ID, ger_name, lat_name, taxo, fam, sys = get_species_info('Reiherente')
#ID, ger_name, lat_name, taxo, fam, sys = 119, 'Reiherente', 'Aythya fuligula', 'Vögel', 'Anatidae', 720
ID = 119
species = ornitho.Species.get(ID) #Reiherente
species_info = [species.id_, species.german_name, species.latin_name, species.taxo_group.name, species.family.latin_name, species.sys_order]

#place_id=85271
#grid_id=...
#observer_id=... #->>>> kein Zugriff drauf!!

date_begin = "01.01.2022"
date_end = "10.01.2022"

filename = 'alle_Arten'

resp = ornitho.Observation.list(date_from=date_begin, date_to=date_end, request_all=True) #8244792, 8968789, 7886764, 3482619, 8045310, 8896843, 8358181
# ----------> possible Options: id_species, id_place, id_observer, id_grid, lat, lon, date_from, date_to
print(f"\nFound {len(resp[0])} observations for {filename} (ID: {ID}) between {date_begin} and {date_end}\n")



rows = []
print('\nExtracting values...')

for obs in resp[0]:    
    row = return_obs_details(obs._raw_data)
    rows.append(row)



header = ['ID_SIGHTING', 'ID_SPECIES', 'NAME_SPECIES', 'LATIN_SPECIES', 'TAXONOMY_NAME', 'SYS_ORDER', 'DATE', 'TIMING', 'ID_FORM', 'TIME_START', 'TIME_STOP', 'FULL_FORM', 'DAILY_TEXT_COMMENT_REM', 'ID_PLACE', 'PLACE', 'MUNICIPALITY', 'COUNTY', 'COUNTRY', 'COORD_LAT', 'COORD_LON', 'GRID_NAME', 'PRECISION, ', 'ALTITUDE', 'ESTIMATION_CODE', 'TOTAL_COUNT', 'DETAIL', 'ATLAS_CODE', 'ID_OBSERVATION_DETAIL', 'OBSERVATION_DETAIL', 'SECOND_HAND', 'HIDDEN', 'ADMIN_HIDDEN', 'COMMENT', 'PRIVATE_COMMENT', 'MEDIA_HAS_MEDIA', 'ANONYMOUS', 'NO_COMMERCIAL_USE', 'SEARCH_EXPORT_ENTITY_SHORT_NAME', 'SEARCH_EXPORT_ENTITY_FULL_NAME', 'SEARCH_EXPORT_ENTITY_TRA_SHORT_NAME', 'SEARCH_EXPORT_ENTITY_TRA_FULL_NAME', 'PROTOCOL', 'HAS_RING_INFO', 'HAS_DEATH_INFO', 'INSERT_DATE', 'UPDATE_DATE']
l = len(header) #47

with open(f'export_{filename}_{date_begin}-{date_end}.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, delimiter=";")

    # write the header
    writer.writerow(header)

    # write multiple rows 
    writer.writerows(rows)

    

print('CSV file successfully created!')
print(f'Total duration: {time.time() - t0}s')