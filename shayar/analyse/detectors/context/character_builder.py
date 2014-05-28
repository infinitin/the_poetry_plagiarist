__author__ = 'Nitin'
import logging
from pattern.text.en import wordnet
from shayar.character import Character
from pattern.text.en import lemma as lemmatise
from pattern.text.en import singularize

MALE_SYNSETS = set([s.gloss for s in wordnet.synsets('male')] +
                   [s.gloss for s in wordnet.synsets('actor')] +
                   [s.gloss for s in wordnet.synsets('husband')] +
                   [s.gloss for s in wordnet.synsets('father')] +
                   [s.gloss for s in wordnet.synsets('brother')] +
                   [s.gloss for s in wordnet.synsets('son')] +
                   [s.gloss for s in wordnet.synsets('king')] +
                   [s.gloss for s in wordnet.synsets('prince')] +
                   [s.gloss for s in wordnet.synsets('kinsman')] +
                   [s.gloss for s in wordnet.synsets('male_aristocrat')] +
                   [s.gloss for s in wordnet.synsets('male_offspring')])

FEMALE_SYNSETS = set([s.gloss for s in wordnet.synsets('female')] +
                     [s.gloss for s in wordnet.synsets('woman')] +
                     [s.gloss for s in wordnet.synsets('wife')] +
                     [s.gloss for s in wordnet.synsets('actress')] +
                     [s.gloss for s in wordnet.synsets('female_aristocrat')] +
                     [s.gloss for s in wordnet.synsets('mother')] +
                     [s.gloss for s in wordnet.synsets('sister')] +
                     [s.gloss for s in wordnet.synsets('daughter')] +
                     [s.gloss for s in wordnet.synsets('queen')] +
                     [s.gloss for s in wordnet.synsets('kinswoman')] +
                     [s.gloss for s in wordnet.synsets('female_offspring')] +
                     [s.gloss for s in wordnet.synsets('princess')])

ANIMATE_SYNSETS = set([s.gloss for s in wordnet.synsets('animate thing')])
PHYSICAL_SYNSETS = set([s.gloss for s in wordnet.synsets('physical object')])

PLURAL_PRONOUNS = {'ours', 'ourselves', 'theirs', 'them', 'themselves', 'they', 'us', 'our', 'their', 'we'}
MALE_PRONOUNS = {'him', 'himself', 'hisself', 'his'}
FEMALE_PRONOUNS = {'hers', 'herself', 'she', 'her'}
NEUTRAL_PRONOUNS = {'it', 'itself', 'one', 'oneself', 'ownself', 'self'}
NON_RESOLUTION_PRONOUNS = {'i', 'we', 'me', 'us', 'you', 'thee', 'thou', 'thy', 'your', 'yours', 'thine', 'ours',
                           'ourselves', 'us', 'our'}

NEXT_CHARACTER_ID = 0


# Find the nouns and pronouns of the sentence.
# Determine the gender (m/f/n/[unknown])
# Determine whether it is plural or singular
# Determine if it is an animate object ('a'), inanimate physical object ('p') or not an object ('n')
# Create the character objects for each and send them back (anaphor resolution to be done later)
def create_characters(dependencies):
    characters = []
    for dependency in dependencies:
        cpostag = dependency['CPOSTAG']
        if not (cpostag.startswith('N') or cpostag.startswith('PR')):
            dependency['CHARACTER_ID'] = ''
            continue

        global NEXT_CHARACTER_ID
        dependency['CHARACTER_ID'] = str(NEXT_CHARACTER_ID)
        NEXT_CHARACTER_ID += 1

        form = dependency['FORM']
        words = form.split(' ')
        gender = ''
        object_state = ''

        if dependency['CPOSTAG'].startswith('P'):
            if set(words) & PLURAL_PRONOUNS:
                num = 'pl'
            else:
                num = 'sg'

            if set(words) & MALE_PRONOUNS:
                gender = 'm'
            elif set(words) & FEMALE_PRONOUNS:
                gender = 'f'
            elif set(words) & NEUTRAL_PRONOUNS:
                gender = 'n'

            if not gender == 'n':
                object_state = 'a'

        else:
            if dependency['POSTAG'].endswith('S'):
                num = 'pl'
            else:
                num = 'sg'

            try:
                synset = wordnet.synsets(singularize(lemmatise(words[-1])))[0]
            except IndexError:
                try:
                    synset = wordnet.synsets(lemmatise(words[-1]))[0]
                except IndexError:
                    try:
                        synset = wordnet.synsets(singularize(words[-1]))[0]
                    except IndexError:
                        try:
                            synset = wordnet.synsets(words[-1])[0]
                        except IndexError:
                            logging.error("Failed to find synset for '" + words[-1] + "'")
                            continue

            hyps = set()
            for h in synset.hypernyms(recursive=True):
                try:
                    hyps.add(h.gloss)
                except ValueError:
                    continue

            hyps.add(synset.gloss)

            object_state = determine_object_state(hyps)
            gender = determine_gender(hyps, object_state)

        character = Character(dependency['ID'], num, gender, object_state)
        character.text = form
        if dependency['POSTAG'].startswith('P') and not set(words) & NON_RESOLUTION_PRONOUNS:
            character.is_pronoun = True
        character.add_relation("IsA", form)
        characters.append(character)

    return characters


def determine_gender(hyps, object_state):
    if object_state == 'p':
        return 'n'
    elif object_state == 'a':
        if hyps & MALE_SYNSETS:
            return 'm'
        elif hyps & FEMALE_SYNSETS:
            return 'f'


def determine_object_state(hyps):
    if hyps & ANIMATE_SYNSETS:
        return 'a'
    elif hyps & PHYSICAL_SYNSETS:
        return 'p'
    else:
        return 'n'