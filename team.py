class Team:

    def __init__(self, team_id, draft_strategy):
        self.team_id = team_id
        self.draft_strategy = draft_strategy
        self.roster = []

    def add_to_roster(self, player):
        self.roster.append(player)

    def __repr__(self):
        return 'Team ' + str(self.team_id) + ' [' + self.draft_strategy.__class__.__name__ + ']'