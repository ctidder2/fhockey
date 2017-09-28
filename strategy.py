from random import choice

class Strategy:

    def __init__(self, team_id, players_available, league_settings):
        """Object used to determine what players to pick.

        :param team_id: int this strategies team id
        :param players_available: list of players_available for the draft
        :param league_settings a LeagueSettings object
        """
        pass

    def notify(self, f_team, player):
        """When a team makes a pick in the draft,
           this function is called with that team and player."""
        pass

    def pick(self, remaining_players):
        """Make a selection of the remaining players."""
        pass

class RandomPickStrategy(Strategy):

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
        return choice(list(players_remaining))
