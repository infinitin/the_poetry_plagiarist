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

PLURAL_PRONOUNS = {'ours', 'ourselves', 'theirs', 'them', 'themselves', 'they', 'us', 'our', 'ours', 'their'}
MALE_PRONOUNS = {'him', 'himself', 'hisself', 'his'}
FEMALE_PRONOUNS = {'hers', 'herself', 'she', 'her'}
NEUTRAL_PRONOUNS = {'it', 'itself', 'one', 'oneself', 'ownself', 'self'}

NEXT_CHARACTER_ID = 0


def create_characters(dependencies):
    characters = {}
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

            if gender == 'm' or gender == 'f':
                object_state = 'a'

        else:
            if dependency['POSTAG'].endswith('S'):
                num = 'pl'
            else:
                num = 'sg'

            try:
                synset = wordnet.synsets(singularize(lemmatise(words[-1])))[0]
            except IndexError:
                print "Failed to find synset for '" + words[-1] + "'"
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
        character.text = form
        character.add_relation("IsA", form)
        characters[dependency['ID']] = character

    return characters