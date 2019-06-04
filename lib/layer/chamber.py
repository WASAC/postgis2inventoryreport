from lib.layer.layerbase import LayerBase


class Chamber(LayerBase):
    def __init__(self, conn):
        super().__init__(conn, 'chamber')

    def plot(self, ax):
        cmap = self.generate_cmap(['green', 'yellow', 'red'])
        typelist= [{'name': 'Air release chamber', 'marker' : 'v', 'column': 'status', 'markersize': 30},
                     {'name': 'Valve chamber', 'marker' : '$><$', 'column': 'status', 'markersize': 45},
                     {'name': 'Washout chamber', 'marker' : 's', 'column': 'status', 'markersize': 30},
                     {'name': 'Break Pressure chamber', 'marker': '^', 'column': 'status', 'markersize': 30},
                     {'name': 'Starting chamber', 'marker' : 'd', 'column': 'status', 'markersize': 30},
                     {'name': 'Collection chamber', 'marker' : 'D', 'column': 'status', 'markersize': 30}]
        self.plot_by_filter(ax, 'chamber_type', typelist, cmap)
