__author__ = 'Nitin'
import xml.etree.ElementTree as ET
import random

luIndex = ET.parse('C:\\Python27\\nltk_data\corpora\\framenet_v15\\luIndex.xml')
root = luIndex.getroot()
pre_tag = '{http://framenet.icsi.berkeley.edu}'


def lu_from_frames(frames):
    all_lus = [lu for lu in root.findall(pre_tag + 'lu') if lu.get('frameName') in frames]
    all_finished_frame_lus = [lu for lu in all_lus if lu.get('status') == 'Finished_Initial']
    if all_finished_frame_lus:
        return random.choice(all_finished_frame_lus)
    else:
        return random.choice(all_lus)


def valence_pattern_from_id(lu_id):
    lu_entry = ET.parse('C:\\Python27\\nltk_data\corpora\\framenet_v15\\lu\\lu' + lu_id + '.xml')
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
        raise Exception("No FE Group found for LU " + str(lu_id))

    #The order given in the group is not necessarily the order in the sentence
    #We could either look up the order in the annoSets, which would be quite accurate
    #But an easier heuristic would be to look at the GF attribute of the valenceUnit
    #Dep always comes *last*, then Obj, then we take the order it came in
    pattern = random.choice(max_fe_group.findall(pre_tag + 'pattern'))
    starters = [valenceUnit for valenceUnit in pattern.findall(pre_tag + 'valenceUnit') if valenceUnit.get('GF') != 'Dep' and valenceUnit.get('GF') != 'Obj']
    objs = [valenceUnit for valenceUnit in pattern.findall(pre_tag + 'valenceUnit') if valenceUnit.get('GF') == 'Obj']
    deps = [valenceUnit for valenceUnit in pattern.findall(pre_tag + 'valenceUnit') if valenceUnit.get('GF') == 'Dep']

    if not starters + objs + deps:
        raise Exception('Where did they go?')

    return starters + objs + deps


#Must be in lowercase. POS must be (converted to): n, v, a, adv, intj, prep, num
def lu_from_word(word, pos):
    lu_name = str(word) + '.' + str(pos)
    lus = [lu for lu in root.findall(pre_tag + 'lu') if lu.get('name') == lu_name]
    finished_frame_lus = [lu for lu in lus if lu.get('status') == 'Finished_Initial']
    if finished_frame_lus:
        return random.choice(finished_frame_lus)
    else:
        return random.choice(lus)