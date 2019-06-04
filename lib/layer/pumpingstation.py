from lib.layer.layerbase import LayerBase


class PumpingStation(LayerBase):
    def __init__(self, conn):
        super().__init__(conn, 'pumping_station')

    def plot(self, ax):
        if self.df.empty:
            return
        cmap = self.generate_cmap(['green', 'yellow', 'red'])
        self.df.plot(ax=ax, figsize=(20, 10), marker='>', column='status',
                      cmap=cmap, markersize=30, label='Pumping Station')

