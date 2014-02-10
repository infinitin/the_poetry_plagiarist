__author__ = 'Nitin'


class Character:

    def __init__(self, character_id, num, gender, object_state):

        self.character_id = character_id      # id given from dependencies
        self.gender = gender                  # 'm', 'f' or 'n', '' if cannot make a commitment
        self.num = num                        # 'sg' or 'pl'
        self.object_state = object_state      # 'a' for animate, 'p' for physical object, 'n' for not an object

        self.text = ""               # Text in the poem referring to it

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

    def __str__(self):
        if self.num == 'pl':
            pr = 'They are'
        else: 
            pr = 'It is'
            if self.gender ==  'm':
                pr = 'He is'
            elif self.gender == 'f':
                pr = 'She is'

        return "This character is represented by the text: '" + self.text + "'.\n\n" + \
            pr + " named " + str(self.named) + "\nbut not named " + str(self.not_named) + ".\n\n" +\
            pr + " " + str(self.is_a) + "\nbut not " + str(self.not_is_a) + ".\n\n" +\
            pr + "has the properties " + str(self.has_property) + "\nbut not the properties " + str(self.not_has_property) + ".\n\n" +\
            pr + "has " + str(self.has_a) + "\nbut doesn't have " + str(self.not_has_a) + ".\n\n" +\
            pr + " part of " + str(self.part_of) + "\nbut not part of " + str(self.not_part_of) + ".\n\n" +\
            pr + " capable of " + str(self.capable_of) + "\nbut not capable of " + str(self.not_capable_of) + ".\n\n" +\
            pr + "can generally be found near " + str(self.at_location) + "\nbut not near " + str(self.not_at_location) + ".\n\n" +\
            pr + "generally has " + str(self.receives_action) + "\nhappen to it but not so much " + str(self.not_receives_action) + ".\n\n" +\
            pr + "generally does " + str(self.takes_action) + "\nbut not so much " + str(self.not_receives_action) + ".\n\n" +\
            pr + " created by " + str(self.created_by) + "\nbut not by " + str(self.not_created_by) + ".\n\n" +\
            pr + " used for " + str(self.used_for) + "\nbut not for " + str(self.not_used_for) + ".\n\n" +\
            pr + " desires " + str(self.desires) + "\nbut doesn't want " + str(self.not_desires) + ".\n\n" +\
            pr + " made of " + str(self.made_of) + "\nbut not " + str(self.not_made_of) + ".\n\n"

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