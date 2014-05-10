__author__ = 'Nitin'


#There are many more, such as half line, caesurae, alliterative verse etc etc.
class Poem:

    def __init__(self, poem):
        self.poem = poem     # A list of poem lines

        self.stanzas = 0                    # Number of stanzas
        self.lines = []                     # List of numbers indicating lines per stanza
        self.repeated_lines = {}            # A map of the repeated line to the locations in the poem
        self.distinct_sentences = 0         # Number of sentences (compare with lines to get relative complexity)

        self.tenses = []                     # Tense of each line (use an enum for tense)
        self.overall_tense = ""
        self.characters = []                # A list of characters (subjects and objects) in the poem

        self.rhyme_scheme = []              # A list of characters representing the rhyme for each line: [A,A,B,B,A]
        self.internal_rhyme_scheme = []     # A list of locations in the poem with internal rhyme

        self.stress_pattern = []            # Stresses for each lines
        self.syllable_count = []            # List of number of syllables per line

        self.consonance = []                # List of lengths of the longest consonance for each line
        self.assonance = []                 # List of lengths of the longest assonance for each line
        self.alliteration = []              # List of lengths of the longest alliteration for each line

        self.onomatopoeia = []              # List of set of onomatopoeia used per line
        self.similes = []                   # List of set of similes used
        self.metaphors = []                 # List of set of metaphors used
        self.personification = []           # List of characters that might be evidence for personification

        self.perspective = ""             # first/second/third person

        self.polarity_by_line = []
        self.subjectivity_by_line = []
        self.modality_by_line = []
        self.mood_by_line = []

    def __str__(self):
        return \
            "This poem has " + str(self.stanzas) + " stanza(s)\n" +\
            " with a total of " + str(sum(self.lines)) + " lines\n" +\
            " in the format of " + str(self.lines) + "\n" +\
            " with " + str(self.distinct_sentences) + " distinct sentences.\n\n" +\
            str(len(self.repeated_lines)) + " line(s) are repeated in this poem\n" +\
            " at positions " + str(self.repeated_lines.values()) + ".\n\n" +\
            "The tenses of the lines in the given poem are " + str(self.tenses) + ",\n" +\
            " giving it a " + str(self.overall_tense) + " tense overall.\n\n" +\
            "The syllable lengths of each line are as follows: " + str(self.syllable_count) + ".\n\n" +\
            "The poem has consonance scores of: " + str(self.consonance) + ",\n" +\
            " assonance scores of: " + str(self.assonance) + "\n" +\
            " and alliteration scores of " + str(self.alliteration) + ".\n\n" +\
            "The rhyme scheme is " + str(self.rhyme_scheme) + ".\n" +\
            "There is also internal rhyme: " + str(self.internal_rhyme_scheme) + ".\n\n" +\
            "The stress patterns of each of the lines is: " + str(self.stress_pattern) + ".\n\n" +\
            "The use of similes probably has an affect: " + str(self.similes) + ",\n" +\
            "As does the use of onomatopoeia: " + str(self.onomatopoeia) + ".\n\n" +\
            "The poem is written in " + str(self.perspective) + " person.\n" +\
            "The characters in the poem are: " + str(self.characters)












