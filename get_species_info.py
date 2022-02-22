import ornitho

def get_species_info(species_name):
    species = ornitho.Species.list_all()
    
    for spec in species:
        if spec.german_name == species_name:
            print(f"{spec.german_name} found at ID = {spec.id_}")
            print(spec._raw_data)
            return spec.id_, spec.german_name, spec.latin_name, spec.taxo_group.name, spec.family.latin_name, spec.sys_order
        
    print('Species not found!')
    return 0
