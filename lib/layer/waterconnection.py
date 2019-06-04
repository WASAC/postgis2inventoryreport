from lib.layer.layerbase import LayerBase


class WaterConnection(LayerBase):
    def __init__(self, conn):
        super().__init__(conn, 'water_connection')

    def plot(self, ax):
        cmap = self.generate_cmap(['green', 'yellow', 'red'])
        typelist = [{'name' : 'Household', 'marker': 'p', 'column': 'status', 'markersize': 45},
                     {'name' : 'Public Tap', 'marker': '$\\bigoplus$', 'column': 'status', 'markersize': 30},
                     {'name' : 'Water Kiosk', 'marker': '$\\bigodot$', 'column': 'status', 'markersize': 30},
                     {'name': 'Industrial', 'marker': '$\\bigotimes$', 'column': 'status', 'markersize': 30}]
        self.plot_by_filter(ax, 'connection_type', typelist, cmap)
