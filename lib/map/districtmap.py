from lib.map.mapbase import MapBase
from lib.layer.district import District
from lib.layer.sector import Sector
from lib.layer.pipeline import Pipeline
from lib.layer.watersource import WaterSource
from lib.layer.reservoir import Reservoir
from lib.layer.pumpingstation import PumpingStation


class DistrictMap(MapBase):
    def __init__(self, db, directory, dist_id, wss_id_list):
        super().__init__(db, directory, "{0}/{1}.png".format(directory, dist_id))
        self.dist_id = dist_id
        self.wss_id_list = wss_id_list

    def create_layers(self, ax):
        for lyr in [District(self.db), Sector(self.db)]:
            lyr.get_data('where dist_id={0}'.format(self.dist_id))
            lyr.plot(ax)

        for lyr in [Pipeline(self.db),
                    WaterSource(self.db),
                    Reservoir(self.db),
                    PumpingStation(self.db)]:
            lyr.get_data('where wss_id IN({0})'.format(self.wss_id_list))
            lyr.plot(ax)
