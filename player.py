from enums import ImportCategory, LeagueCategory, Position

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

    def get_category_score(self, category):
        if category == LeagueCategory.GOAL:
          return float(self.stats[ImportCategory.GOAL])
        if category == LeagueCategory.ASSIST:
          return float(self.stats[ImportCategory.ASSIST])
        if category == LeagueCategory.PLUS_MINUS:
          return float(self.stats[ImportCategory.PLUS_MINUS])
        if category == LeagueCategory.PENALTY_MINUTES:
          return float(self.stats[ImportCategory.PENALTY_MINUTES])
        if category == LeagueCategory.POWER_PLAY_POINT:
          return float(self.stats[ImportCategory.POWER_PLAY_GOAL]) + \
              float(self.stats[ImportCategory.POWER_PLAY_ASSIST])
        if category == LeagueCategory.SHOT:
          return float(self.stats[ImportCategory.SHOT])
        if category == LeagueCategory.WIN:
          return float(self.stats[ImportCategory.WIN])
        if category == LeagueCategory.GOALS_AGAINST_AVERAGE:
          return float(self.stats[ImportCategory.GOALS_AGAINST_AVERAGE])

        if Position.GOALIE in self.positions:
            if category == LeagueCategory.WIN:
              return float(self.stats[ImportCategory.WIN])
            if category == LeagueCategory.SHUT_OUT:
              return float(self.stats[ImportCategory.SHUT_OUT])
            if category == LeagueCategory.SAVE_PERCENTAGE:
              return (float(self.stats[ImportCategory.GOALS_AGAINST]) /
                      float(self.stats[ImportCategory.SAVES]))
        else:
            # This is a player, we return 0.0 for all goalie stats.
            return 0.0

    def __repr__(self):
        return '"' + self.name() + ' ' + self.team + '"'