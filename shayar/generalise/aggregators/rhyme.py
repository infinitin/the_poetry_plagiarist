__author__ = 'Nitin'
from utils import get_most_common
import logging


def agg_rhyme(poems, template):
    logging.info('Starting aggregator: agg_rhyme')
    rhyme_schemes = []

    rhyme_scheme_possibilities = [poem.rhyme_scheme for poem in poems]

    while rhyme_scheme_possibilities:
        possibilities = [rhyme_scheme for rhyme_scheme_possibility in rhyme_scheme_possibilities
                         for rhyme_scheme in rhyme_scheme_possibility]
        try:
            most_common = min(get_most_common(possibilities))
        except ValueError:
            break

        rhyme_schemes.extend([possibility for possibility in possibilities if possibility == most_common])
        rhyme_scheme_possibilities = [rhyme_scheme_possibility for rhyme_scheme_possibility in
                                      rhyme_scheme_possibilities if most_common not in rhyme_scheme_possibility]

    template.rhyme_schemes = rhyme_schemes

    logging.info('Aggregator finished: agg_rhyme')