import csv
from enums import SkaterCategory
from enums import Position
from player import Player

def skip_header(projections_reader):
    """Rotodumped csv files have 3 files with no player info."""
    projections_reader.next()
    projections_reader.next()
    projections_reader.next()

_row_pos_to_skater_cat = {
    4: SkaterCategory.GOAL,
    5: SkaterCategory.ASSIST,
    6: SkaterCategory.PLUS_MINUS,
    7: SkaterCategory.PENALTY_MINUTES,
    8: SkaterCategory.POWER_PLAY_GOAL,
    9: SkaterCategory.POWER_PLAY_ASSIST,
    10: SkaterCategory.SHORT_HANDED_GOAL,
    11: SkaterCategory.SHORT_HANDED_ASSIST,
    12: SkaterCategory.SHOT,
    13: SkaterCategory.HIT,
    14: SkaterCategory.BLOCK,
    15: SkaterCategory.GAME_WINNING_GOAL,
    17: SkaterCategory.WIN,
    20: SkaterCategory.SHUT_OUT,
    21: SkaterCategory.GOALS_AGAINST,
    22: SkaterCategory.SAVES,
    23: SkaterCategory.GOALS_AGAINST_AVERAGE,
}

_pos_str_to_pos_enum = {
    'C': Position.CENTER,
    'LW': Position.LEFT_WING,
    'RW': Position.RIGHT_WING,
    'D': Position.DEFENSEMEN,
    'G': Position.GOALIE,
}

def create_players_from_projections(f='projections.csv'):
    players = []
    with open(f, 'r') as projections_file:
        projections_reader = csv.reader(projections_file, delimiter=',', quotechar='"')
        skip_header(projections_reader)

        for i, row in enumerate(projections_reader):
            last_name, first_name = row[0].split(', ')
            player = Player(first_name, last_name)

            player.team = row[1]
            player.positions.append(_pos_str_to_pos_enum[row[2]])
            player.games_played = row[3]

            for pos, cat in _row_pos_to_skater_cat.iteritems():
                player.stats[cat] = row[pos]

            players.append(player)
    return players

print create_players_from_projections()[0].stats