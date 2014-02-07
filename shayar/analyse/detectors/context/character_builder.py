__author__ = 'Nitin'

from pattern.text.en import wordnet
from shayar.character import Character

MALE_SYNSETS = set(wordnet.synsets('male') + wordnet.synsets('actor') + wordnet.synsets('husband') +
                   wordnet.synsets('father') + wordnet.synsets('brother') + wordnet.synsets('son') +
                   wordnet.synsets('king') + wordnet.synsets('prince'))
FEMALE_SYNSETS = set(wordnet.synsets('female') + wordnet.synsets('woman') + wordnet.synsets('wife') +
                     wordnet.synsets('actress') + wordnet.synsets('female_aristocrat') + wordnet.synsets('mother') +
                     wordnet.synsets('sister') + wordnet.synsets('daughter') + wordnet.synsets('queen') +
                     wordnet.synsets('princess'))

ANIMATE_SYNSETS = set(wordnet.synsets('animate thing'))
PHYSICAL_SYNSETS = set(wordnet.synsets('physical object'))

PLURAL_PRONOUNS = ['ours', 'ourselves', 'theirs', 'them', 'themselves', 'they', 'us', 'our', 'ours', 'their']
MALE_PRONOUNS = ['him', 'himself', 'hisself', 'his']
FEMALE_PRONOUNS = ['hers', 'herself', 'she', 'her']
NEUTRAL_PRONOUNS = ['it', 'itself', 'one', 'oneself', 'ownself', 'self']


def create_characters(dependencies):
    characters = {}
    for dependency in dependencies:
        word = dependency['FORM']
        gender = ''
        object_state = ''

        if word['CPOSTAG'].startswith('P'):
            if word in PLURAL_PRONOUNS:
                num = 'pl'
            else:
                num = 'sg'

            if word in MALE_PRONOUNS:
                gender = 'm'
            elif word in FEMALE_PRONOUNS:
                gender = 'f'
            elif word in NEUTRAL_PRONOUNS:
                gender = 'n'

            if gender == 'm' or gender == 'f':
                object_state = 'a'

        else:
            if dependency['POSTAG'].endswith('S'):
                num = 'pl'
            else:
                num = 'sg'

            synset = wordnet.synsets(word)[0]
            hypernyms = set(synset.hypernyms(recursive=True)).add(synset)

            if hypernyms & ANIMATE_SYNSETS:
                object_state = 'a'
            elif hypernyms & PHYSICAL_SYNSETS:
                object_state = 'p'
            else:
                object_state = 'n'

            if object_state == 'p':
                gender = 'n'
            elif object_state == 'a':
                if hypernyms & MALE_SYNSETS:
                    gender = 'm'
                elif hypernyms & FEMALE_SYNSETS:
                    gender = 'f'

        characters[dependency['ID']] = Character(dependency['ID'], num, gender, object_state)

    return characters