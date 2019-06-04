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

    def create(self):
        plt.figure()
        fig, ax = plt.subplots(1, figsize=(10, 8))
        ax.set_aspect('equal')

        self.create_layers(ax)

        plt.legend(frameon=False, loc='lower center', ncol=3,
                   bbox_to_anchor=(0.5, -0.6)
                   )
        plt.subplots_adjust(bottom=0.4)
        ax.set_axis_off()

    def save(self):
        plt.savefig(self.filename)
        plt.close()

    @abstractmethod
    def create_layers(self, ax):
        pass
