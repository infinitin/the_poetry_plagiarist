__author__ = 'Nitin'
import xml.etree.ElementTree as ET
import random

luIndex = ET.parse('C:\\Python27\\nltk_data\corpora\\framenet_v15\\luIndex.xml')
root = luIndex.getroot()


def random_lu(frames):
    all_lus = [lu for lu in root.findall('lu') if lu.get('frameName') in frames]
    all_finished_frame_lus = [lu for lu in all_lus if lu.get('status') == 'Finished_Initial']
    if all_finished_frame_lus:
        return random.choice(all_finished_frame_lus).get('ID')
    else:
        return random.choice(all_lus).get('ID')


def valence_pattern(lu_id):
    lu_entry = ET.parse('C:\\Python27\\nltk_data\corpora\\framenet_v15\\lu\\lu' + lu_id + '.xml')
    lu = lu_entry.getroot()

    max_fe_group = None
    max_total = 0
    for group in lu.findall('FEGroupRealization'):
        if group.get('total') > max_total:
            max_fe_group = group
            max_total = group.get('total')

    if not max_total:
        raise Exception("No FE Group found for LU " + str(lu_id))

    #The order given in the group is not necessarily the order in the sentence
    #We could either look up the order in the annoSets, which would be quite accurate
    #But an easier heuristic would be to look at the GF attribute of the valenceUnit
    #Dep always comes *last*, then Obj, then we take the order it came in
    pattern = random.choice(max_fe_group)
    starters = [valenceUnit for valenceUnit in pattern.findall('valenceUnit') if valenceUnit.get('GF') != 'Dep' and valenceUnit.get('GF') != 'Obj']
    objs = [valenceUnit for valenceUnit in pattern.findall('valenceUnit') if valenceUnit.get('GF') == 'Obj']
    deps = [valenceUnit for valenceUnit in pattern.findall('valenceUnit') if valenceUnit.get('GF') == 'Dep']

    return starters + objs + deps


def frames(word, pos):
    pass