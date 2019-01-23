import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Visualization(object):

    def __init__(self):
        pass

    def bar_plot(self, labels, height, fig_size=(10,10)):
        plt.figure(figsize=fig_size, dpi=80, facecolor='w', edgecolor='k')
        plt.bar(range(len(height)), height, tick_label=labels, color="y")
        plt.xticks(rotation='vertical')
        plt.show()

    def histogram(self, data, bins=25):
        plt.hist(data, color="g", bins=25)
        plt.show()
        
    def plot_time_series(self, time, values_1, values_2, fig_size=(30,10)):
        plt.figure(figsize=fig_size, dpi=80)

        plt.subplot(211)
        plt.plot(time, values_1, 'mo')
        plt.title("Out of Limit")

        plt.subplot(212)
        plt.plot(time, values_2, 'ro')
        plt.title("Vysledek 0 1")
        
        plt.show()
        