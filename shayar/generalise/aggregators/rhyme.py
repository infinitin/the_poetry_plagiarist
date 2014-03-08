__author__ = 'Nitin'


def agg_rhyme(poems, template):
    rhyme_schemes = []

    rhyme_scheme_possibilities = [poem.rhyme_scheme for poem in poems]

    while rhyme_scheme_possibilities:
        possibilities = [rhyme_scheme for rhyme_scheme_possibility in rhyme_scheme_possibilities
                         for rhyme_scheme in rhyme_scheme_possibility]
        most_common = max(set(possibilities), key=possibilities.count)
        rhyme_schemes.extend([possibility for possibility in possibilities if possibility == most_common])
        rhyme_scheme_possibilities = [rhyme_scheme_possibility for rhyme_scheme_possibility in
                                      rhyme_scheme_possibilities if most_common not in rhyme_scheme_possibility]

    template.rhyme_schemes = rhyme_schemes