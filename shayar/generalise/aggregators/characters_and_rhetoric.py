__author__ = 'Nitin'


def agg_similes(poems, template):
    template.similes = [not not poem.similes for poem in poems]


def agg_character_count(poems, template):
    template.character_count = [len(poem.characters) for poem in poems]