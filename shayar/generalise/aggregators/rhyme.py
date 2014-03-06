__author__ = 'Nitin'


def agg_rhyme(poems, template):
    rhyme_schemes = []

    rhyme_scheme_possibilities = [poem.rhyme_scheme for poem in poems]
    possibilities = [tuple(rhyme_scheme) for rhyme_scheme_possibility in rhyme_scheme_possibilities for rhyme_scheme in
                     rhyme_scheme_possibility]

    while possibilities:
        most_common = max(set(possibilities), key=possibilities.count)
        rhyme_schemes.extend([possibility for possibility in possibilities if possibility == most_common])
        possibilities = [possibility for possibility in possibilities if possibility != most_common]

    template.rhyme_schemes = rhyme_schemes