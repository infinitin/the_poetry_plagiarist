__author__ = 'Nitin'


class Character:

    def __init__(self):
        self.gender = ''             # 'm', 'f' or 'n'
        self.num = ''                # 'sg' or 'pl'

        self.is_a = []               # array of IsA relations
        self.has_a = []              # array of HasA relations
        self.part_of = []            # array of PartOf relations
        self.capable_of = []         # array of CapableOf relations
        self.near_location = []      # array of NearLocation relations
        self.receives_action = []    # array of ReceivesAction relations
        self.created_by = []         # array of CreatedBy relations
        self.used_for = []           # array of UsedFor relations
        self.desires = []            # array of Desires relations
        self.has_property = []       # array of HasProperty relations

