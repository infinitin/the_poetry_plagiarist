__author__ = 'Nitin'
import matplotlib.pyplot as plt
from collections import Counter


def agg_n_stanzas(stanza_nums, plot):
    counts = Counter(stanza_nums).most_common()
    total = sum([count for num, count in counts])
    percentages = {}
    for num, count in counts:
        percentages[num] = count/total

    plot and show_plot(percentages)

    return percentages


def show_plot(percentages):
    plt.bar(tuple(percentages.keys()), tuple(percentages.values()))
    plt.show()