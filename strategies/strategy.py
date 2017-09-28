class Strategy:
    """Base class for a strategy. Strategies must implement these functions."""

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
