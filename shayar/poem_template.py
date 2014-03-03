__author__ = 'Nitin'
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


# Has all the options for producing poems, as well as plot functions for viewing the options
class Template:

    def __init__(self, collection):
        self.collection = collection        # The collection of poems that this template applies to

        self.stanzas = []                   # Number of stanzas
        self.num_lines = []                 # List of numbers indicating lines per stanza
        self.repeated_lines_locations = []  # List of tuples of lines that are the same
        self.num_repeated_lines = []
        self.num_distinct_sentences = []

    def plot(self, attribute):
        if attribute == 'all':
            for func in attribute_plot_map.values():
                func(self)
        else:
            attribute_plot_map[attribute](self)

    def stanzas_plot(self):
        counts = Counter(self.stanzas).most_common()
        plt.bar(tuple([num for num, count in counts]), tuple([count for num, count in counts]))
        plt.show()

    def num_lines_plot(self):
        counts = Counter(self.num_lines).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])

        fig, ax = plt.subplots()
        fig.canvas.draw()

        ax.set_xticklabels(x_ticks)

        plt.bar(x, y)
        plt.show()

    def repeated_lines_plot(self):
        counts = Counter(self.repeated_lines_locations).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])

        fig, ax = plt.subplots()
        fig.canvas.draw()

        ax.set_xticklabels(x_ticks)

        plt.bar(x, y)
        plt.show()

    def num_repeated_lines_plot(self):
        counts = Counter(self.num_repeated_lines).most_common()
        plt.bar(tuple([num for num, count in counts]), tuple([count for num, count in counts]))
        plt.show()

    def num_distinct_sentences_plot(self):
        counts = Counter(self.num_distinct_sentences).most_common()
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
    'num_lines': Template.num_lines_plot,
    'repeated_lines': Template.repeated_lines_plot,
    'num_repeated_lines': Template.num_repeated_lines_plot,
    'num_distinct_sentences': Template.num_distinct_sentences_plot
}









