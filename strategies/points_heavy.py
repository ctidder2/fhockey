from strategies.strategy import Strategy
from random import sample

class PointsHeavyStrategy(Strategy):
    """This strategy will select the people with the highest amount of points
        projected remaining.
    """

    def __init__(self, team_id, players_available, league_settings):
        self.players_available = set(players_available)
        self.team_id = team_id
        self.league_settings = league_settings


    def notify(self, team_id, player):
        """When a team makes a pick in the draft,
           this function is called with that team and player."""
        self.players_available.remove(player)

    def pick(self, players_remaining):
        """Chooses a player from the set of players_remaining.

            Args:
                players_remaining: set. representing players available to pick.
        """
        player_to_pick = sample(players_remaining, 1)[0]

        for player in players_remaining:
            if player_to_pick.get_points() < player.get_points():
                player_to_pick = player
        return player_to_pick