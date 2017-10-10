from random import random

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
        if import_stats[ImportCategory.SAVES] > 0:
            scores[LeagueCategory.SAVE_PERCENTAGE] = (
                float(import_stats[ImportCategory.GOALS_AGAINST]) /
                (float(import_stats[ImportCategory.GOALS_AGAINST] + import_stats[ImportCategory.SAVES])))
        else:
            scores[LeagueCategory.SAVE_PERCENTAGE] = 0.0
        if import_stats[ImportCategory.SAVES] > 0:
            scores[LeagueCategory.GOALS_AGAINST_AVERAGE] = float(import_stats[ImportCategory.GOAL]) / float(num_games)
        else:
            scores[LeagueCategory.GOALS_AGAINST_AVERAGE] = float("inf")
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

    def simulate_games(self, num_games=3):
        import_cats = {cat: 0 for cat in self.stats.keys()}
        fractions = 12
        for _ in xrange(num_games * fractions ):
            period_cat_scores = self._simulate_half_period()
            for cat, score in period_cat_scores.iteritems():
                import_cats[cat] += score
        if Position.GOALIE in self.positions:
            import_cats[ImportCategory.WIN] = (
                1 if (self.stats[ImportCategory.WIN] /
                      float(self.games_played) < random()) else 0
            )
            import_cats[ImportCategory.SHUT_OUT] = (
                1 if (self.stats[ImportCategory.SHUT_OUT] /
                      float(self.games_played) < random()) else 0
            )
        return import_cats


    def _simulate_half_period(self):
        simmed_stats = {}
        if Position.GOALIE in self.positions:
            # Handle Goalie stats.
            saves = (float(self.stats[ImportCategory.SAVES]) /
                     (self.games_played * 3.0) * random())
            simmed_stats[ImportCategory.SAVES] = saves
            simmed_stats[ImportCategory.GOALS_AGAINST] = (
                1 if self.gaa_given_saves() * saves < random() else 0
            )
        else:
            # Handle Player stats.
            for imp_cat, val in self.stats.iteritems():
                if imp_cat in {ImportCategory.ASSIST,
                               ImportCategory.HIT,
                               ImportCategory.SHOT,
                               ImportCategory.BLOCK,
                               ImportCategory.PENALTY_MINUTES}:
                    m = float(val) / (82.0 * 6.0)
                    m /= 2 if imp_cat == ImportCategory.PENALTY_MINUTES else 1
                    simmed_stats[imp_cat] = 1 if m > random() else 0
                if (imp_cat == ImportCategory.SHOT and
                    simmed_stats[imp_cat] > 0):
                    # If we shot, did we score?
                    simmed_stats[ImportCategory.GOAL] = (
                        1 if self.score_chance_for_shot() > random() else 0
                    )
                    if simmed_stats[ImportCategory.GOAL] == 1:
                        # If we scored, was it on the power-play?
                        simmed_stats[ImportCategory.POWER_PLAY_GOAL] = (
                            1 if self.ppg_for_goal() > random() else 0
                        )
                elif (imp_cat == ImportCategory.ASSIST and
                      simmed_stats[imp_cat] == 1):
                    # Was the assist on the power play?
                    simmed_stats[ImportCategory.POWER_PLAY_ASSIST] = (
                        1 if self.ppa_for_assist() > random() else 0
                    )
                # TODO(handle +/-)

        return simmed_stats

    def gaa_given_saves(self):
        return (self.stats[ImportCategory.GOALS_AGAINST] /
                float(self.stats[ImportCategory.SAVES]))

    def ppg_for_goal(self):
        return (self.stats[ImportCategory.POWER_PLAY_GOAL] /
                float(self.stats[ImportCategory.GOAL]))

    def ppa_for_assist(self):
        return (self.stats[ImportCategory.POWER_PLAY_ASSIST] /
                float(self.stats[ImportCategory.ASSIST]))

    def score_chance_for_shot(self):
        return (self.stats[ImportCategory.GOAL] /
                float(self.stats[ImportCategory.SHOT]))

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

    def __repr__(self):
        return '"' + self.name() + ' ' + self.team + '"'