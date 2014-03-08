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