__author__ = 'Nitin'
import xml.etree.ElementTree as Et
import random
import logging

FRAMENET_DATA_LOC = 'C:\\Python27\\framenet_data\\'
lu_index = Et.parse(FRAMENET_DATA_LOC + 'luIndex.xml')
root = lu_index.getroot()
pre_tag = '{http://framenet.icsi.berkeley.edu}'


def lu_from_frames(frames, pos=''):
    all_lus = [lu for lu in root.findall(pre_tag + 'lu') if lu.get('frameName') in frames]

    if pos:
        all_lus = [lu for lu in all_lus if lu.get('name').partition('.')[2] == pos]

    all_finished_frame_lus = [lu for lu in all_lus if
                              lu.get('status') == 'Finished_Initial' and not '_' in lu.get('name')]
    if all_finished_frame_lus:
        return random.choice(all_finished_frame_lus)
    else:
        return random.choice(all_lus)


def valence_pattern_from_id(lu_id):
    lu_entry = Et.parse(FRAMENET_DATA_LOC + 'lu\\lu' + lu_id + '.xml')
    lu = lu_entry.getroot()

    max_fe_group = None
    max_total = 0
    group_realizations = []
    for valence in lu.findall(pre_tag + 'valences'):
        group_realizations.extend(valence.findall(pre_tag + 'FEGroupRealization'))

    for group in group_realizations:
        if int(group.get('total')) > int(max_total):
            max_fe_group = group
            max_total = group.get('total')

    if not max_total:
        return []

    #The order given in the group is not necessarily the order in the sentence
    #We could either look up the order in the annoSets, which would be quite accurate
    #But an easier heuristic would be to look at the GF attribute of the valenceUnit
    #Dep and Obj come last
    patterns = max_fe_group.findall(pre_tag + 'pattern')
    best_pattern = random.choice(patterns)
    max_total = 0
    for pattern in patterns:
        if len(pattern.findall(pre_tag + 'valenceUnit')) <= 2 and int(pattern.get('total')) > max_total:
            best_pattern = pattern
            max_total = int(pattern.get('total'))

    starters = [valenceUnit for valenceUnit in best_pattern.findall(pre_tag + 'valenceUnit') if
                valenceUnit.get('GF') != 'Dep' and valenceUnit.get('GF') != 'Obj']
    deps = [valenceUnit for valenceUnit in best_pattern.findall(pre_tag + 'valenceUnit') if
            valenceUnit.get('GF') == 'Dep']
    objs = [valenceUnit for valenceUnit in best_pattern.findall(pre_tag + 'valenceUnit') if
            valenceUnit.get('GF') == 'Obj']

    if len(starters) + len(deps) + len(objs) > 2:
        starters = [starter for starter in starters if starter.get('GF') != '--']
        deps = [dep for dep in deps if dep.get('GF') != '--']
        objs = [obj for obj in objs if obj.get('GF') != '--']

        if len(starters) + len(deps) + len(objs) > 2:
            starters = [starters[0]] if starters else []
            deps = [deps[0]] if deps else []
            objs = [objs[0]] if objs else []

    return [tuple(starters), tuple(deps), tuple(objs)]


#Must be in lowercase. POS must be (converted to): n, v, a, adv, intj, prep, num
def lu_from_word(word, pos):
    lu_name = str(word) + '.' + str(pos)
    lus = [lu for lu in root.findall(pre_tag + 'lu') if lu.get('name') == lu_name]
    finished_frame_lus = [lu for lu in lus if lu.get('status') == 'Finished_Initial']
    if finished_frame_lus:
        return random.choice(finished_frame_lus)
    else:
        return random.choice(lus)


def strict_lu_from_word(word, pos):
    lu_name = str(word) + '.' + str(pos)
    lus = [lu for lu in root.findall(pre_tag + 'lu') if lu.get('name') == lu_name]
    finished_frame_lus = [lu for lu in lus if lu.get('status') == 'Finished_Initial']
    if finished_frame_lus:
        return random.choice(finished_frame_lus)
    else:
        raise IndexError


def lu_from_id(lu_id):
    return [lu for lu in root.findall(pre_tag + 'lu') if lu.get('ID') == lu_id][0]


simplenlg_lexicon = Et.parse('default-lexicon.xml')
word_root = simplenlg_lexicon.getroot()


#We would like to look up framenet in the future, but for now we look up the default lexicon for simplenlg
def get_random_word(pos):
    logging.warn('Getting a RANDOM word')
    category = 'noun'
    if pos.startswith('V'):
        category = 'verb'
    elif pos.startswith('AVP'):
        category = 'adverb'
    elif pos.startswith('A'):
        category = 'adjective'
    return random.choice(
        [word.find('base').text for word in word_root.findall('word') if word.find('category').text == category])


def filter_candidates(candidates, pos):
    category = 'noun'
    if pos.startswith('V'):
        category = 'verb'
    elif pos.startswith('AVP'):
        category = 'adverb'
    elif pos.startswith('A'):
        category = 'adjective'

    options = [word.find('base').text for word in word_root.findall('word') if
               word.find('base').text in candidates and word.find('category').text == category]

    if not options and pos != 'A':
        options = [word.find('base').text for word in word_root.findall('word') if
                   word.find('base').text in candidates and word.find('category').text == 'A']

    return options


def find_pos(search_word):
    return [word.find('category').text for word in word_root.findall('word') if word.find('base').text == search_word]