from collections import defaultdict
from league import YLeagueSettings
from roto_importer import create_players_from_projections
from strategy import RandomPickStrategy

NUM_TEAMS = 12
NUM_ROUNDS = 16

def init_teams(players, league_settings):
    """Returns a list of teams (initialized Strategy objects)."""
    teams = []
    for id in xrange(NUM_TEAMS):
        teams.append(RandomPickStrategy(id, players, league_settings))

    return teams

def notify_all_teams_of_pick(teams, team_id, player):
    """Send a notification to each team (strategy) of a pick made."""
    for team in teams:
        team.notify(team_id, player)

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
    rosters = defaultdict(list)

    for picking_team_id in draft_order:
        picked_player = teams[picking_team_id].pick(available_players)

        if not picked_player in available_players:
            raise ValueError(
                "Team %s tried to pick player %s that was not available. ",
                teams[picking_team_id],
                picked_player
            )

        available_players.remove(picked_player)
        drafted_players.append(picked_player)
        rosters[picking_team_id].append(picked_player)
        notify_all_teams_of_pick(teams, picking_team_id, picked_player)
    return rosters

rosters = simulate_draft()
for i, roster in enumerate(rosters.iteritems()):
    print i, roster[1]
