__author__ = 'Nitin'
from collections import defaultdict
from pattern.text.en import tag
import logging


def agg_similes(poems, template):
    logging.info('Starting aggregator: agg_similes')
    template.similes = [not not poem.similes for poem in poems]
    logging.info('Aggregator finished: agg_similes')


def agg_character_count(poems, template):
    logging.info('Starting aggregator: agg_character_count')

    for poem in poems:
        n = 0
        for character in poem.characters:
            for word, pos in tag(character.text):
                if pos.startswith('N') and word != 'of':
                    n += 1
                    continue
        if n > 0:
            template.character_count.append(n)

    logging.info('Aggregator finished: agg_character_count')


def agg_character_gender(poems, template):
    logging.info('Starting aggregator: agg_character_gender')
    characters = []
    for poem in poems:
        characters.extend(poem.characters)

    for character in characters:
        if not character.gender:
            template.character_genders.append('unknown')
        elif character.gender == 'm':
            template.character_genders.append('male')
        elif character.gender == 'f':
            template.character_genders.append('female')
        elif character.gender == 'n':
            template.character_genders.append('neutral')

    logging.info('Aggregator finished: agg_character_gender')


def agg_character_num(poems, template):
    logging.info('Starting aggregator: agg_character_num')
    characters = []
    for poem in poems:
        characters.extend(poem.characters)
    template.character_nums = [character.num for character in characters]
    logging.info('Aggregator finished: agg_character_num')


def agg_character_animation(poems, template):
    logging.info('Starting aggregator: agg_character_animation')
    characters = []
    for poem in poems:
        characters.extend(poem.characters)

    for character in characters:
        if not character.object_state:
            template.character_animations.append('unknown')
        elif character.object_state == 'a':
            template.character_animations.append('animate')
        elif character.object_state == 'p':
            template.character_animations.append('physical')
        elif character.object_state == 'n':
            template.character_animations.append('non-object')

    logging.info('Aggregator finished: agg_character_animation')


def agg_character_personification(poems, template):
    logging.info('Starting aggregator: agg_character_personification')
    characters = []
    for poem in poems:
        characters.extend(poem.characters)
    template.character_personifications = [character.personification for character in characters]
    logging.info('Aggregator finished: agg_character_personification')


def agg_character_relations(poems, template):
    logging.info('Starting aggregator: agg_character_relations')
    characters = []
    for poem in poems:
        characters.extend(poem.characters)

    relations = characters[0].type_to_list.keys()
    relations_dict = defaultdict(int)
    for character in characters:
        for relation in relations:
            relations_dict[relation] += len(character.type_to_list[relation])

    template.character_relations = relations_dict
    logging.info('Aggregator finished: agg_character_relations')


def agg_character_relation_distribution(poems, template):
    logging.info('Starting aggregator: agg_character_relation_distribution')
    max_num_characters = max([len(poem.characters) for poem in poems])
    #The first list in the heirarchy contains the characters with the most relations.
    # The number of relations decreases as you go down the heirarchy.
    character_heirarchy = [[] for i in range(max_num_characters)]

    for poem in poems:
        ordered_characters = sort_characters_by_num_relations(poem.characters)
        for n in range(0, len(ordered_characters)):
            character_heirarchy[n].append(ordered_characters[n])

    template.character_relation_distribution = [relation_distribution(level) for level in character_heirarchy]

    logging.info('Aggregator finished: agg_character_relation_distribution')


def sort_characters_by_num_relations(characters):
    totals = [0] * len(characters)
    for n in range(0, len(characters)):
        totals[n] = len([entry for relation in characters[n].type_to_list.values() for entry in relation])

    return [character for (total, character) in sorted(zip(totals, characters))]


def relation_distribution(characters):
    sums = defaultdict(float)
    for character in characters:
        for relation in character.type_to_list.keys():
            sums[relation] += len(character.type_to_list[relation])

    for relation in sums.keys():
        sums[relation] /= len(characters)

    return sums