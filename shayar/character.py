__author__ = 'Nitin'


class Character:

    def __init__(self, character_id, num, gender, object_state):

        self.character_id = character_id      # id given from dependencies
        self.gender = gender                  # 'm', 'f' or 'n', '' if cannot make a commitment
        self.num = num                        # 'sg' or 'pl'
        self.object_state = object_state      # 'a' for animate, 'p' for physical object, 'n' for not an object

        self.text = ""               # Text in the poem referring to it
        self.is_pronoun = False      # Whether or not it is a pronoun (and needs to be resolved)

        self.named = []              # list of Named
        self.is_a = []               # list of IsA
        self.has_property = []       # list of HasProperty
        self.has_a = []              # list of HasA
        self.part_of = []            # list of PartOf
        self.capable_of = []         # list of CapableOf
        self.at_location = []        # list of NearLocation
        self.receives_action = []    # list of ReceivesAction
        self.takes_action = []       # list of TakesAction
        self.created_by = []         # list of CreatedBy
        self.used_for = []           # list of UsedFor
        self.desires = []            # list of Desires
        self.made_of = []            # list of MadeOf
        self.believes = []
        self.send_message = []
        self.receive_message = []

        self.not_named = []              # list of NotNamed
        self.not_is_a = []               # list of NotIsA
        self.not_has_property = []       # list of NotHasProperty
        self.not_has_a = []              # list of NotHasA
        self.not_part_of = []            # list of NotPartOf
        self.not_capable_of = []         # list of NotCapableOf
        self.not_at_location = []        # list of NotNearLocation
        self.not_receives_action = []    # list of NotReceivesAction
        self.not_takes_action = []       # list of NotTakesAction
        self.not_created_by = []         # list of NotCreatedBy
        self.not_used_for = []           # list of NotUsedFor
        self.not_desires = []            # list of NotDesires
        self.not_made_of = []            # list of NotMadeOf
        self.not_believes = []
        self.not_send_message = []
        self.not_receive_message = []

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
                if self.object_state == 'p':
                    return_text += "It is a physical object.\n"
                else:
                    return_text += "It is not a physical object.\n"
            else:
                if self.object_state == 'p':
                    return_text += "They are physical objects.\n"
                else:
                    return_text += "They are not physical objects.\n"

        for elem in self.named:
            return_text += "Named: " + elem + ".\n"

        for elem in self.not_named:
            return_text += "NotNamed: " + elem + ".\n"

        for elem in self.is_a:
            return_text += "Is: " + elem + ".\n"

        for elem in self.not_is_a:
            return_text += "NotIs: " + elem + ".\n"

        for elem in self.has_property:
            return_text += "HasProperty: " + elem + ".\n"

        for elem in self.not_has_property:
            return_text += "NotHasProperty: " + elem + ".\n"

        for elem in self.has_a:
            return_text += "Has: " + elem + ".\n"

        for elem in self.not_has_a:
            return_text += "NotHas: " + elem + ".\n"

        for elem in self.part_of:
            return_text += "PartOf: " + elem + ".\n"

        for elem in self.not_part_of:
            return_text += "NotPartOf: " + elem + ".\n"

        for elem in self.capable_of:
            return_text += "CapableOf: " + elem + ".\n"

        for elem in self.not_capable_of:
            return_text += "NotCapableOf: " + elem + ".\n"

        for elem in self.at_location:
            return_text += "AtLocation: " + elem + ".\n"

        for elem in self.not_at_location:
            return_text += "NotAtLocation: " + elem + ".\n"

        for elem in self.receives_action:
            return_text += "ReceivesAction: " + elem + ".\n"

        for elem in self.not_receives_action:
            return_text += "NotReceivesAction: " + elem + ".\n"

        for elem in self.takes_action:
            return_text += "TakesAction: " + elem + ".\n"

        for elem in self.not_takes_action:
            return_text += "NotTakesAction: " + elem + ".\n"

        for elem in self.created_by:
            return_text += "CreatedBy: " + elem + ".\n"

        for elem in self.not_created_by:
            return_text += "NotCreatedBy: " + elem + ".\n"

        for elem in self.used_for:
            return_text += "UsedFor: " + elem + ".\n"

        for elem in self.not_used_for:
            return_text += "NotUsedFor: " + elem + ".\n"

        for elem in self.desires:
            return_text += "Desires: " + elem + ".\n"

        for elem in self.not_desires:
            return_text += "NotDesires: " + elem + ".\n"

        for elem in self.made_of:
            return_text += "MadeOf: " + elem + ".\n"

        for elem in self.not_made_of:
            return_text += "NotMadeOf: " + elem + ".\n"

        for elem in self.believes:
            return_text += "Believes: " + elem + ".\n"

        for elem in self.not_believes:
            return_text += "NotBelieves: " + elem + ".\n"

        for elem in self.send_message:
            return_text += "SendMessage: " + elem + ".\n"

        for elem in self.not_send_message:
            return_text += "NotSendMessage: " + elem + ".\n"

        for elem in self.receive_message:
            return_text += "ReceiveMessage: " + elem + ".\n"
        
        for elem in self.not_receive_message:
            return_text += "NotReceiveMessage: " + elem + ".\n"

        if self.num == 'pl':
            pr = 'They are'
        else: 
            pr = 'It is'
            if self.gender ==  'm':
                pr = 'He is'
            elif self.gender == 'f':
                pr = 'She is'

        return return_text

    def add_relation(self, type, text):
        if type == 'Named':
            self.named.append(text)
        if type == 'IsA':
            self.is_a.append(text)
        if type == 'HasProperty':
            self.has_property.append(text)
        if type == 'HasA':
            self.has_a.append(text)
        if type == 'PartOf':
            self.part_of.append(text)
        if type == 'CapableOf':
            self.capable_of.append(text)
        if type == 'AtLocation':
            self.at_location.append(text)
        if type == 'ReceivesAction':
            self.receives_action.append(text)
        if type == 'TakesAction':
            self.takes_action.append(text)
        if type == 'CreatedBy':
            self.created_by.append(text)
        if type == 'UsedFor':
            self.used_for.append(text)
        if type == 'Desires':
            self.desires.append(text)
        if type == 'MadeOf':
            self.made_of.append(text)
        if type == 'Believes':
            self.believes.append(text)
        if type == 'SendMessage':
            self.send_message.append(text)
        if type == 'ReceiveMessage':
            self.receive_message.append(text)

        if type == 'NotNamed':
            self.not_named.append(text)
        if type == 'NotIsA':
            self.not_is_a.append(text)
        if type == 'NotHasProperty':
            self.not_has_property.append(text)
        if type == 'NotHasA':
            self.not_has_a.append(text)
        if type == 'NotPartOf':
            self.not_part_of.append(text)
        if type == 'NotCapableOf':
            self.not_capable_of.append(text)
        if type == 'NotAtLocation':
            self.not_at_location.append(text)
        if type == 'NotReceivesAction':
            self.not_receives_action.append(text)
        if type == 'NotTakesAction':
            self.not_takes_action.append(text)
        if type == 'NotCreatedBy':
            self.not_created_by.append(text)
        if type == 'NotUsedFor':
            self.not_used_for.append(text)
        if type == 'NotDesires':
            self.not_desires.append(text)
        if type == 'NotMadeOf':
            self.not_made_of.append(text)
        if type == 'NotBelieves':
            self.not_believes.append(text)
        if type == 'NotSendMessage':
            self.not_send_message.append(text)
        if type == 'NotReceiveMessage':
            self.not_receive_message.append(text)