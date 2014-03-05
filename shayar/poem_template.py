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
        self.line_tenses = []
        self.overall_tense = []

        self.assonance = {}

    def plot(self, attribute):
        if not attribute:
            pass
        elif attribute == 'all':
            for func in attribute_plot_map.values():
                func(self)
        else:
            attribute_plot_map[attribute](self)

    def plot_stanzas(self):
        counts = Counter(self.stanzas).most_common()
        x = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Number of stanzas', 'Number of occurrences', x, 'Range of number of stanzas')

    def plot_num_lines(self):
        counts = Counter(self.num_lines).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Number of lines for all stanza amounts', 'Number of occurrences', x_ticks,
                        'Range of number of lines per stanza')

    def plot_repeated_lines(self):
        counts = Counter(self.repeated_lines_locations).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Positions of repeated lines', 'Number of occurrences', x_ticks,
                        'Range of positions of repeated lines')

    def plot_num_repeated_lines(self):
        counts = Counter(self.num_repeated_lines).most_common()
        x = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Number of repeated lines', 'Number of occurrences', x,
                        'Range of number of repeated lines')

    def plot_num_distinct_sentences(self):
        counts = Counter(self.num_distinct_sentences).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Number of distinct sentences', 'Number of occurrences', x_ticks,
                        'Range of number of distinct sentences')

    def plot_line_tenses(self):
        counts = Counter(self.line_tenses).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Permutations of line tenses', 'Number of occurrences', x_ticks,
                        'Range of permutations of tenses for each line')

    def plot_overall_tense(self):
        counts = Counter(self.overall_tense).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Overall tense', 'Number of occurrences', x_ticks,
                        'Range of overall poem tense')

    def plot_assonance(self):
        counts = Counter(self.overall_tense).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_stacked(x, y, 'Overall tense', 'Number of occurrences', x_ticks,
                         'Range of overall poem tense')


attribute_plot_map = {
    'stanzas': Template.plot_stanzas,
    'num_lines': Template.plot_num_lines,
    'repeated_lines': Template.plot_repeated_lines,
    'num_repeated_lines': Template.plot_num_repeated_lines,
    'num_distinct_sentences': Template.plot_num_distinct_sentences,
    'line_tenses': Template.plot_line_tenses,
    'overall_tense': Template.plot_overall_tense,
    'assonance': Template.plot_assonance
}


def plot_bar_simple(x, y, x_axis, y_axis, x_ticks, title):
    width = 0.5

    fig, ax = plt.subplots()
    ax.bar(x, y, width=width, align='center')

    ax.set_xticklabels(x_ticks)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    plt.xticks(x, ha='center')

    plt.show()


def plot_bar_stacked(x, y, x_axis, y_axis, x_ticks, title):
    width = 0.5

    fig, ax = plt.subplots()
    ax.bar(x, y, width=width, align='center')

    ax.set_xticklabels(x_ticks)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    plt.xticks(x, ha='center')

    plt.show()







