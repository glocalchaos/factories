import json
from flask_sqlalchemy import SQLAlchemy

def load_preset(filepath: str):
    try:
        f = open(filepath, "r")
        
    except FileNotFoundError:
        raise Exception("error while setting up preset table: \
                        file not found ({filepath})")
    except Exception as e:
        raise Exception("error while setting up preset table:", e) 
    return json.load(f)


def upload_regions(db: SQLAlchemy,
                   filepath: str = "app/data/regionswithfactories.json"):
    from ..entities.models import RegionModel, FactoryModel

    regions = load_preset(filepath)
    session = db.session
    for region in regions:
        if session.query(RegionModel).filter(RegionModel.code == region['code']).scalar() is None:
            session.add(RegionModel(
                code=region["code"],
                name=region["region_name"]
            ))
        
        for factory in region['factories']:
            if session.query(FactoryModel).filter(FactoryModel.name == factory['factory_name']).scalar() is None:
                session.add(FactoryModel(
                    name=factory['factory_name'],
                    region_id=region["code"]
                ))
    
    session.commit()
    session.close()