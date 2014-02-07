__author__ = 'Nitin'


class Character:

    def __init__(self, character_id, num, gender, object_state):

        self.character_id = character_id      # id given from dependencies
        self.gender = gender                  # 'm', 'f' or 'n', '' if cannot make a commitment
        self.num = num                        # 'sg' or 'pl'
        self.object_state = object_state      # 'a' for animate, 'p' for physical object, 'n' for not an object

        self.named = []              # list of Named tuples
        self.is_a = []               # list of IsA tuples
        self.has_a = []              # list of HasA tuples
        self.part_of = []            # list of PartOf tuples
        self.capable_of = []         # list of CapableOf tuples
        self.at_location = []        # list of NearLocation tuples
        self.receives_action = []    # list of ReceivesAction tuples
        self.created_by = []         # list of CreatedBy tuples
        self.used_for = []           # list of UsedFor tuples
        self.desires = []            # list of Desires tuples
        self.has_property = []       # list of HasProperty tuples

