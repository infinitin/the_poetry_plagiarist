__author__ = 'Nitin'
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


# Has all the options for producing poems, as well as plot functions for viewing the options
class Template:

    def __init__(self, collection):
        self.collection = collection        # The collection of poems that this template applies to

        self.stanzas = []                    # Number of stanzas
        self.lines = []                     # List of numbers indicating lines per stanza

    def plot(self, attribute):
        if attribute == 'all':
            for func in attribute_plot_map.values():
                func(self)

        attribute_plot_map[attribute]()

    def stanzas_plot(self):
        counts = Counter(self.stanzas).most_common()
        plt.bar(tuple([num for num, count in counts]), tuple([count for num, count in counts]))
        plt.show()

    def lines_plot(self):
        counts = Counter(self.lines).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])

        fig, ax = plt.subplots()
        fig.canvas.draw()

        ax.set_xticklabels(x_ticks)

        plt.bar(x, y)
        plt.show()


attribute_plot_map = {
    'stanzas': Template.stanzas_plot,
    'lines': Template.lines_plot
}









