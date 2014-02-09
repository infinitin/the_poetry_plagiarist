__author__ = 'Nitin'
from pattern.text.en import lemma as lemmatise

frame_relations = {}

NEGATIVE_EXPERIENCES = {'abhor', 'abhorrence', 'abominate', 'afraid', 'antipathy', 'apprehensive', 'despair',
                        'desperation', 'despise', 'detest', 'detestation', 'discomfort', 'dislike', 'dislike',
                        'dissatisfied', 'dread', 'envy', 'fazed', 'fear', 'fed up', 'feverish', 'feverishly', 'grieve',
                        'hate', 'hatred', 'intimidated', 'irritated', 'loathe', 'loathing', 'mourn', 'nervous',
                        'nettled', 'pity', 'regret', 'resent', 'resentment', 'rue', 'rueful', 'scared',
                        'terrified', 'upset', 'worked up', 'worried'}


def build_candidate_relations_from_frames(json, dependencies, characters):
    build_frame_relations()
    candidate_relations = {}
    frames = json["sentences"][0]["frames"]
    for frame in frames:
        try:
            candidate_relation_template = frame_relations[frame["target"]["name"]]
            candidate_relation = fill_relation_template(candidate_relation_template, frame)

            if not validate_relation_syntax(candidate_relation, frame["target"]["text"], dependencies):
                print 'The operative word is not of the right POS'
                continue

            if not validate_relation_semantics(candidate_relation, dependencies):
                print 'The relation parameters are not of the correct semtype'
                continue

            accept_if_complete(candidate_relation, characters)
            candidate_relations[frame["target"]["text"]] = candidate_relation
        except KeyError:
            continue

    return candidate_relations


def accept_if_complete(candidate_relation, characters):
    #Check for completion
    for param in candidate_relation:
        if not param:
            #Actually, turn this into a Syntax instruction
            return

    subject_text = candidate_relation[0]
    relation_type = candidate_relation[1]
    for character in characters:
        if subject_text in character.text:
            character.add_relation(relation_type, candidate_relation[2])


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


def check_desirability_polarity(target):
    polarity = ''
    lemma = lemmatise(target)
    if lemma in NEGATIVE_EXPERIENCES:
        polarity = 'Not'
    #check if it is in the list of negatives
    return polarity


def check_special_params(param, frame):
    original = param
    frame_elements = frame["annotationSets"][0]["frameElements"]
    if '"' in param:
        param.replace('"', '')
        words = param.split(' ')
        try:
            words[-1] = get_element_text(words[-1], frame_elements)
            param = ' '.join(words)
        except KeyError:
            param = ''

    elif '/' in param:
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


def get_element_text(element_name, frame_elements):
    for element in frame_elements:
        if element["name"] == element_name:
            return element["text"]

    return ''


def validate_relation_syntax(candidate_relation, word, dependencies):
    #Make sure that the operative word is the pos that Framenet expects

    #Get the LUs for this relation
    #Get word out of that set
    #Check its type up against the type stored in dependencies
    #return the result

    return True


def validate_relation_semantics(candidate_relation, dependencies):
    #Make sure that the operative parameters are of the semtype that Framenet expects

    #Map the relation parameter TYPE to the word(s) itself
    #Check the semtype of that paramater TYPE
    #Get the noun out of the words
    #Check its character object for the object_state
    #Match up the object_State and the semtype
    #return the result

    return True


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

    frame_relations['Substance'] = ('Syntax: Noun After', 'MadeOf', 'Substance')

    frame_relations['Causes'] = ('Cause_to_start', 'Causes', 'Effect')
    frame_relations['Causation'] = ('Actor', 'Causes', 'Affected')
    frame_relations['Causation'] = ('Cause', 'Causes', 'Effect')
    frame_relations['Condition_Symptom_Relation'] = ('Medical_condition', 'Causes', 'Symptom')
    frame_relations['Corroding_caused'] = ('Cause', 'Causes', '"Corrosion of " Undergoer')
    frame_relations['Cognitive_connection'] = ('Concept_1', 'Causes', 'Concept_2')
    #if not above and startswith('Cause'), Cause, endofcategory (e.g. Cause_to_wake)
    frame_relations[''] = ('', 'Causes', '')

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

    frame_relations['Used_up'] = ('Syntax: Subject', 'NotHas', 'Resource')
    frame_relations['Expend_resource'] = ('Syntax: Subject', 'NotHas', 'Resource')
    frame_relations['Abandonment'] = ('Agent', 'NotHas', 'Theme')

    frame_relations['Being_named'] = ('Entity', 'Named', 'Name')

    frame_relations['Awareness'] = ('Cognizer', 'Belief', 'Content')
    frame_relations['Certainty'] = ('Cognizer', 'Belief', 'Content')
    frame_relations['Religious_belief'] = ('Believer', 'Belief', 'Content')
    frame_relations['Trust'] = ('Cognizer', 'Belief', 'Information')
    frame_relations['Opinion'] = ('Cognizer', 'Belief', 'Opinion')

    frame_relations['Communication'] = ('Communicator', 'Communication', 'Message/Topic', 'Addressee')
    frame_relations['Telling'] = ('Speaker', 'Communication', 'Message', 'Addressee')
    frame_relations['Request'] = ('Speaker', 'Communication', 'Message', 'Addressee')
    frame_relations['Speak_on_topic'] = ('Speaker', 'Communication', 'Topic', 'Audience')
    frame_relations['Statement'] = ('Speaker', 'Communication', 'Message/Topic', 'Addressee')
    frame_relations['Prevarication'] = ('Speaker', 'Communication', 'Topic', 'Addressee')
    frame_relations['Reporting'] = ('Informer', 'Communication', 'Behaviour/Wrongdoer', 'Authorities')
    frame_relations['Text_creation'] = ('Author', 'Communication', 'Text', 'Addressee')
    frame_relations['Chatting'] = ('Interlocutor_1', 'Communication', 'Topic', 'Interlocutor_2')

    frame_relations['Relation'] = ('Entitiy_1', 'Relation', 'Relation_type', 'Entity_2')
    frame_relations['Relation_between_individuals'] = ('Individual_1', 'Relation', 'Relation', 'Individual_2')
    frame_relations['Social_connection'] = ('Individual_1', 'Relation', 'Connection', 'Individual_2')
    frame_relations['Kinship'] = ('Alter', 'Relation', 'OpWord', 'Ego')
    frame_relations['Personal_relationship'] = ('Partner_1', 'Relation', 'Relationship', 'Partner_2')