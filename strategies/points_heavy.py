from strategies.strategy import Strategy
from random import sample

class PointsHeavyStrategy(Strategy):
    """This strategy will select the people with the highest amount of points
        projected remaining.
    """

    def notify(self, team_id, player):
        self.players_available.remove(player)

    def pick(self, players_remaining):
        player_to_pick = sample(players_remaining, 1)[0]

        for player in players_remaining:
            if player_to_pick.get_points() < player.get_points():
                player_to_pick = player
        return player_to_pick