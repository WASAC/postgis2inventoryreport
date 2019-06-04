from lib.layer.layerbase import LayerBase


class District(LayerBase):
    def __init__(self, conn):
        super().__init__(conn, 'district')

    def plot(self, ax):
        if self.df.count == 0:
            return
        self.df.plot(ax=ax, figsize=(20, 10), alpha=0.5, color='white', edgecolor='black', linewidth=1.0, label="District")
