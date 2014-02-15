__author__ = 'Nitin'


class Character:
    def __init__(self, character_id, num, gender, object_state):

        self.character_id = character_id      # id given from dependencies
        self.gender = gender                  # 'm', 'f' or 'n', '' if cannot make a commitment
        self.num = num                        # 'sg' or 'pl'
        self.object_state = object_state      # 'a' for animate, 'p' for physical object, 'n' for not an object

        self.text = ""               # Text in the poem referring to it
        self.is_pronoun = False      # Whether or not it is a pronoun (and needs to be resolved)

        self.type_to_list = {
            'Named': list(),
            'IsA': list(),
            'HasProperty': list(),
            'HasA': list(),
            'PartOf': list(),
            'CapableOf': list(),
            'AtLocation': list(),
            'ReceivesAction': list(),
            'TakesAction': list(),
            'CreatedBy': list(),
            'UsedFor': list(),
            'Desires': list(),
            'MadeOf': list(),
            'Believes': list(),
            'SendMessage': list(),
            'ReceiveMessage': list(),

            'NotNamed': list(),
            'NotIsA': list(),
            'NotHasProperty': list(),
            'NotHasA': list(),
            'NotPartOf': list(),
            'NotCapableOf': list(),
            'NotAtLocation': list(),
            'NotReceivesAction': list(),
            'NotTakesAction': list(),
            'NotCreatedBy': list(),
            'NotUsedFor': list(),
            'NotDesires': list(),
            'NotMadeOf': list(),
            'NotBelieves': list(),
            'NotSendMessage': list(),
            'NotReceiveMessage': list(),
        }

    def __str__(self):
        return_text = "This character is represented by the text: '" + self.text + "'.\n"

        if self.gender == 'm':
            if self.num == 'sg':
                return_text += "He is male.\n"
            else:
                return_text += "They are male.\n"
        elif self.gender == 'f':
            if self.num == 'sg':
                return_text += "She is female.\n"
            else:
                return_text += "They are female.\n"
        else:
            if self.num == 'sg':
                if self.object_state == 'a':
                    return_text += "It is a living thing.\n"
                elif self.object_state == 'p':
                    return_text += "It is a physical object.\n"
                else:
                    return_text += "It is not a physical object.\n"
            else:
                if self.object_state == 'a':
                    return_text += "They are a living things.\n"
                elif self.object_state == 'p':
                    return_text += "They are physical objects.\n"
                else:
                    return_text += "They are not physical objects.\n"

        for relation_type in self.type_to_list.keys():
            for elem in self.type_to_list[relation_type]:
                return_text += relation_type + ": " + elem + ".\n"
        
        return return_text

    def add_relation(self, relation_type, text):
        relation_list = self.type_to_list[relation_type]
        if text not in relation_list:
            relation_list.append(text)
