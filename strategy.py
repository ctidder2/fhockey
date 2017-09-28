from random import choice

class Strategy:

    def __init__(self, players_available):
        """Players available is a list of players available to the draft."""
        pass

    def notify(self, f_team, player):
        """When a team makes a pick in the draft,
           this function is called with that team and player."""
        pass

    def pick(self, remaining_players):
        """Make a selection of the remaining players."""
        pass

class RandomPickStrategy(Strategy):

    def __init__(self, players_available, team_id):
        self.players_available = set(players_available)
        self.team_id = team_id


    def notify(self, team_id, player):
        """When a team makes a pick in the draft,
           this function is called with that team and player."""
        self.players_available.remove(player)

    def pick(self, players_remaining):
        """Chooses a player from the set of players_remaining.

            Args:
                players_remaining: set. representing players available to pick.
        """
        return choice(list(players_remaining))
