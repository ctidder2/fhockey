from random import choice, shuffle

from draft_sim import simulate_draft
from enums import LeagueCategory, Position
from league import LeagueSettings
from roto_importer import create_players_from_projections
from strategies.random_strategy import RandomPickStrategy
from strategies.points_heavy import PointsHeavyStrategy
from team import Team

NUM_WEEKS = 27
NUM_GAMES_PER_WEEK = 3

Y_LEAGUE_SETTINGS = LeagueSettings(
    num_teams=12,
    categories=[
        LeagueCategory.GOAL,
        LeagueCategory.ASSIST,
        LeagueCategory.PLUS_MINUS,
        LeagueCategory.PENALTY_MINUTES,
        LeagueCategory.POWER_PLAY_POINT,
        LeagueCategory.SHOT,
        LeagueCategory.WIN,
        LeagueCategory.GOALS_AGAINST_AVERAGE,
        LeagueCategory.SAVE_PERCENTAGE,
        LeagueCategory.SHUT_OUT,
    ],
    playable_per_position=[
        (Position.CENTER, 2),
        (Position.LEFT_WING, 2),
        (Position.RIGHT_WING, 2),
        (Position.DEFENSEMEN, 4),
        (Position.GOALIE, 2),
    ],
    bench_size=4
)

def init_teams(players, league_settings):
    """Returns a list of teams (initialized Strategy objects)."""
    teams = []
    strategy_types = [PointsHeavyStrategy, RandomPickStrategy]
    for id in xrange(league_settings.num_teams):
        strategy_type = choice(strategy_types)
        teams.append(Team(id, strategy_type(id, players, league_settings)))

    return teams

def _create_round_robin(team_ids):
    """Create a full schedule for each team to play each team.
    Credit: ih84ds on github.
    """
    s = []
    n = len(team_ids)
    map = list(range(n))
    mid = n // 2
    for i in range(n-1):
        l1 = map[:mid]
        l2 = map[mid:]
        l2.reverse()
        round = []
        for j in range(mid):
            t1 = team_ids[l1[j]]
            t2 = team_ids[l2[j]]
            round.append((t1, t2))
        s.append(round)
        # rotate list by n/2, leaving last element at the end
        map = map[mid:-1] + map[:mid] + map[-1:]
    return s

def set_league_schedule(team_ids):
    weekly_matchups = []
    while len(weekly_matchups) < NUM_WEEKS:
        rr = _create_round_robin(team_ids)
        shuffle(rr)
        weekly_matchups.extend(rr)
    return weekly_matchups[:NUM_WEEKS]

def sim_week():
    # TODO
    pass

league_settings = Y_LEAGUE_SETTINGS
players = create_players_from_projections()
teams = init_teams(players, league_settings)
teams_map = {team.id : team for team in teams}
simulate_draft(teams, players, league_settings)
weekly_matchups = set_league_schedule(teams_map.keys())
