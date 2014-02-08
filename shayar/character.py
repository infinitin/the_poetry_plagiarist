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
        self.has_a = []              # list of HasA
        self.part_of = []            # list of PartOf
        self.capable_of = []         # list of CapableOf
        self.at_location = []        # list of NearLocation
        self.receives_action = []    # list of ReceivesAction
        self.created_by = []         # list of CreatedBy
        self.used_for = []           # list of UsedFor
        self.desires = []            # list of Desires
        self.made_of = []            # list of MadeOf

    def add_relation(self, type, text):
        if type == 'Named':
            self.desires.append(text)
        if type == 'IsA':
            self.is_a.append(text)
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
        if type == 'CreatedBy':
            self.created_by.append(text)
        if type == 'UsedFor':
            self.used_for.append(text)
        if type == 'Desires':
            self.desires.append(text)
        if type == 'MadeOf':
            self.made_of.append(text)