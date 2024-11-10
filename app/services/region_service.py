from typing import Dict, Iterable

from app.repositories.region_repository import RegionRepository


class RegionService:
    def __init__(self):
        self.repository = RegionRepository()

    # def region_code_exists(self, code: int) -> bool:
    #     return self.repository.get_region_by_code is not None
    
    def upload_region(self, code: int, name: str):
        if not self.repository.region_exists_by_code(code):
            self.repository.upload_region(code, name)

    def upload_regions(self, regions: Dict[int, str]):
        regions_list = {}
        for code, name in regions.items:
            if not self.region_code_exists(code):
                regions_list[code] = name
            
        self.repository.upload_regions(regions_list)
