from abc import abstractmethod
import matplotlib as mpl
import matplotlib.pyplot as plt
import os


class MapBase(object):
    def __init__(self, db, directory, filename):
        self.db = db
        self.filename = filename
        self.directory = "./{0}".format(directory)
        if not os.path.exists(self.directory):
            os .makedirs(self.directory)
        mpl.use('Agg')
        mpl.rcParams['axes.xmargin'] = 0
        mpl.rcParams['axes.ymargin'] = 0

    def create(self):
        plt.figure()
        fig, ax = plt.subplots(1, figsize=(8, 5))

        self.create_layers(ax)
        ax.set_aspect('equal')

        plt.legend(frameon=False, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.6), borderaxespad=0)
        ax.set_axis_off()

    def save(self):
        plt.savefig(self.filename, bbox_inches="tight", pad_inches=0)
        plt.close()

    @abstractmethod
    def create_layers(self, ax):
        pass
