__author__ = 'Nitin'
import matplotlib.pyplot as plt

import numpy as np
from collections import Counter

global pp


# Has all the options for producing poems, as well as plot functions for viewing the options
class Template:
    def __init__(self, collection):
        self.collection = collection  # The collection of poems that this template applies to

        #Pick one randomly out of the lists, repetitions will take care of probability
        self.stanzas = []  # List of numbers
        self.num_lines = []  # List of tuples of numbers
        self.repeated_lines_locations = []  # List of tuples of numbers
        self.num_repeated_lines = []  # List of numbers
        self.num_distinct_sentences = []  # List of numbers
        self.line_tenses = []  # List of tuples of strings
        self.overall_tense = []  # List of strings

        self.assonance = {}  # Dictionary<string, list(num)>
        self.consonance = {}  # Dictionary<string, list(num)>
        self.alliteration = {}  # Dictionary<string, list(num)>

        self.rhyme_schemes = []  # List of strings
        self.syllable_patterns = []  # List of tuples of numbers
        self.stress_patterns = []  # List of strings

        self.similes = []  # List of booleans

        self.character_count = []  # List of numbers
        self.character_genders = []  # List of strings
        self.character_nums = []  # List of strings
        self.character_animations = []  # List of strings
        self.character_personifications = []  # List of booleans
        self.character_relations = {}  # Dictionary<string, list(num)>
        self.character_relation_distribution = []  # List of dictionary<string, num)

        self.n_grams_by_line = []  # List of list of strings
        self.n_grams = []  # List of strings

        self.hypernym_ancestors = []  # List of tuples<string, num>

        self.polarity_by_line = []  # List of floats
        self.subjectivity_by_line = []  # List of floats
        self.modality_by_line = []  # List of floats
        self.mood_by_line = []  # List of strings

    def plot(self, attribute, pdfpages):
        global pp
        pp = pdfpages
        if not attribute:
            pass
        elif attribute == 'all':
            for a in self.__dict__:
                if a != 'collection':
                    plot_func = getattr(self, 'plot_' + a)
                    plot_func()
        else:
            plot_func = getattr(self, 'plot_' + attribute)
            plot_func()

    def plot_stanzas(self):
        simple_plotter(self.stanzas, 'Number of stanzas', 'Number of occurrences', 'Range of number of stanzas')

    def plot_num_lines(self):
        simple_plotter(self.num_lines, 'Number of lines for all stanza amounts', 'Number of occurrences',
                       'Range of number of lines per stanza')

    def plot_repeated_lines_locations(self):
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

    def plot_rhyme_schemes(self):
        simple_plotter(self.rhyme_schemes, 'Rhyme Scheme', 'Number of occurrences', 'Range of Possible Rhyme Schemes')

    def plot_syllable_patterns(self):
        simple_plotter(self.syllable_patterns, 'Syllable Patterns', 'Number of occurrences', 'Possible Syllabic Rhythm')

    def plot_stress_patterns(self):
        for line in self.stress_patterns:
            simple_plotter(line, 'Stress Pattern', 'Number of occurrences',
                           'Range of Possible Stress Patterns for Line ' + str(self.stress_patterns.index(line) + 1))

    def plot_similes(self):
        simple_plotter(self.similes, 'Existence', 'Number of occurrences', 'Existence of Simile')

    def plot_character_count(self):
        simple_plotter(self.character_count, 'Number of persona', 'Number of occurrences',
                       'Range of number of persona')

    def plot_character_genders(self):
        simple_plotter(self.character_genders, 'Gender', 'Number of occurrences', 'Range of persona genders')

    def plot_character_nums(self):
        simple_plotter(self.character_nums, 'Num', 'Number of occurrences', 'Range of persona nums')

    def plot_character_animations(self):
        simple_plotter(self.character_animations, 'Object State', 'Number of occurrences',
                       'Range of persona animation')

    def plot_character_personifications(self):
        simple_plotter(self.character_personifications, 'Personification', 'Number of occurrences',
                       'Existence of persona personification')

    def plot_character_relations(self):
        x = tuple(np.arange(len(self.character_relations.keys())))
        x_ticks = tuple(self.character_relations.keys())
        y = tuple(self.character_relations.values())
        plot_bar_simple(x, y, 'Relation', 'Number of occurrences', x_ticks, 'Range of persona relations')

    def plot_character_relation_distribution(self):
        n = 1
        for relation_distribution in self.character_relation_distribution:
            x = tuple(np.arange(len(relation_distribution.keys())))
            x_ticks = tuple(relation_distribution.keys())
            y = tuple(relation_distribution.values())
            plot_bar_simple(x, y, 'Relation', 'Number of occurrences', x_ticks,
                            'Average number of each relation for persona' + str(n))
            n += 1

    def plot_n_grams_by_line(self):
        for line in self.n_grams_by_line:
            x = tuple(np.arange(len(line)))
            x_ticks = tuple([gram for gram, count in line])
            y = tuple([count for gram, count in line])
            plot_bar_simple(x, y, 'Lemmatised n-grams', 'Number of occurrences', x_ticks,
                            'Common n-grams for Line ' + str(self.n_grams_by_line.index(line) + 1))

    def plot_n_grams(self):
        x = tuple(np.arange(len(self.n_grams)))
        x_ticks = tuple([gram for gram, count in self.n_grams])
        y = tuple([count for gram, count in self.n_grams])
        plot_bar_simple(x, y, 'Lemmatised n-grams', 'Number of occurrences', x_ticks, 'Common n-grams throughout poem')

    def plot_hypernym_ancestors(self):
        x = tuple(np.arange(len(self.hypernym_ancestors)))
        x_ticks = tuple([hypernym for hypernym, count in self.hypernym_ancestors])
        y = tuple([count for hypernym, count in self.hypernym_ancestors])
        plot_bar_simple(x, y, 'Hypernym Ancestors', 'Number of occurrences', x_ticks, 'Types of Persona')

    def plot_modality_by_line(self):
        for line in self.modality_by_line:
            simple_plotter(line, 'Modality (degree of certainty)', 'Number of occurrences',
                           'Modality for Line ' + str(self.modality_by_line.index(line) + 1))

    def plot_polarity_by_line(self):
        for line in self.polarity_by_line:
            simple_plotter(line, 'Polarity (degree of positivity)', 'Number of occurrences',
                           'Polarity for Line ' + str(self.polarity_by_line.index(line) + 1))

    def plot_subjectivity_by_line(self):
        for line in self.subjectivity_by_line:
            simple_plotter(line, 'Subjectivity (degree of bias)', 'Number of occurrences',
                           'Subjectivity for Line ' + str(self.subjectivity_by_line.index(line) + 1))

    def plot_mood_by_line(self):
        for line in self.mood_by_line:
            simple_plotter(line, 'Mood (fact/command/conjecture/wish)', 'Number of occurrences',
                           'Mood for Line ' + str(self.mood_by_line.index(line) + 1))


def plot_bar_simple(x, y, x_axis, y_axis, x_ticks, title):
    width = 0.5

    fig, ax = plt.subplots()
    ax.bar(x, y, width=width, align='center')

    ax.set_xticklabels(x_ticks)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    plt.xticks(x, ha='center', size='small')

    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)

    plt.tight_layout()

    pp.savefig(bbox_inches='tight')
    plt.close()


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
    plt.xticks(x, ha='center', size='small')

    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)

    plt.tight_layout()

    pp.savefig(bbox_inches='tight')
    plt.close()


def simple_plotter(attribute, x_axis, y_axis, title, use_x=False):
    counts = Counter(attribute).most_common()
    x = tuple(np.arange(len(counts)))
    x_ticks = x if use_x else tuple([num for num, count in counts])
    y = tuple([count for num, count in counts])
    plot_bar_simple(x, y, x_axis, y_axis, x_ticks, title)




