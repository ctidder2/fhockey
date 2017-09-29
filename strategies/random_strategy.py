from random import choice
from strategies.strategy import Strategy

class RandomPickStrategy(Strategy):

    def notify(self, team_id, player):
        self.players_available.remove(player)

    def pick(self, players_remaining):
        return choice(list(players_remaining))
