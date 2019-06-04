from lib.map.mapbase import MapBase
from lib.layer.pipeline import Pipeline
from lib.layer.watersource import WaterSource
from lib.layer.reservoir import Reservoir
from lib.layer.pumpingstation import PumpingStation
from lib.layer.waterconnection import WaterConnection
from lib.layer.chamber import Chamber


class WssMap(MapBase):
    def __init__(self, db, directory, wss_id):
        super().__init__(db, directory, "{0}/{1}.png".format(directory, wss_id))
        self.wss_id = wss_id

    def create_layers(self, ax):
        for lyr in [Pipeline(self.db),
                    WaterSource(self.db),
                    Reservoir(self.db),
                    PumpingStation(self.db),
                    WaterConnection(self.db),
                    Chamber(self.db)]:
            lyr.get_data('where wss_id = {0}'.format(self.wss_id))
            lyr.plot(ax)
