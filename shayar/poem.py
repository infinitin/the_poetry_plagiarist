__author__ = 'Nitin'


#There are many more, such as half line, caesurae, alliterative verse etc etc.
class Poem:

    def __init__(self, poem):
        self.poem = poem     # A list of poem lines

        self.stanzas = 0                    # Number of stanzas
        self.lines = []                     # List of numbers indicating lines per stanza
        self.repeated_lines = {}            # A map of the repeated line to the locations in the poem

        self.tense = []                     # Tense of each line (use an enum for tense)
        self.unusual_words = []             # List of words that are unusual (perhaps indicative of the era)
        self.verbs = []                     # A list of the set of verbs used in each line
        self.nouns = []                     # A list of the set of nouns used in each line
        self.adjectives = []                # A list of the set of adjectives used in each line
        self.pronouns = []                  # A list of the set of pronouns used in each line
        self.adverbs = []                   # A list of the set of adverbs used in each line
        self.characters = {}                # A map of the characters (nouns and pronouns after anaphora resolution)
                                                                      # to the locations they are mentioned

        self.rhyme_scheme = []              # A list of characters representing the rhyme for each line: [A,A,B,B,A]
        self.internal_rhyme_scheme = []     # A list of locations in the poem with internal rhyme

        self.stress_pattern = []            # Stresses for each lines
        self.rhythm = ""                    # Foot and metre stress according to pattern, e.g. iambic pentameter
        self.syllable_count = []            # List of number of syllables per line
        self.parallel_structure = []        # List consistent verb-noun order for each line, if any

        self.consonance = []                # List of lengths of the longest consonance for each line
        self.assonance = []                 # List of lengths of the longest assonance for each line
        self.alliteration = []              # List of lengths of the longest alliteration for each line

        self.onomatopoeia = []              # List of set of onomatopoeia used per line
        self.similes = []                   # List of set of similes used per line
        self.metaphors = []                 # List of set of metaphors used per line

    def __str__(self):
        return "This is an empty poem"












