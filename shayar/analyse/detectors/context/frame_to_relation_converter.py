__author__ = 'Nitin'
from pattern.text.en import lemma as lemmatise

frame_relations = {}


# Some of the Experience focus lexical units carry a negative naturally
NEGATIVE_EXPERIENCES = {'abhor', 'abhorrence', 'abominate', 'afraid', 'antipathy', 'apprehensive', 'despair',
                        'desperation', 'despise', 'detest', 'detestation', 'discomfort', 'dislike', 'dislike',
                        'dissatisfied', 'dread', 'envy', 'fazed', 'fear', 'fed up', 'feverish', 'feverishly', 'grieve',
                        'hate', 'hatred', 'intimidated', 'irritated', 'loathe', 'loathing', 'mourn', 'nervous',
                        'nettled', 'pity', 'regret', 'resent', 'resentment', 'rue', 'rueful', 'scared',
                        'terrified', 'upset', 'worked up', 'worried'}


# Grab the 'target' i.e. the word that determines the type of frame from the frame semantic parse in the json
# Get the corresponding concept-frame net relation template for this target (if any)
# Fill the relation template with the parameters given from the frame semantic parse
# Add it to a map from the target
def build_candidate_relations_from_frames(frames):
    build_frame_relations()
    candidate_relations = {}
    for frame in frames:
        try:
            candidate_relation_template = frame_relations[frame["target"]["name"]]
            candidate_relation = fill_relation_template(candidate_relation_template, frame)

            candidate_relations[frame["target"]["text"]] = candidate_relation
        except KeyError:
            continue

    return candidate_relations


# Take a concept-frame net relation template and fill it in with the parameters provided in the frame-semantic parse
# If the parameter that we desire cannot be found, we just leave it blank and deal with it downstream.
# Special case for Experiencer focus because of the inherent polarity issues
# Also need to watch for the relations with more than two parameters (SendMessage etc.)
def fill_relation_template(candidate_relation_template, frame):
    #Replace the first and last tuple 'key' with the value
    relation = candidate_relation_template[1]

    if frame["target"]["name"] == 'Experiencer_focus':
        polarity = check_desirability_polarity(frame["target"]["text"])
        relation = polarity + relation

    first_param = check_special_params(candidate_relation_template[0], frame)
    second_param = check_special_params(candidate_relation_template[2], frame)

    double_relation = (first_param, relation, second_param)

    if len(candidate_relation_template) > 3:
        third_param = check_special_params(candidate_relation_template[3], frame)
        final_relation = double_relation + (third_param,)
    else:
        final_relation = double_relation

    return final_relation


# Check if the Experiencer_focus relation has a target that is negative or positive
def check_desirability_polarity(target):
    polarity = ''
    lemma = lemmatise(target)
    if lemma in NEGATIVE_EXPERIENCES:
        polarity = 'Not'

    return polarity


# Some parameters do not come straight out of the box:
# If / character, the parameter on either side of the slash
# OpWord brings in the target word as the parameter
def check_special_params(param, frame):
    original = param
    frame_elements = frame["annotationSets"][0]["frameElements"]
    if '/' in param:
        first_params = param.split('/')
        for param in first_params:
            try:
                param = get_element_text(param, frame_elements)
                break
            except KeyError:
                continue
        if param == original:
            param = ''

    elif param == "OpWord":
        param = frame["target"]["text"]

    else:
        try:
            param = get_element_text(param, frame_elements)
        except KeyError:
            param = ''

    return param


# Get the actual text of the desired parameter in the json frame sematic parse
def get_element_text(element_name, frame_elements):
    for element in frame_elements:
        if element["name"] == element_name:
            return element["text"]

    return ''


