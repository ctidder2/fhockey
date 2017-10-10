from random import choice, shuffle
from collections import defaultdict
from itertools import chain

from draft_sim import simulate_draft
from enums import LeagueCategory, Position
from league import LeagueSettings
from player import league_scores_from_import_stats
from roto_importer import create_players_from_projections
from strategies.additional_strategy import AdditionalValueStrategy
from strategies.points_heavy import PointsHeavyStrategy
from strategies.random_strategy import RandomPickStrategy
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
    strategy_types = [PointsHeavyStrategy, RandomPickStrategy, AdditionalValueStrategy]
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

league_settings = Y_LEAGUE_SETTINGS
players = create_players_from_projections()
teams = init_teams(players, league_settings)
teams_map = {team.id : team for team in teams}
simulate_draft(teams, players, league_settings)
for team in teams:
    print team, team.roster

def team_score(team_id, num_games=3):
    imp_cats_vals = defaultdict(float)
    for player in teams_map[team_id].roster:
        for imp_cat, val in player.simulate_games(num_games).iteritems():
            imp_cats_vals[imp_cat] += val
    goalie_scores = league_scores_from_import_stats([Position.GOALIE],
                                                    imp_cats_vals,
                                                    num_games=3)
    player_scores = league_scores_from_import_stats([],  # Non-Goalie
                                                    imp_cats_vals,
                                                    num_games=3)
    return {cat: score for cat, score in chain(goalie_scores.iteritems(),
                                               player_scores.iteritems())}


def sim_matchup(team_1_id, team_2_id):
    scoreboard = {
        team_1_id: [0,0,0],
        team_2_id: [0,0,0],
    }

    team_1_score = team_score(team_1_id)
    team_2_score = team_score(team_2_id)

    for cat in league_settings.categories:
        if team_1_score[cat] == team_2_score[cat]:
            scoreboard[team_1_id][2] += 1
            scoreboard[team_2_id][2] += 1
        elif (team_1_score > team_2_score and
            cat != LeagueCategory.GOALS_AGAINST_AVERAGE):
            scoreboard[team_1_id][0] += 1
            scoreboard[team_2_id][1] += 1
        else:
            scoreboard[team_1_id][1] += 1
            scoreboard[team_2_id][0] += 1
    return scoreboard


def sim_week(matchups):
    matchup_scores = []
    for matchup in matchups:
        matchup_scores.append(sim_matchup(matchup[0], matchup[1]))
    return matchup_scores

standings = {team_id : [0,0,0] for team_id in teams_map.keys()}
weekly_matchups = set_league_schedule(teams_map.keys())
weekly_results = []
for week in weekly_matchups:
    weekly_results.append(sim_week(week))
    for scoreboard in weekly_results[-1]:
        for team_id, score in scoreboard.iteritems():
            record = standings[team_id]
            for i in xrange(2):
                record[i] += score[i]
            standings[team_id] = record

sorted_standings = sorted(standings.iteritems(), key=lambda x: (x[1][0], x[1][2]), reverse=True)

win_pct = {}
for team_id, record in sorted_standings:
    win_pct[team_id] = (record[0] + record[2] / 2.0) / 206.0
    print "%f.3" % win_pct[team_id], str(teams_map[team_id]), record

