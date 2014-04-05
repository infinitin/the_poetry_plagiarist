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
        self.consonance = {}
        self.alliteration = {}

        self.rhyme_schemes = []
        self.syllable_patterns = []
        self.stress_patterns = []

        self.similes = []

        self.character_count = []
        self.character_genders = []
        self.character_nums = []
        self.character_animations = []
        self.character_personifications = []
        self.character_relations = {}
        self.character_relation_distribution = []

        self.n_grams_by_line = []
        self.n_grams = []

        self.hypernym_ancestors = []

    def plot(self, attribute):
        if not attribute:
            pass
        elif attribute == 'all':
            for func in attribute_plot_map.values():
                func(self)
        else:
            attribute_plot_map[attribute](self)

    def plot_stanzas(self):
        simple_plotter(self.stanzas, 'Number of stanzas', 'Number of occurrences', 'Range of number of stanzas',
                       use_x=True)

    def plot_num_lines(self):
        simple_plotter(self.num_lines, 'Number of lines for all stanza amounts', 'Number of occurrences',
                       'Range of number of lines per stanza')

    def plot_repeated_lines(self):
        simple_plotter(self.repeated_lines_locations, 'Positions of repeated lines', 'Number of occurrences',
                       'Range of positions of repeated lines')

    def plot_num_repeated_lines(self):
        simple_plotter(self.num_repeated_lines, 'Number of repeated lines', 'Number of occurrences',
                       'Range of number of repeated lines', use_x=True)

    def plot_num_distinct_sentences(self):
        simple_plotter(self.num_distinct_sentences, 'Number of distinct sentences', 'Number of occurrences',
                       'Range of number of distinct sentences')

    def plot_line_tenses(self):
        simple_plotter(self.line_tenses, 'Permutations of line tenses', 'Number of occurrences',
                       'Range of permutations of tenses for each line')

    def plot_overall_tense(self):
        simple_plotter(self.overall_tense, 'Overall tense', 'Number of occurrences', 'Range of overall poem tense')

    def plot_assonance(self):
        x = tuple(np.arange(len(self.assonance.keys())))
        x_ticks = tuple(self.assonance.keys())
        ys = self.assonance.values()

        for y in ys:
            if len(y) < len(x):
                y.extend([0] * (len(x) - len(y)))

        zipped_ys = zip(*ys)
        plot_bar_stacked(x, zipped_ys, 'Vowel Phonemes', 'Number of occurrences stacked by poem', x_ticks, 'Assonance')

    def plot_consonance(self):
        x = tuple(np.arange(len(self.consonance.keys())))
        x_ticks = tuple(self.consonance.keys())
        ys = self.consonance.values()

        for y in ys:
            if len(y) < len(x):
                y.extend([0] * (len(x) - len(y)))

        zipped_ys = zip(*ys)
        plot_bar_stacked(x, zipped_ys, 'Consonant Phonemes', 'Number of occurrences stacked by poem', x_ticks,
                         'Consonance')

    def plot_alliteration(self):
        x = tuple(np.arange(len(self.alliteration.keys())))
        x_ticks = tuple(self.alliteration.keys())
        ys = self.alliteration.values()

        for y in ys:
            if len(y) < len(x):
                y.extend([0] * (len(x) - len(y)))

        zipped_ys = zip(*ys)
        plot_bar_stacked(x, zipped_ys, 'Consonant Phonemes', 'Number of occurrences stacked by poem', x_ticks,
                         'Alliteration')

    def plot_rhyme(self):
        simple_plotter(self.rhyme_schemes, 'Rhyme Scheme', 'Number of occurrences', 'Range of Possible Rhyme Schemes')

    def plot_syllable_patterns(self):
        simple_plotter(self.syllable_patterns, 'Syllable Patterns', 'Number of occurrences', 'Possible Syllabic Rhythm')

    def plot_stress_patterns(self):
        for line in self.stress_patterns:
            simple_plotter(line, 'Stress Pattern', 'Number of occurrences',
                           'Range of Possible Stress Patterns for Line ' + str(self.stress_patterns.index(line) + 1))

    def plot_similes(self):
        simple_plotter(self.similes, 'Existence', 'Number of occurrences', 'Exsistence of Simile')

    def plot_character_count(self):
        simple_plotter(self.character_count, 'Number of characters', 'Number of occurrences',
                       'Range of number of characters')

    def plot_character_genders(self):
        simple_plotter(self.character_genders, 'Gender', 'Number of occurrences', 'Range of character genders')

    def plot_character_nums(self):
        simple_plotter(self.character_nums, 'Num', 'Number of occurrences', 'Range of character nums')

    def plot_character_animations(self):
        simple_plotter(self.character_animations, 'Object State', 'Number of occurrences',
                       'Range of character animation')

    def plot_character_personifications(self):
        simple_plotter(self.character_personifications, 'Existence', 'Number of occurrences',
                       'Existence of character personification')

    def plot_character_relations(self):
        x = tuple(np.arange(len(self.character_relations.keys())))
        x_ticks = tuple(self.character_relations.keys())
        y = tuple(self.character_relations.values())
        plot_bar_simple(x, y, 'Relation', 'Number of occurrences', x_ticks, 'Range of character relations')

    def plot_character_relation_distribution(self):
        n = 1
        for relation_distribution in self.character_relation_distribution:
            x = tuple(np.arange(len(relation_distribution.keys())))
            x_ticks = tuple(relation_distribution.keys())
            y = tuple(relation_distribution.values())
            plot_bar_simple(x, y, 'Relation', 'Number of occurrences', x_ticks,
                            'Average number of each relation for character ' + str(n))
            n += 1

attribute_plot_map = {
    'stanzas': Template.plot_stanzas,
    'num_lines': Template.plot_num_lines,
    'repeated_lines': Template.plot_repeated_lines,
    'num_repeated_lines': Template.plot_num_repeated_lines,
    'num_distinct_sentences': Template.plot_num_distinct_sentences,
    'line_tenses': Template.plot_line_tenses,
    'overall_tense': Template.plot_overall_tense,
    'assonance': Template.plot_assonance,
    'consonance': Template.plot_consonance,
    'alliteration': Template.plot_alliteration,
    'rhyme': Template.plot_rhyme,
    'syllable_patterns': Template.plot_syllable_patterns,
    'stress_patterns': Template.plot_stress_patterns,
    'similes': Template.plot_similes,
    'character_count': Template.plot_character_count,
    'character_genders': Template.plot_character_genders,
    'character_nums': Template.plot_character_nums,
    'character_animations': Template.plot_character_animations,
    'character_personifications': Template.plot_character_personifications,
    'character_relations': Template.plot_character_relations,
    'character_relation_distributions': Template.plot_character_relation_distribution,
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


def plot_bar_stacked(x, ys, x_axis, y_axis, x_ticks, title):
    width = 0.5

    fig, ax = plt.subplots()
    prev = 0
    colour = 'b'
    for y in ys:
        ax.bar(x, y, bottom=prev, width=width, color=colour, align='center')
        prev = y
        if colour == 'b':
            colour = 'r'
        else:
            colour = 'b'

    ax.set_xticklabels(x_ticks)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    plt.xticks(x, ha='center')

    plt.show()


def simple_plotter(attribute, x_axis, y_axis, title, use_x=False):
    counts = Counter(attribute).most_common()
    x = tuple(np.arange(len(counts)))
    x_ticks = x if use_x else tuple([num for num, count in counts])
    y = tuple([count for num, count in counts])
    plot_bar_simple(x, y, x_axis, y_axis, x_ticks, title)




