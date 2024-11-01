from app import db
# from app import app
import json
from ..models.region import RegionModel

def populate_regions(regions_filepath: str="../data/regions.json"):
    try:
        f = open(regions_filepath, "r")
        session = db.session
        regions = json.load(f)
        print(regions)
    except FileNotFoundError:
        app.logger.error("error while setting up regions table: file not found")
    except Exception as e:
        app.logger.error("error while setting up regions table:", e)    
    


def populate_db():
    populate_regions()