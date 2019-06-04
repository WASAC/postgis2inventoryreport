from lib.layer.layerbase import LayerBase


class Pipeline(LayerBase):
    def __init__(self, conn):
        super().__init__(conn, 'pipeline')

    def plot(self, ax):
        if self.df.empty:
            return
        self.df.plot(ax=ax, figsize=(20, 10), color='blue', linewidth=1, label="Pipeline")
