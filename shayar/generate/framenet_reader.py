__author__ = 'Nitin'
import xml.etree.ElementTree as ET
import random

FRAMENET_DATA_LOC = 'C:\\Python27\\framenet_data\\'
lu_index = ET.parse(FRAMENET_DATA_LOC + 'luIndex.xml')
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
    lu_entry = ET.parse(FRAMENET_DATA_LOC + 'lu\\lu' + lu_id + '.xml')
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
    #Dep always comes *last*, then Obj, then we take the order it came in
    patterns = max_fe_group.findall(pre_tag + 'pattern')
    pattern = random.choice(patterns)
    for p in patterns:
        if len(p.findall(pre_tag + 'valenceUnit')) <= 2:
            pattern = p
            break
    starters = [valenceUnit for valenceUnit in pattern.findall(pre_tag + 'valenceUnit') if
                valenceUnit.get('GF') != 'Dep' and valenceUnit.get('GF') != 'Obj']
    objs = [valenceUnit for valenceUnit in pattern.findall(pre_tag + 'valenceUnit') if valenceUnit.get('GF') == 'Obj']
    deps = [valenceUnit for valenceUnit in pattern.findall(pre_tag + 'valenceUnit') if valenceUnit.get('GF') == 'Dep']

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


simplenlg_lexicon = ET.parse('default-lexicon.xml')
word_root = simplenlg_lexicon.getroot()


#We would like to look up framenet in the future, but for now we look up the default lexicon for simplenlg
def get_random_word(pos):
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