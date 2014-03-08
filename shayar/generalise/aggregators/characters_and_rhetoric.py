__author__ = 'Nitin'


def agg_similes(poems, template):
    template.similes = [not not poem.similes for poem in poems]
    print template.similes