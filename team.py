class Team:

    def __init__(self, id, draft_strategy):
        self.id = id
        self.draft_strategy = draft_strategy
        self.roster = []

    def add_to_roster(self, player):
        self.roster.append(player)

    def __repr__(self):
        return 'Team ' + str(self.id) + ' [' + self.draft_strategy.__class__.__name__ + ']'