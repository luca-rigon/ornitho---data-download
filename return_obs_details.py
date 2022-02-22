import ornitho
import convert_strings

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
