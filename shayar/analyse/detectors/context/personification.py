__author__ = 'Nitin'
from relation_builder import get_all_related_dependencies


personification_relations = {'Named', 'NotNamed', 'Desires', 'NotDesires', 'Believes', 'NotBelieves', 'SendMessage',
                             'NotSendMessage', 'ReceiveMessage', 'NotReceiveMessage'}


def determine_personification(characters, frames, dependencies):
    sentient_frame_targets = find_sentient_frames(frames)
    for character in characters:
        if character.object_state == 'p':
            detect_personification_relations(character)
            if character.personification:
                continue
            detect_personification_frames(character, sentient_frame_targets, dependencies)


def find_sentient_frames(frames):
    sentient_frame_targets = []

    for frame in frames:
        target = frame["target"]["name"]
        parameters = frame["annotationSets"][0]["frameElements"]
        # Look up the frame (target) in framenet
        # See if any of the parameters need sentient
        # If so, add frame["target"]["text"] to list

    return sentient_frame_targets


def detect_personification_relations(character):
    for relation in personification_relations:
        if character.type_to_list[relation]:
            character.personification = True
            return


def detect_personification_frames(character, sentient_frame_targets, dependencies):
    for dependency in dependencies:
        if character.character_id == dependency['ID']:
            # Related dependencies are the ones that might create a relation for a particular character.
            related_dependencies = get_all_related_dependencies(dependency, dependencies)
            for related_dependency in related_dependencies:
                for target in sentient_frame_targets:
                    if target in related_dependency[1]['FORM']:
                        character.personification = True
                        return