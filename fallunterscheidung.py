# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 12:03:59 2022

@author: user
"""

def export_data(ID_species=None, ID_place=None, ID_observer=None, ID_grid=None, lat=None, lon=None, date_begin=None, date_end=None):
     
    species_bool = False
    filename = ''
    
    if ID_species!=None:    #search by species
        print('Search by species')
        species_bool = True
        species = ornitho.Species.get(ID_species) #Reiherente
        species_info = [species.id_, species.german_name, species.latin_name, species.taxo_group.name, species.family.latin_name, species.sys_order]
        filename = species_info[1]
        
        if ID_observer!=None:   #search for a specific observer
            print('Search by Observer')
            filename = filename + '_obs_' + str(ID_observer)
            if lat!=None:
                resp = ornitho.Observation.list(id_species=ID, id_observer=ID_observer, lat=lat, lon=lon, date_from=date_begin, date_to=date_end)
            elif ID_place != None:
                resp = ornitho.Observation.list(id_species=ID, id_observer=ID_observer, id_place=ID_place, date_from=date_begin, date_to=date_end)
            elif ID_grid != None:
                resp = ornitho.Observation.list(id_species=ID, id_observer=ID_observer, id_grid=ID_grid, date_from=date_begin, date_to=date_end)
            else:
                resp = ornitho.Observation.list(id_species=ID, id_observer=ID_observer, date_from=date_begin, date_to=date_end)

        
        else:               #by all observers
            if lat!=None:
                resp = ornitho.Observation.list(id_species=ID, lat=lat, lon=lon, date_from=date_begin, date_to=date_end)
            elif ID_place != None:
                resp = ornitho.Observation.list(id_species=ID, id_place=ID_place, date_from=date_begin, date_to=date_end)
            elif ID_grid != None:
                resp = ornitho.Observation.list(id_species=ID, id_grid=ID_grid, date_from=date_begin, date_to=date_end)
            else:
                resp = ornitho.Observation.list(id_species=ID, date_from=date_begin, date_to=date_end)



    else:               #search all species
        if ID_observer!=None:   #all observations by one observer
            filename = 'By_observer_' + str(ID_observer)
            if lat!=None:
                resp = ornitho.Observation.list(id_observer=ID_observer, lat=lat, lon=lon, date_from=date_begin, date_to=date_end)
            elif ID_place != None:
                resp = ornitho.Observation.list(id_observer=ID_observer, id_place=ID_place, date_from=date_begin, date_to=date_end)
            elif ID_grid != None:
                resp = ornitho.Observation.list(id_observer=ID_observer, id_grid=ID_grid, date_from=date_begin, date_to=date_end)
            else:
                resp = ornitho.Observation.list(id_observer=ID_observer, date_from=date_begin, date_to=date_end)

        
        else:           #any species, all observers
            filename = 'All_sightings'
            if lat!=None:
                resp = ornitho.Observation.list(lat=lat, lon=lon, date_from=date_begin, date_to=date_end)
            elif ID_place != None:
                resp = ornitho.Observation.list(id_place=ID_place, date_from=date_begin, date_to=date_end)
            elif ID_grid != None:
                resp = ornitho.Observation.list(id_grid=ID_grid, date_from=date_begin, date_to=date_end)
            else:
                resp = ornitho.Observation.list(date_from=date_begin, date_to=date_end)


    print(f"\nFound {len(resp[0])} observations between {date_begin} and {date_end}\n")
    

    rows = []
    count = 0
    print('\nExtracting values...')
    for obs in resp[0]:
        
        if count % int(len(resp[0])/10) == 0:
            print(f'Sighting Nr. {count+1}')
            
        count +=1
        
        if species_bool:
            row = return_obs_details(obs._raw_data)#, species_info=species_info)
        else:
            row = return_obs_details(obs._raw_data)
        #print(row)
        rows.append(row)
        
        
         
    header = ['ID_SIGHTING', 'ID_SPECIES', 'NAME_SPECIES', 'LATIN_SPECIES', 'TAXONOMY_NAME', 'FAMILY_NAME', 'SYS_ORDER', 'DATE', 'TIMING', 'ID_FORM', 'TIME_START', 'TIME_STOP', 'FULL_FORM', 'DAILY_TEXT_COMMENT_REM', 'ID_PLACE', 'PLACE', 'MUNICIPALITY', 'COUNTY', 'COUNTRY', 'COORD_LAT', 'COORD_LON', 'GRID_NAME', 'PRECISION, ', 'ALTITUDE', 'ESTIMATION_CODE', 'TOTAL_COUNT', 'DETAIL', 'ATLAS_CODE', 'ID_OBSERVATION_DETAIL', 'OBSERVATION_DETAIL', 'SECOND_HAND', 'HIDDEN', 'ADMIN_HIDDEN', 'COMMENT', 'PRIVATE_COMMENT', 'MEDIA_HAS_MEDIA', 'ANONYMOUS', 'NO_COMMERCIAL_USE', 'SEARCH_EXPORT_ENTITY_SHORT_NAME', 'SEARCH_EXPORT_ENTITY_FULL_NAME', 'SEARCH_EXPORT_ENTITY_TRA_SHORT_NAME', 'SEARCH_EXPORT_ENTITY_TRA_FULL_NAME', 'PROTOCOL', 'HAS_RING_INFO', 'HAS_DEATH_INFO', 'INSERT_DATE', 'UPDATE_DATE']
    l = len(header) #47

    with open(f'export_{filename}_{date_begin}-{date_end}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=";")

        # write the header
        writer.writerow(header)

        # write multiple rows 
        writer.writerows(rows)
        
    print('CSV file successfully created!')