__author__ = 'Nitin'
import xml.etree.ElementTree as ET
import random

FRAMENET_DATA_LOC = 'C:\\Python27\\framenet_data\\'
lu_index = ET.parse(FRAMENET_DATA_LOC + 'luIndex.xml')
root = lu_index.getroot()
pre_tag = '{http://framenet.icsi.berkeley.edu}'


def lu_from_frames(frames):
    all_lus = [lu for lu in root.findall(pre_tag + 'lu') if lu.get('frameName') in frames]
    all_finished_frame_lus = [lu for lu in all_lus if lu.get('status') == 'Finished_Initial' and not '_' in lu.get('name')]
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
        if group.get('total') > max_total:
            max_fe_group = group
            max_total = group.get('total')

    if not max_total:
        raise Exception("No FE Group found for LU " + str(lu_id))  # FIXME: Find a synonym, don't just die.

    #The order given in the group is not necessarily the order in the sentence
    #We could either look up the order in the annoSets, which would be quite accurate
    #But an easier heuristic would be to look at the GF attribute of the valenceUnit
    #Dep always comes *last*, then Obj, then we take the order it came in
    pattern = random.choice(max_fe_group.findall(pre_tag + 'pattern'))
    starters = [valenceUnit for valenceUnit in pattern.findall(pre_tag + 'valenceUnit') if valenceUnit.get('GF') != 'Dep' and valenceUnit.get('GF') != 'Obj']
    objs = [valenceUnit for valenceUnit in pattern.findall(pre_tag + 'valenceUnit') if valenceUnit.get('GF') == 'Obj']
    deps = [valenceUnit for valenceUnit in pattern.findall(pre_tag + 'valenceUnit') if valenceUnit.get('GF') == 'Dep']

    return [tuple(starters), tuple(objs), tuple(deps)]


#Must be in lowercase. POS must be (converted to): n, v, a, adv, intj, prep, num
def lu_from_word(word, pos):
    lu_name = str(word) + '.' + str(pos)
    lus = [lu for lu in root.findall(pre_tag + 'lu') if lu.get('name') == lu_name]
    finished_frame_lus = [lu for lu in lus if lu.get('status') == 'Finished_Initial']
    if finished_frame_lus:
        return random.choice(finished_frame_lus)
    else:
        return random.choice(lus)


def lu_from_id(id):
    return [lu for lu in root.findall(pre_tag + 'lu') if lu.get('ID') == id][0]


simplenlg_lexicon = ET.parse('default-lexicon.xml')


#We would like to look up framenet in the future, but for now we look up the default lexicon for simplenlg
def get_random_word(pos):
    category = 'noun'
    if pos.startswith('V'):
        category = 'verb'
    elif pos.startswith('AVP'):
        category = 'adverb'
    elif pos.startswith('A'):
        category = 'adjective'
    word_root = simplenlg_lexicon.getroot()
    return random.choice([word.find('base').text for word in word_root.findall('word') if word.find('category').text == category])