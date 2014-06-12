__author__ = 'Nitin'
from shayar.character import Character
from shayar.knowledge.knowledge import get_synset
from shayar.analyse.detectors.context.character_builder import determine_gender, determine_object_state


def create_new_character(noun, character_id):
    synset = get_synset(noun, pos='N')
    if not synset:
        animation = ''
        gender = ''
    else:
        hyps = set()
        for h in synset.hypernyms(recursive=True):
            try:
                hyps.add(h)
            except ValueError:
                continue

        hyps.add(synset)
        animation = determine_object_state(hyps)
        gender = determine_gender(hyps, animation)

    new_character = Character(character_id, 'sg', gender, animation)
    new_character.add_relation('IsA', noun)

    return new_character