from collections import defaultdict
from random import choice

from league import YLeagueSettings
from roto_importer import create_players_from_projections
from strategies.random_strategy import RandomPickStrategy
from strategies.points_heavy import PointsHeavyStrategy
from team import Team

NUM_TEAMS = 12
NUM_ROUNDS = 16

def init_teams(players, league_settings):
    """Returns a list of teams (initialized Strategy objects)."""
    teams = []
    strategy_types = [PointsHeavyStrategy, RandomPickStrategy]
    for id in xrange(NUM_TEAMS):
        strategy_type = choice(strategy_types)
        teams.append(Team(id, strategy_type(id, players, league_settings)))

    return teams

def notify_all_teams_of_pick(teams, team_id, player):
    """Send a notification to each team (strategy) of a pick made."""
    for team in teams:
        team.draft_strategy.notify(team_id, player)

def set_draft_order():
    """Returns a list representing order of team ids to pick."""
    forwards = range(NUM_TEAMS)
    backwards = list(reversed(forwards))

    draft_order = []
    for i in xrange(NUM_ROUNDS):
        draft_order.extend(backwards if i % 2 else forwards)
    return draft_order

def simulate_draft():
    players = create_players_from_projections()
    teams = init_teams(players, YLeagueSettings)
    draft_order = set_draft_order()

    available_players = set(players)
    drafted_players = []

    for picking_team_id in draft_order:
        picked_player = teams[picking_team_id].draft_strategy.pick(available_players)

        if not picked_player in available_players:
            raise ValueError(
                "Team %s tried to pick player %s that was not available. ",
                teams[picking_team_id],
                picked_player
            )

        available_players.remove(picked_player)
        drafted_players.append(picked_player)
        teams[picking_team_id].add_to_roster(picked_player)
        notify_all_teams_of_pick(teams, picking_team_id, picked_player)
    return teams
