__author__ = 'Nitin'


def detect_personification(characters):
    personified_characters = []
    for character in characters:
        if character.object_state == 'p':
            personified_characters.extend(detect_personification_relations(character))
            #personified_characters.extend(detect_personification_actions(character))
            #personified_characters.extend(detect_personification_descriptions(character))

    return personified_characters


def detect_personification_relations(character):
    personification_relations = {'Named', 'NotNamed', 'Desires', 'NotDesires', 'Believes', 'NotBelieves', 'SendMessage',
                                 'NotSendMessage', 'ReceiveMessage', 'NotReceiveMessage'}
    personified_characters = []
    for relation in personification_relations:
        if character.type_to_list[relation]:
            personified_characters.append(character)

    return personified_characters