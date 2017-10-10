import csv
from enums import ImportCategory, Position
from player import Player

def skip_header(projections_reader):
    """Rotodumped csv files have 3 files with no player info."""
    projections_reader.next()
    projections_reader.next()
    projections_reader.next()

_row_pos_to_skater_cat = {
    4: ImportCategory.GOAL,
    5: ImportCategory.ASSIST,
    6: ImportCategory.PLUS_MINUS,
    7: ImportCategory.PENALTY_MINUTES,
    8: ImportCategory.POWER_PLAY_GOAL,
    9: ImportCategory.POWER_PLAY_ASSIST,
    10: ImportCategory.SHORT_HANDED_GOAL,
    11: ImportCategory.SHORT_HANDED_ASSIST,
    12: ImportCategory.SHOT,
    13: ImportCategory.HIT,
    14: ImportCategory.BLOCK,
    15: ImportCategory.GAME_WINNING_GOAL,
    17: ImportCategory.WIN,
    20: ImportCategory.SHUT_OUT,
    21: ImportCategory.GOALS_AGAINST,
    22: ImportCategory.SAVES,
    23: ImportCategory.GOALS_AGAINST_AVERAGE,
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
            player.games_played = float(row[3])

            for pos, cat in _row_pos_to_skater_cat.iteritems():
                player.stats[cat] = float(row[pos])

            players.append(player)
    return players
