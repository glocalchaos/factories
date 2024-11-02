import json


def load_preset_regions(regions_filepath: str="app/data/regions.json"):
    try:
        f = open(regions_filepath, "r")
        
    except FileNotFoundError:
        raise Exception("error while setting up regions table: file not found")
    except Exception as e:
        raise Exception("error while setting up regions table:", e) 
    return json.load(f)