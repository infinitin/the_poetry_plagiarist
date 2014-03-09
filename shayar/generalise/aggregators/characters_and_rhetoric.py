__author__ = 'Nitin'
from collections import defaultdict

def agg_similes(poems, template):
    template.similes = [not not poem.similes for poem in poems]


def agg_character_count(poems, template):
    template.character_count = [len(poem.characters) for poem in poems]


def agg_character_gender(poems, template):
    characters = []
    for poem in poems:
        characters.extend(poem.characters)
    template.character_genders = [character.gender for character in characters]


def agg_character_num(poems, template):
    characters = []
    for poem in poems:
        characters.extend(poem.characters)
    template.character_nums = [character.num for character in characters]


def agg_character_animation(poems, template):
    characters = []
    for poem in poems:
        characters.extend(poem.characters)
    template.character_animations = [character.object_state for character in characters]


def agg_character_personification(poems, template):
    characters = []
    for poem in poems:
        characters.extend(poem.characters)
    template.character_personifications = [character.personification for character in characters]


def agg_character_relations(poems, template):
    characters = []
    for poem in poems:
        characters.extend(poem.characters)

    relations = characters[0].type_to_list.keys()
    relations_dict = defaultdict(int)
    for character in characters:
        for relation in relations:
            relations_dict[relation] += len(character.type_to_list[relation])

    template.character_relations = relations_dict


def agg_character_relation_distribution(poems, template):
    max_num_characters = max([len(poem.characters) for poem in poems])
    character_heirarchy = [[] for i in range(max_num_characters)]

    for poem in poems:
        ordered_characters = sort_characters(poem.characters)
        for n in range(0, len(ordered_characters)):
            character_heirarchy[n].append(ordered_characters[n])

    template.character_relation_distribution = [relation_distribution(level) for level in character_heirarchy]
    print str(template.character_relation_distribution)


def sort_characters(characters):
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