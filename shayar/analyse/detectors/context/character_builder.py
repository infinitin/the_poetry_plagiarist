__author__ = 'Nitin'

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
                   [s.gloss for s in wordnet.synsets('prince')])

FEMALE_SYNSETS = set([s.gloss for s in wordnet.synsets('female')] +
                     [s.gloss for s in wordnet.synsets('woman')] +
                     [s.gloss for s in wordnet.synsets('wife')] +
                     [s.gloss for s in wordnet.synsets('actress')] +
                     [s.gloss for s in wordnet.synsets('female_aristocrat')] +
                     [s.gloss for s in wordnet.synsets('mother')] +
                     [s.gloss for s in wordnet.synsets('sister')] +
                     [s.gloss for s in wordnet.synsets('daughter')] +
                     [s.gloss for s in wordnet.synsets('queen')] +
                     [s.gloss for s in wordnet.synsets('princess')])

ANIMATE_SYNSETS = set([s.gloss for s in wordnet.synsets('animate thing')])
PHYSICAL_SYNSETS = set([s.gloss for s in wordnet.synsets('physical object')])

PLURAL_PRONOUNS = ['ours', 'ourselves', 'theirs', 'them', 'themselves', 'they', 'us', 'our', 'ours', 'their']
MALE_PRONOUNS = ['him', 'himself', 'hisself', 'his']
FEMALE_PRONOUNS = ['hers', 'herself', 'she', 'her']
NEUTRAL_PRONOUNS = ['it', 'itself', 'one', 'oneself', 'ownself', 'self']

NEXT_CHARACTER_ID = 0
ENTITY_ID = -1
ENTITY_CHARACTER = None


def create_characters(dependencies, frames):
    quantity = ''
    entity = ''
    for frame in frames:
        if frame["target"]["name"] == 'Quantity':
            if len(frame["annotationSets"][0]["frameElements"]) > 1:
                quantity = frame["annotationSets"][0]["frameElements"][0]["text"]
                entity = frame["annotationSets"][0]["frameElements"][1]["text"]

            break

    characters = {}
    for dependency in dependencies:
        cpostag = dependency['CPOSTAG']
        if not (cpostag.startswith('N') or cpostag.startswith('PR')):
            dependency['CHARACTER_ID'] = ''
            continue

        global NEXT_CHARACTER_ID
        global ENTITY_ID
        word = dependency['FORM']
        form = word

        if word in entity:
            form = quantity + ' ' + entity
            if ENTITY_ID >= 0:
                dependency['CHARACTER_ID'] = str(ENTITY_ID)
            else:
                dependency['CHARACTER_ID'] = str(NEXT_CHARACTER_ID)
                ENTITY_ID = NEXT_CHARACTER_ID
                NEXT_CHARACTER_ID += 1

        elif word in quantity:
            if ENTITY_ID >= 0:
                dependency['CHARACTER_ID'] = str(ENTITY_ID)
            else:
                dependency['CHARACTER_ID'] = str(NEXT_CHARACTER_ID)
                ENTITY_ID = NEXT_CHARACTER_ID
                NEXT_CHARACTER_ID += 1
            continue

        else:
            dependency['CHARACTER_ID'] = str(NEXT_CHARACTER_ID)
            NEXT_CHARACTER_ID += 1

        gender = ''
        object_state = ''

        if dependency['CPOSTAG'].startswith('P'):
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

            try:
                synset = wordnet.synsets(singularize(lemmatise(word)))[0]
            except IndexError:
                print "Failed to find synset for " + word
                continue

            hyps = set([h.gloss for h in synset.hypernyms(recursive=True)])
            hyps.add(synset.gloss)

            if hyps & ANIMATE_SYNSETS:
                object_state = 'a'
            elif hyps & PHYSICAL_SYNSETS:
                object_state = 'p'
            else:
                object_state = 'n'

            if object_state == 'p':
                gender = 'n'
            elif object_state == 'a':
                if hyps & MALE_SYNSETS:
                    gender = 'm'
                elif hyps & FEMALE_SYNSETS:
                    gender = 'f'

        character = Character(dependency['CHARACTER_ID'], num, gender, object_state)
        character.is_a.append(form)
        characters[dependency['ID']] = character
        if word in entity:
            global ENTITY_CHARACTER
            ENTITY_CHARACTER = character

    for dependency in dependencies:
        word = dependency['FORM']
        cpostag = dependency['CPOSTAG']
        if word in quantity and (cpostag.startswith('N') or cpostag.startswith('PR')):
            characters[dependency['ID']] = ENTITY_CHARACTER
            break

    return characters