from enums import LeagueCategory, GOALIE_CATEGORIES, Position
from strategies.strategy import Strategy
from collections import defaultdict
from random import sample

_league_cat_weight = {
    LeagueCategory.GOAL : 1.0,
    LeagueCategory.ASSIST : 1.0,
    LeagueCategory.PLUS_MINUS : 1.0,
    LeagueCategory.PENALTY_MINUTES : 1.0,
    LeagueCategory.POWER_PLAY_POINT : 1.0,
    LeagueCategory.SHOT : 1.0,
    LeagueCategory.WIN : 0.5,
    LeagueCategory.GOALS_AGAINST_AVERAGE : 0.5,
    LeagueCategory.SAVE_PERCENTAGE : 0.5,
    LeagueCategory.SHUT_OUT : 0.5,
}

ceiling_weight = 1.5

class AdditionalValueStrategy(Strategy):
    """This strategy will select the people with highest additional value
        according to category scores.
    """

    def __init__(self, team_id, players_available, league_settings):
        """Object used to determine what players to pick.

        :param team_id: int this strategies team id
        :param players_available: list of players_available for the draft
        :param league_settings a LeagueSettings object
        """
        Strategy.__init__(self, team_id, players_available, league_settings)
        self.category_scores = defaultdict(float)
        self.category_max_scores = self.compute_category_max_scores()

    def notify(self, team_id, player):
        self.players_available.remove(player)
        if team_id == self.team_id:
            for category in self.league_settings.categories:
                self.category_scores[category] += player.get_category_score().get(category, 0.0)

    def pick(self, players_remaining):
        player_to_pick = sample(players_remaining, 1)[0]

        for player in players_remaining:
            if self.get_player_value(player_to_pick) < \
                self.get_player_value(player):
                player_to_pick = player
        return player_to_pick

    def get_player_value(self, player):
        score = 0
        for category in self.league_settings.categories:
            score += self.get_category_addtional_value(player, category) * \
                _league_cat_weight[category]
        return score

    def get_category_addtional_value(self, player, category):
        score = self.category_scores[category]
        maximum = self.category_max_scores[category]

        new_score = score + float(player.get_category_score().get(category, 0.0))
        if new_score > maximum:
            new_score = maximum

        delta_score = new_score - score
        if delta_score < 0:
            delta_score = 0

        return delta_score / maximum if maximum > 0 else 0

    def compute_category_max_scores(self):
        category_max_scores = defaultdict(float)
        player_to_score_cats = {player: player.get_category_score() for player in self.players_available}
        for category in self.league_settings.categories:
            max_num_players = 0
            is_goalie_category = category in GOALIE_CATEGORIES
            for position, count in self.league_settings.playable_per_position:
                if position == Position.GOALIE and is_goalie_category:
                    max_num_players += count
                elif position != Position.GOALIE and not is_goalie_category:
                    max_num_players += count

            scores = [player_to_score_cats[player].get(category, 0.0) for player in self.players_available]
            scores.sort(reverse=True)
            scores = scores[:max_num_players*self.league_settings.num_teams]
            category_max_scores[category] = sum(scores)*ceiling_weight/self.league_settings.num_teams
        return category_max_scores