__author__ = 'Nitin'


def agg_lines_per_stanza(poems, template):
    lines_per_stanza = [str(poem.lines) for poem in poems]
    template.lines = lines_per_stanza


def agg_n_stanzas(poems, template):
    stanza_nums = [poem.stanzas for poem in poems]
    template.stanzas = stanza_nums