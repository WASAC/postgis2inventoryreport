from lib.layer.layerbase import LayerBase


class Village(LayerBase):
    def __init__(self, conn):
        super().__init__(conn, 'village')

    def plot(self, ax):
        if self.df.empty:
            return
        self.df.plot(ax=ax, figsize=(20, 10), alpha=0.5, color='white', edgecolor='black', linewidth=1.0, label="Village")