# All of the relations that have been manually selected from FrameNet, mapped from type of target
def build_frame_relations():
    #map from target text name to the relation three-tuple
    frame_relations['Architectural_part'] = ('Part', 'PartOf', 'Whole')
    frame_relations['Building_subparts'] = ('Building_part', 'PartOf', 'Whole')
    frame_relations['Clothing_parts'] = ('Subpart', 'PartOf', 'Clothing')
    frame_relations['Observable_body_parts'] = ('Body_part', 'PartOf', 'Possessor')
    frame_relations['Part_edge'] = ('Part', 'PartOf', 'Whole')
    frame_relations['Part_inner_outer'] = ('Part', 'PartOf', 'Whole')
    frame_relations['Part_ordered_segments'] = ('Part', 'PartOf', 'Whole')
    frame_relations['Part_orientational'] = ('Part', 'PartOf', 'Whole')
    frame_relations['Part_piece'] = ('Piece', 'PartOf', 'Substance')
    frame_relations['Part_whole'] = ('Part', 'PartOf', 'Whole')
    frame_relations['Shaped_part'] = ('Part', 'PartOf', 'Whole')
    frame_relations['Vehicle_subpart'] = ('Part', 'PartOf', 'Whole')
    frame_relations['Wholes_and_parts'] = ('Part', 'PartOf', 'Whole')
    frame_relations['Inclusion'] = ('Part', 'PartOf', 'Total')

    frame_relations['Creating'] = ('Created_Entity', 'CreatedBy', 'Creator')
    frame_relations['Cooking_creation'] = ('Produced_food', 'CreatedBy', 'Cook')
    frame_relations['Intentionally_create'] = ('Created_Entity', 'CreatedBy', 'Creator')
    frame_relations['Text_creation'] = ('Text', 'CreatedBy', 'Author')
    frame_relations['Manufacturing'] = ('Product', 'CreatedBy', 'Producer/Factory')

    frame_relations['Substance'] = ('', 'MadeOf', 'Substance')

    frame_relations['Desiring'] = ('Experiencer', 'Desires', 'Event')
    #Polarity of operative word needs to be checked
    frame_relations['Experiencer_focus'] = ('Experiencer', 'Desires', 'Content')

    frame_relations['Capability'] = ('Entity', 'CapableOf', 'Event')

    frame_relations['Expend_resource'] = ('Resource', 'UsedFor', 'Purpose')
    frame_relations['Using'] = ('Instrument', 'UsedFor', 'Purpose')
    frame_relations['Tool_purpose'] = ('Tool', 'UsedFor', 'Purpose')
    frame_relations['Ingest_substance'] = ('Substance', 'UsedFor', 'Purpose')
    frame_relations['Using_resource'] = ('Resource', 'UsedFor', 'Purpose')
    frame_relations['Usefulness'] = ('Entity', 'UsedFor', 'Purpose')

    frame_relations['Purpose'] = ('Means', 'MotivatedByGoal', 'Goal/Value')

    frame_relations['Possession'] = ('Owner', 'Has', 'Possession')
    frame_relations['Have_associated'] = ('Topical_entity', 'Has', 'Entity')
    frame_relations['Inclusion'] = ('Total', 'Has', 'Part')
    frame_relations['Containers'] = ('Container', 'Has', 'Contents')

    frame_relations['Used_up'] = ('', 'NotHas', 'Resource')
    frame_relations['Expend_resource'] = ('', 'NotHas', 'Resource')
    frame_relations['Abandonment'] = ('Agent', 'NotHas', 'Theme')

    frame_relations['Being_named'] = ('Entity', 'Named', 'Name')
    frame_relations['Referring_by_name'] = ('Entity', 'Named', 'Name')

    frame_relations['Awareness'] = ('Cognizer', 'Believes', 'Content')
    frame_relations['Certainty'] = ('Cognizer', 'Believes', 'Content')
    frame_relations['Religious_belief'] = ('Believer', 'Believes', 'Content')
    frame_relations['Trust'] = ('Cognizer', 'Believes', 'Information')
    frame_relations['Opinion'] = ('Cognizer', 'Believes', 'Opinion')

    frame_relations['Communication'] = ('Communicator', 'SendMessage', 'Message/Topic', 'Addressee')
    frame_relations['Telling'] = ('Speaker', 'SendMessage', 'Message', 'Addressee')
    frame_relations['Request'] = ('Speaker', 'SendMessage', 'Message', 'Addressee')
    frame_relations['Speak_on_topic'] = ('Speaker', 'SendMessage', 'Topic', 'Audience')
    frame_relations['Statement'] = ('Speaker', 'SendMessage', 'Message/Topic', 'Addressee')
    frame_relations['Prevarication'] = ('Speaker', 'SendMessage', 'Topic', 'Addressee')
    frame_relations['Reporting'] = ('Informer', 'SendMessage', 'Behaviour/Wrongdoer', 'Authorities')
    frame_relations['Text_creation'] = ('Author', 'SendMessage', 'Text', 'Addressee')
    frame_relations['Chatting'] = ('Interlocutor_1', 'SendMessage', 'Topic', 'Interlocutor_2')

    frame_relations['Being_located'] = ('Theme', 'AtLocation', 'Location')
    frame_relations['Origin_Frame'] = ('Entity', 'AtLocation', 'Origin')