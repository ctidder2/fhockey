class LeagueCategory:
    """Categories used by leagues for scoring."""
    GOAL = 0
    ASSIST = 1
    PLUS_MINUS = 2
    PENALTY_MINUTES = 3
    POWER_PLAY_POINT = 4
    SHOT = 5
    WIN = 6
    GOALS_AGAINST_AVERAGE = 7
    SAVE_PERCENTAGE = 8
    SHUT_OUT = 9

GOALIE_CATEGORIES = frozenset([
    LeagueCategory.WIN,
    LeagueCategory.SHUT_OUT,
    LeagueCategory.SAVE_PERCENTAGE,
    LeagueCategory.GOALS_AGAINST_AVERAGE])

class ImportCategory:
    """Categories found in raw data."""
    GOAL = 0
    ASSIST = 1
    PLUS_MINUS = 2
    PENALTY_MINUTES = 3
    POWER_PLAY_GOAL = 4
    POWER_PLAY_ASSIST = 5
    SHORT_HANDED_GOAL = 6
    SHORT_HANDED_ASSIST = 7
    SHOT = 8
    HIT = 9
    BLOCK = 10
    GAME_WINNING_GOAL = 11
    WIN = 12
    SHUT_OUT = 13
    GOALS_AGAINST = 14
    SAVES = 15
    GOALS_AGAINST_AVERAGE = 16
    SAVE_PERCENTAGE = 17

class Position:
    CENTER = 0
    LEFT_WING = 1
    RIGHT_WING = 2
    DEFENSEMEN = 3
    GOALIE = 4