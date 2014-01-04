__author__ = 'Nitin'


#There are many more, such as half line, caesurae, alliterative verse etc etc.
class Poem:

    def __init__(self, poem):
        self.poem = poem     # A list of poem lines

        self.stanzas = 0                    # Number of stanzas
        self.lines = []                     # List of numbers indicating lines per stanza
        self.repeated_lines = {}            # A map of the repeated line to the locations in the poem

        self.tenses = []                     # Tense of each line (use an enum for tense)
        self.overall_tense = ""
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

        self.point_of_view = ""             # first/second/third person

    def __str__(self):
        return \
            "This poem has " + str(self.stanzas) + " stanza(s)\n" +\
            " with a total of " + str(sum(self.lines)) + " lines\n" +\
            " in the format of " + str(self.lines) + ".\n\n" +\
            str(len(self.repeated_lines)) + " line(s) are repeated in this poem\n" +\
            " at positions " + str(self.repeated_lines.values()) + ".\n\n" +\
            "The tenses of the lines in the given poem are " + str(self.tenses) + ",\n" +\
            " giving it a " + str(self.overall_tense) + " tense overall.\n\n" +\
            "The syllable lengths of each line are as follows: " + str(self.syllable_count) + ".\n\n" +\
            "The poem has consonance scores of: " + str(self.consonance) + ",\n" +\
            " assonance scores of: " + str(self.assonance) + "\n" +\
            " and alliteration scores of " + str(self.alliteration) + "\n" +\
            "Scores >0.5 indicate presence, <0.5 indicate abscence and 0.5 indicate uncertainty.\n\n" +\
            "The rhyme scheme is " + str(self.rhyme_scheme) + ".\n" +\
            "There is also internal rhyme: " + str(self.internal_rhyme_scheme) + ".\n\n" +\
            "The stress patterns of each of the lines is: " + str(self.stress_pattern) + ".\n\n" +\
            "The poem is written in " + str(self.point_of_view) + " person."












