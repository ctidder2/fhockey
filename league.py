from enums import LeagueCategory, Position

class LeagueSettings:

    def __init__(self, num_teams, categories, playable_per_position, bench_size):
        """

        :param num_teams: int, number of teams in the league
        :param categories: list of categories that count for scoring
        :param playable_per_position: list of tuples,
            first entry is the Position and the second is the number at that position
        :param bench_size: int, number of players allowed to be kept on the bench
        """
        self.categories = categories
        self.num_teams = num_teams
        self.playable_per_position = playable_per_position
        self.bench_size = bench_size

YLeagueSettings = LeagueSettings(
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