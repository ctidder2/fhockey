from enums import ImportCategory, LeagueCategory, Position

def league_scores_from_import_stats(positions, import_stats, num_games=82):
    scores = dict()
    if Position.GOALIE not in positions:
        scores[LeagueCategory.GOAL] = float(import_stats[ImportCategory.GOAL])
        scores[LeagueCategory.ASSIST] = float(import_stats[ImportCategory.ASSIST])
        scores[LeagueCategory.PLUS_MINUS] = float(import_stats[ImportCategory.PLUS_MINUS])
        scores[LeagueCategory.PENALTY_MINUTES] = float(import_stats[ImportCategory.PENALTY_MINUTES])
        scores[LeagueCategory.POWER_PLAY_POINT] = (
            float(import_stats[ImportCategory.POWER_PLAY_GOAL]) +
            float(import_stats[ImportCategory.POWER_PLAY_ASSIST]))
        scores[LeagueCategory.SHOT] = float(import_stats[ImportCategory.SHOT])
    else:
        scores[LeagueCategory.WIN] = float(import_stats[ImportCategory.GOAL])
        scores[LeagueCategory.SAVE_PERCENTAGE] = (
            float(import_stats[ImportCategory.GOALS_AGAINST]) /
            (float(import_stats[ImportCategory.GOALS_AGAINST] + import_stats[ImportCategory.SAVES])))
        scores[LeagueCategory.GOALS_AGAINST_AVERAGE] = float(import_stats[ImportCategory.GOAL]) / float(num_games)
        scores[LeagueCategory.SHUT_OUT] = float(import_stats[ImportCategory.SHUT_OUT])
    return scores


class Player:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

        self.team = ''
        self.positions = []
        self.games_played = 0
        self.stats = dict()

        self.memoize_gp_league_scores = {}

    def name(self):
        return ' '.join([self.first_name, self.last_name])

    def simulate_games(self, r, cats, num_games=3):
        scoring_cats = {cat: 0 for cat in cats}
        fractions = 12
        for _ in xrange(num_games * fractions ):
            period_cat_scores = self._simulate_period(r, cats)
            for cat, score in period_cat_scores.iter_items():
                scoring_cats[cat] += score
        return scoring_cats


    def _simulate_period(self, r):
        scoring_cats = {cat: 0 for cat in cats}

        return scoring_cats

    def get_points(self):
        # TODO: Create a general get_league_category function
        return (
            int(self.stats[ImportCategory.GOAL]) +
            int(self.stats[ImportCategory.ASSIST]))

    def get_category_score(self):
        if self.games_played in self.memoize_gp_league_scores:
            return self.memoize_gp_league_scores[self.games_played]
        else:
            val = league_scores_from_import_stats(self.positions, self.stats, self.games_played)
            self.memoize_gp_league_scores[self.games_played] = val
            return val
        # if category == LeagueCategory.GOAL:
        #   return float(self.stats[ImportCategory.GOAL])
        # if category == LeagueCategory.ASSIST:
        #   return float(self.stats[ImportCategory.ASSIST])
        # if category == LeagueCategory.PLUS_MINUS:
        #   return float(self.stats[ImportCategory.PLUS_MINUS])
        # if category == LeagueCategory.PENALTY_MINUTES:
        #   return float(self.stats[ImportCategory.PENALTY_MINUTES])
        # if category == LeagueCategory.POWER_PLAY_POINT:
        #   return float(self.stats[ImportCategory.POWER_PLAY_GOAL]) + \
        #       float(self.stats[ImportCategory.POWER_PLAY_ASSIST])
        # if category == LeagueCategory.SHOT:
        #   return float(self.stats[ImportCategory.SHOT])
        # if category == LeagueCategory.WIN:
        #   return float(self.stats[ImportCategory.WIN])
        # if category == LeagueCategory.GOALS_AGAINST_AVERAGE:
        #   return float(self.stats[ImportCategory.GOALS_AGAINST_AVERAGE])
        #
        # if Position.GOALIE in self.positions:
        #     if category == LeagueCategory.WIN:
        #       return float(self.stats[ImportCategory.WIN])
        #     if category == LeagueCategory.SHUT_OUT:
        #       return float(self.stats[ImportCategory.SHUT_OUT])
        #     if category == LeagueCategory.SAVE_PERCENTAGE:
        #       return (float(self.stats[ImportCategory.GOALS_AGAINST]) /
        #               float(self.stats[ImportCategory.SAVES]))
        # else:
        #     # This is a player, we return 0.0 for all goalie stats.
        #     return 0.0

    def __repr__(self):
        return '"' + self.name() + ' ' + self.team + '"'