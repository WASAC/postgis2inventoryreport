from abc import abstractmethod
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


class LayerBase(object):
    def __init__(self, db, table):
        self.db = db
        self.df = None
        self.table = table

    def generate_cmap(self, colors):
        """自分で定義したカラーマップを返す"""
        values = range(len(colors))

        vmax = np.ceil(np.max(values))
        color_list = []
        for v, c in zip(values, colors):
            color_list.append((v / vmax, c))
        return LinearSegmentedColormap.from_list('custom_cmap', color_list)

    def get_data(self, where):
        sql = "select * from {0} {1}".format(self.table, where)
        tmpdf = self.db.get_geodataframe_from_postgis(sql)
        tmpdf.crs = {'init': 'epsg:4326'}
        self.df = tmpdf.to_crs(epsg=3857)

    def plot_by_filter(self, ax, filter_column, typelist, cmap):
        for type in typelist:
            tmpdf= self.df[self.df[filter_column].isin([type['name']])]
            if tmpdf.empty:
                continue
            try:
                tmpdf.plot(ax=ax, figsize=(20, 10), marker=type['marker'], column=type['column'],
                           cmap=cmap, markersize=type['markersize'], label=type['name'])
            except ValueError:  # raised if tmpdf is empty.
                pass

    @abstractmethod
    def plot(self, ax):
        pass
