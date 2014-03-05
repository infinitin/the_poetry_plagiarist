__author__ = 'Nitin'


def agg_lines_per_stanza(poems, template):
    template.num_lines = [tuple(poem.lines) for poem in poems]


def agg_n_stanzas(poems, template):
    template.stanzas = [poem.stanzas for poem in poems]


def agg_repeated_line_locations(poems, template):
    template.repeated_lines_locations = [tuple(poem.repeated_lines.values()) for poem in poems]


def agg_n_repeated_lines(poems, template):
    template.num_repeated_lines = [len(poem.repeated_lines.values()) for poem in poems]


def agg_n_distinct_sentences(poems, template):
    template.num_distinct_sentences = [poem.distinct_sentences for poem in poems]


def agg_line_tenses(poems, template):
    template.line_tenses = [tuple(poem.tenses) for poem in poems]


def agg_overall_tense(poems, template):
    template.overall_tense = [poem.overall_tense for poem in poems]