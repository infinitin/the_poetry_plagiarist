__author__ = 'Nitin'
from difflib import get_close_matches
from shayar.analyse.detectors.utils import ono_type_map

ono_relation_map_top = {
    'coins': 'IsA money',
    'weapon': 'IsA weapon',
    'hard_hit': 'ReceivesAction hard hit',
    'punch': 'ReceivesAction punch',
    'fall': 'TakesAction fall',
    'light_hit': 'ReceivesAction light hit',
    'automotive': 'IsA automotive',
    'engine': 'Has engine',
    'frog': 'IsA frog',
    'cat': 'IsA cat',
    'dog': 'IsA dog',
    'bird': 'IsA bird'
}

ono_relation_map_bottom = {
    'laughter': 'TakesAction laugh',
    'laughing': 'TakesAction laugh',
    'rubber': 'MadeOf rubber',
    'music': 'HasProperty musical',
    'disease': 'HasProperty ill',
    'surprise': 'HasProperty surprised',
    'dismay': 'HasProperty dismay',
    'pain': 'HasProperty in pain',
    'telephone': 'HasA ringer',
    'siren': 'HasA siren',
    'liquid': 'HasProperty wet',
    'water': 'HasProperty wet',
    'wet': 'HasProperty wet',
    'rain': 'HasProperty wet',
    'metal': 'MadeOf metal',
    'hit': 'RecievesAction hit',
    'electronic': 'HasProperty electronic',
    'static': 'HasProperty electronic',
    'electric': 'HasProperty electronic',
    'television': 'HasProperty electronic',
    'video games': 'HasProperty electronic',
    'animal': 'IsA animal'
}


def add_onomatopoeia_relations(form, character):
    ono = []
    for onomato in ono_type_map.keys():
        if set(form.split(' ')) & set(onomato.split(' ')):
            ono = [onomato]
        else:
            ono = get_close_matches(form, ono_type_map.keys(), 1, 0.9)

    if ono:
        relation = 'MakesSound'
        character.add_relation(relation, form)
        types_string = ono_type_map[ono]
        ono_types = types_string.split(',')
        for ono_type in ono_types:
            try:
                bonus_relation = ono_relation_map_top[ono_type.strip()]
                relation = bonus_relation.split(' ')[0]
                character.add_relation(relation, bonus_relation[len(relation) + 1:])
                return
            except KeyError:
                continue

        for ono_type in ono_types:
            try:
                bonus_relation = ono_relation_map_bottom[ono_type.strip()]
                relation = bonus_relation.split(' ')[0]
                character.add_relation(relation, bonus_relation[len(relation) + 1:])
                return
            except KeyError:
                continue

