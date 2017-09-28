from enums import ImportCategory

class Player:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

        self.team = ''
        self.positions = []
        self.games_played = 0
        self.stats = dict()

    def name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_points(self):
        # TODO: Create a general get_league_category function
        return (
            int(self.stats[ImportCategory.GOAL]) +
            int(self.stats[ImportCategory.ASSIST]))

    def __repr__(self):
        return '"' + self.name() + ' ' + self.team + '"'