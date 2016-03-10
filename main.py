import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os


class PercentPie():
    def __init__(self, file, label, main_data, subdata):
        self.data = pd.read_excel(file)
        self.data = self.data.sort(main_data)
        self.labels = self.data[label].tolist()
        self.maindata = np.array(self.data[main_data].tolist())
        self.subdata = np.array(self.data[subdata].tolist())
        self.percent_array = self.subdata / self.maindata

    def __genColormap__(self, length, alpha):
        cmap = cm.rainbow(np.arange(length) / length)  # Using Accent_r map
        cmap[:, 3] -= (1-alpha)
        return cmap

    def __pickSlice__(self, cmap, percents, index, alpha):
        new_cmap = cmap
        new_cmap[:, 3] -= new_cmap[:, 3]
        new_cmap[index, 3] += alpha
        new_labels = ['' for i in range(len(percents))]
        new_labels[index] = '%2.2f %%' % (percents[index] * 100)
        print(new_cmap)
        return new_cmap, new_labels

    def drawPie(self, figsize, figname):
        parts_num = len(self.labels)
        background = self.__genColormap__(parts_num, 0.3)
        r = 1
        plt.figure(figsize=figsize, dpi=320, facecolor=None)
        plt.axis('equal')
        plt.pie(self.maindata, labels=self.labels, center=(0, 0), colors=background, radius=r)
        for i in range(parts_num):
            part_cmap, part_label = self.__pickSlice__(background, self.percent_array, i, 0.8)
            part_radius = r * self.percent_array[i]
            plt.pie(self.maindata, center=(0, 0), colors=part_cmap, radius=part_radius, shadow=False,
                    wedgeprops={'linewidth': 0})
        plt.tight_layout()
        plt.savefig(figname)
        plt.show()


if __name__ == '__main__':
    mpl.style.use('ggplot')
    file = os.path.join(os.getcwd(), 'control.xlsx')
    GovControl = PercentPie(file, label='行业', main_data='总市值', subdata='国有市值')
    figname = os.path.join(os.getcwd(), 'GovControl.png')
    GovControl.drawPie(figsize=(10, 10), figname=figname)
