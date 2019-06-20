import os
from lib.map.districtmap import DistrictMap
from lib.map.wssmap import WssMap


class MapCreator(object):
    def __init__(self, db, district, main_directory):
        self.db = db
        self.district = district
        self.main_directory = main_directory

    def create(self):
        if not os.path.exists(self.main_directory):
            os.makedirs(self.main_directory, exist_ok=True)
        dist_dir = "/".join([self.main_directory, "images", str(self.district.dist_id)])
        dist_map = DistrictMap(self.db, dist_dir, self.district.dist_id, self.district.wss_id_list)
        dist_map.create()
        for wss_id in self.district.wss_id_list.split(','):
            wss = WssMap(self.db, dist_dir, wss_id)
            wss.create()
