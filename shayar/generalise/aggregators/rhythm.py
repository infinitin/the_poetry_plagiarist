__author__ = 'Nitin'


def agg_syllable(poems, template):
    template.syllable_patterns = [poem.syllable_count for poem in poems]

