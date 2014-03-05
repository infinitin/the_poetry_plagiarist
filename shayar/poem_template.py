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

    def plot_stanzas(self):
        counts = Counter(self.stanzas).most_common()
        x = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar(x, y, 'Number of stanzas', 'Number of occurrences', x, 'Range of number of stanzas')

    def num_lines_plot(self):
        counts = Counter(self.num_lines).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar(x, y, 'Number of lines for all stanza amounts', 'Number of occurrences', x_ticks,
                 'Range of number of lines per stanza')

    def repeated_lines_plot(self):
        counts = Counter(self.repeated_lines_locations).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar(x, y, 'Positions of repeated lines', 'Number of occurrences', x_ticks,
                 'Range of positions of repeated lines')

    def num_repeated_lines_plot(self):
        counts = Counter(self.num_repeated_lines).most_common()
        x = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar(x, y, 'Number of repeated lines', 'Number of occurrences', x, 'Range of number of repeated lines')

    def num_distinct_sentences_plot(self):
        counts = Counter(self.num_distinct_sentences).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar(x, y, 'Number of distinct sentences', 'Number of occurrences', x_ticks,
                 'Range of number of distinct sentences')


attribute_plot_map = {
    'stanzas': Template.plot_stanzas,
    'num_lines': Template.num_lines_plot,
    'repeated_lines': Template.repeated_lines_plot,
    'num_repeated_lines': Template.num_repeated_lines_plot,
    'num_distinct_sentences': Template.num_distinct_sentences_plot
}


def plot_bar(x, y, x_axis, y_axis, x_ticks, title):
    width = 0.5

    fig, ax = plt.subplots()
    ax.bar(x, y, width=width, align='center')

    ax.set_xticklabels(x_ticks)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    plt.xticks(x, ha='center')

    plt.show()








